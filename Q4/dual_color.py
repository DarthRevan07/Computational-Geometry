import numpy as np
from Q1.DCEL.DCEL import *
from Q1.DCEL.main import buildSimplePolygon
from Q3.triangulator import *
from Q2.main import *
import pickle
DEBUG = False
import matplotlib.pyplot as plt
import os


class Colorizer(object):
    def __init__(self, d, listTriangle):
        # Initialize color to -1
        self.colors = {tuple(v.coords): -1 for v in d.getVertices()}

        # Creating Dual Graph
        self.vdual = {i: listTriangle[i] for i in range(0, len(listTriangle))}
        self.edual = {}
        for i in range(0, len(listTriangle)):
            j = i + 1
            for j in range(0, len(listTriangle)):
                triangle_i = [x.coords for x in listTriangle[i]]
                triangle_j = [x.coords for x in listTriangle[j]]
                if len(set(tuple(pt) for pt in triangle_i) & set(tuple(pt) for pt in triangle_j)) > 1:
                    if i in self.edual and j not in self.edual[i] and i is not j:
                        self.edual[i].append(j)
                    elif i not in self.edual and i is not j:
                        self.edual[i] = [j]
                    if j in self.edual and i not in self.edual[j] and i is not j:
                        self.edual[j].append(i)
                    elif j not in self.edual and i is not j:
                        self.edual[j] = [i]

    def DFS(self, s):
        visited, stack = set(), [s]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                colorsum = self.colors[tuple(self.vdual[vertex][0].coords)] + self.colors[tuple(self.vdual[vertex][1].coords)] + \
                           self.colors[tuple(self.vdual[vertex][2].coords)]
                if DEBUG:
                    print("Changing Coloring of Triangle#:" + str(vertex) + "  from: ", self.colors[tuple(self.vdual[vertex][0].coords)], \
                          self.colors[tuple(self.vdual[vertex][1].coords)], self.colors[tuple(self.vdual[vertex][2].coords)])
                if colorsum < 3:
                    if self.colors[tuple(self.vdual[vertex][0].coords)] == -1:
                        self.colors[tuple(self.vdual[vertex][0].coords)] = 3 - self.colors[tuple(self.vdual[vertex][1].coords)] - \
                                                                    self.colors[tuple(self.vdual[vertex][2].coords)]
                    elif self.colors[tuple(self.vdual[vertex][1].coords)] == -1:
                        self.colors[tuple(self.vdual[vertex][1].coords)] = 3 - self.colors[tuple(self.vdual[vertex][0].coords)] - \
                                                                    self.colors[tuple(self.vdual[vertex][2].coords)]
                    elif self.colors[tuple(self.vdual[vertex][2].coords)] == -1:
                        self.colors[tuple(self.vdual[vertex][2].coords)] = 3 - self.colors[tuple(self.vdual[vertex][1].coords)] - \
                                                                    self.colors[tuple(self.vdual[vertex][0].coords)]
                if DEBUG:
                    print("to: ", self.colors[tuple(self.vdual[vertex][0].coords)], self.colors[tuple(self.vdual[vertex][1].coords)], \
                    self.colors[tuple(self.vdual[vertex][2].coords)])
                visited.add(vertex)
                stack.extend(set(self.edual[vertex]) - visited)

    def colorize(self):
        # key = first triangle to be 3-colored
        key = 0
        if DEBUG:
            print("############################# INITIAL COLORING OF ONE TRIANGLE ##################################")
            print("Triangle #" + str(key) + " Vertex #0 colored to 0")
        self.colors[tuple(self.vdual[key][0].coords)] = 0
        if DEBUG:
            print("Triangle #" + str(key) + " Vertex #1 colored to 1")
        self.colors[tuple(self.vdual[key][1].coords)] = 1
        if DEBUG:
            print("Triangle #" + str(key) + " Vertex #2 colored to 2")
        self.colors[tuple(self.vdual[key][2].coords)] = 2
        if DEBUG:
            print("############################# GOING TO COLOR REMAINING TRIANGLES ###############################")
        self.DFS(key)
        output, col = self.findMinColor()
        return output, col

    def findMinColor(self):
        rcount, gcount, bcount = 0, 0, 0
        r, g, b = [], [], []
        out = set()
        for t in self.vdual.values():
            for it in t:
                if tuple(it.coords) not in out:
                    if self.colors[it.coords] == 0:
                        rcount += 1
                        r.append(it)
                    elif self.colors[it.coords] == 1:
                        gcount += 1
                        g.append(it)
                    elif self.colors[it.coords] == 2:
                        bcount += 1
                        b.append(it)
                    out.add(it.coords)
        if rcount is gcount and rcount is bcount:
            return r, rcount
        if rcount <= gcount and rcount <= bcount:
            return r, rcount
        if gcount <= rcount and gcount <= bcount:
            return g, gcount
        if bcount <= rcount and bcount <= gcount:
            return b, bcount


if __name__ == "__main__":
    with open('../Q1/polygon/vertex_list.pkl', 'rb') as file:
        vertex_list = pickle.load(file)

    dcel = buildSimplePolygon(vertex_list)

    print("Built a DCEL on the given Polygon...")

    # We create a dictionary to map each vertex's coordinates to the corresponding vertex object (x)
    # for x in dcel.getVertices():
    #     print(type(x.coords))
    #     input()
    map_points = {tuple(x.coords): x for x in dcel.getVertices()}

    # Convert vertex_list to a list of Tuples to allow hashing
    vertices = [(vert[0], vert[1]) for vert in vertex_list]


    # Establish a cyclic order of vertices by setting next and prev pointers for each vertice ( to traverse the polygon in a cyclic manner)
    for i in range(1, len(vertices) - 1):
        map_points[vertices[i]].next = map_points[vertices[i + 1]]
        map_points[vertices[i + 1]].prev = map_points[vertices[i]]
    map_points[vertices[0]].prev = map_points[vertices[-1]]
    map_points[vertices[0]].next = map_points[vertices[1]]
    map_points[vertices[1]].prev = map_points[vertices[0]]
    map_points[vertices[-1]].next = map_points[vertices[0]]

    d1 = dcel

    def newline(p, q):
        X = np.linspace(p[0], q[0], endpoint=True)
        Y = np.linspace(p[1], q[1], endpoint=True)
        return X, Y

    """ toDraw : A List of lists, where each sublist contains [X, Y, style]"""
    def nowDraw(toDraw, string = ""):
        for x in toDraw:
            plt.plot(x[0], x[1], x[2])
            plt.title(string)
        plt.show()


    diagnls = monotonePartitioningDgnls(dcel)
    print("Performed Trapezoidalization, and obtained diagonals for Monotones")

    listOfMonos = insertDgnls(dcel, [(x[0].coords, x[1].coords) for x in diagnls])
    print("Obtained a list of Monotones, each of which is a separate DCEL object")

    DEBUG = True
    toDraw = []
    listOfTriangles = []
    tmp = -1

    for mono in listOfMonos:
        diagnls = triangulateMonotonePolygon(mono)
        vv = [(x[0].coords, x[1].coords) for x in diagnls]
        listOfTriangles += insertDgnls(mono, vv)
        tmp += len(diagnls) + 1

    # for t in listOfTriangles:
    #     faces = t.getFaces()
    #     print(f"Number of faces: {len(faces)}")
    #
    #     for idx, face in enumerate(t.getFaces()):
    #         boundary = face.getOuterBoundary()
    #         print(f"Face {idx} has {len(boundary)} half-edges in its outer boundary.")

    # input()
    # print(t.getFaces()[1].getOuterBoundary()[2].origin.coords)
    # input()
    lst = []
    for t in listOfTriangles:
        try:
    # Extracting vertices of the triangles so obtained from the DCEL structure
            element =  [t.getFaces()[1].getOuterBoundary()[0].origin,
                        t.getFaces()[1].getOuterBoundary()[1].origin,
                        t.getFaces()[1].getOuterBoundary()[2].origin
                        ]
            lst.append(element)
        except:
            pass

    listOfTriangles = lst


    colorizer = Colorizer(dcel, listOfTriangles)
    x = colorizer.colorize()
    # print x
    toDraw = []
    for e in d1.getEdges():
        p1, q1 = list(e.origin.coords), list(e.getTwin().origin.coords)
        X, Y = newline(p1, q1)
        toDraw.append([X, Y, 'r'])
    for g in x[0]:
        toDraw.append([g.coords[0], g.coords[1], 'bo'])
    plt.plot(0, 0, label='Guards required: ' + str(x[1]))
    plt.legend()
    nowDraw(toDraw)
    # os.system('rm cgalinput cgalout a.out')