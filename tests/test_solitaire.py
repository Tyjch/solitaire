import pytest
import random
from solitaire import Card, Deck, Tableau, Game
from pprint import pprint


class TestCard:

    def test_card(self):
        card = Card('s', 'T')
        print(); print(card)

    def test_hidden(self):
        card = Card('h', 'A', hidden=True)
        print(); print(card)

    def test_shown_to_hidden(self):
        card = Card('h', 'A')
        print(); print(card)
        card.hidden = True
        print(card)

    def test_hidden_to_shown(self):
        card = Card('h', 'A', hidden=True)
        print(); print(card)
        card.hidden = False
        print(card)

    def test_foundation_keys(self):
        card = Card('h', 'A')

    def test_equality_of_identical_cards_both_hidden(self):
        card_one = Card('h', 'A', hidden=True)
        card_two = Card('h', 'A', hidden=True)
        print(); print(card_one, card_two)
        assert card_one == card_two

    def test_equality_of_identical_cards_both_not_hidden(self):
        card_one = Card('h', 'A')
        card_two = Card('h', 'A')
        print(); print(card_one, card_two)
        assert card_one == card_two

    def test_inequality_of_different_cards_both_hidden(self):
        card_one = Card('s', 'J', hidden=True)
        card_two = Card('h', 'A', hidden=True)
        print(); print(card_one, card_two)
        assert card_one != card_two

    def test_inequality_of_different_cards_both_not_hidden(self):
        card_one = Card('s', 'J')
        card_two = Card('h', 'A')
        print(); print(card_one, card_two)
        assert card_one != card_two


class TestDeck:

    def test_deck_hidden(self):
        deck = Deck()
        print(); print(deck)

    def test_deck_shown(self):
        deck = Deck(hidden=False)
        print(); print(deck)

    def test_shuffle_same_seed(self):
        deck_one = Deck(hidden=False, seed=2)
        deck_two = Deck(hidden=False, seed=2)

        for deck in (deck_one, deck_two):
            deck.shuffle()

        for (c1, c2) in zip(deck_one.cards, deck_two.cards):
            assert c1 == c2

    def test_shuffle_different_seed(self):
        deck_one = Deck(hidden=False, seed=0)
        deck_two = Deck(hidden=False, seed=4)

        for deck in (deck_one, deck_two):
            deck.shuffle()

        for (c1, c2) in zip(deck_one.cards, deck_two.cards):
            assert c1 != c2

    def test_deal(self):
        deck = Deck(hidden=False)
        deck.shuffle()

        print(); print(deck)
        print(deck.deal(3))


class TestGame:

    def test_game(self):
        game = Game()
        game.deck.cards = game.deck.cards[:-1]

        print()
        print()
        for i in range(100):
            print( f'Round: {i}', '==' * 50)
            game.render()
            game.draw()
            game.get_actions()