import random

#===============================================================================
#variables----------------------------------------------------------------------
#===============================================================================

#the characters for visualization
chars=['-', 'x', 'o']

#the portions of symmetry across the board
#   0 1 2     # 1 2     0 # 2     0 1 # 
# 0:# # #   1:3 # 5   2:3 # 5   3:3 # 5 
#   6 7 8 	  6 7 #     6 # 8     # 7 8 
symmetry = [
	[[0, 1, 2], [6, 7, 8]],
	[[1, 2, 5], [3, 6, 7]],
	[[0, 3, 6], [2, 5, 8]],
	[[1, 0, 3], [5, 8, 7]]
]

#choose the random highest percent?
randomHighestPercent = True

#===============================================================================
#array--------------------------------------------------------------------------
#===============================================================================

#concatinates an array
def concat(arr1, arr2):
	for i in arr2:
		arr1.append(i)
	return arr1

#gets the sum of all the elements in the array
def getArraySum(array):
	arraySum = 0
	for i in array:
		arraySum = arraySum + i
	return arraySum
	
#returns random highest element
def highestElement(array):
	arrayMax = max(array)
	#the location of the highest elements
	highest = []
	for i in range(len(array)):
		if array[i] == arrayMax:
			highest.append(i)
	return highest[random.randint(0, len(highest) - 1)]

#compares the two sets of numbers with their elements in the array
def compare3x2(set1, set2, array):
	if array[set1[0]] == array[set2[0]] and array[set1[1]] == array[set2[1]] and array[set1[2]] == array[set2[2]]:
		return True
	else:
		return False
		
#removes every instance of an element
def removeElement(array, element):
	rArray = []
	for i in array:
		if i != element:
			rArray.append(i)
	return rArray

#returns element in array[1] of given element in array[0]
def getOpposite(array, element):
	if element in array[0]:
		return array[1][array[0].index(element)]
	elif element in array[1]:
		return array[0][array[1].index(element)]
	else:
		return -1

#===============================================================================
#board management---------------------------------------------------------------
#===============================================================================

#prints a board array in a user friendly way
def printAsBoard(board):
	print("\n\t", chars[board[0]], chars[board[1]], chars[board[2]])
	print("\t", chars[board[3]], chars[board[4]], chars[board[5]])
	print("\t", chars[board[6]], chars[board[7]], chars[board[8]], "\n")

#swaps x and o
def invert(num):
	if num == 1:
		return 2
	elif num == 2:
		return 1
	else:
		return num

#swaps the x's and o's on the board
def invertBoard(board):
	invBoard = []
	for i in board:
		invBoard.append(invert(i))
	return invBoard

#===============================================================================
#checks and comparisons---------------------------------------------------------
#===============================================================================

#equates three elements and returns their value if so. If not it will return the original parameter. For use as: dead = check3(s1, s2, s3, dead)
def check3(s1, s2, s3, original):
	if s1 == s2 and s1 == s3 and s1 != 0:
		return s1
	else:
		return original

#checks if a conclusion has been reached for a board
#0 - not dead
#1 - x
#2 - o
#3 - cat
def checkDead(board):
	if board.count(0) == 0:
		dead = 3
	else:
		dead = 0
	
	dead = check3(board[0], board[1], board[2], dead)
	dead = check3(board[3], board[4], board[5], dead)
	dead = check3(board[6], board[7], board[8], dead)
	
	dead = check3(board[0], board[3], board[6], dead)
	dead = check3(board[1], board[4], board[7], dead)
	dead = check3(board[2], board[5], board[8], dead)
	
	dead = check3(board[0], board[4], board[8], dead)
	dead = check3(board[6], board[4], board[2], dead)
	
	return dead
	
#===============================================================================
#algorithm----------------------------------------------------------------------
#===============================================================================


#returns one percent based on player
def handleWinPercents(winPercents, player):
	#if these are x's possible moves
	if player == 1:
		#return the maximum of the percents
		return max(winPercents)

	#if these are o's possible moves
	elif player == 2:
		#remove the -1's in winPercents
		winPercents = removeElement(winPercents, -1)
		#return the average of all the elements
		return getArraySum(winPercents) / len(winPercents)
		
		
#gets the likelyhood that x will win for every possible move
def getWinPercents(board, player):
	#-----------------------------------------------------------setup
	#create array for lines of symmetry
	symmetryLines = [False, False, False, False]
	#is the first line symmetrical?
	if compare3x2(symmetry[0][0], symmetry[0][1], board):
		symmetryLines[0] = True
	if compare3x2(symmetry[1][0], symmetry[1][1], board):
		symmetryLines[1] = True
	if compare3x2(symmetry[2][0], symmetry[2][1], board):
		symmetryLines[2] = True
	if compare3x2(symmetry[3][0], symmetry[3][1], board):
		symmetryLines[3] = True
	
	#-----------------------------------------------------------looping
	#create the array we will be returning and fill it with -1
	#-1 represents an impossible move
	winPercents = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
	#for every space on the board
	for space in range(len(board)):
		#--------------------------------------------------win percent
		#check if it is an open space and if the win percent isn't already there, if so:
		if board[space] == 0 and winPercents[space] == -1:
			#create a copy of the board
			psBoard = board.copy();
			#put the player's character on the copy board where the space is
			psBoard[space] = player;
			
			#check if the  copy board is dead
			dead = checkDead(psBoard);
			#if x won
			if dead == 1:
				#return a 100% win chance
				winPercent = 100
			#if o won
			elif dead == 2:
				#return a 0% win chance
				winPercent = 0
			#if it's a cat game
			elif dead == 3:
				#return a 50% win chance
				winPercent = 50
			#if game can continue
			else:
				#get the win percents for the copy board
				psWinPercents = getWinPercents(psBoard, invert(player));
				#handle the win percents for the copy board and set the win percent to the result
				winPercent = handleWinPercents(psWinPercents, invert(player))
			#add our win percent to the array
			winPercents[space] = winPercent
			
			#---------------------------------------------symmetry
			#if the first line is symmetrical and the space is able to duplicate
			if symmetryLines[0] and getOpposite(symmetry[0], space) != -1:
				#set the win percent to the opposite space
				winPercents[getOpposite(symmetry[0], space)] = winPercent
			#if the line is symmetrical and the space is able to duplicate
			if symmetryLines[1] and getOpposite(symmetry[1], space) != -1:
				#set the win percent to the opposite space
				winPercents[getOpposite(symmetry[1], space)] = winPercent
			#if the first line is symmetrical and the space is able to duplicate
			if symmetryLines[2] and getOpposite(symmetry[2], space) != -1:
				#set the win percent to the opposite space
				winPercents[getOpposite(symmetry[2], space)] = winPercent
			#if the first line is symmetrical and the space is able to duplicate
			if symmetryLines[3] and getOpposite(symmetry[3], space) != -1:
				#set the win percent to the opposite space
				winPercents[getOpposite(symmetry[3], space)] = winPercent
				
	#print
	print("Got win percent for " + chars[player] + ":", board)
	for i in winPercents:
		print("\t", i)
	#return the win percents
	return winPercents


#selects the best move for player on the given board
def selectMove(board, player):
	#if the player is o then invert the board
	if player == 2:
		board = invertBoard(board)
	
	#get the moves for x move (if the player was o it will invert)
	moves = getWinPercents(board, 1)
	#select the best one at random
	return highestElement(moves)

#===============================================================================
#main---------------------------------------------------------------------------
#===============================================================================

print(selectMove([1, 0, 0, 0, 0, 0, 0, 0, 0], 2))


