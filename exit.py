import screen

cLine = 0

def touch(x,y):
	global cLine

	if x in range(cLine,cLine + 3):
		if y in range(44,53):
			screen.sysCall('clear')
			exit()
		draw(cLine)

def draw(line):
	global cLine
	cLine = line

	screen.goTo(0,cLine)
	screen.printLine(" "*44 + " XX XX ")
	screen.printLine(" "*44 + "   X   ")
	screen.printLine(" "*44 + " XX XX ")

