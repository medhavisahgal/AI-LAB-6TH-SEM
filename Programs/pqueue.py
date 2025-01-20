from pyamaze import maze,agent,COLOR,textLabel
from queue import PriorityQueue

def manhattan_distance(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

def BestFirstSearch(m):
    goal = (1, 1)
    start = (m.rows, m.cols)
    frontier = PriorityQueue()
    frontier.put((manhattan_distance(start, goal), start))
    explored = {start}
    bfsPath = {}
    
    while not frontier.empty():
        current_cost, currCell = frontier.get()
        if currCell == goal:
            break
            
        for d in 'ESNW':
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])
                
                if childCell not in explored:
                    frontier.put((manhattan_distance(childCell, goal), childCell))
                    explored.add(childCell)
                    bfsPath[childCell] = currCell
    
    fwdPath = {}
    cell = goal
    while cell != start:
        fwdPath[bfsPath[cell]] = cell
        cell = bfsPath[cell]
    return fwdPath

if __name__ == '__main__':
    m = maze(5, 7)
    m.CreateMaze(loopPercent=40)
    path = BestFirstSearch(m)
    a = agent(m, footprints=True, filled=True)
    m.tracePath({a:path})
    l = textLabel(m, 'Length of Best First Path', len(path) + 1)
    m.run()