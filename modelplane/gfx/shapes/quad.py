from modelplane.gfx.shapes.shape import PrimitiveShape


class Quad(PrimitiveShape):

    _DEFAULT_VERTICES = [0.5, 0.5, 0.0,   0.0, 0.0, 0.0,
                         0.5, -0.5, 0.0,  0.0, 0.0, 0.0,
                         -0.5, -0.5, 0.0, 0.0, 0.0, 0.0,
                         -0.5, 0.5, 0.0,  0.0, 0.0, 0.0]

    _DEFAULT_INDICES = [0, 1, 3,
                        1, 2, 3]

    def __init__(self, vertices=None, indices=None):
        if vertices is None:
            vertices = self._DEFAULT_VERTICES
        if indices is None:
            indices = self._DEFAULT_INDICES
        super().__init__(vertices, indices)
