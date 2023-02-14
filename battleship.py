from tabulate import tabulate

def main():
    #TD: Figlet welcome
    name = "Felix"
    grid = create_grid()
    print(tabulate(grid, tablefmt="heavy_grid"))

# Create empty grid
def create_grid():
    # Save dictionary of letters (keys) and corresponding numbers (values)
    letters = {"A": "1", "B": "2", "C": "3", "D": "4", "E": "5", "F": "6", "G": "7", "H": "8"}
    # Create 9 x 9 2D-list
    grid = [ [""]*9 for i in range(9)]
    # Add numbers (horizontally) and letters (vertically) to grid
    for i in range(1, 9):
        grid[0][i] = i
        # Get keys (letters) from values (numbers)
        key = [k for k, v in letters.items() if v == f"{i}"]
        grid[i][0] = key[0]
    
    return grid

if __name__ == "__main__":
    main()