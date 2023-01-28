from random import shuffle, randint
import pandas as pd
from mimesis import Text


def generate_csv(filename):
    planets_df = pd.DataFrame(columns=['word', 'page'])

    text = Text('ru')

    words = ['Меркурий', 'Венера', 'Марс', 'Юпитер', 'Сатурн', 'Уран', 'Нептун', 'Земля',
             'Солнце', 'Астероид', 'Космонавт', 'Галактика', 'Луна', 'Звезда', 'Вселенная']

    random_words = text.words(quantity=1000)
    for i in range(len(random_words)):
        random_words[i] = random_words[i].title()

    words.extend(random_words)

    shuffle(words)

    for i in range(len(words)):
        planets_df = planets_df.append({'word': words[i], 'page': randint(1, 800)},
                                       ignore_index=True)

    planets_df.to_csv(filename, sep=',', index=False)


generate_csv('planets.csv')
