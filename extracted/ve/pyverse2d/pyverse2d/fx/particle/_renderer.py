# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._rendering import Pipeline

from ...abc import ParticleEmitter

import ctypes
import numpy as np
import pyglet.gl as gl
from pyglet.graphics.shader import Shader, ShaderProgram

# ======================================== CONSTANTS ========================================
_QUAD = np.array([
    -0.5, -0.5, 0.5, -0.5,  0.5, 0.5,
    -0.5, -0.5, 0.5,  0.5, -0.5, 0.5,
], dtype=np.float32)

_STRIDE = 32

# ======================================== SHADERS ========================================
_VERT = """
#version 330 core
layout(location = 0) in vec2 in_corner;
layout(location = 1) in vec2 in_position;
layout(location = 2) in float in_rotation;
layout(location = 3) in float in_size;
layout(location = 4) in vec4 in_color;

uniform mat4 u_projection;
uniform mat4 u_view;

out vec2 v_local;
out vec4 v_color;

void main() {
    float c = cos(in_rotation);
    float s = sin(in_rotation);
    vec2 rotated = vec2(
        in_corner.x * c - in_corner.y * s,
        in_corner.x * s + in_corner.y * c
    );
    vec2 world = in_position + rotated * in_size;
    gl_Position = u_projection * u_view * vec4(world, 0.0, 1.0);
    v_local = in_corner;
    v_color = in_color;
}
"""

_FRAG = """
#version 330 core
in vec2 v_local;
in vec4 v_color;
out vec4 out_color;

void main() {
    float d = dot(v_local, v_local) * 4.0;
    float alpha = 1.0 - smoothstep(0.0, 1.0, d);
    out_color = vec4(v_color.rgb, v_color.a * alpha);
}
"""

# ======================================== RENDERER ========================================
class ParticleRenderer:
    """Renderer de particules"""

    _program: ShaderProgram = None
    _vao: gl.GLuint = None
    _quad_vbo: gl.GLuint = None
    _inst_vbo: gl.GLuint = None
    _inst_capacity: int = 0

    @classmethod
    def _get_program(cls) -> ShaderProgram:
        if cls._program is None:
            cls._program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG, 'fragment'))
        return cls._program

    @classmethod
    def _ensure_vao(cls) -> None:
        if cls._vao is not None:
            return

        cls._vao = gl.GLuint()
        gl.glGenVertexArrays(1, ctypes.byref(cls._vao))
        gl.glBindVertexArray(cls._vao)

        cls._quad_vbo = gl.GLuint()
        gl.glGenBuffers(1, ctypes.byref(cls._quad_vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, cls._quad_vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, _QUAD.nbytes, _QUAD.ctypes.data_as(ctypes.POINTER(gl.GLfloat)), gl.GL_STATIC_DRAW)
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))

        cls._inst_vbo = gl.GLuint()
        gl.glGenBuffers(1, ctypes.byref(cls._inst_vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, cls._inst_vbo)

        for loc, size, offset in [(1, 2, 0), (2, 1, 8), (3, 1, 12), (4, 4, 16)]:
            gl.glEnableVertexAttribArray(loc)
            gl.glVertexAttribPointer(loc, size, gl.GL_FLOAT, gl.GL_FALSE, _STRIDE, ctypes.c_void_p(offset))
            gl.glVertexAttribDivisor(loc, 1)

        gl.glBindVertexArray(0)

    @classmethod
    def _upload(cls, data: np.ndarray) -> None:
        count = len(data)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, cls._inst_vbo)
        if count > cls._inst_capacity:
            gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data.ctypes.data_as(ctypes.POINTER(gl.GLfloat)), gl.GL_DYNAMIC_DRAW)
            cls._inst_capacity = count
        else:
            gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, data.nbytes, data.ctypes.data_as(ctypes.POINTER(gl.GLfloat)))

    # ======================================== INTERFACE ========================================
    def render(self, pipeline: Pipeline, emitters: list[ParticleEmitter], additive: bool) -> None:
        """Rendu instancié de toutes les particules

        Args:
            pipeline: Pipeline courant
            emitters: émetteurs à rendre
            additive: blending additif ou alpha classique
        """
        chunks = [r for e in emitters if (r := e.collect()) is not None]
        if not chunks:
            return

        positions = np.concatenate([c[0] for c in chunks])
        rotations = np.concatenate([c[1] for c in chunks])
        sizes = np.concatenate([c[2] for c in chunks])
        colors = np.concatenate([c[3] for c in chunks])
        count = len(positions)

        data = np.empty((count, 8), dtype=np.float32)
        data[:, 0:2] = positions
        data[:, 2] = rotations
        data[:, 3] = sizes
        data[:, 4:8] = colors

        self._ensure_vao()
        self._upload(data)

        program = self._get_program()
        program.use()
        program['u_projection'] = pipeline.static_matrix
        program['u_view'] = pipeline.view_matrix

        gl.glEnable(gl.GL_BLEND)
        if additive:
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
        else:
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glBindVertexArray(ParticleRenderer._vao)
        gl.glDrawArraysInstanced(gl.GL_TRIANGLES, 0, 6, count)
        gl.glBindVertexArray(0)

        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        program.stop()