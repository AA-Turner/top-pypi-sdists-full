# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect
from ..._rendering import Pipeline, PygletShapeRenderer
from ...typing import BorderAlign
from ...asset import Color
from ...abc import Widget, Shape
from ...math import Point

from .._context import RenderContext

from numbers import Real

# ======================================== WIDGET ========================================
class Border(Widget):
    """Composant GUI simple: Bordure

    Args:
        shape: forme de la bordure
        position: position
        anchor: ancre locale relative
        width: largeur de la bodure
        align: alignement de la bordure
        color: couleur de la bordure
        opacité: opacité [0; 1]
        clipping: rendu des widgets enfants strictement dans le AABB de la hitbox
    """
    __slots__ = (
        "_shape", "_shape_renderer",
        "_width", "_align", "_color",
    )

    def __init__(
            self,
            shape: Shape,
            position: Point = (0.0, 0.0),
            anchor: Point = (0.5, 0.5),
            scale: Real = 1.0,
            rotation: Real = 0.0,
            width: int = 1,
            align: BorderAlign = "center",
            color: Color = (0, 0, 0),
            opacity: Real = 1.0,
            clipping: bool = False
        ):
        # Attributs publiques
        self._shape: Shape = shape
        self._width: int = width
        self._align: BorderAlign = align
        self._color: Color = Color(color)

        if __debug__:
            expect(self._shape, Shape)
            expect(self._width, int)
            expect(self._align, str)

        # Attributs privés
        self._shape_renderer: PygletShapeRenderer = None

        # Initialisation du widget
        super().__init__(position, anchor, scale, rotation, opacity, clipping=clipping)

        # Hooks
        self.on_show(self._show_hook)
        self.on_hide(self._hide_hook)

    # ======================================== GETTERS ========================================
    @property
    def shape(self) -> Shape:
        """Forme de la bordure"""
        return self._shape
    
    @shape.setter
    def shape(self, value: Shape) -> None:
        assert isinstance(value, Shape), f"shape ({value}) must be a Shape object"
        self._shape = value.copy()
        self._invalidate_geometry()
        self._invalidate_scissor()
    
    @property
    def width(self) -> int:
        """Largeur de la bordure"""
        return self._width
    
    @width.setter
    def width(self, value: int) -> None:
        if __debug__:
            expect(value, int)
        self._width = value
    
    @property
    def align(self) -> BorderAlign:
        """Alignement de la bordure"""
        return self._align
    
    @align.setter
    def align(self, value: BorderAlign) -> None:
        self._align = value
    
    @property
    def color(self) -> Color:
        """Couleur de la bordure"""
        return self._color
    
    @color.setter
    def color(self, value: Color) -> None:
        self._color = Color(value)
    
    @property
    def hitbox(self) -> Shape:
        """Renvoie la hitbox de la forme"""
        return self._shape
    
    # ======================================== INTERFACE ========================================
    def copy(self) -> Border:
        """Renvoie une copie du widget"""
        return Border(
            shape = self._shape,
            position = self._transform.position,
            anchor = self._transform.anchor,
            scale = self._transform.scale,
            rotation = self._transform.rotation,
            width = self._width,
            align = self._align,
            color = self._color,
            opacity = self._opacity,
            clipping = self._clipping,
        )
    
    # ======================================== HOOKS ========================================
    def _show_hook(self) -> None:
        """Devient visible"""
        if self._shape_renderer is None:
            return
        self._shape_renderer.visible = True

    def _hide_hook(self) -> None:
        """Devient invisible"""
        if self._shape_renderer is None:
            return
        self._shape_renderer.visible = False

    # ======================================== LIFE CYCLE ========================================
    def _update(self, dt: float) -> None:
        """Actualisation
        
        Args:
            dt: delta-time
        """
        ...
    
    def _draw(self, pipeline: Pipeline, context: RenderContext) -> None:
        """Affichage"""
        # Construction du renderer
        if self._shape_renderer is None:
            self._shape_renderer = PygletShapeRenderer(
                geometry = self._geometry,
                filling = False,
                border_width = self._width,
                border_align = self._align,
                border_color = self._color,
                opacity = context.opacity,
                pipeline = pipeline,
                z = context.z,
                parent=context.group,
            )

        # Mise à jour du renderer
        else:
            self._shape_renderer.update(
                geometry = self._geometry,
                filling = False,
                border_width = self._width,
                border_align = self._align,
                border_color = self._color,
                opacity = context.opacity,
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