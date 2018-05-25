from tkinter import *
import time
import random as rnd

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
light1 = canvas.create_rectangle(192, 196, 196, 200, fill='green')
light2 = canvas.create_rectangle(200, 192, 204, 196, fill='red')

master_clock = 0
light_clock = 0
road1 = {}
road2 = {}
number_of_car_on_raod1 = 0
number_of_car_on_raod2 = 0

while True:
	for car in road1:
		canvas.move(road1[car], 4, 0)
	for car in road2:
		canvas.move(road2[car], 0, 4)
		
	if clock % (rnd.randint(1, 10) + 8) == 0:
		# generate a car on road1
		car = 'car' + str(number_of_car_on_raod1)
		road1[car] = canvas.create_rectangle(0, 196, 4, 200, fill='white')
		number_of_car_on_raod1 += 1
		
	if clock % (rnd.randint(1, 10) + 5) == 0:
		# generate a car on road2
		car = 'car' + str(number_of_car_on_raod2)
		road2[car] = canvas.create_rectangle(200, 0, 204, 4, fill='white')
		number_of_car_on_raod2 += 1
	
	root.update()
	master_clock += 1
	time.sleep(0.2)

root.mainloop()