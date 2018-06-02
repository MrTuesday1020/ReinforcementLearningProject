# Reinforcement Learning Project

## Moduel

**Tkinter(canvas)**: 

Tkinter is used to establish a visible window to simulate the environment. Then we create roads, cars and roads by canvas. And we make animations by canvas.move function to simulate the move of the cars.

**Random**: 

Random lib is used to generate cars randomly.

**Numpy and Pandas**: 

We use this two libs to process and analyse data in a convenient way.

**Matplotlib**: 

We use this lib to convert data into high quality figures and help us analyse data in a more efficient method.



## Code

**1. TrafficLightSimulator.py**: 

In this script, we firstly build up an traffic light simulator by Tkinter. We denote that every 8 pxiel is a unit. Cars and traffict lights are 1 unit * 1 unit squares. The length of each road is 100 unit and the width is 1 unit. And we assume that the intersection is in the exactly middle of the environment. In the main part of this python script, we do loops and each iteration is a time step. So every time the simulator arrives a new time step, there are few things we need to do. First we need to choose an action according to the result of reinforcement learning. Then we update the states of every car and traffic light. So we have move functions to move cars according to the light setting on each road. Then, we generate new cars on roads randomly. After updating the environment, we need to provide the state value and reward value to Reinforcement Learning algorithm to learn. At the same time, the number of cars will be recorded at each time step and the sum of numbers of cars stopped in the period of 1000 time steps will be the performance measure.


**2. ReinforcementLearning.py**

In this python file, we have a class called RL(Reinforcement Learning) and two Reinforcement Learning algorithms inherit it: Q-learning and Sarsa. Here are the function and paramater explainations:

***actions***: a list contain 2 actions: decide to switch or not.

***alpha***: learning rate

***gamma***: discount factor

***epsilon***: epsilon greedy exploration rate

***q_table***: a table to store vlaues after each learning



**check_state_exist function**: if the state is not in q_table, append the state into the table and return false, otherwise, retuen true.

**choose_action function**: choose action according to the current state.

**learn function**: learn according to the reward and state and uppdate q table.
