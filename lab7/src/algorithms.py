from random import random
from itertools import permutations


def full_search(matrix, size):
    all_ways = permutations(range(size))
    best_way = []
    min_len = float("inf")
    for way in all_ways:
        way = list(way) + [way[0]]
        cur_len = 0
        for i in range(size):
            cur_len += matrix[way[i]][way[i + 1]]
        if cur_len < min_len:
            best_way = way
            min_len = cur_len

    print("ПОЛНЫЙ ПЕРЕБОР")
    print("Минимальный путь: ", best_way)
    print("Длина: ", min_len)

    return min_len


def calc_prob(p_numerator, cur_city, size, root):
    res_probs = []

    for i in range(size):
        if i in root:
            res_probs.append(0)
        else:
            cur_prob = p_numerator[cur_city][i]
            res_probs.append(cur_prob)

    sum_probs = sum(res_probs)

    if sum_probs:
        for i in range(size):
            res_probs[i] /= sum_probs

    return res_probs


def ant_iteration(matrix, eta, tau, size, a, b, q, p, best_way, min_len):
    p_numerator = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            p_numerator[i][j] = (eta[j][i] ** a) * (tau[j][i] ** b)

    delta_tau = [[0] * size for _ in range(size)]

    for i in range(size):
        way = [i]
        for j in range(size - 1):
            temp_probs = calc_prob(p_numerator, way[-1], size, way)
            prob = random()
            temp_sum = 0
            k = 0
            while k < size:
                if temp_probs[k] != 0:
                    temp_sum += temp_probs[k]
                    if temp_sum > prob:
                        break
                k += 1
            if k == size:
                k = size - 1
            way.append(k)

        way.append(way[0])

        cur_len = 0
        for x in range(len(way) - 1):
            cur_len += matrix[way[x]][way[x + 1]]

        if cur_len < min_len:
            best_way = way
            min_len = cur_len

        for v in range(size):
            delta_tau[way[v]][way[v + 1]] += q / cur_len

    for i in range(size):
        for j in range(size):
            tau[i][j] *= (1 - p)
            tau[i][j] += delta_tau[i][j]

    return tau, best_way, min_len


def ant_algorithm(matrix, size, a, b, p, time):
    q = 0
    for i in range(size):
        for j in range(i):
            if matrix[i][j] < float("inf"):
                q += matrix[i][j]

    eta = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(i):
            eta[i][j] = 1 / matrix[i][j]
            eta[j][i] = 1 / matrix[j][i]
    tau = [[0.2] * size for _ in range(size)]

    best_way = []
    min_len = float("inf")

    for t in range(time):
        tau, best_way, min_len = ant_iteration(matrix, eta, tau, size, a, b, q, p, best_way, min_len)

    print("МУРАВЬИНЫЙ АЛГОРИТМ")
    print("Минимальный путь: ", best_way)
    print("Длина: ", min_len)

    return min_len
