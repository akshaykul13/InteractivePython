"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """        
        print self.get_number(target_row, target_col)
        val = self.get_number(target_row, target_col)
        if val != 0:
            return False
        if target_col != self.get_width()-1:
            for idx in range(target_col+1, self.get_width()):
                if self.get_number(target_row, idx) != idx + self.get_width()*(target_row):
                    return False
        if target_row != self.get_height()-1:
            for row_idx in range(target_row+1, self.get_height()):
                for col_idx in range(0, self.get_width()):
                    if self.get_number(row_idx, col_idx) != col_idx + self.get_width()*(row_idx):
                        return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """        
        print self
        move_string = ""
        zero_row, zero_col = self.current_position(0, 0)
        # position 0 in the target cell
        if zero_row != target_row or zero_col != target_col:
            if zero_col < target_col:
                for idx in range(zero_col, target_col):
                    move_string = move_string + "r"
                    print idx + idx
            elif zero_col > target_col:
                for idx in range(target_col, zero_col):
                    move_string = move_string + "l"
                    
            if zero_row < target_row:
                for idx in range(zero_row, target_row):
                    move_string = move_string + "d"
            
            print "Zero movement : " + move_string
            self.update_puzzle(move_string)
            print self
        
        # find the target value
        move_string1 = ""
        req_row, req_col = self.current_position(target_row, target_col)
        if req_row < target_row:
            for idx in range(req_row, target_row):
                move_string1 = move_string1 + "u"
        if req_col < target_col:
                for idx in range(req_col, target_col):
                    move_string1 = move_string1 + "l"
        elif req_col > target_col:
            for idx in range(target_col, req_col):
                move_string1 = move_string1 + "r"
        print "Found target : " + move_string1
        self.update_puzzle(move_string1)
        print self
        move_string = move_string + move_string1
        
        #move the target value to target position
        move_string2 = ""        
        cur_row, cur_col = self.current_position(target_row, target_col)
        print cur_col, cur_row
        while cur_col != target_col:
            zero_row, zero_col = self.current_position(0, 0)
            if zero_col < cur_col:
                if zero_row != self.get_height()-1:
                    move_string2 = move_string2 + "drrul"
                    self.update_puzzle("drrul")
                else:
                    move_string2 = move_string2 + "urrdl"
                    self.update_puzzle("urrdl")
                print self
            elif zero_col > cur_col:
                move_string2 = move_string2 + "dllur"
                self.update_puzzle("dllur")
                print self
            cur_row, cur_col = self.current_position(target_row, target_col)
        while cur_row != target_row:
            zero_row, zero_col = self.current_position(0, 0)
            if zero_row == cur_row:
                move_string2 = move_string2 + "druld"
                self.update_puzzle("druld")
            else:
                move_string2 = move_string2 + "lddruld"
                self.update_puzzle("lddruld")
            print self
            cur_row, cur_col = self.current_position(target_row, target_col)
        move_string = move_string + move_string2 
        
        zero_row, zero_col = self.current_position(0, 0)        
        if zero_col != cur_col-1:
            move_string = move_string + "l"
            self.update_puzzle("l")
        if zero_row != cur_row:
            move_string = move_string + "d"
            self.update_puzzle("d")
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """        
        # find the target value
        print self
        move_string = ""
        move_string1 = ""
        target_col = 0
        req_row, req_col = self.current_position(target_row, target_col)
        if req_row < target_row:
            for idx in range(req_row, target_row):
                move_string1 = move_string1 + "u"
                print idx
        if req_col > target_col:
            for idx in range(target_col, req_col):
                move_string1 = move_string1 + "r"
        print "Found target : " + move_string1
        self.update_puzzle(move_string1)
        print self
        move_string = move_string + move_string1
                
        #move target value to target position of i-1, 1 and apply 3x2 transformaation
        move_string2 = ""        
        cur_row, cur_col = self.current_position(target_row, target_col)
        zero_row, zero_col = self.current_position(0, 0)
        print zero_col
        #check if aleady in position
        if cur_row == target_row and cur_col == 0:
            for val in range(self.get_width()-1):
                move_string = move_string + "r"
                self.update_puzzle("r")
                print val
                print self
            return move_string
        if zero_row == cur_row:
            while cur_row != target_row-1:
                move_string2 = move_string2 + "dlurd"
                self.update_puzzle("dlurd")
                print self
                cur_row, cur_col = self.current_position(target_row, target_col)
            if cur_col == 0:
                move_string2 = move_string2 + "l"
                self.update_puzzle("l")
                print "Row set"
                print self
            else:
                move_string2 = move_string2 + "ulld"
                self.update_puzzle("ulld")
                print "Row set"
                print self
            cur_row, cur_col = self.current_position(target_row, target_col)                
            while cur_col != 1:
                move_string2 = move_string2 + "rulld"
                self.update_puzzle("rulld")
                print self            
                cur_row, cur_col = self.current_position(target_row, target_col)
        else:
            while cur_row != target_row-1:
                move_string2 = move_string2 + "rddlu"
                self.update_puzzle("rddlu")
                print self
                cur_row, cur_col = self.current_position(target_row, target_col)
            move_string2 = move_string2 + "rdl"
            self.update_puzzle("rdl")
            print self
            cur_row, cur_col = self.current_position(target_row, target_col)
        print "Final 3x2 puzzle"
        move_string2 = move_string2 + "ruldrdlurdluurddlur"
        self.update_puzzle("ruldrdlurdluurddlur")
        print self
        move_string = move_string + move_string2
        
        zero_row, zero_col = self.current_position(0, 0)
        if zero_col != self.get_width()-1:
            print "Here"
            for val in range(zero_col, self.get_width()-1):
                move_string = move_string + "r"
                self.update_puzzle("r")
                print val
                print self
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        val = self.get_number(0, target_col)
        if val != 0:
            return False
        if target_col != self.get_width()-1:
            for idx in range(target_col+1, self.get_width()):
                if self.get_number(0, idx) != idx + self.get_width()*(0):
                    return False
                if self.get_number(1, idx) != idx + self.get_width()*(1):
                    return False
        if self.get_number(1, target_col) != target_col + self.get_width()*(1):
            return False
        
        for row_idx in range(2, self.get_height()):
            for col_idx in range(0, self.get_width()):
                if self.get_number(row_idx, col_idx) != col_idx + self.get_width()*(row_idx):
                    return False
        return True        

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        val = self.get_number(1, target_col)
        if val != 0:
            return False
        if target_col != self.get_width()-1:
            for idx in range(target_col+1, self.get_width()):
                if self.get_number(1, idx) != idx + self.get_width()*(1):
                    return False
                if self.get_number(0, idx) != idx + self.get_width()*(0):
                    return False
        for row_idx in range(2, self.get_height()):
            for col_idx in range(0, self.get_width()):
                if self.get_number(row_idx, col_idx) != col_idx + self.get_width()*(row_idx):
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        print self
        move_string = ""               
        
        # find the target value
        move_string1 = ""
        req_row, req_col = self.current_position(0, target_col)        
        if req_col < target_col-1:
            for idx in range(req_col, target_col-1):
                move_string1 = move_string1 + "l"   
                print idx
        zero_row, zero_col = self.current_position(0, 0)
        print zero_col
        if req_row == 1 and req_col == target_col-1:
            move_string1 = move_string1 + "lld"
        else:
            if req_row == 0 and zero_row == 1:
                move_string1 = move_string1 + "ul"
            elif req_row == 1 and zero_row == 0:
                move_string1 = move_string1 + "dl"            
            elif req_row == 0 and zero_row == 0:
                move_string1 = move_string1 + "l"
            else:
                move_string1 = move_string1 + "l"
        print "Found target : " + move_string1
        self.update_puzzle(move_string1)
        print self
        move_string = move_string + move_string1
        
        #move the target value to target position
        move_string2 = ""        
        cur_row, cur_col = self.current_position(0, target_col)        
        zero_row, zero_col = self.current_position(0, 0)
        print cur_row, cur_col
        if cur_row == 0 and cur_col == target_col:
            if zero_row == 0:
                move_string = move_string + "d"
                self.update_puzzle("d")
                print self
                return move_string
            else:
                return move_string
        cur_row, cur_col = self.current_position(0, target_col)        
        if cur_col != target_col-1:
            if cur_row == 0:                
                while cur_col!= target_col-1:
                    move_string2 = move_string2 + "drrul"
                    self.update_puzzle("drrul")
                    print self
                    cur_row, cur_col = self.current_position(0, target_col)
            else:                
                while cur_col!= target_col-1:
                    move_string2 = move_string2 + "urrdl"
                    self.update_puzzle("urrdl")
                    print self
                    cur_row, cur_col = self.current_position(0, target_col)
        print self
        if cur_col == target_col-1 and cur_row == 0:
            move_string2 = move_string2 + "druld"
            self.update_puzzle("druld")
            cur_row, cur_col = self.current_position(1, target_col)
        move_string = move_string + move_string2
        
        move_string = move_string + "urdlurrdluldrruld"
        self.update_puzzle("urdlurrdluldrruld")
        print self
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        print self
        move_string = ""        
        zero_row, zero_col = self.current_position(0, 0)
        # position 0 in the target cell
        if zero_row != 1 or zero_col != target_col:
            if zero_col < target_col:
                for idx in range(zero_col, target_col):
                    move_string = move_string + "r"
                    print idx + idx
            elif zero_col > target_col:
                for idx in range(target_col, zero_col):
                    move_string = move_string + "l"
                    
            if zero_row < 1:
                for idx in range(zero_row, 1):
                    move_string = move_string + "d"
            
            print "Zero movement : " + move_string
            self.update_puzzle(move_string)
            print self
            
        # find the target value
        move_string1 = ""
        req_row, req_col = self.current_position(1, target_col)
        if req_row == 0:
            move_string1 = move_string1 + "u"
        if req_col < target_col:
            for idx in range(req_col, target_col):
                move_string1 = move_string1 + "l"        
                print idx
        print "Found target : " + move_string1
        self.update_puzzle(move_string1)
        print self
        move_string = move_string + move_string1
        
        #move the target value to target position
        move_string2 = ""        
        cur_row, cur_col = self.current_position(1, target_col)        
        zero_row, zero_col = self.current_position(0, 0)
        print zero_col
        if cur_col == target_col and cur_row == 1:
            if zero_row == 1:
                move_string = move_string + "ur"
                self.update_puzzle("ur")
                print self
                return move_string
            else:
                return move_string
        if cur_col != target_col:
            if cur_row == 0:
                while cur_col!= target_col:
                    move_string2 = move_string2 + "drrul"
                    self.update_puzzle("drrul")
                    print self
                    cur_row, cur_col = self.current_position(1, target_col)
            else:
                while cur_col!= target_col:
                    move_string2 = move_string2 + "urrdl"
                    self.update_puzzle("urrdl")
                    print self
                    cur_row, cur_col = self.current_position(1, target_col)
        print self
        if cur_col == target_col and cur_row == 0:
            move_string2 = move_string2 + "druld"
            self.update_puzzle("druld")
            cur_row, cur_col = self.current_position(1, target_col)
        move_string = move_string + move_string2
        print self
        
        move_string = move_string + "ur"
        self.update_puzzle("ur")
        print self
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        print "Entering 2x2 solver"
        move_string = ""
        zero_row, zero_col = self.current_position(0, 0)
        if zero_row != 0 and zero_col != 0:
            if zero_row == 0:
                move_string = move_string + "l"
            else:
                if zero_col == 0:
                    move_string = move_string + "u"
                else:
                    move_string = move_string + "lu"
        self.update_puzzle(move_string)
        print self
        while True:            
            if self.check2x2():
                break
            self.update_puzzle("rdlu")
            print self
            move_string = move_string + "rdlu"
            
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        print self
        move_string = ""
        height = self.get_height()
        width = self.get_width()
        # solve all rows except first two
        for row_idx in range(0, height-2):
            for col_idx in range(0, width):
                temp = ""
                actual_row = height - row_idx -1
                actual_col = width - col_idx - 1
                print "Solving row = " + str(actual_row) + " col = " + str(actual_col)
                if actual_col != 0:
                    temp = self.solve_interior_tile(actual_row, actual_col)
                else:
                    temp = self.solve_col0_tile(actual_row)                
                print self
                move_string = move_string + temp
                
        # solve first two rows
        for col_idx in range(0, width-2):
            for row_idx in range(0, 2):
                temp = ""
                actual_row = 1 - row_idx
                actual_col = width - col_idx - 1
                print "Solving row = " + str(actual_row) + " col = " + str(actual_col)
                if actual_row == 1:
                    temp = self.solve_row1_tile(actual_col)
                else:
                    temp = self.solve_row0_tile(actual_col)
                print self
                move_string = move_string + temp
        
        temp = self.solve_2x2()
        move_string = move_string + temp
        print self
        return move_string
    
    def check2x2(self):  
        """
        To check a valid 2x2 formation
        """
        if self.current_position(0, 0) == (0,0) and self.current_position(0, 1) == (0,1) and self.current_position(1, 0) == (1,0) and self.current_position(1, 1) == (1, 1):
            return True
        else:
            return False

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print obj.lower_row_invariant(1, 2) 
#obj = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [7, 0, 8]])
#print obj.lower_row_invariant(2, 1) 
#obj = Puzzle(4, 5, [[12, 11, 10, 9, 8], [7, 6, 5, 4, 3], [2, 1, 0, 13, 14], [15, 16, 17, 18, 19]])
#print obj.lower_row_invariant(2, 2) 
#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print obj.solve_interior_tile(2, 2)
#print obj.solve_interior_tile(2, 1)
#print obj.solve_col0_tile(2) 
#obj = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [0, 7, 8]])
#print obj.solve_col0_tile(2)
#obj = Puzzle(4, 5, [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]])
#print obj.solve_col0_tile(3)
#obj = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#print obj
#print obj.row0_invariant(2)
#obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
#print obj.solve_2x2()
#obj = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]])
#print obj.solve_row1_tile(2)
#obj = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]])
#print obj.solve_row0_tile(2)
#obj = Puzzle(4, 5, [[1, 2, 0, 3, 4], [6, 5, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print obj.solve_row0_tile(2) 
#obj = Puzzle(4, 5, [[7, 6, 5, 3, 0], [4, 8, 2, 1, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print obj.solve_row0_tile(4)
#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print obj.solve_puzzle() 
#obj = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
#print obj.solve_puzzle()
#obj = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#print obj.solve_puzzle()
#obj = Puzzle(5, 4, [[5, 4, 2, 3], [1, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15], [16, 17, 18, 19]])
#print obj.solve_puzzle()
#obj = Puzzle(3, 6, [[16, 7, 13, 17, 5, 9], [3, 0, 14, 10, 12, 6], [4, 15, 2, 11, 8, 1]])
#print obj.solve_puzzle() 
#obj = Puzzle(2, 4, [[0, 3, 2, 7], [4, 5, 6, 1]])
#print obj.solve_puzzle()