import random
import time
from threading import Thread

import numpy as np
import gym

env = gym.make('Taxi-v3').env


class Agent:
    def __init__(self, alpha=0.1, gamma=0.6, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = dict()
        self.cur_state = None
        self.done = False

    @classmethod
    def from_trained(cls, q_table, initial_state):
        agent = cls(alpha=0.0, gamma=0.0, epsilon=0.0)
        agent.q_table = q_table
        agent.cur_state = initial_state
        return agent

    def get_q_values(self, state):
        if state not in self.q_table:
            action_value_pairs = {
                action: 0 for action in range(env.action_space.n)}
            self.q_table.update({state: action_value_pairs})

        return self.q_table[state]

    def make_move(self):
        if random.uniform(0, 1) < self.epsilon:
            action = env.action_space.sample()
        else:
            action = self.get_argmax_q()

        next_state, reward, done, _ = env.step(action)

        old_value = self.get_q_values(self.cur_state)[action]
        next_state_max = max(self.get_q_values(next_state).values())

        new_value = (1 - self.alpha) * old_value + self.alpha * \
            (reward + self.gamma * next_state_max)

        self.q_table[self.cur_state][action] = new_value
        self.cur_state = next_state
        self.done = done

        return list(env.decode(self.cur_state)), action

    def get_argmax_q(self):
        action_vals = self.get_q_values(self.cur_state)
        argmax_action = max(action_vals, key=action_vals.get)
        return argmax_action

    @staticmethod
    def train(num_epochs=100000):
        agent = Agent()
        for cur_epoch in range(num_epochs):
            agent.cur_state = env.reset()
            agent.done = False

            if cur_epoch % 10000 == 0:
                print('Current epoch:', cur_epoch)

            while not agent.done:
                agent.make_move()

        return Agent.from_trained(agent.q_table, env.reset())
