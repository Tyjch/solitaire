from colors import color
from pprint import pprint
from collections import OrderedDict
from more_itertools import padded
from utility import get_number
import random, json


EMPTY  = 0
GLYPHS = {'s': '\u2660', 'h': '\u2665', 'd': '\u2666', 'c': '\u2663'}
SUITS  = ('s', 'h', 'c', 'd')
RANKS  = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
LOCATIONS = ('tableau', 'foundation', 'deck', 'waste')


def get_opposite_suits(suit: str):
    if suit in ('s', 'c'):
        return 'h', 'd'
    elif suit in ('h', 'd'):
        return 's', 'c'
    else:
        raise ValueError(f'{suit} is not in {SUITS}')

def cards_product(ranks, suits):
    cards = []
    for s in suits:
        for r in ranks:
            cards.append(Card(r, s))
    return cards

def set_container(items, container):
    for i in items:
        i.container = container

def get_parent_card(card):
    # Really only used to tell if the parent is hidden and will be revealed upon a move
    # This is used to increase score for revealing hidden cards
    # Only works for cards in Tableaus
    container = card.container
    if isinstance(container, Tableau):
        card_index = container.cards.index(card)
        parent_card = container.cards[card_index - 1]
        return parent_card

def print_observation(game_state: OrderedDict):
    print()
    print('OBSERVATION')
    print('DECK:       ', game_state['Deck'])
    print('WASTE:      ', game_state['Waste'])
    print('FOUNDATIONS:', list(game_state['Foundations'].items()))
    print('LEGAL MOVES:', game_state['Legal Moves'])
    print('TABLEAUS:')
    for t in game_state['Tableaus'].items():
        print(t)



class Card:

    def __init__(self, rank: str = None, suit: str = None, location: str = 'deck', hidden: bool = False, container: object = None):
        """
        Parameters
        ----------
        rank : str, optional
            Indicates the rank of the card as an uppercase character
        suit : str, optional
            Indicates the suit of the card as a lowercase character
        hidden : bool, optional
            Indicates the card is hidden, it cannot be a target or a source for a move

        Notes
        -----
        `card = Card()` is a tableau card, it can only be a target. Only kings can be placed on it.
        `card = Card(suit='h')` is a foundation card, it can only be a target. Only aces of the same suit can be placed on it.
        """

        # Validating `rank` argument
        if (rank in RANKS) or (rank is None): self.rank = rank
        else: raise ValueError(f'{rank} is not in {RANKS} or None')

        # Validating `suit` argument
        if (suit in SUITS) or (suit is None): self.suit = suit
        else: raise ValueError(f'{suit} is not in {SUITS} or None')

        # Validating `location` argument
        if location in LOCATIONS:
            self.location = location
        else:
            raise ValueError(f'{location} is not in {LOCATIONS}')

        # Overwrite location if suit or empty card
        if not self.suit and not self.rank:
            self.location = 'tableau'
        elif not self.rank:
            self.location = 'foundation'

        self.hidden = hidden
        self.container = container

        '''
        # Ensuring that only normal cards can be hidden
        if rank and suit: self.hidden = hidden
        else: self.hidden = False
        '''

    def __hash__(self):
        """
        Returns
        -------
        int:
            An integer representing the card,
        """
        return hash((self.rank, self.suit, self.hidden))

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

    def __repr__(self):
        if self.hidden:
            return chr(int("0001F0A0", base=16))

        elif not self.suit and not self.rank:
            return chr(int("0001F0E0", base=16))

        elif self.suit:
            if self.rank:
                string = f"{self.rank}{GLYPHS[self.suit]}"
            else:
                string = f"{GLYPHS[self.suit]}"

            if self.suit in ('s', 'c'):
                return color(string, 'darkgray')
            elif self.suit in ('h', 'd'):
                return color(string, 'red')

    def allowable_children(self) -> list:
        if self.location == 'tableau':
            if self.rank:
                if self.rank == 'A':
                    # In the tableau, aces have no children
                    return []
                else:
                    # In the tableau, children are of the opposite color and one rank lower
                    child_rank  = RANKS[RANKS.index(self.rank) - 1]
                    child_suits = get_opposite_suits(self.suit)
            else:
                # In the tableau, any king can be placed on an empty card
                child_rank  = 'K'
                child_suits = SUITS

        elif self.location == 'foundation':
            if self.rank:
                if self.rank == 'K':
                    # In the foundation, kings have no children
                    return []
                else:
                    # In the foundation, children are of the same suit and one rank higher
                    child_rank  = RANKS[RANKS.index(self.rank) + 1]
                    child_suits = self.suit
            else:
                # In the foundation, only an ace of the same suit can be placed on a suit card
                child_rank  = 'A'
                child_suits = self.suit

        else:
            return []

        cards = cards_product(child_rank, child_suits)
        return cards

    def dump(self):
        if self.hidden:
            return 58
        else:
            return get_number(self.rank, self.suit)

class Deck:

    def __init__(self, hidden=True, seed=0):
        self.seed  = seed
        self.cards = []
        self.waste = []
        self.order = None
        self.times_rebuilt = 0
        for s in SUITS:
            for r in RANKS:
                self.cards.append(Card(r, s, hidden=True, container=self.cards))
        self.refresh()

    def __repr__(self):
        return str(self.cards)

    def shuffle(self):
        random.seed(self.seed)
        random.shuffle(self.cards)
        if self.order is None:
            self.order = self.cards[:]

    def deal(self, num=1):
        if len(self.cards) == 0:
            self.rebuild()
        num = min(num, len(self.cards))
        return [self.cards.pop(0) for n in range(num)]

    def rebuild(self):
        self.cards.extend(self.waste)
        self.waste = []
        self.cards = sorted(self.cards, key=lambda y: self.order.index(y))
        self.times_rebuilt += 1
        self.refresh()

    def draw(self):
        if len(self.cards) > 0:
            self.waste[:0] = self.deal(3)
            for c in self.waste:
                c.hidden = False
                c.container = self.waste
        else:
            self.rebuild()

    def sources(self):
        return [self.waste[0]]

    def refresh(self):
        for c in self.cards:
            c.location = 'deck'
        for c in self.waste:
            c.location = 'deck'
        set_container(self.waste, self)

    def find(self, rank, suit):
        for c in self.cards:
            if (c.rank == rank) and (c.suit == suit) and not c.hidden:
                return c
        for c in self.waste:
            if (c.rank == rank) and (c.suit == suit):
                return c

    def dump(self):
        deck  = tuple(padded([c.dump() for c in self.cards], EMPTY, 24))
        waste = tuple(padded([c.dump() for c in self.waste], EMPTY, 24))
        return deck, waste

class Foundation:

    def __init__(self, suit, cards=()):
        self.suit = suit
        self.cards = [Card(suit=suit, location='foundation')]
        self.cards.extend(cards)
        self.refresh()

    def __repr__(self) -> str:
        return str(self.cards)

    def target(self) -> Card:
        return self.cards[-1]

    def sources(self) -> list:
        return [self.cards[-1]]

    def add(self, cards: list):
        target = self.target()
        children = target.allowable_children()

        if cards[0] in children:
            self.cards.extend(cards)
            self.refresh()
        else:
            raise ValueError(f"{cards[0]} not in {target.allowable_children()}")

    def pop(self):
        return self.cards.pop()

    def split(self, card):
        return [self.pop()]

    def refresh(self):
        for c in self.cards:
            c.hidden   = False
            c.location = 'foundation'
        set_container(self.cards, self)

    def find(self, rank, suit):
        for c in self.cards:
            if (c.rank == rank) and (c.suit == suit):
                return c

    def dump(self):
        return self.suit, self.target().dump()

class Tableau:

    def __init__(self, cards=()):
        self.cards = [Card(location='tableau')]
        self.cards.extend(cards)
        self.refresh()

    def __repr__(self) -> str:
        return str(self.cards)

    def target(self) -> Card:
        return self.cards[-1]

    def sources(self):
        cards = []

        # Returns empty card if nothing is on top of it
        if len(self.cards) == 1:
            return [self.cards[0]]

        for c in reversed(self.cards[1:]):
            if not c.hidden:
                cards.append(c)
            else:
                break

        return list(reversed(cards))

    def add(self, cards: list):
        target = self.target()
        children = target.allowable_children()

        if cards[0] in children:
            self.cards.extend(cards)
            self.refresh()
        else:
            raise ValueError(f"{cards[0]} not in {target.allowable_children()}")

    def pop(self):
        return self.cards.pop()

    def split(self, card):
        index = self.cards.index(card)
        if len(self.cards) > 1:
            split_cards = self.cards[index:]
            self.cards  = self.cards[:index]
            self.refresh()
            return split_cards
        else:
            return [self.cards.pop()]

    def refresh(self):
        for c in self.cards:
            c.location = 'tableau'
        if self.target().hidden is True:
            self.target().hidden = False
        set_container(self.cards, self)

    def find(self, rank, suit):
        if rank and suit:
            for c in self.cards:
                if (c.rank == rank) and (c.suit == suit) and not c.hidden:
                    return c
        elif not rank and not suit:
            c = self.cards[-1]
            if not c.rank and not c.suit:
                return c

    def dump(self):
        return tuple(padded([c.dump() for c in self.cards], EMPTY, 19))

class Game:

    def __init__(self, seed=None):
        self.deck = Deck(seed=seed)
        self.deck.shuffle()
        self.score = 0
        self.foundations = [Foundation(suit) for suit in SUITS]
        self.tableaus = [Tableau(cards=self.deck.deal(i)) for i in range(1, 8)]
        for t in self.tableaus: t.cards[-1].hidden = False

    def render(self, deck=True, waste=True, foundations=True, tableaus=True, targets=False, sources=False, legal_moves=True):
        print()

        if deck:
            print('DECK:', len(self.deck.cards), 'cards')
            print(self.deck)
            print()

        if waste:
            print('WASTE:', len(self.deck.waste), 'cards')
            print(self.deck.waste)
            print()

        if foundations:
            print('FOUNDATIONS')
            print(self.foundations)
            print()

        if tableaus:
            print('TABLEAUS')
            pprint(self.tableaus)
            print()

        if targets:
            print('TARGETS')
            print(self.targets())
            print()

        if sources:
            print('SOURCES')
            print(self.sources())
            print()

        if legal_moves:
            print('LEGAL MOVES')
            print(self.legal_moves())
            print()

    def targets(self):
        target_cards = []
        for attribute in (self.tableaus, self.foundations):
            for pile in attribute:
                target_cards.append(pile.target())
        return target_cards

    def sources(self):
        source_cards = []
        for attribute in (self.tableaus, self.foundations):
            for pile in attribute:
                source_cards.extend(pile.sources())

        try:
            source_cards.extend(self.deck.sources())
        except IndexError:
            pass

        return source_cards

    def legal_moves(self):
        moves = []
        for target in self.targets():
            children = target.allowable_children()
            for source in self.sources():
                if source in children:
                    moves.append((target, source))
        return moves

    def move_cards(self, move):
        target, source = move

        try:
            cards = source.container.split(source)
            target.container.add(cards)
        except AttributeError:
            if self.deck.waste[0] == source:
                cards = [self.deck.waste.pop(0)]
                target.container.add(cards)

        '''
        self.score += reward
        print()
        print('REWARD')
        print(reward)
        print()
        print('TOTAL SCORE')
        print(self.score)
        '''

    def get_move_reward(self, move):
        foundation_scores = {
            'A': 100.0,
            '2': 90.0,
            '3': 80.0,
            '4': 70.0,
            '5': 60.0,
            '6': 50.0,
            '7': 40.0,
            '8': 30.0,
            '9': 20.0,
            'T': 10.0,
            'J': 10.0,
            'Q': 10.0,
            'K': 10.0
        }
        target, source = move
        reward = 0.0

        # Moving cards to foundation (target card is in foundation)
        if target.location == 'foundation':
            reward += foundation_scores[source.rank]
        # Moving cards from foundation (takes away points you gained)
        if source.location == 'foundation':
            reward -= foundation_scores[source.rank]
        # 20 points for playing card from waste (source card is in waste)
        if source.location == 'deck':
            reward += 20.0
        # 20 points for uncovering hidden cards in tableau (source card is in tableau)
        if source.location == 'tableau':
            parent_card = get_parent_card(card=source)
            if parent_card.hidden:
                reward += 20.0

        return reward

    def get_draw_reward(self):
        # -20 points for going through deck more than 3? times (Deck)
        max_rebuilds = 3
        if len(self.deck.cards) == 0:
            if self.deck.times_rebuilt >= max_rebuilds:
                return -20.0
            else:
                return 0.0
        else:
            return 0.0

    def find_card(self, rank, suit):
        for attribute in (self.foundations, self.tableaus, self.deck):
            try:
                for pile in attribute:
                    found_card = pile.find(rank, suit)
                    if found_card:
                        return found_card
            except TypeError:
                found_card = attribute.find(rank, suit)

    def state(self):
        tableau_names = '1st', '2nd', '3rd', '4th', '5th', '6th', '7th'

        states      = OrderedDict()
        deck, waste = self.deck.dump()
        foundations = OrderedDict([f.dump() for f in self.foundations])
        tableaus    = OrderedDict([(name, t.dump()) for name, t in zip(tableau_names, self.tableaus)])
        legal_moves = tuple(padded([(k.dump(), v.dump()) for (k,v) in self.legal_moves()], (0, 0), 8))

        states['Deck']        = deck
        states['Foundations'] = foundations
        states['Legal Moves'] = legal_moves
        states['Tableaus']    = tableaus
        states['Waste']       = waste

        return states






if __name__ == '__main__':
    game = Game(seed=1)

    for x in range(50000):
        print()
        print(f'Round: {x}', '==' * 100)
        #game.render()
        possible_moves = game.legal_moves()
        print('Number of Legal Moves:', len(possible_moves))
        if len(possible_moves) > 5:
            game.render()
        try:
            chosen_move = random.choice(possible_moves)
            game.move_cards(chosen_move)
        except IndexError:
            game.deck.draw()

        print_observation(game.state())