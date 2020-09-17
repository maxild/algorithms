# find local maximum/peak via bruteforce iterations -- O(n)
def peak_finding_1d_bruteforce(xs):
    for i in range(1, len(xs) - 1):
        if xs[i - 1] <= xs[i] and xs[i] >= xs[i + 1]:
            return i
    return -1


def peak_finding_1d(xs):
    return peak_finding_1d_helper(xs, 0, len(xs))


# find peak in the range l, l+1,...,h-1 -- O(log n)
def peak_finding_1d_helper(xs, l: int, h: int):
    if l >= h:
        return -1
    else:
        m = (l + h) // 2  # middle index of range(l, h), where m-l=h-m such that we divide en equal halves
        if xs[m - 1] <= xs[m] and xs[m] >= xs[m + 1]:
            return m
        elif xs[m - 1] > xs[m]:
            # must be a peak before xs[m], i.e. in (l, l+1, ..., m-1) of length m-l
            return peak_finding_1d_helper(xs, l, m)
        # elif xs[m+1] > xs[m]:
        else:
            # must be a peak after xs[m], i.e. in (m, m+1, ..., h-1) of length h-m
            return peak_finding_1d_helper(xs, m, h)


# TODO: Create 2d peak finder using divide and conquer (find maximum on middle row and column, plus boundary, and
#       recurse on quadrant containing the maximum with the biggest neighbour). Only recurse if maximum is not a peak
#       (local maximum)

def main():
    xs = [1, 3, 4, 7, 12, 4, 5]
    # i = peak_finding_1d_bruteforce(xs)
    i = peak_finding_1d(xs)
    if i >= 0:
        print(f"Local maximum {xs[i]} found at index {i}.")
    else:
        print("No maximum")


if __name__ == '__main__':
    main()
