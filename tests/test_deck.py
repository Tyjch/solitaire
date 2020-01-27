import pytest
from solitaire2 import Deck

class TestDeck:

    def test_init(self):
        deck = Deck()
        print(); print(deck)

    def test_init_shown(self):
        deck = Deck(hidden=False)
        print(); print(deck)

    def test_shuffle(self):
        deck = Deck(hidden=False)
        deck.shuffle()
        print(); print(deck)

    def test_deal(self):
        deck = Deck(hidden=False)
        deck.shuffle()
        print(); print(deck)
        cards = deck.deal()
        print(cards)

    def test_rebuild(self):
        deck = Deck(hidden=False)

        # Shuffle the deck
        deck.shuffle()
        print()
        print('times rebuilt:', deck.times_rebuilt)
        print(f'original deck: {len(deck.cards)} ', deck)

        # Deal a few cards
        dealt_cards = deck.deal(6)
        print(f'dealt cards: {len(dealt_cards)}    ', dealt_cards)

        # Play a few of the dealt cards
        print('played card:', dealt_cards.pop(3))
        print('played card:', dealt_cards.pop(1))

        # Add the unplayed cards back to the end of the deck
        deck.cards.extend(dealt_cards)
        print(f'messed up deck: {len(deck.cards)}', deck)

        # Rebuild the deck
        print(f'order: {len(deck.order)}         ', deck.order)
        deck.rebuild()
        print(f'rebuilt deck: {len(deck.cards)}  ', deck)
        print('times rebuilt:', deck.times_rebuilt)

    def test_draw(self):
        deck = Deck(hidden=False)
        deck.shuffle(); print()
        print(deck)
        print(deck.waste)

        for n in range(3):
            print(f"Draw {n}")
            deck.draw()
            print(deck)
            print(deck.waste)
            played_card = deck.waste.pop(1)
            print(played_card)

        deck.rebuild()
        print(deck)
        print(deck.waste)
