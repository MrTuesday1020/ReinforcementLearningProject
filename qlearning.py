import numpy as np
import pandas as pd

class QLearningTable:
	def __init__(self, actions=['switch', 'no_switch'], gamma=0.9, alpha=0.1, e_greedy=0.9):
		self.actions = actions	# Two actions: decide to switch or not.
		self.gamma = gamma	# Use discount factor: gamma = .9
		self.alpha = alpha	# Use learning rate: alpha = .1
		self.epsilon = e_greedy	# Epsilon-greedy exploration 10%
		self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

	def choose_action(self, observation):
		self.check_state_exist(observation)
		# Epsilon-greedy choice
		if np.random.uniform() < self.epsilon:	
			state_action = self.q_table.loc[observation,:]
			state_action = state_action.reindex(np.random.permutation(state_action.index))
			action = state_action.argmax()
		# random choice
		else:
			action = np.random.choice(self.actions)
		return action

	def learn(self, s, a, r, s_):
		self.check_state_exist(s_)
		q_predict = self.q_table.loc[s,a]
		q_target = r + self.gamma * self.q_table.loc[s_,:].max()
		self.q_table.loc[s, a] += self.alpha * (q_target - q_predict)

	def check_state_exist(self, state):
		if state not in self.q_table.index:
			self.q_table = self.q_table.append(pd.Series([0]*len(self.actions),index=self.q_table.columns,name=state))
			
	def print_table(self):
		self.q_table.to_csv('qtable', sep='\t')
		