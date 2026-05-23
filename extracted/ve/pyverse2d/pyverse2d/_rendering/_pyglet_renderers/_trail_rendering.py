# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...asset import Image, Color
from ..._rendering import Pipeline
from ...math.easing import EasingFunc

from collections import deque
from typing import ClassVar

import pyglet
import pyglet.gl as gl
from pyglet.graphics import Group
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.gl import (
    glBindTexture, glTexParameteri,
    GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T,
    GL_CLAMP_TO_EDGE, GL_REPEAT,
)

import math

# ======================================== CONSTANTS ========================================
_UNSET: object = object()

# ======================================== SHADERS ========================================
_VERT_COLOR = """
#version 330 core
layout(location = 0) in vec2 in_position;
layout(location = 1) in vec4 in_color;
out vec4 v_color;
uniform mat4 u_mvp;
void main() {
    gl_Position = u_mvp * vec4(in_position, 0.0, 1.0);
    v_color = in_color;
}
"""

_FRAG_COLOR = """
#version 330 core
in vec4 v_color;
out vec4 out_color;
void main() {
    out_color = v_color;
}
"""

_VERT_TEX = """
#version 330 core
layout(location = 0) in vec2 in_position;
layout(location = 1) in vec2 in_uv;
layout(location = 2) in float in_alpha;
out vec2 v_uv;
out float v_alpha;
uniform mat4 u_mvp;
void main() {
    gl_Position = u_mvp * vec4(in_position, 0.0, 1.0);
    v_uv = in_uv;
    v_alpha = in_alpha;
}
"""

_FRAG_TEX = """
#version 330 core
uniform sampler2D u_texture;
uniform vec3 u_tint;
in vec2 v_uv;
in float v_alpha;
out vec4 out_color;
void main() {
    vec4 tex = texture(u_texture, v_uv);
    out_color = vec4(tex.rgb * u_tint, tex.a * v_alpha);
}
"""

# ======================================== DRAW GROUP ========================================
class _TrailGroup(Group):
    """Group pyglet qui exécute le draw de la trail au bon moment dans le batch"""

    __slots__ = ("_renderer",)

    def __init__(self, renderer: PygletTrailRenderer, order: int, parent: Group | None) -> None:
        super().__init__(order=order, parent=parent)
        self._renderer: PygletTrailRenderer = renderer

    def set_state(self) -> None:
        self._renderer._raw_draw()

    def unset_state(self) -> None:
        gl.glBindVertexArray(0)
        gl.glUseProgram(0)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, _TrailGroup)
            and self._renderer is other._renderer
            and self._order == other._order
            and self.parent == other.parent
        )

    def __hash__(self) -> int:
        return hash((id(self._renderer), self._order, self.parent))

# ======================================== RENDERER ========================================
class PygletTrailRenderer:
    """Renderer bas niveau pour un ``TrailRenderer``

    Args:
        max_points: bucket de points
        image: texture de la trail *(couleur unie si None)*
        color: couleur RGBA *(mode couleur unie)*
        opacity: opacité globale [0.0 ; 1.0]
        width: largeur maximale en unités monde
        duration: durée de vie des points en secondes
        width_easing: courbe de largeur *(None = largeur fixe)*
        opacity_easing: courbe d'opacité *(None = opacité fixe)*
        tiling: texture en carrelage étirée
        tile_size: longueur en unités monde d'une répétition *(ignoré si tiling=False)*
        z: z-order dans le batch du layer courant
        pipeline: pipeline de rendu
    """
    __slots__ = (
        "_image", "_color", "_opacity",
        "_width", "_duration",
        "_width_easing", "_opacity_easing",
        "_tiling", "_tile_size",
        "_z", "_pipeline",
        "_vao", "_vbo",
        "_textured", "_texture_id",
        "_max_verts", "_vertex_count",
        "_floats_per_vert",
        "_visible",
        "_group", "_anchor_vlist",
    )

    _color_program: ClassVar[ShaderProgram | None] = None
    _tex_program:   ClassVar[ShaderProgram | None] = None
    _texture_cache: ClassVar[dict[str, int]] = {}

    @classmethod
    def _get_color_program(cls) -> ShaderProgram:
        if cls._color_program is None:
            cls._color_program = ShaderProgram(
                Shader(_VERT_COLOR, 'vertex'),
                Shader(_FRAG_COLOR, 'fragment'),
            )
        return cls._color_program

    @classmethod
    def _get_tex_program(cls) -> ShaderProgram:
        if cls._tex_program is None:
            cls._tex_program = ShaderProgram(
                Shader(_VERT_TEX, 'vertex'),
                Shader(_FRAG_TEX, 'fragment'),
            )
        return cls._tex_program

    @classmethod
    def _load_texture(cls, path: str, tiling: bool) -> int:
        """Charge (ou retourne depuis le cache) une texture GL depuis un chemin

        Args:
            path: chemin du fichier image
            tiling: active GL_REPEAT sur les deux axes

        Returns:
            identifiant GL de la texture
        """
        cache_key = f"{path}|{'repeat' if tiling else 'clamp'}"
        if cache_key in cls._texture_cache:
            return cls._texture_cache[cache_key].id

        try:
            img = pyglet.image.load(path)
            texture = img.get_texture()
            wrap_mode = GL_REPEAT if tiling else GL_CLAMP_TO_EDGE
            glBindTexture(GL_TEXTURE_2D, texture.id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_mode)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_mode)
            glBindTexture(GL_TEXTURE_2D, 0)
            cls._texture_cache[cache_key] = texture
            return texture.id
        except Exception as e:
            print(f"[PygletTrailRenderer] Cannot load texture: {path} ({e})")
            return 0

    def __init__(
        self,
        max_points: int,
        image: Image | None = None,
        color: Color = None,
        opacity: float = 1.0,
        width: float = 1.0,
        duration: float = 1.0,
        width_easing: EasingFunc | None = None,
        opacity_easing: EasingFunc | None = None,
        tiling: bool = True,
        tile_size: float = 0.1,
        z: int = 0,
        pipeline: Pipeline = None,
    ) -> None:
        # Attributs publiques
        self._image: Image | None = image
        self._color: Color = color
        self._opacity: float = opacity
        self._width: float = width
        self._duration: float = duration
        self._width_easing: EasingFunc | None = width_easing
        self._opacity_easing: EasingFunc | None = opacity_easing
        self._tiling: bool = tiling
        self._tile_size: float = max(tile_size, 1e-3)
        self._z: int = z
        self._pipeline: Pipeline = pipeline

        # Attributs internes
        self._vertex_count: int = 0
        self._visible: bool = True
        self._max_verts: int = max_points * 2

        self._group: _TrailGroup | None = None
        self._anchor_vlist: object | None = None

        # Construction
        self._build()

    # ======================================== BUILD ========================================
    def _build(self) -> None:
        """Alloue le VAO/VBO, configure les attributs, et s'enregistre dans le batch"""
        self._textured: bool = self._image is not None
        self._texture_id: int = self._load_texture(self._image.path, self._tiling) if self._image is not None else 0
        self._floats_per_vert: int = 5 if self._textured else 6

        # VAO / VBO
        self._vao = (gl.GLuint * 1)()
        self._vbo = (gl.GLuint * 1)()
        gl.glGenVertexArrays(1, self._vao)
        gl.glGenBuffers(1, self._vbo)
        gl.glBindVertexArray(self._vao[0])
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo[0])

        stride = self._floats_per_vert * 4
        total_bytes = self._max_verts * stride
        gl.glBufferData(gl.GL_ARRAY_BUFFER, total_bytes, None, gl.GL_DYNAMIC_DRAW)

        if self._textured:
            # x, y, u, v, alpha
            gl.glEnableVertexAttribArray(0)
            gl.glVertexAttribPointer(0, 2, gl.GL_FLOAT, gl.GL_FALSE, stride, 0)
            gl.glEnableVertexAttribArray(1)
            gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, stride, 8)
            gl.glEnableVertexAttribArray(2)
            gl.glVertexAttribPointer(2, 1, gl.GL_FLOAT, gl.GL_FALSE, stride, 16)
        else:
            # x, y, r, g, b, a
            gl.glEnableVertexAttribArray(0)
            gl.glVertexAttribPointer(0, 2, gl.GL_FLOAT, gl.GL_FALSE, stride, 0)
            gl.glEnableVertexAttribArray(1)
            gl.glVertexAttribPointer(1, 4, gl.GL_FLOAT, gl.GL_FALSE, stride, 8)

        gl.glBindVertexArray(0)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

        # Intégration dans le batch via un _TrailGroup
        self._group = _TrailGroup(
            renderer=self,
            order=self._z,
            parent=self._pipeline.get_group(z=self._z),
        )
        prog = pyglet.shapes.get_default_shader()
        self._anchor_vlist = prog.vertex_list(
            3,
            gl.GL_TRIANGLES,
            batch=self._pipeline.batch,
            group=self._group,
            position=('f', [0.0, 0.0] * 3),
            colors=('Bn', (0, 0, 0, 0) * 3),
        )

    def _rebuild(self) -> None:
        """Détruit le VAO/VBO et l'ancre batch existants puis reconstruit"""
        if self._anchor_vlist is not None:
            self._anchor_vlist.delete()
            self._anchor_vlist = None
        gl.glDeleteVertexArrays(1, self._vao)
        gl.glDeleteBuffers(1, self._vbo)
        self._vertex_count = 0
        self._build()

    def _rebuild_group(self) -> None:
        """Recrée uniquement le group + l'ancre batch (changement de z ou pipeline)"""
        if self._anchor_vlist is not None:
            self._anchor_vlist.delete()
        self._group = _TrailGroup(
            renderer=self,
            order=self._z,
            parent=self._pipeline.get_group(z=self._z),
        )
        prog = pyglet.shapes.get_default_shader()
        self._anchor_vlist = prog.vertex_list(
            3,
            gl.GL_TRIANGLES,
            batch=self._pipeline.batch,
            group=self._group,
            position=('f', [0.0, 0.0] * 3),
            colors=('Bn', (0, 0, 0, 0) * 3),
        )

    # ======================================== GETTERS ========================================
    @property
    def image(self) -> Image | None: return self._image
    @property
    def color(self) -> Color: return self._color
    @property
    def opacity(self) -> float: return self._opacity
    @property
    def width(self) -> float: return self._width
    @property
    def duration(self) -> float: return self._duration
    @property
    def width_easing(self) -> EasingFunc | None: return self._width_easing
    @property
    def opacity_easing(self) -> EasingFunc | None: return self._opacity_easing
    @property
    def tiling(self) -> bool: return self._tiling
    @property
    def tile_size(self) -> float: return self._tile_size
    @property
    def z(self) -> int: return self._z
    @property
    def pipeline(self) -> Pipeline: return self._pipeline
    @property
    def textured(self) -> bool: return self._textured

    # ======================================== VISIBILITY ========================================
    @property
    def visible(self) -> bool:
        """Visibilité"""
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        self._visible = value
        if self._group is not None:
            self._group.visible = value

    # ======================================== LIFE CYCLE ========================================
    def update(self, points: deque[tuple[float, float, float]], **kwargs) -> None:
        """Met à jour le mesh et uploade au GPU.

        Args:
            points: buffer de points courant *(x, y, age)*
            image: nouvelle texture *(None = couleur unie)*
            color: couleur RGBA
            opacity: opacité globale [0.0 ; 1.0]
            width: largeur en unités monde
            duration: durée de vie des points en secondes
            width_easing: courbe de largeur *(None = fixe)*
            opacity_easing: courbe d'opacité *(None = fixe)*
            tiling: active le carrelage de texture
            tile_size: taille d'une tuile en unités monde
            z: z-order dans le batch
            pipeline: pipeline de rendu
        """
        changes: set[str] = set()
        for key, value in kwargs.items():
            current = getattr(self, f"_{key}", _UNSET)
            if current is _UNSET or value == current:
                continue
            setattr(self, f"_{key}", value)
            changes.add(key)

        rebuild = False
        rebuild_group = False
        for key in changes:
            handler = getattr(self, f"_handle_{key}", None)
            if handler:
                result = handler()
                if result == "rebuild":
                    rebuild = True
                elif result == "rebuild_group":
                    rebuild_group = True

        if rebuild:
            self._rebuild()
        elif rebuild_group:
            self._rebuild_group()

        self._upload_mesh(points)

    def delete(self) -> None:
        """Libère les ressources GPU"""
        if self._anchor_vlist is not None:
            self._anchor_vlist.delete()
            self._anchor_vlist = None
        gl.glDeleteVertexArrays(1, self._vao)
        gl.glDeleteBuffers(1, self._vbo)

    # ======================================== HANDLERS ========================================
    def _handle_image(self) -> str | None:
        """Changement d'image"""
        was_textured = self._textured
        will_be_textured = self._image is not None
        if was_textured != will_be_textured:
            return "rebuild"
        self._texture_id = self._load_texture(self._image.path, self._tiling) if self._image is not None else 0
        return None

    def _handle_tiling(self) -> None:
        """Changement de mode tiling : recharge la texture avec le bon wrap"""
        if self._image is not None:
            self._texture_id = self._load_texture(self._image.path, self._tiling)

    def _handle_tile_size(self) -> None:
        self._tile_size = max(self._tile_size, 1e-3)

    def _handle_z(self) -> str:
        """Changement de z-order : recrée le group et l'ancre dans le batch"""
        return "rebuild_group"

    def _handle_pipeline(self) -> str:
        """Changement de pipeline : recrée le group et l'ancre dans le nouveau batch"""
        return "rebuild_group"

    # ======================================== MESH ========================================
    def _upload_mesh(self, points: deque[tuple[float, float, float]]) -> None:
        """Reconstruit le mesh depuis le buffer de points et uploade au GPU"""
        pt_list = list(points)
        n = len(pt_list)

        if n < 2:
            self._vertex_count = 0
            return

        # Longueurs cumulées
        lengths: list[float] = [0.0]
        for i in range(1, n):
            ax, ay = pt_list[i-1][0], pt_list[i-1][1]
            bx, by = pt_list[i][0], pt_list[i][1]
            dx, dy = bx - ax, by - ay
            lengths.append(lengths[-1] + math.sqrt(dx*dx + dy*dy))
        total_length = lengths[-1] if lengths[-1] > 1e-6 else 1.0

        cr, cg, cb = self._color.rgb
        fpv = self._floats_per_vert
        buf = (gl.GLfloat * (self._max_verts * fpv))()
        vi = 0

        for i, pt in enumerate(pt_list):
            if vi >= self._max_verts:
                break

            px, py, age = pt[0], pt[1], pt[2]
            nx, ny = _normal_at(pt_list, i)

            t_life = max(0.0, min(1.0, 1.0 - age / self._duration))
            hw = self._width * 0.5 * (self._width_easing(t_life) if self._width_easing else 1.0)

            lx, ly = px + nx * hw, py + ny * hw
            rx, ry = px - nx * hw, py - ny * hw

            u = lengths[i] / self._tile_size if self._tiling else lengths[i] / total_length
            alpha = (self._opacity_easing(t_life) if self._opacity_easing else 1.0) * self._opacity

            if self._textured:
                buf[vi * fpv + 0] = lx; buf[vi * fpv + 1] = ly
                buf[vi * fpv + 2] = u; buf[vi * fpv + 3] = 0.0
                buf[vi * fpv + 4] = alpha
                vi += 1
                buf[vi * fpv + 0] = rx; buf[vi * fpv + 1] = ry
                buf[vi * fpv + 2] = u; buf[vi * fpv + 3] = 1.0
                buf[vi * fpv + 4] = alpha
                vi += 1
            else:
                for vx, vy in ((lx, ly), (rx, ry)):
                    buf[vi * fpv + 0] = vx; buf[vi * fpv + 1] = vy
                    buf[vi * fpv + 2] = cr; buf[vi * fpv + 3] = cg
                    buf[vi * fpv + 4] = cb; buf[vi * fpv + 5] = alpha
                    vi += 1

        self._vertex_count = vi

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo[0])
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, vi * fpv * 4, buf)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    # ======================================== RAW DRAW ========================================
    def _raw_draw(self) -> None:
        """Appelé par _TrailGroup.set_state() lors du flush du batch"""
        if not self._visible or self._vertex_count < 2:
            return

        mvp = self._pipeline.full_matrix

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glBindVertexArray(self._vao[0])

        if self._textured:
            prog = self._get_tex_program()
            prog.use()
            prog['u_mvp'] = mvp
            prog['u_tint'] = self._color.rgb
            prog['u_texture'] = 0
            gl.glActiveTexture(gl.GL_TEXTURE0)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self._texture_id)
        else:
            prog = self._get_color_program()
            prog.use()
            prog['u_mvp'] = mvp

        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, self._vertex_count)

# ======================================== HELPERS ========================================
def _catmull_rom(
    p0: tuple, p1: tuple, p2: tuple, p3: tuple, t: float,
) -> tuple[float, float, float, float, float]:
    """Évalue position + normale analytique sur une spline Catmull-Rom

    Returns:
        ``(x, y, age, nx, ny)`` avec (nx, ny) normale normalisée
    """
    t2 = t * t
    t3 = t2 * t

    x = 0.5 * (
        (2*p1[0]) +
        (-p0[0] + p2[0]) * t +
        (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0]) * t2 +
        (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0]) * t3
    )
    y = 0.5 * (
        (2*p1[1]) +
        (-p0[1] + p2[1]) * t +
        (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1]) * t2 +
        (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1]) * t3
    )

    tx = 0.5 * (
        (-p0[0] + p2[0]) +
        2 * (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0]) * t +
        3 * (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0]) * t2
    )
    ty = 0.5 * (
        (-p0[1] + p2[1]) +
        2 * (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1]) * t +
        3 * (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1]) * t2
    )

    ln = math.sqrt(tx * tx + ty * ty)
    if ln > 1e-6:
        tx /= ln
        ty /= ln

    nx, ny = -ty, tx
    age = p1[2] + (p2[2] - p1[2]) * t
    return x, y, age, nx, ny


def _perpendicular(ax: float, ay: float, bx: float, by: float) -> tuple[float, float]:
    """Vecteur perpendiculaire normalisé entre deux points"""
    dx, dy = bx - ax, by - ay
    length = math.sqrt(dx * dx + dy * dy)
    if length < 1e-6:
        return 0.0, 1.0
    return -dy / length, dx / length


def _normal_at(pt_list: list, i: int) -> tuple[float, float]:
    """Normale moyennée aux segments adjacents pour une polyline brute"""
    n = len(pt_list)
    if i == 0:
        return _perpendicular(
            pt_list[0][0], pt_list[0][1],
            pt_list[1][0], pt_list[1][1],
        )
    if i == n - 1:
        return _perpendicular(
            pt_list[-2][0], pt_list[-2][1],
            pt_list[-1][0], pt_list[-1][1],
        )
    nx1, ny1 = _perpendicular(
        pt_list[i-1][0], pt_list[i-1][1],
        pt_list[i][0], pt_list[i][1],
    )
    nx2, ny2 = _perpendicular(
        pt_list[i][0], pt_list[i][1],
        pt_list[i+1][0], pt_list[i+1][1],
    )
    nx, ny = (nx1 + nx2) * 0.5, (ny1 + ny2) * 0.5
    ln = math.sqrt(nx * nx + ny * ny)
    if ln > 1e-6:
        nx, ny = nx / ln, ny / ln
    return nx, ny

# ======================================== EXPORTS ========================================
__all__ = [
    "PygletTrailRenderer",
]