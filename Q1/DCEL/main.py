from Q1.DCEL.DCEL import *
from Q1.DCEL.face import *
from Q1.DCEL.edge import *
from Q1.DCEL.point import *
import pickle

def buildSimplePolygon(points):
    d = DCEL()
    if points:
        exterior = d.getExteriorFace()
        interior = Face()
        verts = []
        for p in points:
            verts.append(Point(p))
        innerEdges = []
        outerEdges = []
        for i in range(len(verts)):
            e = Edge()
            e.setOrigin(verts[i])
            verts[i].setIncidentEdge(e)
            e.setFace(interior)
            t = Edge()
            t.setOrigin(verts[(i+1)%len(verts)])
            t.setFace(exterior)
            t.setTwin(e)
            e.setTwin(t)
            innerEdges.append(e)
            outerEdges.append(t)

        for i in range(len(verts)):
            innerEdges[i].setNext(innerEdges[(i+1)%len(verts)])
            innerEdges[i].setPrev(innerEdges[i-1])
            outerEdges[i].setNext(outerEdges[i-1])
            outerEdges[i].setPrev(outerEdges[(i+1)%len(verts)])
        interior.setOuterComponent(innerEdges[0])
        exterior.addInnerComponent(outerEdges[0])
    return d


if __name__ == "__main__":
    with open('../polygon/vertex_list.pkl', 'rb') as file:
        vertex_list = pickle.load(file)

    dcel = buildSimplePolygon(vertex_list)

    with open('dcel_vertices.txt', 'w') as vertex_file, open('dcel_edges.txt', 'w') as edge_file:
        # Write the vertices into 'dcel_vertices.txt'
        vertex_file.write("DCEL Vertices:\n\n")
        for vertex in dcel.getVertices():
            vertex_file.write(str(vertex))
            vertex_file.write("\n")
        vertex_file.write("\n\n")  # Adding space for readability

        # Write the edges into 'dcel_edges.txt'
        edge_file.write("DCEL Edges: \n\n")
        for edge in dcel.getEdges():
            edge_file.write(str(edge))
            edge_file.write("\n\n")
        edge_file.write("\n\n")  # Adding space for readability

    print("Vertices and edges have been written to 'dcel_vertices.txt' and 'dcel_edges.txt' respectively.")