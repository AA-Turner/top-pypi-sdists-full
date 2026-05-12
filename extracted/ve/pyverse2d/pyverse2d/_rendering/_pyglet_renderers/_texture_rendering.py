# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._core import Transform
from ...asset import Color
from ...math import Vector

from .. import Pipeline

import pyglet
import pyglet.sprite
from pyglet.graphics import Group

# ======================================== CONSTANTS ========================================
_UNSET: object = object()

# ======================================== TEXTURE RENDERER ========================================
class PygletTextureRenderer:
    """Renderer pyglet unifié pour une texture brute (ex: frame vidéo

    Args:
        texture: texture pyglet brute
        transform: transformation monde
        offset: décalage par rapport au transform
        width: largeur d'affichage en pixels
        height: hauteur d'affichage en pixels)
        color: teinte multiplicative
        opacity: opacité [0, 1]
        z: z-order
        pipeline: pipeline de rendu
        parent: groupe parent
    """
    __slots__ = (
        "_texture",
        "_transform", "_offset",
        "_width", "_height",
        "_color", "_opacity",
        "_z", "_pipeline", "_parent",
        "_transform_version", "_sprite",
    )

    def __init__(
        self,
        texture,
        transform: Transform,
        offset: Vector = None,
        width: int = None,
        height: int = None,
        color: Color = None,
        opacity: float = 1.0,
        z: int = 0,
        pipeline: Pipeline = None,
        parent: Group = None,
    ):
        # Attributs publiques
        self._texture: pyglet.image.AbstractImage | pyglet.image.Texture = texture
        self._transform: Transform = transform
        self._offset: Vector | None = offset
        self._width: int | None = width
        self._height: int | None = height
        self._color: Color = color
        self._opacity: float = opacity
        self._z: int = z
        self._pipeline: Pipeline = pipeline
        self._parent: Group = parent

        # Attributs internes
        self._transform_version: int = self._transform.version
        self._sprite: pyglet.sprite.Sprite = None
        self._build()

    # ======================================== BUILD ========================================
    def _build(self) -> None:
        """Construit le sprite pyglet depuis la texture brute"""
        if self._texture is None:
            return

        r, g, b, a = self._color.rgba8 if self._color is not None else (255, 255, 255, 255)
        a = int(a * self._opacity)

        self._sprite = pyglet.sprite.Sprite(
            self._texture,
            batch=self._pipeline.batch,
            group=self._pipeline.get_group(z=self._z) if self._parent is None else self._parent,
        )
        self._sprite.color = (r, g, b, a)
        self._refresh_transform()

    # ======================================== GETTERS ========================================
    @property
    def texture(self): return self._texture
    @property
    def transform(self) -> Transform: return self._transform
    @property
    def offset(self) -> Vector | None: return self._offset

    @property
    def width(self) -> int | None: return self._width
    @property
    def height(self) -> int | None: return self._height
    @property
    def color(self) -> Color: return self._color
    @property
    def opacity(self) -> float: return self._opacity

    @property
    def z(self) -> int: return self._z
    @property
    def pipeline(self) -> Pipeline: return self._pipeline
    @property
    def parent(self) -> Group: return self._parent

    @property
    def content_width(self) -> int:
        """Largeur effective affichée"""
        return self._sprite.width if self._sprite else 0

    @property
    def content_height(self) -> int:
        """Hauteur effective affichée"""
        return self._sprite.height if self._sprite else 0

    # ======================================== VISIBILITY ========================================
    @property
    def visible(self) -> bool:
        """Renvoie la visibilité"""
        return self._sprite.visible if self._sprite else False

    @visible.setter
    def visible(self, value: bool) -> None:
        """Active ou désactive la visibilité"""
        if self._sprite:
            self._sprite.visible = value

    def is_visible(self) -> bool:
        """Vérifie la visibilité"""
        return self._sprite is not None and self._sprite.visible

    # ======================================== LIFE CYCLE ========================================
    def update(self, **kwargs) -> None:
        """Met à jour le renderer texture

        Args:
            texture: nouvelle texture pyglet brute
            transform: transformation monde
            offset: décalage
            width: largeur d'affichage
            height: hauteur d'affichage
            color: teinte multiplicative
            opacity: opacité
            z: z-order
            pipeline: pipeline de rendu
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

        # Vérification de la version du transform
        tr_version = self._transform.version
        if tr_version != self._transform_version:
            changes.add("transform")
            self._transform_version = tr_version

        if not changes:
            return

        # Activation des handlers
        rebuild: bool = False
        refresh: bool = False
        for key in changes:
            handler = getattr(self, f"_handle_{key}", None)
            if handler:
                output: str | None = handler()
                if output == "rebuild":
                    rebuild = True
                elif output == "refresh":
                    refresh = True

        # Recalculs globaux
        if rebuild:
            self._rebuild()
        elif refresh:
            self._refresh_transform()

    def delete(self) -> None:
        """Libère les ressources pyglet"""
        if self._sprite:
            self._sprite.delete()
            self._sprite = None

    # ======================================== HANDLERS ========================================
    def _handle_texture(self) -> str:
        """Swap de texture sans reconstruire le sprite"""
        if self._sprite is None:
            return "rebuild"
        if self._texture is None:
            self.delete()
            return None
        self._sprite.image = self._texture
        return "refresh"

    def _handle_transform(self) -> str:
        """Actualisation de la transformation monde"""
        return "refresh"

    def _handle_offset(self) -> str:
        """Actualisation du décalage"""
        return "refresh"

    def _handle_width(self) -> str:
        """Actualisation de la largeur d'affichage"""
        return "refresh"

    def _handle_height(self) -> str:
        """Actualisation de la hauteur d'affichage"""
        return "refresh"

    def _handle_color(self) -> None:
        """Actualisation de la teinte multiplicative"""
        if self._sprite is None:
            return
        r, g, b, a = self._color.rgba8 if self._color is not None else (255, 255, 255, 255)
        a = int(a * self._opacity)
        self._sprite.color = (r, g, b, a)

    def _handle_opacity(self) -> None:
        """Actualisation de l'opacité"""
        if self._sprite is None:
            return
        a = self._color.a if self._color is not None else 1.0
        self._sprite.opacity = int(255 * a * self._opacity)

    def _handle_z(self) -> None:
        """Actualisation du z-order"""
        if self._sprite is None:
            return
        self._sprite.group = self._pipeline.get_group(z=self._z) if self._parent is None else self._parent

    def _handle_parent(self) -> None:
        """Actualisation du groupe parent"""
        if self._sprite is None:
            return
        self._sprite.group = self._pipeline.get_group(z=self._z) if self._parent is None else self._parent

    # ======================================== INTERNALS ========================================
    def _rebuild(self) -> None:
        """Reconstruit le sprite avec les paramètres courants"""
        self.delete()
        self._build()

    def _refresh_transform(self) -> None:
        """Actualise la transformation sans reconstruire"""
        if self._sprite is None:
            return

        img = self._sprite.image

        # Anchor
        img.anchor_x = int(self._transform.anchor_x * img.width)
        img.anchor_y = int(self._transform.anchor_y * img.height)

        # Position
        if self._offset is None:
            self._sprite.x, self._sprite.y = self._transform.position
        else:
            self._sprite.x = self._transform.x + self._offset.x
            self._sprite.y = self._transform.y + self._offset.y

        # Échelle
        self._sprite.scale_x, self._sprite.scale_y = self._effective_scales(img)

        # Rotation
        self._sprite.rotation = -self._transform.rotation

    def _effective_scales(self, img) -> tuple[float, float]:
        """Calcule les échelles effectives selon width/height demandés"""
        raw_w = img.width
        raw_h = img.height

        if raw_w == 0 or raw_h == 0:
            return (1.0, 1.0)

        sx = (self._width / raw_w) if self._width is not None else 1.0
        sy = (self._height / raw_h) if self._height is not None else 1.0

        return self._transform.scale * sx, self._transform.scale * sy

# ======================================== EXPORTS ========================================
__all__ = [
    "PygletTextureRenderer",
]