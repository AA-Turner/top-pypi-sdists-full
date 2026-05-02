# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, HasPosition
from ...abc import System

from .._world import World
from .._component import SoundEmitter, Transform

# ======================================== SYSTEM ========================================
class SoundSystem(System):
    """Système gérant les composants ``SoundEmitter``

    Ce système est automatiquement ajouté à la scène.

    Args:
        origin: référentiel de position pour les sons (généralement la caméra)
    """
    __slots__ = ("_origin")

    order = 110
    exclusive = False

    def __init__(self, origin: HasPosition):
        self._origin: HasPosition = origin

        if __debug__:
            expect(origin, HasPosition)

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du système"""
        return f"SoundSystem(origin={(self._origin.x, self._origin.y)})"
    
    # ======================================== LIFE CYCLE ========================================
    def update(self, world: World, dt: float) -> None:
        """Met à jour les sons émis"""
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