# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import System
from .._world import World, Entity
from .._component import Transform, SpriteRenderer, ShapeRenderer, TextRenderer
from ..._rendering import Pipeline, PygletShapeRenderer, PygletSpriteRenderer, PygletLabelRenderer
from ..._core import Geometry

from typing import Callable

# ======================================== RENDER ORDER ========================================
_ORDER_SHAPE = 0
_ORDER_SPRITE = 1
_ORDER_LABEL = 2

# ======================================== SYSTEM ========================================
class RenderSystem(System):
    """Système gérant le rendu des entités"""
    __slots__ = (
        "_sprites", "_shapes", "_labels",
        "_geometries_cache", "_geometries_keys",
    )
    
    order = 100
    exclusive = True

    def __init__(self):
        # Caches des renderers
        self._sprites: dict[int, PygletSpriteRenderer] = {}
        self._shapes: dict[int, PygletShapeRenderer] = {}
        self._labels: dict[int, PygletLabelRenderer] = {}

        # Caches des géométries
        self._geometries_cache: dict[int, Geometry] = {}
        self._geometries_keys: dict[int, tuple] = {}

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du système"""
        return f"RenderSystem(sprites={len(self._sprites)}, shapes={len(self._shapes)}, labels={len(self._labels)})"

    # ======================================== LIFE CYCLE ========================================
    def update(self, world: World, dt: float):
        """Actualisation du pilotage

        Args:
            world: monde courant
            dt: delta temps
        """
        pass

    def draw(self, world: World, pipeline: Pipeline):
        """Synchronise toutes les entités renderables avec le Batch de rendu

        Args:
            world(World): monde à rendre
            pipeline(Pipeline): pipeline active
        """
        active_sprites = set()
        active_shapes = set()
        active_labels = set()

        for entity in world.query(Transform):
            eid = entity.id
            tr: Transform = entity.get(Transform)

            if entity.has(ShapeRenderer):
                active_shapes.add(eid)
                self._sync_shape(entity, tr, pipeline)

            if entity.has(SpriteRenderer):
                active_sprites.add(eid)
                self._sync_sprite(entity, tr, pipeline)

            if entity.has(TextRenderer):
                active_labels.add(eid)
                self._sync_text(entity, tr, pipeline)

        # Nettoyage des entités inactives
        for eid in list(self._sprites):
            if eid not in active_sprites:
                self._sprites.pop(eid).delete()

        for eid in list(self._shapes):
            if eid not in active_shapes:
                self._shapes.pop(eid).delete()

        for eid in list(self._labels):
            if eid not in active_labels:
                self._labels.pop(eid).delete()

    # ======================================== SYNC SHAPE ========================================
    def _sync_shape(self, entity: Entity, tr: Transform, pipeline: Pipeline):
        """Crée ou met à jour le renderer de shape de l'entité"""
        # Raccourcis
        sr: ShapeRenderer = entity.get(ShapeRenderer)
        eid = entity.id

        # Invisible
        if not sr.is_visible():
            if eid in self._shapes:
                self._shapes[eid].visible = False
            return
        
        # Construction de la géométrie si nécessaire
        key = (id(sr), id(tr))
        geom_key = self._geometries_keys.get(eid)

        if geom_key != key:
            self._geometries_cache[eid] = Geometry(sr.shape, tr, sr.offset)
            self._geometries_keys[eid] = key

            if geom_key is None:
                entity.on_kill(self._make_clear_geometry_func(eid))

        geometry = self._geometries_cache[eid]

        # Calcul du z-order
        z = sr.z * 3 + _ORDER_SHAPE

        # Construction du renderer
        if eid not in self._shapes:
            self._shapes[eid] = PygletShapeRenderer(
                geometry = geometry,
                filling = sr.filling,
                color = sr.filling_color,
                border_width = sr.border_width,
                border_align = sr.border_align,
                border_color = sr.border_color,
                opacity = sr.opacity,
                z = z,
                pipeline = pipeline,
            )

        # Actualisation du renderer
        else:
            self._shapes[eid].update(
                geometry = geometry,
                filling = sr.filling,
                color = sr.filling_color,
                border_width = sr.border_width,
                border_align = sr.border_align,
                border_color = sr.border_color,
                opacity = sr.opacity,
                z = z,
            )
            self._shapes[eid].visible = True

    # ======================================== SYNC SPRITE ========================================
    def _sync_sprite(self, entity: Entity, tr: Transform, pipeline: Pipeline):
        """Crée ou met à jour le renderer de sprite de l'entité"""
        # Raccourcis
        sr: SpriteRenderer = entity.get(SpriteRenderer)
        eid = entity.id

        # Invisible
        if not sr.is_visible():
            if eid in self._sprites:
                self._sprites[eid].visible = False
            return

        # Calcul du z-order
        z = sr.z * 3 + _ORDER_SPRITE

        # Construction du renderer
        if eid not in self._sprites:
            self._sprites[eid] = PygletSpriteRenderer(
                image = sr.image,
                transform = tr,
                offset = sr.offset,
                flip_x = sr.flip_x,
                flip_y = sr.flip_y,
                opacity = sr.opacity,
                color = sr.tint,
                z = z,
                pipeline = pipeline,
            )

        # Actualisation du renderer
        else:
            self._sprites[eid].update(
                image = sr.image,
                transform = tr,
                offset = sr.offset,
                flip_x = sr.flip_x,
                flip_y = sr.flip_y,
                opacity = sr.opacity,
                color = sr.tint,
                z = z,
            )
            self._sprites[eid].visible = True

    # ======================================== SYNC TEXT ========================================
    def _sync_text(self, entity: Entity, tr: Transform, pipeline: Pipeline):
        """Crée ou met à jour le renderer de label de l'entité"""
        # Raccourcis
        tc: TextRenderer = entity.get(TextRenderer)
        eid = entity.id

        # Invisible
        if not tc.is_visible():
            if eid in self._labels:
                self._labels[eid].visible = False
            return

        # Calcul du z-order
        z = tc.z * 3 + _ORDER_LABEL

        # Construction du renderer
        if eid not in self._labels:
            self._labels[eid] = PygletLabelRenderer(
                text = tc.text,
                transform = tr,
                offset = tc.offset,
                weight = tc.weight,
                italic = tc.italic,
                color = tc.color,
                opacity = tc.opacity,
                width = tc.width,
                multiline = tc.multiline,
                align = tc.align,
                z = z,
                pipeline = pipeline,
            )

        # Actualisation du renderer
        else:
            self._labels[eid].update(
                text = tc.text,
                transform = tr,
                offset = tc.offset,
                weight = tc.weight,
                italic = tc.italic,
                color = tc.color,
                opacity = tc.opacity,
                width = tc.width,
                multiline = tc.multiline,
                align = tc.align,
                z = z,
            )
            self._labels[eid].visible = True

    # ======================================== INTERNALS ========================================
    def _make_clear_geometry_func(self, eid: int) -> Callable[[], None]:
        """Construit un token de suppresion d'une géométrie"""

        def clear_geometry() -> None:
            self._geometries_cache.pop(eid, None)
            self._geometries_keys.pop(eid, None)

        return clear_geometry