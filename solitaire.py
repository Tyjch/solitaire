import random
from unicards import unicard
from pprint import pprint

random.seed(1)

SUITS = ['s', 'h', 'c', 'd']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']

class Card:

    foundations = {
        's': '\u2660',
        'h': '\u2661',
        'd': '\u2662',
        'c': '\u2663'
    }

    def __init__(self, suit, rank=None, hidden=False):
        self.rank = rank
        self.suit = suit
        self.hidden = hidden
        
    def __repr__(self):
        if not self.rank:
            return self.foundations[self.suit]
        if self.hidden:
            return chr(int(f"0001F0A0", base=16))
        else:
            return unicard(f"{self.rank}{self.suit}", color=True)


class Deck:

    def __init__(self):
        self.cards = []
        
        for s in SUITS:
            for r in RANKS:
                self.cards.append(Card(s, r, hidden=True))

    def __repr__(self):
        return str(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num=1):
        return [self.cards.pop(0) for n in range(num)]


class Tableau:

    def __init__(self, cards):
        self.cards = cards

    def __repr__(self):
        return str(self.cards)

    @property
    def top(self):
        return self.cards[-1]


class Game:

    def __init__(self):

        # DECK ---------------------------------------------------------------------------------------------------------
        self.deck = Deck()
        self.deck.shuffle()

        # TABLEAUS -----------------------------------------------------------------------------------------------------
        self.tableaus = [Tableau(cards=self.deck.deal(i)) for i in range(1, 8)]
        for t in self.tableaus:
            t.top.hidden = False

        # FOUNDATIONS --------------------------------------------------------------------------------------------------
        self.foundations = [Card(suit) for suit in SUITS]

        # STOCK --------------------------------------------------------------------------------------------------------
        self.stock = []

        # WASTE --------------------------------------------------------------------------------------------------------
        self.waste = []

    

if __name__ == '__main__':
    #deck = Deck()#; print(deck)
    #deck.shuffle()#; print(deck)
    #dealt_cards = deck.deal(3)#; print(dealt_cards); print(deck)

    game = Game()
    print(game.foundations)
    pprint(game.tableaus)

