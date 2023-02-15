from board import Board
import re
import random
import copy

# Dictionary of letters (keys) and corresponding numbers (values) to create squares on the board
letters = {"A": "1", "B": "2", "C": "3", "D": "4", "E": "5", "F": "6", "G": "7", "H": "8"}

# Board_Ships (subclass of Board) to place PLAYER and PC ships
class Board_Ships(Board):
    def __init__(self, name, grid):
        super().__init__(name, grid)
    
    # METHOD 1: Create a single ship of a certain size and name for PLAYER board
    def create_ship(self, size, ship_name):
        print(f"Create a {ship_name} that covers {size} squares.")
        # Loop until a valid ship is created
        while True:
            # Get start and end square from user, check validity and save x (number; no) and y (letter; ch) for both squares
            squares = input(f"Please enter its first and last position from left to right (e. g. 'A1 to A4') or from top to bottom: (e. g. 'A2 to D4'): ")
            if matches := re.search(r"^(([A-H])([1-8])( to )?([A-H])([1-8]))$", squares, re.IGNORECASE):
                square_start_ch, square_start_no, square_end_ch, square_end_no = int(letters[matches[2].upper()]), int(matches[3]), int(letters[matches[5].upper()]), int(matches[6])
            else:
                # Prompt again if one of the given squares does not exist
                print("At least one of the given squares doesn't exist.")
                continue

            # Check if player is trying to build from left to right and gives correct start and end square for the given ship's size -> then try to build the ship
            if square_start_ch == square_end_ch and square_end_no - square_start_no == (size - 1):
                direction = "right"
                # Call METHOD 3: Check if ship can be built (no tiles are occupied)
                if self.check_ship(square_start_ch, square_start_no, square_end_ch, square_end_no, direction):
                    # Call METHOD 4: Build ship
                    self.ship_builder(square_start_ch, square_start_no, square_end_ch, square_end_no, ship_name, direction)
                # Continue with loop if ship can't be built
                else:
                    continue

            # Check if player is trying to build from top to bottom and gives correct start and end square for the given ship's size -> then try to build the ship
            elif square_start_no == square_end_no and square_end_ch - square_start_ch == (size - 1):
                direction = "down"
                # Call METHOD 3: Check if ship can be built (no tiles are occupied)
                if self.check_ship(square_start_ch, square_start_no, square_end_ch, square_end_no, direction):
                    # Call METHOD 4: Build ship
                    self.ship_builder(square_start_ch, square_start_no, square_end_ch, square_end_no, ship_name, direction)
                # Continue with loop if ship can't be built
                else:
                    continue

            # Prompt again if user tries to build ship from right to left or bottom to top
            elif (square_start_ch == square_end_ch and square_end_no < square_start_no) or (square_start_no == square_end_no and square_end_ch < square_start_ch):
                print(f"You have to build your ships from left to right or from top to bottom.")
                continue

            # Prompt again if user tries to build one-square ship, i. e. start and end square are identical
            elif (square_start_ch == square_end_ch and square_start_no == square_end_no):
                print(f"The start and end square of your ship cannot be identical.")
                continue

            # Prompt again in any other uncaught case
            else:
                print(f"Oops, that didn't work. Make sure your ship covers {size} squares.")
                continue

            # Break out of the loop if any of the desired conditions have been met (ship built from left to tight or top to bottom)
            break
    
    # METHOD 2: Auto-generate a single ship of certain size and name in random position for PC board
    def auto_generate_ship(self, size, ship_name): 
        while True:
            # Generate random start square and building direction
            square_start_ch = random.randint(1, 8)
            square_start_no = random.randint(1, 8)
            direction = random.choice(["right", "down"])

            # Try ship from left to right if direction is "right"
            if direction == "right":
                # Create variables for end square according to size
                square_end_ch = copy.copy(square_start_ch)
                square_end_no = square_start_no + (size -1)
                # Try again if end square is out of bounds (> 8):
                if square_end_no > 8:
                    continue
                else:
                    # Call METHOD 3: Check if ship can be built (no tiles are occupied)
                    if self.check_ship(square_start_ch, square_start_no, square_end_ch, square_end_no, direction):
                        # Call METHOD 4: Build ship
                        self.ship_builder(square_start_ch, square_start_no, square_end_ch, square_end_no, ship_name, direction)
                    # Continue with loop if ship can't be built
                    else:
                        continue

            # Try ship from top to bottom if direction is "down"            
            elif direction == "down":
                # Create variables for end square according to size
                square_end_ch = square_start_ch + (size -1)
                square_end_no = copy.copy(square_start_no) 
                # Try again if end square is out of bounds (> 8):
                if square_end_ch > 8:
                    continue
                else:
                    # Call METHOD 3: Check if ship can be built (no tiles are occupied)
                    if self.check_ship(square_start_ch, square_start_no, square_end_ch, square_end_no, direction):
                        # Call METHOD 4: Build ship
                        self.ship_builder(square_start_ch, square_start_no, square_end_ch, square_end_no, ship_name, direction)
                    # Continue with loop if ship can't be built
                    else:
                        continue
            # Break out of the loop if any of the desired conditions have been met (ship built from left to tight or top to bottom)
            break
       
    # METHOD 3: Check if any squares needed for a new ship are already occupied by existing ships
    def check_ship(self, start_ch, start_no, end_ch, end_no, direction):
        # Check from left to right
        if direction == "right":
            for i in range(start_no, end_no + 1):
                # Return False if a square is already occupied (is not None)
                if self.grid[start_ch][i]["ship"] != None:
                    return False
            # Return True if all needed squares are empty
            return True

        # Check from top to bottom
        if direction == "down":
            for i in range(start_ch, end_ch + 1):
                # Return False if a square is already occupied (is not None)
                if self.grid[i][start_no]["ship"] != None:
                    return False
            # Return True if all needed squares are empty
            return True
    
    # METHOD 4: Build actual ships on board
    def ship_builder(self, start_ch, start_no, end_ch, end_no, ship_name, direction):
        # Build from left to right
        if direction == "right":
            # Assign dictionary to square: {"ship": "name_of_ship"}
            for i in range(start_no, end_no + 1):
                self.grid[start_ch][i]["ship"] = ship_name

        # Build from top to bottom
        elif direction == "down":
            # Assign dictionary to square: {"ship": "name_of_ship"}
            for i in range(start_ch, end_ch + 1):
                self.grid[i][start_no]["ship"] = ship_name
        
        # Exit if any error occurs that I haven't yet thought of
        else:
            sys.exit("Some unknown error has occured while trying to auto-generate a ship. Please contact the programmer.")