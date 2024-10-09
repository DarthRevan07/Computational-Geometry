import math as m
class Vertex:
    """Minimal implementation of a vertex of a 2D dcel"""

    def __init__(self, x_co, y_co):
        self.x = x_co
        self.y = y_co
        self.hedgelist = []

    def print_hedge(self):
        for i in self.hedgelist:
            print(i)
    def sortincident(self):
        self.hedgelist.sort(key=lambda h: h.angle, reverse = True)

    def __repr__(self):
        return f"Vertex({self.x}, {self.y})"


def hsort(h1, h2):
    """Sorts two half edges counterclockwise"""

    if h1.angle < h2.angle:
        return -1
    elif h1.angle > h2.angle:
        return 1
    else:
        return 0