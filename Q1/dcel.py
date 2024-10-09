import math as m
import numpy as np
from Q1.utility import Xygraph
from Q1.vertex import Vertex
from Q1.half_edge import HalfEdge
from Q1.face import Face
import pickle


class DCEL(Xygraph):
    """ Implementation of a Doubly-Connected Edge List"""

    def __init__(self, vl : list, el : list, clip = None):
        """ The Xygraph utility initializes a system of undirected graphs with the following variables being
            changed by the Xygraph class :

            v_list : A list of co-ordinates (can be np.ndarrays or just tuples)
            e_list : Initially passed as empty, used to store the undirected edges between co-ordinates
                     in pairwise order starting from the left.
            clip : A utility flag that can delete the vertices that lie outside the bounding box """
        Xygraph.__init__(self, vl, el)
        # print(self.vl)
        # input()
        self.vertices = []
        self.half_edges = []
        self.faces = []

        #
        if not vl:
            raise ValueError("The vertices list is empty.")

        if clip is not None:
            self.clip(clip)
        self.build_dcel()

    def build_dcel(self):
        """
        Creates the Doubly Connected Edge List from the list of vertices and edges
        """

        # Step 1: vertex list creation
        for v in self.vl:
            self.vertices.append(Vertex(v[0], v[1]))

        # Step 2: hedge list creation. Assignment of twins and
        # vertices
        for e in self.el:
            # e is a tuple of indices (i, j)
            if e[0] >= 0 and e[1] >= 0:
                # Instantiate 2 half-edge objects to start from first vertex
                h1 = HalfEdge(self.vertices[e[0]], self.vertices[e[1]])
                # h1 is i-->j

                h2 = HalfEdge(self.vertices[e[1]], self.vertices[e[0]])
                # h2 is j-->i

                h1.twin = h2
                h2.twin = h1

                # Go to the Vertex object indexed by j
                self.vertices[e[0]].hedgelist.append(h1)
                self.vertices[e[1]].hedgelist.append(h2)

                # Appending the HalfEdge objects to the half_edges list,
                self.half_edges.append(h2)
                self.half_edges.append(h1)

        # for v in self.vertices:
        #     v.print_hedge()
        #     input()


        # Step 3: Identification of next and prev hedges
        for v in self.vertices:
            v.sortincident()
            l = len(v.hedgelist)
            if l < 2:
                # In this scenario it won't be possible to determine
                # prev and next vertices.
                raise ValueError(
                    "Badly formed dcel: less than two hedges in vertex")
            else:
                for i in range(l - 1):
                    v.hedgelist[i].nexthedge = v.hedgelist[i + 1].twin
                    v.hedgelist[i + 1].prevhedge = v.hedgelist[i]
                v.hedgelist[l - 1].nexthedge = v.hedgelist[0].twin
                v.hedgelist[0].prevhedge = v.hedgelist[l - 1]

        # Step 4: Face assignment
        provlist = self.half_edges[:]
        nf = 0
        nh = len(self.half_edges)

        while nh > 0:
            h = provlist.pop()
            nh -= 1
            # We check if the hedge already points to a face
            if h.face == None:
                f = Face()
                nf += 1
                # We link the hedge to the new face
                f.wedge = h
                f.wedge.face = f
                # And we traverse the boundary of the new face
                while (not h.nexthedge is f.wedge):
                    h = h.nexthedge
                    h.face = f
                self.faces.append(f)
        # And finally we have to determine the external face
        for f in self.faces:
            f.external = f.area() < 0

        return

    def print_entities(self):
        print("Vertices:")
        for vertex in self.vertices:
            print(vertex)

        print("\nHalf-Edges:")
        for hedge in self.half_edges:
            print(hedge)

        print("\nFaces:")
        for face in self.faces:
            print(face)


if __name__ == "__main__":

    with open('polygon/vertex_list.pkl', 'rb') as file:
        vertex_list = pickle.load(file)
        # print(vertex_list)


    with open('polygon/edge_index_list.pkl', 'rb') as file:
        edge_list = pickle.load(file)
        # print(edge_list)

    dcel = DCEL(vertex_list, edge_list)
    dcel.print_entities()