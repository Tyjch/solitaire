import pytest
import random
from solitaire import Card, Deck, Tableau, Game, ActionError
from pprint import pprint

annotations = {
    0: '[(♦, A♦), (8♠, 7♦), (2♣, A♦)]',
    1: '[(♦, A♦), (8♠, 7♦)]',
    2: '[(♦, A♦)]',
    3: '[(8♥, 7♠), (2♣, A♦)]',
    4: '[(7♠, 6♦), (2♣, A♦)]',
    38: '[(2♣, 3♣), (9♥, 8♠), (9♣, 8♥)]'
}


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


class TestTableau:

    seed = 2

    def test_tableau(self):
        deck = Deck(hidden=False, seed=self.seed)
        deck.shuffle()
        print(deck)

        cards   = deck.deal(8)
        tableau = Tableau(cards, kind='tableau')
        actions = tableau.get_candidates()

        print()
        print('TABLEAU')
        print('Card:', tableau.cards[-1])
        print('Actions:', actions)
        print()

    def test_foundation(self):
        deck = Deck(hidden=False, seed=self.seed)
        deck.shuffle()
        cards = deck.deal(8)
        tableau = Tableau(cards, kind='foundation')
        actions = tableau.get_candidates()

        print()
        print('FOUNDATION')
        print('Card:', tableau.cards[-1])
        print('Actions:', actions)
        print()

    def test_find_shown_card(self):
        # [3♥, 4♣, T♠, 9♥, 5♠, 7♠, K♦, A♣]
        deck = Deck(seed=self.seed)
        deck.shuffle()
        cards = deck.deal(8)
        tableau = Tableau(cards)
        tableau.cards[-1].hidden = False
        tableau.cards[-2].hidden = False
        card = Card('d', 'K')
        location = tableau.find_card(card)

        print()
        print('TABLEAU:  ', tableau)
        print('CARD:     ', card)
        print('LOCATION: ', location)

    def test_find_hidden_card(self):
        deck = Deck(seed=self.seed)
        deck.shuffle()
        cards = deck.deal(8)
        tableau = Tableau(cards)
        tableau.cards[-1].hidden = False
        tableau.cards[-2].hidden = False
        card = Card('h', '9')

        with pytest.raises(ValueError):
            location = tableau.find_card(card)

        print('\n')
        print('TABLEAU:', tableau)
        print('HIDDEN: ', '[3♥, 4♣, T♠, 9♥, 5♠, 7♠, K♦, A♣]')
        print('CARD:   ', card)

        print('ValueError raised: hidden card not found')

    def test_split_on_shown_card(self):
        # [3♥, 4♣, T♠, 9♥, 5♠, 7♠, K♦, A♣]
        deck = Deck(seed=self.seed)
        deck.shuffle()
        cards = deck.deal(8)
        tableau = Tableau(cards)
        tableau.cards[-1].hidden = False
        tableau.cards[-2].hidden = False
        card = Card('d', 'K')

        location = tableau.find_card(card)
        split_cards = tableau.split(location)

        print('\n')
        print('LOCATION:', location)
        print('TABLEAU:', tableau)
        print('SPLIT CARDS:', split_cards)


class TestGame:

    def test_rebuild(self):
        game = Game()
        saved_deck = game.deck.cards[:]

        print()
        for i in range(1000):
            if i > 1000:
                print()
                print( f'Round: {i}', '==' * 100)
                game.render()
            moves = game.get_moves()
            try:
                move = random.choice(moves)
                try:
                    game.move_cards(move)
                    game.get_reward(move)
                except ActionError:
                    print('Action Error')
                    continue
                game.draw()
            except (IndexError, ValueError):
                game.draw()
                print('No moves to choose from')
                continue

        game.render()
