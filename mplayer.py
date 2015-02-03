import screen,re,os,types
import subprocess as sp
import fcntl

mPlayer = None
currentPlaylistItem = 0
playList = []
title = 'Stop'

cLine = 0

def non_block_read(output):
	fd = output.fileno()
	fl = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
	try:
		return output.read()
	except:
		return ""

def touch(x,y):
	global cmd,cLine

	if x in range(cLine + 3,cLine + 8):
		if y in range(0,9): # rewind
			rew()
		if y in range(11,26): # stop - kill mplayer
			stopMplayer()
		if y in range(28,42): # play - start mplayer
			startMplayer()
		if y in range(44,52): # forward (next playlist)
			fwd()

		draw(cLine)

def getPlayList():
	playList = []
	content =  open(os.path.dirname(os.path.abspath(__file__)) + '/mplayer.m3u', 'r').read()

	for item in content.split("\r\n"):
		m = re.search('^http(s)?.*$',item)
		if type(m) == types.NoneType: continue
		playList.append(item)

	return playList

def fwd():
	global currentPlaylistItem
	playList = getPlayList()
	currentPlaylistItem += 1
	if currentPlaylistItem >= len(playList):
		currentPlaylistItem = 0
	stopMplayer()
	startMplayer()

def rew():
	global currentPlaylistItem
	playList = getPlayList()
	currentPlaylistItem -= 1
	if currentPlaylistItem < 0 :
		currentPlaylistItem = len(playList)-1

	stopMplayer()
	startMplayer()

def startMplayer():
	global mPlayer,currentPlaylistItem,title,grep

	playList = getPlayList()

	title = 'Init: ' + playList[currentPlaylistItem]
	draw(cLine)

	cmd = ['mplayer','-playlist',playList[currentPlaylistItem],'-idle','-slave','-cache-min','30']

	mPlayer = sp.Popen(
		cmd,
		stdout=sp.PIPE,
		stderr=sp.PIPE
	)

def stopMplayer():
	global mPlayer,title,grep

	if mPlayer is not None:
		mPlayer.kill()
		mPlayer = None
		title = 'Stop'

def draw(line):
	global mPlayer, cLine, title,grep

	cLine = line

	screen.goTo(0,cLine)
	screen.printLine("="*19 + ' MPlayer ' + "="*26)

	line = ''
	if mPlayer is not None:
		line = non_block_read(mPlayer.stdout)
		m = re.search("StreamTitle\=[\"\'](.+?)[\"\']",line)
		if type(m) != types.NoneType:
			title = m.group(1)

	screen.printLine(title)
	screen.printLine(line)

	screen.printLine("-" * 53)

	# prev: 0..9
	# stop: 11..26
	# play: 28..42
	# next: 44..52

	screen.printLine('   ****** |    ********    |     **        | ******   ')
	screen.printLine('  ******  |    ********    |     ****      |  ******  ')
	screen.printLine(' ******   |    ********    |     ******    |   ****** ')
	screen.printLine('  ******  |    ********    |     ****      |  ******  ')
	screen.printLine('   ****** |    ********    |     **        | ******   ')

	screen.printLine("=" * 53)
