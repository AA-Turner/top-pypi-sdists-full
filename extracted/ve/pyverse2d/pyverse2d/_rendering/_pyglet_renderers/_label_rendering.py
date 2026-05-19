# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...asset import Color, Text
from ..._core import Transform
from ...math import Vector

from .. import Pipeline
from .._fbo import Framebuffer

import pyglet
import pyglet.text
import pyglet.sprite
import pyglet.image
import pyglet.gl as gl
from pyglet.graphics import Group
from pyglet.math import Mat4

# ======================================== CONSTANTS ========================================
_UNSET: object = object()

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
        "_fbo", "_texture", "_sprite",
        "_fbo_w", "_fbo_h", "_world_w", "_world_h", "_last_font_px",
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

        # Objets de rendu
        self._fbo: Framebuffer = None
        self._texture: pyglet.image.Texture = None
        self._sprite: pyglet.sprite.Sprite = None
        self._label: pyglet.text.Label = None

        # Dimensions
        self._fbo_w: int = 0
        self._fbo_h: int = 0
        self._world_w: float = 0.0
        self._world_h: float = 0.0
        self._last_font_px: int = 0

        # Construction
        self._transform_version: int = self._transform.version
        self._build()

    # ======================================== INTERNALS ========================================
    def _build(self) -> None:
        """Construit le label offscreen et met à jour le FBO et le Sprite monde"""
        font = self._text.font

        # Taille framebuffer cible
        font_px: int = max(int(self._pipeline.scale_to_framebuffer(font.size * self._transform.scale)), 1)
        self._last_font_px = font_px

        # Boîte éventuelle en px framebuffer
        box_w_px = int(self._pipeline.scale_to_framebuffer(self._width  * self._transform.scale)) if self._width  is not None else None
        box_h_px = int(self._pipeline.scale_to_framebuffer(self._height * self._transform.scale)) if self._height is not None else None

        # Couleur
        r, g, b, a = self._color.rgba8 if self._color is not None else (255, 255, 255, 255)
        a = int(a * self._opacity)

        # Label
        if self._label is not None:
            self._label.delete()
        self._label = pyglet.text.Label(
            text=self._text.text,
            font_name=font.name,
            font_size=font_px,
            weight=self._weight,
            italic=self._italic,
            color=(r, g, b, a),
            anchor_x="left",
            anchor_y="bottom",
            width=box_w_px,
            height=box_h_px,
            multiline=self._multiline,
            rotation=0,
            x=0,
            y=0,
        )
        self._apply_styles()

        # FBO
        fbo_w: int = max(int(self._label.content_width),  1)
        fbo_h: int = max(int(self._label.content_height), 1)
        if self._fbo is None or self._fbo_w != fbo_w or self._fbo_h != fbo_h:
            if self._fbo is not None:
                self._fbo.delete()
            self._fbo    = Framebuffer(fbo_w, fbo_h)
            self._fbo_w  = fbo_w
            self._fbo_h  = fbo_h
            # Texture
            self._texture = pyglet.image.Texture(
                fbo_w, fbo_h,
                gl.GL_TEXTURE_2D,
                self._fbo.texture_id,
            )

        # Rendu label
        self._flush_to_fbo()

        # Taille monde du contenu
        scale = self._transform.scale
        if font_px > 0 and scale > 0:
            px_per_world     = font_px / (font.size * scale)
            self._world_w    = fbo_w / px_per_world
            self._world_h    = fbo_h / px_per_world
        else:
            self._world_w = self._world_h = 0.0

        # Sprite
        if self._sprite is None:
            self._sprite = pyglet.sprite.Sprite(
                self._texture,
                batch=self._pipeline.batch,
                group=self._pipeline.get_group(z=self._z) if self._parent is None else self._parent,
            )
        elif self._sprite.image is not self._texture:
            self._sprite.image = self._texture

        self._sprite.scale = self._world_w / fbo_w if fbo_w > 0 else 1.0
        self._refresh_transform()

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

    def _flush_to_fbo(self) -> None:
        """Re-rend le label dans le FBO sans reconstruire quoi que ce soit"""
        win = self._pipeline.window.native

        # Sauvegarde état OpenGL
        prev_fbo = (gl.GLint * 1)()
        prev_viewport = (gl.GLint * 4)()
        gl.glGetIntegerv(gl.GL_FRAMEBUFFER_BINDING, prev_fbo)
        gl.glGetIntegerv(gl.GL_VIEWPORT, prev_viewport)
        saved_proj = win.projection
        saved_view = win.view

        # Projection pixel-perfect pour le label offscreen
        win.projection = Mat4.orthogonal_projection(0.0, float(self._fbo_w), 0.0, float(self._fbo_h), -1.0, 1.0)
        win.view = Mat4()

        # Rendu
        self._fbo.bind()
        gl.glViewport(0, 0, self._fbo_w, self._fbo_h)
        gl.glClearColor(0.0, 0.0, 0.0, 0.0)
        self._fbo.clear()
        self._label.draw()

        # Restauration
        win.projection = saved_proj
        win.view = saved_view
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, prev_fbo[0])
        gl.glViewport(prev_viewport[0], prev_viewport[1], prev_viewport[2], prev_viewport[3])

    def _reflush(self) -> None:
        """Met à jour le label en place et re-flush le FBO sans reconstruire"""
        font = self._text.font
        r, g, b, a = self._color.rgba8 if self._color is not None else (255, 255, 255, 255)
        a = int(a * self._opacity)
        self._label.text = self._text.text
        self._label.color = (r, g, b, a)
        self._apply_styles()
        self._flush_to_fbo()

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
    def content_width(self) -> float: return self._world_w
    @property
    def content_height(self) -> float: return self._world_h

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
        """Met à jour le renderer label

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
        reflush: bool = False
        refresh: bool = False

        for key in changes:
            handler = getattr(self, f"_handle_{key}", None)
            if handler:
                output: str | None = handler()
                if output == "rebuild":
                    rebuild = True
                elif output == "reflush":
                    reflush = True
                elif output == "refresh":
                    refresh = True

        # Recalculs globaux 
        if rebuild:
            self._rebuild()
        elif reflush:
            self._reflush()
            self._refresh_transform()
        elif refresh:
            self._refresh_transform()

    def delete(self) -> None:
        """Libère les ressources pyglet"""
        if self._label:
            self._label.delete()
            self._label = None
        if self._sprite:
            self._sprite.delete()
            self._sprite = None
        if self._fbo:
            self._fbo.delete()
            self._fbo = None

    # ======================================== HANDLERS ========================================
    def _handle_text(self) -> str:
        """Actualisation du texte"""
        return "reflush"

    def _handle_transform(self) -> str:
        """Actualisation de la transformation"""
        font_px = max(int(self._pipeline.scale_to_framebuffer(self._text.font.size * self._transform.scale)), 1)
        if font_px != self._last_font_px:
            return "rebuild"
        return "refresh"

    def _handle_offset(self) -> str:
        """Actualisation du décalage"""
        return "refresh"

    def _handle_weight(self) -> str:
        """Actualisation de la graisse"""
        return "rebuild"

    def _handle_italic(self) -> str:
        """Actualisation de l'italique"""
        return "rebuild"

    def _handle_underline(self) -> str:
        """Actualisation du soulignement"""
        return "reflush"

    def _handle_color(self) -> str:
        """Actualisation de la couleur"""
        return "reflush"

    def _handle_opacity(self) -> str:
        """Actualisation de l'opacité"""
        return "reflush"

    def _handle_width(self) -> str:
        """Actualisation de la largeur"""
        return "rebuild"

    def _handle_height(self) -> str:
        """Actualisation de la hauteur"""
        return "rebuild"

    def _handle_multiline(self) -> str:
        """Actualisation du saut de ligne"""
        return "rebuild"

    def _handle_wrap_lines(self) -> str:
        """Actualisation de la conservation"""
        return "rebuild"

    def _handle_align(self) -> str:
        """Actualisation de l'alignement"""
        return "reflush"

    def _handle_margin(self) -> str:
        """Actualisation de la marge"""
        return "reflush"

    def _handle_line_spacing(self) -> str:
        """Actualisation de l'espacement"""
        return "reflush"

    def _handle_z(self) -> None:
        """Actualisation du z-order"""
        if self._sprite:
            self._sprite.group = self._pipeline.get_group(z=self._z) if self._parent is None else self._parent

    def _handle_parent(self) -> None:
        """Actualisation du groupe parent"""
        if self._sprite:
            self._sprite.group = self._pipeline.get_group(z=self._z) if self._parent is None else self._parent

    # ======================================== HELPERS ========================================
    def _refresh_transform(self) -> None:
        """Actualise la position et la rotation du sprite en espace monde"""
        if not self._sprite:
            return

        transform = self._transform
        anchor = transform.anchor

        anchor_dx = anchor.x * self._world_w
        anchor_dy = anchor.y * self._world_h

        if self._offset is not None:
            self._sprite.x = transform.x + self._offset.x - anchor_dx
            self._sprite.y = transform.y + self._offset.y - anchor_dy
        else:
            self._sprite.x = transform.x - anchor_dx
            self._sprite.y = transform.y - anchor_dy

        self._sprite.rotation = -transform.rotation

    def _rebuild(self) -> None:
        """Reconstruit le label avec les paramètres courants"""
        self._build()

# ======================================== EXPORTS ========================================
__all__ = [
    "PygletLabelRenderer",
]