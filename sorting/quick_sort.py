# TODO: Do problem in the book where different ways of choosing pivot is measured w.r.t. perf/number of comparisons

def sort(xs):
    ys = xs[:]
    quick_sort(ys, 0, len(ys))
    return ys


# We cannot use master method, because the partition is not balanced!!!
# We can strive for a balanced partition, and hope for a recursion something like
#    T(n) = 2 * T(n/2) + c*n
# I.e. Theta(n + log(n))
# NOTE: The partition sub-routine puts the pivot element in the correct place (INVARIANT that proofs the correctness)
def quick_sort(xs, l, h):
    if h - l <= 1:
        # base case: for singleton array we are done
        return
    else:
        pivot_index = l  # TODO: choose pivot using strategy pattern
        m = partition(xs, l, h, pivot_index)
        # NOTE: The pivot (m) is excluded from the recursive calls
        quick_sort(xs, l, m)
        quick_sort(xs, m + 1, h)


# TODO: Instrument partition with performance counter (see problem)
# in-place swapping (mutation) of elements such that the array is partitioned into 3 parts
#   1. sub-array before the pivot element (with all elements less than the pivot)
#   2. pivot element
#   3. sub-array after the pivot element (with all elements greater than the pivot)
# returns the index of the pivot element, which describes the partition
# NOTE: a linear scan partitions all elements except the pivot
def partition(xs, l, h, p):
    # normalize pivot index to left-most element (element zero in the current sub-array)
    if p > l:
        xs[l], xs[p] = xs[p], xs[l]

    j = l + 1  # the index of the left-most element in the second sub-array
    for i in range(l + 1, h):
        # we swap any element less than the pivot with the left-most element in the second sub-array
        if xs[i] < xs[l]:
            # NOTE: if j == i (because we haven't seen any bigger elements) we are doing redundant swaps
            xs[i], xs[j] = xs[j], xs[i]
            j += 1

    # swap the pivot into the correct index
    # NOTE: If all elements are bigger than the pivot (j-1 == l) we are doing a redundant swap
    xs[l], xs[j - 1] = xs[j - 1], xs[l]

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


def main():
    xs = [3, 8, 2, 5, 1, 4, 7, 6]
    pivot_index = partition(xs, 0, len(xs), 0)
    print(f'{xs} with pivot index {pivot_index}')
    print(sort(xs))


if __name__ == '__main__':
    main()
