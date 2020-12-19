# author: Tarlan
from enum import Enum
from typing import *
import pynput #TODO: Replace it with pygame's key handler
from pynput import keyboard
from pynput.keyboard import Key

DUMMY_MAP = [ # original
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
MOVE_COST = 1
WRONG_PICKUP_COST = -10
DROP_OFF_REWARD = 30


class Direction(Enum):
	NORTH = "North"
	WEST = "West"
	EAST = "East"
	SOUTH = "South"
	
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
	
	originalGrid = DUMMY_MAP
	currentGrid = DUMMY_MAP
	
	taxiPosition = (-1, -1)
	startPosition = (-1, -1)
	finishPosition = (-1, -1)
	
	isPassengerTaken = False
	
	score = 1000
	
	
	def run(self):
		self.printGrid(self.currentGrid)
		self.locateObjects(self.currentGrid)
		
		print("taxi:", self.taxiPosition, "start:", self.startPosition, "finish:", self.finishPosition)
		print(self.getValidMoves())
		
		listener = keyboard.Listener(on_press=self.on_press)
		listener.start()
		listener.join()
		
	
	def move(self, direction: Direction):
		"""Given a direction and a grid, updates the current grid so that it shows the next position of the taxi.
		\n Side effect: triggers reward calculation"""
		
		newPosition = None
		
		if direction == Direction.NORTH:
			newPosition = Direction.getNorth(self.taxiPosition)
		if direction == Direction.SOUTH:
			newPosition = Direction.getSouth(self.taxiPosition)
		if direction == Direction.WEST:
			newPosition = Direction.getWest(self.taxiPosition)
		if direction == Direction.EAST:
			newPosition = Direction.getEast(self.taxiPosition)
		
		# replace cell with T
		self.currentGrid[newPosition[0]][newPosition[1]] = TAXI_SYMBOL
		
		# replace the old cell with a road
		self.currentGrid[self.taxiPosition[0]][self.taxiPosition[1]] = ROAD_SYMBOL
		
		# update taxi position
		self.taxiPosition = newPosition
		

	def getValidMoves(self) -> List[Direction]:
		"""Returns a list of valid moves for the taxi"""
		validMoves = [Direction.NORTH, Direction.WEST, Direction.EAST, Direction.SOUTH]
		grid = self.currentGrid
		
		x = self.taxiPosition[0]
		y = self.taxiPosition[1]
		
		westPoint = Direction.getWest((x, y))
		eastPoint = Direction.getEast((x, y))
		northPoint = Direction.getNorth((x, y))
		southPoint = Direction.getSouth((x, y))
		
		if grid[westPoint[0]][westPoint[1]] == WALL_SYMBOL:
			validMoves.remove(Direction.WEST)
		if grid[eastPoint[0]][eastPoint[1]] == WALL_SYMBOL:
			validMoves.remove(Direction.EAST)
		if grid[northPoint[0]][northPoint[1]] == WALL_SYMBOL:
			validMoves.remove(Direction.NORTH)
		if grid[southPoint[0]][southPoint[1]] == WALL_SYMBOL:
			validMoves.remove(Direction.SOUTH)
		
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
		
	
	@staticmethod
	def printGrid(grid):
		"""Prints the given grid"""
		for i in range(len(grid)):
			for j in range(len(grid[i])):
				# print((i,j),grid[i][j], end=" ")
				print(grid[i][j], end=" ")
			print()
	

	def on_press(self, key):
		validMoves = self.getValidMoves()
		
		if key == Key.up:
			if Direction.NORTH not in validMoves:
				return
			self.move(Direction.NORTH)
		elif key == Key.down:
			if Direction.SOUTH not in validMoves:
				return
			self.move(Direction.SOUTH)
		elif key == Key.left:
			if Direction.WEST not in validMoves:
				return
			self.move(Direction.WEST)
		elif key == Key.right:
			if Direction.EAST not in validMoves:
				return
			self.move(Direction.EAST)
		
		self.printGrid(self.currentGrid)


def main():
	GameController().run()


if __name__ == "__main__":
	main()
