from algorithms import *
import pandas as pd
import matplotlib.pyplot as plt
from time import process_time


funcs = [[lowenstein_dist_matrix, 'lowenstein_dist_matrix'],
         [damerau_lowenstein_dist_matrix, 'damerau_lowenstein_dist_matrix'],
         [damerau_lowenstein_dist_recursion, 'damerau_lowenstein_dist_recursion'],
         [damerau_lowenstein_dist_recursion_cash, 'damerau_lowenstein_dist_recursion_cash']]

short_strings = [[length, random_string(length), random_string(length)] for length in range(0, 10, 1)]
long_strings = [[length, random_string(length), random_string(length)] for length in range(0, 201, 10)]

n_repeats = 20

time_file_short = 'time_short_str.xlsx'
time_file_long = 'time_long_str.xlsx'

filename_all = 'time_all.png'
filename_matr = 'time_w_matr.png'


def compare_long_strings_without_recursion():
    df_time = pd.DataFrame({'string_length': [x[0] for x in long_strings]})

    for i in range(len(funcs)):
        func, func_name = funcs[i]
        time_measures = []
        if i != 2:
            for string_length, string1, string2 in long_strings:
                start = process_time()
                for _ in range(n_repeats):
                    func(string1, string2)
                end = process_time()
                time = (end - start) / n_repeats
                time_measures.append(time)
            df_time[func_name] = time_measures

    df_time.to_excel(time_file_long)


def compare_short_strings_all():
    df_time = pd.DataFrame({'string_length': [x[0] for x in short_strings]})

    for func, func_name in funcs:
        time_measures = []
        for string_length, string1, string2 in short_strings:
            start = process_time()
            for _ in range(n_repeats):
                func(string1, string2)
            end = process_time()
            time = (end - start) / n_repeats
            time_measures.append(time)
        df_time[func_name] = time_measures

    df_time.to_excel(time_file_short)


def draw_plots_all():
    df = pd.read_excel(time_file_short)

    plt.grid()
    plt.xlabel('Длина строки')
    plt.ylabel('Время работы реализации алгоритма')

    plt.plot(df['string_length'], df['lowenstein_dist_matrix'], label='Левенштейн, итерационный')
    plt.plot(df['string_length'], df['damerau_lowenstein_dist_matrix'], linestyle='--',
             label='Дамерау-Левенштейн, итерационный')
    plt.plot(df['string_length'], df['damerau_lowenstein_dist_recursion'],
             label='Дамерау-Левенштейн, рекурсивный без кеша')
    plt.plot(df['string_length'], df['damerau_lowenstein_dist_recursion_cash'], linestyle='-.',
             label='Дамерау-Левенштейн, рекурсивный с кешем')

    plt.legend(loc='best')
    plt.savefig(filename_all)
    plt.gcf().clear()


def draw_plots_matr():
    df = pd.read_excel(time_file_long)

    plt.grid()
    plt.xlabel('Длина строки')
    plt.ylabel('Время работы реализации алгоритма')

    plt.plot(df['string_length'], df['lowenstein_dist_matrix'], label='Левенштейн, итерационный')
    plt.plot(df['string_length'], df['damerau_lowenstein_dist_matrix'], label='Дамерау-Левенштейн, итерационный')
    plt.plot(df['string_length'], df['damerau_lowenstein_dist_recursion_cash'],
             label='Дамерау-Левенштейн, рекурсивный с кешем')

    plt.legend(loc='best')
    plt.savefig(filename_matr)
    plt.gcf().clear()


if __name__ == '__main__':
    compare_short_strings_all()
    compare_long_strings_without_recursion()
    draw_plots_all()
    draw_plots_matr()
    