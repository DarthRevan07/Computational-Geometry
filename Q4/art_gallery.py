import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import networkx as nx
import pickle

def main():
    with open('../Q1/polygon/vertex_list.pkl', 'rb') as file:
        vertex_list = pickle.load(file)
        # print(vertex_list)

    with open('../Q1/polygon/edge_index_list.pkl', 'rb') as file:
        edge_list = pickle.load(file)

    vertices = np.array(vertex_list)


    def is_ear(i, vertices, remaining_vertices, polygon_edges):
        """Check if the triangle formed by vertex i and its two neighbors is an ear."""
        v0 = vertices[i]
        v1 = vertices[(i + 1) % len(vertices)]
        v2 = vertices[(i - 1) % len(vertices)]
        ear_triangle = np.array([v0, v1, v2])

        # Check if any remaining vertex is inside the ear triangle
        for j in remaining_vertices:
            if j not in [i, (i + 1) % len(vertices), (i - 1) % len(vertices)]:
                if is_point_in_triangle(vertices[j], ear_triangle):
                    return False  # Found a point inside the triangle
        return True

        for edge in polygon_edges:
            if edges_intersect(v0, v1, vertices[edge[0]], vertices[edge[1]]):
                return False  # Intersection found, not an ear
        return True


    def is_point_in_triangle(pt, triangle):
        """Check if a point is inside a triangle using barycentric coordinates."""
        v0, v1, v2 = triangle
        area = 0.5 * (-v1[1] * v2[0] + v0[1] * (-v1[0] + v2[0]) + v0[0] * (v1[1] - v2[1]) + v1[0] * v2[1])
        s = 1 / (2 * area) * (v0[1] * v2[0] - v0[0] * v2[1] + (v2[1] - v0[1]) * pt[0] + (v0[0] - v2[0]) * pt[1])
        t = 1 / (2 * area) * (v0[0] * v1[1] - v0[1] * v1[0] + (v0[1] - v1[1]) * pt[0] + (v1[0] - v0[0]) * pt[1])
        return s > 0 and t > 0 and (s + t) < 1


    def edges_intersect(p1, p2, p3, p4):
        """Check if line segments (p1, p2) and (p3, p4) intersect."""

        def orientation(p, q, r):
            """Return the orientation of the ordered triplet (p, q, r).
            0 -> p, q and r are collinear
            1 -> Clockwise
            2 -> Counterclockwise
            """
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else 2

        o1 = orientation(p1, p2, p3)
        o2 = orientation(p1, p2, p4)
        o3 = orientation(p3, p4, p1)
        o4 = orientation(p3, p4, p2)

        # General case
        if o1 != o2 and o3 != o4:
            return True

        return False

    def ear_clipping_triangulation(vertices):
        """Perform ear clipping triangulation on the polygon defined by the vertices."""
        remaining_vertices = list(range(len(vertices)))
        polygon_edges = edge_list
        triangles = []

        while len(remaining_vertices) > 3:
            for i in range(len(remaining_vertices)):
                if is_ear(remaining_vertices[i], vertices, remaining_vertices, polygon_edges):
                    # Add the ear triangle
                    triangles.append([vertices[remaining_vertices[i]],
                                      vertices[remaining_vertices[(i + 1) % len(remaining_vertices)]],
                                      vertices[remaining_vertices[(i - 1) % len(remaining_vertices)]]])
                    # Remove the vertex
                    del remaining_vertices[i]
                    break
        # Add the last triangle
        if len(remaining_vertices) == 3:
            triangles.append([vertices[remaining_vertices[0]],
                              vertices[remaining_vertices[1]],
                              vertices[remaining_vertices[2]]])
        return triangles

    # Triangulate the polygon
    triangles = ear_clipping_triangulation(vertex_list)

    # Plot the original polygon
    plt.figure(figsize=(10, 6))
    plt.fill(vertices[:, 0], vertices[:, 1], 'lightgray', edgecolor='black', label='Polygon')
    plt.plot(*zip(*vertices), 'o', color='black')  # Vertices

    for idx, triangle in enumerate(triangles):
        print(f"Index {idx} :  {triangle}")

    # Draw triangulation
    for triangle in triangles:
        plt.fill(*zip(*triangle), 'lightblue', edgecolor='black', alpha=0.5)

    plt.title("Obtained Triangulation from the Art-Gallery")
    plt.axis('equal')
    plt.grid()
    plt.legend()
    plt.show()

    # Construct the dual graph
    dual_graph = nx.Graph()
    for i, triangle in enumerate(triangles):
        dual_graph.add_node(i)  # Add triangle as a node
        for j in range(3):
            edge = tuple(sorted((triangle[j], triangle[(j + 1) % 3]))) # Each edge of the triangle
            # print(edge)
            # input()
            for k in range(i + 1, len(triangles)):  # Compare with other triangles
                # Check if they share an edge
                a = [(triangles[k][j], triangles[k][(j+1)%3]) for j in range(3)]
                for ix in a:
                    # print(f"Edge : {edge}, current matched edge : {ix}")
                    if edge == ix or edge == ix[::-1]:
                        dual_graph.add_edge(i, k)  # Add edge between dual nodes
                    #     print("Matched")
                    # input()

    # Plot the dual graph
    pos = nx.spring_layout(dual_graph)  # Positioning for the nodes
    nx.draw(dual_graph, pos, with_labels=True, node_color='red', edge_color='black', node_size=500)
    plt.title("Dual Graph of the Inner Triangulated Art-Gallery Problem")
    plt.axis('equal')
    plt.grid()
    plt.legend()
    plt.show()


if __name__ =="__main__":
    main()