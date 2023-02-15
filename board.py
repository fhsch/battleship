from tabulate import tabulate
import re

# Dictionary of letters (keys) and corresponding numbers (values) for field creation
letters = {"A": "1", "B": "2", "C": "3", "D": "4", "E": "5", "F": "6", "G": "7", "H": "8"}

# Board super class
class Board:
    def __init__(self, name, grid):
        self.name = name
        self.grid = grid
    
    def __str__(self):
        return tabulate(self.grid, tablefmt="heavy_grid")