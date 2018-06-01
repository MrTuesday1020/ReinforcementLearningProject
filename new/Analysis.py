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


x_axis_1,y_axis_1 = axis('sarsa0')
mean_1 = np.mean(y_axis_1)
mean_line_1 = [mean_1 for _ in range(len(y_axis_1))]
plt.plot(x_axis_1, y_axis_1)
plt.plot(x_axis_1, mean_line_1,label='mean=%d'%mean_1)

x_axis_2,y_axis_2 = axis('data')
mean_2 = np.mean(y_axis_2)
mean_line_2 = [mean_2 for _ in range(len(y_axis_1))]
plt.plot(x_axis_2, y_axis_2)
plt.plot(x_axis_2, mean_line_2,label='mean=%d'%mean_2)

plt.ylabel('Performance measure')
plt.xlabel('Number of training')
plt.legend()
plt.savefig('pic/figure_'+'sa0_ql0')
