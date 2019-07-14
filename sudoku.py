
Metadata = namedtuple('Metadata', 'row col val')

class Sudoku:
    @staticmethod
    def constraint_index(row, col, val):
        '''
        Returns the index of the unique constraint in a 9x9 row.
        For all four constraints below, we will construct a 4x9x9
        row and mark the index.
        '''
        r = row // 3 * 3 # Gives the current grid row.
        c = col // 3     # Gives the current grid col.
        grid = r + c     # The grid number from top to bottom, left to right.
        # Grid:
        # 012
        # 345
        # 678
        return (row * 9 + col,         # Each cell can only have one number.
                row * 9 + val - 1,     # For each row, a number can only appear once.
                col * 9 + val - 1,     # For each column, a number can only appear once.
                grid * 9 + val - 1)    # For each region, a number can only appear once.

    @staticmethod
    def parse(sudoku):
        '''
        Build the constraint matrix for all the existing values in the sudoku board,
        as well as the ones that we have not seen yet. Dancing links will try
        to find all the possible combinations.
        '''

        # The actual size of the result is 9 * 9 * 9 for every combination of numbers in each row, col and grid.
        # If we have a partial solution (filled numbers in the sudoku), we can eliminate most of them.
        result, metadata = [], []
        for row in range(0, 9):
            for col in range(0, 9):
                val = sudoku[row, col]
                if val == 0:
                    # The cell is empty. We need to fill it with all the values that are not inside yet.
                    # To do so, find the values that are not in the current row yet.
                    # ! Numbers must be in range 1-9, not index 0.
                    values = [i for i in range(1, 10) 
                              if i not in sudoku[row]]
                else:
                    values = [val]
                for val in values:
                    cell_c, row_c, col_c, grid_c = Sudoku.constraint_index(row, col, val)
                    mat = np.zeros(4*9*9) # Each constraints have 81 indices.
                    mat[cell_c + 0 * 81] = 1
                    mat[row_c + 1 * 81] = 1
                    mat[col_c + 2 * 81] = 1
                    mat[grid_c + 3 * 81] = 1
                    result.append(mat)
                    metadata.append(Metadata(row=row, col=col, val=val))
        return np.array(result), metadata
