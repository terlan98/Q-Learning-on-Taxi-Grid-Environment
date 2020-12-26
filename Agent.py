import random
import time
from threading import Thread

from GameController import GameController, Action
from pynput.keyboard import Key, KeyCode

DUMMY_MAP = [  # original
    ["#", "#", "#", "#", "#", "#", "#"],
    ["#", "=", "=", "#", "=", "=", "#"],
    ["#", "=", "=", "#", "F", "=", "#"],
    ["#", "=", "=", "=", "=", "=", "#"],
    ["#", "=", "=", "T", "=", "=", "#"],
    ["#", "S", "=", "=", "=", "=", "#"],
    ["#", "#", "#", "#", "#", "#", "#"]
]


def flatten(grid):
    return ''.join([char for row in grid for char in row])


class Agent:

    # actions = ['NORTH', 'SOUTH', 'EAST', 'WEST', 'PICK-UP', 'DROP-OFF']

    def __init__(self, env, alpha=0.1, gamma=1.0, epsilon=0.1):
        env.putMarkers()
        self.cur_state = flatten(env.currentGrid)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.env = env
        self.q_table = dict()

    @classmethod
    def from_trained(cls, env, q_table, initial_state):
        agent = cls(env, alpha=0.0, gamma=0.0, epsilon=0.0)
        agent.q_table = q_table
        agent.cur_state = initial_state
        return agent

    def get_q_values(self, state):
        enc_state = flatten(state)

        if enc_state not in self.q_table:
            action_value_pairs = {action: 0 for action in Action}
            self.q_table.update({flatten(enc_state): action_value_pairs})

        return self.q_table[enc_state]

    def make_move(self):
        if random.random() < self.epsilon:
            action = random.choice(list(Action))
        else:
            action = self.get_argmax_q()

        # print('Picked action:', action)

        next_state, reward = flatten(self.env.step(
            action)), self.env.getReward(action)

        old_value = self.get_q_values(self.cur_state)[action]
        next_state_max = max(self.get_q_values(next_state).values())

        new_value = (1 - self.alpha) * old_value + self.alpha * \
            (reward + self.gamma * next_state_max)
        self.q_table[self.cur_state][action] = new_value

        self.cur_state = next_state

        actionToKeyMap = {Action.NORTH: Key.up,
                          Action.SOUTH: Key.down,
                          Action.WEST: Key.left,
                          Action.EAST: Key.right,
                          Action.PICK_UP: KeyCode(char='p'),
                          Action.DROP_OFF: KeyCode(char='d')}

        self.env.on_press(actionToKeyMap[action])

    def get_argmax_q(self):
        action_vals = self.get_q_values(self.cur_state)
        argmax_action = max(action_vals, key=action_vals.get)
        return argmax_action


def printGrid(grid):
    """Prints the given grid"""
    print()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print(grid[i][j], end=" ")
        print()


def print_q_table(q_table):
    """Prints the given Q-table"""
    for state in q_table.keys():
        print(state, end=" ")
        for action in q_table[state]:
            print(action, end=" ")
        print()


if __name__ == "__main__":
    env = GameController(isTraining=True)
    # env.run()

    thread = Thread(target=env.run)
    thread.start()

    agent = Agent(env, alpha=0.8)

    initial_state = agent.cur_state

    num_epochs = 100

    while num_epochs:
        print('Current epoch:', num_epochs)

        agent.make_move()
        num_epochs -= 1

    greedy_agent = Agent.from_trained(env, agent.q_table, initial_state)

    while True:
        agent.make_move()
        time.sleep(2)
