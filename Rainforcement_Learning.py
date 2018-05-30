import numpy as np
import pandas as pd
import os.path


class RL(object):
    def __init__(self, action_space, alpha=0.1, gamma=0.9, e_greedy=0.9):
        self.actions = action_space  # Two actions: decide to switch or not.
        self.alpha = alpha    # Use learning rate: alpha = .1
        self.gamma = gamma   # Use discount factor: gamma = .9
        self.epsilon = e_greedy    # Epsilon-greedy exploration 10%
        if os.path.exists('qtable'):
            self.q_table = pd.read_csv('qtable')
        else:
            self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(pd.Series([0]*len(self.actions), index=self.q_table.columns, name=state))

    def choose_action(self, observation):
        self.check_state_exist(observation)
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
        self.q_table.to_csv('qtable')

# off-policy
class QLearningTable(RL):
    def __init__(self, actions=['switch', 'no_switch'], alpha=0.1, gamma=0.9, e_greedy=0.9):
        super(QLearningTable, self).__init__(actions, alpha, gamma, e_greedy)

    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        self.q_table.loc[s, a] += self.alpha * (q_target - q_predict)  # update


# on-policy
class SarsaTable(RL):

    def __init__(self, actions=['switch', 'no_switch'], alpha=0.1, gamma=0.9, e_greedy=0.9):
        super(SarsaTable, self).__init__(actions, alpha, gamma, e_greedy)

    def learn(self, s, a, r, s_, a_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        q_target = r + self.gamma * self.q_table.loc[s_, a_]  # next state is not terminal
        self.q_table.loc[s, a] += self.alpha * (q_target - q_predict)  # update

# backward eligibility traces
class SarsaLambdaTable(RL):
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9, trace_decay=0.9):
        super(SarsaLambdaTable, self).__init__(actions, learning_rate, reward_decay, e_greedy)

        # backward view, eligibility trace.
        self.lambda_ = trace_decay
        self.eligibility_trace = self.q_table.copy()

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            to_be_append = pd.Series([0] * len(self.actions),index=self.q_table.columns,name=state)
            self.q_table = self.q_table.append(to_be_append)

            # also update eligibility trace
            self.eligibility_trace = self.eligibility_trace.append(to_be_append)

    def learn(self, s, a, r, s_, a_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.loc[s_, a_]  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        error = q_target - q_predict

        # increase trace amount for visited state-action pair

        # Method 1:
        # self.eligibility_trace.loc[s, a] += 1

        # Method 2:
        self.eligibility_trace.loc[s, :] *= 0
        self.eligibility_trace.loc[s, a] = 1

        # Q update
        self.q_table += self.lr * error * self.eligibility_trace

        # decay eligibility trace after update
        self.eligibility_trace *= self.gamma*self.lambda_