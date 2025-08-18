#! /usr/bin/env python3
import glfw
import OpenGL.GL as gl

glfw.init()
glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_ES_API)
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
window = glfw.create_window(640, 480, 'Binder', None, None)
assert window
glfw.make_context_current(window)

# gl.glDispatchCompute(1,1,1) will trigger this for instance
print(gl.extensions.GLQuerier.pullVersion())
