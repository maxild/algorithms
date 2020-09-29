# standard library imports
# import pathlib
# import sys
import os

# local imports (added as source root in pycharm)
# sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import (partition, choose_pivot_randomly, choose_pivot_median_of_three)


# from . import common


def sort_pivot_first(xs):
    ys = xs[:]
    comparisons = quick_sort(ys, 0, len(ys), 0, lambda zs, l, h: l)
    return ys, comparisons


def sort_pivot_last(xs):
    ys = xs[:]
    comparisons = quick_sort(ys, 0, len(ys), 0, lambda zs, l, h: h - 1)
    return ys, comparisons


def sort_pivot_median(xs):
    ys = xs[:]
    comparisons = quick_sort(ys, 0, len(ys), 0, lambda zs, l, h: choose_pivot_median_of_three(zs, l, h))
    return ys, comparisons


def sort_pivot_randomly(xs):
    ys = xs[:]
    comparisons = quick_sort(ys, 0, len(ys), 0, lambda zs, l, h: choose_pivot_randomly(l, h))
    return ys, comparisons


# We cannot use master method, because the partition is not balanced!!!
# We can strive for a balanced partition, and hope for a recursion something like
#    T(n) = 2 * T(n/2) + c*n
# I.e. Theta(n + log(n))
# NOTE: The partition sub-routine puts the pivot element in the correct place (INVARIANT that proofs the correctness)
def quick_sort(xs, l, h, count, pivot_fn):
    length = h - l
    if length <= 1:
        # base case: for singleton array we are done (no comparisons)
        return count
    else:
        # pivot_index = choose_pivot_first(l, h)
        # pivot_index = choose_pivot_last(l, h)
        # pivot_index = choose_pivot_randomly(l, h)
        # pivot_index = choose_pivot_median_of_three(xs, l, h)
        pivot_index = pivot_fn(xs, l, h)
        # Add the number of comparisons made by this recursive call in the following partition sub-routine
        count1 = count + length - 1
        p = partition(xs, l, h, pivot_index)
        # NOTE: The pivot (p) is excluded from the recursive calls
        count2 = quick_sort(xs, l, p, count1, pivot_fn)
        count3 = quick_sort(xs, p + 1, h, count2, pivot_fn)
        return count3


# < 0  means LT
# == 0 means EQ
# > 0 means GT
def numeric_compare(x, y):
    return x - y


def load_list(filename):
    script_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(script_path)
    filepath = os.path.join(dir_path, filename)
    xs = []
    with open(filepath) as fp:
        for number, line in enumerate(fp):
            xs.append(int(line))
            # print("Line {}: {}".format(number, line))
    return xs


def main():
    # data from the book website
    xs = load_list('problem5.6test2.txt')
    # arbitrary (non-sorted) list
    # xs = [3, 8, 2, 5, 1, 4, 7, 6]
    # sorted lists with wort case performance (7 + 6 + ... + 1 = 28 comparisons)
    # xs = [1, 2, 3, 4, 5, 6, 7, 8]
    # xs = [8, 7, 6, 5, 4, 3, 2, 1]
    # pivot_index = partition(xs, 0, len(xs), 0)
    # print(f'{xs} with pivot index {pivot_index}')

    sorted_xs, c = sort_pivot_first(xs)
    print(f'The {len(xs)}-element list have been sorted using {c} comparisons with the first element strategy.')
    sorted_xs, c = sort_pivot_last(xs)
    print(f'The {len(xs)}-element list have been sorted using {c} comparisons with the last element strategy.')
    sorted_xs, c = sort_pivot_median(xs)
    print(f'The {len(xs)}-element list have been sorted using {c} comparisons with the median element strategy.')
    sorted_xs, c = sort_pivot_randomly(xs)
    print(f'The {len(xs)}-element list have been sorted using {c} comparisons with the random element strategy.')


if __name__ == '__main__':
    main()
