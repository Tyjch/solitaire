import pytest, random
import hypothesis.strategies as st
from hypothesis import given
from solitaire import Game

SEEDS = (1, 2)


class TestIntegration:
    @given(seed=st.sampled_from(SEEDS))
    def test_game(self, seed):
        game = Game(seed=seed)
        for x in range(100):
            print(); print(f'Round: {x}', '==' * 100)
            game.render()
            possible_moves = game.legal_moves()
            try:
                chosen_move = random.choice(possible_moves)
                game.move_cards(chosen_move)
            except IndexError:
                game.deck.draw()



