# author: Tarlan
from enum import Enum
from threading import Thread
from typing import *
from pynput import keyboard
from pynput.keyboard import Key  # TODO: Replace it with pygame's key handler
from copy import deepcopy

from GameGraphics import GameGraphics
from MapGenerator import MapGenerator

DUMMY_MAP = [  # original
	["#", "#", "#", "#", "#", "#", "#"],
	["#", "=", "=", "#", "=", "=", "#"],
	["#", "=", "=", "#", "F", "=", "#"],
	["#", "=", "=", "=", "=", "=", "#"],
	["#", "=", "=", "T", "=", "=", "#"],
	["#", "S", "=", "=", "=", "=", "#"],
	["#", "#", "#", "#", "#", "#", "#"]
]

DUMMY_MAP = [
	["#", "#", "#", "#", "#", "#", "#"],
	["#", "=", "=", "#", "=", "=", "#"],
	["#", "=", "=", "#", "F", "=", "#"],
	["#", "=", "=", "=", "=", "=", "#"],
	["#", "=", "=", "=", "=", "=", "#"],
	["#", "S", "=", "=", "=", "T", "#"],
	["#", "#", "#", "#", "#", "#", "#"]
]

WALL_SYMBOL = "#"
ROAD_SYMBOL = "="
TAXI_SYMBOL = "T"
START_SYMBOL = "S"
FINISH_SYMBOL = "F"

# Rewards
WALL_COST = 1
MOVE_COST = 1
WRONG_DROP_OFF_COST = -10
DROP_OFF_REWARD = 30


class Action(Enum):
	NORTH = "North"
	WEST = "West"
	EAST = "East"
	SOUTH = "South"
	PICK_UP = "Pick Up"
	DROP_OFF = "Drop Off"
	
	@staticmethod
	def getNorth(ofPoint: Tuple[int, int]) -> Tuple[int, int]:
		return ofPoint[0] - 1, ofPoint[1]
	
	@staticmethod
	def getSouth(ofPoint: Tuple[int, int]) -> Tuple[int, int]:
		return ofPoint[0] + 1, ofPoint[1]
	
	@staticmethod
	def getWest(ofPoint: Tuple[int, int]) -> Tuple[int, int]:
		return ofPoint[0], ofPoint[1] - 1
	
	@staticmethod
	def getEast(ofPoint: Tuple[int, int]) -> Tuple[int, int]:
		return ofPoint[0], ofPoint[1] + 1


class GameController:
	# originalGrid = deepcopy(DUMMY_MAP)  # we need a deepcopy because otherwise it will be the same as currentGrid
	# currentGrid = DUMMY_MAP
	
	originalGrid = MapGenerator(5, 5, 5, 2).generate()  # we need a deepcopy because otherwise it will be the same as currentGrid
	currentGrid = deepcopy(originalGrid)
	
	graphics = GameGraphics()
	
	taxiPosition = (-1, -1)
	startPosition = (-1, -1)
	finishPosition = (-1, -1)
	
	isCustomerPickedUp = False
	isGameFinished = False
	
	score = 1000
	
	def run(self):
		self.printGrid(self.currentGrid)
		self.locateObjects(self.currentGrid)
		
		print("taxi:", self.taxiPosition, "start:", self.startPosition, "finish:", self.finishPosition)
		
		self.graphics.drawGrid(self.originalGrid)
		
		listener = keyboard.Listener(on_press=self.on_press)
		listener.start()
		
		thread = Thread(target=self.graphics.activateScreen())
		thread.start()
	
	def move(self, direction: Action):
		"""Given a direction and a grid, updates the current grid so that it shows the next position of the taxi.
		\n Side effect: triggers reward calculation"""
		
		newPosition = self.getNextPoint(direction)
		
		# replace cell with T
		self.currentGrid[newPosition[0]][newPosition[1]] = TAXI_SYMBOL
		
		# replace the old cell
		if self.originalGrid[self.taxiPosition[0]][self.taxiPosition[1]] not in [START_SYMBOL, FINISH_SYMBOL]:
			self.currentGrid[self.taxiPosition[0]][self.taxiPosition[1]] = ROAD_SYMBOL
		else:
			self.currentGrid[self.taxiPosition[0]][self.taxiPosition[1]] = self.originalGrid[self.taxiPosition[0]][
				self.taxiPosition[1]]
		
		# update taxi position
		self.taxiPosition = newPosition
		
		self.updateScore(direction)
	
	def step(self, action: Action):
		""" Returns next state of grid after taking an action"""
		newGrid = deepcopy(self.currentGrid)
		
		if action not in self.getValidMoves():
			return newGrid
		
		newPosition = self.getNextPoint(action)
		
		# replace cell with T
		newGrid[newPosition[0]][newPosition[1]] = TAXI_SYMBOL
		
		# replace the old cell
		if self.originalGrid[self.taxiPosition[0]][self.taxiPosition[1]] not in [START_SYMBOL, FINISH_SYMBOL]:
			newGrid[self.taxiPosition[0]
			][self.taxiPosition[1]] = ROAD_SYMBOL
		else:
			newGrid[self.taxiPosition[0]][self.taxiPosition[1]] = self.originalGrid[self.taxiPosition[0]][
				self.taxiPosition[1]]
		
		return newGrid
	
	def getReward(self, action: Action):
		"""Updates the score based on the reward of moving from startPoint to endPoint"""
		reward = 0
		currentOriginalChar = self.originalGrid[self.taxiPosition[0]]
		[self.taxiPosition[1]]
		
		if action == Action.DROP_OFF:
			if self.isCustomerPickedUp and currentOriginalChar == FINISH_SYMBOL:  # correct drop off
				print("CORRECT DROP OFF")
				reward += DROP_OFF_REWARD
			else:
				print("WRONG DROP OFF")
				reward += WRONG_DROP_OFF_COST
		elif action not in self.getValidMoves():
			reward -= WALL_COST
		else:
			reward -= MOVE_COST
		
		return reward
	
	def pickUp(self):
		"""Updates the current grid so that it shows the next state after picking up the customer
		\n Side effect: triggers reward calculation"""
		self.updateScore(Action.PICK_UP)
		
		currentOriginalChar = self.originalGrid[self.taxiPosition[0]][self.taxiPosition[1]]
		if currentOriginalChar != START_SYMBOL:
			return
		
		self.originalGrid[self.startPosition[0]][self.startPosition[1]] = ROAD_SYMBOL
		
		self.isCustomerPickedUp = True
	
	def dropOff(self):
		"""Updates the current grid so that it shows the next state after dropping off the customer
		\n Side effect: triggers reward calculation"""
		self.updateScore(Action.DROP_OFF)
		
		currentOriginalChar = self.originalGrid[self.taxiPosition[0]][self.taxiPosition[1]]
		if currentOriginalChar != FINISH_SYMBOL or not self.isCustomerPickedUp:
			return
		
		self.originalGrid[self.startPosition[0]][self.startPosition[1]] = ROAD_SYMBOL
		
		self.isCustomerPickedUp = False
		self.endGame()
	
	def endGame(self):
		self.isGameFinished = True
		print("\n\nGame finished!")
		print("Final score:", self.score)
	
	def updateScore(self, action: Action):
		"""Updates the score based on the reward of moving from startPoint to endPoint"""
		currentOriginalChar = self.originalGrid[self.taxiPosition[0]][self.taxiPosition[1]]
		
		if action == Action.PICK_UP:
			pass
			# if currentOriginalChar != START_SYMBOL:  # wrong pickup
			# 	print("WRONG PICKUP at", currentOriginalChar)
			# 	self.score += WRONG_PICKUP_COST
		
		elif action == Action.DROP_OFF:
			if self.isCustomerPickedUp and currentOriginalChar == FINISH_SYMBOL:  # correct drop off
				print("CORRECT DROP OFF")
				self.score += DROP_OFF_REWARD
			elif self.isCustomerPickedUp:
				print("WRONG DROP OFF")
				self.score += WRONG_DROP_OFF_COST
		
		else:
			self.score -= MOVE_COST
	
	def on_press(self, key):
		if self.isGameFinished:
			return
		
		validMoves = self.getValidMoves()
		
		if key == Key.up:
			if Action.NORTH not in validMoves:
				return
			self.move(Action.NORTH)
		elif key == Key.down:
			if Action.SOUTH not in validMoves:
				return
			self.move(Action.SOUTH)
		elif key == Key.left:
			if Action.WEST not in validMoves:
				return
			self.move(Action.WEST)
		elif key == Key.right:
			if Action.EAST not in validMoves:
				return
			self.move(Action.EAST)
		elif hasattr(key, 'char') and key.char == 'p':
			self.pickUp()
		elif hasattr(key, 'char') and key.char == 'd':
			self.dropOff()
		else:
			return
		
		if not self.isGameFinished:
			self.printGrid(self.currentGrid)
			self.graphics.drawGrid(self.currentGrid)
			print("SCORE:", self.score, "CUSTOMER :", self.isCustomerPickedUp)
			
			
	
	def getValidMoves(self) -> List[Action]:
		"""Returns a list of valid moves for the taxi"""
		validMoves = [Action.NORTH, Action.WEST, Action.EAST, Action.SOUTH, Action.PICK_UP, Action.DROP_OFF]
		grid = self.currentGrid
		
		x = self.taxiPosition[0]
		y = self.taxiPosition[1]
		
		westPoint = Action.getWest((x, y))
		eastPoint = Action.getEast((x, y))
		northPoint = Action.getNorth((x, y))
		southPoint = Action.getSouth((x, y))
		
		if grid[westPoint[0]][westPoint[1]] == WALL_SYMBOL:
			validMoves.remove(Action.WEST)
		if grid[eastPoint[0]][eastPoint[1]] == WALL_SYMBOL:
			validMoves.remove(Action.EAST)
		if grid[northPoint[0]][northPoint[1]] == WALL_SYMBOL:
			validMoves.remove(Action.NORTH)
		if grid[southPoint[0]][southPoint[1]] == WALL_SYMBOL:
			validMoves.remove(Action.SOUTH)
		
		return validMoves
	
	def locateObjects(self, grid: List[List[str]]):
		"""Locates and sets the coordinates of the taxi, start, and finish"""
		for i in range(len(grid)):
			for j in range(len(grid[i])):
				point = grid[i][j]
				if point == TAXI_SYMBOL:
					self.taxiPosition = (i, j)
				elif point == START_SYMBOL:
					self.startPosition = (i, j)
				elif point == FINISH_SYMBOL:
					self.finishPosition = (i, j)
	
	def getNextPoint(self, direction: Action) -> Tuple[int, int]:
		newPosition = self.taxiPosition
		
		if direction == Action.NORTH:
			newPosition = Action.getNorth(self.taxiPosition)
		if direction == Action.SOUTH:
			newPosition = Action.getSouth(self.taxiPosition)
		if direction == Action.WEST:
			newPosition = Action.getWest(self.taxiPosition)
		if direction == Action.EAST:
			newPosition = Action.getEast(self.taxiPosition)
		
		return newPosition
	
	@staticmethod
	def printGrid(grid):
		"""Prints the given grid"""
		print()
		for i in range(len(grid)):
			for j in range(len(grid[i])):
				# print((i,j),grid[i][j], end=" ")
				print(grid[i][j], end=" ")
			print()


def main():
	GameController().run()


if __name__ == "__main__":
	main()
