import math
import heapq
import tkinter as tk

class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0

ROW = 9
COL = 10
CELL_SIZE = 60

COLORS = {
    'blocked': '#8b0000',        # Dark red
    'unblocked': '#ffffff',      # White
    'start': '#32CD32',          # Lime green
    'end': '#1E90FF',           # Dodger blue
    'path': '#FFD700'           # Gold
}

def is_valid(row, col):
    return 0 <= row < ROW and 0 <= col < COL

def is_unblocked(grid, row, col):
    return grid[row][col] == 1

def calculate_h_value(row, col, dest):
    return abs(row - dest[0]) + abs(col - dest[1])  # Manhattan distance

def trace_path(cell_details, dest):
    path = []
    row, col = dest
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        row, col = cell_details[row][col].parent_i, cell_details[row][col].parent_j
    path.append((row, col))
    return path[::-1]

def a_star_search(grid, src, dest):
    if not all(is_valid(*p) for p in [src, dest]):
        print("Invalid source or destination")
        return None

    if not all(is_unblocked(grid, *p) for p in [src, dest]):
        print("Source or destination is blocked")
        return None

    if src == dest:
        return [src]

    closed_list = [[False]*COL for _ in range(ROW)]
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    i, j = src
    cell_details[i][j].f = cell_details[i][j].g = cell_details[i][j].h = 0
    cell_details[i][j].parent_i, cell_details[i][j].parent_j = i, j

    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    while open_list:
        current = heapq.heappop(open_list)
        i, j = current[1], current[2]

        if closed_list[i][j]:
            continue
        closed_list[i][j] = True

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:  # Only 4 directions for Manhattan
            ni, nj = i+dx, j+dy
            if is_valid(ni, nj) and is_unblocked(grid, ni, nj) and not closed_list[ni][nj]:
                if (ni, nj) == dest:
                    cell_details[ni][nj].parent_i, cell_details[ni][nj].parent_j = i, j
                    return trace_path(cell_details, dest)
                g_new = cell_details[i][j].g + 1
                if g_new < cell_details[ni][nj].g:
                    cell_details[ni][nj].g = g_new
                    cell_details[ni][nj].h = calculate_h_value(ni, nj, dest)
                    cell_details[ni][nj].f = g_new + cell_details[ni][nj].h
                    cell_details[ni][nj].parent_i, cell_details[ni][nj].parent_j = i, j
                    heapq.heappush(open_list, (cell_details[ni][nj].f, ni, nj))

    print("Path not found")
    return None

class PathVisualizer(tk.Tk):
    def __init__(self, grid, path, src, dest):
        super().__init__()
        self.title("A* Pathfinding Visualization")
        self.grid = grid
        self.path = path
        self.src = src
        self.dest = dest
        self.canvas = tk.Canvas(self, 
                              width=COL*CELL_SIZE, 
                              height=ROW*CELL_SIZE,
                              bg='white')
        self.canvas.pack()
        self.draw_grid()
        
    def draw_grid(self):
        for row in range(ROW):
            for col in range(COL):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                
                color = COLORS['unblocked']
                if self.grid[row][col] == 0:
                    color = COLORS['blocked']
                elif (row, col) == self.src:
                    color = COLORS['start']
                elif (row, col) == self.dest:
                    color = COLORS['end']
                elif self.path and (row, col) in self.path:
                    color = COLORS['path']
                
                self.canvas.create_rectangle(x1, y1, x2, y2, 
                                           fill=color, outline='#696969')
                if self.grid[row][col] == 0:
                    self.canvas.create_line(x1, y1, x2, y2, fill='black', width=2)
                    self.canvas.create_line(x1, y2, x2, y1, fill='black', width=2)

def main():
    grid = [
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 0, 0, 1]
    ]
    
    src = (8, 0)
    dest = (0, 0)
    path = a_star_search(grid, src, dest)
    
    if path:
        print("Path found:", path)
        app = PathVisualizer(grid, path, src, dest)
        app.mainloop()
    else:
        print("No path found")

if __name__ == "__main__":
    main()