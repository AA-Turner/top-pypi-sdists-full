# ======================================== IMPORTS ========================================
from __future__ import annotations

import pyglet.gl as gl
from pyglet.graphics.shader import Shader, ShaderProgram
from ctypes import c_float, c_uint

# ======================================== VERTICES ========================================
# Positions NDC + UVs en un seul buffer interleaved (xy, uv)
_QUAD_DATA = (c_float * 16)(
    -1.0, -1.0,  0.0, 0.0,
     1.0, -1.0,  1.0, 0.0,
     1.0,  1.0,  1.0, 1.0,
    -1.0,  1.0,  0.0, 1.0,
)
_QUAD_INDICES = (c_uint * 6)(0, 1, 2, 2, 3, 0)

# ======================================== SHADER ========================================
_VERT_SRC = """
#version 330 core
layout(location = 0) in vec2 in_position;
layout(location = 1) in vec2 in_uv;
out vec2 v_uv;
void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
    v_uv = in_uv;
}
"""

_FRAG_SRC = """
#version 330 core
uniform sampler2D u_texture;
in vec2 v_uv;
out vec4 out_color;
void main() {
    out_color = texture(u_texture, v_uv);
}
"""

# ======================================== QUAD ========================================
class ScreenQuad:
    """Fullscreen quad pour blitter une texture sur le framebuffer principal"""
    __slots__ = ("_shader", "_vao", "_vbo", "_ebo")

    def __init__(self):
        # Shader
        vert = Shader(_VERT_SRC, "vertex")
        frag = Shader(_FRAG_SRC, "fragment")
        self._shader = ShaderProgram(vert, frag)

        # VAO
        self._vao = (gl.GLuint * 1)()
        self._vbo = (gl.GLuint * 1)()
        self._ebo = (gl.GLuint * 1)()
        gl.glGenVertexArrays(1, self._vao)
        gl.glGenBuffers(1, self._vbo)
        gl.glGenBuffers(1, self._ebo)

        gl.glBindVertexArray(self._vao[0])

        # VBO : positions + UVs interleaved
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo[0])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, 64, _QUAD_DATA, gl.GL_STATIC_DRAW)  # 16 floats * 4 bytes

        stride = 4 * 4  # 4 floats par vertex * 4 bytes
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 2, gl.GL_FLOAT, gl.GL_FALSE, stride, 0)
        gl.glEnableVertexAttribArray(1)
        gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, stride, 8)  # offset 2 floats

        # EBO
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._ebo[0])
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, 24, _QUAD_INDICES, gl.GL_STATIC_DRAW)  # 6 uints * 4 bytes

        gl.glBindVertexArray(0)

    # ======================================== INTERFACE ========================================
    def blit(self, texture_id: int) -> None:
        """Blit la texture donnée sur le framebuffer actuellement bindé"""
        self._shader.use()
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
        gl.glBindVertexArray(self._vao[0])
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, 0)
        gl.glBindVertexArray(0)

    def draw_raw(self) -> None:
        """Draw le quad sans toucher au shader"""
        gl.glBindVertexArray(self._vao[0])
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, 0)
        gl.glBindVertexArray(0)

    def delete(self) -> None:
        """Libère les ressources GPU"""
        gl.glDeleteVertexArrays(1, self._vao)
        gl.glDeleteBuffers(1, self._vbo)
        gl.glDeleteBuffers(1, self._ebo)
        del self._shader