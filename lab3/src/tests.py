from time import process_time
from random import choices
import matplotlib.pyplot as plt
from copy import deepcopy

from algorithms import *


def create_best_array(n):
    arr = []
    for i in range(n):
        arr.append(i)

    return arr


def create_worst_array(n):
    arr = [2000000]
    for i in range(n):
        arr.append(n - i)

    return arr


def create_random_array(n):
    arr = choices(range(-10000, 10000), k=n)

    return arr


def create_user_array(n):
    arr = []
    for i in range(n):
        arr.append(int(input('Введите элемент массива: ')))

    return arr


def measure_one_sort_time(func, arr):
    start_time = process_time()
    func(arr)

    return process_time() - start_time


def measure_all_sorts_time(create_array, n_start, n_end, n_step, iterations):
    arr_sizes = range(n_start, n_end + 1, n_step)

    bubble_array_time = []
    insert_array_time = []
    select_array_time = []

    for n in arr_sizes:
        t = 0
        for i in range(iterations):
            arr = create_array(n)
            t += measure_one_sort_time(bubble_sort, arr)

        bubble_array_time.append(t / iterations)

        t = 0
        for i in range(iterations):
            arr = create_array(n)
            t += measure_one_sort_time(insertion_sort, arr)

        insert_array_time.append(t / iterations)

        t = 0
        for i in range(iterations):
            arr = create_array(n)
            t += measure_one_sort_time(bucket_sort, arr)

        select_array_time.append(t / iterations)

        print(n)

    return bubble_array_time, insert_array_time, select_array_time


def print_table(arr_sizes, result):
    for i in range(len(arr_sizes)):
        print(str(arr_sizes[i]), end='')
        for sort_time in result:
            print(' & ' + str(sort_time[i]), end='')
        print(r' \\')
        print(r'\hline')


def time_visualization():
    n_start, n_end, n_step = 100, 1000, 100
    iterations = 100
    arr_sizes = range(n_start, n_end + 1, n_step)

    result1 = measure_all_sorts_time(create_best_array, n_start, n_end + 1, n_step, iterations)
    print_table(arr_sizes, result1)
    result2 = measure_all_sorts_time(create_worst_array, n_start, n_end + 1, n_step, iterations)
    print_table(arr_sizes, result2)
    result3 = measure_all_sorts_time(create_random_array, n_start, n_end + 1, n_step, iterations)
    print_table(arr_sizes, result3)

    for result in (result1, result2, result3):
        fig1 = plt.figure(figsize=(10, 7))
        plot = fig1.add_subplot()
        plot.plot(arr_sizes, result[0], label="Сортировка пузырьком")
        plot.plot(arr_sizes, result[1], label="Сортировка вставками", marker="o")
        plot.plot(arr_sizes, result[2], label="Блочная сортировка", marker="X")
        plt.legend()
        plt.grid()
        plt.title("Временные характеристики алгоритмов сортировки")
        plt.ylabel("Затраченное время (с)")
        plt.xlabel("Длина")

    plt.show()


def test_outputs(create_array, n):
    if n == 0:
        print("Массив пуст")
        return

    arr = create_array(n)
    init_arr = deepcopy(arr)

    print()
    print("Начальный массив:          ", arr)
    print("Ожидаемый результат:       ", sorted(init_arr))
    init_arr = deepcopy(arr)
    print("---------------------------")
    print("Сортировка пузырьком:      ", bubble_sort(init_arr))
    init_arr = deepcopy(arr)
    print("Сортировка вставками:      ", insertion_sort(init_arr))
    init_arr = deepcopy(arr)
    print("Блочная сортировка:        ", bucket_sort(init_arr))


time_visualization()
# test_outputs(create_random_array, 10)
