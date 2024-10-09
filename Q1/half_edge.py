import math as m

class HalfEdge:
    """Class implementation of a half-edge of a 2D dcel"""

    def __init__(self,v1,v2):
        #The origin is defined as the vertex that the edge emanates from
        self.origin = v1
        self.twin = None

        # Points to the face on the left of the half-edge
        self.face = None
        self.angle = hangle(v2.x - v1.x, v2.y - v1.y)
        # The next and the previous half-edge objects.
        self.nexthedge = None
        self.prevhedge = None

    def __repr__(self):
        return f"HalfEdge(from={self.origin}, to={self.twin.origin}, next={self.nexthedge.origin}, prev={self.prevhedge.origin}, face={self.face})"

    def __lt__(self, other):
        """Less than comparison based on angle."""
        return self.angle < other.angle


def hangle(dx,dy):
    """Determines the angle with respect to the x axis of a segment
    of coordinates dx and dy
    """

    l = m.sqrt(dx*dx + dy*dy)
    if dy > 0:
        return m.acos(dx/l)
    else:
        return 2*m.pi - m.acos(dx/l)