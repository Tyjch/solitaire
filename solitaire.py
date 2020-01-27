import random, itertools
from unicards import unicard
from pprint import pprint
from colors import red, faint, color

MODE   = 'text'
RANKS  = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
SUITS  = ('s', 'h', 'c', 'd')
COLORS = {
    's': 'BLACK',
    'h': 'RED',
    'c': 'BLACK',
    'd': 'RED'
}
BLACK_SUITS = ('s', 'c')
RED_SUITS   = ('h', 'd')


class ActionError(Exception):
    pass


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
                if self.color == 'RED':
                    return red(f"{self.foundations[self.suit]}")
                else:
                    return color(f"{self.foundations[self.suit]}", 'darkgray')
            elif self.hidden:
                return chr(int(f"0001F0A0", base=16))
            else:
                if self.color == 'RED':
                    return red(f"{self.rank}{self.foundations[self.suit]}")
                else:
                    return color(f"{self.rank}{self.foundations[self.suit]}", 'darkgray')

    def __eq__(self, other):
        try:
            if (self.rank == other.rank) and (self.suit == other.suit) and (self.hidden == other.hidden):
                return True
        except AttributeError:
            return False

    def __ne__(self, other):
        try:
            if (self.rank != other.rank) or (self.suit != other.suit) or (self.hidden != other.hidden):
                return True
        except AttributeError:
            return False

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
            return [('Empty', Card(suit, 'K')) for suit in SUITS]

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
            candidates.append((card, Card(suit, rank=child_rank)))
        return candidates

    def _get_foundation_candidates(self):
        card = self.cards[-1]

        if card.rank is None:
            return [(card, Card(card.suit, rank='A'))]
        elif card.rank == 'K':
            return []

        rank_index = RANKS.index(card.rank)
        child_rank = RANKS[rank_index + 1]

        return [(card, Card(card.suit, rank=child_rank))]

    def find_card(self, card):
        return self.cards.index(card)

    def split(self, index):
        if len(self.cards) > 1:
            split_cards = self.cards[index:]
            self.cards  = self.cards[:index]
            self.refresh()
            return split_cards
        else:
            return [self.cards.pop()]

    def refresh(self):
        try:
            top_card = self.cards[-1]
            top_card.hidden = False
        except IndexError:
            pass


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

    def __init__(self, seed=0):

        # DECK ---------------------------------------------------------------------------------------------------------
        self.deck = Deck(seed=seed)
        self.deck.shuffle()

        # TABLEAUS -----------------------------------------------------------------------------------------------------
        self.tableaus = [Tableau(cards=self.deck.deal(i)) for i in range(1, 8)]
        for t in self.tableaus:
            t.cards[-1].hidden = False

        # FOUNDATIONS --------------------------------------------------------------------------------------------------
        self.foundations = [Tableau(cards=[Card(suit)], kind='foundation') for suit in SUITS]

        # WASTE --------------------------------------------------------------------------------------------------------
        self.waste = []

    def __getitem__(self, key):
        if key == 'tableau':
            return self.tableaus
        elif key == 'foundation':
            return self.foundations
        elif key == 'waste':
            return self.waste

    def render(self, deck=True, waste=True, foundations=True, tableaus=True, target_cards=True, source_cards=True, candidates=True, moves=True):
        print()

        if deck:
            print('DECK:', len(self.deck.cards), 'cards')
            print(self.deck)
            print()

        if waste:
            print('WASTE:', len(self.waste), 'cards')
            print(self.waste)
            print()

        if foundations:
            print('FOUNDATIONS')
            print(self.foundations)
            print()

        if tableaus:
            print('TABLEAUS')
            pprint(self.tableaus)
            print()

        if target_cards:
            print('TARGET CARDS')
            print(self.target_cards())
            print()

        if source_cards:
            print('SOURCE CARDS')
            print(self.source_cards())
            print()

        if candidates:
            print('CANDIDATES')
            print(self.get_candidates())
            print()

        if moves:
            print('MOVES')
            print(self.get_moves())
            print()

    def draw(self):
        if len(self.deck.cards) > 0:
            self.waste[:0] = self.deck.deal(3)
            for c in self.waste:
                c.hidden = False
        else:
            self.rebuild()

    def rebuild(self):
        reversed_waste = list(reversed(self.waste))
        groups = [list(reversed_waste[i:i+3]) for i in range(0, len(reversed_waste), 3)]
        reversed_groups = [list(reversed(group)) for group in groups]
        final_list = list(itertools.chain.from_iterable(reversed_groups))

        self.deck.cards = final_list
        self.waste = []

    def target_cards(self):
        foundation_cards = []
        tableau_cards    = []
        waste_cards      = []

        for tableau in self.foundations:
            try:
                foundation_cards.append(tableau.cards[-1])
            except IndexError:
                foundation_cards.append('Empty')

        for tableau in self.tableaus:
            try:
                tableau_cards.append(tableau.cards[-1])
            except IndexError:
                tableau_cards.append('Empty')

        try:
            waste_cards.append(self.waste[0])
        except IndexError:
            pass

        return list(itertools.chain(foundation_cards, tableau_cards, waste_cards))

    def source_cards(self):
        foundation_cards = []
        tableau_cards    = []
        waste_cards      = []

        for tableau in self.foundations:
            try:
                foundation_cards.append(tableau.cards[-1])
            except IndexError:
                foundation_cards.append('Empty')

        for tableau in self.tableaus:
            try:
                tableau_cards.extend([card for card in tableau.cards if not card.hidden])
            except IndexError:
                tableau_cards.append('Empty')

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

    def get_moves(self):
        # Example actions: (3♣, 2♥), (3♣, 2♦), (8♠, 7♥)
        target_cards  = self.target_cards() # [♠, A♥, 2♣, A♦, K♥, Q♦, 6♣, J♦, 3♣, 9♣, 9♥, 9♠]
        source_cards  = self.source_cards() # [♠, A♥, 2♣, A♦, K♥, K♠, Q♦, 8♠, 7♦, 6♣, J♦, 8♥, 7♠, 6♦, 5♣, 4♥, 3♣, 9♣, 9♥, T♦]
        candidate_moves = self.get_candidates() # [(♠, A♠), (A♥, 2♥), (2♣, 3♣), (A♦, 2♦), (K♥, Q♠), (K♥, Q♣), (Q♦, J♠), (Q♦, J♣), (6♣, 5♥), (6♣, 5♦), (J♦, T♠), (J♦, T♣), (3♣, 2♥), (3♣, 2♦), (9♣, 8♥), (9♣, 8♦), (9♥, 8♠), (9♥, 8♣)]

        moves = []
        for a in candidate_moves:
            if (a[0] in target_cards) and (a[1] in source_cards):
                moves.append(a)
        return moves

    def find_card(self, card):
        for i, tableau in enumerate(self.tableaus):
            try:
                card_index = tableau.find_card(card)
                return i, card_index, 'tableau'
            except ValueError:
                continue

        for i, tableau in enumerate(self.foundations):
            try:
                card_index = tableau.find_card(card)
                return i, card_index, 'foundation'
            except ValueError:
                continue

        try:
            top_card = self.waste[0]
            if top_card == card:
                return 0, 0, 'waste'
        except IndexError:
            pass

    def move_cards(self, move):
        # move is (target, source)
        #print('SELECTED MOVE')
        #print(f'{move[0]} ← {move[1]}')

        # TARGET
        if move[0] == 'Empty':
            empty_tableaus = [t for t in self.tableaus if len(t.cards) == 0]
            target = empty_tableaus[0]
        else:
            t = self.find_card(move[0])
            if t[2] in ('foundation', 'tableau'):
                target = self[t[2]][t[0]]
            else:
                target = 'Empty'

        # SOURCE
        s = self.find_card(move[1])
        if s[2] == 'waste':
            source = [self[s[2]].pop(0)]
        else:
            source = self[s[2]][s[0]]
            source = source.split(s[1])

        if target:
            print()
            print(f'{target} ← {source}')
            t = self.find_card(move[0])
            if t:
                if t[2] == 'foundation':
                    if len(source) > 1:
                        raise ActionError
            target.cards.extend(source)
            print(target)

    def get_reward(self, move):
        target_card = move[0]
        source_card = move[1]
        target = self.find_card(target_card); print('target', target)
        source = self.find_card(source_card); print('source', source)




        # -20 points for going through deck more than 3? times
        # 20 points for playing card from waste
        # 20 points for uncovering hidden cards in tableau
        # Moving cards to foundation = A:100, 2: 90, 3: 80, 4: 70, 5: 60, 6:50, 7:40, 8:30, 9:20, T:10, J:10, Q:10, K:10
        # Time bonus on ending the game

        pass










