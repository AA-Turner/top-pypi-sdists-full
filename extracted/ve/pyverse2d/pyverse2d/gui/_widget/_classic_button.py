# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect
from ...abc import Shape, Button
from ...math import Point

from ._surface import Surface
from ._sprite import Sprite
from ._label import Label
from ._border import Border

from numbers import Real
from typing import Callable, Any

# ======================================== WIDGET ========================================
class ClassicButton(Button):
    """Composant GUI composé: Bouton classique
    
    Args:
        background: Surface ou Sprite de fond
        label: texte du bouton
        border: bordure du bouton
        position: positionnement
        anchor: ancre relative locale
        scale: facteur de redimensionnement
        rotation: angle de rotation        
        opacity: opacité [0, 1]
        clipping: rendu des widgets enfants strictement dans le AABB de la hitbox
        callback: action au clique
        condition: condition d'action
        id: identifiant du bouton
        give_id: passe l'identifiant à l'action
    """
    __slots__ = (
        "_background", "_label", "_border",
    )

    def __init__(
            self,
            background: Surface | Sprite,
            label: Label | None = None,
            border: Border | None = None,
            position: Point = (0.0, 0.0),
            anchor: Point = (0.5, 0.5),
            scale: Real = 1.0,
            rotation: Real = 0.0,
            opacity: Real = 1.0,
            clipping: bool = False,
            callback: Callable | None = None,
            condition: Callable | None = None,
            id: Any = None,
            give_id: bool = False,
        ):
        if __debug__:
            expect(background, (Surface, Sprite))
            expect(label, (Label, None))
            expect(border, (Border, None))

        # Attributs publiques
        self._background: Surface | Sprite = background.deepcopy()
        self._label: Label | None = label.deepcopy() if label is not None else None
        self._border: Border | None = border.deepcopy() if border is not None else None

        # Initialisation du bouton
        super().__init__(position, anchor, scale, rotation, opacity, clipping,
                         callback, condition, id, give_id)

        # Ajout des enfants
        self.add_child(self._background, name="background", z=0)
        if self._label is not None:
            self.add_child(self._label, name="label", z=10)
        if self._border is not None:
            self.add_child(self._border, name="border", z=20)

    # ======================================== PROPERTIES ========================================
    @property
    def background(self) -> Surface | Sprite:
        """Fond

        Le fond peut être un widget ``Surface`` ou ``Sprite``.
        """
        return self._background
    
    @background.setter
    def background(self, value: Surface | Sprite) -> None:
        assert isinstance(value, (Surface, Sprite)), f"background ({value}) must be a Surface or a Sprite widget"
        self.remove_child(self._background)
        self._background = self.add_child(value.deepcopy(), name="background", z=0)
        self._invalidate_scissor()

    @property
    def label(self) -> Label | None:
        """Texte

        Le texte doit être un widget ``Label``.
        """
        return self._label
    
    @label.setter
    def label(self, value: Label | None) -> None:
        assert value is None or isinstance(value, Label), f"label ({value}) must be a Label widget or None"
        if self._label is not None:
            self.remove_child(self._label)
        self._label = self.add_child(value.deepcopy(), name="label", z=10) if value is not None else None            

    @property
    def border(self) -> Border | None:
        """Bordure

        La bordure doit être un widget ``Border``.
        """
        return self._border

    @border.setter
    def border(self, value: Border | None) -> None:
        assert value is None or isinstance(value, Border), f"border ({value}) must be a Border widget"
        if self._border is not None:
            self.remove_child(self._border)
        self._border = self.add_child(value.deepcopy(), name="border", z=20) if value is not None else None            

    @property
    def hitbox(self) -> Shape:
        """AABB du bouton"""
        return self._background.hitbox

    # ======================================== PREDICATES ========================================
    def collidespoint(self, point):
        """Vérifie la collision avec un point"""
        return self._background.collidespoint(point)

    # ======================================== INTERFACE ========================================
    def copy(self) -> Button:
        """Renvoie une copie du widget"""
        return Button(
            background = self._background,
            label = self._label,
            border = self._border,
            position = self._transform.position,
            anchor = self._transform.anchor,
            scale = self._transform.scale,
            rotation = self._transform.rotation,
            opacity = self._opacity,
            clipping = self._clipping,
            callback = self._callback,
            condition = self._condition,
            id = self._id,
            give_id = self._give_id,
        )