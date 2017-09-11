rows = 'ABCDEFGHI'
columns = '123456789'

assignments = []

count = 0

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    # Find all instances of naked twins
    digits = '123456789'
    do = [dict((d, [b for b in u if d in values[b]]) for d in digits) for u in unitlist]
    nts_dicts = [dict((d, u[d]) for d in u if len(u[d]) == 2) for u in do]
    
    # Eliminate the naked twins as possibilities for their peers
    for i in range(len(nts_dicts)):
        unit = unitlist[i]
        nts_dict = nts_dicts[i]
        for digit in nts_dict:
            digit_boxes = nts_dict[digit]
            units_list = [u for u in unitlist if digit_boxes[0] in u and digit_boxes[1] in u]
            if (len(units_list) == 2):
                for un in units_list:
                    if un != unit:
                        for box in un:
                            values[box] = values[box].replace(digit, '')
                            #assign_value(values, box, values[box].replace(digit, ''))
                
                
    return values
    
def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, columns)

row_units = [cross(r, columns) for r in rows]
column_units = [cross(rows, c) for c in columns]
squre_units = [cross(rs, cs) for rs in ['ABC', 'DEF', 'GHI'] for cs in ['123', '456', '789']]
#diagonal_units = [[rows[i]+columns[i] for i in range(9)],[rows[i]+columns[8-i] for i in range(9)]]
unitlist = row_units + column_units + squre_units 
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = {}
for s in boxes:
    set_peers = set(sum(units[s], []))
    set_peers.discard(s)
    peers[s] = set_peers
    
def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in columns))
        if r in 'CF': print(line)
    return

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_boxes = [box for box in values if len(values[box]) == 1]
    for box in solved_boxes:
        value = values[box]
        for peer in peers[box]:
            if value in values[peer]:
                assign_value(values, peer, values[peer].replace(value, ''))
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # TODO: Implement only choice strategy here
    
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    stalled = False
    attempt = 0
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        eliminate(values)

        # Your code here: Use the Only Choice Strategy
        only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    global count
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        count += 1
        if attempt:
            return attempt
                        
    
def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = search(grid_values(grid))
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    
 
# Trivial
trivial1 = '.4....179..2..8.54..6..5..8.8..7.91..5..9..3..19.6..4.3..4..7..57.1..2..928....6.'

# Easy
easy1 = '..2...5...1.7.5.2.4...9...7.49...73.8.1.3.4.9.36...21.2...8...4.8.9.2.6...7...8..'
easy2 = '.5..1..4.1.7...6.2...9.5...2.8.3.5.1.4..7..2.9.1.8.4.6...4.1...3.4...7.9.2..6..1.'
easy3 = '...6.2...4...5...1.85.1.62..382.671...........194.735..26.4.53.9...2...7...8.9...'

# Medium
medium1 = '..........79.5.18.8.......7..73.68..45.7.8.96..35.27..7.......5.16.3.42..........'
medium2 = '.......85...21...996..8.1..5..8...16.........89...6..7..9.7..523...54...48.......'
medium3 = '7....4..1.2..6..8...15..2..8...9.7...5.3.7.2...6.5...8..8..91...9..1..6.5..8....3'

# Hard
hard1 = '.....3.17.15..9..8.6.......1....7.....9...2.....5....4.......2.5..6..34.34.2.....'
hard2 = '38..........4..785..9.2.3...6..9....8..3.2..9....4..7...1.7.5..495..6..........92'
hard3 = '...7..8....6....31.4...2....24.7.....1..3..8.....6.29....8...7.86....5....2..6...'

extrem = '1.....7..7.9..36..6...28......4...9..1..8..4..5...6......24...9..78..5.2..1.....3'

a = '1................................................................................'

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(extrem))
    print(count)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
