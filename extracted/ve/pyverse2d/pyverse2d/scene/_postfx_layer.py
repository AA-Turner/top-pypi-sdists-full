# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, profile_section
from .._rendering import Pipeline, Camera
from .._flag import Activity
from ..abc import Layer
from ..fx.postfx import PostFxZone, PostFxRenderer
from ..fx.postfx._wave import WavePostFxRenderer

from typing import ClassVar

# ======================================== LAYER ========================================
class PostFxLayer(Layer):
    """Layer appliquant des effets post-processing par zones dans l'espace monde

    Args:
        camera: caméra locale
    """
    __slots__ = (
        "_zones", "_active_zones",
        "_renderer",
    )

    _IS_FX: ClassVar[bool] = True

    def __init__(self, camera: Camera = None):
        # Initialisation du layer
        super().__init__(camera)

        # Attributs internes
        self._zones: set[PostFxZone] = set()
        self._active_zones: list[PostFxZone] = []

        # Renderer
        self._renderer: PostFxRenderer = PostFxRenderer()

    # ======================================== ZONES ========================================
    def add_zone(self, zone: PostFxZone) -> None:
        """Ajoute une zone d'effet

        Args:
            zone: zone à ajouter
        """
        if __debug__:
            expect(zone, PostFxZone)
        self._zones.add(zone)
        if zone.is_enabled():
            self._active_zones.append(zone)

    def remove_zone(self, zone: PostFxZone) -> None:
        """Retire une zone d'effet

        Args:
            zone: zone à retirer
        """
        if zone.is_enabled():
            try:
                self._active_zones.remove(zone)
            except ValueError:
                pass
        self._zones.discard(zone)

    def get_zones(self) -> set[PostFxZone]:
        """Renvoie l'ensemble des zones *(lecture seule)*"""
        return self._zones

    # ======================================== HOOKS ========================================
    def on_start(self) -> None:
        """Activation du layer"""
        pass

    def on_stop(self) -> None:
        """Désactivation du layer"""
        pass

    # ======================================== LIFE CYCLE ========================================
    def _preload(self) -> None:
        """Préchargement spécialisé"""
        pass

    @profile_section("scene.postfx_layer.update")
    def _update(self, dt: float) -> None:
        """Actualisation

        Args:
            dt: delta-time
        """
        WavePostFxRenderer.tick(dt)
        for zone in self._zones:
            state: Activity = zone.update(dt)
            if state is Activity.DEFAULT:
                continue
            if state is Activity.ENABLED:
                self._active_zones.append(zone)
            elif state is Activity.DISABLED:
                try:
                    self._active_zones.remove(zone)
                except ValueError:
                    pass

    @profile_section("scene.postfx_layer.draw")
    def _draw(self, pipeline: Pipeline) -> None:
        """Affichage

        Args:
            pipeline: ``Pipeline`` de rendu courant
        """
        if not self._active_zones:
            return
        self._renderer.render(pipeline, self._active_zones)

# ======================================== EXPORTS ========================================
__all__ = [
    "PostFxLayer",
]