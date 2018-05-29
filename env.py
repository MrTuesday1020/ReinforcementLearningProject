from tkinter import *
import time
import random as rnd
import qlearning as ql

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
light1 = canvas.create_rectangle(48*unit, 49*unit, 49*unit, 50*unit, fill='spring green')
light2 = canvas.create_rectangle(50*unit, 48*unit, 51*unit, 49*unit, fill='red2')

master_clock = 0
road1 = []
road2 = []
number_of_car_on_raod1 = 0
number_of_car_on_raod2 = 0
# 0-8, 9 if no cars
closest_car_position_of_road1 = 9
closest_car_position_of_road2 = 9
# road1 light setting, 0:green, 1:red
light_setting = 0
light_delay = 0
# a fixed change time
change_time = 10
# a list that store the postions that have been occupied
block_list1 = [49*unit]
block_list2 = [49*unit]

observation = str(closest_car_position_of_road1)+str(closest_car_position_of_road2)+str(light_setting)+str(light_delay)


def closest_car(car_position, action, light_setting, clst_car_position_of_road, next_car_position):
	if car_position == 9:
		if clst_car_position_of_road > 9:
			car_position = car_position
		elif clst_car_position_of_road == 9:
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

def update_state(action, observation, road1, road2):
	closest_car_position_of_road1 = 10
	next_car_position1 = 10
	for car in road1:
		px1 = canvas.coords(car[1])[0]
		if px1 < 49*unit:
			closest_car_position_of_road1 = int((49*unit - px1) / unit)
			temp = road1.index(car)
			if temp != len(road1) - 1:
				px2 = canvas.coords(road1[temp+1][1])[0]
				next_car_position1 = int((49*unit - px2) / unit)
			break
	
	closest_car_position_of_road2 = 10
	next_car_position2 = 10
	
	for car in road2:
		px1 = canvas.coords(car[1])[1]
		if px1 < 49*unit:
			closest_car_position_of_road2 = int((49*unit - px1) / unit)
			temp = road2.index(car)
			if temp != len(road2) - 1:
				px2 = canvas.coords(road2[temp+1][1])[1]
				next_car_position2 = int((49*unit - px2) / unit)
			break
	
#	print(closest_car_position_of_road1, closest_car_position_of_road2)
#	print(next_car_position1, next_car_position2)
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
#	print(closest_car_position_of_road1,closest_car_position_of_road2,light_setting,light_delay)
	return observation

RL = ql.QLearningTable()

while master_clock <= 1000:
	
	if light_delay <= 2:
		action = 'no_switch'
		RL.check_state_exist(observation)
	else:
		action = RL.choose_action(observation)
	
	# chaneg light setting
	if action == 'switch':
		light_delay = -1
		if light_setting == 0:
			light_setting = 1
			block_list1 = [49*unit]
			light1 = canvas.create_rectangle(48*unit, 49*unit, 49*unit, 50*unit, fill='red2')
			light2 = canvas.create_rectangle(50*unit, 48*unit, 51*unit, 49*unit, fill='spring green')
		else:
			light_setting = 0
			block_list2 = [49*unit]
			light1 = canvas.create_rectangle(48*unit, 49*unit, 49*unit, 50*unit, fill='spring green')
			light2 = canvas.create_rectangle(50*unit, 48*unit, 51*unit, 49*unit, fill='red2')
	
	if light_setting == 0:
		for car in road1:
			canvas.move(car[1], unit, 0)
		print('road2:', end='')
		for car in reversed(road2):
			position = canvas.coords(car[1])[1]
			# if the car has passed the intersection just move foreward
			if position >= 49*unit:
				# move down a unit
				canvas.move(car[1], 0, unit)
			else:
				print(position)
				print(block_list2)
				if (position + unit) in block_list2:
					block_list2.append(position)
				else:
					canvas.move(car[1], 0, unit)
	else:
		for car in road2:
			canvas.move(car[1], 0, unit)
		for car in reversed(road1):
			position = canvas.coords(car[1])[0]
			# if the car has passed the intersection just move foreward
			if position >= 49*unit:
				# move right a unit
				canvas.move(car[1], unit, 0)
			else:
				if (position + unit) in block_list1:
					block_list1.append(position)
				else:
					canvas.move(car[1], unit, 0)

	if master_clock % (rnd.randint(1, 8)) == 0:
		if rnd.random() > 0.5:
			# generate a car on road1
			car_name = 'car' + str(number_of_car_on_raod1)
			car = canvas.create_rectangle(0, 49*unit, unit, 50*unit, fill='white')
			road1.append([car_name, car])
			number_of_car_on_raod1 += 1
		else:
			# generate a car on road2
			car_name = 'car' + str(number_of_car_on_raod2)
			car = canvas.create_rectangle(50*unit, 0, 51*unit, unit, fill='white')
			road2.append([car_name, car])
			number_of_car_on_raod2 += 1
	
	root.update()
	
	# next state
	
<<<<<<< HEAD
	observation_, reward = update_state(action,observation,road1, road2)
	RL.learn(observation, action, reward, observation_)
	observation = observation_
=======
	observation_ = update_state(action, observation, road1, road2)
	
	reward = - len(block_list1) - len(block_list2) + 2
	
	RL.learn(observation, action, reward, observation_)
	
	observation = observation_
#	print(observation)
>>>>>>> 86c8c35a68a511440fdc080e07f590ef31655dae
	
	light_delay += 1
	master_clock += 1
	time.sleep(0.2)


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


	