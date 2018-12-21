from modelplane.gfx.shapes.shape import PrimitiveShape


class Triangle(PrimitiveShape):
    _DEFAULT_VERTICES = [0.5, -0.5, 0.0,  0.0, 0.0, 0.0,
                         -0.5, -0.5, 0.0, 0.0, 0.0, 0.0,
                         0.0, 0.5, 0.0,   0.0, 0.0, 0.0]

    _DEFAULT_INDICES = [0, 1, 2]

    def __init__(self, vertices=_DEFAULT_VERTICES, indices=_DEFAULT_INDICES):
        super().__init__(vertices, indices)
