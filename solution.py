from collections import Counter
from functools import reduce

from utils import *

assignments = []


def assign_values(values, boxes_and_values):
    for box, value in boxes_and_values:
        assign_value(values, box, value)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
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
    # Eliminate the naked twins as possibilities for their peers


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    result = values.copy()  # don't mutate the original values dict
    solved_boxes = get_solved_boxes(values)
    for box in solved_boxes:
        peers = PEERS[box]
        value = values[box]
        eliminate_from_peers(result, peers, value)
    return result


def get_solved_boxes(values):
    """Returns all solved boxes.
    Args:
        values: Sudoku in dictionary form.
    Returns:
        List of all boxes that are solved.
    """
    return [
        box
        for box, value in values.items()
        if is_solved(value)
    ]


def is_solved(value):
    """Returns if a value is solved (single value).
    Args:
        value: Value string.
    Returns:
        True if is solved, False otherwise.
    """
    return len(value) == 1


def eliminate_from_peers(values, peers, num_to_eliminate):
    """Eliminates a value from all passed in peers.
    This method mutates values, so it is expected that the caller passes in a
    copy of the original values dictionary.
    Args:
        values: Sudoku in dictionary form.
        peers: Iterable of boxes, preferably a set for performance.
        num_to_eliminate: String value of number to eliminate.
    Returns:
        Nothing. This method mutates the original values dictionary.
    """
    for box in peers:
        old_value = values[box]
        if not is_solved(old_value):  # Safer and avoid unnecessary replace
            new_value = old_value.replace(num_to_eliminate, '')
            assign_value(values, box, new_value)
    return


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after filling in only choices.
    """
    new_values = values.copy()  # note: do not modify original values
    for unit in UNITLIST:
        # Use new_values iteratively, so may non-deterministic, but should
        # result in faster convergence.
        only_choices = get_only_choices_for_unit(new_values, unit)
        assign_values(new_values, only_choices)
    return new_values


def get_only_choices_for_unit(values, unit):
    """Returns a list of (box, value) tuples that are valid only choices for a unit.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        List of (box, value) tuples that are only choices.
    """
    possibility_counts = Counter()
    # Maintain an index of value -> box
    # Since we only care about only choices, allow the box to be overwritten
    # Only choices will inherently not be overwritten.
    value_to_box = dict()
    # Count appearances of values and create index of value -> last box
    for box in unit:
        box_values = list(values[box])
        possibility_counts.update(box_values)
        for value in box_values:
            existing_values = value_to_box[value] = box
    return [
        (value_to_box[value], value)
        for value, count in possibility_counts.items()
        if count == 1
    ]


def reduce_puzzle(values):
    """Iteratively reduces the puzzle using the local constraints defined.
    Args:
        values: Sudoku in dictionary form.
    Returns:
        Fully reduced Sudoku puzzle (it may not be a valid solution yet).
    """
    constraints = [eliminate, only_choice]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = get_solved_boxes(values)

        # Reduce puzzle by all constraints
        values = apply_constraints(constraints, values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = get_solved_boxes(values)
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if any([len(value) == 0 for value in values.values()]):
            return False
    return values


def apply_constraints(constraints, values):
    """Applies the constraints in order to the initial Sudoku puzzle, returning
    the reduced puzzle.
    Args:
        constraints: A list of constraint functions with signature values -> values.
        values: Initial Sudoku in dictionary form.
    Returns:
        Reduced puzzle from applying each constraints once.
    """
    return reduce(
        lambda new_values, constraint: constraint(new_values),
        constraints,
        values
    )


def search(values):
    pass


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
