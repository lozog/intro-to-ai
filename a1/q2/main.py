# usage: python main.py <mode> <inputfile>

import sys
import time
from math import floor, sqrt, pow
from copy import deepcopy
from random import randint, shuffle, choice

class Puzzle(object):

    def __init__(self, mode):
        self.assignments = []
        self.empty = []
        self.domain = {1,2,3,4,5,6,7,8,9}
        self.mode = mode

        # each list stores the values already used for each row, column, or block
        self.rowUsed = []
        self.colUsed = []
        self.blockUsed = []

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
                c += 1
            # for
            r += 1
        # for

        # after filling empty list, randomize order of variables
        # unless we're using heuristics
        if mode != 2:
            shuffle(self.empty)

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

    def getRemainingMoves(self, cell):
        r = cell[0]
        c = cell[1]
        b = self.blockIdx(r, c)

        movesRemaining = [1,2,3,4,5,6,7,8,9]
        movesRemaining = [x for x in movesRemaining if x not in self.rowUsed[r]]
        movesRemaining = [x for x in movesRemaining if x not in self.colUsed[c]]
        movesRemaining = [x for x in movesRemaining if x not in self.blockUsed[b]]

        return movesRemaining

    def getNumOfRemainingMoves(self, cell):
        return len( self.getRemainingMoves(cell) )

    def getNumConstraining(self, cell):
        r = cell[0]
        c = cell[1]
        b = self.blockIdx(r, c)

        constrainedCells = set() # use a set to not count duplicates
        for i in range(9):
            if self.assignments[r][i] == '':
                constrainedCells.add( (r,i) )
        for i in range(9):
            if self.assignments[i][c] == '':
                constrainedCells.add( (i, c) )

        rb = floor(b / 3) * 3
        cb = (b % 3) * 3
        for i in range(3):
            for j in range(3):
                if self.assignments[rb + i][cb + j] == '':
                    constrainedCells.add( (rb + i, cb + j) )

        # print(cell,len(constrainedCells))
        # print(constrainedCells)
        return len(constrainedCells)

    # count occurrences of values in the cells that cell constrains
    def getNumConstrainingValue(self, cell, value):
        r = cell[0]
        c = cell[1]
        b = self.blockIdx(r, c)

        seenCells = set() # use a set to not count duplicates
        count = 0

        for i in range(9):
            if (r, i) in seenCells:
                continue

            if self.assignments[r][i] == '':
                seenCells.add( (r,i) )
                if value in self.getRemainingMoves( (r, i) ):
                    count += 1
                    # print((r,i))
        # for

        for i in range(9):
            if (i, c) in seenCells:
                continue

            if self.assignments[i][c] == '':
                seenCells.add( (i, c) )
                if value in self.getRemainingMoves( (i, c) ):
                    count += 1
                    # print((i,c))
        # for

        rb = floor(b / 3) * 3
        cb = (b % 3) * 3
        for i in range(3):
            for j in range(3):
                if (rb + i, cb + j) in seenCells:
                    continue

                if self.assignments[rb + i][cb + j] == '':
                    seenCells.add( (rb + i, cb + j) )
                    if value in self.getRemainingMoves( (rb + i, cb + j) ):
                        count += 1
                        # print( (rb + i, cb + j) )
            # for
        return count

    def selectValue(self, selectedCell, attemptedValues):
        remainingValues = self.getRemainingMoves(selectedCell)
        possibleValues = tuple(self.domain.difference( attemptedValues ))

        # print("remainingValues", remainingValues)
        possibleValues = [ x for x in possibleValues if x in remainingValues ]

        # print("possibleValues", possibleValues)

        if len(possibleValues) == 0:
            return False

        if mode != 2:
            # randomly select from remaining values
            selectedValue = choice( possibleValues )
        else:
            # use Least Constraining Value heuristic to choose from remaining values
            leastConstrainingCount = -1
            leastConstraining = []
            for value in possibleValues:
                numConstraining = self.getNumConstrainingValue(selectedCell, value)
                # print(selectedCell, value, numConstraining)
                if len(leastConstraining) == 0:
                    # base case
                    leastConstraining.append(value)
                    leastConstrainingCount = numConstraining
                elif numConstraining < leastConstrainingCount:
                    leastConstrainingCount = numConstraining
                    leastConstraining = [ value ]
                elif numConstraining == leastConstrainingCount:
                    leastConstraining.append(value)
            # for
            # print(selectedCell, leastConstraining)
            # if there are still possibilities, randomly choose.
            selectedValue = leastConstraining[ randint(0, len(leastConstraining)-1) ]

        return selectedValue

    # selects which cell to fill next
    def selectVariable(self):
        # heuristics:
        # variable (cell): most constrained:
        # fewest legal moves
        # go throught entire grid, find cell with fewest legal values
        mostConstrained = []
        currentNumMostConstrained = -1
        if mode == 2:
            for cell in self.empty:
                numMostConstrained = self.getNumOfRemainingMoves(cell)
                # print(cell,numMostConstrained)

                if len(mostConstrained) == 0:
                    # base case
                    currentNumMostConstrained = numMostConstrained
                    mostConstrained.append( cell )
                else:
                    # if # is new lowest, save it
                    # print(numMostConstrained, currentNumMostConstrained)
                    if numMostConstrained < currentNumMostConstrained:
                        currentNumMostConstrained = numMostConstrained
                        mostConstrained = [ cell ]
                    elif numMostConstrained == currentNumMostConstrained:
                        mostConstrained.append( cell )
            # for
            # print("mostConstrained:", mostConstrained)

            # tiebreaker: most constraining
            # cell with most other empty cells in its row, col, and block
            # for each cell: find cell with LEAST # of things in its rowUSed, colUsed, and blockUsed
            mostConstraining = []
            currentNumConstraining = -1
            for cell in mostConstrained:
                # do shit
                numConstraining = self.getNumConstraining(cell)

                if len(mostConstrained) == 0:
                    # base case
                    currentNumConstraining = numConstraining
                    mostConstraining.append( cell )
                else:
                    # if # is new highest, save it
                    # print(numConstraining, currentNumConstraining)
                    if numConstraining > currentNumConstraining:
                        currentNumConstraining = numConstraining
                        mostConstraining = [ cell ]
                    elif numConstraining == currentNumConstraining:
                        mostConstraining.append( cell )
                # print(mostConstraining)
            # for

            # print("mostConstraining:", mostConstraining)

            # if there are still possibilities, randomly choose.
            selectedCell = mostConstraining[ randint(0, len(mostConstraining)-1) ]
            self.empty.remove( selectedCell )

            # print("randomly selected", selectedCell)

            # print(mostConstrained)
            return selectedCell

        else:
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
        r = selectedCell[0]
        c = selectedCell[1]
        b = self.blockIdx(r, c)

        # ez
        if value in self.rowUsed[r]:
            return False
        if value in self.colUsed[c]:
            return False
        if value in self.blockUsed[b]:
            return False

        return True

    # forward-check after placing selectedCell
    def forwardCheck(self, selectedCell):
        r0 = selectedCell[0]
        c0 = selectedCell[1]
        b0 = self.blockIdx(r0, c0)

        # check that entire row still has legal moves remaining
        for i in range(9):
            r = r0
            c = i
            if self.assignments[r][c] != '':
                break

            if not self.getNumOfRemainingMoves( (r, c) ):
                return False
        # for

        # check that entire column still has legal moves remaining
        for i in range(9):
            r = i
            c = c0
            if self.assignments[r][c] != '':
                break

            if not self.getNumOfRemainingMoves( (r, c) ):
                return False
        # for

        # check that entire block still has legal moves remaining
        # print("forward checking:", selectedCell)
        rb = floor(b0 / 3) * 3
        cb = (b0 % 3) * 3
        # print("topleft of block:",rb,cb)
        for i in range(3):
            for j in range(3):
                r = rb + i
                c = cb + j

                if self.assignments[r][c] != '':
                    break

                if not self.getNumOfRemainingMoves( (r, c) ):
                    return False
            # for
        # for
        # print('')

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

    valuesAttempted = set()

    for i in range(9): # domain has 9 possible values
        value = puzzle.selectValue( selectedCell, valuesAttempted )
        if not value: # no more possible values remaining
            break
        valuesAttempted.add( value )

        numNodes[0] += 1
        # print(numNodes[0])

        if puzzle.isConsistent(selectedCell, value):

            puzzle.setCell(selectedCell, value)

            # puzzle.display()
            # print(puzzle.empty)

            # forward checking
            if puzzle.mode > 0:
                if puzzle.forwardCheck(selectedCell):
                    result = backtrackingSearch( puzzle, numNodes, timeLimit, startTime )
                    if result != False:
                        return result
            else:
                result = backtrackingSearch( puzzle, numNodes, timeLimit, startTime )
                if result != False:
                    return result

            puzzle.removeFromUsed(selectedCell, value)
    # for

    puzzle.setCell(selectedCell, '')
    return False
#************************* def backtrackingSearch **********************************************

################# begin program - read in arguments ##############################

startTime = time.time()

# default arguments
mode = 0
inputFile = "easy.txt"

# parse command line arguments
if len(sys.argv) > 1:
    mode = int(sys.argv[1])
if len(sys.argv) > 2:
    inputFile = sys.argv[2] + ".txt"

#######################################################################

################# run the puzzles within a time limit #################

timeLimit = 1000
results = []
numCompleted = 0

while (time.time() - startTime < timeLimit):

    puzzle = Puzzle(mode)

    # read input from file to list
    inputPuzzle = open(inputFile)
    puzzle.fill( inputPuzzle )

    # puzzle.display()

    # puzzle.displayUsed()
    # exit()

    puzzleStartTime = time.time()
    numNodes = [0] # wrap int in a container so it gets mutated by the recursive calls to backtrackingSearch()
    completedPuzzle = backtrackingSearch( puzzle, numNodes, timeLimit, startTime )

    if completedPuzzle:
        # puzzle.display()
        results.append( (time.time()-puzzleStartTime, numNodes[0]) )
        numCompleted += 1
    else:
        print("ERROR! could not complete puzzle within time limit.")
        # completedPuzzle.display()

    if numCompleted == 50:
        break
# while

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
