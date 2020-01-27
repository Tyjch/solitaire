import pytest
from hypothesis import given
import hypothesis.strategies as st

from solitaire2 import Card, Foundation

valid_card   = Card(rank='4', suit='h', location='foundation')
invalid_card = Card(rank='5', suit='s', location='foundation')
cards = [
    Card(rank='A', suit='h', location='foundation'),
    Card(rank='2', suit='h', location='tableau'),
    Card(rank='3', suit='h', location='waste')
]


class TestFoundation:

    def test_init(self):
        foundation = Foundation(suit='h')
        print(); print(foundation)

    def test_init_with_cards(self):
        foundation = Foundation(suit='h', cards=cards)
        print(); print(foundation)

        for c in foundation.cards:
            assert c.location == 'foundation'
            assert c.hidden   == False

    def test_target(self):
        foundation = Foundation(suit='h', cards=cards)
        print(); print(foundation)
        print(foundation.target())

    def test_sources(self):
        foundation = Foundation(suit='h', cards=cards)
        print(); print(foundation)
        print(foundation.sources())

    def test_add_valid_card(self):
        foundation = Foundation(suit='h', cards=cards)
        print(); print(foundation)
        foundation.add(valid_card)
        print(foundation)

    def test_add_invalid_card(self):
        foundation = Foundation(suit='h', cards=cards)
        print(); print(foundation)

        with pytest.raises(ValueError):
            foundation.add(invalid_card)

    def test_pop(self):
        foundation = Foundation(suit='h', cards=cards)
        print(); print(foundation)
        card = foundation.pop()
        print(f"{foundation} → {card}")