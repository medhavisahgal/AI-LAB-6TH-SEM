import matplotlib.pyplot as plt
import numpy as np
from collections import deque

# Check if a move is valid
def valid(x, y, m):
    return 0 <= x < m.shape[0] and 0 <= y < m.shape[1] and m[x, y] == 0

# Perform BFS for one direction
def bfs(q, v, p, m):
    x, y = q.popleft()
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if valid(nx, ny, m) and (nx, ny) not in v:
            q.append((nx, ny))
            v.add((nx, ny))
            p[(nx, ny)] = (x, y)

# Bidirectional search
def bidir(m, s, g):
    if m[s] == 1 or m[g] == 1:
        return None, None, None

    qs, qg = deque([s]), deque([g])
    vs, vg = {s}, {g}
    ps, pg = {s: None}, {g: None}

    while qs and qg:
        bfs(qs, vs, ps, m)
        bfs(qg, vg, pg, m)
        for n in vs:
            if n in vg:
                return n, ps, pg
    return None, None, None

# Reconstruct path from start to goal
def build_path(n, ps, pg):
    if n is None:
        return []
    path = []
    while n is not None:
        path.append(n)
        n = ps[n]
    path.reverse()
    n = pg[path[-1]]
    while n is not None:
        path.append(n)
        n = pg[n]
    return path

# Visualize the maze and path
def show(m, p, s, g):
    fig, ax = plt.subplots(figsize=(6, 6))
    for y in range(m.shape[0]):
        for x in range(m.shape[1]):
            color = 'white' if m[y, x] == 0 else 'black'
            ax.fill_between([x, x + 1], y, y + 1, color=color)
    for y, x in p:
        ax.fill_between([x, x + 1], y, y + 1, color='gold', alpha=0.5)
    ax.plot(s[1] + 0.5, s[0] + 0.5, 'go')  # Start
    ax.plot(g[1] + 0.5, g[0] + 0.5, 'ro')  # Goal
    ax.set_xlim(0, m.shape[1])
    ax.set_ylim(0, m.shape[0])
    ax.grid(True)
    ax.invert_yaxis()
    plt.show()

# Define maze as a NumPy array
maze = np.array([
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
])

start, goal = (0, 0), (4, 4)
node, ps, pg = bidir(maze, start, goal)
path = build_path(node, ps, pg)
show(maze, path, start, goal)
