from tabulate import tabulate
from pyfiglet import Figlet
from board import Board
from board_ships import Board_Ships
from board_cannoneer import Board_Cannoneer 
import copy
import time
import random

# Global variables
LETTERS = {"A": "1", "B": "2", "C": "3", "D": "4", "E": "5", "F": "6", "G": "7", "H": "8"}
SHIPS = {"Carrier": 5, "Battleship": 4, "Cruiser": 3, "Submarine": 3, "Destroyer": 2}
SQUARE = "■"

def main():
    wins = 0
    for i in range(1000):
        # TEST SEQUENCE
        player_name = "Ara"
        # For PLAYER AND PC: Create SHIP GRIDS (to save own ships), CANNONEER GRIDS (to save hits/misses on enemy's board), and copy of PLAYER SHIP GRID (to track a visual representation of the PC's hits on the PLAYER's board)
        player_ship_grid = create_grid("ships")
        pc_ship_grid = create_grid("ships")
        player_cannoneer_grid = create_grid("cannoneer")
        pc_cannoneer_grid = create_grid("cannoneer")
        pc_hit_tracker = copy.deepcopy(player_ship_grid)
        # Create PLAYER and PC SHIP BOARD Objects (to [auto-]generate ships on the board as dictionaries)
        player_ship_board = Board_Ships(player_name, player_ship_grid)
        pc_ship_board = Board_Ships("PC", pc_ship_grid)
        # Creates all five ships using the ships dictionary and prints updated grid after each one
        for ship in SHIPS:
            player_ship_board.auto_generate_ship(ship, SHIPS[ship])
            print_visual_grid(player_ship_grid)
        # PC SHIP BOARD: Auto-generate all five ships
        for ship in SHIPS:
            pc_ship_board.auto_generate_ship(ship, SHIPS[ship])
        # Create PLAYER/PC CANNONEER BOARD Objects with arguments: ENEMY GRID (to check for hits), OWN CANNONEER GRID, NAME, and copy of PLAYER GRID for PC CANONEER BOARD (to be able to VISUALLY keep track of the PC'S hits)
        player_cannoneer_board = Board_Cannoneer(player_name, pc_ship_grid, player_cannoneer_grid)
        pc_cannoneer_board = Board_Cannoneer("PC", player_ship_grid, pc_cannoneer_grid, pc_hit_tracker)
        # Mark player ships initially as "▢" on copy of the player's ship grid so player can see his own undamaged ships on the opponent's board when printed out
        pc_cannoneer_board.mark_player_ships_on_pc_hit_tracker()

        # GAME LOOP: PLAYER and PC take turns shooting at each other's boards
        while True:
            # PC sequence ONLY: Run object function to find square and shoot at it
            pc_cannoneer_board.get_target_for_pc_and_shoot()
            # Shows updated HIT TRACKER GRID with PC's hits/misses
            print(tabulate(pc_hit_tracker, tablefmt="heavy_grid"))

            # Check if PC wins: End game and print DEFEAT message
            if pc_cannoneer_board.game_over():
                print("GAME OVER!")
                print("The PC has sunk your fleet and wins the game! Better luck next time.")
                wins += 1
                break
    print(f"Wins: {wins}")
    """
    # Create figlet object for animated text
    figlet = Figlet()
    fonts = figlet.getFonts()
    figlet.setFont(font="smslant")
    player_name = start_game()
    player_name = "Felix"
    # Show fake loading animation
    loading_animation(5)

    # For PLAYER AND PC: Create SHIP GRIDS (to save own ships), CANNONEER GRIDS (to save hits/misses on enemy's board), and copy of PLAYER SHIP GRID (to track a visual representation of the PC's hits on the PLAYER's board)
    player_ship_grid = create_grid("ships")
    pc_ship_grid = create_grid("ships")
    player_cannoneer_grid = create_grid("cannoneer")
    pc_cannoneer_grid = create_grid("cannoneer")
    pc_hit_tracker = copy.deepcopy(player_ship_grid)

    # Create PLAYER and PC SHIP BOARD Objects (to [auto-]generate ships on the board as dictionaries)
    player_ship_board = Board_Ships(player_name, player_ship_grid)
    pc_ship_board = Board_Ships("PC", pc_ship_grid)

    # PLAYER SHIP BOARD: Prompt user to create ships on his board
    time.sleep(1)
    print(f"\nLook at all that water, {player_name}! Let's fill your board with some ships.")
    time.sleep(2)
    # Initially prints empty board in visual format (function below)
    print_visual_grid(player_ship_grid) 
    # Creates all five ships using the ships dictionary and prints updated grid after each one
    for ship in SHIPS:
        player_ship_board.create_ship(ship, SHIPS[ship])
        print_visual_grid(player_ship_grid)

    # PC SHIP BOARD: Auto-generate all five ships
    for ship in SHIPS:
        pc_ship_board.auto_generate_ship(ship, SHIPS[ship])
    
    # Fake PC ship creating messages
    time.sleep(1)
    print("\nYour ships have been placed on the board.")
    time.sleep(1)
    print("\nThe PC is setting up its fleet ...")
    time.sleep(2)
    print("Ready.")
    time.sleep(1)
    
    # Prompt PLAYER for GAME START and create PLAYER and PC CANNONEER BOARDS to shoot and keep track of hits and misses
    while True:
        ready = input(f"\nAre you ready to play, {player_name}? Type 'Yes' or 'No': ").lower()
        if ready == "yes":
            # Create PLAYER/PC CANNONEER BOARD Objects with arguments: ENEMY GRID (to check for hits), OWN CANNONEER GRID, NAME, and copy of PLAYER GRID for PC CANONEER BOARD (to be able to VISUALLY keep track of the PC'S hits)
            player_cannoneer_board = Board_Cannoneer(player_name, pc_ship_grid, player_cannoneer_grid)
            pc_cannoneer_board = Board_Cannoneer("PC", player_ship_grid, pc_cannoneer_grid, pc_hit_tracker)
            # Mark player ships initially as "▢" on copy of the player's ship grid so player can see his own undamaged ships on the opponent's board when printed out
            pc_cannoneer_board.mark_player_ships_on_pc_hit_tracker()
            break
        elif ready == "no":
            print("\nWell, please let me know when you are ...")
            continue
        else:
            print("\nWatch what you're typing, scoundrel!")
            continue

    time.sleep(1)
    print("\nWater, nothing but water!")
    print("")
    time.sleep(1)
    
    # GAME LOOP: PLAYER and PC take turns shooting at each other's boards
    while True:
        # PLAYER sequence: Print grid, then SELECT and SHOOT at a square
        print(tabulate(player_cannoneer_grid, tablefmt="heavy_grid"))
        player_cannoneer_board.get_target_from_player_and_shoot()
        time.sleep(1)
        print("\nYour hits and misses so far on the PC's board.")
        time.sleep(1)
        # Shows updated PC SHIP GRID with PLAYER's hits/misses
        print(tabulate(player_cannoneer_grid, tablefmt="heavy_grid"))
        print("")
        time.sleep(2)

        # Check if PLAYER wins: End game and print VICTORY message
        if player_cannoneer_board.game_over():
            print(figlet.renderText("CONGRATULATIONS!"))
            print("You have sunk your opponent's fleet and win the game!")
            break

        # PC sequence: Run object function to find square and shoot at it
        print("The PC takes aim ...")
        time.sleep(2) 
        pc_cannoneer_board.get_target_for_pc_and_shoot()
        print("\nShips the PC has hit on your board (empty squares mark undamaged parts of your ships)")
        time.sleep(1)
        # Shows updated HIT TRACKER GRID with PC's hits/misses
        print(tabulate(pc_hit_tracker, tablefmt="heavy_grid"))
        time.sleep(2)

        # Check if PC wins: End game and print DEFEAT message
        if pc_cannoneer_board.game_over():
            print(figlet.renderText("GAME OVER!"))
            print("The PC has sunk your fleet and wins the game! Better luck next time.")
            break

        # Print message before continuing loop with PLAYER's turn
        print("\nGet ready to load your cannon.")
        time.sleep(1)
    """
# Create EMPTY GRIDS
def create_grid(type_of_board):
    # Create 9 x 9 2D-list
    grid = [ [""]*9 for i in range(9)]
    # Add left and top bar to GRID: NUMBERS (1-8; horizontally) and LETTERS (A-H; vertically) 
    for i in range(1, 9):
        grid[0][i] = i
        # Get keys (letters) from values (numbers)
        key = [k for k, v in LETTERS.items() if v == f"{i}"]
        grid[i][0] = key[0]
    
    # Creates dummy dictionary with key "ship" and value "None" if type of board is "ships"; creates string of "" (empty == water) if type is "cannoneer"
    for i in range(1,9):
        for j in range(1,9):
            if type_of_board == "ships":
                grid[i][j] = {"ship": None}
            elif type_of_board == "cannoneer":
                grid[i][j] = ""

    return grid

# Print GRID showing ships as ■'s instead of dictionaries and water as "" (empty string)
def print_visual_grid(grid):
    # Create a temporary deepcopy of the grid to leave the original grid unchanged (copy alone isn't sufficient with a 2d list)
    grid_copy_to_print = copy.deepcopy(grid)
    # Replaces all non-"None" squares (ships) with ■ and all "None" squares (water) with "" (empty string)
    for i in range(1, 9):
        for j in range(1, 9):
            if grid[i][j]["ship"] != None:
                grid_copy_to_print[i][j] = SQUARE
            else:
                grid_copy_to_print[i][j] = ""

    # Prints the tabulated visual form of the GRID
    print(tabulate(grid_copy_to_print, tablefmt="heavy_grid"))

# Start game
def start_game():
    figlet2 = Figlet()
    fonts = figlet2.getFonts()
    figlet2.setFont(font="slant")
    print("\n                    Welcome to")
    print(figlet2.renderText("Battleship"))
    while True:
        name = input("Please enter your name to begin the game: ")
        if name == "PC":
            print("This name is already taken. Try again.")
            continue
        else:
            return name

# Fake loading animation on game start
def loading_animation(n):
    print("")
    time.sleep(1)
    for i in range(1, n):
        time.sleep(1)
        print("Loading: ", SQUARE * i * 2, random.randint(i * 20, i * 24), "%")
    print("Loading: ", SQUARE * (n + 10), "100 %")
    time.sleep(1)

if __name__ == "__main__":
    main()