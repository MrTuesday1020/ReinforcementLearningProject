#!/usr/bin/python
from tkinter import *

#def next_car(road,direction,revers):
#	closest_car_position_of_road = 10
#	next_car_position = 10
#	for car in road:
#		px1 = canvas.coords(car[1])[direction]
#		#px1 = canvas.coords(car[1])[1]	-> road2
#		if not revers:
#			if px1 < 49*unit:
#				closest_car_position_of_road = int((49*unit - px1) / unit)
#				temp = road.index(car)
#				if temp != len(road) - 1:
#					px2 = canvas.coords(road[temp+1][1])[direction]
#					#px2 = canvas.coords(road2[temp+1][1])[1]
#					next_car_position = int((49*unit - px2) / unit)
#				break
#		else:
#			if px1 > 49*unit:
#				closest_car_position_of_road = int((px1 - 49*unit) / unit)
#				temp = road.index(car)
#				if temp != len(road) - 1:
#					px2 = canvas.coords(road[temp+1][1])[direction]
#					#px2 = canvas.coords(road2[temp+1][1])[1]
#					next_car_position = int((px2 - 49*unit) / unit)
#				break
#	return closest_car_position_of_road,next_car_position

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
	
def move_right(road,block_list):
	for car in road:
		position = canvas.coords(car[1])[0]
		# if the car has passed the intersection just move foreward
		if position >= 49*unit:
			# move right a unit
			canvas.move(car[1], unit, 0)
		else:
			if (position + unit) in block_list:
				if position not in block_list:
					block_list.append(position)
			else:
				canvas.move(car[1], unit, 0)

def move_left(road,block_list):
	for car in road:
		position = canvas.coords(car[1])[0]
		# if the car has passed the intersection just move foreward
		if position <= 50*unit:
			# move left a unit
			canvas.move(car[1], -unit, 0)
		else:
			if (position - unit) in block_list:
				if position not in block_list:
					block_list.append(position)
			else:
				canvas.move(car[1], -unit, 0)
	
def move_down(road,block_list):
	for car in road:
		position = canvas.coords(car[1])[1]
		# if the car has passed the intersection just move foreward
		if position >= 49*unit:
			# move down a unit
			canvas.move(car[1], 0, unit)
		else:
			if (position + unit) in block_list:
				if position not in block_list:
					block_list.append(position)
			else:
				canvas.move(car[1], 0, unit)
	
def move_up(road,block_list):
	for car in road:
		position = canvas.coords(car[1])[1]
		# if the car has passed the intersection just move foreward
		if position <= 50*unit:
			# move up a unit
			canvas.move(car[1], 0, -unit)
		else:
			if (position - unit) in block_list:
				if position not in block_list:
					block_list.append(position)
			else:
				canvas.move(car[1], 0, -unit)