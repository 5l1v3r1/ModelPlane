from OpenGL.GL import *

from modelplane.gfx.util.color import Color


class Scene:

    _DEFAULT_COLOR = Color(0.24, 0.25, 0.27, 1.0)

    def __init__(self, bg_color=_DEFAULT_COLOR):
        self.color = bg_color
        self.shapes = []
        self.selected_shape = None

    def add_shape(self, shape):
        if shape is not None:
            self.shapes.append(shape)

    def remove_shape(self, shape):
        if shape is not None:
            self.shapes.remove(shape)

    def shape_count(self):
        return len(self.shapes)

    def render(self, shader, view_matrix):
        glClearColor(self.color.r, self.color.g, self.color.b, self.color.a)

        for shape in self.shapes:
            shader['u_modelview'] = view_matrix * shape.model_matrix()
            shape.render()
