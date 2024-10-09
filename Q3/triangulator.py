import numpy as np
from Q1.DCEL.DCEL import *
from Q1.DCEL.main import buildSimplePolygon
from Q2.main import *
import pickle
DEBUG = False
import matplotlib.pyplot as plt

def Orientation(p, q, r):
    p = p.coords
    q = q.coords
    r = r.coords
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    return -val


def reflex(p, q, r, chain='l'):
    if (chain == 'r'):
        if Orientation(p, q, r) >= 0:
            return True
        else:
            return False
    elif (chain == 'l'):
        if Orientation(p, q, r) > 0:
            return False
        else:
            return True


def triangulateMonotonePolygon(d):
    pts = [x.origin for x in d.getFaces()[1].getOuterBoundary()]
    if DEBUG:
        print("Polygon Boundary:", [x.coords for x in pts])
    min_index = min(enumerate(pts), key=lambda x: x[1].coords[1])[0]
    max_index = max(enumerate(pts), key=lambda x: x[1].coords[1])[0]
    tmp1 = min(min_index, max_index)
    tmp2 = max(min_index, max_index)
    chain1 = pts[tmp1:(tmp2 + 1)]
    chain2 = pts[tmp2:] + pts[:(tmp1 + 1)]

    if (min(chain1, key=lambda x: x.coords[0]).coords[0] > min(chain2, key=lambda x: x.coords[0]).coords[
        0]):  # ensuring chain1 is left chain
        if DEBUG:
            print("Monotone chains swapped")
        tmp = list(chain1)
        chain1 = chain2
        chain2 = tmp
    if DEBUG:
        print("Left Chain     : ", [x.coords for x in chain1])
        print("Right Chain    : ", [x.coords for x in chain2])
    pts = sorted(pts, key=lambda x: -x.coords[1])
    if DEBUG:
        print("\nSorted pts     : ", [x.coords for x in pts])

    queue = []
    diagonals = []

    queue.append(pts[0])
    queue.append(pts[1])

    i = 2
    while i < (len(pts) - 1):
        if DEBUG:
            print("\ni =", i, ";", pts[i].coords)
        # process(pts[i])
        tmp1 = queue[-1] in chain1
        tmp2 = pts[i] in chain1
        if (tmp1 and not tmp2) or (tmp2 and not tmp1):
            for qpt in queue[1:]:
                diagonals.append((pts[i], qpt))
                if DEBUG:
                    print("Case: a;  \nDiagonals:", [(x[0].coords, x[1].coords) for x in diagonals])
            queue = [queue[-1], pts[i]]
            if DEBUG:
                print("Queue: ", [x.coords for x in queue])
        else:
            if DEBUG:
                print("||||||", queue[-2], queue[-1], pts[i], "chain =", ('l' if tmp1 else 'r'), "|||||")
                print(reflex(queue[-2], queue[-1], pts[i], chain=('l' if tmp1 else 'r')))
                print(Orientation(queue[-2], queue[-1], pts[i]))
            if reflex(queue[-2], queue[-1], pts[i], chain=('l' if tmp1 else 'r')):
                queue.append(pts[i])
                if DEBUG:
                    print("Case: b;  \nDiagonals:")  # reflex
                    print([(x[0].coords, x[1].coords) for x in diagonals])
                    print("Queue: ", [x.coords for x in queue])
            else:
                diagonals.append((pts[i], queue[-2]))
                if DEBUG:
                    print("Case: c;  \nDiagonals:")  # convex
                    print([(x[0].coords, x[1].coords) for x in diagonals])
                    print("Queue: ", [x.coords for x in queue])
                queue.pop(-1)
                if len(queue) == 1:
                    queue.append(pts[i])
                else:
                    i -= 1
        i += 1

    if len(queue) > 2:
        for qpt in queue[1:-1]:
            diagonals.append((pts[i], qpt))
            if DEBUG:
                print("Case: a;  \nDiagonals:", [(x[0].coords, x[1].coords) for x in diagonals])

    if DEBUG:
        print("Queue: ", [x.coords for x in queue])
    return diagonals



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

    # print("OK")
    # input()
    # Plotting the triangles that are obtained by Line-Sweep triangulation on Monotones
    for t in listOfTriangles:
        # print(type(t))
        # input()
        p1, q1 = list(t[0].coords), list(t[1].coords)
        X, Y = newline(p1, q1)
        toDraw.append([X, Y, 'r'])
        p1, q1 = list(t[1].coords), list(t[2].coords)
        X, Y = newline(p1, q1)
        toDraw.append([X, Y, 'b'])
        p1, q1 = list(t[2].coords), list(t[0].coords)
        X, Y = newline(p1, q1)
        toDraw.append([X, Y, 'g'])

    nowDraw(toDraw, string = "Line-Sweep Triangulation of Monotones")