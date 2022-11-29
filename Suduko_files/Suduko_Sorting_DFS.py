from random import shuffle
import copy
"""
SudokuGenerator

Creates a unique Suduko Puzzle that the user has the choice of solving on their own or by using DFS
to solve the puzzle with the total steps taken to complete the puzzle. 

Planning on adding Reinforcment to complete puzzle...
"""



class SudokuGenerator:
	"""Generates and solves Sudoku puzzles using a depth-first search (DFS) algorithm"""
	def __init__(self,grid=None):
		self.Steps = 0
		self.counter = 0
		## Path is for the matplotlib animation
		self.path = []
		## If a grid/puzzle is passed in, make a copy and solve it
		if grid:
			if len(grid[0]) == 9 and len(grid) == 9:
				self.grid = grid
				self.original = copy.deepcopy(grid)
				self.solve_input_sudoku()
			else:
				print("Input needs to be a 9x9 matrix")
		else:
			## If no puzzle is passed, generate one
			self.grid = [[0 for i in range(9)] for j in range(9)]
			self.generate_puzzle()
			self.original = copy.deepcopy(self.grid)
		
		
	def solve_input_sudoku(self):
		"""Solves a puzzle"""
		self.generate_solution(self.grid)
		return

	def generate_puzzle(self):
		"""Generates a new puzzle and solves it"""
		self.generate_solution(self.grid)
		self.print_grid('Full Solution - Completed grid before numbers are removed')
		self.remove_numbers_from_grid()
		self.print_grid('\nIncomplete Solution - Grid after select numbers are removed ready to be completed by depth-first search (DFS) algorithm')

		return

	def print_grid(self, grid_name=None):
		if grid_name:
			print(grid_name)
		for row in self.grid:
			print(row)
		return

	def test_sudoku(self,grid):
		"""Tests each square to make sure it is a valid puzzle"""
		for row in range(9):
			for col in range(9):
				num = grid[row][col]
				## Remove number from grid to test if it's valid
				grid[row][col] = 0
				if not self.valid_location(grid,row,col,num):
					return False
				else:
					#put number back in grid
					grid[row][col] = num
		return True

	def num_used_in_row(self,grid,row,number):
		"""Returns True if the number has been used in that row"""
		if number in grid[row]:
			return True
		return False

	def num_used_in_column(self,grid,col,number):
		"""Returns True if the number has been used in that column"""
		for i in range(9):
			if grid[i][col] == number:
				return True
		return False

	def num_used_in_subgrid(self,grid,row,col,number):
		"""Returns True if the number has been used in that subgrid/box"""
		sub_row = (row // 3) * 3
		sub_col = (col // 3)  * 3
		for i in range(sub_row, (sub_row + 3)): 
			for j in range(sub_col, (sub_col + 3)): 
				if grid[i][j] == number: 
					return True
		return False

	def valid_location(self,grid,row,col,number):
		"""Return False if the number has been used in the row, column or subgrid"""
		if self.num_used_in_row(grid, row,number):
			return False
		elif self.num_used_in_column(grid,col,number):
			return False
		elif self.num_used_in_subgrid(grid,row,col,number):
			return False
		return True

	def find_empty_square(self,grid):
		"""Return the next empty square coordinates in the grid"""
		for i in range(9):
			for j in range(9):
				if grid[i][j] == 0:
					return (i,j)
		return

	def solve_puzzle_dfs(self, grid):
		"""Solve the sudoku puzzle with depth-first search (DFS)"""
		for i in range(0,81):
			row=i//9
			col=i%9
			## Find next empty cell
			if grid[row][col]==0:
				for number in range(1,10):
					## Check that the number hasn't been used in the row/col/subgrid
					if self.valid_location(grid,row,col,number):
						grid[row][col]=number
						self.Steps += 1
						print("Steps: ", self.Steps)
						if not self.find_empty_square(grid):
							self.counter+=1
							break
						else:
							if self.solve_puzzle_dfs(grid):
								return True
				break
		grid[row][col]=0  
		return False

	def generate_solution(self, grid):
		"""Generates a full solution with depth-first search (DFS)"""
		number_list = [1,2,3,4,5,6,7,8,9]
		for i in range(0,81):
			row=i//9
			col=i%9
			## Find next empty cell
			if grid[row][col]==0:
				shuffle(number_list)      
				for number in number_list:
					if self.valid_location(grid,row,col,number):
						self.path.append((number,row,col))
						grid[row][col]=number
						if not self.find_empty_square(grid):
							return True
						else:
							if self.generate_solution(grid):
								## If the grid is full
								return True
				break
		grid[row][col]=0
		return False

	def get_non_empty_squares(self,grid):
		"""Returns a shuffled list of non-empty squares in the puzzle"""
		non_empty_squares = []
		for i in range(len(grid)):
			for j in range(len(grid)):
				if grid[i][j] != 0:
					non_empty_squares.append((i,j))
		shuffle(non_empty_squares)
		return non_empty_squares

	def remove_numbers_from_grid(self):
		"""Remove numbers from the grid to create the puzzle"""
		## Get all non-empty squares from the grid
		non_empty_squares = self.get_non_empty_squares(self.grid)
		non_empty_squares_count = len(non_empty_squares)
		rounds = 3
		while rounds > 0 and non_empty_squares_count >= 17:
			## There should be at least 17 clues
			row,col = non_empty_squares.pop()
			non_empty_squares_count -= 1
			## Might need to put the square value back if there is more than one solution
			removed_square = self.grid[row][col]
			self.grid[row][col]=0
			## Make a copy of the grid to solve
			grid_copy = copy.deepcopy(self.grid)
			## Initialize solutions counter to zero
			self.counter=0
			self.solve_puzzle_dfs(grid_copy)   
			## If there is more than one solution, put the last removed cell back into the grid
			if self.counter!=1:
				self.grid[row][col]=removed_square
				non_empty_squares_count += 1
				rounds -=1			
		return

newPuzzle = int(input("Would you like a Suduko puzzle? 1: Yes\t2: No\nChoice: "))
if(newPuzzle) == 1:
    complete = int(input("Would you like to use depth-first search (DFS) algorithm to complete the puzzle? 1: Yes\tNo: 2\nChoice: "))

    if(complete) == 1:
        ## Solving a new puzzle
        new_puzzle = SudokuGenerator()
        solved = SudokuGenerator(grid = new_puzzle.grid)
        print("\nCompleted puzzle after depth-first search (DFS) algorithm")
        for row in solved.grid:
            print(row)

    elif(complete) == 2:
        new_puzzle = SudokuGenerator()
        print("\nIncomplete Solution - depth-first search (DFS) algorithm was not applied...")
        for row in new_puzzle.grid:
            print(row)
        print("\nYou choose not to complete the puzzle... \n")
    else:
        print("\nThe puzzle was not completed... \n ")

elif(newPuzzle) == 2:
    print("\nNo puzzle was created... \n")
else: 
    print("\nInvalid choice... \n")