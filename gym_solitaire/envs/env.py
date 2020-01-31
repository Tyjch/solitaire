import gym, random
import gym.spaces as spaces
from solitaire import Game
from utility import get_card
from pprint import pprint


class SolitaireEnv(gym.Env):
    action_space = spaces.Discrete(8)
    observation_space = spaces.Dict({
        'Deck'  : spaces.Tuple([spaces.Discrete(59) for x in range(24)]),
        'Waste' : spaces.Tuple([spaces.Discrete(59) for y in range(24)]),
        'Legal Moves' : spaces.Tuple([spaces.Tuple([spaces.Discrete(58) for v in range(2)]) for z in range(8)]),
        'Foundations' : spaces.Dict({
            's' : spaces.Discrete(59),
            'h' : spaces.Discrete(59),
            'c' : spaces.Discrete(59),
            'd' : spaces.Discrete(59)
        }),
        'Tableaus' : spaces.Dict({
            '1st'  : spaces.Tuple([spaces.Discrete(59) for a in range(19)]),
            '2nd'  : spaces.Tuple([spaces.Discrete(59) for b in range(19)]),
            '3rd'  : spaces.Tuple([spaces.Discrete(59) for c in range(19)]),
            '4th'  : spaces.Tuple([spaces.Discrete(59) for d in range(19)]),
            '5th'  : spaces.Tuple([spaces.Discrete(59) for e in range(19)]),
            '6th'  : spaces.Tuple([spaces.Discrete(59) for f in range(19)]),
            '7th'  : spaces.Tuple([spaces.Discrete(59) for g in range(19)]),
        }),
    })

    def __init__(self, env_config):
        random.seed()
        self.game  = Game()
        self.round = 0

    def render(self, mode='human'):
        if mode == 'human':
            print(f'\nRound {self.round}', '==' * 100)
            self.game.render()

    def step(self, action: object):
        state, reward, done, info = self.game.state(), 0.0, False, {}

        if action == 0:
            #print('Action: Ending Game')
            done = True

        elif action == 1:
            #print('Action: Drawing Cards')
            reward = self.game.get_draw_reward()
            self.game.deck.draw()

        else:
            #print('Action: Moving Cards')
            legal_moves = state['Legal Moves']
            try:
                action = legal_moves[int(action) - 2]
                if isinstance(action, tuple) and action != (0, 0):
                    target = self.find_card(action[0])
                    source = self.find_card(action[1])
                    move   = (target, source)

                    if move in self.game.legal_moves():
                        reward = self.game.get_move_reward(move)
                        self.game.move_cards(move)
                    else:
                        #print('Not a legal move')
                        pass
                else:
                    #print('The move corresponding to this action is empty')
                    pass
            except IndexError:
                #print('Action not in action space')
                pass

        self.round += 1
        return self.game.state(), reward, done, info

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
    env.reset()
    env.render()

    for i in range(100):
        sample = env.action_space.sample()
        print('Action:', sample)
        env.step(sample)
        env.render()
