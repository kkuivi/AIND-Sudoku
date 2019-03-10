# Solve Sudoku with AI

## Synopsis

In this project, I extended an existing Sudoku-solving agent to solve _diagonal_ Sudoku puzzles. A diagonal Sudoku puzzle is identical to traditional Sudoku puzzles with the added constraint that the boxes on the two main diagonals of the board must also contain the digits 1-9 in each cell (just like the rows, columns, and 3x3 blocks).

## Functions Implemented
The functions I implemented are in `solution.py`. The functions are:
* `eliminate()`
* `only_choice()`
* `reduce_puzzle()`
* `search()`
