# We start by using list of list representation for matrix in Python
# Later this code would benefit for using NymPy matrix representation
#
# NOTE: We could use nested tuples!!! tuples have (len, indexer, pattern-matching/destructuring/unpacking etc)
#
# from numpy import matrix
# from numpy import linalg
# A = matrix( [[1,2,3],[11,12,13],[21,22,23]]) # Creates a matrix.
# x = matrix( [[1],[2],[3]] )                  # Creates a matrix (like a column vector).
# y = matrix( [[1,2,3]] )                      # Creates a matrix (like a row vector).
# print A.T                                    # Transpose of A.
# print A*x                                    # Matrix multiplication of A and x.
# print A.I                                    # Inverse of A.
# print linalg.solve(A, x)                     # Solve the linear equation system.

# pretty print module not used anymore
# from pprint import pprint as pp

# NOTE: We work with matrices of integers!!!!


# noinspection PyPep8Naming
def matrix_dimensions(A):
    n = len(A)
    assert all(map(lambda row: len(row) == n, A))
    if n > 0:
        return n, len(A[0])
    else:
        return n, 0


# noinspection PyPep8Naming
def ensure_equal_square_dimensions(A, B):
    n1, m1 = matrix_dimensions(A)
    n2, m2 = matrix_dimensions(B)
    if n1 != n2 or m1 != m2 or n1 != n2:
        raise Exception('The two matrices are not square with the same number of rows/columns.')
    return n1


# noinspection PyPep8Naming
def ensure_equal_dimensions(A, B):
    n1, m1 = matrix_dimensions(A)
    n2, m2 = matrix_dimensions(B)
    # same number of rows and columns in both matrices
    if n1 != n2 or m1 != m2:
        raise Exception('The two matrices do not have the same number of rows/columns.')
    return n1, m1


# noinspection PyPep8Naming
def ensure_equal_dimensions4(A, B, C, D):
    n1, m1 = matrix_dimensions(A)
    n2, m2 = matrix_dimensions(B)
    n3, m3 = matrix_dimensions(C)
    n4, m4 = matrix_dimensions(D)
    # same number of rows and columns in all 4 matrices
    if n1 != n2 or n2 != n3 or n3 != n4 or m1 != m2 or m2 != m3 or m3 != m4:
        raise Exception('The four matrices do not have the same number of rows/columns.')
    return n1, m1


# Brute-force iterative algorithm
# noinspection PyPep8Naming
def matrix_multiply_bruteforce(X, Y):
    n = ensure_equal_square_dimensions(X, Y)
    C = []
    for i in range(n):
        C.append([0] * n)
        for j in range(n):
            # C[i][j] = 0
            for k in range(n):
                C[i][j] += X[i][k] * Y[k][j]
    return C


# Simple recursive function (divide and conquer)
# noinspection PyPep8Naming
def matrix_multiply_simple(X, Y):
    n = ensure_equal_square_dimensions(X, Y)
    assert n > 0  # because of padding
    if n <= 1:
        # base case
        return [[X[0][0] * Y[0][0]]]
    else:
        A, B, C, D, pad = split_matrix(X)
        E, F, G, H, pad = split_matrix(Y)
        # simple combination using 8 recursive calls
        AE = matrix_multiply_simple(A, E)
        BG = matrix_multiply_simple(B, G)
        AF = matrix_multiply_simple(A, F)
        BH = matrix_multiply_simple(B, H)
        CE = matrix_multiply_simple(C, E)
        DG = matrix_multiply_simple(D, G)
        CF = matrix_multiply_simple(C, F)
        DH = matrix_multiply_simple(D, H)
        # simple combination
        R11 = matrix_addition(AE, BG)
        R12 = matrix_addition(AF, BH)
        R21 = matrix_addition(CE, DG)
        R22 = matrix_addition(CF, DH)
        # combine the 4 matrices
        return combine_matrix(R11, R12, R21, R22, pad)


# Recursive function (divide and conquer)
# noinspection PyPep8Naming
def matrix_multiply_strassen(X, Y):
    n = ensure_equal_square_dimensions(X, Y)
    assert n > 0  # because of padding
    if n <= 1:
        # base case
        return [[X[0][0] * Y[0][0]]]
    else:
        A, B, C, D, pad = split_matrix(X)
        E, F, G, H, pad = split_matrix(Y)
        # 10 additions and subtractions
        FH = matrix_subtraction(F, H)
        AB = matrix_addition(A, B)
        CD = matrix_addition(C, D)
        GE = matrix_subtraction(G, E)
        AD = matrix_addition(A, D)
        EH = matrix_addition(E, H)
        BD = matrix_subtraction(B, D)
        GH = matrix_addition(G, H)
        AC = matrix_subtraction(A, C)
        EF = matrix_addition(E, F)
        # 7 recursive calls
        P1 = matrix_multiply_strassen(A, FH)
        P2 = matrix_multiply_strassen(AB, H)
        P3 = matrix_multiply_strassen(CD, E)
        P4 = matrix_multiply_strassen(D, GE)
        P5 = matrix_multiply_strassen(AD, EH)
        P6 = matrix_multiply_strassen(BD, GH)
        P7 = matrix_multiply_strassen(AC, EF)
        # strassen combination
        R11 = matrix_add3_subtract1(P4, P5, P6, P2)
        R12 = matrix_addition(P1, P2)
        R21 = matrix_addition(P3, P4)
        R22 = matrix_add2_subtract2(P1, P5, P3, P7)
        # combine the 4 matrices
        return combine_matrix(R11, R12, R21, R22, pad)


# Divide step into 4 matrices of same square size
# If the dimension is even, they are split in half as described.
# If the dimension is odd, zero padding by one row and one column is applied first.
# noinspection PyPep8Naming
def split_matrix(X):
    n, m = matrix_dimensions(X)
    # Assert square matrix
    assert n == m
    # 199 x 199 are divided into 100x100, 100x99, 99x100, 99x99, where all 99 dimensions are padded with zeros
    ln = (n + 1) // 2
    lm = (m + 1) // 2
    assert ln == lm
    # pad = 0 or 1, and for pad == 1 we need to pad a single zero
    padN = 2 * ln - n
    padM = 2 * lm - m
    assert padN == padM
    # We handle odd number of rows/columns by padding with zeros such that A,B,C,D all have same size
    # divide both matrices into 4 distinct matrix-slices, that are all (n/2 x n/2) in dimension
    A = [X[i][:lm] for i in range(ln)]
    B = [pad_col(X[i][lm:], padM) for i in range(ln)]  # pad col
    C = pad_row([X[i][:lm] for i in range(ln, n)], padN, ln)  # pad row
    D = pad_row([pad_col(X[i][lm:], padM) for i in range(ln, n)], padN, ln)  # pad row and col
    return A, B, C, D, padN


def pad_col(xs, pad):
    if pad > 0:
        xs.append(0)
    return xs


def pad_row(xs, pad, l):
    if pad > 0:
        xs.append([0] * l)
    return xs


# Combine step
# NOTE: The code require all 4 matrices to be square and of same size
# NOTE: We remove padding using pad indicator value
# noinspection PyPep8Naming
def combine_matrix(A, B, C, D, pad):
    # compose the 4 distinct slices into one matrix
    l: int = len(A)
    # we have to remove padding again here
    X = matrix(2 * l - pad, 2 * l - pad)
    for i in range(l):
        for j in range(l):
            X[i][j] = A[i][j]
    for i in range(l):
        for j in range(l-pad):
            X[i][j + l] = B[i][j]
    for i in range(l-pad):
        for j in range(l):
            X[i + l][j] = C[i][j]
    for i in range(l-pad):
        for j in range(l-pad):
            X[i + l][j + l] = D[i][j]
    return X


# noinspection PyPep8Naming
def matrix(n, m):
    A = []
    for i in range(n):
        A.append([0] * m)
    return A


# Theta(n**2) or Theta(n*m)
# noinspection PyPep8Naming
def matrix_addition(A, B):
    n, m = ensure_equal_dimensions(A, B)
    R = []
    for i in range(n):
        R.append([0] * m)
        for j in range(m):
            R[i][j] = A[i][j] + B[i][j]
    return R


# Theta(n**2) or Theta(n*m)
# noinspection PyPep8Naming
def matrix_subtraction(A, B):
    n, m = ensure_equal_dimensions(A, B)
    R = []
    for i in range(n):
        R.append([0] * m)
        for j in range(m):
            R[i][j] = A[i][j] - B[i][j]
    return R


# noinspection PyPep8Naming
def matrix_add3_subtract1(A, B, C, D):
    n, m = ensure_equal_dimensions4(A, B, C, D)
    R = []
    for i in range(n):
        R.append([0] * m)
        for j in range(m):
            R[i][j] = A[i][j] + B[i][j] + C[i][j] - D[i][j]
    return R


# noinspection PyPep8Naming
def matrix_add2_subtract2(A, B, C, D):
    n, m = ensure_equal_dimensions4(A, B, C, D)
    R = []
    for i in range(n):
        R.append([0] * m)
        for j in range(m):
            R[i][j] = A[i][j] + B[i][j] - C[i][j] - D[i][j]
    return R


# noinspection PyPep8Naming
def print_matrix(A):
    # end='' implies no newline
    print('[', end='')
    for i, row in enumerate(A):
        if i > 0:
            print(' ', end='')  # indent with single space
        print(row, end='')
        if i < len(A) - 1:
            print()  # print newline
    print(']')


# noinspection PyPep8Naming
def main():
    X = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 1], [3, 4, 5, 1, 2], [4, 5, 1, 2, 3], [5, 1, 2, 3, 4]]
    # X = [[1, 2], [3, 4]]
    print('X + X')
    print_matrix(matrix_addition(X, X))
    print('X - X')
    print_matrix(matrix_subtraction(X, X))
    print('X * X =    (bruteforce)')
    print_matrix(matrix_multiply_bruteforce(X, X))
    print('X * X =    (simple)')
    print_matrix(matrix_multiply_simple(X, X))
    print('X * X =    (strassen)')
    print_matrix(matrix_multiply_strassen(X, X))
    print('tests')
    A, B, C, D, pad = split_matrix(X)
    Y = combine_matrix(A, B, C, D, pad)
    print('Y')
    print_matrix(Y)


if __name__ == '__main__':
    main()
