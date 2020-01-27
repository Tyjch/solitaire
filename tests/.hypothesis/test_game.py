import pytest
from solitaire2 import Game

class TestGame:

    def test_init(self):
        game = Game(seed=1)

        for i in range(1):
            print(f'Round: {i}', '==' * 100)
            game.render()
            game.targets()
            game.sources()