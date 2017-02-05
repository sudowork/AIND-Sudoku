from collections import Counter

from utils import get_solved_boxes, is_solved, assign_values, assign_value
from utils import PEERS, UNITLIST


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
        eliminate_values_from_peers(result, peers, value)
    return result


def eliminate_values_from_peers(values, peers, nums_to_eliminate):
    """Eliminates multiple values from all passed in peers.
    This method mutates values, so it is expected that the caller passes in a
    copy of the original values dictionary.
    Args:
        values: Sudoku in dictionary form.
        peers: Iterable of boxes, preferably a set for performance.
        nums_to_eliminate: String containing values of numbers to eliminate
    Returns:
        Nothing. This method mutates the original values dictionary.
    """
    for num in nums_to_eliminate:
        eliminate_from_peers(values, peers, num)
    return


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


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    new_values = values.copy()
    for unit in UNITLIST:
        unit_twins = get_naked_twins(new_values, unit)
        for value, twins in unit_twins.items():
            peers = set(unit) - twins
            eliminate_values_from_peers(new_values, peers, value)
    return new_values


def get_naked_twins(values, unit):
    """Gets all the naked twins in a unit.
    Args:
        values: Sudoku in dictionary form.

    Returns:
        A dictionary of twin values to the corresponding boxes.
    """
    possible_twins = dict()  # value -> set(box, ...)
    for box in unit:
        value = values[box]
        if len(value) != 2:
            continue
        if value not in possible_twins:
            possible_twins[value] = set()
        possible_twins[value].add(box)
    # filter possible_twins to only those where we have exactly two boxes
    return {
        value: boxes
        for value, boxes in possible_twins.items() if len(boxes) == 2
    }
