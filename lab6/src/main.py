import pymorphy2
import re
from search import process_binary_search, load_csv


def get_planets_by_dist(planets_dist, type):
    res = []

    for planet in planets_dist.keys():
        if planets_dist[planet][type] > planets_dist[planet][type - 1] and \
           planets_dist[planet][type] > planets_dist[planet][type - 2]:
            res.append(planet)

    return res


def inv(a):
    return 1 - a


def special_not(planets_dist, type):
    res = []

    for planet in planets_dist.keys():
        if inv(planets_dist[planet][type]) > planets_dist[planet][type]:
            res.append(planet)
        planets_dist[planet][type] = inv(planets_dist[planet][type])

    return res


def special_very(planets_dist, type):
    res = []

    for planet in planets_dist.keys():
        if (planets_dist[planet][type])**2 > inv((planets_dist[planet][type])**2):
            res.append(planet)
        planets_dist[planet][type] = (planets_dist[planet][type]) ** 2

    return res


def main():
    morph = pymorphy2.MorphAnalyzer()

    question = input("Введите запрос: ")
    question_split = re.split(r'\W{1,}\s?', question)

    distance = [['ближний', 'близко', 'близкий', 'ближайший', 'ближнее', 'близкое', 'ближайшее', 'рядом', 'недалеко',
                'недалёкий'],
                ['средний', 'средне', 'среднее'],
                ['далёкий', 'дальний', 'далёкое', 'дальнее', 'далеко', 'неблизко', 'неблизкий']]

    res = -1
    special_words = []
    flag_planet = False
    flag_earth = False

    for word in question_split:
        n_form = morph.parse(word)[0].normal_form
        if n_form == 'планета':
            flag_planet = True
        if n_form == 'земля':
            flag_earth = True
        for i in range(3):
            if n_form in distance[i]:
                res = i
        if n_form == 'не':
            special_words.append('not')
        if n_form == 'очень':
            special_words.append('very')

    if not flag_planet or not flag_earth or res == -1:
        print("\nВопрос не распознан :(")
    else:
        planets = []

        planets_dist = {'Меркурий': [0, 0.6, 0.4], 'Венера': [1, 0, 0], 'Марс': [0.8, 0.2, 0],
                        'Юпитер': [0, 0.6, 0.4], 'Сатурн': [0, 0.4, 0.6], 'Уран': [0, 0, 1], 'Нептун': [0, 0, 1]}

        special_words.reverse()

        if not special_words:
            planets.extend(get_planets_by_dist(planets_dist, res))
        else:
            tmp_planets = []

            for i in special_words:
                tmp_planets = []
                if i == 'not':
                    tmp_planets.extend(special_not(planets_dist, res))
                elif i == 'very':
                    tmp_planets.extend(special_very(planets_dist, res))

            planets.extend(tmp_planets)

        print()
        print('Результаты:')
        global_dict = load_csv("planets.csv")
        for planet in planets:
            process_binary_search(global_dict, planet)


main()
