class SudokuSolver {
  static SIZE = 9

  static gridConstraint(row, col, n) {
    // Each grid can only have the number 1-9 appearing once.
    const r = Math.floor(row / 3)
    const c = Math.floor(col / 3)
    return (r * 3 + c) * 9 + n - 1
  }

  static rowConstraint(row, n) {
    return row * 9 + n - 1
  }

  static columnConstraint(col, n) {
    return col * 9 + n - 1
  }

  static cellConstraint(row, col) {
    return row * 9 + col
  }

  static buildConstraintMatrix(row, col, n) {
    const constraints = [
      SudokuSolver.gridConstraint(row, col, n),
      SudokuSolver.rowConstraint(row, n),
      SudokuSolver.columnConstraint(col, n),
      SudokuSolver.cellConstraint(row, col)
    ]
    return constraints.map(constraint => {
      const matrix = Array(9 * 9).fill(0)
      matrix[constraint] = 1
      return matrix
    }).reduce((acc, mat) => acc.concat(mat), [])
  }

  static parse(sudoku = []) {
    const matrix = []
    const metadata = []

    for (let row = 0; row < 9; row += 1) {
      for (let col = 0; col < 9; col += 1) {
        const n = sudoku[row][col]
        // The value ranges from 1-9. 0 means that it is unset.
        if (n === 0) {
          for (let n = 1; n < 10; n += 1) {
            // For each number n that is not in the current row, fill them up.
            if (!sudoku[row].includes(n)) {
              const m = SudokuSolver.buildConstraintMatrix(row, col, n)

              matrix.push(m)
              metadata.push({
                row,
                col,
                n
              })
            }
          }
        } else {
          const m = SudokuSolver.buildConstraintMatrix(row, col, n)

          matrix.push(m)
          metadata.push({
            row,
            col,
            n
          })
        }

      }
    }

    return {
      matrix,
      metadata
    }
  }
}

class DataObject {
  constructor(column, row) {
    this.up = this
    this.down = this
    this.left = this
    this.right = this
    this.column = column
    this.row = row
  }
  toString() {
    return `${this.column.name}:${this.row}`
  }
}

class ColumnObject extends DataObject {
  constructor(name = '', size = 0) {
    super(null, null)
    this.column = this
    this.name = name
    this.size = size
  }
}



class DLX {
  static ALPHABETS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split()

  static solve(A) {
    const torodial = DLX.initTorodial(A)
    return DLX.search(torodial)
  }

  static initColumnLabels(A = [
    []
  ]) {
    const cols = (A && A[0].length) || 0
    if (cols < 26) {
      return DLX.ALPHABETS.slice(0, cols)
    }
    return Array(cols).fill(0).map((_, n) => n.toString())
  }

  static initColumnHeader(A) {
    const cols = (A && A[0].length) || 0
    const labels = DLX.initColumnLabels(A)

    // The root header links all the column labels.
    const root = new ColumnObject('root', Infinity)

    let curr = root
    for (let col = 0; col < cols; col += 1) {
      curr.right = new ColumnObject(labels[col])
      curr.right.left = curr
      curr = curr.right
    }

    curr.right = root
    curr.right.left = curr

    return root
  }

  static headerPointer(root) {
    const header = {}
    for (let curr = root.right; curr != root; curr = curr.right) {
      header[curr.name] = curr
    }
    return header
  }
  static smallestColumnObject(root) {
    let smallest = root
    for (let curr = root.column.right; curr != root; curr = curr.right) {
      if (curr.size < smallest.size) {
        smallest = curr
      }
    }
    return smallest
  }

  static initTorodial(A) {
    const labels = DLX.initColumnLabels(A)
    const root = DLX.initColumnHeader(A)
    const header = DLX.headerPointer(root)

    for (let i = 0; i < A.length; i += 1) {
      const row = A[i]

      let prev = null
      let left = null

      for (let j = 0; j < row.length; j += 1) {
        const col = row[j]
        if (col !== 1) continue
        const head = header[labels[j]]
        head.size += 1

        let curr = head.up
        curr.down = new DataObject(head, i)
        curr.down.up = curr

        curr = curr.down
        curr.down = curr.column
        curr.down.up = curr

        if (!prev) {
          prev = curr
          prev.right = curr
          prev.right.left = prev
          left = curr
        } else {
          prev.right = curr
          prev.right.left = prev
          prev = curr
        }
      }
      if (prev) {
        prev.right = left
        prev.right.left = prev
      }
    }
    return root
  }

  static cover(col) {
    col = col.column
    col.right.left = col.left
    col.left.right = col.right

    for (let i = col.down; i != col; i = i.down) {
      for (let j = i.right; j != i; j = j.right) {
        j.up.down = j.down
        j.down.up = j.up
        j.column.size -= 1
      }
    }
  }

  static uncover(col) {
    col = col.column
    for (let i = col.up; i != col; i = i.up) {
      for (let j = i.left; j != i; j = j.left) {
        j.column.size += 1
        j.up.down = j
        j.down.up = j
      }
    }
    col.right.left = col
    col.left.right = col
  }

  static search(root, k = 0, solution = []) {
    if (root.right === root) {
      return [...solution]
    }

    let col = DLX.smallestColumnObject(root)
    DLX.cover(col)


    for (let r = col.down; r != col; r = r.down) {
      let res = r
      solution.push(res.row)

      for (let j = r.right; j != r; j = j.right) {
        DLX.cover(j)
      }

      const result = DLX.search(root, k + 1, solution)
      if (result) return result

      solution.pop()

      r = res
      col = r.column

      for (let j = r.left; j != r; j = j.left) {
        DLX.uncover(j)
      }
    }
    DLX.uncover(col)
  }
}

// assert(DLX.initColumnLabels([[1,2,3]]) === ['a', 'b', 'c']) 


const sudoku = [
  [8, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 3, 6, 0, 0, 0, 0, 0],
  [0, 7, 0, 0, 9, 0, 2, 0, 0],
  [0, 5, 0, 0, 0, 7, 0, 0, 0],
  [0, 0, 0, 0, 4, 5, 7, 0, 0],
  [0, 0, 0, 1, 0, 0, 0, 3, 0],
  [0, 0, 1, 0, 0, 0, 0, 6, 8],
  [0, 0, 8, 5, 0, 0, 0, 1, 0],
  [0, 9, 0, 0, 0, 0, 4, 0, 0]
]

const {
  matrix,
  metadata
} = SudokuSolver.parse(sudoku)


const rows = DLX.solve(matrix)
const solution = Array(9).fill(() => Array(9).fill(0)).map(fn => fn())
for (let r of rows) {
  const {
    row,
    col,
    n
  } = metadata[r]
  solution[row][col] = n
}
console.log(solution)
