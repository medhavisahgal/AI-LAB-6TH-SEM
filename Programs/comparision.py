import heapq
import matplotlib.pyplot as plt
from collections import deque

# Define a simple 5x5 grid with obstacles (1 = obstacle, 0 = free)
grid = [
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0]
]
start = (0, 0)
goal = (4, 4)

# Possible movements: right, down, left, up
moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def is_valid(x, y):
    return 0 <= x < 5 and 0 <= y < 5 and grid[x][y] == 0

# BFS Implementation
def bfs():
    queue = deque([(start, [start])])
    visited = {start}
    nodes_explored = 0
    while queue:
        (x, y), path = queue.popleft()
        nodes_explored += 1
        if (x, y) == goal:
            return path, nodes_explored
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))
    return None, nodes_explored

# DFS Implementation
def dfs():
    stack = [(start, [start])]
    visited = {start}
    nodes_explored = 0
    while stack:
        (x, y), path = stack.pop()
        nodes_explored += 1
        if (x, y) == goal:
            return path, nodes_explored
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and (nx, ny) not in visited:
                visited.add((nx, ny))
                stack.append(((nx, ny), path + [(nx, ny)]))
    return None, nodes_explored

# UCS Implementation
def ucs():
    pq = [(0, start, [start])]  # (cost, position, path)
    visited = {start: 0}
    nodes_explored = 0
    while pq:
        cost, (x, y), path = heapq.heappop(pq)
        nodes_explored += 1
        if (x, y) == goal:
            return path, nodes_explored
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            new_cost = cost + 1  # Uniform cost of 1 per step
            if is_valid(nx, ny) and ((nx, ny) not in visited or new_cost < visited[(nx, ny)]):
                visited[(nx, ny)] = new_cost
                heapq.heappush(pq, (new_cost, (nx, ny), path + [(nx, ny)]))
    return None, nodes_explored

# A* Implementation (Manhattan distance heuristic)
def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def a_star():
    pq = [(0 + manhattan_distance(start, goal), 0, start, [start])]  # (f, g, position, path)
    visited = {start: 0}
    nodes_explored = 0
    while pq:
        f, g, (x, y), path = heapq.heappop(pq)
        nodes_explored += 1
        if (x, y) == goal:
            return path, nodes_explored
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            new_g = g + 1
            if is_valid(nx, ny) and ((nx, ny) not in visited or new_g < visited[(nx, ny)]):
                visited[(nx, ny)] = new_g
                h = manhattan_distance((nx, ny), goal)
                heapq.heappush(pq, (new_g + h, new_g, (nx, ny), path + [(nx, ny)]))
    return None, nodes_explored

# Run algorithms and collect data
algorithms = {"BFS": bfs, "DFS": dfs, "UCS": ucs, "A*": a_star}
results = {}
for name, func in algorithms.items():
    path, nodes = func()
    results[name] = {"path_length": len(path) if path else 0, "nodes_explored": nodes}

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Nodes Explored Bar Chart
ax1.bar(results.keys(), [results[alg]["nodes_explored"] for alg in results], color='skyblue')
ax1.set_title("Nodes Explored by Algorithm")
ax1.set_ylabel("Number of Nodes")

# Path Length Bar Chart (if path found)
path_lengths = {alg: res["path_length"] for alg, res in results.items() if res["path_length"] > 0}
ax2.bar(path_lengths.keys(), path_lengths.values(), color='darkblue')
ax2.set_title("Path Length by Algorithm")
ax2.set_ylabel("Path Length")

plt.tight_layout()
plt.show()