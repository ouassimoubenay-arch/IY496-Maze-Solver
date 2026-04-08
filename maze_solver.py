"""
================================================================================
REPORT
================================================================================

This program solves a maze by finding the shortest path from the top-left cell
(Start) to the bottom-right cell (Finish) using the Breadth-First Search (BFS)
algorithm.

WHY BFS AND NOT A TYPICAL DECISION-MAKING ALGORITHM?
A typical decision-making algorithm (e.g., a greedy "always go right/down"
rule) cannot guarantee the shortest path in a maze because walls force
backtracking and indirect routes. BFS is an AI search algorithm that
systematically explores ALL possible paths level by level (one step at a time),
guaranteeing the shortest path is found first. A simple rule-based approach
would fail on many maze configurations, whereas BFS handles any valid maze.

HOW BFS WORKS:
BFS uses a queue (First-In-First-Out). It starts from the Start cell and
explores its neighbours (up, down, left, right). Each newly discovered cell is
added to the queue along with a record of how it was reached (its "parent").
Cells already visited are tracked to prevent re-visiting. This layer-by-layer
expansion guarantees that the first time the Finish cell is reached, it has
been reached in the fewest possible steps.

LIMITATIONS AND BIAS:
- BFS explores in all four directions equally, so it has no directional bias.
- BFS guarantees the shortest path in terms of number of steps, but all steps
  are treated as equal cost (no weighted edges). In a real-world scenario with
  varying terrain costs, Dijkstra's or A* would be more appropriate.
- Memory usage grows with maze size since BFS stores all frontier nodes.
- The maze must be fully loaded into memory, which could be a constraint for
  extremely large mazes.

CODE STRUCTURE:
The program is divided into four functions:
  1. read_maze()     - Reads the maze from a text file into a 2D list.
  2. is_safe()       - Checks whether a move to a given cell is valid.
  3. bfs_search()    - Performs BFS and returns the shortest path.
  4. print_result()  - Displays the result, path, and a visual maze map.

================================================================================
CODE ATTRIBUTION
================================================================================

The BFS algorithm logic (queue-based exploration, visited set, parent tracking
for path reconstruction) was inspired by the general BFS approach described on:
  Source: Wikipedia - Breadth-First Search
  Link:   https://en.wikipedia.org/wiki/Breadth-first_search

The approach for reading and handling a 2D matrix from a text file was
informed by:
  Source: CodeRivers - Python matrix manipulation
  Link:   https://coderivers.org/blog/python-matrix-manipulation/

All code was written independently based on understanding of these concepts.
================================================================================
"""

from collections import deque


# ==============================================================================
# Function: read_maze
# Description: Reads a maze from a text file and returns it as a 2D list.
#              Each cell is represented as 0 (open/passable) or 1 (wall).
# Inputs:
#   - filename (str): Path to the text file containing the maze.
#                     Each row is a line of space-separated integers.
#                     0 = open cell, 1 = wall cell.
# Outputs:
#   - maze (list of list of int): 2D grid representing the maze.
# Function process:
#   Opens the file, reads each line, splits by whitespace, converts each
#   value to an integer, and appends each row to the maze list.
# ==============================================================================
def read_maze(filename):
    maze = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # skip empty lines
                row = [int(cell) for cell in line.split()]
                maze.append(row)
    return maze


# ==============================================================================
# Function: is_safe
# Description: Checks whether it is safe (valid) to move to a given cell.
#              A cell is safe if it is within the maze boundaries and is not
#              a wall (i.e., its value is 0).
# Inputs:
#   - maze (list of list of int): The 2D maze grid.
#   - row (int): The row index of the cell to check.
#   - col (int): The column index of the cell to check.
#   - rows (int): Total number of rows in the maze.
#   - cols (int): Total number of columns in the maze.
# Outputs:
#   - (bool): True if the move is safe, False otherwise.
# Function process:
#   Checks that row and col are within bounds [0, rows) and [0, cols),
#   then checks that the cell value is 0 (not a wall).
# ==============================================================================
def is_safe(maze, row, col, rows, cols):
    return (0 <= row < rows) and (0 <= col < cols) and (maze[row][col] == 0)


# ==============================================================================
# Function: bfs_search
# Description: Performs Breadth-First Search (BFS) on the maze to find the
#              shortest path from the Start (top-left: {0,0}) to the Finish
#              (bottom-right: {rows-1, cols-1}).
# Inputs:
#   - maze (list of list of int): The 2D maze grid.
# Outputs:
#   - path (list of tuple): Ordered list of (row, col) coordinates forming
#                           the shortest path from Start to Finish.
#                           Returns an empty list if no path exists.
#   - distance (int): The number of steps in the shortest path (not counting
#                     the starting cell). Returns -1 if no path exists.
# Function process:
#   1. Initialise a queue with the start cell and a visited set.
#   2. For each cell dequeued, explore all 4 neighbours (up, down, left, right).
#   3. If a neighbour is safe and unvisited, mark it visited, record its
#      parent (for path reconstruction), and enqueue it.
#   4. When the Finish cell is reached, reconstruct and return the path by
#      following parent pointers back to the Start.
#   5. If the queue empties without reaching Finish, return empty path and -1.
# ==============================================================================
def bfs_search(maze):
    rows = len(maze)
    cols = len(maze[0])

    start = (0, 0)
    finish = (rows - 1, cols - 1)

    # Direction vectors: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Queue holds cells to explore (FIFO)
    queue = deque()
    queue.append(start)

    # Track visited cells to avoid re-processing
    visited = set()
    visited.add(start)

    # parent dict maps each cell to the cell it was reached from
    parent = {start: None}

    while queue:
        current_row, current_col = queue.popleft()

        # Check if we reached the Finish cell
        if (current_row, current_col) == finish:
            # Reconstruct path by tracing parent pointers
            path = []
            cell = finish
            while cell is not None:
                path.append(cell)
                cell = parent[cell]
            path.reverse()  # Reverse to get Start -> Finish order
            distance = len(path) - 1  # Distance = steps taken (excluding start)
            return path, distance

        # Explore all 4 neighbours
        for dr, dc in directions:
            next_row = current_row + dr
            next_col = current_col + dc

            if is_safe(maze, next_row, next_col, rows, cols):
                if (next_row, next_col) not in visited:
                    visited.add((next_row, next_col))
                    parent[(next_row, next_col)] = (current_row, current_col)
                    queue.append((next_row, next_col))

    # No path found
    return [], -1


# ==============================================================================
# Function: print_result
# Description: Prints the shortest distance, the path coordinates, and a
#              visual representation of the maze with the path marked.
# Inputs:
#   - maze (list of list of int): The 2D maze grid.
#   - path (list of tuple): The shortest path as a list of (row, col) tuples.
#   - distance (int): The shortest distance (number of steps).
# Outputs:
#   - Prints results to the screen (no return value).
# Function process:
#   If distance is -1, prints "No path found". Otherwise, prints the distance,
#   lists each step with coordinates, then renders the maze with:
#     'S' = Start, 'F' = Finish, '*' = path, '#' = wall, '.' = open cell.
# ==============================================================================
def print_result(maze, path, distance):
    rows = len(maze)
    cols = len(maze[0])

    print("=" * 50)
    print("  MAZE SOLVER - Breadth-First Search (BFS)")
    print("=" * 50)

    if distance == -1:
        print("\n  Result: No path found between Start and Finish.")
        print("  The maze may be unsolvable.\n")
        return

    print(f"\n  Shortest Distance: {distance} step(s)")
    print(f"\n  Path Coordinates ({len(path)} cells including Start and Finish):")

    for i, (r, c) in enumerate(path):
        label = ""
        if i == 0:
            label = " <- START"
        elif i == len(path) - 1:
            label = " <- FINISH"
        print(f"    Step {i:>3}: {{row={r}, col={c}}}{label}")

    # Build visual maze
    path_set = set(path)
    print("\n  Visual Maze (S=Start, F=Finish, *=Path, #=Wall, .=Open):\n")

    # Column header
    col_header = "      " + "  ".join(str(c) for c in range(cols))
    print(col_header)
    print("      " + "--" * cols)

    for r in range(rows):
        row_str = f"  {r} |  "
        for c in range(cols):
            if (r, c) == (0, 0):
                row_str += "S  "
            elif (r, c) == (rows - 1, cols - 1):
                row_str += "F  "
            elif (r, c) in path_set:
                row_str += "*  "
            elif maze[r][c] == 1:
                row_str += "#  "
            else:
                row_str += ".  "
        print(row_str)

    print()
    print("=" * 50)


# ==============================================================================
# MAIN PROGRAM
# ==============================================================================
def main():
    # --- Configuration ---
    maze_file = "maze.txt"  # Change this to your maze file path

    print(f"\n  Loading maze from: '{maze_file}'")

    # Step 1: Read the maze from file
    maze = read_maze(maze_file)

    rows = len(maze)
    cols = len(maze[0])
    print(f"  Maze size: {rows} rows x {cols} cols")
    print(f"  Start: {{row=0, col=0}}")
    print(f"  Finish: {{row={rows - 1}, col={cols - 1}}}")

    # Step 2: Run BFS to find shortest path
    path, distance = bfs_search(maze)

    # Step 3: Print the result
    print_result(maze, path, distance)


if __name__ == "__main__":
    main()