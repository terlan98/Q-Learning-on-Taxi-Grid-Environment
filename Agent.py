import random

DUMMY_MAP = [  # original
    ["#", "#", "#", "#", "#", "#", "#"],
    ["#", "=", "=", "#", "=", "=", "#"],
    ["#", "=", "=", "#", "F", "=", "#"],
    ["#", "=", "=", "=", "=", "=", "#"],
    ["#", "=", "=", "T", "=", "=", "#"],
    ["#", "S", "=", "=", "=", "=", "#"],
    ["#", "#", "#", "#", "#", "#", "#"]
]


class Agent:

    q_table = dict()
    # actions = ['NORTH', 'SOUTH', 'EAST', 'WEST', 'PICK-UP', 'DROP-OFF']

    def __init__(startState, env, alpha=0.1, gamma=1.0, epsilon=0.1):
        self.cur_state = startState
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.env = env

    def get_q_values(self, state):
        if state not in self.q_able:
            action_value_pairs = {action: 0 for action in self.env.Action}
            self.q_table.update({state: action_value_pairs})

        return self.q_table[state]

    def make_move(self):
        if random.random() < self.epsilon:
            action = random.choice(self.env.Action)
        else:
            action = self.get_argmax_q()

        next_state, reward = self.env.step(action), self.env.getReward(action)

        old_value = self.q_table[self.cur_state][action]
        next_state_max = max(self.q_table[next_state].values())

        new_value = (1 - self.alpha) * old_value + self.alpha * \
            (reward + self.gamma * next_state_max)
        self.q_table[self.cur_state][action] = new_value

        self.cur_state = next_state

    def get_argmax_q(self):
        action_vals = self.q_table[self.cur_state]
        argmax_action = max(action_vals, key=action_vals.get)
        return argmax_action


if __name__ == "__init__":
    pass


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
