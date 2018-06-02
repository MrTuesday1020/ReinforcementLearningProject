import matplotlib.pyplot as plt
import os
import re
import numpy as np


def axis(dirctory):
	files = os.listdir(dirctory)
	files = [i for i in files if re.match('performance_', i)]
	x_axis = []
	y_axis = []

	for item in sorted(files):
		with open(dirctory + '/' + item, 'r') as f:
			stop_cars = f.read()
		
		stop_cars = stop_cars[1:-1]
		stop_cars = sorted([int(i) for i in stop_cars.split(', ')])
		stop_cars = stop_cars[2:-2]
	
		mean_stop_cars = np.mean(stop_cars)
	
		y_axis.append(mean_stop_cars)
	
	x_axis = [i for i in range(len(y_axis))]
	return x_axis,y_axis


x_axis_1,y_axis_1 = axis('sarsa')
x_axis_1 = x_axis_1[:50]
y_axis_1 = y_axis_1[:50]
mean_1 = np.mean(y_axis_1)
mean_line_1 = [mean_1 for _ in range(len(y_axis_1))]
plt.plot(x_axis_1, y_axis_1)
plt.plot(x_axis_1, mean_line_1,label='egreedy=0.1;mean=%d'%mean_1)

x_axis_2,y_axis_2 = axis('eg1')
mean_2 = np.mean(y_axis_2)
mean_line_2 = [mean_2 for _ in range(len(y_axis_2))]
plt.plot(x_axis_2, y_axis_2)
plt.plot(x_axis_2, mean_line_2,label='egreedy=0.01;mean=%d'%mean_2)

x_axis_3,y_axis_3 = axis('eg2')
mean_3 = np.mean(y_axis_3)
mean_line_3 = [mean_3 for _ in range(len(y_axis_3))]
plt.plot(x_axis_3, y_axis_3)
plt.plot(x_axis_3, mean_line_3,label='egreedy=0.05;mean=%d'%mean_3)

x_axis_4,y_axis_4 = axis('eg3')
mean_4 = np.mean(y_axis_4)
mean_line_4 = [mean_4 for _ in range(len(y_axis_4))]
plt.plot(x_axis_4, y_axis_4)
plt.plot(x_axis_4, mean_line_4,label='egreedy=0.2;mean=%d'%mean_4)

plt.ylabel('Average Performance measure(1,000 time steps)')
plt.xlabel('Number of training(per 10,000 time-steps)')
plt.title('Different Epsilon-greedy Exploration')
plt.legend()
plt.savefig('pic/figure1_'+'sa_vs_greedy')
