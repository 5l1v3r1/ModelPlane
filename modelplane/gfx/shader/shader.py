import numpy

from pyrr import Matrix33, Matrix44

from modelplane.gfx.util.error import *


class Shader:

    def __init__(self, vert_shader_path, frag_shader_path):
        if vert_shader_path is None or frag_shader_path is None:
            sys.exit('Vertex or fragment shader path is None')

        vertex_shader = self._create_shader(vert_shader_path, GL_VERTEX_SHADER)
        fragment_shader = self._create_shader(frag_shader_path, GL_FRAGMENT_SHADER)

        self.program = glCreateProgram()

        if self.program == 0:
            sys.exit('ERROR: Failed to create program')

        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)

        glLinkProgram(self.program)
        gl_error_check()

        if glGetProgramiv(self.program, GL_LINK_STATUS, None) == GL_FALSE:
            info_log = glGetProgramInfoLog(self.program)
            sys.exit(f'ERROR: Failed to link GLSL program: {info_log}')

        info_log = glGetProgramInfoLog(self.program)

        if len(info_log) > 0:
            print(f'WARNING: GLSL program log: {info_log}')

        # No longer need the vertex and fragment shaders, as they are compiled into the program.
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

    @staticmethod
    def _create_shader(shader_file, shader_type):
        with open(shader_file, 'r') as f:
            shader_code = f.read()

        shader = glCreateShader(shader_type)
        glShaderSource(shader, shader_code)
        gl_error_check()

        glCompileShader(shader)

        info_log = glGetShaderInfoLog(shader)
        if len(info_log) > 0:
            print(f'WARNING: Shader log: {info_log}')

        if glGetShaderiv(shader, GL_COMPILE_STATUS, None) == GL_FALSE:
            sys.exit('ERROR: Failed to compile shader')

        gl_error_check()

        return shader

    def get_program(self):
        return self.program

    def attrib_location(self, attr):
        if attr is None:
            return -1
        return glGetAttribLocation(self.program, attr)

    def uniform_location(self, uniform):
        if uniform is None:
            return -1
        return glGetUniformLocation(self.program, uniform)

    def set_uniformi(self, uniform, *integers):
        if uniform is None or integers is None or len(integers) not in range(5):
            return

        location = self.uniform_location(uniform)

        if location < 0:
            return

        if len(integers) == 1:
            glUniform1i(location, *integers)
        elif len(integers) == 2:
            glUniform2i(location, *integers)
        elif len(integers) == 3:
            glUniform3i(location, *integers)
        else:
            glUniform4i(location, *integers)

    def set_uniformiv(self, uniform, vector):
        if uniform is None or vector is None:
            return

        location = self.uniform_location(uniform)

        if location < 0:
            return

        vector = numpy.array(vector, numpy.int32)
        glUniform1iv(location, vector)

    def set_uniformf(self, uniform, *floats):
        if uniform is None or floats is None or len(floats) not in range(5):
            return

        location = self.uniform_location(uniform)

        if location < 0:
            return

        if len(floats) == 1:
            glUniform1f(location, *floats)
        elif len(floats) == 2:
            glUniform2f(location, *floats)
        elif len(floats) == 3:
            glUniform3f(location, *floats)
        else:
            glUniform4f(location, *floats)

    def set_uniformfv(self, uniform, vector):
        if uniform is None or vector is None:
            return

        location = self.uniform_location(uniform)

        if location < 0:
            return

        vector = numpy.array(vector, numpy.float32)
        glUniform1fv(location, vector)

    def set_uniform_matrix3fv(self, uniform, matrix):
        if uniform is None or matrix is None:
            return

        location = self.uniform_location(uniform)

        if location < 0:
            return

        glUniformMatrix3fv(location, 1, GL_FALSE, matrix)

    def set_uniform_matrix4fv(self, uniform, matrix):
        if uniform is None or matrix is None:
            return

        location = self.uniform_location(uniform)

        if location < 0:
            return

        glUniformMatrix4fv(location, 1, GL_FALSE, matrix)

    def use(self):
        glUseProgram(self.program)

    @staticmethod
    def end_use():
        glUseProgram(0)

    def __setitem__(self, key, value):
        # Given name is a uniform within the shader
        if key is not None and value is not None and self.uniform_location(key) >= 0:
            if type(value) == Matrix44:
                self.set_uniform_matrix4fv(key, value)
            elif type(value) == Matrix33:
                self.set_uniform_matrix3fv(key, value)
            elif type(value) == list and len(value) > 0 and type(value[0]) == float:
                self.set_uniformfv(key, value)
            elif type(value) == list:
                self.set_uniformiv(key, value)
            elif type(value) == int:
                self.set_uniformi(key, value)
            else:
                self.set_uniformf(key, value)
        # Given name is an attribute within the shader
        elif key is not None and value is not None and self.attrib_location(key) >= 0:
            return
        else:
            raise ValueError(f"ERROR: Attempting to set '{key},' which is not in the shader")
