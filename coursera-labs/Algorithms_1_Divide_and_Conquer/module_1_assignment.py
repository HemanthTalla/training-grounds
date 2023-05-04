'''
Course: https://www.coursera.org/learn/algorithms-divide-conquer
Problem: Implementing Karatsuba Multiplication algorithm in Python3
Author: Hemanth Talla
'''

from math import ceil   
import logging

logging.basicConfig()

def splitNumberIntoTwo(num: int, split_index=None):
    '''
    This method splits a string (of a number, for our usecase) into two roughly equal halfs.
    Number is handled in string format to avoid losing leading zeros in some cases.
    '''
    number_string = str(num)
    number_of_digits = len(number_string)

    if number_of_digits % 2 != 0:
        number_string = '0' + number_string
        number_of_digits = len(number_string)
    
    list_of_digits = list(number_string)
    
    if split_index is None:
        mid_point = number_of_digits // 2
    else:
        mid_point = split_index
    
    #print(f'ns: {number_string} - ls: {list_of_digits} - mp: {mid_point}')

    left_half_string, right_half_string = map(
        ''.join, (list_of_digits[:mid_point], list_of_digits[mid_point:]))

    logging.debug(f'#sNIT[_A]: split: {mid_point} | split: {num} -> {left_half_string}, {right_half_string}')
    return (left_half_string, right_half_string)

def stripTrailingZeros(number):
        '''
        Removes trailing zeroes and return the remaining number and count of removed zeroes as tuple.
        If number contains only zeroes, then remaining number is returned as a zero for multiplication purpose. 
        '''
        number_length = len(number)
        stripped_number = number.rstrip('0')
        stripped_zero_count = number_length - len(stripped_number)
         
        if stripped_zero_count == number_length:
            stripped_number = '0'
        
        return (stripped_number, stripped_zero_count)


def karatsubaProduct(a, b):
    '''
    Main function that performs the karstsuba multiplication. 
    Karatsuba Multiplication Logic: https://en.wikipedia.org/wiki/Karatsuba_algorithm
    Any Trailing zeros are seperated from numbers and added back at end in order to reduce total number of operations.
    '''
    a, b = map(str, (a, b))
    
    # Handling Trailing Zeros
    zero_count = 0

    if a[-1] == '0':
        _a = a
        a, num_of_zeros = stripTrailingZeros(a)
        zero_count += num_of_zeros
        logging.debug(f'#kP[trailing-zeroes]: a: {_a} -> {a}, zeros: {num_of_zeros} ({zero_count})')

    if b[-1] == '0':
        _b = b
        b, num_of_zeros = stripTrailingZeros(b)
        zero_count += num_of_zeros
        logging.debug(f'#kP[trailing-zeroes]: b: {_b} -> {b}, zeros: {num_of_zeros} ({zero_count})')
    
    # BASE CASE - Direct multiplication when number is small enough
    MINIMUM_LENGTH = 2
    base_length = min(map(len, (a, b)))

    if base_length < MINIMUM_LENGTH:
        product_value = int(a) * int(b) * (10**zero_count)
        logging.info(f'#kP[base-case]:- a: {a}, b: {b} | base_length: {base_length} | zeros: {zero_count} | product: {product_value}')
        return product_value
    
    # Handling Leading Zeros
    len_a, len_b = map(len, (a, b))
    n = max(len_a, len_b)

    not_same_length = (len_a != len_b)
    not_even_length = (n % 2 != 0)

    logging.debug(f'#kP[leading-zeroes]:- n: {n}, a:{a}, b:{b} | {not_same_length}, {not_even_length}')


    if  not_same_length or not_even_length:

        n = n+1 if not_even_length else n

        _a, _b = a, b
        a = a.zfill(n)
        b = b.zfill(n)
        logging.debug(f'#kp[leading-zeroes]:- a: {_a} -> {a}, b: {_b} -> {b}')
    
    # RECURSION

    m = n//2 
    # 'm' could be any positive integer lesser than 'n'. 
    # 'm' being roughly half of 'n' gives us a balanced recursion tree.

    a1, a2 = splitNumberIntoTwo(a, split_index=m)
    b1, b2 = splitNumberIntoTwo(b, split_index=m)
    #print(f'#kP: (a1, a2: {a1}, {a2}), (b1, b2: {b1}, {b2})')

    x = karatsubaProduct(a1, b1)
    y = karatsubaProduct(int(a1) + int(a2), int(b1) + int(b2))
    z = karatsubaProduct(a2, b2)

    logging.debug(f'#kP[recursion]:- a: {a}, b: {b} | split: ({a1}, {a2}), ({b1}, {b2}) | m: {m} | x: {x}, y: {y}, z: {z} | zeros: {zero_count}')
    result = ((10**(2*m)) * x + (10**(m)) * (y - x - z) + z) * (10**zero_count)
    logging.info(f'#kP[recursion]:- Expression: ((10**{2*m}) * {x} + (10**{(m)}) * ({y - x - z}) + {z}) * (10**{zero_count}) | result: {result}')
    
    # DEBUG - Answer validation

    # goal = int(a)*int(b)*(10**zero_count)
    # logging.info(f'#kP[answer]: calc\'d: {result}\nactual: {goal} \nEqual: {result == goal}\n')

    return result


if __name__ == "__main__":

    # test-case-1
    m = 3141592653589793238462643383279502884197169399375105820974944592
    n = 2718281828459045235360287471352662497757247093699959574966967627

    # test-case-2
    # m, n = 234500, 2423203

    expected = str(f'{m*n:.0f}')
    answer = str(f'{karatsubaProduct(m, n):.0f}')

    print(f'Actual: {expected}\nCalc\'d: {answer}\nEqual: {answer == expected}')
