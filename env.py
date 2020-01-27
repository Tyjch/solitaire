import gym
import gym.spaces as spaces
from pprint import pprint

class SolitaireEnv(gym.Env):
    # 1 for draw, 2-2,705 for move (target, source)

    action_space = spaces.Dict({
        'Action'      : spaces.Discrete(4),
        'Source Card' : spaces.Discrete(52),
        'Target Card' : spaces.Discrete(52)
    })
    observation_space = spaces.Dict({
        'Deck'  : spaces.MultiDiscrete([52 for x in range(24)]),
        'Waste' : spaces.MultiDiscrete([52 for y in range(3)]),
        'Foundations' : spaces.Dict({
            'spade'   : spaces.Discrete(52),
            'heart'   : spaces.Discrete(52),
            'club'    : spaces.Discrete(52),
            'diamond' : spaces.Discrete(52)
        }),
        'Tableaus' : spaces.Dict({
            '1st'  : spaces.MultiDiscrete([52 for a in range(19)]),
            '2nd'  : spaces.MultiDiscrete([52 for b in range(19)]),
            '3rd'  : spaces.MultiDiscrete([52 for c in range(19)]),
            '4th'  : spaces.MultiDiscrete([52 for d in range(19)]),
            '5th'  : spaces.MultiDiscrete([52 for e in range(19)]),
            '6th'  : spaces.MultiDiscrete([52 for f in range(19)]),
            '7th'  : spaces.MultiDiscrete([52 for g in range(19)]),
        }),
    })

    def __init__(self):
        pass

    def render(self, mode='human'):
        pass

    def step(self, action: object) -> (object, float, bool, dict):
        pass

    def reset(self) -> object:
        pass

    def seed(self, seed=None):
        pass

    def close(self):
        pass


if __name__ == '__main__':
    env = SolitaireEnv()
    pprint(env.action_space.sample(), width=1000)
    pprint(env.observation_space.sample(), width=1000)