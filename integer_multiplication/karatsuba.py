# We use list repr
# We could use bytes (array of ints, indexer passes out int objects of ascii values 0-255),
# str (array of codepoints, indexer passes out str objects), ???

# TODO: better 'split number' representation
# The below todo will make everything so much easier, but we need an ADT for that (I am new to Python)
# TODO: Represent integer numbers as a vector of 0-9 single digits from least to most significant digit (reverse order).


# recursive function
# See also https://github.com/python/cpython/blob/6f2a8c08573c71b78d2f6e2bfaf31641a0cd092b/Objects/longobject.c#L102
def karatsuba_multiplication(xs, ys):
    nx = len(xs)
    ny = len(ys)

    # ensure the same number of digits in both lists, and the number of
    # digits must be a power of 2 (1, 2, 4, 8, ...)
    if nx > ny:
        n = power_of_two(nx)
    else:
        n = power_of_two(ny)

    xs = pad(xs, n - nx)
    ys = pad(ys, n - ny)

    # recursive algorithm
    if n == 1:
        # base case
        c, r = single_digit_multiplication(xs[0], ys[0])
        return [c, r]
        # This this NOT necessary
        # if c > 0:
        #     return [c, r]
        # else:
        #     return [r]
    else:
        m = n // 2
        a = xs[:m]  # head m digits of x
        b = xs[m:]  # tail m digits of x
        c = ys[:m]  # do for y
        d = ys[m:]  # do for y
        # build up the recursive tree calling ourselves (recursively)
        ac = karatsuba_multiplication(a, c)
        bd = karatsuba_multiplication(b, d)
        p = addition(a, b)
        q = addition(c, d)
        pq = karatsuba_multiplication(p, q)
        # traverse up the recursive tree using the non-recursive formula
        ad_bc = subtraction(subtraction(pq, ac), bd)
        return addition(addition(power(ac, n), power(ad_bc, m)), bd)


# The algorithm requires n-digit numbers, where n is the power of 2 (otherwise the decomposition
# and pow calls must be modified)
def power_of_two(n):
    r = 1
    while r < n:
        r *= 2
    return r


# addition (this performs 2n primitive operations by definition in the textbook that is counted by "Big O")
def subtraction(xs, ys):
    ix = len(xs) - 1
    iy = len(ys) - 1
    rs = []
    borrow = 0
    while True:
        more_x = ix >= 0
        more_y = iy >= 0

        if more_x and more_y:
            x = xs[ix]
            y = ys[iy]
        elif more_x:
            x = xs[ix]
            y = 0
        elif more_y:
            x = 0
            y = ys[iy]
        else:
            # never append borrow, result must be positive
            if borrow != 0:
                raise Exception("The result must be positive.")
            break

        d, borrow = single_digit_subtraction(x, y, borrow)
        rs.append(d)

        ix -= 1
        iy -= 1

    # remove trailing zeros
    while len(rs) > 0 and rs[-1] == 0:
        rs.pop()

    return list(reversed(rs))


# primitive subtraction (this is a primitive operation by definition in the textbook) that is counted by "Big O"
def addition(xs, ys):
    ix = len(xs) - 1
    iy = len(ys) - 1
    rs = []
    carry = 0
    while True:
        more_x = ix >= 0
        more_y = iy >= 0

        if more_x and more_y:
            x = xs[ix]
            y = ys[iy]
        elif more_x:
            x = xs[ix]
            y = 0
        elif more_y:
            x = 0
            y = ys[iy]
        else:
            # append carry
            if carry > 0:
                rs.append(carry)
            break

        carry, d = single_digit_addition(x, y, carry)
        rs.append(d)

        ix -= 1
        iy -= 1

    # remove trailing zeros
    while len(rs) > 0 and rs[-1] == 0:
        rs.pop()

    return list(reversed(rs))


def power(xs, n):
    rs = list(xs)
    while n > 0:
        rs.append(0)
        n -= 1
    return rs


def pad(xs, n):
    if n == 0:
        return xs
    rs = []
    while n > 0:
        rs.append(0)
        n -= 1
    for x in xs:
        rs.append(x)
    return rs


def single_digit_multiplication(x, y):
    return convert_to_pair(x * y)


def single_digit_addition(x, y, carry):
    return convert_to_pair(x + y + carry)


def single_digit_subtraction(x, y, borrow):
    r = x - y - borrow
    if r >= 0:
        return r, 0
    else:
        return 10 + r, 1


# convert number to (single-digit) carry and (single-digit) remainder
def convert_to_pair(x):
    # // is integer division operator
    return x // 10, x % 10


def book_example():
    # test case with 64 digit numbers
    xs = [1, 2, 3, 4]  # x = 1234
    ys = [5, 6, 7, 8]  # y = 5679
    result = karatsuba_multiplication(xs, ys)
    if result == [7, 0, 0, 6, 6, 5, 2]:
        print("Success")
    else:
        print("Failure")


def test_case():
    result = karatsuba_multiplication([9, 9, 9, 9, 9], [9, 9, 9, 9])
    if result == [9, 9, 9, 8, 9, 0, 0, 0, 1]:
        print("test case succeeded")
    else:
        print("test case failed")


def convert_to_list(s):
    r = []
    for d in s[::-1]:
        r.append(int(d))
    return r


def convert_to_string(xs):
    s = ""
    for d in xs:
        s += str(d)
    return s


def problem_1_6():
    # 64 digit numbers
    x = "3141592653589793238462643383279502884197169399375105820974944592"
    y = "2718281828459045235360287471352662497757247093699959574966967627"
    xs = convert_to_list(x)
    ys = convert_to_list(y)
    result = karatsuba_multiplication(xs, ys)
    s = convert_to_string(result)
    print(f"The result is {s}")


def main():
    book_example()
    test_case()
    problem_1_6()


if __name__ == '__main__':
    # if len(sys.argv) >= 2:
    #     main(sys.argv[1])
    # else:
    main()
