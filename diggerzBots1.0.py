from selenium import webdriver
import time, json, random, threading, queue
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

#installs newest chromedriver
driver = webdriver.Chrome(ChromeDriverManager().install())

#allows reacting to terminal commands
def read_kbd_input(inputQueue):
	print('Ready for keyboard input:')
	while (True):
		input_str = input()
		inputQueue.put(input_str)
inputQueue = queue.Queue()
inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue,), daemon=True)
inputThread.start()

SIZE = [640, 499]#quarter
#SIZE = [1280, 999]#full size
CANVASSIZE = [SIZE[0] - 25, SIZE[1] - 130]
DIGX = (0.877 * CANVASSIZE[0])
DIGY = (0.679 * CANVASSIZE[1])
COINX = (0.510 * CANVASSIZE[0])
COINY = (0.029 * CANVASSIZE[1])
PRIVDIGX = (0.439 * CANVASSIZE[0])
PRIVDIGY = (0.529 * CANVASSIZE[1])
CHATX = (0.032 * CANVASSIZE[0])
CHATY = (0.983 * CANVASSIZE[1])
SETTINGSX = (0.933 * CANVASSIZE[0])
SETTINGSY = (0.104 * CANVASSIZE[1])
COSTUMIZEX = (0.518 * CANVASSIZE[0])
COSTUMIZEY = (0.282 * CANVASSIZE[1])
COOKIESX = (0.8 * CANVASSIZE[0])
COOKIESY = (0.1 * CANVASSIZE[0])
if SIZE != [640, 499]:
	COOKIESX = (0.51 * CANVASSIZE[0])
	COOKIESY = (0.7 * CANVASSIZE[0])
#                        brazil         australia         turkey         germany           uk
COUNTRIESRELATIVE = [[0.657, 0.414], [0.630, 0.380], [0.600, 0.788], [0.470, 0.475], [0.600, 0.506],
#    usa             china           canada         austria          korea        switzerland
[0.351, 0.820], [0.600, 0.820], [0.379, 0.445], [0.600, 0.380], [0.379, 0.601], [0.538, 0.445],
#    japan           russia           italy          nepal
[0.600, 0.580], [0.563, 0.720], [0.500, 0.580], [0.380, 0.693]]

COUNTRIES = COUNTRIESRELATIVE

#generates actual coordinates out of percentage for the flagg buttons
for i in range(len(COUNTRIESRELATIVE)):
	for x in range(len(COUNTRIESRELATIVE[i])):
		COUNTRIES[i][x] = COUNTRIESRELATIVE[i][x] * CANVASSIZE[x]

		#makes sure nepal can get clicked in both sizes, due to its peculiar shape
		if i is 14:
			if SIZE[0] is 640:
				COUNTRIES[14][0] = COUNTRIES[14][0] + 5

PATH = "/chromedriver"
f = open('diggerz.names', 'r')
NAMES = f.read().split('\n')
NAMESLENGTH = len(NAMES)

keyW = { \
	"code": "KeyW",
	"key": "w",
	"text": "w",
	"unmodifiedText": "w",
	"nativeVirtualKeyCode": ord("W"),
	"windowsVirtualKeyCode": ord("W")
}
keyS = { \
	"code": "KeyS",
	"key": "s",
	"text": "s",
	"unmodifiedText": "s",
	"nativeVirtualKeyCode": ord("S"),
	"windowsVirtualKeyCode": ord("S")
}
keyA = { \
	"code": "KeyA",
	"key": "a",
	"text": "a",
	"unmodifiedText": "a",
	"nativeVirtualKeyCode": ord("A"),
	"windowsVirtualKeyCode": ord("A")
}
keyD = { \
	"code": "KeyD",
	"key": "d",
	"text": "d",
	"unmodifiedText": "d",
	"nativeVirtualKeyCode": ord("D"),
	"windowsVirtualKeyCode": ord("D")
}
KEYS = [keyW, keyA, keyS, keyD]
KEYSLEN = len(KEYS)

name = "Enter Name"

COMMANDS = ["trade", "restart", "pause", "unpause"]

#checks for commands
def checkInput(driver):
	if inputQueue.qsize() > 0:
		print("got input..")
		return inputQueue.get()

#used for the holdKey function
def dispatchKeyEvent(driver, name, options = {}):
	options["type"] = name
	body = json.dumps({'cmd': 'Input.dispatchKeyEvent', 'params': options})
	resource = "/session/%s/chromium/send_command" % driver.session_id
	url = driver.command_executor._url + resource
	driver.command_executor._request('POST', url, body)

#holds key <key> for <duration> seconds
def holdKey(driver, key, duration, side):
	endtime = time.time() + duration
	options = key
	stops = 0
	stoptime = time.time()

	while True:
		dispatchKeyEvent(driver, "rawKeyDown", options)
		dispatchKeyEvent(driver, "char", options)
		stoptime = time.time() - stops

		if (stoptime > endtime):
			dispatchKeyEvent(driver, "keyUp", options)
			break
		if inputQueue.qsize() > 0:
			command = checkInput(driver)
			if command == "trade":
				return command
			elif command == "restart":
				print("restarting")
				return command
			elif command == "pause":
				print("bot paused")
				dispatchKeyEvent(driver, "keyUp", options)
				moveToOffsetAndClick(driver, 'body', 10 if side else CANVASSIZE[0] - 10, CANVASSIZE[1] - 100, 1)
				oldtime = stoptime
				while True:
					command = checkInput(driver)
					if command in COMMANDS:
						if command == "pause":
							print("allready paused")
						elif command == "unpause":
							print("unpausing")
							myAction = ActionChains(driver)
							myAction.click_and_hold().perform()
							stops = stops + time.time() - oldtime - 0.2
							stoptime = time.time() - stops
							break
						else:
							return command
					time.sleep(0.1)
			else:
				print("avaiable commands: " + ", ".join(COMMANDS))

#holds keys <key0> and <key1> for <duration> seconds
def hold2Keys(driver, key0, key1, duration):
	endtime = time.time() + duration
	options0 = key0
	options1 = key1
	stops = 0
	stoptime = time.time()

	while True:
		dispatchKeyEvent(driver, "rawKeyDown", options0)
		dispatchKeyEvent(driver, "rawKeyDown", options1)
		dispatchKeyEvent(driver, "char", options0)
		dispatchKeyEvent(driver, "char", options1)
		stoptime = time.time() - stops

		if stoptime > endtime:
			dispatchKeyEvent(driver, "keyUp", options0)
			dispatchKeyEvent(driver, "keyUp", options1)
			break
		if inputQueue.qsize() > 0:
			command = checkInput(driver)
			if command == "trade":
				return command
			elif command == "restart":
				print("restarting")
				return command
			elif command == "pause":
				print("bot paused")
				dispatchKeyEvent(driver, "keyUp", options0)
				dispatchKeyEvent(driver, "keyUp", options1)
				moveToOffsetAndClick(driver, 'body', DIGX, DIGY, 1)
				oldtime = stoptime
				while True:
					command = checkInput(driver)
					if command in COMMANDS:
						if command == "pause":
							print("allready paused")
						elif command == "unpause":
							print("unpausing")
							myAction = ActionChains(driver)
							myAction.click_and_hold().perform()
							stops = stops + (time.time() - oldtime)
							stoptime = time.time() - stops
							break
						else:
							return command
					time.sleep(0.1)
			else:
				print("avaiable commands: " + ", ".join(COMMANDS))

#holds key <key> and mouse for <duration> seconds
def clickHoldWithKey(driver, key, duration, side):
	command = moveToOffsetAndClick(driver, 'body', 10 if side else CANVASSIZE[0] - 10, CANVASSIZE[1] - 100, 1)
	if command in COMMANDS:
		return command
	myAction = ActionChains(driver)
	myAction.click_and_hold().perform()
	command = holdKey(driver, key, duration, side)
	myAction.release().perform()
	if command in COMMANDS:
		return command

#clicks on a spicific spot (<xcoordinate>, <ycoordinate>) for <clickcount> times
def moveToOffsetAndClick(driver, element, xcoordinate, ycoordinate, clickcount):
	myAction = ActionChains(driver)
	myAction.move_to_element_with_offset(driver.find_element_by_tag_name(element), xcoordinate, ycoordinate)
	command = checkInput(driver)
	for i in range(0, clickcount):
		myAction.click().perform()
		if command in COMMANDS:
			return command

#climbs up walls by sliding
def slideUpbWalls(driver, slidecount):
	for i in range(slidecount):
		if i in range(1, slidecount):
			dispatchKeyEvent(driver, "keyUp", keyW)
		command = hold2Keys(driver, keyD, keyW, 0.175)
		if command == "trade":
			return command
		elif command == "restart":
			return command
		command = holdKey(driver, keyA, 0.3, 0)
		if command == "trade":
			return command
		elif command == "restart":
			return command

#walks to the far left block no matter what starting position with the exception of holes
def walkToTheFarLeftBlock(driver):
	command = holdKey(driver, keyA, 13, 0)
	if command in COMMANDS:
		return command
	command = slideUpbWalls(driver, 2)
	if command in COMMANDS:
		return command
	command = holdKey(driver, keyA, 15, 0)
	if command in COMMANDS:
		return command
	command = slideUpbWalls(driver, 2)
	if command in COMMANDS:
		return command
	command = holdKey(driver, keyA, 13, 0)
	if command in COMMANDS:
		return command
	command = holdKey(driver, keyD, 0.06, 0)
	if command in COMMANDS:
		return command

#digs sideways and switches direction
def digRows(driver):
	side = 0
	direction = keyD
	duration = 38.3
	for i in range(0, 21):
		if i > 9:
			duration = 135
			print("starting to dig big rows")
		row = i + 1
		print("digging " + str(row) + ". row")
		command = clickHoldWithKey(driver, direction, duration, side)
		if command in COMMANDS:
			return command
		if side is 0:
			side = 1
			direction = keyA
		else:
			side = 0
			direction = keyD
		command = clickHoldWithKey(driver, keyS, 1.4, side)
		if command in COMMANDS:
			return command
	
#main function for the digging process
def digging(driver):
	print("walking to the far left block to start digging")
	command = walkToTheFarLeftBlock(driver)
	if command in COMMANDS:
		return command
	print("starting to dig down")
	command = clickHoldWithKey(driver, keyS, 26.3, 0)
	if command in COMMANDS:
		return command
	print("starting to dig rows")
	command = digRows(driver)
	if command in COMMANDS:
		return command

#digs 4 blocks down and then for a while to the side to imitate a real person
def imitateDigging(driver):
	side = random.getrandbits(1)
	command = clickHoldWithKey(driver, keyS, 5.3, 0)
	if command in COMMANDS:
		return command
	command = clickHoldWithKey(driver, keyA if side else keyD, random.randrange(0, 21) + 5, side)
	if command in COMMANDS:
		return command

#jumps and walks around to imitate a real person
def imitateMoving(driver):
	side = random.getrandbits(1)
	for i in range(random.randrange(2, 10)):
		side = random.getrandbits(1)
		if random.getrandbits(1):
			command = holdKey(driver, keyA if side else keyD, 2, 0)
			if command in COMMANDS:
				return command
		else:
			command = hold2Keys(driver, keyA if side else keyD, keyW, 1.5)
			if command in COMMANDS:
				return command

#stands and moves with the head to imitate a real person
def imitateStanding(driver):
	side = random.getrandbits(1)
	for i in range(random.randrange(0, 18)):
		time.sleep(random.randrange(2, 40) / 10)
		if side is 0:
			side = 1
		else:
			side = 0
		#direction(driver, side)
		command = moveToOffsetAndClick(driver, 'body', CANVASSIZE[0] - COOKIESX if side is 0 else COOKIESX, COOKIESY, 1)
		if command in COMMANDS:
			return command

#makes randomized movements to imitate a real person
def imitateRealPerson(driver):
	print("imitating real person")
	move = random.randrange(3)
	if move is 0:
		command = imitateDigging(driver)
		if command in COMMANDS:
			return command
	elif move is 1:
		command = imitateMoving(driver)
		if command in COMMANDS:
			return command
	elif move is 2:
		command = imitateStanding(driver)
		if command in COMMANDS:
			return command
	time.sleep(random.randrange(5, 50) / 10)

#goes into dig + trade
def GoToDigTrade(driver):
	print("going to Dig + Trade, can't react to commands")
	#goes into dig+trade
	command = moveToOffsetAndClick(driver, 'body', DIGX, DIGY, 3)
	if command in COMMANDS:
		return command

	time.sleep(6)

	#cicks to remove pop up of daily super rare items
	command = moveToOffsetAndClick(driver, 'body', COOKIESX, COOKIESY, 1)
	if command in COMMANDS:
		return command

	time.sleep(1)
	#accepts cookies
	moveToOffsetAndClick(driver, 'body', COOKIESX, COOKIESY, 2)

	print("in Dig + Trade and ready for input:")

#goes to private dig
def GoToPrivateDig(driver):
	moveToOffsetAndClick(driver, 'body', PRIVDIGX, PRIVDIGY, 1)
	time.sleep(0.5)
	print("going to private dig, can't react to commands")
	#clicks coin
	command = moveToOffsetAndClick(driver, 'body', COINX, COINY, 1)
	if command in COMMANDS:
		return command

	time.sleep(0.5)

	#clicks yes and goes to private dig
	command = moveToOffsetAndClick(driver, 'body', PRIVDIGX, PRIVDIGY, 1)
	if command in COMMANDS:
		return command

	time.sleep(3)

	#clicks to remove pop up of daily super rare items
	command = moveToOffsetAndClick(driver, 'body', COOKIESX, COOKIESY, 1)
	if command in COMMANDS:
		return command
	print("in private dig and ready for input:")

#goes to settings then to costumize and ramdomly changes flag
def changeFlag(driver):
	print("changing flag, can't react to commands")
	country = random.randrange(0, 15)
	#clicks to tell the bowser im here so it will only need to click once next time
	command = moveToOffsetAndClick(driver, 'body', PRIVDIGX, PRIVDIGY, 1)
	if command in COMMANDS:
		return command
	time.sleep(1)
	#clicks settings
	command = moveToOffsetAndClick(driver, 'body', SETTINGSX, SETTINGSY, 1)
	if command in COMMANDS:
		return command
	time.sleep(1)
	#clicks costumize in settings
	command = moveToOffsetAndClick(driver, 'body', COSTUMIZEX, COSTUMIZEY, 1)
	if command in COMMANDS:
		return command
	time.sleep(1)
	#clicks on a randomly generated flag out of popular countrys
	command = moveToOffsetAndClick(driver, 'body', COUNTRIES[country][0], COUNTRIES[country][1], 1)
	if command in COMMANDS:
		return command
	time.sleep(1)
	#clicks the settingy button again to remove the settings
	command = moveToOffsetAndClick(driver, 'body', SETTINGSX, SETTINGSY, 1)
	if command in COMMANDS:
		return command

#writes <message> into the game  chat and it takes <duration> seconds long + 1
def chat(driver, message, duration):
	command = moveToOffsetAndClick(driver, 'body', CHATX, CHATY, 1)
	if command in COMMANDS:
		return command
	time.sleep(0.5)
	action = ActionChains(driver)
	action.send_keys(message).perform()
	time.sleep(0.5)
	time.sleep(duration)
	action2 = ActionChains(driver)
	action2.send_keys(Keys.RETURN).perform()

#here happens all the digging and walking
def mainlogic(driver):
	#disables trades
	chat(driver, "/notrades", 0)

	time.sleep(1)

	command = imitateRealPerson(driver)
	if command in COMMANDS:
		return command

	moveToOffsetAndClick(driver, 'body', COOKIESX, COOKIESY, 2)
	time.sleep(1)

	command = GoToPrivateDig(driver)
	if command in COMMANDS:
		return command

	time.sleep(1)

	command = digging(driver)
	if command in COMMANDS:
		return command

#deletes old name and types a random new one out of <NAMES>
def makeName(driver, name):
	print("changing name, can't react to commands")
	#deletes last name
	for i in range(0, len(name)):
		action = ActionChains(driver)
		action.send_keys(Keys.BACKSPACE).perform()
	time.sleep(0.5)
	#makes new name
	name = NAMES[random.randrange(0, NAMESLENGTH)]
	action2 = ActionChains(driver)
	action2.send_keys(name)
	action2.perform()

#goes to dig and trade and stays there, so items can be taken
def trade(driver):
	print("going to trade, can't react to commands")
	time.sleep(1)
	driver.refresh()
	time.sleep(4)
	GoToDigTrade(driver)
	time.sleep(0.5)
	chat(driver, "/trades", 0)
	print("ready to trade and ready for input:")
	while True:
		if inputQueue.qsize() > 0:
			command = checkInput(driver)
			if command == "restart":
				print("restarting")
				break
			elif command == "trade":
				print("allready in trade status, if you still want to go trade status type <ok>")
			elif command == "ok":
				trade(driver)
				break
			elif command == "pause":
				print("your're in trade status, already paused")
			elif command == "unpause":
				print("unpausing")
				return command
			else:
				print("avaiable commands: " + ", ".join(COMMANDS))
		time.sleep(0.1)

#driver = webdriver.Chrome(PATH)
driver.set_window_size(SIZE[0], SIZE[1])
driver.get("https://diggerz.io/")
time.sleep(6)

#accepts cookies
moveToOffsetAndClick(driver, 'body', COOKIESX, COOKIESY, 2)
time.sleep(1)

#types name
makeName(driver, name)
time.sleep(1.5)

#changes flag to randomly generated out of popular countries
changeFlag(driver)
time.sleep(1.5)

GoToDigTrade(driver)
time.sleep(1)

while True:
	main = mainlogic(driver)
	command = main
	if command == "trade":
		command = trade(driver)

	if command != "unpause":
		time.sleep(2)
		driver.refresh()
		time.sleep(5)
	else:
		command = "unpause"

	if command != "unpause":

		#accepts cookies
		moveToOffsetAndClick(driver, 'body', COOKIESX, COOKIESY, 2)
		time.sleep(1)

		#types name
		makeName(driver, name)

		time.sleep(1.5)

		#changes flag to randomly generated out of popular countries
		changeFlag(driver)

		time.sleep(1.5)

		GoToDigTrade(driver)

		time.sleep(1)
