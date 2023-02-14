from tabulate import tabulate
from pyfiglet import Figlet
import copy
import re
import time
import random

# Dictionary of letters (keys) and corresponding numbers (values) for field creation
letters = {"A": "1", "B": "2", "C": "3", "D": "4", "E": "5", "F": "6", "G": "7", "H": "8"}
# Variables to (un)toggle bolt font in terminal
bold_on = "\033[1m"
bold_off = "\033[0m"
square = "■"

# Board super class
class Board:
    def __init__(self, name, grid):
        self.name = name
        self.grid = grid
    
    def __str__(self):
        return tabulate(self.grid, tablefmt="heavy_grid")

# Board to place player ships
class Board_Ships(Board):
    def __init__(self, name, grid):
        super().__init__(name, grid)
    
    # Create ships of certain size and name
    def create_ship(self, size, ship_name):
        print(f"Create a {ship_name} that covers {size} squares.")
        # Loop until a valid ship is created
        while True:
            # Get start and end square from userm check validity and save x and y (get numbers corresponding to letters via dict, e. g: A -> 1) separately for both squares
            squares = input(f"Please enter its first and last position from left to right (e. g. 'A1 to A4') or from top to bottom: (e. g. 'A2 to D4'): ")
            if matches := re.search(r"^(([A-H])([1-8])( to )?([A-H])([1-8]))$", squares, re.IGNORECASE):
                field_start_ch, field_start_no, field_end_ch, field_end_no = int(letters[matches[2].upper()]), int(matches[3]), int(letters[matches[5].upper()]), int(matches[6])
            else:
                print("At least one of the given squares doesn't exist.")
                continue

            # Built ship to the right if possible
            if field_start_ch == field_end_ch and field_end_no - field_start_no == (size - 1):
                if(self.check_ship(field_start_ch, field_start_no, field_end_ch, field_end_no, self.grid, "right")):
                        for i in range(field_start_no, field_end_no + 1):
                            self.grid[field_start_ch][i]["ship"] = ship_name

                else:
                    print("Oops. One of the squares seems to be occupied by another ship.")
                    continue

            # Built ship downwards if possible
            elif field_start_no == field_end_no and field_end_ch - field_start_ch == (size - 1):
                if(self.check_ship(field_start_ch, field_start_no, field_end_ch, field_end_no, self.grid, "down")):
                        for i in range(field_start_ch, field_end_ch + 1):
                            self.grid[i][field_start_no]["ship"] = ship_name
                else:
                    print("Oops! One of the squares seems to be occupied by another ship.")
                    continue
            
            # Prompt again if user tries to build ship from right to left or bottom to top
            elif (field_start_ch == field_end_ch and field_end_no < field_start_no) or (field_start_no == field_end_no and field_end_ch < field_start_ch):
                print(f"You have to build your ships from left to right or from top to bottom.")
                continue

            # Prompt again if user tries to build one-square ship, i. e. start and end square are identical
            elif (field_start_ch == field_end_ch and field_start_no == field_end_no):
                print(f"The start and end square of your ship cannot be identical.")
                continue

            # Prompt again in any other uncaught case
            else:
                print(f"Oops, that didn't work. Make sure your ship covers {size} squares.")
                continue

            # Print finished board with all ships and break out of the loop
            print_visual_grid(self.grid)
            break

    # Check if any squares are already occupied by other ships
    def check_ship(self, start_ch, start_no, end_ch, end_no, board, direction):
        # Check from left to right
        if direction == "right":
            for i in range(start_no, end_no + 1):
                if self.grid[start_ch][i]["ship"] != None:
                    return False
            return True
        # Check from top to bottom
        if direction == "down":
            for i in range(start_ch, end_ch + 1):
                if self.grid[i][start_no]["ship"] != None:
                    return False
            return True

# Board to keep track of hits on opponent's board
class Board_Canon:
    ...

def main():
    # Start screen with name prompt returns player name
    name = start_game()
    # Show fake loading animation
    loading_animation(5)
    # Create grid
    grid = create_grid("ships")

    # Create board and change one square to test
    board = Board_Ships(name, grid)

    print("\n" + bold_on + f"Hi {name}! Let's fill your board with some ships." + bold_off)
    # Prints board in visual format 
    print_visual_grid(grid) 
    # Creates ships
    board.create_ship(5, "Carrier")
    board.create_ship(4, "Battleship")
    board.create_ship(3, "Cruiser")
    board.create_ship(3, "Submarine")
    board.create_ship(2, "Destroyer")

    ready = input(f"Well done! Are you ready to play, {name}? Type 'Yes' or 'No': ")

# Create empty grid
def create_grid(type_of_board):
    # Create 9 x 9 2D-list
    grid = [ [""]*9 for i in range(9)]
    # Add left and top bar to grid: numbers (horizontally) and letters (vertically) 
    for i in range(1, 9):
        grid[0][i] = i
        # Get keys (letters) from values (numbers)
        key = [k for k, v in letters.items() if v == f"{i}"]
        grid[i][0] = key[0]
    
    # Creates dictionary with key "ship" and value None if type of board is "ships"
    if type_of_board == "ships":
        for i in range(1,9):
            for j in range(1,9):
                grid[i][j] = {"ship": None}

    return grid

# Print grid showing ships as ■'s instead of dictionaries and water as ~ 
def print_visual_grid(grid):
    # create a temporary deepcopy of the grid to leave the original grid unchanged (copy alone isn't sufficient with a 2d list)
    grid_copy_to_print = copy.deepcopy(grid)
    # replaces all non-None squares (ships) with ■ and all None squares (water) with ~
    for i in range(1, 9):
        for j in range(1, 9):
            if grid[i][j]["ship"] != None:
                grid_copy_to_print[i][j] = "■"
            else:
                grid_copy_to_print[i][j] = "~"
    # prints the tabulated visual form of the grid
    print(tabulate(grid_copy_to_print, tablefmt="heavy_grid"))

# Start game
def start_game():
    figlet = Figlet()
    fonts = figlet.getFonts()
    figlet.setFont(font="slant")
    print("\n                    Welcome to")
    print(figlet.renderText("Battleship"))
    return input("Please enter your name to begin the game: ")

# Fake loading animation on game start
def loading_animation(n):
    time.sleep(1)
    for i in range(1, n):
        time.sleep(1)
        print("Loading: ", square * i * 2, random.randint(i * 20, i * 24), "%")
    print("Loading: ", square * (n + 10), "100 %")
    time.sleep(1)

if __name__ == "__main__":
    main()