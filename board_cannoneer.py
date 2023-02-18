from board import Board
from pyfiglet import Figlet
import re
import random
import time

# Global variables
LETTERS = {"A": "1", "B": "2", "C": "3", "D": "4", "E": "5", "F": "6", "G": "7", "H": "8"}
SHIPS = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]

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

    # Mark player ships initially as "▢" on HIT TRACKER BOARD so player can see his own undamagaged ships on the PC's board (copy of the player grid)
    def mark_player_ships_on_pc_hit_tracker(self):
        for i in range(1,9):
            for j in range(1,9):
                if self.opponent_grid[i][j]["ship"] != None:
                    self.pc_hit_tracker[i][j] = "▢"
                else:
                    self.pc_hit_tracker[i][j] = ""

    # METHOD 1: Get valid square to shoot at from user input
    def get_target_from_player_and_shoot(self):
        while True:
            # Prompt for user input and check if it is a valid square
            square = input("Choose at which square you want to shoot: ")
            if matches := re.search(r"^([A-H])([1-8])$", square, re.IGNORECASE):
                ch, no = int(LETTERS[matches[1].upper()]), int(matches[2])
            else:
                # Prompt again if the user enters an invalid square
                print("This square doesn't exist.")
                continue
            # Check if user tries to fire at a square for the second time (the square is not empty)
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
                # After a hit: Randomly shoot at one of the four squares adjacent to hit square; if direction is saved (two hits), try fields in direction
                while True:
                    # If there are two horizontal hits, randomly try to shoot at a square left/right in range 4 if it can be on the board and is empty
                    if self.direction == "horizontal":
                        # Variables to prevent one side to check further if non-empty square was detected
                        go_right = True
                        go_left = True
                        # Sequentially check fields from one to a maximum of four fields away from last hit
                        for i in [1, 2, 3, 4]:
                            left_or_right= []
                            # Save square to the right in a list if it is on the board and empty
                            if (self.y + i and go_right == True) <= 8:
                                if self.grid[self.x][self.y + i] == "":
                                    left_or_right.append(self.y + i)
                                else:
                                    # Prevent loop in next iterations to check further to the right if a non-empty square is detected
                                    go_right = False
                            # Save square to the left in a list if it is on the board and empty
                            if (self.y - i and go_left == True) >= 1:
                                if self.grid[self.x][self.y - i] == "":
                                    left_or_right.append(self.y - i)
                                else:
                                    # Prevent loop in next iterations to check further to the left if a non-empty square is detected
                                    go_left = False
                            
                            # If there are squares that can be fired at to the left and/or right (list > 0), shuffle the list to randomize next shot
                            if len(left_or_right) > 0:
                                random.shuffle(left_or_right)
                                # Try every square on the list: Break if one of them can be fired at
                                for y_value in left_or_right:
                                    if self.grid[self.x][y_value] == "":
                                        self.fire(self.x, y_value)
                                        break
                                break      
                            # Continue with square one step further from last hit in both directions if there was no shot                
                        break    

                    # If there are two horizontal hits, randomly try to shoot at a square above/below in range 4 if it can be on the board and is empty
                    elif self.direction == "vertical":
                        # Variables to prevent one side to check further if a non-empty square was detected
                        go_down = True
                        go_up = True
                        # Sequentially check fields from one to a maximum of four fields away from last hit
                        for i in [1, 2, 3, 4]:
                            top_or_bottom = []
                            # Save square below in a list if it is on the board and empty
                            if (self.x + i and go_down == True) <= 8:
                                if self.grid[self.x + i][self.y] == "":
                                    top_or_bottom.append(self.x + i)
                                else:
                                    # Prevent loop in next iterations to check further down if a non-empty square is detected
                                    go_down = False
                            # Save square above in a list if it is on the board and empty
                            if (self.x - i) and go_up == True >= 1:
                                if self.grid[self.x - 1][self.y] == "":
                                    top_or_bottom.append(self.x - i)
                                else:
                                    # Prevent loop in next iterations to check further up if a non-empty square is detected
                                    go_up = False

                            # If there are squares that can be fired at above/below (list > 0), shuffle the list to randomize next shot
                            if len(top_or_bottom) > 0:
                                random.shuffle(top_or_bottom)
                                # Try every square on the list: Break if one of them can be fired at
                                for x_value in top_or_bottom:
                                    if self.grid[x_value][self.y] == "":
                                        self.fire(x_value, self.y)
                                        break
                                break       
                            # Continue with square one step further from last hit in both directions if there was no shot                 
                        break     

                    # If there is only ONE HIT (no direction), randomly select one of the four adjacent squares and shoot at it if it is EMPTY
                    else:
                        # Check if the four adjacent squares are EMPTY and within GRID and add them to a list for possible next shots
                        possible_squares_for_next_shot = []
                        if self.y < 8 and self.grid[self.x][self.y + 1] == "":
                            possible_squares_for_next_shot.append("right")
                        if self.y > 1 and self.grid[self.x][self.y - 1] == "":
                            possible_squares_for_next_shot.append("left")
                        if self.x > 1 and self.grid[self.x - 1][self.y] == "":
                            possible_squares_for_next_shot.append("top")
                        if self.x < 8 and self.grid[self.x + 1][self.y] == "":
                            possible_squares_for_next_shot.append("bottom")
                        # Get random square direction from possible choices
                        square_after_hit = random.choice(possible_squares_for_next_shot)
                        # Shoot at adjacent square according to random choice
                        if square_after_hit == "right":
                                self.fire(self.x, self.y + 1)
                                break                 
                        elif square_after_hit == "left":
                                self.fire(self.x, self.y - 1)
                                break
                        elif square_after_hit == "top":           
                                self.fire(self.x - 1, self.y)
                                break
                        elif square_after_hit == "bottom": 
                                self.fire(self.x + 1, self.y)
                                break
                            
    # METHOD 3: Shoot if either PLAYER or PC has provided a valid square
    def fire(self, ch, no):
        # Re-translate target square from number to to letter/number format for hit/miss print (i. e.: 11 -> A1)
        target = [k for k, v in LETTERS.items() if v == str(ch)][0] + str(no)
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
                        self.direction = "vertical"
                    self.x = ch
                    self.y = no
                # Mark that a ship was hit so next round in get_target_for_pc_and_shoot() new coordinates ARE NOT generated unless a ship is sunk; update coordinates
                self.last_hit = True
            # Runs function to update hit count and check for sunk ships
            self.update_hit_count(ch, no)

    # METHOD 4: Update hit count
    def update_hit_count(self, ch, no):
        # Get ship name from hit square
        hit_ship = self.opponent_grid[ch][no]["ship"]
        match hit_ship:
            case "Carrier":
                self.carrier -= 1
                self.check_sunk("Carrier", self.carrier)
            case "Battleship":
                self.battleship -= 1
                self.check_sunk("Battleship", self.battleship)
            case "Cruiser":
                self.cruiser -= 1
                self.check_sunk("Cruiser", self.cruiser)
            case "Submarine":
                self.submarine -= 1
                self.check_sunk("Submarine", self.submarine)
            case "Destroyer":
                self.destroyer -= 1
                self.check_sunk("Destroyer", self.destroyer)

    # METHOD 5: Check for sunk ships, and return number of total sunk ships
    def check_sunk(self, ship_name, ship_count):  
        if ship_count == 0:
            self.sunk += 1
            if self.name == "PC":
                self.last_hit = False
                self.direction = None
                print(f"\nThe PC has sunk your {ship_name}!")
            else:
                print(f"\nYou have sunk the PC's {ship_name}!") 

        # Set last hit to True after all ships have been sunk to not get stuck in first loop
        if self.sunk == 5:
            self.last_hit = True

    # METHOD 6: Return True if the number of sunk ships is 5 (all ships are destroyed)
    def game_over(self):    
        return self.sunk == 5
            
            
