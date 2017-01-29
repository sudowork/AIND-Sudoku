def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [
        s + t
        for s in A
        for t in B
    ]


def concat(A, B):
    "One-to-one concatenation of elements in A and elements in B."
    return [
      s + t
      for s, t in zip(A, B)
    ]


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert re.compile(r'^[1-9.]{81}$').match(grid)
    return {
        box: ALL_NUMS if value == '.' else value
        for box, value in zip(BOXES, grid)
    }


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    value_lengths = (len(value) for _, value in values.items())
    max_value_length = max(value_lengths)
    width = max_value_length + 2
    cell_line = '-' * (width * 3)
    full_line = '+'.join([cell_line] * 3)
    for r in ROWS:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in COLS))
        if r in 'CF':
            print(full_line)

ROWS = 'ABCDEFGHI'
COLS = '123456789'
ALL_NUMS = COLS
BOXES = cross(ROWS, COLS)

# Units
ROW_UNITS = [
  cross(row, COLS)
  for row in ROWS
]
COLUMN_UNITS = [
  cross(ROWS, col)
  for col in COLS
]
SQUARE_UNITS = [
  cross(rs, cs)
  for rs in ('ABC', 'DEF', 'GHI')
  for cs in ('123', '456', '789')
]
DIAGONAL_UNITS = [
    concat(ROWS, COLS),            # top left to bottom right
    concat(ROWS, reversed(COLS)),  # top right to bottom left
]
UNITLIST = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS + DIAGONAL_UNITS
