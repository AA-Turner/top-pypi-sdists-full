# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._component import RigidBody, Collider
from ...._core import Geometry

# ======================================== SPATIAL HASH ========================================
class SpatialHash:
    """Broadphase par grille spatiale"""

    def __init__(self):
        self._cell_size: float | None = None
        self._dynamic_cells: dict[tuple[int, int], list] = {}
        self._static_cells: dict[tuple[int, int], list] = {}
        self._static_built: bool = False

    def clear_static(self):
        """Vide les cellules statiques"""
        self._static_cells.clear()
        self._static_built = False

    def calibrate(self, entities: list, geometry_cache: dict):
        """Calibre la taille des cellules sur les shapes dynamiques présentes"""
        extents = []
        for e in entities:
            rb = e.get(RigidBody) if e.has(RigidBody) else None
            if rb is None or rb.is_static():
                continue
            geom: Geometry = geometry_cache[e.id]
            x_min, y_min, x_max, y_max = geom.world_bounding_box()
            extents.append((x_max - x_min) * 0.5)
            extents.append((y_max - y_min) * 0.5)
        if not extents:
            self._cell_size = 64.0
            return
        extents.sort()
        median = extents[len(extents) // 2]
        self._cell_size = max(median * 2.5, 16.0)

    def update_dynamic(self, entities: list, geometry_cache: dict):
        """Met à jour les cellules dynamiques et reconstruit les statiques si nécessaire"""
        self._dynamic_cells.clear()
        rebuild = not self._static_built
        for entity in entities:
            col: Collider = entity.get(Collider)
            if not col.is_active():
                continue
            rb = entity.get(RigidBody) if entity.has(RigidBody) else None
            is_static = (rb is None) or rb.is_static()
            geom: Geometry = geometry_cache[entity.id]
            if is_static:
                if rebuild:
                    self._insert(self._static_cells, entity, geom, rb)
            else:
                self._insert(self._dynamic_cells, entity, geom, rb)
        if rebuild:
            self._static_built = True

    def get_pairs(self) -> list[tuple]:
        """Renvoie les paires d'entités potentiellement en collision"""
        seen: set[tuple[int, int]] = set()
        pairs: list[tuple] = []

        for cell in self._dynamic_cells.values():
            n = len(cell)
            for i in range(n):
                for j in range(i + 1, n):
                    a, b = cell[i], cell[j]
                    ia, ib = id(a), id(b)
                    key = (ia, ib) if ia < ib else (ib, ia)
                    if key not in seen:
                        seen.add(key)
                        pairs.append((a, b))

        for ck, dyn in self._dynamic_cells.items():
            stat = self._static_cells.get(ck)
            if not stat:
                continue
            for d in dyn:
                for s in stat:
                    id_d, id_s = id(d), id(s)
                    key = (id_d, id_s) if id_d < id_s else (id_s, id_d)
                    if key not in seen:
                        seen.add(key)
                        pairs.append((d, s))

        return pairs

    def _insert(self, cells: dict, entity, geom: Geometry, rb):
        """Insère une entité dans les cellules qu'elle occupe"""
        cs = self._cell_size
        x_min, y_min, x_max, y_max = geom.world_bounding_box()

        if rb is not None and not rb.is_static():
            cx, cy = geom.world_center()
            prev_cx = rb.prev_x - (geom._transform.x - cx)
            prev_cy = rb.prev_y - (geom._transform.y - cy)
            dx = prev_cx - cx
            dy = prev_cy - cy
            min_x = min(x_min, x_min + dx)
            max_x = max(x_max, x_max + dx)
            min_y = min(y_min, y_min + dy)
            max_y = max(y_max, y_max + dy)
        else:
            min_x, max_x, min_y, max_y = x_min, x_max, y_min, y_max

        for gx in range(int(min_x // cs), int(max_x // cs) + 1):
            for gy in range(int(min_y // cs), int(max_y // cs) + 1):
                key = (gx, gy)
                if key not in cells:
                    cells[key] = []
                cells[key].append(entity)