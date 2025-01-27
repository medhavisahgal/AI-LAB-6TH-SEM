from pyamaze import maze, agent

def dfs(m):
    s = (m.rows, m.cols)
    v = [s]
    f = [s]
    p = {}

    while f:
        c = f.pop()
        if c == (1, 1):
            break
        for d in 'ESNW':
            if m.maze_map[c][d]:
                if d == 'E':
                    n = (c[0], c[1] + 1)
                elif d == 'W':
                    n = (c[0], c[1] - 1)
                elif d == 'S':
                    n = (c[0] + 1, c[1])
                elif d == 'N':
                    n = (c[0] - 1, c[1])
                if n in v:
                    continue
                v.append(n)
                f.append(n)
                p[n] = c

    path = {}
    c = (1, 1)
    while c != s:
        path[p[c]] = c
        c = p[c]
    return path

if __name__ == '__main__':
    m = maze(20, 30)
    m.CreateMaze(loopPercent=100)
    path = dfs(m)
    a = agent(m, footprints=True)
    m.tracePath({a: path})
    m.run()
