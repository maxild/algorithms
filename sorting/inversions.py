def count(xs):
    ys = xs[:]
    c = count_and_sort(ys, 0, len(ys))
    return c


def sort(xs):
    ys = xs[:]
    count_and_sort(ys, 0, len(ys))
    return ys


# In this python implementation we will sort the xs list in place
# p = first index
# q = one beyond last index
def count_and_sort(xs, p, q):
    if p >= q - 1:
        # base case: 0 or 1 element list is already sorted and contain zero inversions
        return 0
    else:
        m = (p + q) // 2  # first index in right part
        # sort the left and right part of xs
        count_left = count_and_sort(xs, p, m)
        count_right = count_and_sort(xs, m, q)
        # combine/merge the two sorted parts of the list
        count_split = merge_and_count_split_inversions(xs, p, m, q)

        return count_left + count_right + count_split


def merge_and_count_split_inversions(xs, p, m, q):
    n1 = m - p
    n2 = q - m
    # copy the two sub-lists
    left = xs[p:m]
    right = xs[m:q]
    i = 0
    j = 0
    c = 0
    for k in range(p, q):
        if i == n1:
            # left is exhausted
            xs[k] = right[j]
            j += 1
        elif j == n2:
            # right is exhausted
            xs[k] = left[i]
            i += 1
        elif left[i] <= right[j]:
            xs[k] = left[i]
            i += 1
        else:
            xs[k] = right[j]
            j += 1
            # the number of inversions are equal to the remaining elements in the left list
            c += n1 - i
    return c


def main():
    x = [1, 2, 3, 4, 5, 6]
    x
    number_of_inversions = count(x)
    print(number_of_inversions)
    print(sort(x))


if __name__ == '__main__':
    main()
