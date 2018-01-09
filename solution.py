
from utils import *
import utils

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
unitlist[0] = unitlist[0] + ['D4', 'E5', 'F6', 'G7', 'H8', 'I9']
unitlist[2] = unitlist[2] + ['D6', 'E5', 'F4', 'G3', 'H2', 'I1']
unitlist[4] = unitlist[4] + ['A1', 'B2', 'C3', 'G7', 'H8', 'I9', 'A9', 'B8', 'C7', 'G3', 'H2', 'I1']
unitlist[6] = unitlist[6] + ['F4', 'E5', 'D6', 'C7', 'B8', 'A9']
unitlist[8] = unitlist[8] + ['F6', 'E5', 'D4', 'C3', 'B2', 'A1']

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
    rowTwins = {}
    colTwins = {}
    squareUnitTwins = {}

    generateTwinMaps(rowTwins, colTwins, squareUnitTwins, values)

    removeValuesWithNoTwins(rowTwins)
    removeValuesWithNoTwins(colTwins)
    removeValuesWithNoTwins(squareUnitTwins)

    removeNakedTwins(rowTwins, row_units, values)
    removeNakedTwins(colTwins, column_units, values)
    removeNakedTwins(squareUnitTwins, square_units, values)

def printDict(twinDict):
    for x in twinDict:
        print (x)
        for y in twinDict[x]:
            print (y,':',twinDict[x][y])

def generateTwinMaps(rowTwins, colTwins, squareUnitTwins, values):
    for unit, neighbors in peers.items():
        unitValues = values.get(unit)

        if(len(unitValues) == 2):
            for neighbor in neighbors:
                neighborValue = values.get(neighbor)
                if(unitValues == neighborValue):
                    
                    unitRowArrIndex = getUnitRowNumber(unit)
                    neighborRowArrIndex = getUnitRowNumber(neighbor)
                    if(unitRowArrIndex == neighborRowArrIndex):
                        putTwinsInArr(unit, neighbor, unitValues, unitRowArrIndex, rowTwins)

                    unitColArrIndex = getUnitColNumber(unit)
                    neighborColArrIndex = getUnitColNumber(unit)
                    if(unitColArrIndex == neighborColArrIndex):
                        putTwinsInArr(unit, neighbor, unitValues, unitColArrIndex, colTwins)

                    unitSquareArrIndex = getSquareUnitNumber(unit)
                    neighborSquareArrIndex = getSquareUnitNumber(unit)
                    if(unitSquareArrIndex == neighborSquareArrIndex):
                        putTwinsInArr(unit, neighbor, unitValues, unitSquareArrIndex, squareUnitTwins)

def removeNakedTwins(twinArr, unitArr, values):
    for arrNumber, twinValuesMap in twinArr.items():

        for twinValue, twinSet in twinValuesMap.items():
            val1 = twinValue[0]
            val2 = twinValue[1]

            index1 = list(twinSet)[0]
            index2 = list(twinSet)[1]

            for unit in unitArr[arrNumber]:
                if(len(twinValue) == 2 and unit != index1 and unit != index2):
                    unitValue = values.get(unit)
                    unitValue = unitValue.replace(val1, "")
                    unitValue = unitValue.replace(val2, "")
                    values[unit] = unitValue    


def putTwinsInArr(unit, neighbor, value, arrIndex, twinsArr):

    if arrIndex not in twinsArr:
        twinsArr[arrIndex] = {}
        
    twinValuesMap = twinsArr[arrIndex]
    twinValuesSet = twinValuesMap.get(value)

    if not twinValuesSet:
        twins = set()
        twins.add(unit)
        twins.add(neighbor)
        twinValuesMap[value] = twins
    else:
        twinValuesSet.add(unit)
        twinValuesSet.add(neighbor)

def removeValuesWithNoTwins(twinArr):

    remove = []
    for key, valueMap in twinArr.items():
     if (len(valueMap) != 2):
        remove.append(key)
    
    printDict(twinArr)

    for key in remove:
        del twinArr[key]

def getSquareUnitNumber(unit):

    row = unit[0]
    col = int(unit[1])

    if(row >= 'A' and row <= 'C'):
        if(col >= 1 and col <= 3):
            return 1
        elif(col >= 4 and col <= 6):
            return 2
        elif(col >= 7 and col <= 9):
            return 3

    elif(row >= 'D' and row <= 'F'):
        if(col >= 1 and col <= 3):
            return 4
        elif(col >= 4 and col <= 6):
            return 5
        elif(col >= 7 and col <= 9):
            return 6

    elif(row >= 'G' and row <= 'I'):
        if(col >= 1 and col <= 3):
            return 7
        elif(col >= 4 and col <= 6):
            return 8
        elif(col >= 7 and col <= 9):
            return 9

def getUnitRowNumber(unit):
    rowLetter = unit[0]
    index = ord(rowLetter) - 65
    return index

def getUnitColNumber(unit):
    colNumber = unit[1]
    index = int(colNumber)
    return index-1

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

    num_solved_boxes = len([box for box, val in values.items() if(len(val) == 1)])
    if(reduce_puzzle_result == False):
        return False
    elif(num_solved_boxes == len(values)):
        return reduce_puzzle_result

    boxWithMinPossibleSolutions = findMinUnSolvedBox(values)
    boardVersions = getDiffBoardVersions(values, boxWithMinPossibleSolutions)

    for board in boardVersions:
        search_result = search(board)

        if(search_result != False):
            return search_result

    return False

def findMinUnSolvedBox(values):

    minNumPossibleSolutions = 10
    minBox = ""

    for box, val in values.items():

        if(len(val) > 1 and len(val) < minNumPossibleSolutions):
            minNumPossibleSolutions = len(val)
            minBox = box

    return minBox

def getDiffBoardVersions(values, boxWithPossibleSolutions):

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
