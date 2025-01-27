from pyamaze import maze, agent, textLabel
from queue import PriorityQueue

def h(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

def a_star(m):
    s = (m.rows, m.cols)
    g = {c: float('inf') for c in m.grid}
    f = {c: float('inf') for c in m.grid}
    g[s] = 0
    f[s] = h(s, (1, 1))
    o = PriorityQueue()
    o.put((f[s], h(s, (1, 1)), s))
    p = {}

    while not o.empty():
        _, _, curr = o.get()
        if curr == (1, 1):
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

                t_g = g[curr] + 1
                t_f = t_g + h(n, (1, 1))

                if t_f < f[n]:
                    g[n] = t_g
                    f[n] = t_f
                    o.put((t_f, h(n, (1, 1)), n))
                    p[n] = curr

    fp = {}
    c = (1, 1)
    while c != s:
        fp[p[c]] = c
        c = p[c]
    return fp

if __name__ == '__main__':
    m = maze(20, 30)
    m.CreateMaze()
    path = a_star(m)
    a = agent(m, footprints=True)
    m.tracePath({a: path})
    l = textLabel(m, 'A* Path Length', len(path) + 1)
    m.run()
