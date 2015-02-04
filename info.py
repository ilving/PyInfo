import screen,transmission,mplayer

from evdev import InputDevice
import time,types,threading

screen.sysCall('clear')

def touchModules(x,y):
	if mplayer.touch(x,y): return True
	if transmission.touch(x,y): return True
	return False

def mainLoop():
	while True:
		transmission.draw(0)
		mplayer.draw(14)
#		exit.draw(40)
		time.sleep(1.1)

def readTouch():
	touch = InputDevice('/dev/input/event0')
	for event in touch.read_loop():
		point = screen.readTouch(event)
		if type(point) != types.NoneType:
			touchModules(point[0],point[1])

main = threading.Thread(target=mainLoop)
main.start()

touch = threading.Thread(target=readTouch)
touch.start()