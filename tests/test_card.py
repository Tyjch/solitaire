import pytest
from hypothesis import given
import hypothesis.strategies as st
from solitaire import SUITS, RANKS, LOCATIONS, Card


class TestCard:

    @given(rank=st.sampled_from(RANKS), suit=st.sampled_from(SUITS), location=st.sampled_from(LOCATIONS), hidden=st.booleans())
    def test_normal_card(self, rank, suit, location, hidden):
        card = Card(rank, suit, location, hidden)
        print(card)

        assert card.rank == rank
        assert card.suit == suit
        assert card.location == location
        assert card.hidden == hidden

    @given(suit=st.sampled_from(SUITS), location=st.sampled_from(LOCATIONS), hidden=st.booleans())
    def test_suit_card(self, suit, location, hidden):
        card = Card(suit=suit, location=location, hidden=hidden)
        print(card)

        assert card.rank is None
        assert card.suit == suit
        assert card.location == 'foundation'

    @given(location=st.sampled_from(LOCATIONS), hidden=st.booleans())
    def test_empty_card(self, location, hidden):
        card = Card(location=location, hidden=hidden)
        print(card)

        assert card.rank is None
        assert card.suit is None
        assert card.location == 'tableau'

    @given(rank=st.sampled_from(RANKS), suit=st.sampled_from(SUITS), location=st.sampled_from(LOCATIONS))
    def test_allowable_children_of_normal_card(self, rank, suit, location):
        card = Card(rank, suit, location)
        print(); print(card)
        print(card.location)
        children = card.allowable_children()
        print(children)

        assert 0 <= len(children) <= 2

    @given(suit=st.sampled_from(SUITS), location=st.sampled_from(LOCATIONS))
    def test_allowable_children_of_suit_card(self, suit, location):
        card = Card(suit=suit, location=location)
        print(); print(card)
        print(card.location)
        children = card.allowable_children()
        print(children)

        assert len(children) == 1

    @given(location=st.sampled_from(LOCATIONS))
    def test_allowable_children_of_empty_card(self, location):
        card = Card(location=location)
        print(); print(card)
        print(card.location)
        children = card.allowable_children()
        print(children)
        assert len(children) == 4


