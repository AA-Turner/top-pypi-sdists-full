# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect
from ..abc import Component, System

from ._entity import Entity

from typing import Type, Callable

# ======================================== OBJECT ========================================
class World:
    """Gère le monde virtuel et l'organisation des entités"""
    def __init__(self):
        # Composants
        self._all_entities: dict[str, Entity] = {}
        self._all_systems: list[System] = []

        # Cache
        self._query_cache: dict[tuple, list[Entity]] = {}
        self._cache_dirty: bool = True

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du monde"""
        return f"World(entities={self.entity_count}, systems={self.system_count})"

    def __str__(self) -> str:
        """Renvoie une description du monde"""
        return f"World[entities: {self.entity_count}, systems: {self.system_count}]"

    def __len__(self) -> int:
        """Renvoie le nombre d'entités dans le monde"""
        return len(self._all_entities)

    # ======================================== ENTITIES ========================================
    def add_entity(self, entity: Entity):
        """
        Ajoute une entité au monde

        Args:
            entity(Entity): entité à ajouter
        """
        expect(entity, Entity)
        self._all_entities[entity.id] = entity
        entity.on_kill(self._make_remove_entity_func(entity))
        self._cache_dirty = True

    def remove_entity(self, entity: Entity):
        """
        Supprime une entité du monde

        Args:
            entity(Entity): entité à supprimer
        """
        self._all_entities.pop(entity.id, None)
        self._cache_dirty = True

    @property
    def entity_count(self) -> int:
        """Renvoie le nombre d'entités dans le monde"""
        return len(self._all_entities)

    def has_entity(self, entity: Entity) -> bool:
        """Vérifie que le monde comporte une entité donnée"""
        return expect(entity, Entity).id in self._all_entities

    def invalidate_cache(self):
        """Invalide le cache de query manuellement"""
        self._cache_dirty = True

    def query(self, *component_types: Type[Component]) -> list[Entity]:
        """
        Recherche filtrée par composants des entités.
        Résultat mis en cache jusqu'à la prochaine modification du monde.

        Args:
            component_types(Type[Component]): types des composants requis
        """
        key = component_types

        if not self._cache_dirty and key in self._query_cache:
            return self._query_cache[key]

        result = [
            entity for entity in self._all_entities.values()
            if entity.is_active() and all(entity.has(T) for T in component_types)
        ]

        if self._cache_dirty:
            self._query_cache.clear()
            self._cache_dirty = False

        self._query_cache[key] = result
        return result

    def query_tags(self, *tags: str) -> list[Entity]:
        """
        Recherche filtrée par tags des entités

        Args:
            tags(str): tags requis
        """
        return [
            entity for entity in self._all_entities.values()
            if entity.is_active() and all(entity.has_tag(t) for t in tags)
        ]

    # ======================================== SYSTEMS ========================================
    def add_system(self, system: System):
        """
        Ajoute un système au monde

        Args:
            system(System): système à ajouter
        """
        T = type(expect(system, System))

        # Exclusivité
        if system.exclusive and self.has_system(T):
            raise ValueError(f"Can only have 1 {T.__name__} component")

        # Prérequis
        for req in system.requires:
            if not any(type(s).__name__ == req for s in self._all_systems):
                raise ValueError(f"{T.__name__} requires {req}")

        # Conflits
        for conflict in system.conflicts:
            if any(type(s).__name__ == conflict for s in self._all_systems):
                raise ValueError(f"{T.__name__} conflicts with {conflict}")
        
        for i in range(len(self._all_systems)):
            if system.order < self._all_systems[i].order:
                self._all_systems.insert(i, system)
                return
        self._all_systems.append(system)

    def remove_system(self, system: System):
        """
        Supprime un système du monde

        Args:
            system(System): système à supprimer
        """
        if system in self._all_systems:
            self._all_systems.remove(expect(system, System))

    @property
    def system_count(self) -> int:
        """Renvoie le nombre de systèmes du monde"""
        return len(self._all_systems)

    def has_system(self, system_type: Type[System]) -> bool:
        """
        Vérifie que le monde comporte un système donné

        Args:
            system_type(Type[System]): type du système
        """
        return any(isinstance(s, system_type) for s in self._all_systems)

    def get_system(self, system_type: Type[System]) -> System:
        """
        Renvoie un système du monde

        Args:
            system_type(Type[System]): type du système
        """
        for s in self._all_systems:
            if isinstance(s, system_type):
                return s
        raise ValueError(f"World has no {system_type.__name__} system")
    
    # ======================================== LIFE CYCLE ========================================
    def update(self, dt: float):
        """Actualise le monde en respectant l'ordre des phases

        Args:
            dt(float): delta time en secondes
        """
        for system in self._all_systems:
            system.update(self, dt)

    # ======================================== INTERNALS ========================================
    def _make_remove_entity_func(self, entity: Entity) -> Callable[[], None]:
        """Construit un token de suppression d'entité à sa mort
        
        Args:
            entity: ``Entity`` à supprimer du monde
        """
        def remove_entity() -> None:
            output = self._all_entities.pop(entity, None)
            if output is None:
                entity.on_kill.remove(remove_entity)
        return remove_entity