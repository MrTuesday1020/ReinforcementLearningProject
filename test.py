from tkinter import *
import time

root = Tk()

canvas = Canvas(root, width=404, height=404, background='grey')
canvas.pack()

block1 = canvas.create_rectangle(0, 200, 404, 204, fill='black')
block2 = canvas.create_rectangle(200, 0, 204, 404, fill='black')

car1 = canvas.create_rectangle(0, 200, 4, 204, fill='white')
car2 = canvas.create_rectangle(200, 0, 204, 4, fill='white')

pos_x = 0

while pos_x <= 404:
	print(pos_x)
	pos_x += 1
	canvas.move(car1, 1, 0)
	#canvas.move(car2, 0, 1)
	root.update()
	time.sleep(0.01)

root.mainloop()