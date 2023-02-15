from tabulate import tabulate
from pyfiglet import Figlet
from board import Board
from board_ships import Board_Ships
from board_cannoneer import Board_Cannoneer 
import copy
import time
import random

# Dictionary of letters (keys) and corresponding numbers (values) for grid creation
letters = {"A": "1", "B": "2", "C": "3", "D": "4", "E": "5", "F": "6", "G": "7", "H": "8"}
# Variables to (un)toggle bolt font in terminal; square symbol
bold_on = "\033[1m"
bold_off = "\033[0m"
square = "■"

def main():
    # Start screen with name prompt returns player name
    player_name = start_game()
    # Show fake loading animation
    # loading_animation(5)

    # Create player ship and cannonneer grid; create PC ship grid (PC doesn't need a visual grid to keep track of hits and misses)
    player_ship_grid = create_grid("ships")
    pc_ship_grid = create_grid("ships")
    player_cannoneer_grid = create_grid("cannoneer")
    
    # Create player and PC ship boards
    player_ship_board = Board_Ships(player_name, player_ship_grid)
    pc_ship_board = Board_Ships("PC", pc_ship_grid)
    """
    # PLAYER SHIP BOARD: Prompt user to create ships on his board
    print("\n" + bold_on + f"Look at all that water, {player_name}! Let's fill your board with some ships." + bold_off)
    # Initially prints empty board in visual format 
    print_visual_grid(player_ship_grid) 
    # Creates ships and each time prints grid afterwards
    player_ship_board.create_ship(5, "Carrier")
    print_visual_grid(player_ship_grid) 
    player_ship_board.create_ship(4, "Battleship")
    print_visual_grid(player_ship_grid) 
    player_ship_board.create_ship(3, "Cruiser")
    print_visual_grid(player_ship_grid) 
    player_ship_board.create_ship(3, "Submarine")
    print_visual_grid(player_ship_grid) 
    player_ship_board.create_ship(2, "Destroyer")
    print_visual_grid(player_ship_grid) 
    """
    # PC SHIP BOARD: Auto-generate ships
    pc_ship_board.auto_generate_ship(5, "Carrier")
    pc_ship_board.auto_generate_ship(4, "Battleship")
    pc_ship_board.auto_generate_ship(3, "Cruiser")
    pc_ship_board.auto_generate_ship(3, "Submarine")
    pc_ship_board.auto_generate_ship(2, "Destroyer")

    """
    print("Final player board:")
    print_visual_grid(player_ship_grid) 
    """
    # Prompt user for game start and create cannoneer board to shoot and keep track of hits and misses
    while True:
        ready = input(f"\nAre you ready to play, {player_name}? Type 'Yes' or 'No': ").lower()
        if ready == "yes":
            # Create cannoneer objects with arguments: Opponent's grid (to check), cannoneer grid (only player), name (only player)
            player_cannoneer_board = Board_Cannoneer(pc_ship_grid, player_cannoneer_grid, player_name)
            pc_cannoneer_board = Board_Cannoneer(player_ship_grid)
            break
        elif ready == "no":
            print("Well, please let me know when you are ...")
            continue
        else:
            print("Watch what you're typing, scoundrel!")
            continue
    
    # Print empty cannoneer board
    time.sleep(1)
    print("\nWater, nothing but water!")
    time.sleep(1)
    # Loop: Player and PC take turns shooting at the other's board
    while True:
        print(tabulate(player_cannoneer_grid, tablefmt="heavy_grid"))
        player_cannoneer_board.shoot()
        if player_cannoneer_board.sunk == 5:
            print("\nCongratulations! You have sunk your opponent's fleet and win the game!")
            break

# Create empty grid for boards
def create_grid(type_of_board):
    # Create 9 x 9 2D-list
    grid = [ [""]*9 for i in range(9)]
    # Add left and top bar to grid: numbers (horizontally) and letters (vertically) 
    for i in range(1, 9):
        grid[0][i] = i
        # Get keys (letters) from values (numbers)
        key = [k for k, v in letters.items() if v == f"{i}"]
        grid[i][0] = key[0]
    
    # Creates dictionary with key "ship" and value None if type of board is "ships"; creates string of ~ (water) is type is "cannoneer"
    for i in range(1,9):
        for j in range(1,9):
            if type_of_board == "ships":
                grid[i][j] = {"ship": None}
            elif type_of_board == "cannoneer":
                grid[i][j] = "~"

    return grid

# Print grid showing ships as ■'s instead of dictionaries and water as ~ 
def print_visual_grid(grid):
    # create a temporary deepcopy of the grid to leave the original grid unchanged (copy alone isn't sufficient with a 2d list)
    grid_copy_to_print = copy.deepcopy(grid)
    # replaces all non-None squares (ships) with ■ and all None squares (water) with ~
    for i in range(1, 9):
        for j in range(1, 9):
            if grid[i][j]["ship"] != None:
                grid_copy_to_print[i][j] = square
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
    print("")
    time.sleep(1)
    for i in range(1, n):
        time.sleep(1)
        print("Loading: ", square * i * 2, random.randint(i * 20, i * 24), "%")
    print("Loading: ", square * (n + 10), "100 %")
    time.sleep(1)

if __name__ == "__main__":
    main()