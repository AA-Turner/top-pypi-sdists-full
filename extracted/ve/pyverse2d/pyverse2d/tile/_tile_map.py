# ======================================== IMPORTS ========================================
from __future__ import annotations

from ._tile import Tile

from .._internal import expect, positive
from ..math import Point

from numbers import Real
import numpy as np
from numpy.typing import NDArray

# ======================================== CONSTANTES FLIP ========================================
FLIP_H = 0b001  # flip horizontal
FLIP_V = 0b010  # flip vertical
FLIP_D = 0b100  # flip diagonal (rotation 90°)

# ======================================== TILE MAP ========================================
class TileMap:
    """
    Grille 2D d'identifiants de tuiles

    Args:
        tile(Tile): tileset associé à cette couche
        grid(NDArray): tableau 2D d'entiers (rows, cols) ; 0 = tuile vide
        tile_width(Real): largeur d'une tuile en pixels monde
        tile_height(Real): hauteur d'une tuile en pixels monde
        flags(NDArray, optional): tableau 2D de flags de flip (FLIP_H, FLIP_V, FLIP_D)
        pos(Point, optional): position monde de l'ancre
        anchor(Point, optional): point d'ancrage en [0, 1] ; (0, 0) = coin bas-gauche, (0.5, 0.5) = centre
    """
    __slots__ = ("_tile", "_grid", "_flags", "_tile_width", "_tile_height", "_pos", "_anchor")

    def __init__(
        self,
        tile: Tile,
        grid: NDArray[np.int32],
        tile_width: Real,
        tile_height: Real,
        flags: NDArray[np.uint8] | None = None,
        pos: Point = Point(0.0, 0.0),
        anchor: Point = (0.0, 0.0),
    ):
        self._tile: Tile = expect(tile, Tile)
        self._grid: NDArray[np.int32] = np.asarray(grid, dtype=np.int32)
        self._tile_width: float = float(positive(expect(tile_width, Real)))
        self._tile_height: float = float(positive(expect(tile_height, Real)))
        self._flags: NDArray[np.uint8] = (
            np.asarray(flags, dtype=np.uint8)
            if flags is not None
            else np.zeros(self._grid.shape, dtype=np.uint8)
        )
        self._pos: Point = Point(pos)
        self._anchor: Point = Point(anchor)

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        rows, cols = self._grid.shape
        return f"TileMap(tile={self._tile}, grid={cols}x{rows}, tile={self._tile_width}x{self._tile_height}, pos={self._pos}, anchor={self._anchor})"

    # ======================================== GETTERS ========================================
    @property
    def tile(self) -> Tile:
        """Renvoie le tileset associé"""
        return self._tile

    @property
    def grid(self) -> NDArray[np.int32]:
        """Renvoie une copie de la grille brute"""
        return self._grid.copy()

    @property
    def flags(self) -> NDArray[np.uint8]:
        """Renvoie une copie du tableau de flags"""
        return self._flags.copy()

    @property
    def tile_width(self) -> float:
        """Renvoie la largeur d'une tuile en pixels monde"""
        return self._tile_width

    @property
    def tile_height(self) -> float:
        """Renvoie la hauteur d'une tuile en pixels monde"""
        return self._tile_height

    @property
    def pos(self) -> Point:
        """Renvoie la position monde de l'ancre"""
        return self._pos

    @property
    def x(self) -> float:
        """Renvoie la coordonnée horizontale de l'ancre"""
        return self._pos.x

    @property
    def y(self) -> float:
        """Renvoie la coordonnée verticale de l'ancre"""
        return self._pos.y

    @property
    def anchor(self) -> Point:
        """Renvoie le point d'ancrage"""
        return self._anchor

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

    # ======================================== SETTERS ========================================
    @pos.setter
    def pos(self, value: Point) -> None:
        """Fixe la position monde de l'ancre"""
        self._pos = Point(value)

    @x.setter
    def x(self, value: Real) -> None:
        """Fixe la coordonnée horizontale de l'ancre"""
        self._pos.x = float(expect(value, Real))

    @y.setter
    def y(self, value: Real) -> None:
        """Fixe la coordonnée verticale de l'ancre"""
        self._pos.y = float(expect(value, Real))

    @anchor.setter
    def anchor(self, value: Point) -> None:
        """Fixe le point d'ancrage"""
        self._anchor = Point(value)

    # ======================================== ACCÈS GRILLE ========================================
    def tile_at(self, col: int, row: int) -> int:
        """
        Renvoie l'ID de la tuile à (col, row), ou 0 si hors limites

        Args:
            col(int): colonne
            row(int): ligne
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return int(self._grid[row, col])
        return 0

    def flags_at(self, col: int, row: int) -> int:
        """
        Renvoie les flags de flip de la tuile à (col, row), ou 0 si hors limites

        Args:
            col(int): colonne
            row(int): ligne
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return int(self._flags[row, col])
        return 0

    # ======================================== CONVERSIONS COORDS ========================================
    def world_to_tile(self, x: float, y: float) -> tuple[int, int]:
        """
        Convertit une position monde en (col, row)

        Args:
            x(float): coordonnée horizontale monde
            y(float): coordonnée verticale monde
        """
        ox, oy = self.origin
        return int((x - ox) // self._tile_width), int((y - oy) // self._tile_height)

    def tile_to_world(self, col: int, row: int) -> tuple[float, float]:
        """
        Convertit (col, row) en position monde (coin bas-gauche de la tuile)

        Args:
            col(int): colonne
            row(int): ligne
        """
        ox, oy = self.origin
        return ox + col * self._tile_width, oy + row * self._tile_height

    def tiles_in_region(self, x: float, y: float, width: float, height: float) -> tuple[int, int, int, int]:
        """
        Renvoie la plage de tuiles (col_min, row_min, col_max, row_max) couvrant la région monde

        Args:
            x(float): coin gauche de la région
            y(float): coin bas de la région
            width(float): largeur de la région
            height(float): hauteur de la région
        """
        ox, oy = self.origin
        col_min = max(0, int((x - ox) // self._tile_width))
        row_min = max(0, int((y - oy) // self._tile_height))
        col_max = min(self.cols, int((x + width - ox) // self._tile_width) + 1)
        row_max = min(self.rows, int((y + height - oy) // self._tile_height) + 1)
        return col_min, row_min, col_max, row_max