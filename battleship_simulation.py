from tabulate import tabulate
from battleship import create_grid, print_visual_grid
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
    run_simulation(5)

def run_simulation(n):
    wins = 0
    for i in range(n):
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
            print("The PC takes aim ...")
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

if __name__ == "__main__":
    main()