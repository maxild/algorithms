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


def main():
    print(f'{merge_sort([3, 5, 7, 2, 8, 1, 4, 6])}')


if __name__ == "__main__":
    main()
