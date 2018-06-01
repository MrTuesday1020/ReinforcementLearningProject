import numpy as np
import pandas as pd
import os.path


class RL(object):
    def __init__(self, action_space, alpha, gamma, e_greedy):
        self.actions = action_space  # Two actions: decide to switch or not.
        self.alpha = alpha    # Use learning rate: alpha = .1
        self.gamma = gamma   # Use discount factor: gamma = .9
        self.epsilon = e_greedy    # Epsilon-greedy exploration 10%
        if os.path.exists('qtable.txt'):
            self.q_table = pd.read_csv('qtable.txt', names=['switch', 'no_switch'], header=None)
        else:
            self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            new_row = pd.Series([0]*len(self.actions), index=self.q_table.columns, name=state)
            self.q_table = self.q_table.append(new_row)
            return False
        return True

    def choose_action(self, observation):
        exist = self.check_state_exist(observation)
        # Epsilon-greedy choice
        if np.random.rand() < self.epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))     # some actions have same value
            action = state_action.idxmax()
#            action = state_action.argmax()
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def learn(self, *args):
        pass
            
    def save_table(self):
        self.q_table.to_csv('qtable.txt', header=None)

# off-policy
class QLearningTable(RL):
    def __init__(self, actions=['switch', 'no_switch'], alpha=0.1, gamma=0.9, e_greedy=0.9):
        super(QLearningTable, self).__init__(actions, alpha, gamma, e_greedy)

    def learn(self, s, a, r, s_):
        exist = self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        self.q_table.loc[s, a] += self.alpha * (q_target - q_predict)  # update

# on-policy
class SarsaTable(RL):

    def __init__(self, actions=['switch', 'no_switch'], alpha=0.1, gamma=0.9, e_greedy=0.01):
        super(SarsaTable, self).__init__(actions, alpha, gamma, e_greedy)

    def learn(self, s, a, r, s_, a_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        q_target = r + self.gamma * self.q_table.loc[s_, a_]  # next state is not terminal
        self.q_table.loc[s, a] += self.alpha * (q_target - q_predict)  # update
