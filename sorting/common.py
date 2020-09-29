import random


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
