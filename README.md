# ReinforcementLearningProject

## Moduel

Tkinter(canvas): Tkinter is used to establish a visible window to simulate the environment. Then we create roads, cars and roads by canvas. And we make animations by canvas.move function to simulate the move of the cars.

## Code
1. Basecase.py
We firstly import tkinter module to get a visible window to simulate the intersecting roads, cars and traffic lights, in order that we can see what is happening when cars are running. At the beginning, we set up the simulation with a base case 10 time-steps switching, then use a reinforcement learning algorithm to improve it.


The learning process takes place according to the observation and actions. At each time-step, an action is selected by the learn function which finally return a optimal choice or random choice by epsilon-greedy exploration.

2. TrafficLightSimulator.py

3. ReinforcementLearning.py

4. Analysis.py
