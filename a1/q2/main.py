# usage: python main.py <mode> <inputfile>

import sys
import time
from math import floor, sqrt, pow
from copy import deepcopy
from random import randint, shuffle

class Puzzle(object):

    def __init__(self, mode):
        self.assignments = []
        self.empty = []
        self.domain = {1,2,3,4,5,6,7,8,9}
        self.mode = mode

        # forward checking variables
        # each list stores the values already used for each row, column, or block
        self.rowUsed = []
        self.colUsed = []
        self.blockUsed = []

    # find top-left cell of block, converts that 2-dimensional array index to a 1-dimensional array index
    def blockIdx(self, r, c):
        blockX = floor(r/3)
        blockY = floor(c/3)
        return 3*blockX + blockY

    def fill(self, inputPuzzle):
        for line in inputPuzzle:
            self.assignments.append(line.rstrip().split(','))

        # keeps track of which values have already been used on a row-by-row, col-by-col, or block-by-block basis
        for i in range(9):
            self.rowUsed.append([])
            self.colUsed.append([])
            self.blockUsed.append([])

        r = 0
        for row in self.assignments:
            c = 0
            for value in row:
                if value == '':
                    cellCoords = (r, c) # (r, c) are the coordinates of the current cell
                    self.empty.append(cellCoords)
                else:
                    self.setCell((r, c), int(value)) # convert values to ints
                    if self.mode != 0:
                        self.addToUsed((r, c), int(value))
                c += 1
            # for
            r += 1
        # for

        # after filling empty list, randomize order of variables
        # shuffle(self.empty)

    # adds the value to rowUsed, colUsed, and blockUsed
    def removeFromUsed(self, selectedCell, value):
        r = selectedCell[0]
        c = selectedCell[1]
        b = self.blockIdx(r, c)

        self.rowUsed[r] = [x for x in self.rowUsed[r] if x != value]
        self.colUsed[c] = [x for x in self.colUsed[c] if x != value]
        self.blockUsed[b] = [x for x in self.blockUsed[b] if x != value]

    def addToUsed(self, selectedCell, value):
        r = selectedCell[0]
        c = selectedCell[1]
        b = self.blockIdx(r, c)

        if value not in self.rowUsed[r]:
            self.rowUsed[r].append(value)

        if value not in self.colUsed[c]:
            self.colUsed[c].append(value)

        if value not in self.blockUsed[b]:
            self.blockUsed[b].append(value)

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

    def displayUsed(self):
        print("rows: ")
        for row in self.rowUsed:
            print(row)
        print('')
        print("columns: ")
        for col in self.colUsed:
            print(col)
        print('')
        print("blocks: ")
        for block in self.blockUsed:
            print(block)

    def setCell(self, cell, value):
        r = cell[0]
        c = cell[1]
        b = self.blockIdx(r, c)

        if value == '':
            self.empty.append(cell)
            self.removeFromUsed(cell, self.assignments[r][c])
        else:
            self.addToUsed(cell, value)

        self.assignments[r][c] = value

    # selects which cell to fill next
    def selectVariable(self):
        # empty list has already been shuffled
        selectedCell = self.empty.pop()
        return selectedCell
        # numEmpty = len(self.empty)
        # randIdx = randint(0, numEmpty-1)
        # print(numEmpty, randIdx)
        # return self.empty.pop( randIdx )

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

def backtrackingSearch(puzzle, numNodes, timeLimit, startTime):
    if puzzle.isComplete():
        return puzzle

    # break if exceeding time limit
    if time.time() - startTime > timeLimit:
        return

    selectedCell = puzzle.selectVariable()

    # print("cell: ", end='')
    # print(selectedCell)

    possibleValues = []
    for value in puzzle.domain:
        possibleValues.append(value)
    shuffle(possibleValues)
    # print(possibleValues)

    for value in possibleValues:
        # print("checking value: " + str(value))
        numNodes[0] += 1
        # print(numNodes[0])

        if puzzle.isConsistent(selectedCell, value):

            # puzzle.display()
            # print(puzzle.empty)

            puzzle.setCell(selectedCell, value)

            result = backtrackingSearch( puzzle, numNodes, timeLimit, startTime )

            if result != False:
                return result

    puzzle.setCell(selectedCell, '')
    return False
#************************* def backtrackingSearch **********************************************

startTime = time.time()

# default arguments
mode = 0
inputFile = "easy.txt"

# parse command line arguments
if len(sys.argv) > 1:
    mode = int(sys.argv[1])
if len(sys.argv) > 2:
    inputFile = sys.argv[2] + ".txt"

# main



################# run the puzzles within a time limit #################

timeLimit = 1000
results = []

while (time.time() - startTime < timeLimit):

    puzzle = Puzzle(mode)

    # read input from file to list
    inputPuzzle = open(inputFile)
    puzzle.fill( inputPuzzle )

    puzzle.display()

    # puzzle.displayUsed()
    # exit()

    puzzleStartTime = time.time()
    numNodes = [0] # wrap int in a container so it gets mutated by the recursive calls to backtrackingSearch()
    completedPuzzle = backtrackingSearch( puzzle, numNodes, timeLimit, startTime )

    if completedPuzzle:
        puzzle.display()
        results.append( (time.time()-puzzleStartTime, numNodes[0]) )
    else:
        print("ERROR! could not complete puzzle within time limit.")
        # completedPuzzle.display()

    break

###################################################################

################# analyze results #################

if len(results) == 0:
    exit()

# calculate sums of time & # of nodes
timeSum = 0
nodeSum = 0
for result in results:
    timeSum += result[0]
    nodeSum += result[1]

# calculate means
timeMean = timeSum / len(results)
nodeMean = nodeSum / len(results)
print("time mean: %f, node mean: %f" % (timeMean, nodeMean))

# calculate variance sums
timeVar = 0
nodeVar = 0
for result in results:
    timeVar += pow(result[0] - timeMean, 2)
    nodeVar += pow(result[1] - nodeMean, 2)

# calculate standard deviations
timeSD = sqrt(timeVar / len(results))
nodeSD = sqrt(nodeVar / len(results))
print("time sd: %f, node sd: %f" % (timeSD, nodeSD))

print('\n')
for result in results:
    print(result)

###################################################
