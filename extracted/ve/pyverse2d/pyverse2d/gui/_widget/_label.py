# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, positive, not_null, over
from ..._rendering import Pipeline, PygletLabelRenderer
from ...asset import Text, Color
from ...abc import Widget
from ...math import Point
from ...shape import Rect
from ...typing import HorizontalAlign

from .._context import RenderContext

from numbers import Real, Integral

# ======================================== WIDGET ========================================
class Label(Widget):
    """Composant UI simple: Texte

    Args:
        text: texte à rendre
        position: position
        anchor: ancre relative locale
        scale: facteur de redimensionnement
        rotation: rotation en degrés
        weight: graisse ('bold', 'thin', '100'…'900', ou int pyglet)
        italic: italique
        underline: couleur du soulignement
        color: couleur du texte (Color)
        opacity: opacité globale [0.0 ; 1.0]
        width: largeur de la boîte en pixels (None = pas de boîte)
        height: hauteur de la boîte en pixels (None = pas de boîte)
        multiline: autorise les \\n explicites
        line_spacing: espacement entre les lignes en pixels (None = défaut)
        wrap_lines: word-wrap automatique (nécessite width)
        align: alignement horizontal
        margin: marge intérieure uniforme en pixels
        clipping: rendu des widgets enfants strictement dans le AABB de la hitbox
    """
    __slots__ = (
        "_text", "_text_renderer",
        "_weight", "_italic", "_underline",
        "_color", "_opacity",
        "_width", "_height",
        "_multiline", "_line_spacing", "_wrap_lines",
        "_align", "_margin",
        "_hitbox_key", "_hitbox_cache",
    )
    
    def __init__(
        self,
        text: Text,
        position: Point = (0.0, 0.0),
        anchor: Point = (0.5, 0.5),
        scale: Real = 1.0,
        rotation: Real = 0.0,
        weight: str = "normal",
        italic: bool = False,
        underline: Color | None = None,
        color: Color = (255, 255, 255),
        opacity: Real = 1.0,
        width: Integral | None = None,
        height: Integral | None = None,
        multiline: bool = False,
        line_spacing: Integral | None = None,
        wrap_lines: bool = False,
        align: HorizontalAlign = "left",
        margin: Integral = 0,
        clipping: bool = False
    ):
        # Transtypage et vérifications
        weight = str(weight)
        italic = bool(italic)
        underline = Color(underline) if underline is not None else None
        color = Color(color)
        width = int(width) if width is not None else None
        height = int(height) if height is not None else None
        multiline = bool(multiline)
        line_spacing = int(line_spacing) if line_spacing is not None else None
        wrap_lines = bool(wrap_lines)
        margin = int(margin)

        if __debug__:
            expect(text, Text)
            if width is not None: over(width, 0, include=False)
            if height is not None: over(height, 0, include=False)
            if line_spacing is not None: positive(line_spacing)
            expect(align, HorizontalAlign)
            positive(margin)

        # Attributs publiques
        self._text: Text = text
        self._weight: str = weight
        self._italic: bool = italic
        self._underline: Color | None = underline
        self._color: Color = color
        self._width: int = width
        self._height: int = height
        self._multiline: bool = multiline
        self._line_spacing: int = line_spacing
        self._wrap_lines: bool = wrap_lines
        self._align: HorizontalAlign = align
        self._margin: int = margin

        # Attributs internes
        self._text_renderer: PygletLabelRenderer = None

        # Cache du AABB
        self._hitbox_key: tuple = None
        self._hitbox_cache: Rect = None

        # Initialisation du widget
        super().__init__(position, anchor, scale, rotation, opacity, clipping=clipping)

        # Hooks
        self.on_show(self._show_hook)
        self.on_hide(self._hide_hook)
    
    # ======================================== PROPERTIES ========================================
    @property
    def text(self) -> Text:
        """Texte interne à rendre

        Le texte doit être un Asset Texte
        """
        return self._text
    
    @text.setter
    def text(self, value: Text) -> None:
        if __debug__:
            expect(value, Text)
        self._text = value
        self._invalidate_scissor()

    @property
    def weight(self) -> str:
        """Graisse de la police

        La graisse doit être un string conforme à la norme CSS
        """
        return self._weight
    
    @weight.setter
    def weight(self, value: str) -> None:
        value = str(value)
        self._weight = value

    @property
    def italic(self) -> bool:
        """Mise en italique de la police

        Cette propriété fixe l'utilisation ou non de l'italique
        """
        return self._italic
    
    @italic.setter
    def italic(self, value: bool) -> None:
        value = bool(value)
        self._italic = value

    @property
    def underline(self) -> Color | None:
        """Couleur de soulignage du texte

        La couleur de soulignage doit être un Asset Color ou un tuple rgb/rgba
        Mettre à None pour ne pas souligner le texte
        """
        return self._underline
    
    @underline.setter
    def underline(self, value: Color | None) -> None:
        value = Color(value) if value is not None else None
        self._underline = value

    @property
    def color(self) -> Color:
        """Couleur d'affichage

        La couleur doit être un Asset Color ou un tuple rgb/rgba
        """
        return self._color
    
    @color.setter
    def color(self, value: Color) -> None:
        value = Color(value)
        self._color = value

    @property
    def width(self) -> int | None:
        """Largeur de la boîte de texte

        Cette propriété inclus le texte dans une boîte
        La largeur doit être un entier positif non nul
        """
        return self._width
    
    @width.setter
    def width(self, value: Integral | None) -> None:
        if value is not None:
            value = int(value)
            if __debug__:
                over(value, 0, include=False)
        self._width = value
        self._invalidate_scissor()

    @property
    def height(self) -> int | None:
        """Hauteur de la boîte de texte

        Cette propriété inclus le texte dans une boîte
        La hauteur doit être un entier positif non nul
        """
        return self._height
    
    @height.setter
    def height(self, value: Integral | None) -> None:
        if value is not None:
            value = int(value)
            if __debug__:
                over(value, 0, include=False)
        self._height = value
        self._invalidate_scissor()

    @property
    def multiline(self) -> bool:
        """Saut de lignes

        Cette propriété fixe l'utilisation du saut de lignes
        """
        return self._multiline
    
    @multiline.setter
    def multiline(self, value: bool) -> None:
        value = bool(value)
        self._multiline = value
        self._invalidate_scissor()

    @property
    def line_spacing(self) -> int | None:
        """Espacement entre les lignes

        L'espacement doit être un entier positif non nul
        """
        return self._line_spacing
    
    @line_spacing.setter
    def line_spacing(self, value: Integral | None) -> None:
        if value is not None:
            value = int(value)
            if __debug__:
                positive(value)
        self._line_spacing = value
        self._invalidate_scissor()
    
    @property
    def wrap_lines(self) -> bool:
        """Conservation des mots

        Cette propriété fixe l'utilisation de la conservation des mots
        Lorsqu'activée, les sauts de lignes se font de sorte à ne pas scinder les mots
        """
        return self._wrap_lines
    
    @wrap_lines.setter
    def wrap_lines(self, value: bool) -> None:
        value = bool(value)
        self._wrap_lines = value
        self._invalidate_scissor()

    @property
    def align(self) -> HorizontalAlign:
        """Alignement horizontal du texte

        L'alignement doit être un HorizontalAlign
        Il fixe l'alignement dans texte dans la boîte
        """
        return self._align
    
    @align.setter
    def align(self, value: HorizontalAlign) -> None:
        if __debug__:
            expect(value, HorizontalAlign)
        self._align = value

    @property
    def margin(self) -> int:
        """Marge intérieure

        Cette propriété applique un espacement entre le texte et les bordures de la boîte
        La marge doit être un entier positif non nul
        """
        return self._margin
    
    @margin.setter
    def margin(self, value: Integral) -> None:
        if __debug__:
            positive(value)
        self._margin = value
        self._invalidate_scissor()

    @property
    def hitbox(self):
        """Hitbox du label"""
        if self._hitbox_cache is None:
            return Rect(1, 1)
        return self._hitbox_cache
    
    # ======================================== INTERFACE ========================================
    def copy(self) -> Label:
        """Renvoie une copie du widget"""
        return Label(
            text = self._text,
            position = self._transform.position,
            anchor = self._transform.anchor,
            scale = self._transform.scale,
            rotation = self._transform.rotation,
            weight = self._weight,
            italic = self._italic,
            underline = self._underline,
            color = self._color,
            opacity = self._opacity,
            width = self._width,
            height = self._height,
            multiline = self._multiline,
            line_spacing = self._line_spacing,
            wrap_lines = self._wrap_lines,
            align = self._align,
            margin = self._margin,
            clipping = self._clipping,
        )
    
    # ======================================== HOOKS ========================================
    def _show_hook(self) -> None:
        """Hook d'apparition"""
        if self._text_renderer is None:
            return
        self._text_renderer.visible = True

    def _hide_hook(self) -> None:
        """Hook de disparition"""
        if self._text_renderer is None:
            return
        self._text_renderer.visible = False
        
    # ======================================== LIFE CYCLE ========================================
    def _update(self, dt: float) -> None:
        """Actualisation

        Args:
            dt: delta-time
        """
        ...

    def _draw(self, pipeline: Pipeline, context: RenderContext) -> None:
        """Affichage
        
        Args:
            pipeline: ``Pipeline`` de rendu courant
            context: contexte de rendu courant
        """
        # Construction du renderer
        if self._text_renderer is None:
            self._text_renderer = PygletLabelRenderer(
                text = self._text,
                transform = self._world_transform,
                weight = self._weight,
                italic = self._italic,
                underline = self._underline,
                color = self._color,
                opacity = context.opacity,
                width = self._width,
                height = self._height,
                multiline = self._multiline,
                wrap_lines = self._wrap_lines,
                align = self._align,
                margin = self._margin,
                line_spacing = self._line_spacing,
                z = context.z,
                pipeline = pipeline,
                parent=context.group,
            )
    
        # Mise à jour du renderer
        else:
            self._text_renderer.update(
                text = self._text,
                transform = self._world_transform,
                weight = self._weight,
                italic = self._italic,
                underline = self._underline,
                color = self._color,
                opacity = context.opacity,
                width = self._width,
                height = self._height,
                multiline = self._multiline,
                wrap_lines = self._wrap_lines,
                align = self._align,
                margin = self._margin,
                line_spacing = self._line_spacing,
                z = context.z,
                parent=context.group,
            )

        key = (self._text_renderer.content_width, self._text_renderer.content_height)
        if key != self._hitbox_key:
            self._hitbox_cache = Rect(*key)
            self._invalidate_geometry()

    def _destroy(self) -> None:
        """Libère les ressources pyglet et se détache de son parent"""
        if self._text_renderer:
            self._text_renderer.delete()
            self._text_renderer = None

# ======================================== EXPORTS ========================================
__all__ = [
    "Label",
]