# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect
from ...abc import Component, Shape
from ...math import Point, Vector

# ======================================== COMPONENT ========================================
class Collider(Component):
    """Composant gérant la hitbox

    Ce composant est manipulé par ``CollisionSystem``.

    Args:
        shape(Shape): forme de la hitbox
        offset(Point, optional): décalage par rapport au Transform
        category(int, optional): catégorie binaire de collision
        mask(int, optional): masque binaire de collision
        trigger(bool, optional): collision fantôme
        active(bool, optional): collision active
    """
    __slots__ = (
        "_shape", "_offset", "_category", "_mask", "_trigger", "_active",
        "_contacts", "_coyote_elapsed", "_dirty_shape",
    )

    requires = ("Transform",)
    _COYOTE_TIME = 0.1  # temps avant perte du contact

    def __init__(
            self,
            shape: Shape,
            offset: Vector = (0.0, 0.0),
            category: int = 0b00000001,
            mask: int = 0b11111111,
            trigger: bool = False,
            active: bool = True,
        ):
        # Transtypage
        offset = Vector(offset)

        if __debug__:
            expect(shape, Shape)
            expect(category, int)
            expect(mask, int)
            expect(trigger, bool)
            expect(active, bool)

        # Attributs publiques
        self._shape: Shape = shape
        self._offset: Vector = offset
        self._category: int = category
        self._mask: int = mask
        self._trigger: bool = trigger
        self._active: bool = active

        # Attributs internes
        self._contacts: dict[Collider, Vector] = {}
        self._coyote_elapsed: float = 0.0
        self._dirty_shape: bool = True
    
    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du composant"""
        return f"Collider(category={self._category}, mask={self._mask}, trigger={self._trigger}, active={self._active})"
    
    def get_attributes(self) -> tuple:
        """Renvoie les attributs du composant"""
        return (self._shape, self._offset, self._category, self._mask, self._trigger, self._active)
    
    def copy(self) -> Collider:
        """Renvoie une copie du composant"""
        new = Collider(self._shape, self._offset, self._category, self._mask, self._trigger, self._active)
        return new
    
    # ======================================== PROPERTIES ========================================
    @property
    def shape(self) -> Shape:
        """Forme de la hitbox *(Immuable)*"""
        return self._shape
    
    @property
    def offset(self) -> Vector:
        """Décalage par rapport au ``Transform``
        
        Le décalage peut être un objet ``Vector`` ou n'importe quel tuple ``(vx, vy)``.
        """
        return self._offset
    
    @offset.setter
    def offset(self, value: Vector) -> None:
        self._offset.x, self._offset.y = value
    
    @property
    def category(self) -> int:
        """Catégorie binaire de collision
        
        Cette propriété définie la catégorie à laquelle appartient le ``Collider``.
        Par défaut cette propriété est fixe à *0b00000001*.
        """
        return self._category
    
    @category.setter
    def category(self, value: int) -> None:
        if __debug__:
            expect(value, int)
        self._category = value
    
    @property
    def mask(self) -> int:
        """Masque binaire de collision
        
        Cette propriété définie avec quelles catégories le ``Collider`` peut entrer en contact.
        Par défaut toutes les catégories sont acceptées *0b11111111*.
        """
        return self._mask
    
    @mask.setter
    def mask(self, value: int) -> None:
        if __debug__:
            expect(value, int)
        self._mask = value
    
    # ======================================== PREDICATES ========================================
    def is_trigger(self) -> bool:
        """Vérifie si la collision est fantôme"""
        return self._trigger

    def is_active(self) -> bool:
        """Vérifie que la hitbox soit active"""
        return self._active
    
    def collides_with(self, other: Collider) -> bool:
        """Vérification la possibilité de collision avec un autre collider"""
        return bool(self._mask & other._category)
    
    def collides(self, other: Collider) -> bool:
        """Vérifie la collision avec un autre collider"""
        return other in self._contacts

    # ======================================== INTERFACE ========================================
    def activate(self):
        """Active la collision"""
        self._active = True

    def deactivate(self):
        """Désactive la collision"""
        self._active = False

    def get_contacts(self) -> dict[Collider, Vector]:
        """Renvoie le dictionnaire des contactes et de la normale de collision"""
        return self._contacts

    def collision_normal(self, other: Collider) -> Vector | None:
        """Renvoie la normale de collision avec un autre ``Collider``"""
        if other is self._contacts:
            return self._contacts[other]
        return None