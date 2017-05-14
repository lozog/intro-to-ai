# usage: python main.py <inputfile>

import sys

# parse command line arguments
inputFile = "easy.txt"
if len(sys.argv) > 1:
    inputFile = sys.argv[1] + ".txt"

# read input from file to list
puzzle = []
sudokuInput = open(inputFile)
for line in sudokuInput:
    puzzle.append(line.rstrip().split(','))

for row in puzzle:
    print row
