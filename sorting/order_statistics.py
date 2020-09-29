from common import (partition, choose_pivot_randomly)


# order is 1-based (1, 2, ..., n)
def rselect(xs, order):
    ys = xs[:]
    return random_select(ys, order - 1, 0, len(ys))


# This is a randomized algorithm with different (stochastic) recursion path on each execution
# index is 0-based
# NOTE: When we use a range(l, h), then the pivot index will always be the (zero-based) order of the entire array
def random_select(xs, index, l, h):
    p = choose_pivot_randomly(l, h)
    # calculate the position of the pivot
    pivot_index = partition(xs, l, h, p)
    if pivot_index == index:
        return xs[pivot_index]
    elif pivot_index > index:
        # search the first group of smaller elements l..p-1
        return random_select(xs, index, l, pivot_index)
    else:
        # search the second group of larger elements p+1,...,h-1
        return random_select(xs, index, pivot_index + 1, h)


# TODO: Implement DSelect
#   ChoosePivot
#       group/partition the array into n/5 sub-problems
#       insertion-sort each sub-problem and calculate the median
#       recursively call DSelect on the new (n/5)-element array of medians calculating the n/10 median
#   From here we follow rselect


def main():
    xs = [3, 7, 2, 8, 4, 1, 5, 6]
    order = 3
    print(f'The {order}. order statistics of {xs} is {rselect(xs, order)}')


if __name__ == '__main__':
    main()
