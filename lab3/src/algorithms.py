# Sorting algorithms

def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                
    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        x = arr[i]
        j = i - 1
        while j >= 0 and x < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = x

    return arr


def bucket_sort(arr):
    max_a = max(arr)
    min_a = min(arr)
    n = len(arr)
    size = (max_a - min_a) / n if (max_a - min_a) / n else 1

    buckets_list = []
    for x in range(n):
        buckets_list.append([])

    max_j = int(max_a / size)
    for i in range(n):
        j = n - max_j + int(arr[i] / size)
        if j != n:
            buckets_list[j].append(arr[i])
        else:
            buckets_list[n - 1].append(arr[i])

    arr = []
    for k in range(n):
        insertion_sort(buckets_list[k])
        arr = arr + buckets_list[k]

    return arr
