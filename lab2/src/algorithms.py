'''
    Алгоритмы умножения матриц
'''


def check_matrices_sizes(m1, n1, m2, n2):
    result = True
    if m1 == 0 or n1 == 0 or m2 == 0 or n2 == 0:
        result = False
    if n1 != m2:
        result = False

    return result


def get_correct_matrices_sizes(matr1, matr2):
    try:
        m1, n1 = len(matr1), len(matr1[0])
        m2, n2 = len(matr2), len(matr2[0])
    except:
        print("Данные введены некорректно")
        return

    check = check_matrices_sizes(m1, n1, m2, n2)
    if not check:
        print("Матрицы не могут быть перемножены из-за несоответствия размеров")
        return

    return m1, n1, n2


def standard_matrix_mult(matr1, matr2):
    sizes = get_correct_matrices_sizes(matr1, matr2)
    if not sizes:
        return
    else:
        m, n, q = sizes

    result_matr = [[0] * q for _ in range(m)]
    for i in range(m):
        for j in range(q):
            for k in range(n):
                result_matr[i][j] = result_matr[i][j] + matr1[i][k] * matr2[k][j]

    return result_matr


def vinograd_matrix_mult(matr1, matr2):
    sizes = get_correct_matrices_sizes(matr1, matr2)
    if not sizes:
        return
    else:
        m, n, q = sizes

    result_matr = [[0] * q for _ in range(m)]

    row = [0] * m
    for i in range(m):
        for j in range(n // 2):
            row[i] = row[i] + matr1[i][j * 2] * matr1[i][j * 2 + 1]

    col = [0] * q
    for i in range(q):
        for j in range(n // 2):
            col[i] = col[i] + matr2[j * 2][i] * matr2[j * 2 + 1][i]

    for i in range(m):
        for j in range(q):
            result_matr[i][j] = -row[i] - col[j]
            for k in range(n // 2):
                result_matr[i][j] = result_matr[i][j] + \
                                    (matr1[i][k * 2] + matr2[2 * k + 1][j]) * (matr1[i][2 * k + 1] + matr2[2 * k][j])

    if n % 2 == 1:
        for i in range(m):
            for j in range(q):
                result_matr[i][j] = result_matr[i][j] + matr1[i][n - 1] * matr2[n - 1][j]

    return result_matr


'''
    Оптимизации: 
    1) замена операции x = x + k на x += k;
    2) замена умножения на 2 на побитовый сдвиг;
    3) предвычисление слагаемых для алгоритма.
'''
def vinograd_matrix_mult_optimized(matr1, matr2):
    sizes = get_correct_matrices_sizes(matr1, matr2)
    if not sizes:
        return
    else:
        m, n, q = sizes

    result_matr = [[0] * q for _ in range(m)]

    row = [0] * m
    for i in range(m):
        for j in range(n // 2):
            row[i] += matr1[i][j << 1] * matr1[i][j << 1 + 1]

    col = [0] * q
    for i in range(q):
        for j in range(n // 2):
            col[i] += matr2[j << 1][i] * matr2[j << 1 + 1][i]

    for i in range(m):
        for j in range(q):
            tmp = -row[i] - col[j]
            for k in range(n // 2):
                tmp += (matr1[i][k << 1] + matr2[k << 1 + 1][j]) * \
                       (matr1[i][k << 1 + 1] + matr2[k << 1][j])
            result_matr[i][j] = tmp

    if n % 2 == 1:
        for i in range(m):
            for j in range(q):
                result_matr[i][j] += matr1[i][n - 1] * matr2[n - 1][j]

    return result_matr


def vinograd_matrix_mult_optimized(matr1, matr2):
    sizes = get_correct_matrices_sizes(matr1, matr2)
    if not sizes:
        return
    else:
        m, n, q = sizes

    result_matr = [[0] * q for _ in range(m)]

    n -= 1
    row = [0] * m
    for i in range(m):
        for j in range(0, n, 2):
            row[i] -= matr1[i][j] * matr1[i][j + 1]

    col = [0] * q
    for i in range(q):
        for j in range(0, n, 2):
            col[i] += matr2[j][i] * matr2[j + 1][i]

    for i in range(m):
        for j in range(q):
            result_matr[i][j] = row[i] - col[j]
            for k in range(0, n, 2):
                result_matr[i][j] += (matr1[i][k] + matr2[k + 1][j]) * (matr1[i][k + 1] + matr2[k][j])

    if n % 2 == 0:
        for i in range(m):
            for j in range(q):
                result_matr[i][j] += matr1[i][n] * matr2[n][j]

    return result_matr


def print_matrix(matr):
    if matr:
        for line in matr:
            print(line)


def user_input():
    print('Введите размеры первой матрицы')
    m1 = int(input('m1: '))
    n1 = int(input('n1: '))
    print('Введите первую матрицу построчно, через пробелы:')
    matr1 = []
    for i in range(m1):
        matr1.append(list(map(int, input().split())))
        if len(matr1[-1]) != n1:
            print('Ошибка при вводе матрицы')
            return
    print()

    print('Введите размеры второй матрицы')
    m2 = int(input('m2: '))
    n2 = int(input('n2: '))
    print('Введите вторую матрицу построчно, через пробелы')
    matr2 = []
    for i in range(m2):
        matr2.append(list(map(int, input().split())))
        if len(matr2[-1]) != n2:
            print('Ошибка при вводе матрицы')
            return
    print()

    return matr1, matr2


def init_input():
    matr1 = [[1, 2],
             [3, 4]]
    matr2 = [[1, 2, 3, 4],
             [2, 3, 4, 5]]

    return matr1, matr2


def count_mul(mode):
    if mode == 1:
        matr1, matr2 = user_input()
    elif mode == 2:
        matr1, matr2 = init_input()
    else:
        return

    print(f'\nСтандартный алгоритм')
    answer = standard_matrix_mult(matr1, matr2)
    print('Результат:')
    print_matrix(answer)

    print(f'\nАлгоритм Винограда')
    answer = vinograd_matrix_mult(matr1, matr2)
    print('Результат:')
    print_matrix(answer)

    print(f'\nОптимизированный алгоритм Винограда')
    answer = vinograd_matrix_mult_optimized(matr1, matr2)
    print('Результат:')
    print_matrix(answer)

    print()
    print()


if __name__ == '__main__':
    while True:
        print('Выберите режим: \n'
              '1) пользовательский ввод \n'
              '2) существующий пример \n'
              '3) выход')
        mode = int(input('Ваш выбор: '))
        if mode == 3:
            break
        else:
            count_mul(mode)
