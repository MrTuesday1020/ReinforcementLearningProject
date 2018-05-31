from tkinter import *
import time
import random as rnd
import Rainforcement_Learning as ql

# mode Sarsa or Qlearning
Sarsa = False

root = Tk()
# every 8px is a unit
unit = 8

canvas = Canvas(root, width = 100*unit , height = 100*unit, background='grey')
canvas.pack()
# width of a road is 8px
# the horizontal road
canvas.create_rectangle(0*unit, 49*unit, 100*unit, 51*unit, fill='black')
# the vertical road
canvas.create_rectangle(49*unit, 0*unit, 51*unit, 100*unit, fill='black')
# cars and lights are 4px*4px squares
light_11 = canvas.create_rectangle(48*unit, 49*unit, 49*unit, 50*unit, fill='SpringGreen3')
light_21 = canvas.create_rectangle(50*unit, 48*unit, 51*unit, 49*unit, fill='red2')
light_12 = canvas.create_rectangle(51*unit, 50*unit, 52*unit, 51*unit, fill='SpringGreen3')
light_22 = canvas.create_rectangle(49*unit, 51*unit, 50*unit, 52*unit, fill='red2')

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

amount_of_training = 1
current_training = 0

# do 5 training for basecase
while current_training < amount_of_training:
	
	amount_of_episode = 50
	current_episode = 0
	performance_measure = []
	
	
	# do 100 episodes
	while current_episode < amount_of_episode:

		current_time = 0
		sum_of_stop_cars = 0
		period_of_time = 1000
		
		if Sarsa:
			action = RL.choose_action(str(observation))

		# every 1000 time step as a unit
		while current_time <= period_of_time:
			
			# delete cars which have move outside the canvas
			road_11 = [car for car in road_11 if canvas.coords(car[1])[0] <= 100*unit]
			road_12 = [car for car in road_12 if canvas.coords(car[1])[0] >= 0*unit]
			road_21 = [car for car in road_21 if canvas.coords(car[1])[1] <= 100*unit]
			road_22 = [car for car in road_22 if canvas.coords(car[1])[1] >= 0*unit]
			
			# choose action
			
			# chaneg light setting
			if amber_light != 0:
				if amber_light == 1:	# road1: yellow -> red; road2: red -> green
					canvas.itemconfig(light_11, fill='red2')
					canvas.itemconfig(light_12, fill='red2')
					canvas.itemconfig(light_21, fill='SpringGreen3')
					canvas.itemconfig(light_22, fill='SpringGreen3')
				else:	# road2: yellow -> red; road1: red -> green
					canvas.itemconfig(light_21, fill='red2')
					canvas.itemconfig(light_22, fill='red2')
					canvas.itemconfig(light_11, fill='SpringGreen3')
					canvas.itemconfig(light_12, fill='SpringGreen3')
				amber_light = 0
			
			if light_delay == base_case:
				light_delay = -1
				block_list_11 = [49*unit]
				block_list_12 = [50*unit]
				block_list_21 = [49*unit]
				block_list_22 = [50*unit]
				if light_setting == 0:	# road1: green -> yellow; road2: red -> red
					light_setting = 1
					amber_light = 1
					canvas.itemconfig(light_11, fill='yellow')
					canvas.itemconfig(light_12, fill='yellow')
				else:	# road2: green -> yellow; road1: red -> red
					light_setting = 0
					amber_light = 2
					canvas.itemconfig(light_21, fill='yellow')
					canvas.itemconfig(light_22, fill='yellow')

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
			if current_time % (rnd.randint(1, 10) + 5) == 0:
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

			# compute the amount of stop cars
			stop_cars = len(block_list_11) + len(block_list_12) + len(block_list_21) + len(block_list_22) - 4
			sum_of_stop_cars += stop_cars
			
			light_delay += 1
			current_time += 1
			
		print(sum_of_stop_cars)
		performance_measure.append(sum_of_stop_cars)
		current_episode += 1


	print(performance_measure)
	performance_file = 'basecase/performance_' + str(current_training)
	with open(performance_file, 'w') as f:
		f.write(str(performance_measure))

	current_training += 1

root.mainloop()

#Optimise discounted sum of future reward.