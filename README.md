# BATTLESHIP
#### Video Demo: <https://youtu.be/O_IH2W3Kz7U>

### Description

#### The game
This is a Python command-line game of BATTLESHIP. The player and the computer take turns shooting at each other's boards until one of them has sunk all of the opponent's five ships: a Carrier (5 squares), a Battleship (4 squares), a Cruiser (3 squares), a Submarine (3 squares), and a Destroyer (2 squares).

The game starts with a prompt for the player's name. Afterwards, they user has to place their ships on the board according to the [official rules](https://www.hasbro.com/common/instruct/battleship.pdf). After another prompt to start the game, the player begins by choosing the first square to shoot at. Hits are marked by a '■' and misses by an 'X'. Then, the PC takes its first shot. To remind the player where they initially placed their ships, undamaged squares of a ship are marked with a '▢". When a ship has been sunk, a message including the name of the destroyed ship is displayed. The PC and the player now take turns until one of them has destroyed the enemy's fleet.


![alt text](https://github.com/fhsch/battleship/blob/main/img/battleship.jpg?raw=true)


#### PC functionality
For the PC, both the placement of the ships and the shooting are handled automatically by the programm. The functionality is described in the following parts about the different program files.

#### board.py
Contains the main program, which consists of the game sequence from the beginning to the end. It also includes functions to 1) create board-style grids (which are then passed as parameters to instantiate board objects), 2) print a visual representation of the player's and PC's boards (which contain dictionaries representing the type of ships on any given square), 3) start the game with a prompt for the player's name, and 4) display the game logo and a (very fake) loading animation. All functionality regarding the boards is handled via objects/classes.

#### board.py
Contains the board super class.

#### board_ships.py
Contains a board sub class to create a board object on which the player's/PC's own ships are stored. It includes a function to let the player manually create ships on their board and another one to randomly auto-generate ships for the PC board in vertical or horizontal direction.

#### board_cannoneer.py
Contains a board sub class to create a board to let the player shoot manually at the PC's board/have the PC auto-shoot at the player's board and store the hits and misses, which are marked as '■' and 'X'. For the PC, it contains the functionality to recognize a hit and fire subsequent shots accordingly until a ship has been sunk.

#### test_project.py
Contains three tests regarding the main program's functions to create a grid, start the game, and show the loading animation.
