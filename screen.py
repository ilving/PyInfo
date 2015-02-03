import sys,os,types
from evdev import InputDevice

touch = InputDevice('/dev/input/event0')

lastX = 0;lastY = 0


def goTo(x,y):
	sys.stdout.write("\033[" + str(y) + ";" + str(x) + "H")

def printLine(string):
	string = string.replace("\n",'')
	string = string.replace("\r",'')

	if len(string) >= 53:
		sys.stdout.write(string[0:53])
	else:
		sys.stdout.write("%-53s" % string)
	print ""

def sysCall(cmd):
	remote = os.popen(cmd)
	while 1:
		line = remote.readline()
		if not line: break
		printLine(line)

def readTouch():
	global touch
	global lastX,lastY

	startX = 237; endX = 3893; resX = 42; kX = (endX - startX)/resX
	startY = 220; endY = 3873; resY = 52; kY = (endY - startY)/resY

	event = touch.read_one()
	if type(event) == types.NoneType: return None
	if event.type != 3: return None

	if event.code == 0: lastX = event.value;
	if event.code == 1:	lastY = event.value;

	if event.code == 24 and event.value == 0:
		intX = endX - lastX
		intY = endY - lastY

		lastX = int(intX/kX)
		lastY = int(intY/kY)

		return [lastX,lastY]
	else:
		return None

