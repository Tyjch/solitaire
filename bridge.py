from solitaire import Card, SUITS, RANKS
from pprint import pprint
from bidict import bidict


def cards_values():
    dictionary = bidict()
    n = 1
    for suit in SUITS:
        for rank in RANKS:
            card = Card(suit, rank)
            dictionary[card] = n
            n += 1

    return dictionary






if __name__ == '__main__':
    result = cards_values()
    pprint(result)