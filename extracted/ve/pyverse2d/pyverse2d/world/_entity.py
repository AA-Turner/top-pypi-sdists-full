# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect

from ..abc import Component

from ._component import *

import uuid
from typing import Type

# ======================================== CONSTANTS ========================================
_COMPONENTS: dict[Component, str] = {
    Transform: "_transform",
    Follow: "_follow",
    Collider: "_collider",
    RigidBody: "_rigid_body",
    GroundSensor: "_ground_sensor",
    ShapeRenderer: "_shape_renderer",
    SpriteRenderer: "_sprite_renderer",
    TextRenderer: "_text_renderer",
    Animator: "_animator",
    SoundEmitter: "_sound_emitter",
}

# ======================================== OBJECT ========================================
class Entity:
    """
    Classe représentant les entités en accumulant des composants

    Args:
        components(Component, optional): ensemble des composants de l'entité
        tags(Iterable[str], optional): labels de l'entité
    """
    __slots__ = (
        "_id", "_tags", "_active",
        *_COMPONENTS.values()
        )

    def __init__(self, *components: Component, tags: tuple[str, ...] = ()):
        # Attributs
        self._id: str = str(uuid.uuid4())
        self._tags: set[str] = set(tags)
        self._active: bool = True

        # Composants
        self._transform: Transform = None
        self._follow: Follow = None
        self._shape_renderer: ShapeRenderer = None
        self._sprite_renderer: SpriteRenderer = None
        self._text_renderer: TextRenderer = None
        self._collider: Collider = None
        self._rigid_body: RigidBody = None
        self._ground_sensor: GroundSensor = None
        self._animator: Animator = None
        self._sound_emitter: SoundEmitter = None

        # Ajouts
        for component in components:
            self.add(component)
    
    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation de l'entité"""
        components = ", ".join(str(component) for c in _COMPONENTS.values() if (component := getattr(self, c)) is not None)
        return f"Entity(id={self._id[:8]}..., tags={self._tags}, components=[{components}])"
    
    def __hash__(self) -> int:
        """Renvoie l'entier hashé de l'entité"""
        return hash(self._id)
    
    # ======================================== PROPERTIES ========================================
    @property
    def id(self) -> str:
        """Renvoie l'identifiant de l'entité"""
        return self._id
    
    @property
    def tags(self) -> set[str]:
        """Renvoie les labels de l'entité"""
        return self._tags
    
    @property
    def transform(self) -> Transform | None:
        """composant ``Transform``"""
        return self._transform
    
    @transform.setter
    def transform(self, value: Transform) -> None:
        self._transform = expect(value, Transform)
    
    @property
    def follow(self) -> Follow | None:
        """composant ``Follow``"""
        return self._follow
    
    @follow.setter
    def follow(self, value: Follow) -> None:
        self._follow = expect(value, Follow)
    
    @property
    def shape_renderer(self) -> ShapeRenderer | None:
        """composant ``ShapeRenderer``"""
        return self._shape_renderer
    
    @shape_renderer.setter
    def shape_renderer(self, value: ShapeRenderer) -> None:
        self._shape_renderer = expect(value, ShapeRenderer)
    
    @property
    def sprite_renderer(self) -> SpriteRenderer | None:
        """composant ``SpriteRenderer``"""
        return self._sprite_renderer
    
    @sprite_renderer.setter
    def sprite_renderer(self, value: SpriteRenderer) -> None:
        self._sprite_renderer = expect(value, SpriteRenderer)
    
    @property
    def text_renderer(self) -> TextRenderer | None:
        """composant ``TextRenderer``"""
        return self._text_renderer
    
    @text_renderer.setter
    def text_renderer(self, value: TextRenderer) -> None:
        self._text_renderer = expect(value, TextRenderer)
    
    @property
    def collider(self) -> Collider | None:
        """composant ``Collider``"""
        return self._collider
    
    @collider.setter
    def collider(self, value: Collider) -> None:
        self._collider = expect(value, Collider)
    
    @property
    def rigid_body(self) -> RigidBody | None:
        """composant ``RigidBody``"""
        return self._rigid_body
    
    @rigid_body.setter
    def rigid_body(self, value: RigidBody) -> None:
        self._rigid_body = expect(value, RigidBody)
    
    @property
    def ground_sensor(self) -> GroundSensor | None:
        """composant ``GroundSensor``"""
        return self._ground_sensor
    
    @ground_sensor.setter
    def ground_sensor(self, value: GroundSensor) -> None:
        self._ground_sensor = expect(value, GroundSensor)
    
    @property
    def animator(self) -> Animator | None:
        """composant ``Animator``"""
        return self._animator
    
    @animator.setter
    def animator(self, value: Animator) -> None:
        self._animator = expect(value, Animator)
    
    @property
    def sound_emitter(self) -> SoundEmitter | None:
        """composant ``SoundEmitter``"""
        return self._sound_emitter
    
    @sound_emitter.setter
    def sound_emitter(self, value: SoundEmitter) -> None:
        self._sound_emitter = expect(value, SoundEmitter)

    # ======================================== PREDICATES ========================================
    def __eq__(self, other: Entity) -> bool:
        """Vérifie la correspondance de deux entités"""
        if isinstance(other, Entity):
            return self._id == other._id
        return False
    
    def is_active(self) -> bool:
        """Vérifie l'activité de l'entité"""
        return self._active
    
    # ======================================== INTERFACE ========================================
    def activate(self):
        """Active l'entité"""
        self._active = True

    def deactivate(self):
        """Désactive l'entité"""
        self._active = False
    
    # ======================================== COMPONENTS ========================================
    def add(self, component: Component) -> Entity:
        """
        Ajoute un composant à l'entité

        Args:
            component(Component): composant à ajouter
        """
        T = type(expect(component, Component))
        all_types = self.get_all_types()

        # Exclusivité
        if T in all_types:
            raise ValueError(f"Can only have 1 {T.__name__} component")

        # Prérequis
        for req in component.requires:
            if not any(c.__name__ == req for c in all_types):
                raise ValueError(f"{T.__name__} requires {req}")

        # Conflits
        for conflict in component.conflicts:
            if any(c.__name__ == conflict for c in all_types):
                raise ValueError(f"{T.__name__} conflicts with {conflict}")
            
        setattr(self, _COMPONENTS[T], component)
        return self
    
    def remove(self, component_type: Type[Component] | str) -> Entity:
        """
        Supprime un composant de l'entité

        Args:
            component_type(Type[Component]): type du composant
        """
        if isinstance(component_type, str):
            if component_type not in _COMPONENTS:
                raise ValueError(f"Entity has no {component_type} component")
            setattr(self, component_type, None)
        else:
            if component_type not in self.get_all_types():
                raise ValueError(f"Entity has no {component_type} component")
            setattr(self, _COMPONENTS[component_type], None)
        return self
    
    def get(self, component_type: Type[Component] | str) -> Component:
        """
        Renvoie un composant de l'entité

        Args:
            component_type(Type[Component]): type du composant
        """
        if isinstance(component_type, str):
            return getattr(self, component_type, None)
        return getattr(self, _COMPONENTS[component_type], None)
    
    def get_all(self) -> tuple[Component, ...]:
        """Renvoie l'ensemble des composants de l'entité"""
        return tuple(component for name in _COMPONENTS.values() if (component := getattr(self, name)) is not None)
    
    def get_all_types(self) -> tuple[Component, ...]:
        """Renvoie l'ensemble des types de composant possédés"""
        return tuple(T for T in _COMPONENTS if getattr(self, _COMPONENTS[T]) is not None)
    
    def has(self, component_type: Type[Component] | str) -> bool:
        """
        Vérifie la possession d'un composant

        Args:
            component_type(Type[C]): type du composant
        """
        if type(component_type) is str:
            attr_name = f"_{component_type.lower()}"
        else:
            attr_name = _COMPONENTS.get(component_type)
            if attr_name is None:
                return False
        return getattr(self, attr_name) is not None
    
    # ======================================== TAGS ========================================
    def add_tag(self, tag: str) -> Entity:
        """
        Ajoute un label à l'entité

        Args:
            tag(str): label à ajouter
        """
        self._tags.add(expect(tag, str))
        return self
    
    def remove_tag(self, tag: str) -> Entity:
        """
        Supprime un label de l'entité

        Args:
            tag(str): label à supprimer
        """
        self._tags.discard(expect(tag, str))
        return self
    
    def has_tag(self, tag: str) -> bool:
        """
        Vérifie que l'entité possède un label

        Args:
            tag(str): label à vérifier
        """
        return expect(tag, str) in self._tags