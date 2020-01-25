import random, itertools
from unicards import unicard
from pprint import pprint

RANKS  = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
SUITS  = ('s', 'h', 'c', 'd')
COLORS = {
    's': 'BLACK',
    'h': 'RED',
    'c': 'BLACK',
    'd': 'RED'
}
BLACK_SUITS = ('s', 'c')
RED_SUITS = ('h', 'd')
MODE   = 'text'


class Card:

    foundations = {
        's': '\u2660',
        'h': '\u2665',
        'd': '\u2666',
        'c': '\u2663'
    }

    def __init__(self, suit, rank=None, hidden=False):
        self.rank   = rank
        self.suit   = suit
        self.hidden = hidden
        self.color  = COLORS[self.suit]
        
    def __repr__(self):
        if MODE == 'glyph':
            if not self.rank:
                return self.foundations[self.suit]
            elif self.hidden:
                return chr(int(f"0001F0A0", base=16))
            else:
                return unicard(f"{self.rank}{self.suit}", color=True)
        elif MODE == 'text':
            if not self.rank:
                return f"{self.foundations[self.suit]}"
            elif self.hidden:
                return chr(int(f"0001F0A0", base=16))
            else:
                return f"{self.rank}{self.foundations[self.suit]}"

    def __eq__(self, other):
        if (self.rank == other.rank) and (self.suit == other.suit) and (self.hidden == other.hidden):
            return True

    def __ne__(self, other):
        if (self.rank != other.rank) or (self.suit != other.suit) or (self.hidden != other.hidden):
            return True

    def __hash__(self):
        return hash((self.rank, self.suit, self.hidden))


class Tableau:

    def __init__(self, cards, kind='tableau'):
        self.cards = cards
        self.kind  = kind

    def __repr__(self):
        return str(self.cards)

    def get_candidates(self):
        candidates = []

        if self.kind == 'tableau':
            candidates = self._get_tableau_candidates()
        elif self.kind == 'foundation':
            candidates = self._get_foundation_candidates()

        return candidates

    def _get_tableau_candidates(self):
        try:
            card = self.cards[-1]
        except IndexError:
            return [Card(suit, 'K') for suit in SUITS]

        if card.color == 'RED':
            child_suits = BLACK_SUITS
        elif card.color == 'BLACK':
            child_suits = RED_SUITS

        if card.rank == 'A':
            return []
        else:
            rank_index = RANKS.index(card.rank)
            child_rank = RANKS[rank_index - 1]

        candidates = []
        for suit in child_suits:
            candidates.append(Card(suit, rank=child_rank))
        return candidates

    def _get_foundation_candidates(self):
        card = self.cards[-1]

        if card.rank is None:
            return [Card(card.suit, rank='2')]

        rank_index = RANKS.index(card.rank)
        child_rank = RANKS[rank_index + 1]

        return [Card(card.suit, rank=child_rank)]


class Deck:

    def __init__(self, hidden=True, seed=0):
        self.seed  = seed
        self.cards = []
        
        for s in SUITS:
            for r in RANKS:
                self.cards.append(Card(s, r, hidden=hidden))

    def __repr__(self):
        return str(self.cards)

    def shuffle(self):
        random.seed(self.seed)
        random.shuffle(self.cards)

    def deal(self, num=1):
        num = min(num, len(self.cards))
        return [self.cards.pop(0) for n in range(num)]


class Game:

    def __init__(self):

        # DECK ---------------------------------------------------------------------------------------------------------
        self.deck = Deck()
        self.deck.shuffle()

        # TABLEAUS -----------------------------------------------------------------------------------------------------
        self.tableaus = [Tableau(cards=self.deck.deal(i)) for i in range(1, 8)]
        for t in self.tableaus:
            t.cards[-1].hidden = False

        #for c in self.deck.cards:
        #    c.hidden = False

        # FOUNDATIONS --------------------------------------------------------------------------------------------------
        self.foundations = [Tableau(cards=[Card(suit)], kind='foundation') for suit in SUITS]

        # WASTE --------------------------------------------------------------------------------------------------------
        self.waste = []

    def render(self):
        print()
        print('DECK:', len(self.deck.cards), 'cards')
        print(self.deck)
        print()

        print('WASTE')
        print(self.waste)
        print()

        print('FOUNDATIONS')
        print(self.foundations)
        print()

        print('TABLEAUS')
        pprint(self.tableaus)
        print()

        print('PLAYABLE CARDS')
        print(self.playable_cards())
        print()

        print('CANDIDATES')
        print(self.get_candidates())
        print()

    def draw(self):
        if len(self.deck.cards) > 0:
            self.waste[:0] = self.deck.deal(3)
            for c in self.waste:
                c.hidden = False
        else:
            self.rebuild()

    def rebuild(self):
        # TODO: Clean up
        print('ORIGINAL DECK:')
        print('[Q♦, J♥, 4♠, 5♦, T♠, 9♦, 7♠, 2♦, 6♥, 9♠, 8♦, A♥, Q♣, T♥, 5♣, 7♥, K♥, 6♣, 7♣, 4♥, 3♠, A♣, T♦]')

        print('WASTE:')
        print(self.waste)

        print('REVERSED WASTE:')
        reversed_waste = list(reversed(self.waste))
        print(reversed_waste)

        print('GROUPS:')
        groups = [list(reversed_waste[i:i+3]) for i in range(0, len(reversed_waste), 3)]
        print(groups)

        print('REVERSED GROUPS:')
        reversed_groups = [list(reversed(group)) for group in groups]
        print(reversed_groups)

        print('FINAL LIST:')
        final_list = list(itertools.chain.from_iterable(reversed_groups))
        print(final_list)

        self.deck.cards = final_list
        self.waste = []

    def playable_cards(self):
        foundation_cards = []
        for tableau in self.foundations:
            try:
                foundation_cards.append(tableau.cards[-1])
            except IndexError:
                continue

        tableau_cards = []
        for tableau in self.tableaus:
            try:
                tableau_cards.append(tableau.cards[-1])
            except IndexError:
                continue

        waste_cards = []
        try:
            waste_cards.append(self.waste[0])
        except IndexError:
            pass

        return list(itertools.chain(foundation_cards, tableau_cards, waste_cards))

    def get_candidates(self):
        candidates = []
        for foundation in self.foundations:
            candidates.extend(foundation.get_candidates())
        for tableau in self.tableaus:
            candidates.extend(tableau.get_candidates())

        return candidates

    def get_actions(self):
        actions = set(self.playable_cards()) & set(self.get_candidates())
        print(actions)


'''
if __name__ == '__main__':
    deck = Deck()#; print(deck)
    deck.shuffle()#; print(deck)
    #dealt_cards = deck.deal(3)#; print(dealt_cards); print(deck)

    game = Game()
    print(game.foundations)
    pprint(game.tableaus)
'''
