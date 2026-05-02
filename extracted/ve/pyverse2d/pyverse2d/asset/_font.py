# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect
from ..abc import Asset

import pyglet
import os
import sys
import winreg
import importlib.resources as resources

from numbers import Real
from pyglet.font.base import Font as PygletFont

# ======================================== OBJET ========================================
class Font(Asset):
    """
    Descripteur de police

    Args:
        name(str): nom ou path de la police
        size(int, optional): taille de la police
    """
    __slots__ = ("_name", "_size", "_glyph_cache", "_pyglet_font")

    def __init__(self, name: str = None, size: int = 16):
        # Paramètres
        self._size: int = expect(size, int)
        self._glyph_cache: dict[str, Glyph] = {}

        # Chargement de la police
        if name and name.lower().endswith((".ttf", ".otf")):
            # Path
            try:
                pyglet.font.add_file(name)
                loaded_font = pyglet.font.load(os.path.splitext(os.path.basename(name))[0], self._size)
                self._name: str = loaded_font.name
                self._pyglet_font: PygletFont = loaded_font

            # Fallback
            except Exception:
                self._name: str | None = None
                self._pyglet_font: PygletFont = self._load_default_font()

        # SysFont
        elif name:
            loaded_font = pyglet.font.load(name, self._size)
            self._name: str = loaded_font.name
            self._pyglet_font: PygletFont = loaded_font

        # Default Font
        else:
            self._pyglet_font: PygletFont = self._load_default_font()
            self._name: str = self._pyglet_font.name

    # ======================================== CONVERSION ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation de la police"""
        return f"Font(name={self._name}, size={self._size})"

    # ======================================== GETTERS ========================================
    @property
    def name(self) -> str:
        """Renvoie le nom de la police"""
        return self._name

    @property
    def size(self) -> int:
        """Renvoie la taille de la police"""
        return self._size

    @property
    def ascent(self) -> int:
        """Renvoie le dépassement haut de la police"""
        return self._pyglet_font.ascent

    @property
    def descent(self) -> int:
        """Renvoie le dépassement bas de la police"""
        return self._pyglet_font.descent

    @property
    def native(self) -> PygletFont:
        """Renvoie la font pyglet"""
        return self._pyglet_font

    @classmethod
    def get_fonts(cls) -> list[str]:
        """Retourne la liste des polices disponibles sur le système"""
        found = {}
        def _scan_dir(directory):
            if not os.path.isdir(directory):
                return
            for _, _, files in os.walk(directory):
                for f in files:
                    if f.lower().endswith((".ttf", ".otf")):
                        name = os.path.splitext(f)[0]
                        found[name.lower().replace(" ", "")] = name

        if sys.platform == "win32":
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts")
                i = 0
                while True:
                    try:
                        name, _, _ = winreg.EnumValue(key, i)
                        clean = name.split("(")[0].strip()
                        found[clean.lower().replace(" ", "")] = clean
                        i += 1
                    except OSError:
                        break
            except OSError:
                _scan_dir(os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts"))

        elif sys.platform == "darwin":
            for d in [
                "/Library/Fonts",
                "/System/Library/Fonts",
                "/Network/Library/Fonts",
                os.path.expanduser("~/Library/Fonts"),
            ]:
                _scan_dir(d)

        else:  # Linux
            for d in [
                "/usr/share/fonts",
                "/usr/local/share/fonts",
                "/usr/X11R6/lib/X11/fonts",
                os.path.expanduser("~/.fonts"),
                os.path.expanduser("~/.local/share/fonts"),
            ]:
                _scan_dir(d)

        return sorted(found.values())

    # ======================================== PUBLIC METHODS ========================================
    def text_width(self, text: str) -> int:
        """
        Renvoie la largeur théorique d'un texte

        Args:
            text(str): texte à vérifier
        """
        return sum(self._get_glyph(c).advance for c in text)

    def text_height(self, text: str) -> int:
        """
        Renvoie la hauteur théorique d'un texte

        Args:
            text(str): texte à vérifier
        """
        return max(self._get_glyph(c).height for c in text)

    def clip_text(self, text: str, max_width: Real, suffix: str = "") -> str:
        """
        Retourne le texte tronqué pour rentrer dans max_width

        Args:
            text(str): texte à tronquer
            max_width(Real): largeur maximale du texte (en px)
            suffix(str, optional): suffixe de tronquage
        """
        if not text: return ""

        suffix_width = self.text_width(suffix) if suffix else 0
        effective_width = max_width - suffix_width
        if effective_width <= 0:
            return suffix if suffix else ""

        lo = 0
        hi = len(text)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.text_width(text[:mid]) <= effective_width:
                lo = mid
            else:
                hi = mid - 1

        if lo < len(text) and suffix:
            return text[:lo] + suffix
        return text[:lo]

    # ======================================== INTERNALS ========================================
    def _load_default_font(self) -> PygletFont:
        """Charge la police par défaut (FreeSans)"""
        with resources.path("pyverse2d._assets", "freesansbold.ttf") as path:
            pyglet.font.add_file(str(path))
            return pyglet.font.load("FreeSans", self._size)

    def _get_glyph(self, char: str) -> Glyph:
        """Renvoie un Glyph"""
        if char not in self._glyph_cache:
            pyglet_glyph = self._pyglet_font.get_glyphs(char)[0]
            self._glyph_cache[char] = Glyph(
                advance=pyglet_glyph.advance,
                width=pyglet_glyph.width,
                height=pyglet_glyph.height,
                tex_coords=getattr(pyglet_glyph, "tex_coords", None)
            )
        return self._glyph_cache[char]

# ======================================== GLYPH OBJECT ========================================
class Glyph:
    """Stocke les informations essentielles d'un glyphe"""
    def __init__(self, advance, width, height, tex_coords=None):
        self.advance = advance
        self.width = width
        self.height = height
        self.tex_coords = tex_coords