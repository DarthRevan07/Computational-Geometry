from Q1.DCEL.face import Face

class DCEL:
    def __init__(self):
        self.exterior = Face()
    def getExteriorFace(self):
        return self.exterior
    def getFaces(self):
        result = []
        known = set()
        temp = []
        temp.append(self.exterior)
        known.add(self.exterior)
        while temp:
            f = temp.pop(0)
            result.append(f)
            for e in f.getOuterBoundary():
                nb = e.getTwin().getFace()
                if nb and nb not in known:
                    known.add(nb)
                    temp.append(nb)
            for inner in f.getInnerComponents():
                for e in inner.getFaceBoundary():
                    nb = e.getTwin().getFace()
                    if nb and nb not in known:
                        known.add(nb)
                        temp.append(nb)
        return result

    def getEdges(self):
        edges = set()
        for f in self.getFaces():
            edges.update(f.getOuterBoundary())
            for inner in f.getInnerComponents():
                edges.update(inner.getFaceBoundary())
        return edges

    def getVertices(self):
        verts = set()
        for f in self.getFaces():
            verts.update(f.getIsolatedVertices())
            verts.update([e.getOrigin() for e in f.getOuterBoundary()])
            for inner in f.getInnerComponents():
                verts.update([e.getOrigin() for e in inner.getFaceBoundary()])
        return verts