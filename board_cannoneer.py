from board import Board

# Board_Cannoneer (subclass of Board) to keep track of HITS and MISSES on opponent's board
class Board_Cannoneer(Board):
    def __init__(self, name, grid):
        super().__init__(name, grid)