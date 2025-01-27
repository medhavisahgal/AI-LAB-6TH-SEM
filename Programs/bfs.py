from pyamaze import maze, agent, textLabel

def bfs(m):
    s = (m.rows, m.cols)
    q = [s]
    v = [s]
    p = {}

    while q:
        c = q.pop(0)
        if c == (1, 1):
            break

        for d in 'ESNW':
            if m.maze_map[c][d]:
                if d == 'E':
                    n = (c[0], c[1] + 1)
                elif d == 'W':
                    n = (c[0], c[1] - 1)
                elif d == 'N':
                    n = (c[0] - 1, c[1])
                elif d == 'S':
                    n = (c[0] + 1, c[1])

                if n in v:
                    continue

                q.append(n)
                v.append(n)
                p[n] = c

    path = {}
    c = (1, 1)
    while c != s:
        path[p[c]] = c
        c = p[c]

    return path

if __name__ == '__main__':
    m = maze(20, 30)
    m.CreateMaze(loopPercent=40)
    path = bfs(m)

    a = agent(m, footprints=True, filled=True)
    m.tracePath({a: path})
    l = textLabel(m, 'Shortest Path Length', len(path) + 1)

    m.run()
