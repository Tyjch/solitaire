from bidict import bidict
from itertools import permutations
from pprint import pprint

cards_mapping = bidict({
        1 : ('A', 's'),
        2 : ('2', 's'),
        3 : ('3', 's'),
        4 : ('4', 's'),
        5 : ('5', 's'),
        6 : ('6', 's'),
        7 : ('7', 's'),
        8 : ('8', 's'),
        9 : ('9', 's'),
        10: ('T', 's'),
        11: ('J', 's'),
        12: ('Q', 's'),
        13: ('K', 's'),
        14: ('A', 'h'),
        15: ('2', 'h'),
        16: ('3', 'h'),
        17: ('4', 'h'),
        18: ('5', 'h'),
        19: ('6', 'h'),
        20: ('7', 'h'),
        21: ('8', 'h'),
        22: ('9', 'h'),
        23: ('T', 'h'),
        24: ('J', 'h'),
        25: ('Q', 'h'),
        26: ('K', 'h'),
        27: ('A', 'c'),
        28: ('2', 'c'),
        29: ('3', 'c'),
        30: ('4', 'c'),
        31: ('5', 'c'),
        32: ('6', 'c'),
        33: ('7', 'c'),
        34: ('8', 'c'),
        35: ('9', 'c'),
        36: ('T', 'c'),
        37: ('J', 'c'),
        38: ('Q', 'c'),
        39: ('K', 'c'),
        40: ('A', 'd'),
        41: ('2', 'd'),
        42: ('3', 'd'),
        43: ('4', 'd'),
        44: ('5', 'd'),
        45: ('6', 'd'),
        46: ('7', 'd'),
        47: ('8', 'd'),
        48: ('9', 'd'),
        49: ('T', 'd'),
        50: ('J', 'd'),
        51: ('Q', 'd'),
        52: ('K', 'd'),
        53: (None, 's'),
        54: (None, 'h'),
        55: (None, 'c'),
        56: (None, 'd'),
        57: (None, None)
    })

def get_number(rank='', suit=''):
        if not rank: rank = None
        if not suit: suit = None
        return cards_mapping.inverse[(rank, suit)]

def get_card(number):
        return cards_mapping[number]

def get_actions():
    cards = cards_mapping.keys()
    card_product = permutations(cards, 2)

    mapping = bidict()

    actions = ['draw', 'undo', 'end']
    actions.extend(card_product)
    for i, move in enumerate(actions):
        mapping[i] = move
    return mapping

action_mapping = get_actions()



if __name__ == '__main__':
    r = get_actions()
    print(len(r))
    pprint(r)