import screen,transmission,mplayer,exit
import time

screen.sysCall('clear')

def wait():
	for i in range(0,500):
		time.sleep(0.002)
		touch = screen.readTouch()
		if touch is not None:
			touchModules(touch[0],touch[1])

def touchModules(x,y):
	if mplayer.touch(x,y): return True
	if transmission.touch(x,y): return True
	if exit.touch(x,y): return True
	return False

while 1:
	transmission.draw(0)
	mplayer.draw(14)
	exit.draw(40)

	wait()

