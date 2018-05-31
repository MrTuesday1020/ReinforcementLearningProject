import matplotlib.pyplot as plt
import os
import re
import numpy as np

dirctory = 'qlearning1'
files = os.listdir(dirctory)
files = [i for i in files if re.match('performance_', i)]
x_axis = []
y_axis = []
x_axis_1 = []
y_axis_1 = []

for item in sorted(files):
	with open(dirctory + '/' + item, 'r') as f:
		stop_cars = f.read()
		
	stop_cars = stop_cars[1:-1]
	stop_cars_1 = stop_cars[1:-1]
	stop_cars = [int(i) for i in stop_cars.split(', ')]
	
	temp0 = stop_cars[0:10]
	temp1 = stop_cars[10:20]
	temp2 = stop_cars[20:30]
	temp3 = stop_cars[30:40]
	temp4 = stop_cars[40:50]
	
	
	y_axis.append(np.mean(temp0))
	y_axis.append(np.mean(temp1))
	y_axis.append(np.mean(temp2))
	y_axis.append(np.mean(temp3))
	y_axis.append(np.mean(temp4))
	
	
	stop_cars_1 = stop_cars[5:-5]
	
	mean_stop_cars = np.mean(stop_cars_1)
	
	y_axis_1.append(mean_stop_cars)
	
	
x_axis_1 = [(i+1)*5 for i in range(len(y_axis_1))]

	
x_axis = [i for i in range(len(y_axis))]

plt.plot(x_axis, y_axis)
plt.plot(x_axis_1, y_axis_1)
plt.ylabel('Performance measure')
plt.xlabel('Number of training')
plt.show()
#plt.savefig(dirctory + '/figure')