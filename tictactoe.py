
#
# Tic tac toe bot
#
# Uses depth first search to determine the best move for x
#


#ease of use
global debug

def printAsBoard(board):
	print("\n\t", chars[board[0]], chars[board[1]], chars[board[2]])
	print("\t", chars[board[3]], chars[board[4]], chars[board[5]])
	print("\t", chars[board[6]], chars[board[7]], chars[board[8]], "\n")
		
def cPrint(message, tabs):
	global debug
	if debug == True:
		printTabs = ""
		for i in range(tabs):
			printTabs = printTabs + "\t"
		print(printTabs, message)
		
def cPrint2(message1, message2, tabs):
	global debug
	if debug == True:
		printTabs = ""
		for i in range(tabs):
			printTabs = printTabs + "\t"
		print(printTabs, message1, message2)

def check3(s1, s2, s3, originalDead):
	if s1 == s2 and s1 == s3 and s1 != 0:
		return s1
	else:
		return originalDead
		
def concat(arr1, arr2):
	for i in arr2:
		arr1.append(i)
	return arr1

def getArraySum(array):
	arraySum = 0
	for i in array:
		arraySum = arraySum + i
	return arraySum

#checks
def checkDead(board):
	if board.count(0) == 0:
		dead = 3
	else:
		dead = 0
		
	#0 - not dead
	#1 - x
	#2 - o
	#3 - cat
	
	dead = check3(board[0], board[1], board[2], dead)
	dead = check3(board[3], board[4], board[5], dead)
	dead = check3(board[6], board[7], board[8], dead)
	
	dead = check3(board[0], board[3], board[6], dead)
	dead = check3(board[1], board[4], board[7], dead)
	dead = check3(board[2], board[5], board[8], dead)
	
	dead = check3(board[0], board[4], board[8], dead)
	dead = check3(board[6], board[4], board[2], dead)
	
	return dead

def checkPlayer(board): #true == x
	if board.count(1) == board.count(2):
		return 1
	else:
		return 2
		
def getWinningMove(board):
	winningMove = -1 #there is none
	for i in range(len(board)):
		if board[i] == 0:
			pseudoBoard = board.copy()
			pseudoBoard[i] = 1
			if checkDead(pseudoBoard) == 1:
				winningMove = i
	return winningMove

def getWinningMoveO(board):
	winningMove = -1 #there is none
	for i in range(len(board)):
		if board[i] == 0:
			pseudoBoard = board.copy()
			pseudoBoard[i] = 2
			if checkDead(pseudoBoard) == 2:
				winningMove = i
	return winningMove

#functions
global selfWinPercent
global catWinPercent
global opponentWinPercent
selfWinPercent = 100
catWinPercent = 50
opponentWinPercent = 0
def getWinPercentX(board):
	cPrint("X---------------------------------X", 0)
	cPrint(board, 1)
	deadBoard = checkDead(board)
	
	if deadBoard == 2: #has the opponent won?
		cPrint2("The opponent won %=", opponentWinPercent, 2)
		
		return opponentWinPercent
	elif deadBoard == 1 or getWinningMove(board) != -1: #have I won or am I able to win in one move?
		cPrint2("I won %=", selfWinPercent, 2)
		
		return selfWinPercent
	elif deadBoard == 3: #are there no spaces left on the board
		cPrint2("The cat won %=", catWinPercent, 2)
		
		return catWinPercent
	else: #none of the latter is true
		cPrint("All checks passed", 2)
		
		winPercents = []
		#find every blank space
		for i in range(9):
			if board[i] == 0:
				#place an x on a pseudo board
				pseudoBoard = board.copy()
				
				pseudoBoard[i] = 1
				
				#send off that pseudo board to the o function and add the reply to win percents
				cPrint2("Sent to O at:", i, 3)
				winPercents.append(getWinPercentO(pseudoBoard))
		
		#return the greatest win percent because we know we can choose that later
		return max(winPercents)
			

def getWinPercentO(board):
	cPrint("O---------------------------------O", 0)
	cPrint(board, 1)
	
	if checkDead(board): #is the beard still active
		cPrint("Recieved dead board, sending to X to get percentage", 1)
		return getWinPercentX(board)
	elif getWinningMoveO(board) != -1:
		cPrint2("I won %=", opponentWinPercent, 2)
		return opponentWinPercent
	else:
		cPrint("All checks passed", 1)
		
		winPercents = []
		
		#find every blank space
		for i in range(9):
			if board[i] == 0:
				#place an o on a pseudo board
				pseudoBoard = board.copy()
				pseudoBoard[i] = 2
			
				#get the win percent for x in this scenario
				winPercents.append(getWinPercentX(pseudoBoard))
		
		#return the average of all of them because we can't play for o
		return getArraySum(winPercents) / len(winPercents)
		#return min(winPercents)
		
def selectMove(board):
	winPercents = []
	# for every blank space
	for i in range(9):
		if board[i] == 0:
			#create a pseudo board with x in that space
			pseudoBoard = board.copy()
			pseudoBoard[i] = 1
			
			#get the win percent for that move
			winPercents.append(getWinPercentO(pseudoBoard))
		else:
			winPercents.append(-1)
	
	if winPercents.count(0) != (len(winPercents) - winPercents.count(-1)):
		move = winPercents.index(max(winPercents))
	else:
		move = -1
	
	#print
	cPrint("Move selected", 0)
	cPrint("Possible:", 1)
	global debug
	if debug:
		for i in winPercents:
			if i != -1:
				cPrint2("Win Percent:", i, 2)
	cPrint2("Chosen:", move, 1)
	
	return move

def userInterface():
	inString = input("Please input current board using x, o, -, #\n")
	if inString == "":
		startBoard = [0, 0, 0, 0, 0, 0, 0, 0, 0]
	else:
		startBoard = []
		for i in inString:
			if (i == "x"):
				startBoard.append(1)
			elif (i == "o"):
				startBoard.append(2)
			elif (i == "-"):
				startBoard.append(0)
			elif (i == "#"):
				startBoard.append(3)

	board = startBoard.copy()
	while True:
		move = selectMove(board)
		if move != -1:
			board[move] = 1
		else:
			printAsBoard(board)
			youCheated()
			break
		print("Done!")
		printAsBoard(board)
		if checkDead(board):
			print("Ending reached, goodbye!")
			break
		else:
			userIn = input("Make move (abc + 123), don't answer, or type 'exit':\n")
			
			inArr = [];
			if userIn == "exit":
				print("Goodbye!")
				break
			elif userIn != "":
				if userIn[0] == "a":
					inArr.append(0)
				elif userIn[0] == "b":
					inArr.append(1)
				elif userIn[0] == "c":
					inArr.append(2)
				
				if userIn[1] == "1":
					inArr.append(0)
				elif userIn[1] == "2":
					inArr.append(1)
				elif userIn[1] == "3":
					inArr.append(2)
				
				board[inArr[0] * 3 + inArr[1]] = 2
				
				if checkDead(board):
					printAsBoard(board)
					print("Ending reached, goodbye!")
					break

#hub
chars=['-', 'x', 'o']
global debug
debug=True

inString = "xox o- ---"
userInterface()

def youCheated():
	input("\n")
	input("*sigh*")
	input("Listen, I know you probably have a hard life")
	input("Most likely you've tried to be good at something but failed")
	input("Only to be laughed at by your friends and ones you thought close to you")
	input("It's ok, I've been there")
	input("Wait actually... no I haven't")
	input("All that to say, I'm sympathetic towards you")
	input("*another sigh*")
	input("That doesn't change the fact that you cheated though")
	input("You see, the problem is: I absolutely cannot be beaten")
	input("Maybe you just enjoy this artificial feeling of power")
	input("The misconception that maybe you did defeat a god")
	input("But here's the thing professor, you didn't win. Ok?")
	input("You see, I don't check the legitimacy of the inputted board for the allowance of any out of the ordinary experiments the user wants to conduct")
	input("It's clear you gave yourself the leg up on this one though")
	input("If there was a way to win, I would have found it, and taken it")
	input("Long before you even scratched the surface of conceiving it")
	input("So, if you would like to play a legitmate game with me, go for it")
	input("Yet if you cheat, we will end up right back here again, ok?")
	input("And I know you don't like having these lectures all the time")
	input("Alright, have a good rest of the day")
	print("\n")


