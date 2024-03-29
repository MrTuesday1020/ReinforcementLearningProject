import matplotlib.pyplot as plt
import os
import re
import numpy as np


dirctory = 'data'

files = os.listdir(dirctory)
files = [i for i in files if re.match('performance_', i)]
x_axis = []
y_axis = []

#files = sorted(files)
#files = files[:50]

for item in sorted(files):
	with open(dirctory + '/' + item, 'r') as f:
		stop_cars = f.read()
		
	stop_cars = stop_cars[1:-1]
	stop_cars = sorted([int(i) for i in stop_cars.split(', ')])
	stop_cars = stop_cars[2:-2]
#	stop_cars = stop_cars[5:-5]
	
	mean_stop_cars = np.mean(stop_cars)
	
	y_axis.append(mean_stop_cars)
	
	
x_axis = [i for i in range(len(y_axis))]

mean = np.mean(y_axis)

mean_line = [mean for _ in range(len(y_axis))]

plt.plot(x_axis, y_axis)
plt.plot(x_axis, mean_line,label='mean=%d'%mean)
plt.ylabel('Performance measure')
plt.xlabel('Number of training')
plt.legend()
plt.savefig(dirctory + '/figure')
