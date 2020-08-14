from random import randint
from random import sample
from copy import deepcopy
import collections

class Dice:
	dice = list()
	dice_grid = [('A','E','A','N','E','G'),
	('A','H','S','P','C','O'),
	('A','S','P','F','F','K'),
	('O','B','J','O','A','B'),
	('I','O','T','M','U','C'),
	('R','Y','V','D','E','L'),
	('L','R','E','I','X','D'),
	('E','I','U','N','E','S'),
	('W','N','G','E','E','H'),
	('L','N','H','N','R','Z'),
	('T','S','T','I','Y','D'),
	('O','W','T','O','A','T'),
	('E','R','T','T','Y','L'),
	('T','O','E','S','S','I'),
	('T','E','R','W','H','V'),
	('N','U','I','H','M','Qu')]

	def get_length(self):
		return len(self.dice_grid)

	def roll(self):
		self.dice = [x[randint(0,5)] for x in self.dice_grid]
		return self.dice

	def shuff(self):
		return sample(self.dice,len(self.dice)) if self.dice else sample(self.roll(),len(self.roll()))

class Game():
	dices = list()
	board = list()
	dim = 4
	def __init__(self,dice):
		self.dices = dice.shuff()
		self.board = [self.dices[i*self.dim:(i*self.dim)+self.dim] for i in range(self.dim)]

	def get_board(self):
		for i in range(0,len(self.board)):
			for j in range(0,len(self.board[i])):
				print("["+self.board[i][j]+"]",end=' ')
			print()

	def change_Qu_Q_internally(self):
		for i in range(0,len(self.board)):
			for j in range(0,len(self.board[i])):
				 if self.board[i][j] == "Qu":
				 	self.board[i][j] = "Q"

class Scorer():

	scores_dict = {3 : 1, 4 : 1, 5 : 2, 6 : 3, 7 : 5}
	checked_words = list()
	scores = list()

	def __init__(self,user_inputs,game):
		self.inputs = user_inputs
		self.dictionary = [line.strip().upper() for line in open('words.txt')]
		self.game = game
		self.indices = collections.defaultdict(list)

	def check_duplicity(self,word):		
		return word in self.checked_words

	def check_insufficient_length(self,word):
		return len(word) < 3

	def check_invalid_word(self,word):	
		return word not in self.dictionary

	def get_character_index(self,w):
		character_present_flag = False
		if w not in self.indices:
			for line in self.game.board:
				for c in range(len(line)):
					if line[c] == w:
						coordinate = (self.game.board.index(line),c)
						character_present_flag = True;
						self.indices[w].append(coordinate)
		else:
			character_present_flag = True
		return character_present_flag

	def check_not_in_grid(self,word):
		word = word.replace("QU","Q")
		for character in word:
			if  not self.get_character_index(character):							 	
			 	return True

		return False

	def get_boolean_board(self,boolean_board):
		for i in range(0,len(boolean_board)):
			for j in range(0,len(boolean_board[i])):
				print("["+str(boolean_board[i][j])+"]",end=' ')
			print()

		print("\n")

	def get_adjacent_coordinate(self,coordinate):
		x = list()
		y = list()

		a = coordinate[0] 
		if a == 0:
			x.extend([0,1])
		elif a == 3:
			x.extend([2,3])
		else:
			x.extend([a-1,a,a+1])

		b = coordinate[1] 
		if b == 0:
			y.extend([0,1])
		elif b == 3:
			y.extend([2,3])
		else:
			y.extend([b-1,b,b+1])

		adjacent_coordinates = [(i,j) for i in x for j in y]		
		adjacent_coordinates.pop(adjacent_coordinates.index(coordinate))
		return adjacent_coordinates

	def check_valid_path(self,coordinates,word,boolean_board):
		if len(word) == 1:
			return True

		if len(coordinates) == 0:
			return False

		coordinate = coordinates[0]

		boolean_board[coordinate[0]][coordinate[1]] = True
		paths = list()
		for x,y in self.get_adjacent_coordinate(coordinate):
			if self.game.board[x][y] == word[1] and boolean_board[x][y] == False:
				paths.append((x,y))

		a = self.check_valid_path(paths,word[1:],deepcopy(boolean_board)) if len(paths) != 0 else False
		boolean_board[coordinate[0]][coordinate[1]] = False
		b = self.check_valid_path(coordinates[1:],word,deepcopy(boolean_board))
		
		return a or b

	def check_same_letter_cube(self,word):			
		word = word.replace("QU","Q")
		boolean_board = [[False for row in range(0,4)] for column in range(0,4)]
		if self.check_valid_path(self.indices[word[0]],word,boolean_board) == True:
			self.checked_words.append(word.replace("Q","QU"))
			return False
		else:
			return True

	def score(self,word):
		word = word.replace("QU","Q")
		word = word.replace("Q","QU")
		if (len(word) < 8):
			sco = self.scores_dict[len(word)]
		else:
			sco = 11
		print("The word {} is worth {} point".format(word,sco))
		self.scores.append(sco)


	def validate(self,word):
		if (self.check_duplicity(word) == True):
			print("The word {} has already been used.".format(word))
			return False

		if (self.check_insufficient_length(word) == True):
			print("The word {} is too short.".format(word))	
			return False

		if (self.check_invalid_word(word) == True):
			print("The word {} is not a word.".format(word))
			return False

		if (self.check_not_in_grid(word) == True):
			print("The word {} is not present in the grid.".format(word))	
			return False

		if (self.check_same_letter_cube(word) == True):
			print("The word {} is not present in the grid.".format(word))	
			return False

		self.score(word)

	def startgrading(self):
		for input in self.inputs:
			self.validate(input.upper())

		print("\nYour total score is {} points!".format(sum(self.scores)))


dice = Dice()
game = Game(dice)
game.get_board()
game.change_Qu_Q_internally()
print("Start typing your words! (press enter after each word and enter 'X' when done):")

user_inputs = list()

current_input = "";
while(current_input not in ['X','x']):
	current_input = input("> ")
	user_inputs.append(current_input)
user_inputs.pop()

scorer = Scorer(user_inputs,game)
scorer.startgrading()