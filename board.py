from tabulate import tabulate

# Board super class
class Board:
    def __init__(self, name, grid):
        self.name = name
        self.grid = grid
    
    def __str__(self):
        return tabulate(self.grid, tablefmt="heavy_grid")