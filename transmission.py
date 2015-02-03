import screen,re,os,types

cLine = 0

def draw(line):
	global cLine

	cLine = line
	screen.goTo(0,cLine)

	screen.printLine(("=" * 19) + ' Transmission ' + ("=" * 20))

	screen.printLine(" ETA         Status       Name")
	remote = os.popen("transmission-remote 9091 --list | egrep 'Seeding|Download|Up & Down|Queued|Stopped' -m3")
	i = 0
	while 1:
		line = remote.readline()
		if not line: break
		screen.printLine(line[23:36] + line[57:])
		i += 1

	while i < 3:
		screen.printLine("")
		i += 1
	screen.printLine("-" * 53)

	screen.sysCall("transmission-remote 9091 -si | grep 'Download directory free space'")
	screen.sysCall("transmission-remote 9091 -st | egrep 'Uploaded|Downloaded' -m2")

	screen.printLine("-" * 53)
	screen.printLine('      **********           |        *** ** ***        ')
	screen.printLine('      **********           |          *** ** ***      ')
	screen.printLine('      **********           |        *** ** ***        ')

def torrentsIDs():
	ids = []
	remote = os.popen("transmission-remote 9091 --list")
	while 1:
		line = remote.readline()
		if not line: break
		m = re.search('^(\d+).*$',line.strip())
		if type(m) == types.NoneType: continue
		ids.append(m.group(1))
	return ids

def stop():
	ids = torrentsIDs()
	os.popen("transmission-remote 9091 -t" + (",".join(ids) + " --stop"))

def start():
	ids = torrentsIDs()
	os.popen("transmission-remote 9091 -t" + (",".join(ids) + " --start"))

def touch(x,y):
	global cLine
	if x in range(cLine+9,cLine+13):
		if y in range(0,27):
			stop()
		if y in range(19,52):
			start()
		draw(cLine)
