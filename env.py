import gym, json
import gym.spaces as spaces
from solitaire import Game, Card
from pprint import pprint
from utility import get_number, get_card, action_mapping, cards_mapping


class SolitaireEnv(gym.Env):
    action_space = spaces.Dict({
        'Action' : spaces.Discrete(4),
        'Source' : spaces.Discrete(59),
        'Target' : spaces.Discrete(59)
    })
    observation_space = spaces.Dict({
        'Deck'  : spaces.MultiDiscrete([59 for x in range(24)]),
        'Waste' : spaces.MultiDiscrete([58 for y in range(24)]),
        'Foundations' : spaces.Dict({
            's' : spaces.Discrete(59),
            'h' : spaces.Discrete(59),
            'c' : spaces.Discrete(59),
            'd' : spaces.Discrete(59)
        }),
        'Tableaus' : spaces.Dict({
            '1st'  : spaces.MultiDiscrete([59 for a in range(19)]),
            '2nd'  : spaces.MultiDiscrete([59 for b in range(19)]),
            '3rd'  : spaces.MultiDiscrete([59 for c in range(19)]),
            '4th'  : spaces.MultiDiscrete([59 for d in range(19)]),
            '5th'  : spaces.MultiDiscrete([59 for e in range(19)]),
            '6th'  : spaces.MultiDiscrete([59 for f in range(19)]),
            '7th'  : spaces.MultiDiscrete([59 for g in range(19)]),
        }),
    })

    def __init__(self):
        self.game = Game()

    def render(self, mode='human'):
        if mode == 'human':
            self.game.render()

    def step(self, action: object) -> (object, float, bool, dict):
        act = action_mapping[action['Action']]
        reward = 0

        if act == 'move':
            target = self.find_card(action['Target'])
            source = self.find_card(action['Source'])
            move   = (target, source)
            reward = self.game.get_move_reward(move)
            self.game.move_cards(move)

        elif act == 'draw':
            reward = self.game.get_draw_reward()
            self.game.deck.draw()

        return self.game.state(), reward, False, {}

    def find_card(self, number):
        ranksuit = get_card(number)
        return self.game.find_card(ranksuit[0], ranksuit[1])

    def reset(self) -> object:
        self.game = Game()
        return self.game.state()

    def close(self):
        pass


if __name__ == '__main__':
    env = SolitaireEnv()
    observation = env.observation_space.sample()
    r = env.observation_space.contains(env.game.state())

    print('Observation:\n', observation)
    print('Game State: \n', env.game.state())
    print('\n', r)

