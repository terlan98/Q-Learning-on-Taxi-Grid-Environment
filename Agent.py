import random
import time
from threading import Thread

import numpy as np
import gym
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

env = gym.make('Taxi-v3').env


def visualize_training(episodes, total_rewards, total_epochs, epoch_rewards):
    plt.plot(episodes, total_rewards)
    plt.xlabel('Episode Number', )
    plt.ylabel('Reward Value')

    plt.title('Reward Values on Each Episode')
    plt.legend()
    plt.show()

    print('Average reward per episode: {}'.format(
        sum(total_rewards) / len(total_rewards)))


class Agent:
    def __init__(self, alpha=0.1, gamma=0.6, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = dict()
        self.cur_state = None
        self.done = False

    @ classmethod
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

        return list(env.decode(self.cur_state)), action, reward

    def evaluate_agent(self, num_episodes):
        episodes = []
        episode_rewards = []
        epoch_rewards = []
        total_epochs = 0

        for episode_idx in range(num_episodes):
            self.cur_state = env.reset()
            self.done = False
            episode_reward = 0

            while not self.done:
                _, _, reward = self.make_move()
                episode_reward += reward
                epoch_rewards.append(reward)
                total_epochs += 1

            episodes.append(episode_idx)
            episode_rewards.append(episode_reward)

        return episodes, episode_rewards, total_epochs, epoch_rewards

    def get_argmax_q(self):
        action_vals = self.get_q_values(self.cur_state)
        argmax_action = max(action_vals, key=action_vals.get)
        return argmax_action

    @ staticmethod
    def train(num_episodes=100000):
        agent = Agent()

        episodes = []
        episode_rewards = []
        epoch_rewards = []
        total_epochs = 0

        for cur_episode in range(num_episodes):
            agent.cur_state = env.reset()
            agent.done = False
            episode_reward = 0

            if cur_episode % 10000 == 0:
                print('Current episode:', cur_episode)

            while not agent.done:
                _, _, reward = agent.make_move()
                episode_reward += reward
                epoch_rewards.append(reward)
                total_epochs += 1

            episodes.append(cur_episode)
            episode_rewards.append(episode_reward)

        visualize_training(episodes, episode_rewards,
                           total_epochs, epoch_rewards)

        return Agent.from_trained(agent.q_table, env.reset())
