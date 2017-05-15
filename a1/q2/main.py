# usage: python main.py <inputfile>

import sys
from random import randint

class Puzzle(object):

    def __init__(self):
        self.assignments = []
        self.empty = []
        self.domain = {1,2,3,4,5,6,7,8,9}

    # selects which cell to fill next
    def selectVariable(self):
        return self.empty[ randint(0, len(self.empty)) ]

    # checks if entire puzzle is filled out
    def isComplete(self):
        return len(self.empty) == 0

    # check if given value follows restraints
    def isConsistent(self, value):
        # TODO: check alldiff of each row
        # TODO: check alldiff of each col
        # TODO: check alldiff of each block
        return False


# parse command line arguments
inputFile = "easy.txt"
if len(sys.argv) > 1:
    inputFile = sys.argv[1] + ".txt"

puzzle = Puzzle()

# read input from file to list
sudokuInput = open(inputFile)
for line in sudokuInput:
    puzzle.assignments.append(line.rstrip().split(','))

domain = {1,2,3,4,5,6,7,8,9}

r = 0
for row in puzzle.assignments:
    print row
    c = 0
    for cell in row:
        if cell == '':
            cellCoords = (r, c) # (r, c) are the coordinates of the interatee cell
            puzzle.empty.append(cellCoords)
        c += 1
    r += 1

print puzzle.empty
print puzzle.selectVariable()

def backtrackingSearch(puzzle):
    if puzzle.isComplete():
        return puzzle
    var = puzzle.selectVariable()

    for value in domainValues():
        if puzzle.isConsistent(value):
            puzzle[x][y] = value

            result = backtrackingSearch(puzzle)

            if result != False:
                return result

            puzzle[x][y] = ''
    return False
