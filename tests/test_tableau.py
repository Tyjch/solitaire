import pytest
from hypothesis import given
import hypothesis.strategies as st

from solitaire2 import Card, Tableau

valid_card   = Card(rank='T', suit='c', location='foundation')
invalid_card = Card(rank='5', suit='s', location='foundation')
cards = [
    Card(rank='3', suit='s', location='foundation', hidden=True),
    Card(rank='6', suit='s', location='tableau', hidden=True),
    Card(rank='7', suit='d', location='waste', hidden=True),
    Card(rank='K', suit='h', location='foundation'),
    Card(rank='Q', suit='s', location='tableau'),
    Card(rank='J', suit='d', location='waste')
]


class TestTableau:

    def test_init(self):
        tableau = Tableau()
        print(); print(tableau)

    def test_init_with_cards(self):
        tableau = Tableau(cards=cards)
        print(); print(tableau)

        for c in tableau.cards:
            assert c.location == 'tableau'

    def test_target(self):
        tableau = Tableau(cards=cards)
        print(); print(tableau)
        print(tableau.target())

    def test_sources(self):
        tableau = Tableau(cards=cards)
        print(); print(tableau)
        print(tableau.sources())

    def test_add_valid_card(self):
        tableau = Tableau(cards=cards)
        print(); print(tableau)
        tableau.add([valid_card])
        print(tableau)

    def test_add_invalid_card(self):
        tableau = Tableau(cards=cards)
        print(); print(tableau)

        with pytest.raises(ValueError):
            tableau.add([invalid_card])

    def test_pop(self):
        tableau = Tableau(cards=cards)
        print(); print(tableau)
        card = tableau.pop()
        print(f"{tableau} → {card}")

    def test_split(self):
        tableau = Tableau(cards=cards)
        card = Card(rank='K', suit='h')
        print(); print(tableau)
        split_cards = tableau.split(card)
        print(f"{tableau.cards} → {split_cards}")

    