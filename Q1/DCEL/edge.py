class Edge:
    def __init__(self, auxData=None):
        self.data = auxData
        self.twin = None
        self.origin = None
        self.face = None
        self.next = None
        self.prev = None

    def __hash__(self):
        return hash(id(self))

    def getTwin(self):
        return self.twin

    def setTwin(self, twin):
        self.twin = twin

    def getData(self):
        return self.data

    def setData(self, auxData):
        self.data = auxData

    def getNext(self):
        return self.next

    def setNext(self, edge):
        self.next = edge

    def getOrigin(self):
        return self.origin

    def setOrigin(self, v):
        self.origin = v

    def getPrev(self):
        return self.prev

    def setPrev(self, edge):
        self.prev = edge
    def getDest(self):
        return self.twin.origin

    def getFace(self):
        return self.face

    def getFaceBoundary(self):
        visited = set()
        bound = []
        here = self
        while here and here not in visited:
            bound.append(here)
            visited.add(here)
            here = here.getNext()
        return bound

    def setFace(self, face):
        self.face = face

    def clone(self):
        c = Edge()
        c.data,c.twin,c.origin,c.face,c.next,c.prev = self.data,self.twin,self.origin,self.face,self.next,self.prev

    def __repr__(self):
        return 'DCEL.Edge from Origin: DCEL.Point with coordinates (' + str(self.getOrigin().coords[0])+','+str(self.getOrigin().coords[1])+')' + '\nDestination: DCEL.Point with coordinates (' + str(self.getDest().coords[0])+','+str(self.getDest().coords[1])+')'