# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._rendering import Pipeline, ImageLoader
from ...abc import ParticleEmitter

import pyglet.gl as gl
from pyglet.graphics.shader import Shader, ShaderProgram
import numpy as np

import ctypes
from typing import ClassVar

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

uniform mat4 u_mvp;

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
    gl_Position = u_mvp * vec4(world, 0.0, 1.0);
    v_local = in_corner;
    v_color = in_color;
}
"""

_FRAG_BLOB = """
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

_FRAG_TEX = """
#version 330 core
uniform sampler2D u_texture;
in vec2 v_local;
in vec4 v_color;
out vec4 out_color;

void main() {
    vec2 uv = v_local + 0.5;
    vec4 tex = texture(u_texture, uv);
    out_color = vec4(v_color.rgb * tex.rgb, v_color.a * tex.a);
}
"""

# ======================================== RENDERER ========================================
class ParticleRenderer:
    """Renderer de particules"""

    _program_blob: ClassVar[ShaderProgram] = None
    _program_tex: ClassVar[ShaderProgram] = None
    _vao: ClassVar[gl.GLuint] = None
    _quad_vbo: ClassVar[gl.GLuint] = None
    _inst_vbo: ClassVar[gl.GLuint] = None
    _inst_capacity: ClassVar[int] = 0

    @classmethod
    def _get_program_blob(cls) -> ShaderProgram:
        """Renvoie le programme de shader blob"""
        if cls._program_blob is None:
            cls._program_blob = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG_BLOB, 'fragment'))
        return cls._program_blob

    @classmethod
    def _get_program_tex(cls) -> ShaderProgram:
        """Renvoie le programme de shader texturé"""
        if cls._program_tex is None:
            cls._program_tex = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG_TEX, 'fragment'))
        return cls._program_tex

    @classmethod
    def _ensure_vao(cls) -> None:
        """Prépare les arrêtes pour le GPU"""
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
        """Passe les données au GPU

        Args:
            data: données à passer
        """
        count = len(data)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, cls._inst_vbo)
        if count > cls._inst_capacity:
            gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data.ctypes.data_as(ctypes.POINTER(gl.GLfloat)), gl.GL_DYNAMIC_DRAW)
            cls._inst_capacity = count
        else:
            gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, data.nbytes, data.ctypes.data_as(ctypes.POINTER(gl.GLfloat)))

    # ======================================== INTERFACE ========================================
    def render(self, pipeline: Pipeline, emitters: list[ParticleEmitter], blending: float) -> None:
        """Rendu instancié de toutes les particules

        Args:
            pipeline: Pipeline courant
            emitters: émetteurs à rendre
            blending: interpolation entre alpha classique et blending additif *[0, 1]*
        """
        # Grouper par texture
        groups: dict = {}
        for emitter in emitters:
            tex = emitter.particle.texture
            key = tex.path if tex is not None else None
            if key not in groups:
                groups[key] = (tex, [])
            r = emitter.collect()
            if r is not None:
                groups[key][1].append(r)

        if not any(chunks for _, chunks in groups.values()):
            return

        self._ensure_vao()

        gl.glEnable(gl.GL_BLEND)
        if blending >= 1.0:
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
        elif blending <= 0.0:
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        else:
            gl.glBlendFuncSeparate(
                gl.GL_SRC_ALPHA,
                gl.GL_ONE_MINUS_SRC_ALPHA,
                gl.GL_ONE,
                gl.GL_ONE_MINUS_SRC_ALPHA
            )

        gl.glBindVertexArray(ParticleRenderer._vao)

        for tex, chunks in groups.values():
            if not chunks:
                continue

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
            self._upload(data)

            if tex is None:
                program = self._get_program_blob()
                program.use()
            else:
                program = self._get_program_tex()
                program.use()
                gl.glActiveTexture(gl.GL_TEXTURE0)
                gl.glBindTexture(gl.GL_TEXTURE_2D, ImageLoader.get_id(tex.path))
                program['u_texture'] = 0

            program['u_mvp'] = pipeline.full_matrix
            gl.glDrawArraysInstanced(gl.GL_TRIANGLES, 0, 6, count)
            program.stop()

        gl.glBindVertexArray(0)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

# ======================================== EXPORTS ========================================
__all__ = [
    "ParticleRenderer",
]