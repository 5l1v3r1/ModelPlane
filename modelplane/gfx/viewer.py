import glfw

from OpenGL.GL import *
from OpenGL.GLU import *
from pyrr import Matrix44, Vector4

from modelplane.gfx.shapes.cube import Cube
from modelplane.gfx.shader.shader import Shader
from modelplane.gfx.scene import Scene
from modelplane.interaction import Interaction
from modelplane.gfx.util.error import *


class Viewer:

    _DEFAULT_FOV = 70
    _DEFAULT_NEAR_PLANE = 0.1
    _DEFAULT_FAR_PLANE = 800.0

    def __init__(self, width, height, title):
        if not width or not height or width < 0 or height < 0:
            raise ValueError('Width and height should be 0 or more')

        if title is None:
            raise ValueError('Viewer needs to have a title')

        self._last_width = width - 1
        self._last_height = height - 1

        self._inverse_modelview = Matrix44().identity()
        self._modelview = Matrix44().identity()

        self._window = self._init_interface(width, height, title)
        self._init_opengl(width, height)
        self._scene = self._init_scene()
        self._interaction = self._init_interaction(self._window)
        self._shader = Shader('gfx/shader/viewer_shader.vert', 'gfx/shader/viewer_shader.frag')

    def main_loop(self):
        self._shader.use()

        while not glfw.window_should_close(self._window):
            glfw.poll_events()
            self._render()
            glfw.swap_buffers(self._window)

        self._shader.end_use()

        glfw.destroy_window(self._window)
        glfw.terminate()

    def _render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        width, height = glfw.get_window_size(self._window)

        # Prevent errors upon minimizing the window. Cannot just set to 1, as
        # errors will occur in the perspective projection matrix creation.
        if height == 0:
            return

        if width != self._last_width and height != self._last_height:
            self._shader['u_projection'] = Matrix44.perspective_projection(
                self._DEFAULT_FOV, float(width) / float(height), self._DEFAULT_NEAR_PLANE, self._DEFAULT_FAR_PLANE) * \
                Matrix44.from_translation(Vector4([0.0, 0.0, -self._interaction.camera().distance, 0.0]))
            self._last_width = width
            self._last_height = height

        current_model_view = Matrix44.from_translation(self._interaction.camera().position) * self._interaction.matrix()
        #self._modelview = current_model_view.T
        #self._inverse_modelview = self._modelview.inverse

        self._scene.render(self._shader, current_model_view)

    def _init_interface(self, width, height, title):
        if not width or not height or not title:
            raise ValueError('Interface initializing was passed None')

        if width < 0 or height < 0:
            raise ValueError('Width and height must be 0 or greater')

        glfw.set_error_callback(self._window_error_callback)

        if not glfw.init():
            sys.exit('Error: Failed to initialize GLFW.')

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        if 'darwin' in sys.platform:  # Mac platform
            glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

        window = glfw.create_window(width, height, title, None, None)

        if not window:
            glfw.terminate()
            sys.exit('Error: Failed to create GLFW window.')

        glfw.make_context_current(window)
        glfw.swap_interval(1)

        # Setup event callbacks
        glfw.set_window_size_callback(window, self._window_size_callback)

        return window

    @staticmethod
    def _init_opengl(width, height):
        if width < 0 or height < 0:
            raise ValueError('Width and height must be 0 or greater')
        glViewport(0, 0, width, height)
        glEnable(GL_DEPTH_TEST)
        gl_error_check()

    @staticmethod
    def _init_scene():
        cube = Cube()

        scene = Scene()
        scene.add_shape(cube)

        return scene

    @staticmethod
    def _init_interaction(window):
        if not window:
            raise ValueError('Interaction window is None')

        return Interaction(window)

    def _window_size_callback(self, window, width, height):
        if window is None or width < 0 or height < 0:
            return
        glViewport(0, 0, width, height)
        self._shader['u_projection'] = Matrix44.perspective_projection(
            self._DEFAULT_FOV, float(width) / float(height), self._DEFAULT_NEAR_PLANE, self._DEFAULT_FAR_PLANE) * \
            Matrix44.from_translation(Vector4([0.0, 0.0, -self._interaction.camera().distance, 0.0]))
        self._last_width = width
        self._last_height = height

    def _window_error_callback(self, issue, info):
        glfw.destroy_window(self._window)
        glfw.terminate()
        sys.exit(f'Error {issue}: {info}')
