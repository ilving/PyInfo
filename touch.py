#import struct, InputDevice
#
#file = open( "/dev/input/event0", "rb" )
#
#def getMouseEvent():
#	buf = file.read(3)
#	button = ord( buf[0] )
#	bLeft = button & 0x1
#	bMiddle = ( button & 0x4 ) > 0
#	bRight = ( button & 0x2 ) > 0
#	x,y = struct.unpack( "bb", buf[1:] )
#	print ("L:%d, M: %d, R: %d, x: %d, y: %d" % (bLeft,bMiddle,bRight, x, y) )
#	# return stuffs
#
#while( 1 ):
#	getMouseEvent()
#file.close()

from evdev import InputDevice

dev = InputDevice('/dev/input/event0')
print(dev)

startX = 237; endX = 3893; resX = 42; kX = (endX - startX)/resX
startY = 220; endY = 3873; resY = 52; kY = (endY - startY)/resY

lastX = 0
lastY = 0


for event in dev.read_loop():
	if event.type != 3: continue;

#	print "Event: ",event.type, " / ", event.code," / ", event.value

	if event.code == 0: lastX = event.value;
	if event.code == 1:	lastY = event.value;


	if event.code == 24 and event.value == 0:
		intX = endX - (lastX)
		intY = endY - (lastY)

		intX = int(intX/kX)
		intY = int(intY/kY)

		print intX , "(", lastX, ") / " , intY, " (", lastY, ")"
		lastX = 0
		lastY = 0
