# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, clamped, over, inferior_to, superior_to
from ...abc import Component
from ...math import Vector

from typing import TYPE_CHECKING
from numbers import Real

if TYPE_CHECKING:
    from .._entity import Entity

# ======================================== COMPONENT ========================================
class Follow(Component):
    """``Component`` gérant le suivi

    Ce composant est manipulé par ``SteeringSystem``.

    Args:
        entity: ``Entité`` à suivre
        offset: ``Vecteur`` de décalage par rapport à la cible
        smoothing: facteur de retard relatif [0, 1[ *(uniquement cas cinématique)*
        force: force d'attraction en Newtons *(uniquement cas dynamique)*
        damping: coefficient d'amortissement de la vélocité *(uniquement cas dynamique)*
        radius_min: borne intérieure de la zone de tolérance
        radius_max: borne extérieure de la zone de tolérance
        angle: angle cible dans la zone de tolérance
        cone: cone angulaire tolérée par rapport à l'angle cible
        cone_gap: décalage minimal par rapport à l'angle cible
        axis_x: activer le suivi horizontal
        axis_y: activer le suivi vertical
    """
    __slots__ = (
        "_entity", "_offset",
        "_smoothing", "_force", "_damping",
        "_radius_min", "_radius_max",
        "_angle", "_cone", "_cone_gap",
        "_axis_x", "_axis_y",
        "_arrived"
    )
    requires = ("Transform",)

    def __init__(
            self,
            entity: Entity,
            offset: Vector = (0.0, 0.0),
            smoothing: Real = 0.0,
            force: Real = 5000.0,
            damping: Real = 0.0,
            radius_min: Real = 0.0,
            radius_max: Real = 0.0,
            angle: Real = 0.0,
            cone: Real = 180,
            cone_gap: Real = 0.0,
            axis_x: bool = True,
            axis_y: bool = True,
        ):
        # Attributs publiques
        self._entity: Entity = entity
        self._offset: Vector = Vector(offset)
    
        self._smoothing: float = float(smoothing)
        self._force: float = float(force)
        self._damping: float = abs(float(damping))
    
        self._radius_min: float = abs(float(radius_min))
        self._radius_max: float = abs(float(radius_max))

        self._angle: float = (float(angle) + 180.0) % 360.0 - 180.0
        self._cone: float = abs(float(cone))
        self._cone_gap: float = abs(float(cone_gap))

        self._axis_x: bool = axis_x
        self._axis_y: bool = axis_y

        if __debug__:
            from .._entity import Entity
            expect(self._entity, Entity)
            if not self._entity.has("Transform"): raise ValueError(f"Entity {self._entity.id}... has no Transform component") 
            clamped(self._smoothing, include_max=False)
            over(self._force, 0.0, include=False)
            inferior_to(self._radius_min, self._radius_max)
            superior_to(self._cone, self._cone_gap)
            expect(self._axis_x, bool)
            expect(self._axis_y, bool)
            
        # Attributs internes        
        self._arrived: bool = False
        
    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du composant"""
        return f"Follow(entity={self._entity.id[:8]}..., offset={self._offset})"

    def get_attributes(self) -> tuple:
        """Renvoie les attributs du composant"""
        return (
            self._entity, self._offset,
            self._smoothing, self._force, self._damping,
            self._radius_min, self._radius_max,
            self._angle, self._cone, self._cone_gap,
            self._axis_x, self._axis_y,
        )
    
    def copy(self) -> Follow:
        """Renvoie une copie du composant"""
        new = Follow(
            self._entity, self._offset,
            self._smoothing, self._force, self._damping,
            self._radius_min, self._radius_max,
            self._angle, self._cone, self._cone_gap,
            self._axis_x, self._axis_y,
        )
        new._arrived = self._arrived
        return new

    # ======================================== PROPERTIES ========================================
    @property
    def entity(self) -> Entity:
        """Entité à suivre

        L'entité doit être un objet ``Entity`` avec un composant ``Transform``.
        """
        return self._entity

    @entity.setter
    def entity(self, value: Entity) -> None:
        from .._entity import Entity
        assert isinstance(value, Entity), f"Entity must be an instance of Entity, got {type(value).__name__}"
        assert value.has("Transform"), f"Entity {value.id}... has no Transform component"
        self._entity = value
    @property
    def offset(self) -> Vector:
        """Décalage par rapport à la cible

        Le décalage peut être un objet ``Vector`` ou un tuple ``(vx, vy)``.
        """
        return self._offset

    @offset.setter
    def offset(self, value: Vector) -> None:
        self._offset = Vector(value)

    @property
    def smoothing(self) -> float:
        """Facteur de retard

        Le facteur doit être un ``Réel`` compris dans l'intervalle [0, 1[.
        Plus la valeur est élevée, plus le suivi est progressif.
        Le facteur de retard n'est appliqué que dans le cas cinématique.
        """
        return self._smoothing

    @smoothing.setter
    def smoothing(self, value: Real) -> None:
        value = float(value)
        assert 0 <= value < 1.0, f"smoothing must be within 0.0 and 1.0, got {value}"
        self._smoothing = value

    @property
    def force(self) -> float:
        """Force d'attraction en Newtons

        La force doit être un ``Réel`` positif non nul.
        La force n'est pris en compte que dans le cas dynamique.
        """
        return self._force

    @force.setter
    def force(self, value: Real) -> None:
        value = float(value)
        assert 0 < value, f"force must be over 0.0, got {value}"
        self._force = value

    @property
    def damping(self) -> float:
        """Coefficient d'amortissement de la vélocité

        Applique une force opposée à la vélocité à chaque frame, provoquant
        une décélération progressive. Plus la valeur est élevée, plus le
        ralentissement est fort. 
        Un coefficient de 0.0 revient à ne pas appliquer d'amortissement.
        Le coefficient d'amortissement n'est appliqué que dans le cas dynamique.
        """
        return self._damping

    @damping.setter
    def damping(self, value: Real) -> None:
        self._damping = abs(float(value))

    @property
    def radius_min(self) -> float:
        """Borne intérieure de la zone de tolérance

        En dessous de cette distance, une force répulsive est appliquée.
        Un rayon de 0.0 signifie que tout point de distance inférieure à rayon_max est toléré.
        Doit être inférieur ou égal à radius_max.
        """
        return self._radius_min

    @radius_min.setter
    def radius_min(self, value: Real) -> None:
        value = abs(float(value))
        assert value <= self._radius_max, f"radius_min ({value}) cannot be superior to radius_max ({self._radius_max})"
        self._radius_min = value

    @property
    def radius_max(self) -> float:
        """Borne extérieure de la zone de tolérance

        Au delà de cette distance, une force attractive est appliquée.
        Un rayon de 0.0 signifie pile sur la cible. 
        Doit être supérieur ou égal à radius_min.
        """
        return self._radius_max

    @radius_max.setter
    def radius_max(self, value: Real) -> None:
        value = abs(float(value))
        assert value >= self._radius_min, f"radius_max ({value}) cannot be inferior to radius_min ({self._radius_min})"
        self._radius_max = value

    @property
    def angle(self) -> float:
        """Angle cible

        Cette propriété définit l'angle cible de l'anneau formé par les rayons de tolérance.
        Ne fonctionne que si radius_max est supérieur à 0.0.
        L'angle est *en degrés* dans le sens trigonométrique *(CCW)*.
        """
        return self._angle

    @angle.setter
    def angle(self, value: Real) -> None:
        self._angle = (float(value) + 180) % 360 - 180

    @property
    def cone(self) -> float:
        """Cone angulaire de tolérance par rapport à l'angle cible

        Cette propriété définit un cone angulaire dans la direction de l'angle.
        Ne fonctionne que si radius_max est supérieur à 0.0.
        Le cone angulaire est *en degrés*.
        Le cone doit être supérieur ou égale à ``cone_gap``.
        """
        return self._cone

    @cone.setter
    def cone(self, value: Real) -> None:
        value = abs(float(value))
        assert value >= self._cone_gap, f"cone ({value}) cannot be inferior to cone_gap ({self._cone_gap})"
        self._cone = value

    @property
    def cone_gap(self) -> float:
        """Cone d'écart à l'angle cible

        Cette propriété défini un angle d'écart minimal entre l'angle cible et la zone de tolérance.
        Ne fonctionne que si radius_max est supérieur à 0.0.
        L'écart est *en degrés*.
        L'écart doit être inférieur ou égale à ``cone``.
        """
        return self._cone_gap

    @cone_gap.setter
    def cone_gap(self, value: Real) -> None:
        value = abs(float(value))
        assert value <= self._cone, f"cone_gap ({value}) cannot be superior to cone ({self._cone})"
        self._cone_gap = value

    @property
    def axis_x(self) -> bool:
        """Suivi horizontal actif
        
        Si cette propriété est désactivée, la position horizontale de l'entité ne sera pas modifiée.
        """
        return self._axis_x

    @axis_x.setter
    def axis_x(self, value: bool) -> None:
        assert isinstance(value, bool) , f"axis_x must be a boolean, got {type(value).__name__}"
        self._axis_x = value

    @property
    def axis_y(self) -> bool:
        """Suivi horizontal actif
        
        Si cette propriété est désactivée, la position verticale de l'entité ne sera pas modifiée."""
        return self._axis_y

    @axis_y.setter
    def axis_y(self, value: bool) -> None:
        assert isinstance(value, bool), f"axis_y must be a boolean, got {type(value).__name__}"
        self._axis_y = value

    # ======================================== PREDICATES ========================================
    def is_arrived(self) -> bool:
        """Vérifie que la cible soit atteinte"""
        return self._arrived