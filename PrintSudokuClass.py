class PrintSudoku:

    ############################################################################
    ## Initialisation ##########################################################
    ############################################################################

    def __init__(self, sudoku, constraints = 0):
        # sudoku attribute is array of values
        # constraints attribute is array of constraints of sudoku, 0 = standard sudoku (no extra constraints)
        self.sudoku = sudoku
        self.constraints = constraints

    def printSudoku(self, elaborate = 1):
        # creates graphical representation of sudoku
        # elaborate is bool for printing constraints, 1 = yes, 0 = no

        pass
