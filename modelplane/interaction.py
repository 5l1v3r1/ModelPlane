import math

import glfw

from OpenGL.GL import *
from pyrr import Matrix44

from modelplane.camera import Camera

_MAX_KEYS = 1024
_MAX_MOUSE_BUTTONS = 32


class Interaction:

    def __init__(self, window):
        if not window:
            raise ValueError('Interaction window is None')

        self._key_pressed = [False] * _MAX_KEYS
        self._mb_pressed = [False] * _MAX_MOUSE_BUTTONS

        self.cameras = [Camera()]
        self.active_camera = 0
        self.zoom_sensitivity = 0.1
        self.xmove_sensitivity = 0.20
        self.ymove_sensitivity = 0.20

        self.last_frame = 0.0
        self.delta_time = 0.0

        self.window = window

        # current mouse location
        self.mouse_location = None
        self.callbacks = {}

        self._register()

    def _register(self):
        glfw.set_mouse_button_callback(self.window, self._handle_mouse_button)
        glfw.set_key_callback(self.window, self._handle_key)
        glfw.set_scroll_callback(self.window, self._handle_scroll_wheel)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)  # TODO ???
        glfw.set_cursor_pos_callback(self.window, self._handle_mouse_move)

    def translate(self, x, y, z):
        self.cameras[self.active_camera].translate(x, y, z)

    def camera(self):
        return self.cameras[self.active_camera]

    def matrix(self):
        return self.cameras[self.active_camera].matrix()

    def register_callback(self, call_by, action_func):
        if call_by and action_func:
            self.callbacks[call_by] = action_func
        else:
            raise ValueError('Attempt to register None callback')

    def _handle_key(self, window, key, scancode, action, mode):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, GL_TRUE)

        if key in range(len(self._key_pressed)):
            if action == glfw.PRESS:
                self._key_pressed[key] = True
            elif action == glfw.RELEASE:
                self._key_pressed[key] = False

    def _handle_mouse_button(self, window, button, action, mods):
        if button not in range(len(self._mb_pressed)):
            raise ValueError('Mouse button not supported')

        width, height = glfw.get_window_size(window)

        x, y = glfw.get_cursor_pos(window)
        y = height - y  # invert y coordinate because OpenGL is inverted

        self.mouse_location = (x, y)

        if action == glfw.PRESS:
            self._mb_pressed[button] = True
        elif action == glfw.RELEASE:
            self._mb_pressed[button] = False

    def _handle_scroll_wheel(self, window, xoff, yoff):
        cam_pos = self.camera().position

        if math.isclose(cam_pos[0], 0.0) and math.isclose(cam_pos[1], 0.0) and \
                math.isclose(cam_pos[2], self.camera().distance) and yoff > 0:
            return

        self.translate(0.0, 0.0, yoff * self.zoom_sensitivity)

    def _handle_mouse_move(self, window, x, y):
        width, height = glfw.get_window_size(window)

        if self._mb_pressed[glfw.MOUSE_BUTTON_MIDDLE] and self.camera().trackball is not None:
            dx = (x - self.mouse_location[0]) * self.xmove_sensitivity
            dy = (y - self.mouse_location[1]) * self.ymove_sensitivity
            x, y, dx, dy = self._wrap_around(window, width, height, x, y, dx, dy)
            self.camera().trackball.drag_to(self.mouse_location[0], self.mouse_location[1], dx, dy)

        self.mouse_location = (x, y)

    @staticmethod
    def _wrap_around(window, width, height, x, y, dx, dy):
        wrapped = False

        if x <= 0.0:
            x = width - 1.0
            wrapped = True
        elif x >= width:
            x = 0.0
            wrapped = True

        if y <= 0.0:
            y = height - 1.0
            wrapped = True
        elif y >= height:
            y = 0.0
            wrapped = True

        if wrapped:
            glfw.set_cursor_pos(window, x, y)
            dx = 0.0
            dy = 0.0

        return x, y, dx, dy

    def _trigger(self, call_by, *args, **kwargs):
        for action_func in self.callbacks[call_by]:
            action_func(*args, **kwargs)
