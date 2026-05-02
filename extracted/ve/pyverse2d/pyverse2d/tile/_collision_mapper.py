# ======================================== IMPORTS ========================================
from __future__ import annotations

from ._tile_map import TileMap, FLIP_H, FLIP_V, FLIP_D
from ._tile import TileMeta

from .._internal import expect, positive
from ..world import World, Entity, Transform, Collider, RigidBody
from ..shape import Rect, Polygon
from ..abc import Shape

from numbers import Real

# ======================================== COLLISION MAPPER ========================================
class CollisionMapper:
    """Convertit les tuiles solides d'un TileMap en bodies statiques dans le World

    Args:
        tile_map: couche source
        solid_tag: tag identifiant les tuiles solides
        friction: friction par défaut
        restitution: restitution par défaut
        category: catégorie binaire par défaut
        mask: masque binaire par défaut
    """
    __slots__ = ("_tile_map", "_solid_tag", "_friction", "_restitution", "_category", "_mask", "_entities")

    def __init__(
        self,
        tile_map: TileMap,
        solid_tag: str = "solid",
        friction: Real = 0.3,
        restitution: Real = 0.0,
        category: int = 0b00000001,
        mask: int = 0b11111111,
    ):
        self._tile_map: TileMap = expect(tile_map, TileMap)
        self._solid_tag: str = expect(solid_tag, str)
        self._friction: float = float(positive(expect(friction, Real)))
        self._restitution: float = float(positive(expect(restitution, Real)))
        self._category: int = expect(category, int)
        self._mask: int = expect(mask, int)
        self._entities: list = []

    # ======================================== PUBLIC METHODS ========================================
    def inject(self, world: World) -> None:
        """Parcourt la grille injecte les hitboxes dans le World

        Args:
            world: monde cible
        """
        for col, row, shape, friction, restitution, category, mask in self._custom_shapes():
            wx, wy = self._tile_map.tile_to_world(col, row)
            tw = self._tile_map.tile_width
            th = self._tile_map.tile_height
            entity = Entity(
                Transform(position=(wx + tw / 2, wy + th / 2)),
                Collider(shape=shape, category=category, mask=mask),
                RigidBody(friction=friction, restitution=restitution),
            )
            world.add_entity(entity)
            self._entities.append(entity)

        for col, row, w, h, friction, restitution, category, mask in self._merged_rects():
            wx, wy = self._tile_map.tile_to_world(col, row)
            entity = Entity(
                Transform(position=(wx + w / 2, wy + h / 2)),
                Collider(shape=Rect(w, h), category=category, mask=mask),
                RigidBody(friction=friction, restitution=restitution),
            )
            world.add_entity(entity)
            self._entities.append(entity)

    def remove(self, world: World) -> None:
        """Supprime toutes les entités précédemment injectées dans le World

        Args:
            world: monde cible
        """
        for entity in self._entities:
            world.remove_entity(entity)
        self._entities.clear()

    # ======================================== INTERNALS ========================================
    def _has_custom_shape(self, col: int, row: int) -> bool:
        """Vérifie si la tuile à ``(col, row)`` a une collision_shape custom"""
        tile_id = self._tile_map.tile_at(col, row)
        if tile_id == 0:
            return False
        meta = self._tile_map.tile.get_meta(tile_id)
        return meta is not None and meta.collision_shape is not None

    def _is_solid(self, col: int, row: int) -> bool:
        """Vérifie si la tuile à ``(col, row)`` est solide et sans shape custom"""
        tile_id = self._tile_map.tile_at(col, row)
        if tile_id == 0:
            return False
        meta = self._tile_map.tile.get_meta(tile_id)
        if meta is None:
            return False
        if meta.collision_shape is not None:
            return False
        return meta.has_tag(self._solid_tag)

    def _resolve_props(self, tile_id: int) -> tuple[float, float, int, int]:
        """Résout friction, restitution, category, mask pour un tile_id — meta > global"""
        meta: TileMeta | None = self._tile_map.tile.get_meta(tile_id)
        friction = meta.friction if (meta and meta.friction is not None) else self._friction
        restitution = meta.restitution if (meta and meta.restitution is not None) else self._restitution
        category = meta.category if (meta and meta.category is not None) else self._category
        mask = meta.mask if (meta and meta.mask is not None) else self._mask
        return friction, restitution, category, mask

    def _custom_shapes(self) -> list[tuple]:
        """Renvoie les tuiles avec collision_shape custom sous forme ``(col, row, shape, friction, restitution, category, mask)``"""
        tm = self._tile_map
        tw = tm.tile_width
        th = tm.tile_height
        result = []
        for row in range(tm.rows):
            for col in range(tm.cols):
                if not self._has_custom_shape(col, row):
                    continue
                tile_id = tm.tile_at(col, row)
                meta = tm.tile.get_meta(tile_id)
                friction, restitution, category, mask = self._resolve_props(tile_id)
                flip = tm.flags_at(col, row)
                shape = _apply_flip(meta.collision_shape, flip, tw, th)
                result.append((col, row, shape, friction, restitution, category, mask))
        return result

    def _merged_rects(self) -> list[tuple[int, int, float, float, float, float, int, int]]:
        """Fusionne les tuiles solides en rectangles par sweep horizontal puis vertical"""
        tm = self._tile_map
        tw = tm.tile_width
        th = tm.tile_height
        rects = []

        visited = [[False] * tm.cols for _ in range(tm.rows)]
        for row in range(tm.rows):
            for col in range(tm.cols):
                if visited[row][col] or not self._is_solid(col, row):
                    continue

                tile_id = tm.tile_at(col, row)
                props = self._resolve_props(tile_id)

                w = 1
                while (
                    col + w < tm.cols
                    and not visited[row][col + w]
                    and self._is_solid(col + w, row)
                    and self._resolve_props(tm.tile_at(col + w, row)) == props
                ):
                    w += 1

                h = 1
                while row + h < tm.rows:
                    can_extend = all(
                        not visited[row + h][col + c]
                        and self._is_solid(col + c, row + h)
                        and self._resolve_props(tm.tile_at(col + c, row + h)) == props
                        for c in range(w)
                    )
                    if not can_extend:
                        break
                    h += 1

                for dr in range(h):
                    for dc in range(w):
                        visited[row + dr][col + dc] = True

                friction, restitution, category, mask = props
                rects.append((col, row, w * tw, h * th, friction, restitution, category, mask))

        return rects


# ======================================== FLIP HELPER ========================================
import numpy as np

def _apply_flip(shape: Shape, flip: int, tw: float, th: float) -> Shape:
    """Applique les transformations de flip à une collision shape
    
    Args:
        shape: shape source
        flip: flags FLIP_H, FLIP_V, FLIP_D
        tw: largeur monde de la tuile
        th: hauteur monde de la tuile
    """
    if flip == 0:
        return shape
    if isinstance(shape, Rect):
        return shape
    if not isinstance(shape, Polygon):
        return shape

    verts = np.asarray(shape.get_vertices(), dtype=np.float32)

    # Décomposition
    x = verts[:, 0]
    y = verts[:, 1]

    # Flip diagonal
    if flip & FLIP_D:
        x, y = y * (tw / th), x * (th / tw)

    # Flip horizontal
    if flip & FLIP_H:
        x = tw - x

    # Flip vertical
    if flip & FLIP_V:
        y = th - y

    verts = np.column_stack((x, y))
    return Polygon(*verts)