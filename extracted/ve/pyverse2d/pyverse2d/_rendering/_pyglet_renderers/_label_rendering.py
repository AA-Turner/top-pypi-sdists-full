# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...asset import Color, Text
from ..._core import Transform
from ...math import Vector

from .. import Pipeline

import pyglet
import pyglet.text
from pyglet.graphics import Group

# ======================================== CONSTANTS ========================================
_UNSET = object()

# ======================================== PUBLIC ========================================
class PygletLabelRenderer:
    """Renderer pyglet unifié pour un label texte

    Args:
        text: texte à rendre
        transform: transformation monde
        offset: décalage au transform
        weight: graisse ('bold', 'thin', '100'…'900', ou int pyglet)
        italic: italique
        underline: couleur du soulignement
        color: couleur du texte (Color)
        opacity: opacité globale [0.0 ; 1.0]
        line_spacing: espacement entre les lignes en pixels (None = défaut)
        width: largeur de la boîte en pixels (None = pas de boîte)
        height: hauteur de la boîte en pixels (None = pas de boîte)
        multiline: autorise les \\n explicites
        wrap_lines: word-wrap automatique (nécessite width)
        align: 'left' | 'center' | 'right'
        margin: marge intérieure uniforme en pixels
        z: z-order
        pipeline: pipeline de rendu
        parent: groupe parent
    """
    __slots__ = (
        "_text",
        "_transform", "_offset",
        "_weight", "_italic", "_underline",
        "_color", "_opacity",
        "_width", "_height", "_multiline", "_wrap_lines", "_align",
        "_margin", "_line_spacing",
        "_z", "_pipeline", "_parent",
        "_transform_version", "_label",
    )

    def __init__(
        self,
        text: Text,
        transform: Transform,
        offset: Vector = None,
        weight: str | int = "normal",
        italic: bool = False,
        underline: Color = None,
        color: Color = None,
        opacity: float = 1.0,
        width: int = None,
        height: int = None,
        multiline: bool = False,
        wrap_lines: bool = True,
        align: str = "left",
        margin: int = 0,
        line_spacing: float = None,
        z: int = 0,
        pipeline: Pipeline = None,
        parent: Group = None,
    ):
        # Paramètres publics
        self._text: Text = text
        self._transform: Transform = transform
        self._offset: Vector = offset
        self._weight: str | int = weight
        self._italic: bool = italic
        self._underline: Color = underline
        self._color: Color = color
        self._opacity: float = opacity
        self._width: int = width
        self._height: int = height
        self._multiline: bool = multiline
        self._wrap_lines: bool = wrap_lines
        self._align: str = align
        self._margin: int = margin
        self._line_spacing: float = line_spacing
        self._z: int = z
        self._pipeline: Pipeline = pipeline
        self._parent: Group = parent

        # Construction
        self._transform_version: int = self._transform.version
        self._label: pyglet.text.Label = None
        self._build()

    # ======================================== INTERNALS ========================================
    def _build(self) -> None:
        """Construit le label pyglet et applique tous les styles"""
        # Font
        font = self._text.font

        # Couleur
        r, g, b, a = self._color.rgba8 if self._color is not None else (255, 255, 255, 255)
        a = int(a * self._opacity)

        # Boîte
        width = int(self._width) if self._width is not None else None
        height = int(self._height) if self._height is not None else None

        self._label = pyglet.text.Label(
            text=self._text.text,
            font_name=font.name,
            font_size=int(font.size * self._transform.scale),
            weight=self._weight,
            italic=self._italic,
            color=(r, g, b, a),
            anchor_x="left",
            anchor_y="bottom",
            width=width,
            height=height,
            multiline=self._multiline,
            rotation=-self._transform.rotation,
            batch=self._pipeline.batch,
            group=self._pipeline.get_group(z=self._z) if self._parent is None else self._parent,
        )
        self._apply_styles()
        self._refresh_position()

    def _apply_styles(self) -> None:
        """Applique les styles set_style en une passe"""
        margin = self.margin
        s = self._label.set_style
        s("wrap_lines", self._wrap_lines)
        s("align", self._align)
        s("margin_left", margin)
        s("margin_right", margin)
        s("margin_top", margin)
        s("margin_bottom", margin)
        if self._line_spacing is not None:
            s("line_spacing", self._line_spacing)
        if self._underline is not None:
            s("underline", self._underline.rgba8)

    # ======================================== GETTERS ========================================
    @property
    def text(self) -> Text: return self._text
    @property
    def transform(self) -> Transform: return self._transform
    @property
    def offset(self) -> Vector: return self._offset

    @property
    def weight(self) -> str | int: return self._weight
    @property
    def italic(self) -> bool: return self._italic
    @property
    def underline(self) -> Color: return self._underline
    @property
    def color(self) -> Color: return self._color
    @property
    def opacity(self) -> float: return self._opacity

    @property
    def width(self) -> int: return self._width
    @property
    def height(self) -> int: return self._height
    @property
    def multiline(self) -> bool: return self._multiline
    @property
    def wrap_lines(self) -> bool: return self._wrap_lines
    @property
    def align(self) -> str: return self._align
    @property
    def margin(self) -> int: return self._margin
    @property
    def line_spacing(self) -> float: return self._line_spacing

    @property
    def z(self) -> int: return self._z
    @property
    def pipeline(self) -> Pipeline: return self._pipeline
    @property
    def parent(self) -> Group: return self._parent

    @property
    def content_width(self) -> int: return self._label.content_width if self._label else 0
    @property
    def content_height(self) -> int: return self._label.content_height if self._label else 0

    # ======================================== VISIBILITY ========================================
    @property
    def visible(self) -> bool:
        """Renvoie la visibilité"""
        return self._label.visible if self._label else False
    
    @visible.setter
    def visible(self, value: bool) -> None:
        """Active ou désactive la visibilité"""
        if self._label:
            self._label.visible = value

    def is_visible(self) -> bool:
        """Vérifie la visibilité"""
        return self._label is not None and self._label.visible

    # ======================================== LIFE CYCLE ========================================
    def update(self, **kwargs) -> None:
        """
        Met à jour le renderer label

        Args:
            text: texte à rendre
            transform: transformation monde
            offset: décalage au transform
            weight: graisse ('bold', 'thin', '100'…'900', ou int pyglet)
            italic: italique
            underline: couleur du soulignement
            color: couleur du texte (Color)
            opacity: opacité globale [0.0 ; 1.0]
            line_spacing: espacement entre les lignes en pixels (None = défaut)
            width: largeur de la boîte en pixels (None = pas de boîte)
            height: hauteur de la boîte en pixels (None = pas de boîte)
            multiline: autorise les \\n explicites
            wrap_lines: word-wrap automatique (nécessite width)
            align: 'left' | 'center' | 'right'
            margin: marge intérieure uniforme en pixels
            z: z-order
            pipeline: pipeline de rendu
            parent: groupe parent
        """
        changes: set[str] = set()

        # Actualisation des paramètres
        for key, value in kwargs.items():
            current = getattr(self, f"_{key}", _UNSET)
            if current is _UNSET or value == current:
                continue
            setattr(self, f"_{key}", value)
            changes.add(key)

        # Vérification de la version du Transform
        tr_version = self._transform.version
        if tr_version != self._transform_version:
            changes.add("transform")
            self._transform_version = tr_version

        # Appel des handlers
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
        if self._label:
            self._label.delete()
            self._label = None

    # ======================================== HANDLERS ========================================
    def _handle_text(self) -> str:
        """Actualisation du text"""
        font = self._text.font
        self._label.text = self._text.text
        self._label.font_name = font.name
        return "refresh"

    def _handle_transform(self) -> str:
        """Actualisation de la transformation"""
        return "refresh"
    
    def _handle_offset(self) -> str:
        """Actualisation du décalage"""
        return "refresh"

    def _handle_weight(self) -> None:
        """Actualisation de la graisse"""
        self._label.weight = self._weight

    def _handle_italic(self) -> None:
        """Actualisation de l'italique"""
        self._label.italic = self._italic

    def _handle_underline(self) -> None:
        """Actualisation du soulignement"""
        self._label.set_style("underline", self.underline.rgba8 if self.underline else None)

    def _handle_color(self) -> None:
        """Actualisation de la couleur"""
        r, g, b, a = self._color.rgba8 if self._color is not None else (255, 255, 255, 255)
        a = int(a * self._opacity)
        self._label.color = (r, g, b, a)

    def _handle_opacity(self) -> None:
        """Actualisation de l'opacité"""
        a = self._color.a if self._color is not None else 1.0
        self._label.opacity = int(255 * a * self._opacity)

    def _handle_width(self) -> str:
        """Actualisation de la largeur"""
        self._label.width = self._width
        return "refresh"

    def _handle_height(self) -> str:
        """Actualisation de la hauteur"""
        self._label.height = self._height
        return "refresh"
    
    def _handle_multiline(self) -> str:
        """Actualisation du saut de ligne"""
        return "rebuild"
    
    def _handle_wrap_lines(self) -> str:
        """Actualisation de la conservation"""
        return "rebuild"

    def _handle_align(self) -> None:
        """Actualisation de l'alignement"""
        self._label.set_style("align", self._align)

    def _handle_margin(self) -> str:
        """Actualisation de la marge"""
        margin = self._margin
        s = self._label.set_style
        s("margin_left", margin)
        s("margin_right", margin)
        s("margin_top", margin)
        s("margin_bottom", margin)
        return "refresh"

    def _handle_line_spacing(self) -> str:
        """Actualisation de l'espacement"""
        self._label.set_style("line_spacing", self._line_spacing)
        return "refresh"

    def _handle_z(self) -> None:
        """Actualisation du z-order"""
        self._label.group = self._pipeline.get_group(z=self._z) if self._parent is None else self._parent

    def _handle_parent(self) -> None:
        """Actualisation du groupe parent"""
        self._label.group = self._pipeline.get_group(z=self._z) if self._parent is None else self._parent

    # ======================================== HELPERS ========================================
    def _refresh_transform(self) -> None:
        """Actualise la transformation monde"""
        transform = self._transform

        self._label.font_size = int(self._text.font.size * transform.scale)
        self._label.rotation = -transform.rotation

        if self._offset is not None:
            self._label.x = transform.x + self._offset.x
            self._label.y = transform.y + self._offset.y
        else:
            self._label.x = transform.x
            self._label.y = transform.y

    def _rebuild(self) -> None:
        """Reconstruit le label avec les paramètres courants"""
        self.delete()
        self._build()

# ======================================== EXPORTS ========================================
__all__ = [
    "PygletLabelRenderer",
]