import heapq
from termcolor import colored

# Class to represent the state of the 8-puzzle
class PuzzleState:
    def __init__(self, board, parent, move, depth, cost):
        self.board = board  # The puzzle board configuration
        self.parent = parent  # Parent state
        self.move = move  # Move to reach this state
        self.depth = depth  # Depth in the search tree
        self.cost = cost  # Cost (depth + heuristic)

    def __lt__(self, other):
        return self.cost < other.cost

# Function to display the board in a visually appealing format
def print_board(board):
    
    print("+---+---+---+")
    for row in range(0, 9, 3):
        row_visual = "|"
        for tile in board[row:row + 3]:
            if tile == 0:  # Blank tile
                row_visual += f" {colored(' ', 'cyan')} |"
            else:
                row_visual += f" {colored(str(tile), 'yellow')} |"
        print(row_visual)
        print("+---+---+---+")

# Goal state for the puzzle
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Possible moves for the blank tile (up, down, left, right)
moves = {
    'U': -3,  # Move up
    'D': 3,   # Move down
    'L': -1,  # Move left
    'R': 1    # Move right
}

# Heuristic 1: Number of misplaced tiles
def h1_misplaced_tiles(board):
    misplaced = 0
    for i in range(9):
        if board[i] != 0 and board[i] != goal_state[i]:
            misplaced += 1
    return misplaced

# Heuristic 2: Sum of Manhattan distances of all tiles from their goal positions
def h2_manhattan_distance(board):
    distance = 0
    for i in range(9):
        if board[i] != 0:
            x1, y1 = divmod(i, 3)
            x2, y2 = divmod(board[i] - 1, 3)
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

# Function to get the new state after a move
def move_tile(board, move, blank_pos):
    new_board = board[:]
    new_blank_pos = blank_pos + moves[move]
    new_board[blank_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[blank_pos]
    return new_board

# A* search algorithm
def a_star(start_state, heuristic_func):
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, PuzzleState(start_state, None, None, 0, heuristic_func(start_state)))

    nodes_explored = 0

    while open_list:
        current_state = heapq.heappop(open_list)
        nodes_explored += 1

        if current_state.board == goal_state:
            return current_state, nodes_explored

        closed_list.add(tuple(current_state.board))

        blank_pos = current_state.board.index(0)

        for move in moves:
            if move == 'U' and blank_pos < 3:  # Invalid move up
                continue
            if move == 'D' and blank_pos > 5:  # Invalid move down
                continue
            if move == 'L' and blank_pos % 3 == 0:  # Invalid move left
                continue
            if move == 'R' and blank_pos % 3 == 2:  # Invalid move right
                continue

            new_board = move_tile(current_state.board, move, blank_pos)

            if tuple(new_board) in closed_list:
                continue

            new_state = PuzzleState(new_board, current_state, move, current_state.depth + 1, current_state.depth + 1 + heuristic_func(new_board))
            heapq.heappush(open_list, new_state)

    return None, nodes_explored

# Function to print the solution path
def print_solution(solution):
    path = []
    current = solution
    while current:
        path.append(current)
        current = current.parent
    path.reverse()

    for step in path:
        print(f"Move: {step.move}")
        print_board(step.board)

# Initial state of the puzzle
initial_state = [1, 2, 3, 4, 0, 5, 6, 7, 8]

# Solve the puzzle using A* algorithm with both heuristics
print(colored("Solving with H1 (Misplaced Tiles):", "blue"))
solution_h1, nodes_h1 = a_star(initial_state, h1_misplaced_tiles)
if solution_h1:
    print(colored("Solution found:", "green"))
    print_solution(solution_h1)
    print(f"Nodes explored: {nodes_h1}")
    print(f"Solution depth: {solution_h1.depth}")
else:
    print(colored("No solution exists.", "red"))

print("\n" + colored("Solving with H2 (Manhattan Distance):", "blue"))
solution_h2, nodes_h2 = a_star(initial_state, h2_manhattan_distance)
if solution_h2:
    print(colored("Solution found:", "green"))
    print_solution(solution_h2)
    print(f"Nodes explored: {nodes_h2}")
    print(f"Solution depth: {solution_h2.depth}")
else:
    print(colored("No solution exists.", "red"))

# Compare performance of the two heuristics
print("\n" + colored("Performance Comparison:", "blue"))
print(f"H1 (Misplaced Tiles): Nodes explored = {nodes_h1}, Solution depth = {solution_h1.depth}")
print(f"H2 (Manhattan Distance): Nodes explored = {nodes_h2}, Solution depth = {solution_h2.depth}")