from tkinter import *
import time
import random as rnd
import qlearning as ql
from extension import *

root = Tk()
# every 8px is a unit
unit = 8

canvas = Canvas(root, width = 100*unit , height = 100*unit, background='grey')
canvas.pack()
# width of a road is 8px
# the horizontal road
canvas.create_rectangle(0*unit, 49*unit, 100*unit, 51*unit, fill='black')
# the vertical road
canvas.create_rectangle(49*unit, 0*unit, 51*unit, 100*unit, fill='black')
# cars and lights are 4px*4px squares
light_11 = canvas.create_rectangle(48*unit, 48*unit, 49*unit, 49*unit, fill='spring green')
light_21 = canvas.create_rectangle(51*unit, 48*unit, 52*unit, 49*unit, fill='red2')
light_12 = canvas.create_rectangle(51*unit, 50*unit, 52*unit, 51*unit, fill='spring green')
light_22 = canvas.create_rectangle(49*unit, 51*unit, 50*unit, 52*unit, fill='red2')

master_clock = 0
road_11 = []
road_21 = []
road_12 = []
road_22 = []
number_of_car_on_raod_11 = 0
number_of_car_on_raod_21 = 0
number_of_car_on_raod_12 = 0
number_of_car_on_raod_22 = 0
# 0-8, 9 if no cars
closest_car_position_of_road_11 = 9
closest_car_position_of_road_21 = 9
closest_car_position_of_road_12 = 9
closest_car_position_of_road_22 = 9
# road1 light setting, 0:green, 1:red
light_setting = 0
amber_light = 0
light_delay = 0
# base case change time
base_case = 10
# a list that store the postions that have been occupied
block_list_11 = [49*unit]
block_list_21 = [49*unit]
block_list_12 = [50*unit]
block_list_22 = [50*unit]

closest_car_position_of_road1 = min(closest_car_position_of_road_11,closest_car_position_of_road_12)
closest_car_position_of_road2 = min(closest_car_position_of_road_21,closest_car_position_of_road_22)

length_of_experiment = 1000
replicaiton_of_experiment = 100

sum_of_stop_cars = 0
index_of_this_experiment = 0
performance_measure = []

observation = str(closest_car_position_of_road1)+str(closest_car_position_of_road2)+str(light_setting)+str(light_delay)

RL = ql.QLearningTable()

########################################### update observation ###########################################
#State = 
#closest car position from intersection for road 1 (0-8, 9 if no cars) X
#closest car position from intersection for road 2 (0-8, 9 if no cars X
#light setting (ie 0-green, 1 red for one of the roads) X
#light delay (0-3)

def closest_car(car_position, action, light_setting, clst_car_position_of_road, next_car_position):
	if car_position == 9:
		if clst_car_position_of_road > 9:	# 9 -> 9
			car_position = car_position
		elif clst_car_position_of_road == 9:	# 9 -> 8
			car_position -= 1
	elif car_position > 0:
		car_position -= 1
	elif car_position == 0:
		if next_car_position > 9:
			next_car_position = 10
		if action == 'switch':
			if light_setting == 1:	# red -> green
				car_position = next_car_position - 1
			else:	# green -> red
				car_position = car_position
		else:
			if light_setting == 1:	# red -> red
				car_position = car_position
			else:	# green -> green
				car_position = next_car_position - 1
	return car_position
	
def next_car_left(road,loc):
	closest_car_position_of_road = 10
	next_car_position = 10
	for car in road:
		px1 = canvas.coords(car[1])[0]
		if px1 < loc*unit:
			closest_car_position_of_road = int((loc*unit - px1) / unit)
			temp = road.index(car)
			if temp != len(road) - 1:
				px2 = canvas.coords(road[temp+1][1])[0]
				next_car_position = int((loc*unit - px2) / unit)
			break
	return closest_car_position_of_road,next_car_position
	
def next_car_right(road,loc):
	closest_car_position_of_road = 10
	next_car_position = 10
	for car in road:
		px1 = canvas.coords(car[1])[0]
		if px1 > loc*unit:
			closest_car_position_of_road = int((px1 - loc*unit) / unit)
			temp = road.index(car)
			if temp != len(road) - 1:
				px2 = canvas.coords(road[temp+1][1])[0]
				next_car_position = int((px2 - loc*unit) / unit)
			break
	return closest_car_position_of_road,next_car_position
	
def next_car_down(road,loc):
	closest_car_position_of_road = 10
	next_car_position = 10
	for car in road:
		px1 = canvas.coords(car[1])[1]
		if px1 < loc*unit:
			closest_car_position_of_road = int((loc*unit - px1) / unit)
			temp = road.index(car)
			if temp != len(road) - 1:
				px2 = canvas.coords(road[temp+1][1])[1]
				next_car_position = int((loc*unit - px2) / unit)
			break
	return closest_car_position_of_road,next_car_position
	
def next_car_up(road,loc):
	closest_car_position_of_road = 10
	next_car_position = 10
	for car in road:
		px1 = canvas.coords(car[1])[1]
		if px1 > loc*unit:
			closest_car_position_of_road = int((px1 - loc*unit) / unit)
			temp = road.index(car)
			if temp != len(road) - 1:
				px2 = canvas.coords(road[temp+1][1])[1]
				next_car_position = int((px2 - loc*unit) / unit)
			break
	return closest_car_position_of_road,next_car_position
	
def update_state(action, observation, road_11, road_21, road_12, road_22):
	closest_car_position_of_road_11,next_car_position_11 = next_car_left(road_11,49)
	closest_car_position_of_road_12,next_car_position_12 = next_car_right(road_12,50)
	closest_car_position_of_road_21,next_car_position_21 = next_car_down(road_21,49)
	closest_car_position_of_road_22,next_car_position_22 = next_car_up(road_22,50)

	closest_car_position_of_road1 = min(closest_car_position_of_road_11,closest_car_position_of_road_12)
	next_car_position1 = min(next_car_position_11,next_car_position_12)
	closest_car_position_of_road2 = min(closest_car_position_of_road_21,closest_car_position_of_road_22)
	next_car_position2 = min(next_car_position_21,next_car_position_22)
	
	closest_car_position_of_road1 = closest_car(int(observation[0]), action, observation[2], closest_car_position_of_road1, next_car_position1)
	closest_car_position_of_road2 = closest_car(int(observation[1]), action, observation[2], closest_car_position_of_road2, next_car_position2)
 	
	if action == 'switch':
		if observation[2] == '0':
			light_setting = 1
		else:
			light_setting = 0
		light_delay = 0
	else:
		light_setting = int(observation[2])
		
		if observation[3] != '3':
			light_delay = int(observation[3]) + 1
		else:
			light_delay = int(observation[3])
		
	observation = str(closest_car_position_of_road1)+str(closest_car_position_of_road2)+str(light_setting)+str(light_delay)
	return observation
	
########################################### move ###########################################

def move_left(road,block_list,loc):
	for car in road:
		position = canvas.coords(car[1])[0]
		# if the car has passed the intersection just move foreward
		if position >= loc*unit:
			canvas.move(car[1], unit, 0)
		else:
			if (position + unit) in block_list:
				if position not in block_list:
					block_list.append(position)
			else:
				canvas.move(car[1], unit, 0)
	return block_list

def move_right(road,block_list,loc):
	for car in road:
		position = canvas.coords(car[1])[0]
		if position <= loc*unit:
			canvas.move(car[1], -unit, 0)
		else:
			if (position - unit) in block_list:
				if position not in block_list:
					block_list.append(position)
			else:
				canvas.move(car[1], -unit, 0)
	return block_list
	
def move_down(road,block_list,loc):
	for car in road:
		position = canvas.coords(car[1])[1]
		if position >= loc*unit:
			canvas.move(car[1], 0, unit)
		else:
			if (position + unit) in block_list:
				if position not in block_list:
					block_list.append(position)
			else:
				canvas.move(car[1], 0, unit)
	return block_list
	
def move_up(road,block_list,loc):
	for car in road:
		position = canvas.coords(car[1])[1]
		if position <= loc*unit:
			canvas.move(car[1], 0, -unit)
		else:
			if (position - unit) in block_list:
				if position not in block_list:
					block_list.append(position)
			else:
				canvas.move(car[1], 0, -unit)
	return block_list

########################################### main loop ###########################################

while master_clock <= length_of_experiment * replicaiton_of_experiment:
	
	# delete cars which have move outside the canvas
	road_11 = [car for car in road_11 if canvas.coords(car[1])[0] <= 100*unit]
	road_12 = [car for car in road_12 if canvas.coords(car[1])[0] >= 0*unit]
	road_21 = [car for car in road_21 if canvas.coords(car[1])[1] <= 100*unit]
	road_22 = [car for car in road_22 if canvas.coords(car[1])[1] >= 0*unit]
	
	# choose action
	if light_delay <= 2:
		action = 'no_switch'
		RL.check_state_exist(observation)
	else:
		action = RL.choose_action(observation)
	
	# chaneg light setting
	if amber_light != 0:
		if amber_light == 1:	# road1: yellow -> red; road2: red -> green
			canvas.itemconfig(light_11, fill='red2')
			canvas.itemconfig(light_12, fill='red2')
			canvas.itemconfig(light_21, fill='spring green')
			canvas.itemconfig(light_22, fill='spring green')
		else:	# road2: yellow -> red; road1: red -> green
			canvas.itemconfig(light_21, fill='red2')
			canvas.itemconfig(light_22, fill='red2')
			canvas.itemconfig(light_11, fill='spring green')
			canvas.itemconfig(light_12, fill='spring green')
		amber_light = 0
	
	if action == 'switch':
		light_delay = -1
		block_list_11 = [49*unit]
		block_list_12 = [50*unit]
		block_list_21 = [49*unit]
		block_list_22 = [50*unit]
		if light_setting == 0:	# road1: green -> yellow; road2: red -> red
			light_setting = 1
			amber_light = 1
			canvas.itemconfig(light_11, fill='blue')
			canvas.itemconfig(light_12, fill='blue')
		else:	# road2: green -> yellow; road1: red -> red
			light_setting = 0
			amber_light = 2
			canvas.itemconfig(light_21, fill='blue')
			canvas.itemconfig(light_22, fill='blue')

	# car move
	if light_setting == 0:
		if amber_light == 0:
			for car in road_11:
				canvas.move(car[1], unit, 0)
			for car in road_12:
				canvas.move(car[1], -unit, 0)
		else:
			block_list_11 = move_left(road_11,block_list_11,49)
			block_list_12 = move_right(road_12,block_list_12,50)
		block_list_22 = move_up(road_22,block_list_22,50)
		block_list_21 = move_down(road_21, block_list_21,49)
	else:
		if amber_light == 0:
			for car in road_21:
				canvas.move(car[1], 0, unit)
			for car in road_22:
				canvas.move(car[1], 0, -unit)
		else:
			block_list_21 = move_down(road_21,block_list_21,49)
			block_list_22 = move_up(road_22,block_list_22,50)
		block_list_11 = move_left(road_11,block_list_11,49)
		block_list_12 = move_right(road_12,block_list_12,50)
					

	# car appear
	if master_clock % (rnd.randint(1, 8) ) == 0:
		randappear = rnd.random()
		if randappear > 0.75:
			# generate a car on road_11
			car_name = 'car' + str(number_of_car_on_raod_11)
			car = canvas.create_rectangle(0, 49*unit, unit, 50*unit, fill='grey')
			road_11.append([car_name, car])
			number_of_car_on_raod_11 += 1
		elif randappear > 0.5:
			# generate a car on road_12
			car_name = 'car' + str(number_of_car_on_raod_12)
			car = canvas.create_rectangle(99*unit, 50*unit, 100*unit, 51*unit, fill='grey')
			road_12.append([car_name, car])
			number_of_car_on_raod_12 += 1
		elif randappear > 0.25:
			# generate a car on road_22
			car_name = 'car' + str(number_of_car_on_raod_22)
			car = canvas.create_rectangle(49*unit, 99*unit, 50*unit, 100*unit, fill='white')
			road_22.append([car_name, car])
			number_of_car_on_raod_22 += 1
		else:
			# generate a car on road_21
			car_name = 'car' + str(number_of_car_on_raod_21)
			car = canvas.create_rectangle(50*unit, 0, 51*unit, unit, fill='white')
			road_21.append([car_name, car])
			number_of_car_on_raod_21 += 1	
	root.update()
	
	# next state
	observation_ = update_state(action, observation, road_11, road_21, road_12, road_22)
	
	
	# Reward -1.0 if a car is stopped at a red light on either road, zero otherwise.
	if len(block_list_11) > 1 or len(block_list_12) > 1 or len(block_list_21) > 1 or len(block_list_22) > 1:
		reward = -1
	else:
		reward = 0
	
	# coompute the amount of stop cars
	stop_cars = len(block_list_11) + len(block_list_12) + len(block_list_21) + len(block_list_22) - 4
	sum_of_stop_cars += stop_cars
	index_of_this_experiment += 1
	if index_of_this_experiment == length_of_experiment:
		print(sum_of_stop_cars)
		performance_measure.append(sum_of_stop_cars)
		sum_of_stop_cars = 0
		index_of_this_experiment = 0
	
	# learning
	RL.learn(observation, action, reward, observation_)
	
	observation = observation_
	light_delay += 1
	master_clock += 1

with open('performance_measure', 'w') as f:
	f.write(str(performance_measure))

RL.save_table()

root.mainloop()

#Optimise discounted sum of future reward.