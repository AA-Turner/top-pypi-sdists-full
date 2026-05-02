# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect
from ..._rendering import Pipeline, PygletSpriteRenderer
from ...abc import Widget
from ...asset import Image, Color
from ...math import Point
from ...shape import Rect

from .._context import RenderContext

from numbers import Real

# ======================================== WIDGET ========================================
class Sprite(Widget):
    """Composant GUI simple: Image

    Args:
        image: asset ``Image`` à rendre
        position: position ``(x, y)``
        anchor: ancre relative locale ``(ax, ay)``
        scale: facteur de redimensionnement
        flip_x: mirroir horizontal
        flip_y: mirroir vertical
        rotation: angle de rotation en degrés
        color: asset ``Color`` de teinte
        opacity: opacité
        clipping: rendu des widgets enfants strictement dans le AABB de la hitbox
    """
    __slots__ = (
        "_image",  "_image_renderer",
        "_flip_x", "_flip_y",
        "_color",
        "_hitbox_key", "_hitbox_cache",
    )

    def __init__(
            self,
            image: Image,
            position: Point = (0.0, 0.0),
            anchor: Point = (0.5, 0.5),
            scale: Real = 1.0,
            flip_x: bool = False,
            flip_y: bool = False,
            rotation: Real = 0.0,
            color: Color = (255, 255, 255),
            opacity: Real = 1.0,
            clipping: bool = False
        ):
        # Initialisation du widget
        super().__init__(position, anchor, scale, rotation, opacity, clipping=clipping)

        # Image
        self._image: Image = expect(image, Image)
        self._image_renderer: PygletSpriteRenderer = None

        # Transform
        self._flip_x: bool = expect(flip_x, bool)
        self._flip_y: bool = expect(flip_y, bool)

        # Affichage
        self._color: Color = Color(color)

        # Cache du AABB
        self._hitbox_key: tuple = None
        self._hitbox_cache: Rect = None

        # Hooks
        self.on_show(self._on_show)
        self.on_hide(self._on_hide)

    # ======================================== PROPERTIES ========================================
    @property
    def image(self) -> Image:
        """Image à rendre

        L'image doit être un Asset ``Image``
        """
        return self._image
    
    @image.setter
    def image(self, value: Image) -> None:
        self._image = expect(value, Image)
        self._invalidate_scissor()

    @property
    def flip_x(self) -> bool:
        """Mirroir horizontal

        Cette propriété appliquera ou non une inversion horizontale de l'image
        """
        return self._flip_x
    
    @flip_x.setter
    def flip_x(self, value: bool) -> None:
        self._flip_x = expect(value, bool)
        self._invalidate_scissor()

    @property
    def flip_y(self) -> bool:
        """Mirroir vertical

        Cette propriété appliquera ou non une inversion verticale de l'image
        """
        return self._flip_y
    
    @flip_y.setter
    def flip_y(self, value: bool) -> None:
        self._flip_y = expect(value, bool)
        self._invalidate_scissor()

    @property
    def color(self) -> Color:
        """Couleur de teinte

        La couleur doit être un asset ``Color`` ou un tuple rgb/rgba
        """
        return self._color
    
    @color.setter
    def color(self, value: Color) -> None:
        self._color = Color(value)

    @property
    def hitbox(self):
        """Hitbox du sprite"""
        if self._image_renderer is None:
            return Rect(1, 1)
        key = (self._image_renderer.width, self._image_renderer.height)
        if key != self._hitbox_key:
            self._hitbox_cache = Rect(*key)
        return self._hitbox_cache
    
    # ======================================== INTERFACE ========================================
    def copy(self) -> Sprite:
        """Renvoie une copie du widget"""
        return Sprite(
            image = self._image,
            position = self._position,
            anchor = self._anchor,
            scale = self._scale,
            rotation = self._rotation,
            color = self._color,
            opacity = self._opacity,
            clipping = self._clipping,
        )

    def flip(self, horizontal: bool = False, vertical: bool = False) -> None:
        """Applique un mirroir

        L'effet mirroir inverse le rendu horizontal/vertical de l'image
        """
        self._flip_x ^= horizontal
        self._flip_y ^= vertical

    # ======================================== HOOKS ========================================
    def _on_show(self) -> None:
        """Devient visible"""
        if self._image_renderer is None:
            return
        self._image_renderer.visible = True

    def _on_hide(self) -> None:
        """Devient invisible"""
        if self._image_renderer is None:
            return
        self._image_renderer.visible = False

    # ======================================== LIFE CYCLE ========================================
    def _update(self, dt: float) -> None:
        """Actualisation"""
        ...

    def _draw(self, pipeline: Pipeline, context: RenderContext) -> None:
        """Affichage"""
        # Construction du renderer
        if self._image_renderer is None:
            self._image_renderer = PygletSpriteRenderer(
                image = self._image,
                x = context.x,
                y = context.y,
                anchor_x = self.anchor_x,
                anchor_y = self.anchor_y,
                scale_x = context.scale,
                scale_y = context.scale,
                flip_x = self._flip_x,
                flip_y = self._flip_y,
                rotation = context.rotation,
                color = self._color,
                opacity = context.opacity,
                z = context.z,
                pipeline = pipeline,
                parent=context.group,
            )
        
        # Mise à jour du renderer
        else:
            self._image_renderer.update(
                image = self._image,
                x = context.x,
                y = context.y,
                anchor_x = self.anchor_x,
                anchor_y = self.anchor_y,
                scale_x = context.scale,
                scale_y = context.scale,
                flip_x = self._flip_x,
                flip_y = self._flip_y,
                rotation = context.rotation,
                color = self._color,
                opacity = context.opacity,
                z = context.z,
                pipeline = pipeline,
                parent=context.group,
            )
    
    def _destroy(self):
        """Destruction du widget"""
        self._image_renderer.delete()
        self._image_renderer = None