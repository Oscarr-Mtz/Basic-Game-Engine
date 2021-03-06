# A* search homework
# CS 314, Fall 2020

from graphics import *
from time import *
import math

# width and height of graphics screen
WIDTH = 800
HEIGHT = 600


INFINITY = 1000000000

# read in the map into a matrix, m (0 is empty cell, 1 is an impassable cell)
# source into a list, src
# destination into a list, dst
def loadMap(mapName):
    f = open(mapName, "r")
    meta = f.readline()
    rowcol = meta.split()
    rows = int(rowcol[0])
    cols = int(rowcol[1])
    m = [[0 for i in range(cols)] for j in range(rows)]
    src = [0, 0]  # coordinate of starting point
    dst = [0, 0]  # coordinate of ending point
    for i in range(rows):
        line = f.readline()
        for j in range(cols):
            if line[j] == "#":
                m[i][j] = 1   # Wall at this location
            elif line[j] == "1":
                src = [i, j]
            elif line[j] == "2":
                dst = [i, j]
    return m, src, dst

# fills in cell (i, j) in graphics window
def fillCell(w, i, j, m, color):
    rows = len(m)
    cols = len(m[0])
    r = Rectangle(Point(i * WIDTH/cols, j * HEIGHT/rows), Point((i + 1) * WIDTH/cols, (j + 1) * HEIGHT/rows))
    r.setFill(color)
    r.draw(w)

# draw the map
def drawMap(m, src, dst):
    w = GraphWin("A* example", WIDTH, HEIGHT)
    rows = len(m)
    cols = len(m[0])
    for i in range(rows):
        for j in range(cols):
            if m[i][j] == 1:
                fillCell(w, i, j, m, "black")

    # draw source and destination
    fillCell(w, src[0], src[1], m, "green")
    fillCell(w, dst[0], dst[1], m, "red")

    return w



def Dijkstra(w, m, src, dst):
    rows = len(m)
    cols = len(m[0])

    # get mappings from coordinate in grid to node and vice versa
    node = 0
    nodeToCoord = {}
    coordToNode = {}
    for i in range(rows):
        for j in range(cols):
            nodeToCoord[node] = (i, j)
            coordToNode[(i, j)] = node
            node = node + 1
    #print(type(nodeToCoord))

    # populate adjacency matrix
    dist = [[INFINITY for i in range(rows * cols)] for j in range(rows * cols)]
    for i in range(rows):
        for j in range(cols):
            if m[i][j] == 0:
                if i > 0 and j > 0 and m[i-1][j-1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i - 1, j - 1)]] = 14 # NW
                if i > 0 and m[i-1][j] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i - 1, j)]] = 10     # N
                if i > 0 and j < cols - 1 and m[i-1][j+1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i - 1, j + 1)]] = 14 # NE
                if j > 0 and m[i][j-1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i, j - 1)]] = 10     # W
                if j < cols - 1 and m[i][j+1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i, j + 1)]] = 10     # E
                if i < rows - 1 and j > 0 and m[i+1][j-1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i + 1, j - 1)]] = 14 # SW
                if i < rows - 1 and m[i+1][j] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i + 1, j)]] = 10     # S
                if i < rows - 1 and j < cols - 1and m[i+1][j+1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i + 1, j + 1)]] = 14 # SE

    # now perform Dijkstra's algorithm search on graph
    d = {}
    previous = {}
    #print(type(d))
    for i in range(rows * cols):
        d[i] = INFINITY
        previous[i] = None
    u = coordToNode[(src[0], src[1])] # start with source
    #print(u)
    destination = coordToNode[(dst[0], dst[1])]
    d[u] = 0
    Q = [i for i in range(rows * cols)]
    while u != destination:
        # find unvisited node with smallest distance
        u = Q[0]
        for i in range(1, len(Q)):
            if d[Q[i]] < d[u]:
                u = Q[i]
        Q.remove(u)

        (i, j) = nodeToCoord[u]
        fillCell(w, i, j, m, "yellow")

        if d[u] == INFINITY:
            # No path available
            return

        for v in range(rows * cols):
            if dist[u][v] < INFINITY: # neighbours
                alt = d[u] + dist[u][v]
                if alt < d[v]:
                    d[v] = alt
                    previous[v] = u

    S = []
    while previous[u] != None:
        S = [u] + S  # prepend u to S
        u = previous[u]

    for v in S:
        (i, j) = nodeToCoord[v]
        fillCell(w, i, j, m, "blue")

def Astar(w, m, src, dst):
    rows = len(m)
    cols = len(m[0])

    # get mappings from coordinate in grid to node and vice versa
    node = 0
    nodeToCoord = {}
    coordToNode = {}
    for i in range(rows):
        for j in range(cols):
            nodeToCoord[node] = (i, j)
            coordToNode[(i, j)] = node
            node = node + 1
    #print(type(nodeToCoord))

    # populate adjacency matrix
    dist = [[INFINITY for i in range(rows * cols)] for j in range(rows * cols)]
    for i in range(rows):
        for j in range(cols):
            if m[i][j] == 0:
                if i > 0 and j > 0 and m[i-1][j-1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i - 1, j - 1)]] = 14 # NW
                if i > 0 and m[i-1][j] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i - 1, j)]] = 10     # N
                if i > 0 and j < cols - 1 and m[i-1][j+1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i - 1, j + 1)]] = 14 # NE
                if j > 0 and m[i][j-1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i, j - 1)]] = 10     # W
                if j < cols - 1 and m[i][j+1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i, j + 1)]] = 10     # E
                if i < rows - 1 and j > 0 and m[i+1][j-1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i + 1, j - 1)]] = 14 # SW
                if i < rows - 1 and m[i+1][j] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i + 1, j)]] = 10     # S
                if i < rows - 1 and j < cols - 1and m[i+1][j+1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i + 1, j + 1)]] = 14 # SE

    # now perform A* algorithm search on graph
    #intialize values
    d = {}
    previous = {}
    g = {}
    h = {}
    f = {}

    # start with source
    u = coordToNode[(src[0], src[1])]

    #intialize closed set and open set
    closedSet = []
    openSet = [u]

    destination = coordToNode[(dst[0], dst[1])]

    x1 = dst[0]
    y1 = dst[1]
    #print(type(d))
    for i in range(rows * cols):
        d[i] = INFINITY
        f[i] = INFINITY
        previous[i] = None
        g[i] = None
        # print (nodeToCoord[i], i)
        x2, y2 = nodeToCoord[i]
        h[i] = math.sqrt( (x1- x2)**2 + (y1-y2)**2 )

        # print(i)


    #print(u)
    g[u] = 0
    f[u] = h[u] + g[u]
    #print(u)

    while len(openSet) > 0:
        minf = f[openSet[0]]
        u = openSet[0]
        # find unvisited node with smallest distance

        for i in range(len(openSet)):
            if f[openSet[i]] < minf:
                u = openSet[i]
                minf = f[openSet[i]]

        openSet.remove(u)
        closedSet.append(u)

        if u == dst:
            print("Found")
            break;


        (ui, uj) = nodeToCoord[u]
        fillCell(w, ui, uj, m, "yellow")
        sleep(0.03)
        for neighbour in dist[u]:
                v = coordToNode[neighbour]
                if v not in closedSet:
                    if v  not in openSet:
                        openSet.append(v)
                        previous[v] = u
                        # print("g[n]: ", g[v], "\n")
                        # print("g[u]: ", g[u], "\n")
                        # print("d[u][n]: ", dist[u][v], "\n")
                        g[v] = g[u] + dist[u][v]
                        f[v] = g[u] + h[v]

                    elif (g[u] + dist[u][v] <= g[v]):
                        previous[v] = u
                        g[v] = g[u] + dist[u][v]
                        f[v] = g[u] + h[v]

            # print("big for loop")
        # print(len(openSet))

    print("Broke")
    if dst not in closedSet:
        print ("No Path Found")
        return

    S = []
    while previous[u] != None:
        S = [u] + S  # prepend u to S
        u = previous[u]

    for v in S:
        (i, j) = nodeToCoord[v]
        print("HERE")
        fillCell(w, i, j, m, "blue")


def main():
    for level in ["maps/toronto.txt", "maps/vee.txt", "maps/gate.txt", "maps/oval.txt", "maps/quadrant.txt", "maps/trix.txt", "maps/u.txt"]:
        m, src, dst = loadMap(level)

        # run Dijkstra
        w = drawMap(m, src, dst)
        # print("This is m: ", m)
        # print("\nThis is src: ", src)
        # print("\nThis is dst: ", dst)
        Dijkstra(w, m, src, dst)
        w.getMouse()
        w.close()

         # run A*
        w = drawMap(m, src, dst)
        Astar(w, m, src, dst)
        w.getMouse()
        w.close()


if __name__ == "__main__":
    main()
