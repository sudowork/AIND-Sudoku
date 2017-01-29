# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)

Q: How do we use constraint propagation to solve the naked twins problem?

A: The naked twins problem is similar to the only choice problem.
However, instead of looking for a single choice, we are looking for a pair of twins within a unit.
The algorithm can briefly be described as:

1. For each unit:
    1. Find pairs of naked twins (boxes with the same two possible values).
    1. For all peers in the unit, eliminate the two twin values.

# Question 2 (Diagonal Sudoku)

Q: How do we use constraint propagation to solve the diagonal sudoku problem?

A: In addition to having units for rows, columns, and squares, have units for diagonals.
In this case, the diagonals would be:
```
[A1, B2, C3, D4, E5, F6, G7, H8, I9]
[A9, B8, C7, D6, E5, F4, G3, H2, I1]
```
By adding these units, our constraint propagation code should automatically apply:

- Elimination: Elimination looks at peers when eliminating. Because peers are calculated from the units, diagonals are taken care of.
- Only Choice: Only choice looks at choices within a unit, so diagonals are taken care of.
- Naked Twins: Also only looks at twins within a unit, so diagonals are taken care of.
- Search: Search is orthoganol to the constraint propagation.
As long as all constraints are maintained, search only needs to check if the board is solved or not; otherwise, it will descend down the solution tree.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
