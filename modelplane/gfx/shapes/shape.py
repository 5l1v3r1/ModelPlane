import numpy
from pyrr import matrix44, Matrix44, aabb, Vector3
from OpenGL.GL import *
from math import radians

from modelplane.gfx.shader.shader import Shader
from modelplane.gfx.util.color import Color
from modelplane.gfx.util.error import gl_error_check

_DRAW_STYLES = [GL_STATIC_DRAW, GL_DYNAMIC_DRAW, GL_STREAM_DRAW]


class Shape:

    def __init__(self):
        self.color = Color(0.0, 0.0, 0.0)
        self.aabb = aabb.create_from_bounds([0.0, 0.0, 0.0], [0.5, 0.5, 0.5])
        self.translation_matrix = Matrix44.identity()
        self.scale_matrix = Matrix44.identity()
        self.rotation_matrix = Matrix44.identity()
        self.selected = False

    def render(self):
        self.render_self()

    def translate(self, x, y, z):
        self.translation_matrix = matrix44.create_from_translation(Vector3([x, y, z]))

    def rotate(self, xrot, yrot, zrot):
        xrot_mat = matrix44.create_from_x_rotation(radians(xrot))
        yrot_mat = matrix44.create_from_y_rotation(radians(yrot))
        zrot_mat = matrix44.create_from_z_rotation(radians(zrot))
        self.rotation_matrix = xrot_mat * yrot_mat * zrot_mat

    def scale(self, scale):
        if type(scale) == Matrix44:
            self.scale_matrix = scale
        else:
            self.scale_matrix = matrix44.create_from_scale(Vector3(scale))

    # Scale first, rotate, then translate
    # TODO CHECK AND MAKE SURE THIS MULTIPLICATION FOLLOWS THE ORDER ABOVE
    def model_matrix(self):
        return self.scale_matrix * self.rotation_matrix * self.translation_matrix

    def render_self(self):
        raise NotImplementedError("Abstract Shape Class does not implement 'render_self'")


class PrimitiveShape(Shape):

    def __init__(self, vertices, indices):
        super().__init__()

        self.vertices = numpy.array(vertices, numpy.float32)
        self.indices = numpy.array(indices, numpy.int32)
        self.vao = self._create_vao(self.vertices, self.indices, GL_DYNAMIC_DRAW)

    def render_self(self):
        glBindVertexArray(self.vao)
        ebo_offset = ctypes.c_void_p(0)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, ebo_offset)
        glBindVertexArray(0)

    @staticmethod
    def _create_vao(vertices, indices, draw_style):
        if vertices is None or indices is None or draw_style is None:
            raise ValueError("Shape's vertices, indices, and change rate cannot be None")

        if draw_style not in _DRAW_STYLES:
            raise ValueError('Draw style invalid')

        vao = glGenVertexArrays(1)  # Vertex array object - stores the vbo and ebo and will bind them automatically
        vbo = glGenBuffers(1)  # Vertex buffer object - stores vertices
        ebo = glGenBuffers(1)  # Element buffer object - stores the indices to the vertices to render

        glBindVertexArray(vao)

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, len(vertices) * sizeof(ctypes.c_float), vertices, draw_style)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * sizeof(ctypes.c_int32), indices, draw_style)

        vert_attr_idx = 0
        vert_size = 3  # x, y, z
        vert_data_type = GL_FLOAT
        vert_normalize = GL_FALSE
        stride = 6 * sizeof(ctypes.c_float)  # x, y, z, r, g, b
        pos_data_start = ctypes.c_void_p(0)

        glVertexAttribPointer(vert_attr_idx, vert_size, vert_data_type, vert_normalize, stride, pos_data_start)
        glEnableVertexAttribArray(vert_attr_idx)

        # TODO ATTRIBUTE ENGINE?

        color_attr_idx = 1
        color_size = 3  # r, g, b
        color_data_type = GL_FLOAT
        color_normalize = GL_FALSE
        stride = 6 * sizeof(ctypes.c_float)  # x, y, z, r, g, b
        color_data_start = ctypes.c_void_p(3 * sizeof(ctypes.c_float))

        glVertexAttribPointer(color_attr_idx, color_size, color_data_type, color_normalize, stride, color_data_start)
        glEnableVertexAttribArray(color_attr_idx)

        '''tex_attr_idx = 2
        tex_size = 2  # s, t
        tex_data_type = GL_FLOAT
        tex_normalize = GL_FALSE
        stride = 8 * sizeof(ctypes.c_float)  # x, y, z, r, g, b, s, t
        tex_data_start = ctypes.c_void_p(6 * sizeof(ctypes.c_float))

        glVertexAttribPointer(tex_attr_idx, tex_size, tex_data_type, tex_normalize, stride, tex_data_start)
        glEnableVertexAttribArray(tex_attr_idx)'''

        # Unbind all buffers
        glBindVertexArray(0)

        gl_error_check()

        return vao


class HierarchicalShape(Shape):

    def __init__(self):
        super().__init__()
        self.child_shapes = []

    def render_self(self):
        for child in self.child_shapes:
            child.render()

    def add_child(self, child):
        if child:
            self.child_shapes.append(child)

    def remove_child(self, child):
        if child:
            self.child_shapes.remove(child)
