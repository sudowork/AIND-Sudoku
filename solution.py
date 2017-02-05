from functools import reduce

from constraints import eliminate, only_choice, naked_twins
from utils import *


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)


def search(values):
    """
    Using depth-first search and propagation, create a search tree and solve.
    NOTE: This assumes that we only want A single solution, not ALL solutions.
    Args:
        values: Sudoku in dictionary form.
    Returns:
        A solution if one exists; otherwise, False
    """
    # First, reduce the puzzle using the previous function
    reduced_values = reduce_puzzle(values)

    # Base case when puzzle is unsolvable
    if reduced_values is False:
        return False

    # Choose one of the unfilled squares with the fewest possibilities
    min_choice = get_box_with_fewest_possibilities(reduced_values)

    # Base case when puzzle is already solved
    if min_choice is None:
        return reduced_values

    min_box, possible_values = min_choice

    # Now use recursion to solve each one of the resulting sudokus
    # If one returns a value (not False), return that answer!
    for possible_value in list(possible_values):
        subtree_values = reduced_values.copy()
        subtree_values[min_box] = possible_value
        subtree_solution = search(subtree_values)
        if subtree_solution is not False:
            return subtree_solution

    # Unsolvable puzzle
    return False


def reduce_puzzle(values):
    """Iteratively reduces the puzzle using the local constraints defined.
    Args:
        values: Sudoku in dictionary form.
    Returns:
        Fully reduced Sudoku puzzle (it may not be a valid solution yet).
    """
    constraints = [eliminate, only_choice, naked_twins]
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


def get_box_with_fewest_possibilities(values):
    """Returns a (box, value) tuple of a box with the least possible solutions.
    Args:
        values: Sudoku in dictionary form.
    Returns:
        (box, value) tuple for one of the boxes of minmum possible solutions.
    """
    unsolved_values = [
        (box, value)
        for box, value in values.items() if len(value) > 1
    ]
    if len(unsolved_values) == 0:
        return None
    sorted_values = sorted(unsolved_values, key=lambda x: len(x[1]))
    return sorted_values[0]


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
