# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, positive, not_null
from ..._rendering import Pipeline, PygletShapeRenderer
from ...asset import Color
from ...abc import Widget, Shape
from ...math import Point

from .._context import RenderContext

from numbers import Real

# ======================================== WIDGET ========================================
class Surface(Widget):
    """Composant GUI simple: Surface

    Args:
        shape: forme de la surface
        position: position
        anchor: ancre locale relative
        scale: facteur de redimensionnement
        rotation: angle de rotation
        color: couleur de remplissage
        opacité: opacité [0; 1]
        clipping: rendu des widgets enfants strictement dans le AABB de la hitbox
    """
    __slots__ = (
        "_shape", "_shape_renderer",
        "_color",
    )

    def __init__(
            self,
            shape: Shape,
            position: Point = (0.0, 0.0),
            anchor: Point = (0.5, 0.5),
            scale: Real = 1.0,
            rotation: Real = 0.0,
            color: Color = (125, 125, 125),
            opacity: Real = 1.0,
            clipping: bool = False,
        ):
        # Initialisation du widget
        super().__init__(position, anchor, scale, rotation, opacity, clipping=clipping)

        # Forme
        self._shape: Shape = expect(shape, Shape)
        self._shape_renderer: PygletShapeRenderer = None

        # Affichage
        self._color: Color = Color(color)

        # Hooks
        self.on_show(self._on_show)
        self.on_hide(self._on_hide)

    # ======================================== GETTERS ========================================
    @property
    def shape(self) -> Shape:
        """Renvoie la forme de la surface"""
        return self._shape
    
    @property
    def color(self) -> Color:
        """Renvoie la couleur de remplissage"""
        return self._color
    
    @property
    def hitbox(self) -> Shape:
        """Renvoie la hitbox de la surface"""
        return self._shape
    
    # ======================================== SETTERS ========================================
    @shape.setter
    def shape(self, value: Shape) -> None:
        """Fixe la forme de la surface"""
        self._shape = expect(value, Shape)
        self._invalidate_scissor()
    
    @color.setter
    def color(self, value: Color) -> None:
        """Fixe la couleur de remplissage"""
        self._color = Color(value)

    # ======================================== INTERFACE ========================================
    def copy(self) -> Surface:
        """Renvoie une copie du widget"""
        return Surface(
            shape = self._shape,
            position = self._position,
            anchor = self._anchor,
            scale = self._scale,
            rotation = self._rotation,
            color=self._color,
            opacity = self._opacity,
            clipping = self._clipping,
        )
    
    # ======================================== HOOKS ========================================
    def _on_show(self) -> None:
        """Devient visible"""
        if self._shape_renderer is None:
            return
        self._shape_renderer.visible = True

    def _on_hide(self) -> None:
        """Devient invisible"""
        if self._shape_renderer is None:
            return
        self._shape_renderer.visible = False

    # ======================================== LIFE CYCLE ========================================
    def _update(self, dt: float) -> None:
        """Actualisation"""
        ...
    
    def _draw(self, pipeline: Pipeline, context: RenderContext) -> None:
        """Affichage"""
        # Construction du renderer
        if self._shape_renderer is None:
            self._shape_renderer = PygletShapeRenderer(
                shape = self._shape,
                x = context.x,
                y = context.y,
                anchor_x = self.anchor_x,
                anchor_y = self.anchor_y,
                scale = context.scale,
                rotation = context.rotation,
                color = self._color,
                opacity = context.opacity,
                pipeline = pipeline,
                z = context.z,
                parent=context.group,
            )

        # Mise à jour du renderer
        else:
            self._shape_renderer.update(
                x = context.x,
                y = context.y,
                anchor_x = self.anchor_x,
                anchor_y = self.anchor_y,
                scale = context.scale,
                rotation = context.rotation,
                color = self._color,
                opacity = context.opacity,
                pipeline=pipeline,
                z=context.z,
                parent=context.group,
            )
 
    def _destroy(self) -> None:
        """
        Libère les ressources pyglet et se détache de son parent.
        À appeler explicitement quand le widget n'est plus utilisé.
        """
        if self._shape_renderer is not None:
            self._shape_renderer.delete()
            self._shape_renderer = None