# usage: python main.py <inputfile>

import sys
from random import randint

class Puzzle(object):

    def __init__(self):
        self.assignments = []
        self.empty = []
        self.domain = {1,2,3,4,5,6,7,8,9}

    def setCell(self, cell, value):
        self.assignments[cell[0]][cell[1]] = value

    # selects which cell to fill next
    def selectVariable(self):
        # return (0,0)
        return self.empty.pop( randint(0, len(self.empty)) )

    # checks if entire puzzle is filled out
    def isComplete(self):
        return len(self.empty) == 0

    # check if given value follows restraints
    def isConsistent(self, selectedCell, value):
        x = selectedCell[0]
        y = selectedCell[1]
        self.assignments[x][y] = value

        # check alldiff of each row
        for r in range(9):
            row = [x for x in self.assignments[r] if x != ''] # get # of values in row - ignore empty spaces, they have no impact on consistency
            rowSet = set(row) # get # of unique values in row
            if len(row) != len(rowSet):
                # print row
                # print rowSet
                return False

        # check alldiff of each column
        for c in range(9):
            col = [row[c] for row in self.assignments if row[c] != '']
            colSet = set(col)
            if len(col) != len(colSet):
                # print col
                # print colSet
                return False

        # check alldiff of each block
        # (blockX, blockY) is the top-left most cell of each block
        for blockX in {0,3,6}:
            for blockY in {0,3,6}:
                block = []

                # loop over each cell in the block
                for i in range(3):
                    for j in range(3):
                        value = self.assignments[blockX + i][blockY + j]
                        if value != '':
                            block.append( value )

                blockSet = set(block)
                if len(block) != len(blockSet):
                    # print block
                    # print blockSet
                    return False

        return True

def backtrackingSearch(puzzle):
    if puzzle.isComplete():
        return puzzle
    selectedCell = puzzle.selectVariable()
    print "cell: ",
    print selectedCell

    for value in puzzle.domain:
        print "checking value: " + str(value)
        if puzzle.isConsistent(selectedCell, value):
            print "consistent!"

            puzzle.setCell(selectedCell, value)

            result = backtrackingSearch(puzzle)

            if result != False:
                return result

            puzzle.setCell(selectedCell, '')
    return False

puzzle = Puzzle()

# parse command line arguments
inputFile = "easy.txt"
if len(sys.argv) > 1:
    inputFile = sys.argv[1] + ".txt"

# read input from file to list
sudokuInput = open(inputFile)
for line in sudokuInput:
    puzzle.assignments.append(line.rstrip().split(','))

r = 0
for row in puzzle.assignments:
    c = 0
    for value in row:
        if value == '':
            cellCoords = (r, c) # (r, c) are the coordinates of the current cell
            puzzle.empty.append(cellCoords)
        else:
            puzzle.setCell((r, c), int(value)) # convert values to ints
        c += 1
    print row
    r += 1

# main
completedPuzzle = backtrackingSearch(puzzle)

if completedPuzzle != False:
    for row in completedPuzzle:
        print row
else:
    print "could not complete puzzle"
