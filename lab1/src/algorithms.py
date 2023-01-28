import string
import random

DEBUG = True


def lowenstein_dist_matrix(str1, str2):
    str1 = ' ' + str1
    str2 = ' ' + str2
    n = len(str1)
    m = len(str2)
    matrix = [[0] * m for _ in range(n)]

    for i in range(1, n):
        matrix[i][0] = i
    for j in range(1, m):
        matrix[0][j] = j

    for i in range(1, n):
        for j in range(1, m):
            insert = matrix[i][j - 1] + 1
            delete = matrix[i - 1][j] + 1
            replace = matrix[i - 1][j - 1] + int(str1[i] != str2[j])

            matrix[i][j] = min(insert, delete, replace)

    if DEBUG:
        print_dist_matrix(matrix)

    return matrix[n - 1][m - 1]


def damerau_lowenstein_dist_matrix(str1, str2):
    str1 = ' ' + str1
    str2 = ' ' + str2
    n = len(str1)
    m = len(str2)
    matrix = [[0] * m for _ in range(n)]

    for i in range(1, n):
        matrix[i][0] = i
    for j in range(1, m):
        matrix[0][j] = j

    for i in range(1, n):
        for j in range(1, m):
            insert = matrix[i][j - 1] + 1
            delete = matrix[i - 1][j] + 1
            replace = matrix[i - 1][j - 1] + int(str1[i] != str2[j])
            if (i > 1 and j > 1) and (str1[i] == str2[j - 1] and str1[i - 1] == str2[j]):
                xchange = matrix[i - 2][j - 2] + 1
                matrix[i][j] = min(insert, delete, replace, xchange)
            else:
                matrix[i][j] = min(insert, delete, replace)

    if DEBUG:
        print_dist_matrix(matrix)

    return matrix[n - 1][m - 1]


def damerau_lowenstein_dist_recursion(str1, str2):
    n = len(str1)
    m = len(str2)

    if n == 0 or m == 0:
        return n + m

    insert = damerau_lowenstein_dist_recursion(str1, str2[:-1]) + 1
    delete = damerau_lowenstein_dist_recursion(str1[:-1], str2) + 1
    replace = damerau_lowenstein_dist_recursion(str1[:-1], str2[:-1]) + int(str1[-1] != str2[-1])

    if (n > 1 and m > 1) and (str1[-1] == str2[-2] and str1[-2] == str2[-1]):
        xchange = damerau_lowenstein_dist_recursion(str1[:-2], str2[:-2]) + 1
        return min(insert, delete, replace, xchange)
    else:
        return min(insert, delete, replace)


def damerau_lowenstein_dist_recursion_cash(str1, str2):

    def recursion(str1, str2, matrix):
        len1 = len(str1)
        len2 = len(str2)

        if len1 == 0 or len2 == 0:
            matrix[len1][len2] = len1 + len2
        else:
            # insert
            if matrix[len1][len2 - 1] == -1:
                recursion(str1, str2[:-1], matrix)
            # delete
            if matrix[len1 - 1][len2] == -1:
                recursion(str1[:-1], str2, matrix)
            # replace
            if matrix[len1 - 1][len2 - 1] == -1:
                recursion(str1[:-1], str2[:-1], matrix)

            if (len1 > 1 and len2 > 1) and (str1[-1] == str2[-2] and str1[-2] == str2[-1]):
                recursion(str1[:-2], str2[:-2], matrix)
                matrix[len1][len2] = min(matrix[len1][len2 - 1] + 1,
                                         matrix[len1 - 1][len2] + 1,
                                         matrix[len1 - 1][len2 - 1] + int(str1[-1] != str2[-1]),
                                         matrix[len1 - 2][len2 - 2] + 1)
            else:
                matrix[len1][len2] = min(matrix[len1][len2 - 1] + 1,
                                         matrix[len1 - 1][len2] + 1,
                                         matrix[len1 - 1][len2 - 1] + int(str1[-1] != str2[-1]))

        return

    n = len(str1) + 1
    m = len(str2) + 1
    matrix = [[-1 for _ in range(m)] for __ in range(n)]
    recursion(str1, str2, matrix)

    if DEBUG:
        print_dist_matrix(matrix)

    return matrix[n - 1][m - 1]


def print_dist_matrix(matrix):
    print('Матрица расстояний:')
    for line in matrix:
        print(line)


def random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def user_input():
    str1 = input('Введите строку 1: ')
    str2 = input('Введите строку 2: ')

    print(f'\nЛевенштейн, итерационный')
    answer = lowenstein_dist_matrix(str1, str2)
    print(f'Ответ: {answer}')

    print(f'\nДамерау-Левенштейн, итерационный')
    answer = damerau_lowenstein_dist_matrix(str1, str2)
    print(f'Ответ: {answer}')

    print(f'\nДамерау-Левенштейн, рекурсивный без кеша')
    answer = damerau_lowenstein_dist_recursion(str1, str2)
    print(f'Ответ: {answer}')

    print(f'\nДамерау-Левенштейн, рекурсивный с кешем')
    answer = damerau_lowenstein_dist_recursion_cash(str1, str2)
    print(f'Ответ: {answer}')

    print()


if __name__ == '__main__':
    while True:
        print('Выберите команду: \n'
              '1) ввод \n'
              '2) выход')
        mode = int(input('Ваш выбор: '))
        if mode == 2:
            break
        else:
            user_input()
