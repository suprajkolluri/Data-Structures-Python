# -*- coding: utf-8 -*-
from numpy import *  # analysis:ignore

# STOCK_PRICES  = [100,113,110,85,105,102,86,63,81,101,94,106,101,79,94,90,97]
STOCK_PRICE_CHANGES = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]


def find_maximum_subarray_brute(A, low=0, high=-1):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Implement the brute force method from chapter 4
    time complexity = O(n^2)
    >>> STOCK_PRICE_CHANGES = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
    >>> find_maximum_subarray_brute(STOCK_PRICE_CHANGES, 0, 15)
    (7, 10)
    >>> ALL_NEGATIVES = [-4, -3, -5, -6, -2, -5]
    >>> find_maximum_subarray_brute(ALL_NEGATIVES, 0, 5)
    (4, 4)
    >>> ALL_POSITIVES = [1, 2, 3, 4, 5, 6]
    >>> find_maximum_subarray_brute(ALL_POSITIVES, 0, 5)
    (0, 5)
    """
    max_sum = A[0]
    for i in range(high):
        cur_sum = 0
        for j in range(i, high + 1):
            cur_sum = cur_sum + A[j]
            if cur_sum > max_sum:
                max_sum = cur_sum
                max_left = i
                max_right = j
    return max_left, max_right


def find_maximum_crossing_subarray(A, low, mid, high):
    """
    Find the maximum subarray that crosses mid
    Return a tuple (i,j) where A[i:j] is the maximum subarray
    """
    left_sum = A[mid]
    right_sum = A[mid + 1]
    max_left = mid
    max_right = mid + 1
    cur_sum = 0
    for i in range(mid, low - 1, -1):
        cur_sum = cur_sum + A[i]
        if cur_sum > left_sum:
            left_sum = cur_sum
            max_left = i
    cur_sum = 0
    for j in range(mid + 1, high + 1):
        cur_sum = cur_sum + A[j]
        if cur_sum > right_sum:
            right_sum = cur_sum
            max_right = j
    return max_left, max_right, left_sum + right_sum


def find_maximum_subarray_recursive(A, low=0, high=-1):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Recursive method from chapter 4
    >>> STOCK_PRICE_CHANGES = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
    >>> find_maximum_subarray_recursive(STOCK_PRICE_CHANGES, 0, 15)
    (7, 10, 43)
    >>> ALL_NEGATIVES = [-4, -3, -5, -6, -2, -5]
    >>> find_maximum_subarray_recursive(ALL_NEGATIVES, 0, 5)
    (4, 4, -2)
    >>> ALL_POSITIVES = [1, 2, 3, 4, 5, 6]
    >>> find_maximum_subarray_recursive(ALL_POSITIVES, 0, 5)
    (0, 5, 21)
    """
    if low == high:
        return low, high, A[low]
    else:
        mid = (low + high) / 2
        left_low, left_high, left_sum = find_maximum_subarray_recursive(A, low, mid)
        right_low, right_high, right_sum = find_maximum_subarray_recursive(A, mid + 1, high)
        cross_low, cross_high, cross_sum = find_maximum_crossing_subarray(A, low, mid, high)
        if left_sum >= right_sum and left_sum >= cross_sum:
            return left_low, left_high, left_sum
        elif right_sum >= left_sum and right_sum >= cross_sum:
            return right_low, right_high, right_sum
        else:
            return cross_low, cross_high, cross_sum


def find_maximum_subarray_iterative(A, low=0, high=-1):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Do problem 4.1-5 from the book.
    >>> STOCK_PRICE_CHANGES = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
    >>> find_maximum_subarray_iterative(STOCK_PRICE_CHANGES, 0, 15)
    (7, 10)
    >>> ALL_NEGATIVES = [-4, -3, -5, -6, -2, -5]
    >>> find_maximum_subarray_iterative(ALL_NEGATIVES, 0, 5)
    (4, 4)
    >>> ALL_POSITIVES = [1, 2, 3, 4, 5, 6]
    >>> find_maximum_subarray_iterative(ALL_POSITIVES, 0, 5)
    (0, 5)
    """
    max_left = 0
    max_right = 0
    cur_sum = 0
    final_sum = A[0]
    flag = 0
    for i in range(len(A)):
        cur_sum = cur_sum + A[i]
        if (cur_sum > final_sum):
            max_left = flag
            max_right = i
            final_sum = cur_sum
        if (cur_sum < 0):
            cur_sum = 0
            flag = i + 1
    return max_left, max_right


def square_matrix_multiply(A, B):
    """
    Return the product AB of matrix multiplication.
    >>> A = [[0, 1], [1, 1]]
    >>> B = [[1, 2], [2, 1]]
    >>> square_matrix_multiply(A, B)
    [[2, 1], [3, 3]]
    """
    A = asarray(A)
    B = asarray(B)
    assert A.shape == B.shape
    assert A.shape == A.T.shape
    C = [[0 for i in range(A.shape[0])] for j in range(A.shape[0])]
    for i in range(A.shape[0]):
        for j in range(A.shape[0]):
            C[i][j] = 0
            for k in range(A.shape[0]):
                C[i][j] = C[i][j] + A[i][k] * B[k][j]
    return C


def add(A, B):
    n = len(A)
    C = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C


def subtract(A, B):
    n = len(A)
    C = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C


def split_matrix(C, size):
    c11 = [[0 for i in range(size)] for j in range(size)]
    c12 = [[0 for j in range(size)] for i in range(size)]
    c21 = [[0 for j in range(size)] for i in range(size)]
    c22 = [[0 for j in range(size)] for i in range(size)]
    for i in range(size):
        for j in range(size):
            c11[i][j] = C[i][j]
            c12[i][j] = C[i][j + size]
            c21[i][j] = C[i + size][j]
            c22[i][j] = C[i + size][j + size]
    return c11, c12, c21, c22


def combine_matrix(c11, c12, c21, c22, size):
    n = size * 2
    C = [[0 for j in range(n)] for i in range(n)]
    for i in range(0, size):
        for j in range(0, size):
            C[i][j] = c11[i][j]
            C[i][j + size] = c12[i][j]
            C[i + size][j] = c21[i][j]
            C[i + size][j + size] = c22[i][j]

    return C


def square_matrix_multiply_strassens(A, B):
    """
    Return the product AB of matrix multiplication.
    Assume len(A) is a power of 2
    >>> A = [[0, 1], [1, 1]]
    >>> B = [[1, 2], [2, 1]]
    >>> square_matrix_multiply(A, B)
    [[2, 1], [3, 3]]
    """
    A = asarray(A)
    B = asarray(B)
    assert A.shape == B.shape
    assert A.shape == A.T.shape
    assert (len(A) & (len(A) - 1)) == 0, "A is not a power of 2"

    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]
    else:
        size = n / 2

    a11, a12, a21, a22 = split_matrix(A, size)
    b11, b12, b21, b22 = split_matrix(B, size)

    s1 = subtract(b12, b22)
    s2 = add(a11, a12)
    s3 = add(a21, a22)
    s4 = subtract(b21, b11)
    s5 = add(a11, a22)
    s6 = add(b11, b22)
    s7 = subtract(a12, a22)
    s8 = add(b21, b22)
    s9 = subtract(a11, a21)
    s10 = add(b11, b12)

    p1 = square_matrix_multiply_strassens(a11, s1)
    p2 = square_matrix_multiply_strassens(s2, b22)
    p3 = square_matrix_multiply_strassens(s3, b11)
    p4 = square_matrix_multiply_strassens(a22, s4)
    p5 = square_matrix_multiply_strassens(s5, s6)
    p6 = square_matrix_multiply_strassens(s7, s8)
    p7 = square_matrix_multiply_strassens(s9, s10)

    t1 = add(p5, p4)
    t2 = subtract(p6, p2)
    c11 = add(t1, t2)

    c12 = add(p1, p2)
    c21 = add(p3, p4)

    t3 = add(p5, p1)
    t4 = add(p3, p7)
    c22 = subtract(t3, t4)

    return combine_matrix(c11, c12, c21, c22, size)


def test():
    A = [[0, 1], [1, 1]]
    B = [[1, 2], [2, 1]]
    print "Max Sub Array Brute force Output: " + str(find_maximum_subarray_brute(STOCK_PRICE_CHANGES, 0, 15))
    print "Max Sub Array Recursive Output: " + str(find_maximum_subarray_recursive(STOCK_PRICE_CHANGES, 0, 15))
    print "Max Sub Array Iterative Output: " + str(find_maximum_subarray_iterative(STOCK_PRICE_CHANGES, 0, 15))
    print "Matrix Multiplication Output: " + str(square_matrix_multiply(A, B))
    print "Matrix Multiplication Output using Strassens method" + str(square_matrix_multiply(A, B))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    test()
