# problem 3.1
def fast_power(a, b):
    if b == 1:
        return a
    else:
        c = a * a
        d = b // 2
        ans = fast_power(c, d)
        if b % 2 > 0:
            return a * ans  # b is odd
        else:
            return ans      # b is even


def main():
    a = 2
    b = 7
    c = fast_power(a, b)
    print('{}^{} = {}'.format(a, b, c))


if __name__ == '__main__':
    main()
