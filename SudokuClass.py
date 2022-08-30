class Sudoku:

    ###############################################################################
    ## Initialisation #############################################################
    ###############################################################################

    def __init__(self, inputs):
        # initialise sudoku attributes
        self.box = [set() for _ in range(9)]
        self.row = [set() for _ in range(9)]
        self.col = [set() for _ in range(9)]
        self.sudoku_cells = np.zeros([9,9])
        self.first_unknown = [0,0]

        # initialise sudoku with input (nested list of values)
        # inputs = self.readIn()
        for row, row_values in enumerate(inputs):
            for col, value in enumerate(row_values):
                if value != 0:
                    check = self.addValue(value, [row,col], 'normal', 1, 1)
                    if check == False:
                        print('Invalid Sudoku')
                        return False
        self.given_cells = np.copy(self.sudoku_cells)


    def readIn(self):
    # ask for prompts one row at a time
    # empty cells given by 0
        sudoku_info = list(list())
        valid_digits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
        for i in range(9):
            invalid_input = True
            while invalid_input:
                row_input = input('Type in the digits in row {}. Only use digits and input empty cells as 0.\n'.format(i))
                row_values = [x for x in row_input]
                if len(row_values) != 9:
                    print('Need 9 digits')
                elif not set(row_values).issubset(valid_digits):
                    print('Use only digits 0-9')
                else:
                    invalid_input = False
                    row = [int(x) for x in row_values]
                    sudoku_info.append(row)
        return sudoku_info

    ###############################################################################
    ## Views ######################################################################
    ###############################################################################

    def peekAtCurrentSudoku(self):
        # eventually turn this graphical
        return self.sudoku_cells

    def peekAtOriginalSudoku(self):
        # eventually turn this graphical
        return self.given_cells

    ###############################################################################
    ## Values #####################################################################
    ###############################################################################

    def validValue(self, value):
        valid_values = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
        val_str = str(value)
        if (len(val_str) != 1) or (val_str not in valid_values):
            return False
        else:
            return True

    def addValue(self, value, cell, state, printing=0, validation=0):
        # adds value to cell
        # returns True if adding can be done according to Sudoku rules, otherwise False
        # state: 'normal' for sudoku_cells, 'solving' for solution
        # printing: 0 specifies not printing error messages, 1 specifies printing messages
        # validation: whether to check validity of input, 0 do not check, 1 do check. (not checking sudoku rules)
        if validation == 1:
            if not self.validValue(value):
                if printing == 1:
                    print('{} is not a valid digit from 0-9 (0 represents a blank cell)'.format(value))
                return False
            elif not self.validCell(cell):
                if printing == 1:
                    print('Invalid cell specified')
                return False
            elif value == 0:
                if printing == 1:
                    print('Do not add blank cells')
                return False
        if state == 'normal':
            if self.sudoku_cells[cell[0],cell[1]] != 0:
                if printing == 1:
                    print('Cell already has a value')
                return False
            else:
                row, col, box = self.computeInfo(cell)
                if value in self.row[row]:
                    if printing == 1:
                        print('Clash in row')
                    return False
                elif value in self.col[col]:
                    if printing == 1:
                        print('Clash in column')
                    return False
                elif value in self.box[box]:
                    if printing == 1:
                        print('Clash in box')
                    return False
                else:
                    self.sudoku_cells[cell[0],cell[1]] = value
                    self.row[row].add(value)
                    self.col[col].add(value)
                    self.box[box].add(value)
                    if self.first_unknown != 'solved':
                        if cell == self.first_unknown:
                            next_cell = self.nextCell(cell)
                            while not self.isCellBlank(next_cell, 1):
                                next_cell = self.nextCell(next_cell)
                                if next_cell == False:
                                    print('You have solved the sudoku')
                                    self.first_unknown = 'solved'
                                    return True
                            self.first_unknown = next_cell
                    return True
        elif state == 'solving':
            if self.solution[cell[0],cell[1]] != 0:
                if printing == 1:
                    print('Cell already has a value')
                return False
            else:
                row, col, box = self.computeInfo(cell)
                if value in self.srow[row]:
                    if printing == 1:
                        print('Clash in row')
                    return False
                elif value in self.scol[col]:
                    if printing == 1:
                        print('Clash in column')
                    return False
                elif value in self.sbox[box]:
                    if printing == 1:
                        print('Clash in box')
                    return False
                else:
                    self.solution[cell[0],cell[1]] = value
                    self.srow[row].add(value)
                    self.scol[col].add(value)
                    self.sbox[box].add(value)
                    return True

    # want to think about deleting solution when you add values (instead maybe compare to solution)

    def removeValue(self, cell, state, printing=0, validation=0):
        # removes value from cell
        # returns True if removal was successful, otherwise False
        # state: 'normal' for sudoku_cells, 'solving' for solution
        # printing: 0 specifies not printing error messages, 1 specifies printing messages
        # validation: whether to check validity of input, 0 do not check, 1 do check. (not checking sudoku rules)
        if validation == 1:
            if not self.validCell(cell):
                if printing == 1:
                    print('Invalid cell specified')
                return False

        if state == 'normal':
            if self.sudoku_cells[cell[0],cell[1]] == 0:
                if printing == 1:
                    print('Cell already has no value')
                return False
            else:
                row, col, box = self.computeInfo(cell)
                value = self.sudoku_cells[cell[0],cell[1]]
                self.sudoku_cells[cell[0],cell[1]] = 0
                self.row[row].remove(value)
                self.col[col].remove(value)
                self.box[box].remove(value)
                return True
        elif state == 'solving':
            if self.solution[cell[0],cell[1]] == 0:
                if printing == 1:
                    print('Cell already has no value')
                return False
            else:
                row, col, box = self.computeInfo(cell)
                value = self.solution[cell[0], cell[1]]
                self.solution[cell[0], cell[1]] = 0
                self.srow[row].remove(value)
                self.scol[col].remove(value)
                self.sbox[box].remove(value)
                return True

    def replaceValue(self, value, cell, printing=0, validation=0):
        if self.removeValue(cell, 'normal', printing, validation):
            check = self.addValue(value, cell, 'normal', printing, validation)
            return check
        else:
            return False

    ###############################################################################
    ## Cells ######################################################################
    ###############################################################################

    def computeInfo(self, cell):
        # returns (row, col, box) info of cell
        row = cell[0]
        col = cell[1]
        box = 3*(row//3) + (col//3)
        return (row, col, box)

    def validCell(self, cell):
        valid_dims = {'0', '1', '2', '3', '4', '5', '6', '7', '8'}
        if len(cell) != 2:
            invalid = True
        else:
            row = str(cell[0])
            col = str(cell[1])
            if (len(row) != 1) or (len(col) !=1):
                invalid = True
            elif row not in valid_dims:
                invalid = True
            elif col not in valid_dims:
                invalid = True
            else:
                invalid = False

        if invalid:
            return False
        else:
            return True

    def nextCell(self, cell):
        row = int(cell[0])
        col = int(cell[1])
        if col != 8:
            return [row, col+1]
        elif row != 8:
            return [row+1, 0]
        else:
            return False

    def cellValue(self, cell, validation=0):
        # returns cell value
        # validation: 0 no checking if cell is valid, 1 will check
        if validation == 1:
            if not self.validCell(cell):
                print('Invalid Cell')
                return 'False'
        cell_value = int(self.sudoku_cells[cell[0],cell[1]])
        return cell_value

    def isCellBlank(self, cell, validation=0):
        # checks if cell is blank
        # returns True if blank cell, False otherwise
        # validation: 0 no checking if cell is valid, 1 will check
        check = self.cellValue(cell, validation)
        if check == 'False':
            return False
        else:
            return check == 0
    def nextBlankCell(self, cell):
        next_cell = self.nextCell(cell)
        while not self.isCellBlank(next_cell, 0):
            next_cell = self.nextCell(next_cell)
            if next_cell == False:
                return False
        return next_cell

    ###############################################################################
    ## Solve ######################################################################
    ###############################################################################


#     def iterativeSolve(self):
#         temp = copy(self.sudoku_cells)
#         values = [1,2,3,4,5,6,7,8,9]
#         dfs_stack = [(self.first_unknown, False)]
#         while dfs_stack:
#             cell, visited = dfs_stack.pop()
#             if cell:
#                 if visited:

#         pass
#         #return self.solution

    def recursiveSolve(self):
        # Note: want to think about printing solution, if solution already calculated
        self.solution = np.copy(self.sudoku_cells)
        self.srow=copy.deepcopy(self.row)
        self.scol=copy.deepcopy(self.col)
        self.sbox=copy.deepcopy(self.box)
        path = []
        def helper(cell, path):
            values = [1,2,3,4,5,6,7,8,9]
            for guess in values:
                if self.addValue(guess, cell, 'solving', 0, 0):
                    path.append((guess, cell))
                    #input('Guess worked: {}'.format(path))
                    next_cell = self.nextBlankCell(cell)
                    if next_cell == False:
                        return True
                    if helper(next_cell, path):
                        return True
                    else:
                        path.pop()
                        self.removeValue(cell, 'solving', 0, 0)

            return False

        solvable = helper(self.first_unknown, path)
        if solvable == True:
            return self.solution
        else:
            del self.solution
            del self.srow
            del self.scol
            del self.sbox
            return False

    def isSolvable(self):
        # check if sudoku as presented is solvable
        return self.recursiveSolve() is not False

    ###############################################################################
    ## Other ######################################################################
    ###############################################################################

    def presentGraphically(self, state):
        # graphically present sudoku state
        pass

    def checkUniqueness(self):
        # check if there is unique solution
        pass
