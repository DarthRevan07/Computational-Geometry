# -----------------------------------------------------------------------------
#   Improved polygon generation algorithm
# -----------------------------------------------------------------------------

from edge import Edge
from polygon import Polygon
from Math import quickhull, pnt2line

import heapq
import sys
import matplotlib.pyplot as plt
import time
import pickle


if __name__ == "__main__":

    # take input from test.txt
    f = open("test.txt", "r")

    # start timer
    start = time.time()

    # insert input points to list
    points = []
    n = int(f.readline())
    for i in range(n):
        coord = f.readline().split(' ')
        points.append([float(coord[0]), float(coord[1])])

    # initialize the polygon as a convex hull of the points
    polygon = Polygon(quickhull(points))

    # update points set to exclude polygon vertices
    points = [x for x in points if x not in polygon.vertices]

    # initialize MinPQ, dictionary
    distances = []
    heapq.heapify(distances)
    distancesDict = {}

    # pre-process by adding the distances between every edge-point pair into MinPQ and dictionary
    for edge in polygon.edges:
        for point in points:
            curr_dist = pnt2line(point, edge.start, edge.end)
            heapq.heappush(distances, curr_dist)
            distancesDict[curr_dist] = (edge, point)

    # iterate so long as there still exist points in the interior
    while points and len(distances) != 0:

        # get the current shortest distance and its corresponding edge-point pair
        curr_dist = heapq.heappop(distances)
        e = distancesDict[curr_dist][0]
        point = distancesDict[curr_dist][1]

        # check if the edge exists in the current polygon
        containsE = False
        for edge in polygon.edges:
            if e.start == edge.start and e.end == edge.end:
                containsE = True

        # proceed only if edge is in polygon, point is in interior, and it is a
        # valid addition to the polygon
        if containsE and point in points and e.valid(polygon, point):
            # get index of the edge
            for edge in polygon.edges:
                if e.start == edge.start and e.end == edge.end:
                    i = polygon.edges.index(edge)
            # insert new edges and point into the polygon,
            # remove old edge from polygon and remove point from interior
            polygon.vertices.insert(i + 1, point)
            polygon.edges[i] = Edge(e.start, point)
            polygon.edges.insert(i + 1, Edge(point, e.end))
            points.remove(point)
            # update MinPQ by adding distances between two new edges
            # and every point in interior
            e1 = Edge(e.start, point)
            e2 = Edge(point, e.end)
            for point in points:
                curr_dist_e1 = pnt2line(point, e1.start, e1.end)
                curr_dist_e2 = pnt2line(point, e2.start, e2.end)
                heapq.heappush(distances, curr_dist_e1)
                heapq.heappush(distances, curr_dist_e2)
                distancesDict[curr_dist_e1] = (e1, point)
                distancesDict[curr_dist_e2] = (e2, point)

    # print results
    print()
    print("--------------- From the Approach, --------------")
    print("Number of vertices:  %i" % n)
    print("Execution time:      %s seconds" % (time.time() - start))
    print("------------------------------------------------")
    print()
    print("--------------- Polygon Info : ------------------")
    # print(polygon.vertices)
    # for edge in polygon.edges:
    #     print(edge.start, "------", edge.end)
    print(polygon.vertices)
    print()
    # Creating index-wise edge list to be used for DCEL
    edgeset = polygon.edges
    vertex_list = polygon.vertices

    edge_list = []
    edge_index = []
    for edge in edgeset:
        edge_tup = (edge.start, edge.end)
        edge_list.append(edge_tup)

    i_list, j_list = zip(*edge_list)
    del edge_list, edgeset

    for iter in range(len(i_list)):
        tup = (vertex_list.index(i_list[iter]), vertex_list.index(j_list[iter]))
        edge_index.append(tup)

    # print(edge_index)

    with open('vertex_list.pkl', 'wb') as file:
        pickle.dump(vertex_list, file)


    with open('edge_index_list.pkl', 'wb') as file:
        pickle.dump(edge_index, file)

    # plot the polygon
    pset = polygon.vertices
    pset.append(pset[0])
    xs, ys = zip(*pset)
    plt.plot(xs, ys)
    plt.show()

    # close test.txt file
    f.close()