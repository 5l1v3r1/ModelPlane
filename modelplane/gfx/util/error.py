import inspect
import sys

from OpenGL.GL import *
from OpenGL.GLU import *


def gl_error_check():
    error_code = glGetError()
    if error_code != GL_NO_ERROR:
        caller_frame_record = inspect.stack()[1]  # line from caller
        frame = caller_frame_record[0]
        info = inspect.getframeinfo(frame)
        sys.exit(f'ERROR in {info.filename}, {info.function}, before {info.lineno}: '
                 f'OpenGL error: {gluErrorString(error_code)}')
