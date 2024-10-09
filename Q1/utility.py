import numpy as np
import math as m

class Xygraph:
    """Represents a set of vertices connected by undirected edges.
    The vertices are stored in a list of coordinates, while
    the edges are stored as a pair of indices (i,j) of the vertices
    list.
    """

    def __init__(self, vl : list, el : list):
        """Creates the 2D graph formed by a list of vertices (x,y)
        and a list of indices (i,j)
        """
        if not vl:
             raise TypeError("Please enter a non-empty list of points.")
        # if vl.shape[1] != 2:
        #     raise ValueError("Vertex list should be a 2D array with shape (n, 2).")

        self.vl = vl
        self.el = el
        if self.vl != []:
            self.minmax()

        return None

    def minmax(self):
        """Determines the boundary box of the vertices in the graph"""
        vx = [v[0] for v in self.vl]
        vy = [v[1] for v in self.vl]
        self.xmax, self.xmin = max(vx), min(vx)
        self.ymax, self.ymin = max(vy), min(vy)

        return None

    def clip(self, clipbox):
        """Trims the vertex and edge list of elements that lie
        outside a clipping box [(xmin,xmax),(ymin,ymax)]"""
        pmin, pmax = clipbox
        ind = []
        vlt = []
        #Direct elimination of out of bounds edges and vertices
        for i in range(len(self.vl)):
            if self.vl[i][0] < pmin[0] or self.vl[i][1] < pmin[1] or \
                self.vl[i][0] > pmax[0] or self.vl[i][1] > pmax[1]:
                ind.append(i)
            else:
                vlt.append(self.vl[i])
        elt = filter((lambda x:(x[0] not in ind) and (x[1] not in ind)),
            self.el)
        li = filter((lambda x: x not in ind),range(len(self.vl)))
        #We rename the indices in the trimmed edge list
        lf = range(len(self.vl) - len(ind))
        equiv = {}
        for i in range(len(li)):
            if li[i] != lf[i]:
                equiv[li[i]] = lf[i]

        for i in range(len(elt)):
            if elt[i][0] in equiv:
                x = equiv[elt[i][0]]
            else:
                x = elt[i][0]
            if elt[i][1] in equiv:
                y = equiv[elt[i][1]]
            else:
                y = elt[i][1]
            elt[i] = (x,y)

        self.vl = vlt
        self.el = elt
        self.minmax()