# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, HasPosition, profile_section
from ...abc import System

from .._world import World
from .._component import SoundEmitter, Transform

from typing import ClassVar

# ======================================== SYSTEM ========================================
class SoundSystem(System):
    """Système gérant les composants ``SoundEmitter``

    Ce système est automatiquement ajouté à la scène.

    Args:
        origin: référentiel de position pour les sons *(généralement la caméra)*
    """
    __slots__ = ("_origin",)

    _ORDER: ClassVar[int] = 110

    _IS_EXCLUSIVE: ClassVar[bool] = False

    def __init__(self, origin: HasPosition):
        # Vérifications
        if __debug__:
            expect(origin, HasPosition)

        # Attributs publiques
        self._origin: HasPosition = origin

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du système"""
        return f"SoundSystem(origin={(self._origin.x, self._origin.y)})"
    
    # ======================================== PROPERTIES ========================================
    @property
    def origin(self) -> HasPosition:
        """Référentiel d'écoute des sons
        
        Cette propriété définie le point de référence spatial pour l'atténuation du volume sonore.
        """
        return self._origin
    
    @origin.setter
    def origin(self, value: HasPosition) -> None:
        if __debug__:
            expect(value, HasPosition)
        self._origin = value
    
    # ======================================== LIFE CYCLE ========================================
    @profile_section("world.sound.update")
    def update(self, world: World, dt: float) -> None:
        """Met à jour les sons émis
        
        Args:
            world: monde à actualiser
            dt: delta-time
        """
        for entity in world.query(SoundEmitter):
            se: SoundEmitter = entity.sound_emitter
            tr: Transform | None = entity.transform
            
            # Calcul de la distance à l'origine
            if tr is None:  # Cas générique
                distance = 0.0
            else:           # Cas positionnel
                distance = ((tr.x - self._origin.x) ** 2 + (tr.y - self._origin.y) ** 2) ** 0.5

            # Calcul du volume distantiel
            if se.outer_radius == 0.0 or distance <= se.inner_radius:
                volume = 1.0
            elif distance > se.outer_radius:
                volume = 0.0
            else:
                volume = 1.0 - (distance - se.inner_radius) / (se.outer_radius - se.inner_radius)
            volume *= se.volume
            
            # Actualisation des sons en cours de lecture
            for handle in se._playing:
                handle.play_volume = volume

            # Lecture des sons à jouer
            for request in se._to_play:
                handle = request.sound.play(volume=volume, loop=request.loop, limit=request.limit, on_end=se._remove_handle)
                if handle is not None:
                    se._add_handle(handle)
            se._to_play.clear()

# ======================================== EXPORTS ========================================
__all__ = [
    "SoundSystem",
]