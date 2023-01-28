from time import process_time_ns
import numpy as np
import matplotlib.pyplot as plt
from algorithms import ant_algorithm, full_search


def read_file_matrix(file_name):
    file = open("data/" + file_name, "r")
    size = len(file.readline().split())
    file.seek(0)

    matrix = [[0] * size for _ in range(size)]

    i = 0
    for line in file.readlines():
        j = 0
        for num in line.split():
            matrix[i][j] = int(num)
            j += 1
        i += 1

    file.close()

    return matrix, size


def generate_matrix(size, spread=30):
    matrix = np.random.randint(1, spread, (size, size))

    for i in range(size):
        for j in range(size):
            if i == j:
                matrix[i][j] = 0
            elif j > i:
                matrix[i][j] = matrix[j][i]

    filename = "data/mtr.txt"
    f = open(filename, 'w')
    for i in range(size):
        for j in range(size):
            f.write(str(matrix[i][j]))
            f.write(" ")
        f.write("\n")

    f.close()


def demonstration():
    filename = input("Введите название файла с матрицей расстояний между городами: ")
    try:
        matrix, size = read_file_matrix(filename)
        print('=' * 100)
        print("Исходная матрица: ")
        for i in range(size):
            for j in range(size):
                print(matrix[i][j], end=" ")
            print()
        print('=' * 100)
        full_search(matrix, size)
        print('=' * 100)
        a = float(input("Введите параметр alpha: "))
        p = float(input("Введите коэффициент испарения феромона p: "))
        t_max = int(input("Введите максимальное число итераций t: "))
        print('=' * 100)
        ant_algorithm(matrix, size, a, 1 - a, p, t_max)
    except:
        print("Возникла ошибка ввода")


def time():
    a = 1
    b = 1
    p = 0.5
    t_max = 1000

    search = []
    ant_ = []
    X = range(2, 11, 1)
    for _size in X:
        generate_matrix(_size)
        matrix, size = read_file_matrix("mtr.txt")

        time_start = process_time_ns()
        full_search(matrix, size)
        search.append(process_time_ns() - time_start)

        time_start = process_time_ns()
        ant_algorithm(matrix, size, a, b, p, t_max)
        ant_.append(process_time_ns() - time_start)

    for i in range(len(search)):
        print(X[i], search[i], ant_[i])

    plt.plot(X, search, label="Полный перебор")
    plt.plot(X, ant_, label="Муравьиный алгоритм", marker="o")

    plt.xlabel("Размер матрицы", fontsize=14)
    plt.ylabel("Время, нс", fontsize=14)

    plt.grid(True)
    plt.legend()

    plt.show()


def check_params():
    filename = "mtr.txt"

    a_list = [0.1, 0.25, 0.5, 0.75, 0.9]
    p_list = [0.1, 0.25, 0.5, 0.75, 0.9]
    t_list = [100, 200, 300, 400, 500]

    generate_matrix(11, 10)
    matrix1, size1 = read_file_matrix(filename)

    generate_matrix(11, 1000)
    matrix2, size2 = read_file_matrix(filename)

    res1 = full_search(matrix1, size1)
    res2 = full_search(matrix2, size2)

    f = open("result.txt", "w")

    for t in t_list:
        for a in a_list:
            for p in p_list:
                f.write(str(a) + " & " + str(p) + " & " + str(t))
                ex1 = ant_algorithm(matrix1, size1, a, 1 - a, p, t)
                ex2 = ant_algorithm(matrix2, size2, a, 1 - a, p, t)
                f.write(" & " + str(ex1 - res1) + " & " + str(ex2 - res2) + " \\ " + "\n\hline\n")

    f.close()


demonstration()
