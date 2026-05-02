# ======================================== IMPORTS ========================================
from __future__ import annotations

import ctypes
import numpy as np
import pyglet.gl as gl
import pyglet.image
import pyglet.graphics.shader as shader_module

from ._tile_map import TileMap, FLIP_H, FLIP_V, FLIP_D

# ======================================== SHADER ========================================
_VERT_SRC = """
#version 330 core
layout(location = 0) in vec2 position;
layout(location = 1) in vec3 tex_coord;
out vec3 v_tex;

layout(std140) uniform WindowBlock {
    mat4 projection;
    mat4 view;
} window;

void main() {
    gl_Position = window.projection * window.view * vec4(position, 0.0, 1.0);
    v_tex = tex_coord;
}
"""

_FRAG_SRC = """
#version 330 core
in vec3 v_tex;
out vec4 out_color;
uniform sampler2DArray u_tiles;
void main() {
    out_color = texture(u_tiles, v_tex);
    if (out_color.a < 0.01) discard;
}
"""

_program: shader_module.ShaderProgram | None = None


def _get_program() -> shader_module.ShaderProgram:
    """Renvoie le shader program (singleton par contexte GL)"""
    global _program
    if _program is None:
        vert = shader_module.Shader(_VERT_SRC, 'vertex')
        frag = shader_module.Shader(_FRAG_SRC, 'fragment')
        _program = shader_module.ShaderProgram(vert, frag)
    return _program

# ======================================== TEXTURE ARRAY ========================================
class TileArrayTexture:
    """Texture array GL — une tranche par tile du tileset"""
    __slots__ = ("_tex_id", "_tile_to_layer")

    def __init__(self, image_path: str, src_tw: int, src_th: int, margin: int, spacing: int):
        self._tex_id: int | None = None
        self._tile_to_layer: dict[int, int] = {}
        self._build(image_path, src_tw, src_th, margin, spacing)

    # ======================================== BUILD ========================================
    def _build(self, image_path: str, src_tw: int, src_th: int, margin: int, spacing: int) -> None:
        """Charge la spritesheet et upload chaque tile dans une tranche dédiée"""
        try:
            img = pyglet.image.load(image_path)
        except FileNotFoundError:
            return

        img_w = img.width
        img_h = img.height
        stride_x = src_tw + spacing
        stride_y = src_th + spacing

        if spacing > 0:
            cols = max(1, (img_w - margin + spacing) // stride_x)
            rows = max(1, (img_h - margin + spacing) // stride_y)
        else:
            cols = max(1, (img_w - margin) // src_tw)
            rows = max(1, (img_h - margin) // src_th)

        n_tiles = cols * rows

        tex = gl.GLuint()
        gl.glGenTextures(1, ctypes.byref(tex))
        self._tex_id = tex.value

        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self._tex_id)
        gl.glTexImage3D(
            gl.GL_TEXTURE_2D_ARRAY, 0, gl.GL_RGBA8,
            src_tw, src_th, n_tiles,
            0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, None,
        )

        layer = 0
        for ts_row in range(rows):
            for ts_col in range(cols):
                tile_id = ts_row * cols + ts_col + 1
                x = margin + ts_col * stride_x
                y = margin + (rows - 1 - ts_row) * stride_y
                region = img.get_region(x, y, src_tw, src_th)
                data = region.get_image_data().get_data('RGBA', src_tw * 4)
                gl.glTexSubImage3D(
                    gl.GL_TEXTURE_2D_ARRAY, 0,
                    0, 0, layer,
                    src_tw, src_th, 1,
                    gl.GL_RGBA, gl.GL_UNSIGNED_BYTE,
                    data,
                )
                self._tile_to_layer[tile_id] = layer
                layer += 1

        gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, 0)

    # ======================================== INTERFACE ========================================
    def get_layer(self, tile_id: int) -> int:
        """Renvoie l'index de tranche pour un tile_id, ou -1 si inconnu"""
        return self._tile_to_layer.get(tile_id, -1)

    def bind(self, unit: int = 0) -> None:
        """Bind la texture array à l'unité de texture spécifiée"""
        gl.glActiveTexture(gl.GL_TEXTURE0 + unit)
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self._tex_id)

    def delete(self) -> None:
        """Libère la texture GL"""
        if self._tex_id is not None:
            tex = gl.GLuint(self._tex_id)
            gl.glDeleteTextures(1, ctypes.byref(tex))
            self._tex_id = None

# ======================================== TILE RENDERER ========================================
class TileRenderer:
    """Renderer interne pour TileLayer

    Args:
        tile_map(TileMap): couche source
        chunk_size(int): nombre de tuiles par côté de chunk
    """
    __slots__ = (
        "_tile_map", "_chunk_size",
        "_texture",
        "_vao", "_vbo",
        "_chunk_offsets",
        "_built",
    )

    def __init__(self, tile_map: TileMap, chunk_size: int):
        self._tile_map: TileMap = tile_map
        self._chunk_size: int = chunk_size
        self._texture: TileArrayTexture | None = None
        self._vao: int | None = None
        self._vbo: int | None = None
        self._chunk_offsets: dict[tuple[int, int], tuple[int, int]] = {}
        self._built: bool = False

    # ======================================== GETTERS ========================================
    @property
    def built(self) -> bool:
        """Vérifie si le renderer est construit"""
        return self._built

    @property
    def has_chunks(self) -> bool:
        """Vérifie s'il y a des chunks à rendre"""
        return bool(self._chunk_offsets)

    # ======================================== BUILD ========================================
    def build(self) -> None:
        """Construit la texture array et le VAO global"""
        self.delete()

        tm = self._tile_map
        tile = tm.tile

        self._texture = TileArrayTexture(
            tile.image_path,
            int(tile.tile_width),
            int(tile.tile_height),
            int(tile.margin),
            int(tile.spacing),
        )

        tw = tm.tile_width
        th = tm.tile_height
        chunk_cols = (tm.cols + self._chunk_size - 1) // self._chunk_size
        chunk_rows = (tm.rows + self._chunk_size - 1) // self._chunk_size

        # Accumulation de tous les sommets dans un seul buffer
        segments: list[np.ndarray] = []
        cursor = 0

        for cr in range(chunk_rows):
            for cc in range(chunk_cols):
                verts = self._build_chunk_verts(cc, cr, tw, th)
                if verts is not None:
                    count = len(verts)
                    self._chunk_offsets[(cc, cr)] = (cursor, count)
                    segments.append(verts)
                    cursor += count

        if not segments:
            return

        data = np.concatenate(segments)

        vao = gl.GLuint()
        vbo = gl.GLuint()
        gl.glGenVertexArrays(1, ctypes.byref(vao))
        gl.glGenBuffers(1, ctypes.byref(vbo))
        self._vao = vao.value
        self._vbo = vbo.value

        gl.glBindVertexArray(self._vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo)

        raw = data.tobytes()
        gl.glBufferData(gl.GL_ARRAY_BUFFER, len(raw), raw, gl.GL_STATIC_DRAW)

        stride = 5 * 4
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 2, gl.GL_FLOAT, gl.GL_FALSE, stride, 0)
        gl.glEnableVertexAttribArray(1)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, ctypes.c_void_p(8))

        gl.glBindVertexArray(0)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

        self._built = True

    def _build_chunk_verts(self, cc: int, cr: int, tw: float, th: float) -> np.ndarray | None:
        """Génère les sommets (x, y, u, v, layer) pour tous les quads d'un chunk

        Pré-alloue le buffer numpy au maximum théorique puis tronque.
        """
        tm = self._tile_map
        row_start = cr * self._chunk_size
        col_start = cc * self._chunk_size
        row_end = min(row_start + self._chunk_size, tm.rows)
        col_end = min(col_start + self._chunk_size, tm.cols)

        max_tiles = (row_end - row_start) * (col_end - col_start)
        buf = np.empty((max_tiles * 6, 5), dtype=np.float32)  # 6 sommets/tile, 5 floats/sommet
        idx = 0

        for row in range(row_start, row_end):
            for col in range(col_start, col_end):
                tile_id = tm.tile_at(col, row)
                if tile_id == 0:
                    continue
                layer = self._texture.get_layer(tile_id)
                if layer < 0:
                    continue
                wx, wy = tm.tile_to_world(col, row)
                bl, br, tr_, tl = _flip_uvs(tm.flags_at(col, row))
                l = float(layer)
                buf[idx    ] = [wx,      wy,      bl[0],  bl[1],  l]
                buf[idx + 1] = [wx + tw, wy,      br[0],  br[1],  l]
                buf[idx + 2] = [wx + tw, wy + th, tr_[0], tr_[1], l]
                buf[idx + 3] = [wx,      wy,      bl[0],  bl[1],  l]
                buf[idx + 4] = [wx + tw, wy + th, tr_[0], tr_[1], l]
                buf[idx + 5] = [wx,      wy + th, tl[0],  tl[1],  l]
                idx += 6

        return buf[:idx] if idx > 0 else None

    # ======================================== DRAW ========================================
    def begin(self) -> None:
        """Active le shader et bind la texture array"""
        program = _get_program()
        program.use()
        block_idx = gl.glGetUniformBlockIndex(program.id, b"WindowBlock")
        gl.glUniformBlockBinding(program.id, block_idx, 0)
        if self._texture:
            self._texture.bind(0)
        program['u_tiles'] = 0

    def draw_visible(self, cc_min: int, cc_max: int, cr_min: int, cr_max: int) -> None:
        """Dessine tous les chunks visibles en un seul appel GL

        Args:
            cc_min(int): colonne de chunk minimale (inclusive)
            cc_max(int): colonne de chunk maximale (exclusive)
            cr_min(int): ligne de chunk minimale (inclusive)
            cr_max(int): ligne de chunk maximale (exclusive)
        """
        firsts: list[int] = []
        counts: list[int] = []

        for cr in range(cr_min, cr_max):
            for cc in range(cc_min, cc_max):
                entry = self._chunk_offsets.get((cc, cr))
                if entry:
                    firsts.append(entry[0])
                    counts.append(entry[1])

        if not firsts:
            return

        n = len(firsts)
        c_firsts = (gl.GLint   * n)(*firsts)
        c_counts = (gl.GLsizei * n)(*counts)

        gl.glBindVertexArray(self._vao)
        gl.glMultiDrawArrays(gl.GL_TRIANGLES, c_firsts, c_counts, n)

    def end(self) -> None:
        """Désactive le shader"""
        pass

    # ======================================== LIFE CYCLE ========================================
    def delete(self) -> None:
        """Libère toutes les ressources GL"""
        if self._vao is not None:
            v = gl.GLuint(self._vao)
            gl.glDeleteVertexArrays(1, ctypes.byref(v))
            self._vao = None
        if self._vbo is not None:
            v = gl.GLuint(self._vbo)
            gl.glDeleteBuffers(1, ctypes.byref(v))
            self._vbo = None
        self._chunk_offsets.clear()
        if self._texture:
            self._texture.delete()
            self._texture = None
        self._built = False

# ======================================== UV HELPERS ========================================
def _flip_uvs(flip: int) -> tuple[tuple, tuple, tuple, tuple]:
    """Calcule les UV des 4 coins (BL, BR, TR, TL) selon les flags de flip Tiled

    Args:
        flip(int): combinaison de FLIP_H, FLIP_V, FLIP_D
    """
    corners = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    if flip & FLIP_D:
        corners = [(v, u) for u, v in corners]
    if flip & FLIP_H:
        corners = [(1.0 - u, v) for u, v in corners]
    if flip & FLIP_V:
        corners = [(u, 1.0 - v) for u, v in corners]
    return tuple(corners)