from time import process_time
import matplotlib.pyplot as plt
from random import randint
import pandas as pd

from algorithms import *

time_file = 'table.xlsx'
filename_plots = 'plots.png'


def measure_time():
    standard_time = []
    vinograd_time = []
    vinograd_optimized_time = []

    mul_funcs = [standard_matrix_mult, vinograd_matrix_mult, vinograd_matrix_mult_optimized]
    time_lists = [standard_time, vinograd_time, vinograd_optimized_time]

    n_list = list(range(101, 1002, 100))

    for i in range(len(n_list)):
        print(i)
        n = n_list[i]
        n_repeats = 2 if i < 3 else 1

        matr1 = [[randint(0, 100)] * n for _ in range(n)]
        matr2 = [[randint(0, 100)] * n for _ in range(n)]

        for alg in range(3):
            time = 0
            for j in range(n_repeats):
                start = process_time()
                mul_funcs[alg](matr1, matr2)
                end = process_time()
                time += (end - start)
            time /= n_repeats
            time_lists[alg].append(time)

    df = pd.DataFrame({'N': n_list})
    df['standard'] = standard_time
    df['vinograd'] = vinograd_time
    df['vinograd_optimized'] = vinograd_optimized_time

    df.to_excel(time_file)


def draw_plots():
    df = pd.read_excel(time_file)

    plt.xlabel('Размерность матриц (n*n)')
    plt.ylabel('Время работы реализации (c)')
    plt.grid()

    plt.plot(df['N'], df['standard'], label='Стандартный')
    plt.plot(df['N'], df['vinograd'], label='Винограда')
    plt.plot(df['N'], df['vinograd_optimized'], label='Винограда, опт.')

    plt.legend(loc='best')
    plt.savefig(filename_plots)
    plt.gcf().clear()


if __name__ == '__main__':
    measure_time()
    draw_plots()
