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
        sleep(0.05)

        if d[u] == INFINITY:
            # No path available
            return

        for v in range(rows * cols):
            if dist[u][v] < INFINITY: # neighbors
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
