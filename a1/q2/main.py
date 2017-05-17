# usage: python main.py <forwardCheck> <inputfile>

import sys
from math import floor
from copy import deepcopy
from random import randint

class Puzzle(object):

    def __init__(self, forwardCheck):
        self.assignments = []
        self.empty = []
        self.domain = {1,2,3,4,5,6,7,8,9}
        self.remaining = []
        self.forwardCheck = forwardCheck

    def fill(self, inputPuzzle):
        for line in inputPuzzle:
            self.assignments.append(line.rstrip().split(','))

        if puzzle.forwardCheck:
            # fill grid of remaining possible values for forward checking
            for r in range(9):
                self.remaining.append([])
                for c in range(9):
                    self.remaining[r].append(deepcopy(self.domain)) # create a copy in each cell in self.remaining
                # for
            # for

        r = 0
        for row in self.assignments:
            c = 0
            for value in row:
                if value == '':
                    cellCoords = (r, c) # (r, c) are the coordinates of the current cell
                    self.empty.append(cellCoords)
                else:
                    self.setCell((r, c), int(value)) # convert values to ints
                    if self.forwardCheck:
                        self.removeFromRemaining((r, c), int(value))
                c += 1
            # for
            r += 1
        # for

    def removeFromRemaining(self, selectedCell, value):
        r = selectedCell[0]
        c = selectedCell[1]

        for i in range(9):
            # print(self.remaining[r][i])
            self.remaining[r][i] = [x for x in self.remaining[r][i] if x != value]
            # print(self.remaining[r][i])
            self.remaining[i][c] = [x for x in self.remaining[i][c] if x != value]
        # for

        # remove all possible values from selectedCell
        self.remaining[r][c] = []

        # remove as possible value for entire block

        # find top-left cell of block
        blockX = floor(r/3)*3
        blockY = floor(c/3)*3

        for i in range(3):
            for j in range(3):
                self.remaining[blockX + i][blockY + j] = [x for x in self.remaining[blockX + i][blockY + j] if x != value]
            # for
        # for

    def display(self):
        print("   0 1 2 3 4 5 6 7 8\n")

        i = 0
        for row in self.assignments:
            print(i,' ', end='')
            i += 1
            for value in row:
                if value == '':
                    print('_ ', end='')
                else:
                    print(str(value)+' ', end='')
            # for
            print('\n', end='')
        # for

    def displayRemaining(self):
        print("   0 1 2 3 4 5 6 7 8\n")

        i = 0
        for row in self.remaining:
            print(i,' ', end='')
            i += 1
            for value in row:
                if len(value) == 0:
                    print('_ ', end='')
                else:
                    print(str(len(value))+' ', end='')
            # for
            print('\n', end='')
        # for

    def setCell(self, cell, value):
        self.assignments[cell[0]][cell[1]] = value
        if value == '':
            self.empty.append(cell)

    # selects which cell to fill next
    def selectVariable(self):
        numEmpty = len(self.empty)
        selectedCell = self.empty.pop()
        return selectedCell
        # return self.empty.pop( randint(0, numEmpty) )

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
            row = [i for i in self.assignments[r] if i != ''] # get # of values in row - ignore empty spaces, they have no impact on consistency
            rowSet = set(row) # get # of unique values in row
            if len(row) != len(rowSet):
                self.assignments[x][y] = ''
                return False
        # for

        # check alldiff of each column
        for c in range(9):
            col = [row[c] for row in self.assignments if row[c] != '']
            colSet = set(col)
            if len(col) != len(colSet):
                self.assignments[x][y] = ''
                return False
        # for

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
                    # for
                # for

                blockSet = set(block)
                if len(block) != len(blockSet):
                    self.assignments[x][y] = ''
                    return False
            # for
        # for

        return True
#************************* class Puzzle **********************************************

def backtrackingSearch(puzzle):
    if puzzle.isComplete():
        return puzzle

    selectedCell = puzzle.selectVariable()

    # print("cell: ", end='')
    # print(selectedCell)

    for value in puzzle.domain:
        # print("checking value: " + str(value))
        if puzzle.isConsistent(selectedCell, value):

            # puzzle.display()
            # print(puzzle.empty)

            puzzle.setCell(selectedCell, value)

            result = backtrackingSearch( puzzle )

            if result != False:
                return result

    puzzle.setCell(selectedCell, '')
    return False
#************************* def backtrackingSearch **********************************************

# default arguments
forwardCheck = False
inputFile = "easy.txt"

# parse command line arguments
if len(sys.argv) > 1:
    forwardCheck = sys.argv[1]
if len(sys.argv) > 2:
    inputFile = sys.argv[2] + ".txt"

puzzle = Puzzle(forwardCheck)

# read input from file to list
inputPuzzle = open(inputFile)
puzzle.fill( inputPuzzle )

# main

# checks puzzle.remaining against puzzle.assignments
# for i in range(9):
#     for j in range(9):
#         if len(puzzle.remaining[i][j]) == 0 and puzzle.assignments[i][j] == '':
#             print(i,j)
#         else:
#             print('good')

if puzzle.forwardCheck:
    puzzle.displayRemaining()
    print('')
puzzle.display()
completedPuzzle = backtrackingSearch( puzzle )

if completedPuzzle:
    print("\ndone!\n")
    completedPuzzle.display()
else:
    print("Couldn't solve puzzle :(")
