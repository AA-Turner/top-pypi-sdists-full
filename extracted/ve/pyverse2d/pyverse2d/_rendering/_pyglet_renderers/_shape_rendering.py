# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...typing import BorderAlign
from ...asset import Color
from ...abc import Shape
from ..._core import Geometry

from .. import Pipeline

import pyglet
import pyglet.gl
from pyglet.graphics import ShaderGroup, Group
from pyglet.graphics.shader import ShaderProgram

import numpy as np

# ======================================== CONSTANTS ========================================
_UNSET = object()

_REBUILD_KEYS: frozenset[str] = frozenset({"z", "geometry", "parent"})
_STYLE_KEYS: frozenset[str] = frozenset({"opacity", "color"})

_STRIP_REFRESH_KEYS: frozenset[str] = frozenset({"transform", "border_width", "border_align"})
_STRIP_STYLE_KEYS: frozenset[str] = frozenset({"opacity", "border_color"})

# ======================================== PUBLIC ========================================
class PygletShapeRenderer:
    """Renderer pyglet unifié pour une shape géométrique

    Args:
        geometry: géométrie monde
        filling: activer le remplissage
        color: couleur de remplissage
        border_width: épaisseur de la bordure en pixels
        border_align: alignement de la bordure ("center" | "in" | "out")
        border_color: couleur de la bordure
        opacity: opacité globale [0.0, 1.0]
        z: z-order
        pipeline: pipeline de rendu
        parent: groupe parent
    """
    __slots__ = (
        "_geometry",
        "_filling", "_color",
        "_border_width", "_border_align", "_border_color",
        "_opacity", "_z", "_pipeline", "_parent",
        "_transform_version", "_fill", "_border",
    )

    # Cache partagé des shader groups
    _PROGRAM: ShaderProgram = None
    _GROUPS: dict[tuple[int, int], ShaderGroup] = {}

    @classmethod
    def get_program(cls) -> ShaderProgram:
        """Renvoie le shader programme des formes"""
        if cls._PROGRAM is None:
            cls._PROGRAM = pyglet.shapes.get_default_shader()
        return cls._PROGRAM

    @classmethod
    def get_group(cls, pipeline: Pipeline, z: int = 0, order: int = 0, parent: Group = None) -> ShaderGroup:
        """Renvoie le groupe correspondant avec mise en cache"""
        key = (z, order, parent)
        if key not in cls._GROUPS:
            cls._GROUPS[key] = ShaderGroup(cls.get_program(), order=order, parent=pipeline.get_group(z=z) if parent is None else parent)
        return cls._GROUPS[key]

    def __init__(
        self,
        geometry: Geometry,
        filling: bool = True,
        color: Color = None,
        border_width: int = 0,
        border_align: BorderAlign = "center",
        border_color: Color = None,
        opacity: float = 1.0,
        z: int = 0,
        pipeline: Pipeline = None,
        parent: Group = None,
    ):
        # Attributs publiques
        self._geometry: Geometry = geometry
        self._filling: bool = filling
        self._color: Color = color
        self._border_width: int = border_width
        self._border_align: BorderAlign = border_align
        self._border_color: Color = border_color
        self._opacity: float = opacity
        self._z: int = z
        self._pipeline: Pipeline = pipeline
        self._parent: Group = parent

        # Attributs internes
        self._transform_version: int = self._geometry.transform.version
        self._fill: _FillRenderer = None
        self._border: _BorderRenderer = None
        self._build()

    # ======================================== INTERNALS ========================================
    def _build(self) -> None:
        """Construit les sous-renderers fill et border"""
        if self._filling and self._color is not None:
            self._fill = _FillRenderer(self)
        if self._border_width > 0 and self._border_color is not None:
            self._border = _BorderRenderer(self)

    # ======================================== GETTERS ========================================
    @property
    def geometry(self) -> Geometry: return self._geometry
    @property
    def shape(self) -> Shape: return self._geometry.shape

    @property
    def filling(self) -> bool: return self._filling
    @property
    def color(self) -> Color: return self._color

    @property
    def border_width(self) -> int: return int(self._border_width)
    @property
    def border_align(self) -> BorderAlign: return self._border_align
    @property
    def border_color(self) -> Color: return self._border_color
    @property
    def opacity(self) -> float: return self._opacity

    @property
    def z(self) -> int: return self._z
    @property
    def pipeline(self) -> Pipeline: return self._pipeline
    @property
    def parent(self) -> Group: return self._parent
    
    # ======================================== VISIBILITY ========================================
    @property
    def visible(self) -> bool:
        """Visibilité"""
        if self._fill: return self._fill.visible
        if self._border: return self._border.visible
        return False

    @visible.setter
    def visible(self, value: bool) -> None:
        if self._fill: self._fill.visible = value
        if self._border: self._border.visible = value

    def is_visible(self) -> bool:
        """Vérifie la visibilité effective"""
        return self.visible and ((self._filling and self._color is not None) or (self._border_width > 0 and self._border_color is not None))

    # ======================================== LIFE CYCLE ========================================
    def update(self, **kwargs) -> None:
        """Actualisation

        Args:
            geometry: géométrie monde
            filling: remplissage activé
            color: couleur de remplissage
            border_width: épaisseur de bordure
            border_align: alignement de la bordure
            border_color: couleur de bordure
            opacity: opacité
            z: z-order
            parent: groupe parent
        """
        # Détection des changements
        changes: set[str] = set()
        for key, value in kwargs.items():
            current = getattr(self, f"_{key}", _UNSET)
            if current is _UNSET or value == current:
                continue
            setattr(self, f"_{key}", value)
            changes.add(key)

        # Vérication de la version du Transform
        tr_version = self._geometry.transform.version
        if tr_version != self._transform_version:
            changes.add("transform")
            self._transform_version = tr_version

        if not changes:
            return

        # Remplissage
        if self._filling:
            if self._fill is not None:
                self._fill.update(self, changes)
            elif self._color is not None:
                self._fill = _FillRenderer(self)
        elif self._fill is not None:
            self._fill.delete()
            self._fill = None

        # Bordure
        if self._border_width > 0:
            if self._border is not None:
                self._border.update(self, changes)
            elif self._border_color is not None:
                self._border = _BorderRenderer(self)
        elif self._border is not None:
            self._border.delete()
            self._border = None

    def delete(self) -> None:
        """Libère toutes les ressources pyglet"""
        if self._fill:
            self._fill.delete()
            self._fill = None
        if self._border:
            self._border.delete()
            self._border = None

# ======================================== FILL RENDERER ========================================
class _FillRenderer:
    """Remplissage mesh-based"""
    __slots__ = ("_vlist", "_n", "_visible", "_stored_colors")

    def __init__(self, psr: PygletShapeRenderer):
        self._vlist = None
        self._n: int = 0
        self._visible: bool = True
        self._stored_colors = None
        self._build(psr)

    # ======================================== BUILD ========================================
    def _build(self, psr: PygletShapeRenderer) -> None:
        """Construit le ``vertex_list_indexed`` depuis le Mesh de la shape"""
        if self._vlist is not None:
            self._vlist.delete()

        vertices = psr.geometry.world_vertices()
        indexes = psr.geometry.shape.get_indexes()
        self._n = len(vertices)

        r, g, b, a = psr.color.rgba8
        a = int(a * psr.opacity)

        self._vlist = psr.get_program().vertex_list_indexed(
            count = self._n,
            mode = pyglet.gl.GL_TRIANGLES,
            indices = indexes.flatten().tolist(),
            batch = psr.pipeline.batch,
            group = psr.get_group(pipeline=psr.pipeline, z=psr.z, order=0, parent=psr.parent),
            position = ('f', vertices.flatten().tolist()),
            colors = ('Bn', (r, g, b, a) * self._n),
        )

    # ======================================== PROPERTIES ========================================
    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        """Active ou masque via alpha"""
        if value == self._visible:
            return
        self._visible = value
        if value:
            self._vlist.colors[:] = self._stored_colors
            self._stored_colors = None
        else:
            self._stored_colors = list(self._vlist.colors[:])
            self._vlist.colors[:] = (0, 0, 0, 0) * self._n

    # ======================================== LIFE CYCLE ========================================
    def update(self, psr: PygletShapeRenderer, changes: set[str]) -> None:
        """Actualisation"""
        # Changement de z-order
        if not changes.isdisjoint(_REBUILD_KEYS):
            self._build(psr)
            return
        
        # Changement de position
        if "transform" in changes:
            vertices = psr.geometry.world_vertices()
            self._vlist.position[:] = vertices.flatten().tolist()

        # Changement de style
        if not changes.isdisjoint(_STYLE_KEYS):
            r, g, b, a = psr.color.rgba8
            a = int(a * psr.opacity)
            self._vlist.colors[:] = (r, g, b, a) * self._n

    def delete(self) -> None:
        """Libère les ressources pyglet"""
        if self._vlist is not None:
            self._vlist.delete()
            self._vlist = None

# ======================================== BORDER RENDERER ========================================
class _BorderRenderer:
    """Bordure via triangle strip"""
    __slots__ = ("_vlist", "_n", "_visible", "_stored_colors")

    def __init__(self, psr: PygletShapeRenderer):
        self._vlist = None
        self._n: int = 0
        self._visible: bool = True
        self._stored_colors = None
        self._build(psr)

    # ======================================== BUILD ========================================
    def _build(self, psr: PygletShapeRenderer) -> None:
        """Construit le ``vertex_list`` du triangle strip"""
        if self._vlist is not None:
            self._vlist.delete()

        strip = _world_strip(psr)
        self._n = len(strip)

        r, g, b, a = psr.border_color.rgba8
        a = int(a * psr.opacity)

        self._vlist = psr.get_program().vertex_list(
            count = self._n,
            mode = pyglet.gl.GL_TRIANGLE_STRIP,
            batch = psr.pipeline.batch,
            group = psr.get_group(pipeline=psr.pipeline, z=psr.z, order=1),
            position = ('f', strip.flatten().tolist()),
            colors = ('Bn', (r, g, b, a) * self._n),
        )

    def _refresh_strip(self, psr: PygletShapeRenderer) -> None:
        """Rebuild du strip monde si border_width ou border_align changent"""
        strip = _world_strip(psr)
        self._n = len(strip)
        self._vlist.position[:] = strip.flatten().tolist()

    # ======================================== PROPERTIES ========================================
    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        if value == self._visible:
            return
        self._visible = value
        if value:
            self._vlist.colors[:] = self._stored_colors
            self._stored_colors = None
        else:
            self._stored_colors = list(self._vlist.colors[:])
            self._vlist.colors[:] = (0, 0, 0, 0) * self._n

    # ======================================== LIFE CYCLE ========================================
    def update(self, psr: PygletShapeRenderer, changes: set[str]) -> None:
        """Actualisation"""
        # Changement de z-order
        if not changes.isdisjoint(_REBUILD_KEYS):
            self._build(psr)
            return

        # Changement de bordure
        if not changes.isdisjoint(_STRIP_REFRESH_KEYS):
            self._refresh_strip(psr)

        # Changement de style
        if not changes.isdisjoint(_STRIP_STYLE_KEYS):
            r, g, b, a = psr.border_color.rgba8
            a = int(a * psr.opacity)
            self._vlist.colors[:] = (r, g, b, a) * self._n

    def delete(self) -> None:
        """Libère les ressources pyglet"""
        if self._vlist is not None:
            self._vlist.delete()
            self._vlist = None

# ======================================== HELPERS ========================================
def _world_strip(psr: PygletShapeRenderer) -> np.ndarray:
    """Génère le triangle strip en espace monde"""
    world = psr.geometry.world_vertices()
    return _build_strip(world, psr.border_width * psr.geometry.transform.scale, psr.border_align)

def _build_strip(contour: np.ndarray, width: float, align: str = "center") -> np.ndarray:
    """Génère un triangle strip ``(N+1)*2`` points autour d'un contour fermé"""
    n = len(contour)
    prev_pts = contour[(np.arange(n) - 1) % n]
    next_pts = contour[(np.arange(n) + 1) % n]

    def edge_normals(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        d = b - a
        lengths = np.linalg.norm(d, axis=1, keepdims=True)
        lengths = np.where(lengths == 0, 1, lengths)
        d /= lengths
        return np.column_stack((-d[:, 1], d[:, 0]))

    n1 = edge_normals(prev_pts, contour)
    n2 = edge_normals(contour, next_pts)
    miter = n1 + n2

    miter_len = np.linalg.norm(miter, axis=1, keepdims=True)
    miter_len = np.where(miter_len == 0, 1, miter_len)
    miter /= miter_len

    dot = np.einsum('ij,ij->i', n1, miter).reshape(-1, 1)
    dot = np.where(np.abs(dot) < 0.01, 0.01, dot)

    if align == "center":
        half = width / 2.0
        miter_dist = np.clip(half / dot, -width * 3, width * 3)
        outer = contour + miter * miter_dist
        inner = contour - miter * miter_dist
    elif align == "in":
        miter_dist = np.clip(width / dot, -width * 3, width * 3)
        outer = contour + miter * miter_dist
        inner = contour
    elif align == "out":
        miter_dist = np.clip(width / dot, -width * 3, width * 3)
        outer = contour
        inner = contour - miter * miter_dist

    strip = np.empty(((n + 1) * 2, 2), dtype=np.float32)
    strip[0::2][:n] = outer
    strip[1::2][:n] = inner
    strip[-2] = outer[0]
    strip[-1] = inner[0]

    return strip

# ======================================== EXPORTS ========================================
__all__ = [
    "PygletShapeRenderer",
]