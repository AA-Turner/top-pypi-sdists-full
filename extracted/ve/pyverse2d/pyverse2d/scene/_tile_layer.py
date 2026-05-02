# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect
from .._rendering import Pipeline, Camera
from ..abc import Layer
from ..tile import TileMap, TileRenderer

from contextlib import nullcontext

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
        chunk_size: int = 16,
        clip_camera: Camera | None = None,
        camera: Camera = None,
    ):
        super().__init__(camera)

        # TileMap
        self._tile_map: TileMap = expect(tile_map, TileMap)
        self._chunk_size: int = max(1, expect(chunk_size, int))
        self._clip_camera: Camera | None = expect(clip_camera, (Camera, None))

        # Rendu
        self._renderer: TileRenderer = TileRenderer(self._tile_map, self._chunk_size)

    # ======================================== GETTERS ========================================
    @property
    def tile_map(self) -> TileMap:
        """TileMap assigné"""
        return self._tile_map
    
    @tile_map.setter
    def tile_map(self, value: TileMap) -> None:
        self._tile_map = expect(value, TileMap)
        self._renderer.delete()
        self._renderer = TileRenderer(self._tile_map, self._chunk_size)
    
    @property
    def chunk_size(self) -> int:
        """Taille des chunks en tuiles"""
        return self._chunk_size
    
    @chunk_size.setter
    def chunk_size(self, value: int) -> None:
        self._chunk_size = max(1, expect(value, int))
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
        self._clip_camera = expect(value, (Camera, None))

    # ======================================== HOOKS========================================
    def on_start(self) -> None:
        """Activation du layer"""
        ...

    def on_stop(self) -> None:
        """Désactivation du layer"""
        self._renderer.delete()

    # ======================================== LIFE CYCLE ========================================
    def _preload(self) -> None:
        """Préchargement"""
        pass

    def _update(self, dt: float) -> None:
        """Actualisation"""
        ...

    def _draw(self, pipeline: Pipeline) -> None:
        """Affuchage"""
        if not self._renderer.built:
            self._renderer.build()
        if not self._renderer.has_chunks:
            return

        # Frustum visible (world space)
        vx_min, vy_min, vx_max, vy_max = pipeline.visible_world_rect()

        # Region visible (tilemap)
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