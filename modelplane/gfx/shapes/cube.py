from modelplane.gfx.shapes.shape import PrimitiveShape


class Cube(PrimitiveShape):
    vertices = [
        -0.5, 0.5, 0.5, 0.0, 1.0, 0.0,
        0.5, 0.5, 0.5, 0.0, 1.0, 0.0,
        -0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
        0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
        -0.5, 0.5, -0.5, 1.0, 0.0, 0.0,
        0.5, 0.5, -0.5, 1.0, 0.0, 0.0,
        -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
        0.5, -0.5, -0.5, 1.0, 0.0, 0.0
    ]

    indices = [
        0, 1, 3,  # Front face
        0, 2, 3,
        1, 7, 3,  # Right face
        1, 5, 7,
        4, 2, 0,  # Left face
        4, 6, 2,
        4, 6, 5,  # Back face
        5, 6, 7,
        0, 4, 5,  # Top face
        0, 1, 5,
        2, 6, 7,  # Bottom face
        2, 7, 3
    ]

    def __init__(self):
        super().__init__(self.vertices, self.indices)
