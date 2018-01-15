
from utils import *
import utils

from collections import defaultdict

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
                ['A9',  'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
unitlist = row_units + column_units + diagonal_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """

    all_pairs = []

    for key, val in values.items():
        if(len(val) == 2):
            all_pairs.append(key)

    row_twins = defaultdict(list)
    col_twins = defaultdict(list)
    square_unit_twins = defaultdict(list)

    for i in range(len(all_pairs)):
        unit = all_pairs[i]
        for j in range(i+1, len(all_pairs)):
            other_unit = all_pairs[j]

            unit_value = values[unit]
            other_unit_value = values[other_unit]

            if(unit_value == other_unit_value):

                if(same_row(unit, other_unit)):
                    row_number = get_index_number(unit, row_units)
                    row_twins[row_number].append([unit, other_unit])

                elif(same_col(unit, other_unit)):
                    col_number = get_index_number(unit, column_units)
                    col_twins[col_number].append([unit, other_unit])

                if(same_square_unit(unit, other_unit)):
                    square_unit_number = get_index_number(unit, square_units)
                    square_unit_twins[square_unit_number].append([unit, other_unit])

    removeTwinValues(row_twins, row_units, values)
    removeTwinValues(col_twins, column_units, values)
    removeTwinValues(square_unit_twins, square_units, values)

    return values

def removeTwinValues(unit_twin_map, unit_arr, values):

    for index, twin_sets in unit_twin_map.items():

        for twin_set in twin_sets:
            twin1 = twin_set[0]
            twin2 = twin_set[1]

            twin_value = values[twin1]
            for unit in unit_arr[index]:
                if((unit != twin1) and (unit != twin2)):
                    unit_value = values[unit]
                    unit_value = unit_value.replace(twin_value[0], "")
                    unit_value = unit_value.replace(twin_value[1], "")
                    values[unit] = unit_value


def same_row(unit, other_unit):
    unit_index_number = get_index_number(unit, row_units)
    other_unit_index_number = get_index_number(other_unit, row_units)
    
    if(unit_index_number == -1 or other_unit_index_number == -1):
        return False

    return unit_index_number == other_unit_index_number

def same_col(unit, other_unit):
    unit_index_number = get_index_number(unit,column_units)
    other_unit_index_number = get_index_number(other_unit,column_units)

    if(unit_index_number == -1 or other_unit_index_number == -1):
        return False

    return unit_index_number == other_unit_index_number 

def same_square_unit(unit, other_unit):
    unit_index_number = get_index_number(unit,square_units)
    other_unit_index_number = get_index_number(other_unit,square_units)

    if(unit_index_number == -1 or other_unit_index_number == -1):
        return False;

    return unit_index_number == other_unit_index_number 

def get_index_number(unit, unit_arr):

    for index in range(len(unit_arr)):
        list_of_units = unit_arr[index]
        if unit in list_of_units:
            return index

    return -1

def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    for key, value in peers.items():
        boxPeers = value
        boxValue = values.get(key)
        if(len(boxValue) == 1):
            for peer in boxPeers:
                peerValue = values.get(peer)
                if(len(peerValue) > 1):
                    listOfPossibleValues = peerValue.replace(boxValue,"")
                    values[peer] = listOfPossibleValues
    
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    for unit in unitlist:

        for val in '123456789':
            boxesContainingVal = [box for box in unit if val in values.get(box)]
            if(len(boxesContainingVal) == 1):
                values[boxesContainingVal[0]] = val


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        eliminate(values)
        only_choice(values)
        naked_twins(values)
        # Check how many boxes have a determined value, to compare

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values



def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    reduce_puzzle_result = reduce_puzzle(values)

    if(reduce_puzzle_result == False):
        return False
    elif(is_puzzle_solved(values)):
        return reduce_puzzle_result

    boxWithMinPossibleSolutions = findMinUnSolvedBox(values)
    boardVersions = getDiffBoardVersions(values, boxWithMinPossibleSolutions)
    for board in boardVersions:
        search_result = search(board)

        if(search_result != False):
            return search_result

    return False

def is_puzzle_solved(values):

    for box, val in values.items():

        if((len(val) == 1) and (int(val) >= 1 and int(val) <= 9)):
            for peer in peers[box]:
                peer_value = values[peer]
                if(val in peer_value):
                    return False
        else:
            return False

    return True                 

def findMinUnSolvedBox(values):

    minNumPossibleSolutions = 10
    minBox = ""

    for box, val in values.items():
        if(len(val) > 1 and len(val) < minNumPossibleSolutions):
            minNumPossibleSolutions = len(val)
            minBox = box

    return minBox

def getDiffBoardVersions(values, boxWithPossibleSolutions):

    if(len(boxWithPossibleSolutions) == 0):
        return []

    boardVersions = []
    for val in values.get(boxWithPossibleSolutions):
        newBoard = values.copy()
        newBoard[boxWithPossibleSolutions] = val
        boardVersions.append(newBoard)

    return boardVersions

def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values

if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
