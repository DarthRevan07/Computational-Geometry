

class Face:
    """Implements a face of a 2D dcel"""

    def __init__(self):
        self.wedge = None
        self.data = None
        self.external = None

    def __repr__(self):
        return f"Face(external={self.external})"


    def area(self):
        h = self.wedge
        a = 0
        while(not h.nexthedge is self.wedge):
            p1 = h.origin
            p2 = h.nexthedge.origin
            a += p1.x*p2.y - p2.x*p1.y
            h = h.nexthedge

        p1 = h.origin
        p2 = self.wedge.origin
        a = (a + p1.x*p2.y - p2.x*p1.y)/2
        return a

    def perimeter(self):
        h = self.wedge
        p = 0
        while (not h.nexthedge is self.wedge):
            p += h.length
            h = h.nexthedge
        return p

    def vertexlist(self):
        h = self.wedge
        pl = [h.origin]
        while (not h.nexthedge is self.wedge):
            h = h.nexthedge
            pl.append(h.origin)
        return pl

    def isinside(self, p):
        """Determines whether a point is inside a face"""

        h = self.wedge
        inside = False
        if lefton(h, p):
            while (not h.nexthedge is self.wedge):
                h = h.nexthedge
                if not lefton(h, p):
                    return False
            return True
        else:
            return False

def lefton(hedge, point):
    """Determines if a point is to the left of a hedge"""

    return area2(hedge, point) >= 0


def area2(hedge, point):
    """Determines the area of the triangle formed by a hedge and
    an external point"""

    pa = hedge.twin.origin
    pb=hedge.origin
    pc=point
    return (pb.x - pa.x)*(pc[1] - pa.y) - (pc[0] - pa.x)*(pb.y - pa.y)