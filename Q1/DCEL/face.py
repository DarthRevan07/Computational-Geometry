class Face:
    def __init__(self, auxData=None):
        self.data = auxData
        self.outer = None
        self.inner = set()
        self.isolated = set()

    def __hash__(self):
        return hash(id(self))

    def getOuterComponent(self):
        return self.outer

    def setOuterComponent(self, edge):
        self.outer = edge

    def getData(self):
        return self.data

    def setData(self, auxData):
        self.data = auxData
    def getOuterBoundary(self):
        if self.outer:
            return self.outer.getFaceBoundary()
        else:
            return []

    def getOuterBoundaryCoords(self):
        original_pts = self.getOuterBoundary()
        return [x.origin.coords for x in original_pts]

    def getInnerComponents(self):
        return list(self.inner)

    def addInnerComponent(self, edge):
        self.inner.add(edge)

    def removeInnerComponent(self, edge):
        self.inner.discard(edge)

    def removeIsolatedVertex(self,Point):
        self.isolated.discard(Point)

    def getIsolatedVertices(self):
        return list(self.isolated)

    def addIsolatedVertex(self,Point):
        self.isolated.add(Point)