from tabulate import tabulate

# Board super class (Children: SHIP board and CANNONEER board)
class Board:
    def __init__(self, name, grid):
        self.name = name
        self.grid = grid
    
    # ToString returns BOARD showing dictionaries: {"Ship": Type}
    def __str__(self):
        return tabulate(self.grid, tablefmt="heavy_grid")