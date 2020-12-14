# author: Tarlan

from typing import *

DUMMY_MAP = [
	["#", "#", "#", "#", "#", "#", "#"],
	["#","=", "=", "#","=", "=", "#"],
	["#", "=", "=", "#", "F", "=", "#"],
	["#","=","=","=","=","=","#"],
	["#","=","=","T","=","=","#"],
	["#","S","=","=","=","=","#"],
	["#","#","#","#","#","#","#"]
]

WALL = "#"
ROAD = "="
TAXI = "T"
START = "S"
FINISH = "F"


def main():
	a = locateObjects(DUMMY_MAP)
	print(a)


def locateObjects(grid: List[int]):
	"""Locates and returns the coordinates of the taxi, start, and finish"""
	taxi, start, finish = ((-1, -1), (-1, -1), (-1, -1))
	
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			point = grid[j][i]
			if point == TAXI:
				taxi = (i, j)
			elif point == START:
				start = (i, j)
			elif point == FINISH:
				finish = (i, j)
	
	return (taxi, start, finish)


if __name__ == "__main__":
	main()