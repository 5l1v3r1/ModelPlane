from pyrr import Vector3, Matrix44, vector4

from modelplane.gfx.trackball import Trackball


class Camera:

    _DEFAULT_POSITION = Vector3([0.0, 0.0, 0.0])
    _DEFAULT_DISTANCE = 2.0

    def __init__(self, position=_DEFAULT_POSITION, distance=_DEFAULT_DISTANCE):
        self.distance = distance
        self.position = position
        self.trackball = Trackball(theta=0, distance=self.distance)

    def translate(self, x, y, z):
        self.position += [x, y, z]

    def matrix(self):
        return Matrix44(self.trackball.matrix)
