from pyamaze import maze, agent, textLabel
from queue import PriorityQueue

def man_dist(c, g):
    return abs(c[0] - g[0]) + abs(c[1] - g[1])

def bfs(m):
    g = (1, 1)
    s = (m.rows, m.cols)
    pq = PriorityQueue()
    pq.put((man_dist(s, g), s))
    v = {s}
    p = {}

    while not pq.empty():
        _, curr = pq.get()
        if curr == g:
            break
        for d in 'ESNW':
            if m.maze_map[curr][d]:
                if d == 'E':
                    n = (curr[0], curr[1] + 1)
                elif d == 'W':
                    n = (curr[0], curr[1] - 1)
                elif d == 'N':
                    n = (curr[0] - 1, curr[1])
                elif d == 'S':
                    n = (curr[0] + 1, curr[1])
                if n not in v:
                    pq.put((man_dist(n, g), n))
                    v.add(n)
                    p[n] = curr

    path = {}
    c = g
    while c != s:
        path[p[c]] = c
        c = p[c]
    return path

if __name__ == '__main__':
    m = maze(5, 7)
    m.CreateMaze(loopPercent=40)
    path = bfs(m)
    a = agent(m, footprints=True, filled=True)
    m.tracePath({a: path})
    textLabel(m, 'Best First Path Length', len(path) + 1)
    m.run()
