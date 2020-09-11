def merge_sort(xs):
    l: int = len(xs)
    if l < 2:
        return xs
    else:
        m = l // 2
        xs_head = xs[:m]
        xs_tail = xs[m:]
        sorted_xs_head = merge_sort(xs_head)
        sorted_xs_tail = merge_sort(xs_tail)
        return merge(sorted_xs_head, sorted_xs_tail)


def merge(xs, ys):
    rs = []
    ix = 0
    iy = 0
    len_xs = len(xs)
    len_ys = len(ys)

    if ix >= len_xs:
        return ys
    else:
        x = xs[ix]

    if iy >= len_ys:
        return xs
    else:
        y = ys[iy]

    # NOTE: We have chosen to only perform one append, index-increment and stop-criteria per loop-iteration
    while True:
        if x < y:
            rs.append(x)
            ix += 1
            if ix >= len_xs:
                rs.extend(ys[iy:])
                break
            else:
                x = xs[ix]
        else:
            rs.append(y)
            iy += 1
            if iy >= len_ys:
                rs.extend(xs[ix:])
                break
            else:
                y = ys[iy]

    return rs

# Pseudo Code from the book for Merge
#
# C and D are sorted arrays (length n/2 each)
# B is the resulting sorted array (length n)
#
# i := 0  # C's index
# j := 0  # D's index
# for k := 0 to n-1 do
#    # C's exhausted thus fill up B with D
#    if C's length = i
#       B[k] := D[j]
#       j := j + 1
#    # D's exhausted thus fill up B with C
#    elif D's length = j
#       B[k] := D[i]
#       i := i + 1
#    elif C[i] < D[j]
#       B[k] := C[i]
#       i := i + 1
#    else
#       B[k] := D[j]
#       j := j + 1
#  return B

# Python 3 has no int.maxvalue because integers are not fixed sized. One can
# use sys.maxsize = 2**63 - 1 (signed 64-bit integer maxvalue). Minvalue is
# calculated as -2**63 = ~sys.maxsize, for same signed 64-bit integer.


def main():
    print(f'{merge_sort([3, 5, 7, 2, 8, 1, 4, 6])}')


if __name__ == "__main__":
    main()
