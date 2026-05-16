# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, over, positive
from ..abc import Shape

from numbers import Real, Integral

# ======================================== TILE ========================================
class Tile:
    """Spritesheet découpée en tuiles de taille uniforme

    Args:
        image_path: chemin de l'image source
        tile_width: largeur d'une tuile en pixels
        tile_height: hauteur d'une tuile en pixels
        margin: marge extérieure en pixels
        spacing: espacement entre tuiles en pixels
    """
    __slots__ = ("_image_path", "_tile_width", "_tile_height", "_margin", "_spacing", "_meta")

    def __init__(
        self,
        image_path: str,
        tile_width: Real = 1.0,
        tile_height: Real = 1.0,
        margin: Real = 0.0,
        spacing: Real = 0.0,
    ):
        # Transtypage et vérifications
        image_path = str(image_path)
        tile_width = float(tile_width)
        tile_height = float(tile_height)
        margin = float(margin)
        spacing = float(spacing)

        if __debug__:
            over(tile_width, 0, include=False)
            over(tile_height, 0, include=False)
            positive(margin)
            positive(spacing)

        # Attributs publiques
        self._image_path: str = image_path
        self._tile_width: float = tile_width
        self._tile_height: float = tile_height
        self._margin: float = margin
        self._spacing: float = spacing

        # Attributs internes
        self._meta: dict[int, TileMeta] = {}

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        return (
            f"Tile(path={self._image_path}, "
            f"tile={self._tile_width}x{self._tile_height}, "
            f"margin={self._margin}, spacing={self._spacing})"
        )

    # ======================================== GETTERS ========================================
    @property
    def image_path(self) -> str:
        """Renvoie le chemin de l'image source"""
        return self._image_path

    @property
    def tile_width(self) -> float:
        """Renvoie la largeur d'une tuile en pixels"""
        return self._tile_width

    @property
    def tile_height(self) -> float:
        """Renvoie la hauteur d'une tuile en pixels"""
        return self._tile_height

    @property
    def margin(self) -> float:
        """Renvoie la marge extérieure en pixels"""
        return self._margin

    @property
    def spacing(self) -> float:
        """Renvoie l'espacement entre tuiles en pixels"""
        return self._spacing

    def tile_region(self, tile_id: int) -> tuple[float, float, float, float]:
        """
        Renvoie la région (x, y, w, h) de la tuile dans l'image source

        Args:
            tile_id(int): identifiant local de la tuile (0-indexé)
        """
        tile_id = int(tile_id)
        stride = self._tile_width + self._spacing
        cols = self._columns_hint(stride)
        col = tile_id % cols
        row = tile_id // cols
        x = self._margin + col * stride
        y = self._margin + row * stride
        return (x, y, self._tile_width, self._tile_height)

    def get_meta(self, tile_id: int) -> TileMeta | None:
        """
        Renvoie les métadonnées d'une tuile, ou None si aucune n'est définie

        Args:
            tile_id(int): identifiant local de la tuile
        """
        tile_id = int(tile_id)
        return self._meta.get(tile_id)

    # ======================================== PUBLIC METHODS ========================================
    def set_meta(self, tile_id: int, meta: TileMeta) -> None:
        """Associe des métadonnées à une tuile

        Args:
            tile_id(int): identifiant local de la tuile
            meta(TileMeta): métadonnées à associer
        """
        tile_id = int(tile_id)
        if __debug__:
            expect(meta, TileMeta)
        self._meta[tile_id] = meta

    # ======================================== INTERNALS ========================================
    def _columns_hint(self, stride: float) -> int:
        """Placeholder"""
        return max(1, int(stride))

# ======================================== TILE META ========================================
class TileMeta:
    """Métadonnées associées à un ID de tuile dans un Tile

    Args:
        *tags: tags de la tuile *(ex. "solid", "ladder")*
        collision_shape: forme de collision custom
        friction: friction de la tuile
        restitution: restitution de la tuiler
        category: catégorie binaire de collision
        mask: masque binaire de collision
    """
    __slots__ = (
        "_tags", 
        "_collision_shape", "_friction", "_restitution",
        "_category", "_mask",
    )

    def __init__(
        self,
        *tags: str,
        collision_shape: Shape | None = None,
        friction: Real | None = None,
        restitution: Real | None = None,
        category: Integral | None = None,
        mask: Integral | None = None,
    ):
        # Transtypage et vérifications
        tags = frozenset(tags)
        friction = float(friction) if friction is not None else None
        restitution = float(restitution) if restitution is not None else None
        category = int(category) if category is not None else None
        mask = int(mask) if mask is not None else None

        if __debug__:
            expect(tags, frozenset[str])
            expect(collision_shape, (Shape, None))
            positive(friction)
            positive(restitution)

        # Attributs publiques
        self._tags: frozenset[str] = tags
        self._collision_shape: Shape | None = collision_shape
        self._friction: float | None =friction
        self._restitution: float | None = restitution
        self._category: int | None = category
        self._mask: int | None = mask

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation de la ``TileMeta``"""
        return (
            f"TileMeta(tags={self._tags}, "
            f"friction={self._friction}, restitution={self._restitution}, "
            f"category={self._category}, mask={self._mask}, "
            f"collision_shape={self._collision_shape})"
        )

    # ======================================== PROPERTIES ========================================
    @property
    def tags(self) -> frozenset[str]:
        """Renvoie les tags de la tuile"""
        return self._tags

    @property
    def collision_shape(self) -> Shape | None:
        """Renvoie la forme de collision custom, ou None si bounding box"""
        return self._collision_shape

    @property
    def friction(self) -> float | None:
        """Renvoie la friction de la tuile"""
        return self._friction

    @property
    def restitution(self) -> float | None:
        """Renvoie la restitution de la tuile"""
        return self._restitution

    @property
    def category(self) -> int | None:
        """Renvoie la catégorie binaire"""
        return self._category

    @property
    def mask(self) -> int | None:
        """Renvoie le masque binaire"""
        return self._mask

    # ======================================== PREDICATES ========================================
    def has_tag(self, tag: str) -> bool:
        """Vérifie si la tuile possède un tag"""
        return tag in self._tags

    def is_solid(self) -> bool:
        """Vérifie si la tuile est solide"""
        return "solid" in self._tags
    
# ======================================== EXPORTS ========================================
__all__ = [
    "Tile",
    "TileMeta",
]