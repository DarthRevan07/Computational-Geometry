import numpy as np
DEBUG = False

class Point:
    def __init__(self, coordinates,auxData=None):
        self.data=auxData
        self.coords = coordinates
        self.edge = None
        self.ear = False
        self.next = None
        self.prev = None
        self.color= -1

    def ___str___(self):
        return str(self.ID)

    def __getitem__(self,key):
        return self.coords[key]

    def scale(self, k1, k2):
        self.coords = list(self.coords)
        self.coords[0] = int(self.coords[0] * k1)
        self.coords[1] = int(self.coords[1] * k2)
        self.coords = tuple(self.coords)

    def __hash__(self):
        return hash(id(self))

    def getData(self):
        return self.data

    def setData(self, auxData):
        self.data = auxData

    def getCoords(self):
        return Point(self.coords)

    def setCoords(self, coordinates):
        self.coords = coordinates

    def getOutgoingEdges(self):
        visited = set()
        out = []
        here = self.edge
        while here and here not in visited:
            out.append(here)
            visited.add(here)
            temp = here.getTwin()
            if temp:
                here = temp.getNext()
            else:
                here = None
        return out

    def getIncidentEdge(self):
        return self.edge

    def setIncidentEdge(self, edge):
        self.edge = edge

    def __repr__(self):
        return 'DCEL.Point with coordnates (' + str(self.coords[0])+','+str(self.coords[1])+')'
