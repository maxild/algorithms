import os
import random


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


# noinspection PyUnusedLocal
def choose_pivot_first(l, h):
    return l


# noinspection PyUnusedLocal
def choose_pivot_last(l, h):
    return h - 1


def choose_pivot_randomly(l, h):
    return random.randint(l, h - 1)


# NOTE: get better performance for (nearly) sorted arrays (also reverse sorted arrays)
def choose_pivot_median_of_three(xs, l, h):
    # NOTE: for 2 elements we just replicate the last element
    m = (l + h - 1) // 2  # NOTE: For an equal number of elements we pick the left-most of the 2 middle indices
    ys = [xs[l], xs[m], xs[h - 1]]
    indices = [l, m, h - 1]
    insertion_sort(ys, indices)
    return indices[1]


# insertion sort hard coded to 3 elem list/array
def insertion_sort(xs, perm):
    if xs[1] < xs[0]:
        xs[1], xs[0] = xs[0], xs[1]
        perm[1], perm[0] = perm[0], perm[1]
    if xs[2] < xs[1]:
        xs[2], xs[1] = xs[1], xs[2]
        perm[2], perm[1] = perm[1], perm[2]
        if xs[1] < xs[0]:
            xs[1], xs[0] = xs[0], xs[1]
            perm[1], perm[0] = perm[0], perm[1]


# < 0  means LT
# == 0 means EQ
# > 0 means GT
def numeric_compare(x, y):
    return x - y


# TODO: Instrument partition with performance counter (see problem)
# Partition the range(l, h) == l..h-1
# in-place swapping (mutation) of elements such that the array is partitioned into 3 parts
#   1. sub-array before the pivot element (with all elements less than the pivot)
#   2. pivot element
#   3. sub-array after the pivot element (with all elements greater than the pivot)
# returns the index of the pivot element, which describes the partition
# NOTE: a linear scan partitions all elements except the pivot
# INVARIANT:
#   * All elements between the pivot xs[l] and j are less than the pivot: l+1..j
#   * All elements between j and i are greater than the pivot: j+1..h-1
def partition(xs, l, h, p):
    # normalize pivot index to left-most element (element zero in the current sub-array)
    if p > l:
        xs[l], xs[p] = xs[p], xs[l]

    j = l + 1  # the index of the left-most element in the second sub-array
    for i in range(l + 1, h):
        # we swap any element less than the pivot with the left-most element in the second sub-array (enforce INVARIANT)
        if xs[i] < xs[l]:
            # NOTE: if j == i (because we haven't seen any bigger elements) we are doing redundant swaps
            xs[i], xs[j] = xs[j], xs[i]
            j += 1

    # swap the pivot into the correct index
    # NOTE: If all elements are bigger than the pivot (j-1 == l) we are doing a redundant swap
    xs[l], xs[j - 1] = xs[j - 1], xs[l]

    # report final pivot position (index)
    return j - 1


# This partition sub-routine is not elegant (and my own invention)
def my_partition(xs, p):
    # normalize pivot index to zero
    if p > 0:
        xs[0], xs[p] = xs[p], xs[0]
    pval = xs[0]
    i = 1
    j = len(xs) - 1

    while True:
        if j - i + 1 <= 0:
            break

        if xs[i] < pval:
            i += 1
        elif xs[j] < pval:
            xs[i], xs[j] = xs[j], xs[i]
            i += 1
            j -= 1

        if j - i + 1 <= 0:
            break

        if xs[j] > pval:
            j -= 1
        elif xs[i] > pval:
            xs[i], xs[j] = xs[j], xs[i]
            i += 1
            j -= 1

    # swap pivot and last i-element
    xs[0], xs[i - 1] = xs[i - 1], xs[0]

    return i - 1


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
