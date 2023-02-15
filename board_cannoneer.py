from board import Board
import re

# Dictionary of letters (keys) and corresponding numbers (values) to get squares from user input
letters = {"A": "1", "B": "2", "C": "3", "D": "4", "E": "5", "F": "6", "G": "7", "H": "8"}

# Board_Cannoneer (subclass of Board) to keep track of HITS and MISSES on opponent's board
class Board_Cannoneer(Board):
    def __init__(self, opponent_grid, grid=None, name="PC"):
        super().__init__(name, grid)
        self.opponent_grid = opponent_grid
        self.sunk = 0
        self.carrier = 5
        self.battleship = 4
        self.cruiser = 3
        self.submarine = 3
        self.destroyer = 2
    
    def shoot(self):
        while True:
            # Prompt for user input and check if it is a valid square
            square = input("Choose at which square you want to shoot: ")
            if matches := re.search(r"^([A-H])([1-8])$", square, re.IGNORECASE):
                ch, no = int(letters[matches[1].upper()]), int(matches[2])
            else:
                # Prompt again if the user tries to fire at a square they had fired at before
                print("This square doesn't exist.")
                continue
            # Check if user tries to fire at a square for the second time
            if self.grid[ch][no] != "~":
                print("You have already fired at that square. Please choose a different target.")
                continue
            # Marks square with X if no shit was hit
            if self.opponent_grid[ch][no]["ship"] == None:
                self.grid[ch][no] = "X"
                break
            # Marks square with ■ if a ship was hit; METHOD 1: updates ship's hit count, check if it was sunk; METHOD 2: Check if all ships are sunk -> ends the game
            else:
                self.grid[ch][no] = "■"
                self.update_hit_count(ch, no)
                self.check_game_end()
                break

    # METHOD 1: Update hitcount and check for sunk ships
    def update_hit_count(self, ch, no):
        match self.opponent_grid[ch][no]["ship"]:
            case "Carrier":
                self.carrier -= 1
                if self.carrier == 0:
                    self.sunk += 1
                    print(f"\nYou have sunk your opponent's Carrier!")
            case "Battleship":
                self.battleship -= 1
                if self.battleship == 0:
                    self.sunk += 1
                    print(f"\nYou have sunk your opponent's Battleship!")
            case "Cruiser":
                self.cruiser -= 1
                if self.cruiser == 0:
                    self.sunk += 1
                    print(f"\nYou have sunk your opponent's Cruiser!")
            case "Submarine":
                self.submarine -= 1
                if self.submarine == 0:
                    print(f"\nYou have sunk your opponent's Submarine!")
                    self.sunk += 1
            case "Destroyer":
                self.destroyer -= 1
                if self.destroyer == 0:
                    self.sunk += 1
                    print(f"\nYou have sunk your opponent's Destroyer!")

    # METHOD 2: Check if all ships were sunk
    def check_game_end(self):
        return self.sunk
            
            
