from board import Board
from pyfiglet import Figlet
import re
import random
import time

# Dictionary of letters (keys) and corresponding numbers (values) to get squares from user input
letters = {"A": "1", "B": "2", "C": "3", "D": "4", "E": "5", "F": "6", "G": "7", "H": "8"}

# Create figlet object for hit/miss messages
figlet = Figlet()
fonts = figlet.getFonts()
figlet.setFont(font="smslant")

# Board_Cannoneer (subclass of Board) to keep track of HITS and MISSES on opponent's board
class Board_Cannoneer(Board):
    def __init__(self, name, opponent_grid, grid, pc_hit_tracker=None):
        super().__init__(name, grid)
        # Opponent's grid to be able to check for hits and misses
        self.opponent_grid = opponent_grid
        # Extra grid to overlay and show PC hits and misses on a copy of the player board
        self.pc_hit_tracker = pc_hit_tracker
        # Variables to keep track of hits
        self.sunk = 0
        self.carrier = 5
        self.battleship = 4
        self.cruiser = 3
        self.submarine = 3
        self.destroyer = 2
        # Variables for auto-shooting (PC only)
        self.x = None
        self.y = None
        self.last_hit = None
        self.direction = None

    # Mark player ships initially as "▢" so player can see his own undamagaged ships on the PC's board (copy of the player grid)
    def mark_player_ships_on_pc_hit_tracker(self):
        for i in range(1,9):
            for j in range(1,9):
                if self.opponent_grid[i][j]["ship"] != None:
                    self.pc_hit_tracker[i][j] = "▢"
                else:
                    self.pc_hit_tracker[i][j] = ""

    # METHOD 1: Get valid square to shoot at from user input
    def get_target_from_player_and_shoot(self):
        # change active turn to user
        # self.turn = "user"
        while True:
            # Prompt for user input and check if it is a valid square
            square = input("Choose at which square you want to shoot: ")
            if matches := re.search(r"^([A-H])([1-8])$", square, re.IGNORECASE):
                ch, no = int(letters[matches[1].upper()]), int(matches[2])
            else:
                # Prompt again if the user enters an invalid square
                print("This square doesn't exist.")
                continue
            # Check if user tries to fire at a square for the second time
            if self.grid[ch][no] != "":
                print("You have already fired at that square. Please choose a different target.")
                continue
            # Fire if the square is valid and break out of the loop
            self.fire(ch, no)
            break

    # METHOD 2: Get valid square to shoot at for PC through algorithm
    def get_target_for_pc_and_shoot(self):
            if not self.last_hit:
                while True:
                    self.x = random.randint(1, 8)
                    self.y = random.randint(1, 8)
                     # Check if square has already been shot at
                    if self.grid[self.x][self.y] != "":
                        continue        
                    else:
                        self.fire(self.x, self.y)
                        break
            else:
                # After a hit: Shoot at squares adjacent to hit square; after four tries move hit one square to the left and continue (x - 1)
                while True:
                    # Try square on the right of the hit
                    if self.direction != "vertical" and self.y < 8 and self.grid[self.x][self.y + 1] == "":
                        self.fire(self.x, self.y + 1)
                        break                 
                    # Try square on the left of the hit
                    elif self.direction != "vertical" and self.y > 1 and self.grid[self.x][self.y - 1] == "":
                        self.fire(self.x, self.y - 1,)
                        break
                    # If there are already two hits and the direction is horizontal, try up to 3 more squares to the left
                    elif self.direction == "horizontal":
                        for i in [2, 3, 4]:
                            if self.grid[self.x][self.y - i] == "":
                                self.fire(self.x, self.y - i)
                                break
                        break      
                    # Try square above the hit
                    elif self.x > 1 and self.grid[self.x - 1][self.y] == "":
                        self.fire(self.x - 1, self.y)
                        break
                    # Try square below the hit
                    elif self.x < 8 and self.grid[self.x + 1][self.y] == "":
                        self.fire(self.x + 1, self.y)
                        break
                    # If there are already two hits and the direction is vertical, try up to 3 more squares down
                    elif self.direction == "vertical":
                        for i in [2, 3, 4]:
                            if self.grid[self.x + i][self.y] == "":
                                self.fire(self.x + i, self.y)
                                break
                        break      
                    else:
                        break
                            
    # METHOD 3: Shoot if either player or PC has provided a valid square
    def fire(self, ch, no):
        # Re-translate target square from number to to letter/number format for hit/miss print (i. e.: 11 -> A1)
        target = [k for k, v in letters.items() if v == str(ch)][0] + str(no)
        # Marks square with X if no ship was hit and prints miss
        if self.opponent_grid[ch][no]["ship"] == None:
            self.grid[ch][no] = "X"
            time.sleep(1)
            if self.name == "PC":
                # Marks PC miss on hit tracker
                self.pc_hit_tracker[ch][no] = "X"
                print(f"... and hits no target on square {target}.")
                time.sleep(1)
            else:
                print(f"{self.name} hits no target on square {target}.")
                time.sleep(1)

        # Mark square with ■ if a ship was hit -> METHOD 4: updates ship's hit count, check if it was sunk, and return number of total sunk ships
        else:
            self.grid[ch][no] = "■"
            time.sleep(1)
            print(figlet.renderText("HIT"), end="")
            time.sleep(1)
            if self.name == "PC":
                # Marks PC hit on hit tracker
                self.pc_hit_tracker[ch][no] = "■"
                print(f"... and hits a target on square {target}.")
                time.sleep(1)
            else:
                print(f"{self.name} hits a target on square {target}.")
                time.sleep(1)

            # Updates hit position only for PC
            if self.name == "PC":
                # Save direction of ship on consecutive hits and update coordinates of last hit for PC
                if self.last_hit == True:
                    if self.x == ch:
                        self.direction = "horizontal"
                    elif self.y == no:
                        print("vertical")
                        self.direction = "vertical"
                    self.x = ch
                    self.y = no
                # Mark that a ship was hit so next round in get_target_for_pc_and_shoot() new coordinates ARE NOT generated unless a ship is sunk; update coordinates
                self.last_hit = True
            # Runs function to update hit count and check for sunk ships
            self.update_hit_count(ch, no)

    # METHOD 4: Update hitcount, check for sunk ships, and return number of total sunk ships
    def update_hit_count(self, ch, no):
        match self.opponent_grid[ch][no]["ship"]:
            case "Carrier":
                self.carrier -= 1
                if self.carrier == 0:
                    self.sunk += 1
                    # Reset last_hit for PC after shit has been sunk
                    if self.name == "PC":                 
                        self.last_hit = False
                        self.direction = None
                    if self.name == "PC":
                        print(f"\nThe PC has sunk your Carrier!")
                    else:
                        print(f"\nYou have sunk the PC's Carrier!") 

            case "Battleship":
                self.battleship -= 1
                if self.battleship == 0:
                    self.sunk += 1
                    # Reset last_hit for PC after shit has been sunk
                    if self.name == "PC":                 
                        self.last_hit = False
                        self.direction = None
                    if self.name == "PC":
                        print(f"\nThe PC has sunk your Battleship!")
                    else:
                        print(f"\nYou have sunk the PC's Battleship!") 
            case "Cruiser":
                self.cruiser -= 1
                if self.cruiser == 0:
                    self.sunk += 1
                    # Reset last_hit for PC after shit has been sunk
                    if self.name == "PC":                 
                        self.last_hit = False
                        self.direction = None
                    if self.name == "PC":
                        print(f"\nThe PC has sunk your Cruiser!")
                    else:
                        print(f"\nYou have sunk the PC's Cruiser!") 
            case "Submarine":
                self.submarine -= 1
                if self.submarine == 0:
                    self.sunk += 1
                    # Reset last_hit for PC after shit has been sunk
                    if self.name == "PC":                 
                        self.last_hit = False
                        self.direction = None
                    if self.name == "PC":
                        print(f"\nThe PC has sunk your Submarine!")
                    else:
                        print(f"\nYou have sunk the PC's Submarine!")                  
            case "Destroyer":
                self.destroyer -= 1
                if self.destroyer == 0:
                    self.sunk += 1
                    if self.name == "PC":                 
                        self.last_hit = False
                        self.direction = None
                    if self.name == "PC":
                        print(f"\nThe PC sunk your Destroyer!")
                    else:
                        print(f"\nYou have sunk the PC's Destroyer!") 
            case _:
                pass
        # Set last hit to True after all ships have been sunk to not get stuck in first loop
        if self.sunk == 5:
            self.last_hit = True

    def game_over(self):    
        return self.sunk == 5
            
            
