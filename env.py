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
light_11 = canvas.create_rectangle(48*unit, 49*unit, 49*unit, 50*unit, fill='spring green')
light_21 = canvas.create_rectangle(50*unit, 48*unit, 51*unit, 49*unit, fill='red2')
light_12 = canvas.create_rectangle(51*unit, 50*unit, 52*unit, 51*unit, fill='spring green')
light_22 = canvas.create_rectangle(49*unit, 51*unit, 50*unit, 52*unit, fill='red2')

master_clock = 0
#road1 = []
#road2 = []
road_11 = []
road_21 = []
road_12 = []
road_22 = []
#number_of_car_on_raod1 = 0
#number_of_car_on_raod2 = 0
number_of_car_on_raod_11 = 0
number_of_car_on_raod_21 = 0
number_of_car_on_raod_12 = 0
number_of_car_on_raod_22 = 0
# 0-8, 9 if no cars
#closest_car_position_of_road1 = 9
#closest_car_position_of_road2 = 9
closest_car_position_of_road_11 = 9
closest_car_position_of_road_21 = 9
closest_car_position_of_road_12 = 9
closest_car_position_of_road_22 = 9
# road1 light setting, 0:green, 1:red
light_setting = 0
light_delay = 0
# a fixed change time
change_time = 10
# a list that store the postions that have been occupied
#block_list1 = [49*unit]
#block_list2 = [49*unit]
block_list_11 = [49*unit]
block_list_21 = [49*unit]
block_list_12 = [50*unit]
block_list_22 = [50*unit]

closest_car_position_of_road1 = min(closest_car_position_of_road_11,closest_car_position_of_road_12)
closest_car_position_of_road2 = min(closest_car_position_of_road_21,closest_car_position_of_road_22)

length_of_experiment = 1000
replicaiton_of_experiment = 100

sum_of_reward = 0
index_of_this_experiment = 0
reward_list = []

observation = str(closest_car_position_of_road1)+str(closest_car_position_of_road2)+str(light_setting)+str(light_delay)

def next_car(road,direction,revers):
	closest_car_position_of_road = 10
	next_car_position = 10
	for car in road:
		px1 = canvas.coords(car[1])[direction]
		#px1 = canvas.coords(car[1])[1]	-> road2
		if not revers:
			if px1 < 49*unit:
				closest_car_position_of_road = int((49*unit - px1) / unit)
				temp = road.index(car)
				if temp != len(road) - 1:
					px2 = canvas.coords(road[temp+1][1])[direction]
					#px2 = canvas.coords(road2[temp+1][1])[1]
					next_car_position = int((49*unit - px2) / unit)
				break
		else:
			if px1 > 49*unit:
				closest_car_position_of_road = int((px1 - 49*unit) / unit)
				temp = road.index(car)
				if temp != len(road) - 1:
					px2 = canvas.coords(road[temp+1][1])[direction]
					#px2 = canvas.coords(road2[temp+1][1])[1]
					next_car_position = int((px2 - 49*unit) / unit)
				break
	return closest_car_position_of_road,next_car_position

def update_state(action, observation, road_11, road_21, road_12, road_22):
	
	closest_car_position_of_road_11,next_car_position_11 = next_car(road_11,0,False)
	closest_car_position_of_road_12,next_car_position_12 = next_car(road_12,0,True)
	closest_car_position_of_road1 = min(closest_car_position_of_road_11,closest_car_position_of_road_12)
	next_car_position1 = min(next_car_position_11,next_car_position_12)
	
	closest_car_position_of_road_21,next_car_position_21 = next_car(road_21,1,False)
	closest_car_position_of_road_22,next_car_position_22 = next_car(road_22,1,True)
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

observation = str(closest_car_position_of_road1)+str(closest_car_position_of_road2)+str(light_setting)+str(light_delay)

RL = ql.QLearningTable()
#last_switch_time = master_clock

########################################### main loop ###########################################

while master_clock <= length_of_experiment * replicaiton_of_experiment:
	
	if light_delay <= 2:
		action = 'no_switch'
		RL.check_state_exist(observation)
	else:
		action = RL.choose_action(observation)
		
#	if action == 'switch':
#		print(master_clock-last_switch_time)
#		last_switch_time = master_clock
	
	# chaneg light setting
	if action == 'switch':
		light_delay = -1
		if light_setting == 0:
			light_setting = 1
			block_list_11 = [49*unit]
			block_list_12 = [50*unit]
			canvas.itemconfig(light_11, fill='red2')
			canvas.itemconfig(light_12, fill='red2')
			canvas.itemconfig(light_21, fill='spring green')
			canvas.itemconfig(light_22, fill='spring green')
		else:
			light_setting = 0
			block_list_21 = [49*unit]
			block_list_22 = [50*unit]
			canvas.itemconfig(light_11, fill='spring green')
			canvas.itemconfig(light_12, fill='spring green')
			canvas.itemconfig(light_21, fill='red2')
			canvas.itemconfig(light_22, fill='red2')
	
	if light_setting == 0:
		for car in road_11:
			canvas.move(car[1], unit, 0)
		for car in road_12:
			canvas.move(car[1], -unit, 0)
		for car in road_21:
			position = canvas.coords(car[1])[1]
			# if the car has passed the intersection just move foreward
			if position >= 49*unit:
				# move down a unit
				canvas.move(car[1], 0, unit)
			else:
				if (position + unit) in block_list_21:
					if position not in block_list_21:
						block_list_21.append(position)
				else:
					canvas.move(car[1], 0, unit)
		for car in road_22:
			position = canvas.coords(car[1])[1]
			# if the car has passed the intersection just move foreward
			if position <= 50*unit:
				# move down a unit
				canvas.move(car[1], 0, -unit)
			else:
				if (position - unit) in block_list_22:
					if position not in block_list_22:
						block_list_22.append(position)
				else:
					canvas.move(car[1], 0, -unit)
	else:
		for car in road_21:
			canvas.move(car[1], 0, unit)
		for car in road_22:
			canvas.move(car[1], 0, -unit)
		for car in road_11:
			position = canvas.coords(car[1])[0]
			# if the car has passed the intersection just move foreward
			if position >= 49*unit:
				# move right a unit
				canvas.move(car[1], unit, 0)
			else:
				if (position + unit) in block_list_11:
					if position not in block_list_11:
						block_list_11.append(position)
				else:
					canvas.move(car[1], unit, 0)
		for car in road_12:
			position = canvas.coords(car[1])[0]
			# if the car has passed the intersection just move foreward
			if position <= 50*unit:
				# move right a unit
				canvas.move(car[1], -unit, 0)
			else:
				if (position - unit) in block_list_12:
					block_list_12.append(position)
				else:
					canvas.move(car[1], -unit, 0)

	# car appear
	if master_clock % (rnd.randint(1, 10) + 5) == 0:
		randappear = rnd.random()
		if randappear > 0.75:
			# generate a car on road_11
			car_name = 'car' + str(number_of_car_on_raod_11)
			car = canvas.create_rectangle(0, 49*unit, unit, 50*unit, fill='white')
			road_11.append([car_name, car])
			number_of_car_on_raod_11 += 1
		elif randappear > 0.5:
			# generate a car on road_12
			car_name = 'car' + str(number_of_car_on_raod_11)
			car = canvas.create_rectangle(99*unit, 50*unit, 100*unit, 51*unit, fill='white')
			road_12.append([car_name, car])
			number_of_car_on_raod_11 += 1
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
	
	reward = - len(block_list_11) - len(block_list_12)- len(block_list_21) - len(block_list_22) + 4
	# coompute current reward
	
	sum_of_reward += reward
	index_of_this_experiment += 1
	if index_of_this_experiment == length_of_experiment:
		print(sum_of_reward)
		reward_list.append(sum_of_reward)
		sum_of_reward = 0
		index_of_this_experiment = 0
	
	# learning
	RL.learn(observation, action, reward, observation_)
	
	observation = observation_
	light_delay += 1
	master_clock += 1
	time.sleep(0.1)

with open('reward', 'w') as f:
	f.write(str(reward_list))

RL.print_table()

root.mainloop()


#
#State = 
#closest car position from intersection for road 1 (0-8, 9 if no cars) X
#closest car position from intersection for road 2 (0-8, 9 if no cars X
#light setting (ie 0-green, 1 red for one of the roads) X
#light delay (0-3)
#
#Reward -1.0 if a car is stopped at a red light on either road, zero otherwise.
#Optimise discounted sum of future reward.


	