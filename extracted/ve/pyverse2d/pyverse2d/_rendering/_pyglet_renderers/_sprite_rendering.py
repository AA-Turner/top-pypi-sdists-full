# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._core import Transform
from ...asset import Color, Image
from ...math import Vector

from .. import Pipeline

import pyglet
import pyglet.sprite
from pyglet.gl import (
    glBindTexture, glTexParameteri,
    GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE
)
from pyglet.graphics import Group

import os

# ======================================== CONSTANTS ========================================
_UNSET = object()   # élément non défini

# ======================================== SPRITE RENDERER ========================================
class PygletSpriteRenderer:
    """Renderer pyglet unifié pour un sprite

    Args:
        image: descripteur d'image (asset)
        transform: transformation monde
        offset: décalage par rapport au transform
        flip_x: miroir horizontal
        flip_y: miroir vertical
        color teinte multiplicative
        opacity: opacité [0.0 ; 1.0]
        z: z-order
        pipeline: pipeline de rendu
        parent: groupe parent
    """
    __slots__ = (
        "_image","_transform", "_offset",
        "_flip_x", "_flip_y",
        "_color", "_opacity",
        "_z", "_pipeline", "_parent",
        "_transform_version", "_sprite",
    )

    def __init__(
        self,
        image: Image,
        transform: Transform,
        offset: Vector = None,
        flip_x: bool = False,
        flip_y: bool = False,
        rotation: float = 0.0,
        color: Color = None,
        opacity: float = 1.0,
        z: int = 0,
        pipeline: Pipeline = None,
        parent: Group = None,
    ):
        # Attributs publiques
        self._image: Image = image
        self._transform: Transform = transform
        self._offset: Vector = None
        self._flip_x: bool = flip_x
        self._flip_y: bool = flip_y
        self._rotation: float = rotation
        self._opacity: float = opacity
        self._color: Color = color
        self._z: int = z
        self._pipeline: Pipeline = pipeline
        self._parent: Group = parent

        # Attributs internes
        self._transform_version: int = self._transform.version
        self._sprite: pyglet.sprite.Sprite = None
        self._build()

    # ======================================== LOADING ========================================
    @classmethod
    def _load_image(cls, path: str) -> pyglet.image.AbstractImage | None:
        """Charge  une texture depuis son chemin"""
        directory = os.path.dirname(os.path.abspath(path))
        if directory not in pyglet.resource.path:
            pyglet.resource.path.append(directory)
            pyglet.resource.reindex()

        try:
            raw = pyglet.resource.image(os.path.basename(path), atlas=False)
            glBindTexture(GL_TEXTURE_2D, raw.get_texture().id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            return raw
        except pyglet.resource.ResourceNotFoundException:
            print(f"[PygletSpriteRenderer] Cannot load image: {path}")
            return None

    # ======================================== BUILD ========================================
    def _build(self) -> None:
        """Construit le sprite pyglet"""
        # Couleur
        r, g, b, a = self._color.rgba8 if self._color is not None else (255, 255, 255, 255)
        a = int(a * self._opacity)

        # Image brute
        raw = self._load_image(self._image.path)
        if raw is None:
            return
 
        # Travaille sur une région
        region = raw.get_region(0, 0, raw.width, raw.height)
    
        # Construction du sprite
        self._sprite = pyglet.sprite.Sprite(
            region,
            batch=self._pipeline.batch,
            group=self._pipeline.get_group(z=self._z) if self._parent is None else self._parent,
        )
        self._sprite.color = (r, g, b, a)

        # Application de la transformation
        self._refresh_transform()

    # ======================================== GETTERS ========================================
    @property
    def image(self) -> Image:
        """Descripteur d'image"""
        return self._image
    
    @property
    def transform(self) -> Transform:
        """Transformation monde"""
        return self._transform
    
    @property
    def offset(self) -> Vector | None:
        """Décalage au transform"""
        return self._offset

    @property
    def flip_x(self) -> bool:
        """Renvoie le miroir horizontal"""
        return self._flip_x

    @property
    def flip_y(self) -> bool:
        """Renvoie le miroir vertical"""
        return self._flip_y

    @property
    def opacity(self) -> float:
        """Renvoie l'opacité"""
        return self._opacity

    @property
    def color(self) -> Color:
        """Renvoie la teinte multiplicative"""
        return self._color

    @property
    def z(self) -> int:
        """Renvoie le z-order"""
        return self._z

    @property
    def pipeline(self) -> Pipeline:
        """Renvoie la pipeline de rendu"""
        return self._pipeline
    
    @property
    def parent(self) -> Group:
        """Renvoie le groupe parent"""
        return self._parent
    
    @property
    def width(self) -> int:
        """Renvoie la largeur de la texture"""
        return self._sprite.width
    
    @property
    def height(self) -> int:
        """Renvoie la hauteur de la texture"""
        return self._sprite.height

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
        """
        Met à jour le renderer sprite

        Args:
            image: descripteur d'image
            transform: transformation monde
            offset: décalage
            flip_x: miroir horizontal
            flip_y: miroir vertical
            opacity: opacité
            color: teinte multiplicative
            z: z-order
            pipeline: pipeline de rendu
            parent: groupe parent
        """
        # Détection des changements
        changes: list[str] = set()
        for key, value in kwargs.items():
            current = getattr(self, f"_{key}", _UNSET)
            if current is _UNSET or value == current:
                continue
            setattr(self, f"_{key}", value)
            changes.add(key)

        # Vérificatin de la version du transform
        tr_version = self._transform.version
        if tr_version != self._transform_version:
            changes.add("transform")
            self._transform_version = tr_version

        # Activation des handlers
        rebuild: bool = False
        refresh: bool = False
        for key in changes:
            handler = getattr(self, f"_handle_{key}", None)
            if handler:
                output: str | None = handler()
                if output:
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
    def _handle_image(self) -> str:
        """Actualisation de l'image"""
        return "rebuild"

    def _handle_transform(self) -> str:
        """Actualisation de la transformation monde"""
        return "refresh"
    
    def _handle_offset(self) -> str:
        """Actualisation du décalage"""
        return "refresh"
    
    def _handle_flip_x(self) -> str:
        """Actualisation du mirroir horizontal"""
        return "refresh"

    def _handle_flip_y(self) -> str:
        """Actualisation du mirroir vertical"""
        return "refresh"

    def _handle_color(self) -> None:
        """Actualisation de la couleur de teinte"""
        r, g, b, a = self._color.rgba8 if self._color is not None else (255, 255, 255, 255)
        a = int(a * self._opacity)
        self._sprite.color = (r, g, b, a)

    def _handle_opacity(self) -> None:
        """Actualisation de l'opacité"""
        self._sprite.opacity = int(255 * self._color.a * self._opacity)

    def _handle_z(self) -> None:
        """Actualisation du z-order"""
        self._sprite.group = self._pipeline.get_group(z=self._z) if self._parent is None else self._parent

    def _handle_parent(self) -> None:
        """Actualisation du groupe parent"""
        self._sprite.group = self._pipeline.get_group(z=self._z) if self._parent is None else self._parent

    # ======================================== INTERNALS ========================================
    def _rebuild(self) -> None:
        """Reconstruit le sprite avec les paramètres courants"""
        self.delete()
        self._build()

    def _refresh_transform(self) -> None:
        """Actualise transform sans reconstruire"""
        if self._sprite is None:
            return

        # Anchor
        img = self._sprite.image
        img.anchor_x = int(self._transform.anchor_x * img.width)
        img.anchor_y = int(self._transform.anchor_y * img.height)

        # Position
        if self._offset is None:
            self._sprite.x, self._sprite.y = self._transform.position
        else:
            self._sprite.x = self._transform.x + self._offset.x
            self._sprite.y = self._transform.y + self._offset.y

        # Échelle
        self._sprite.scale_x, self._sprite.scale_y = self._effective_scales(self._sprite.image)

        # Rotation
        self._sprite.rotation = -self._transform.rotation

    def _effective_scales(self, raw: pyglet.image.AbstractImage) -> tuple[float, float]:
        """Calcule les tailles effectifs"""
        img_sx: float | None = (self._image.width / raw.width if self._image.width else None)
        img_sy: float | None = (self._image.height / raw.height if self._image.height else None)

        if img_sx is None and img_sy is None:
            img_sx = img_sy = 1.0
        elif img_sx is None:
            img_sx = img_sy
        elif img_sy is None:
            img_sy = img_sx

        f  = self._image.scale_factor
        fx = -1 if self._flip_x else 1
        fy = -1 if self._flip_y else 1
        return self._transform.scale * img_sx * f * fx, self._transform.scale * img_sy * f * fy

# ======================================== EXPORTS ========================================
__all__ = [
    "PygletSpriteRenderer",
]