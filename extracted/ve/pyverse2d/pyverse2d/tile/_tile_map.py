# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, over
from .._core import Positionable
from ..math import Point

from ._tile import Tile

from numbers import Real
import numpy as np
from numpy.typing import NDArray

# ======================================== CONSTANTES FLIP ========================================
FLIP_H: int = 0b001  # flip horizontal
FLIP_V: int = 0b010  # flip vertical
FLIP_D: int = 0b100  # flip diagonal

# ======================================== TILE MAP ========================================
class TileMap(Positionable):
    """Grille 2D d'identifiants de tuiles

    Args:
        tile: tileset associé à cette couche
        grid: tableau 2D d'entiers (rows, cols) ; 0 = tuile vide
        tile_width: largeur d'une tuile en pixels monde
        tile_height: hauteur d'une tuile en pixels monde
        flags: tableau 2D de flags de flip (FLIP_H, FLIP_V, FLIP_D)
        pos: position monde de l'ancre
        anchor: point d'ancrage normalisé
    """
    __slots__ = (
        "_tile", "_grid",
        "_anchor",
        "_tile_width", "_tile_height", "_flags",
    )

    def __init__(
        self,
        tile: Tile,
        grid: NDArray[np.int32],
        position: Point = Point(0.0, 0.0),
        anchor: Point = (0.0, 0.0),
        tile_width: Real = 1.0,
        tile_height: Real = 1.0,
        flags: NDArray[np.uint8] | None = None,
    ):
        # Initialisation de la position
        Positionable.__init__(self, position)

        # Transtypage et vérifications
        grid = np.asarray(grid, dtype=np.int32)
        anchor = Point(anchor)
        tile_width = float(tile_width)
        tile_height = float(tile_height)
        flags = np.asarray(flags, dtype=np.uint8) if flags is not None else np.zeros(self._grid.shape, dtype=np.uint8)

        if __debug__:
            expect(tile, Tile)
            over(tile_width, 0, include=False)
            over(tile_height, 0, include=False)

        # Attributs publiques
        self._tile: Tile = tile
        self._grid: NDArray[np.int32] = grid
        self._tile_width: float = tile_width
        self._tile_height: float = tile_height
        self._flags: NDArray[np.uint8] = flags
        self._anchor: Point = anchor

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation de la carte"""
        rows, cols = self._grid.shape
        return f"TileMap(tile={self._tile}, grid={cols}x{rows}, tile={self._tile_width}x{self._tile_height}, pos={self._pos}, anchor={self._anchor})"

    # ======================================== PROPERTIES ========================================
    @property
    def tile(self) -> Tile:
        """Renvoie le tileset associé"""
        return self._tile

    @property
    def grid(self) -> NDArray[np.int32]:
        """Renvoie la grille brute"""
        return self._grid
    
    @property
    def anchor(self) -> Point:
        """Point d'ancrage"""
        return self._anchor
    
    @anchor.setter
    def anchor(self, value: Point) -> None:
        self._anchor.x, self._anchor.y = value
    
    @property
    def anchor_x(self) ->float:
        """Ancrage horizontal"""
        return self._anchor.x
    
    @anchor_x.setter
    def value(self, value: Real) -> None:
        self._anchor.x = value
    
    @property
    def anchor_y(self) -> float:
        """Ancrage vertical"""
        return self._anchor.y
    
    @anchor_y.setter
    def anchor_y(self, value: Real) -> None:
        self._anchor.y = value

    @property
    def flags(self) -> NDArray[np.uint8]:
        """Renvoie le tableau de flags"""
        return self._flags

    @property
    def tile_width(self) -> float:
        """Renvoie la largeur d'une tuile en pixels monde"""
        return self._tile_width

    @property
    def tile_height(self) -> float:
        """Renvoie la hauteur d'une tuile en pixels monde"""
        return self._tile_height

    @property
    def cols(self) -> int:
        """Renvoie le nombre de colonnes"""
        return self._grid.shape[1]

    @property
    def rows(self) -> int:
        """Renvoie le nombre de lignes"""
        return self._grid.shape[0]

    @property
    def pixel_width(self) -> float:
        """Renvoie la largeur totale de la map en pixels monde"""
        return self.cols * self._tile_width

    @property
    def pixel_height(self) -> float:
        """Renvoie la hauteur totale de la map en pixels monde"""
        return self.rows * self._tile_height

    @property
    def origin(self) -> tuple[float, float]:
        """Renvoie le coin bas-gauche de la map en coordonnées monde"""
        ox = self._pos.x - self._anchor[0] * self.pixel_width
        oy = self._pos.y - self._anchor[1] * self.pixel_height
        return ox, oy

    # ======================================== INTERFACE ========================================
    def tile_at(self, col: int, row: int) -> int:
        """Renvoie l'ID de la tuile à ``(col, row)``, ou 0 si hors limites

        Args:
            col: colonne
            row: ligne
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return int(self._grid[row, col])
        return 0

    def flags_at(self, col: int, row: int) -> int:
        """Renvoie les flags de flip de la tuile à ``(col, row)``, ou 0 si hors limites

        Args:
            col: colonne
            row: ligne
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return int(self._flags[row, col])
        return 0

    # ======================================== CONVERSIONS ========================================
    def world_to_tile(self, x: float, y: float) -> tuple[int, int]:
        """Convertit une position monde en ``(col, row)``

        Args:
            x: coordonnée horizontale monde
            y: coordonnée verticale monde
        """
        ox, oy = self.origin
        return int((x - ox) // self._tile_width), int((y - oy) // self._tile_height)

    def tile_to_world(self, col: int, row: int) -> tuple[float, float]:
        """Convertit ``(col, row)`` en position monde *(coin bas-gauche de la tuile)*

        Args:
            col: colonne
            row: ligne
        """
        ox, oy = self.origin
        return ox + col * self._tile_width, oy + row * self._tile_height

    def tiles_in_region(self, x: float, y: float, width: float, height: float) -> tuple[int, int, int, int]:
        """Renvoie la plage de tuiles ``(col_min, row_min, col_max, row_max)`` couvrant la région monde

        Args:
            x: coin gauche de la région
            y: coin bas de la région
            width: largeur de la région
            height: hauteur de la région
        """
        ox, oy = self.origin
        col_min = max(0, int((x - ox) // self._tile_width))
        row_min = max(0, int((y - oy) // self._tile_height))
        col_max = min(self.cols, int((x + width - ox) // self._tile_width) + 1)
        row_max = min(self.rows, int((y + height - oy) // self._tile_height) + 1)
        return col_min, row_min, col_max, row_max
    
# ======================================== EXPORTS ========================================
__all__ = [
    "TileMap",
]