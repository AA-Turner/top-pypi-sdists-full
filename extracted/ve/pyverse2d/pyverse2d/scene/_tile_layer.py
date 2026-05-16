# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, profile_section, over
from .._rendering import Pipeline, Camera
from ..abc import Layer
from ..tile import TileMap, TileRenderer

from contextlib import nullcontext
from numbers import Integral

# ======================================== LAYER ========================================
class TileLayer(Layer):
    """Layer affichant un TileMap

    Args:
        tile_map: couche de tuiles à afficher
        chunk_size: nombre de tuiles par côté d'un chunk
        clip: limitation du rendu par rapport à une autre caméra
        camera: caméra locale
    """
    __slots__ = (
        "_tile_map", "_chunk_size",
        "_clip_camera",
        "_renderer",
    )

    def __init__(
        self,
        tile_map: TileMap,
        chunk_size: Integral = 16,
        clip_camera: Camera | None = None,
        camera: Camera = None,
    ):
        # Initialisation du layer
        super().__init__(camera)

        # Transtypage et vérifications
        chunk_size = int(chunk_size)

        if __debug__:
            expect(tile_map, TileMap)
            over(chunk_size, 0, include=False)
            expect(clip_camera, (Camera, None))

        # Attributs publiques
        self._tile_map: TileMap = tile_map
        self._chunk_size: int = chunk_size
        self._clip_camera: Camera | None = clip_camera

        # Attributs internes
        self._renderer: TileRenderer = TileRenderer(self._tile_map, self._chunk_size)

    # ======================================== GETTERS ========================================
    @property
    def tile_map(self) -> TileMap:
        """TileMap assigné"""
        return self._tile_map
    
    @tile_map.setter
    def tile_map(self, value: TileMap) -> None:
        if __debug__:
            expect(value, TileMap)
        self._tile_map = value
        self._renderer.delete()
        self._renderer = TileRenderer(self._tile_map, self._chunk_size)
    
    @property
    def chunk_size(self) -> int:
        """Taille des chunks en tuiles"""
        return self._chunk_size
    
    @chunk_size.setter
    def chunk_size(self, value: Integral) -> None:
        value = int(value)
        if __debug__:
            over(value, 0, include=False)
        self._chunk_size = value
        self._renderer.delete()
        self._renderer = TileRenderer(self._tile_map, self._chunk_size)
    
    @property
    def clip_camera(self) -> Camera | None:
        """Limitation du rendu à la zone initiale par rapport à une autre caméra
        
        Cette propriété sert à notamment à éviter l'overflow du parallax.
        """
        return self._clip_camera
    
    @clip_camera.setter
    def clip_camera(self, value: Camera | None) -> None:
        if __debug__:
            expect(value, (Camera, None))
        self._clip_camera = value

    # ======================================== HOOKS========================================
    def on_start(self) -> None:
        """Activation du layer"""
        pass

    def on_stop(self) -> None:
        """Désactivation du layer"""
        self._renderer.delete()

    # ======================================== LIFE CYCLE ========================================
    def _preload(self) -> None:
        """Préchargement"""
        pass

    @profile_section("scene.tile_layer.draw")
    def _update(self, dt: float) -> None:
        """Actualisation
        
        Args:
            dt: delta-time
        """
        pass

    @profile_section("scene.tile_layer.draw")
    def _draw(self, pipeline: Pipeline) -> None:
        """Affichage
        
        Args:
            pipeline: ``Pipeline``de rendu courant
        """
        # Vérifications
        if not self._renderer.built:
            self._renderer.build()
        if not self._renderer.has_chunks:
            return

        # Frustum visible
        vx_min, vy_min, vx_max, vy_max = pipeline.visible_world_rect()

        # Region visible
        tm = self._tile_map
        tw, th = tm.tile_width, tm.tile_height
        ox, oy = tm.origin
        chunk_w = self._chunk_size * tw
        chunk_h = self._chunk_size * th
        chunk_cols = (tm.cols + self._chunk_size - 1) // self._chunk_size
        chunk_rows = (tm.rows + self._chunk_size - 1) // self._chunk_size

        cc_min = max(0, int((vx_min - ox) // chunk_w))
        cc_max = min(chunk_cols, int((vx_max - ox) // chunk_w) + 1)
        cr_min = max(0, int((vy_min - oy) // chunk_h))
        cr_max = min(chunk_rows, int((vy_max - oy) // chunk_h) + 1)

        # Génération du contexte
        if self._clip_camera:
            ctx = pipeline.scissor_world(ox + 1, oy + 1, tm.cols * tw - 2, tm.rows * th - 2, camera=self._clip_camera)
        else:
            ctx = nullcontext()

        # Rendu avec contexte
        with ctx:
            self._renderer.begin()
            self._renderer.draw_visible(cc_min, cc_max, cr_min, cr_max)
            self._renderer.end()

# ======================================== EXPORTS ========================================
__all__ = [
    "TileLayer",
]