import pytest
import hypothesis.strategies as st
from hypothesis import given
from solitaire import cards_product, get_opposite_suits, get_parent_card, set_container
from solitaire import GLYPHS, SUITS, RANKS, LOCATIONS


@given(suits=st.sampled_from())
def test_get_opposite_suits():
    pass