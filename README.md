# opencv-sudoku
Experimenting sudoku solver with OpenCV


## Dancing Links (DLX)

- also known as algorithm x
- is an exact cover problem
- attempts to find the all the rows of 1s, when merged, will have the full columns on 1s
- only works with 0s and 1s
- uses the toroidal data structure, which is basically a circular linked list that are linked from left to right, top to bottom.

## Sudoku Solver

- uses the dancing links algorithm
- the fastest sudoku solver (?) - definitely faster than brute force attempt
- requires some modification - DLX only works on 1s and 0s, sudoku has numbers ranging from 1-9
- the sudoku constraints are converted into binary 1s and 0s to be used with DLX
- how to convert the numbers in sudoku to binary? Say we have number 9 at the uppermost top-left position (indicated by matrix `(i, j) = (0 ,0)`). Assuming that we can only have one unique number per row, then we have 81 possibilities. So we create an array of 81 zeros, and mark the position of the current number. For the number 9 in row 0 and column 0, the equivalent position is calculated by `row * 9 + val - 1` (minus 1, since the index starts from 0, but sudoku number starts from 1), which is index 8.
- there are four possible constraints - unique column, unique row, unique region, unique number in cell, which gives a total of `4 x 81`. This will be the size of the constraint matrix.
