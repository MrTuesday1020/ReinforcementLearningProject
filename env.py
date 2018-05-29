from tkinter import *
import time
import random as rnd
import qlearning as ql

root = Tk()
# every 4px is a unit
canvas = Canvas(root, width=400, height=400, background='grey')
canvas.pack()
# width of a road is 8px
# the horizontal road
canvas.create_rectangle(0, 196, 400, 204, fill='black')
# the vertical road
canvas.create_rectangle(196, 0, 204, 400, fill='black')
# cars and lights are 4px*4px squares
light1 = canvas.create_rectangle(192, 196, 196, 200, fill='spring green')
light2 = canvas.create_rectangle(200, 192, 204, 196, fill='red2')

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
block_list1 = [196]
block_list2 = [196]

RL = ql.QLearningTable()

observation = [closest_car_position_of_road1, closest_car_position_of_road2, light_setting, light_delay]

def closest_car(car_position,action,light_setting, closest_car_position_of_road,next_car_position):
	if car_position == 9:
		if closest_car_position_of_road > 9:
			car_position = car_position
		elif closest_car_position_of_road == 9:
			car_position -= 1
	elif car_position > 0:
		car_position -= 1
	elif car_position == 0:
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
	for car in reversed(road1):
		position1 = canvas.coords(car[1])[0]
		if position1 < 196:
			closest_car_position_of_road1 = int((196 - position1) / 4)
			temp = road1.index(car)
			if temp != 0:
				position2 = canvas.coords(road1[temp-1][1])[0]
				next_car_position1 = int((196 - position2) / 4)
			else:
				next_car_position1 = 10
	
	for car in reversed(road2):
		position1 = canvas.coords(car[1])[1]
		if position1 < 196:
			closest_car_position_of_road2 = int((196 - position1) / 4)
			temp = road1.index(car)
			if temp != 0:
				position2 = canvas.coords(road1[temp-1][1])[0]
				next_car_position2 = int((196 - position2) / 4)
			else:
				next_car_position2 = 10
	
	closest_car_position_of_road1 = closest_car(observation[0], action, light_setting, closest_car_position_of_road1, next_car_position1)
	closest_car_position_of_road2 = closest_car(observation[1], action, light_setting, closest_car_position_of_road2, next_car_position2)
 	
	if action == 'switch':
		if observation[2] == 0:
			light_setting = 1
		else:
			light_setting = 0
		
		light_delay = 0
	else:
		light_setting = observation[2]
		
		if observation[3] != 3:
			light_delay = observation[3] + 1
		else:
			light_delay = observation[3]
		
		


while master_clock <= 1000:
	
	if light_delay <= 2:
		action = 'no_switch'
	else:
		action = RL.choose_action(str(observation))
	
	# chaneg light setting
	if action == 'switch':
		light_delay = -1
		if light_setting == 0:
			light_setting = 1
			block_list1 = [196]
			light1 = canvas.create_rectangle(192, 196, 196, 200, fill='red2')
			light2 = canvas.create_rectangle(200, 192, 204, 196, fill='spring green')
		else:
			light_setting = 0
			block_list2 = [196]
			light1 = canvas.create_rectangle(192, 196, 196, 200, fill='spring green')
			light2 = canvas.create_rectangle(200, 192, 204, 196, fill='red2')
	
	if light_setting == 0:
		for car in road1:
			
			canvas.move(car[1], 4, 0)
		for car in reversed(road2):
			position = canvas.coords(car[1])[1]
			# if the car has passed the intersection just move foreward
			if position >= 196:
				# move down a unit
				canvas.move(car[1], 0, 4)
			else:
				if (position + 4) in block_list2:
					block_list2.append(position)
				else:
					canvas.move(car[1], 0, 4)
	else:
		for car in road2:
			canvas.move(car[1], 0, 4)
		for car in reversed(road1):
			position = canvas.coords(car[1])[0]
			# if the car has passed the intersection just move foreward
			if position >= 196:
				# move right a unit
				canvas.move(car[1], 4, 0)
			else:
				if (position + 4) in block_list1:
					block_list1.append(position)
				else:
					canvas.move(car[1], 4, 0)

	if master_clock % (rnd.randint(1, 8)) == 0:
		if rnd.random() > 0.5:
			# generate a car on road1
			car_name = 'car' + str(number_of_car_on_raod1)
			car = canvas.create_rectangle(0, 196, 4, 200, fill='white')
			road1.append([car_name, car])
			number_of_car_on_raod1 += 1
		else:
			# generate a car on road2
			car_name = 'car' + str(number_of_car_on_raod2)
			car = canvas.create_rectangle(200, 0, 204, 4, fill='white')
			road2.append([car_name, car])
			number_of_car_on_raod2 += 1
	
	root.update()
	
	# next state
	
	observation_, reward = update_state(action,observation,road1, road2)
	RL.learn(observation, action, reward, observation_)
	observation = observation_
	
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


	