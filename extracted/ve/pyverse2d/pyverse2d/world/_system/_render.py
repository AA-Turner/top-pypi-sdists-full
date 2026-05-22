# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import profile_section
from ...abc import System

from .._world import World, Entity
from .._component import Transform, SpriteRenderer, ShapeRenderer, TextRenderer, TrailRenderer
from ..._rendering import Pipeline, PygletShapeRenderer, PygletSpriteRenderer, PygletLabelRenderer, PygletTrailRenderer
from ..._core import Geometry

from typing import Callable, ClassVar

# ======================================== CONSTANTS ========================================
_ORDER_SHAPE: int = 1
_ORDER_SPRITE: int = 2
_ORDER_LABEL: int = 3
_ORDER_TRAIL: int = 0

# ======================================== SYSTEM ========================================
class RenderSystem(System):
    """Système gérant le rendu des entités"""
    __slots__ = (
        "_sprites", "_shapes", "_labels", "_trails",
        "_geometries_cache", "_geometries_keys",
    )
    
    _ORDER: ClassVar[int] = 100

    _IS_EXCLUSIVE: ClassVar[bool] = True
    _IS_RENDERABLE: ClassVar[bool] = True

    _ACTIVE_SPRITES_SET: ClassVar[set[int]] = set()
    _ACTIVE_SHAPES_SET: ClassVar[set[int]] = set()
    _ACTIVE_LABELS_SET: ClassVar[set[int]] = set()
    _ACTIVE_TRAILS_SET: ClassVar[set[int]] = set()

    def __init__(self):
        # Caches des renderers
        self._sprites: dict[int, PygletSpriteRenderer] = {}
        self._shapes: dict[int, PygletShapeRenderer] = {}
        self._labels: dict[int, PygletLabelRenderer] = {}
        self._trails: dict[int, PygletTrailRenderer] = {}

        # Caches des géométries
        self._geometries_cache: dict[int, Geometry] = {}
        self._geometries_keys: dict[int, tuple] = {}

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du système"""
        return f"RenderSystem(sprites={len(self._sprites)}, shapes={len(self._shapes)}, labels={len(self._labels)}, trails={len(self._trails)})"

    # ======================================== LIFE CYCLE ========================================
    @profile_section("world.animation.update")
    def update(self, world: World, dt: float):
        """Actualisation du pilotage

        Args:
            world: monde courant
            dt: delta-time
        """
        for entity in world.query(Transform, TrailRenderer):
            tc: TrailRenderer = entity.get(TrailRenderer)
            tr: Transform = entity.get(Transform)
            if tc.is_visible():
                tc._tick(dt)
                tc._push(tr.x, tr.y)

    @profile_section("world.animation.draw")
    def draw(self, world: World, pipeline: Pipeline):
        """Synchronise toutes les entités renderables avec le Batch de rendu

        Args:
            world: monde à rendre
            pipeline: ``Pipeline`` de rendu courant
        """
        # Récupération des sets pré-alloués
        active_sprites = RenderSystem._ACTIVE_SPRITES_SET
        active_shapes = RenderSystem._ACTIVE_SHAPES_SET
        active_labels = RenderSystem._ACTIVE_LABELS_SET
        active_trails = RenderSystem._ACTIVE_TRAILS_SET

        # Nettoyage
        active_sprites.clear()
        active_shapes.clear()
        active_labels.clear()
        active_trails.clear()

        # Affichage des renderers
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

            if entity.has(TrailRenderer):
                active_trails.add(eid)
                self._sync_trail(entity, tr, pipeline)

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

        for eid in list(self._trails):
            if eid not in active_trails:
                self._trails.pop(eid).delete()

    # ======================================== SYNC SHAPE ========================================
    def _sync_shape(self, entity: Entity, tr: Transform, pipeline: Pipeline):
        """Crée ou met à jour le renderer de shape de l'entité
        
        Args:
            entity: ``Entity`` possédant le renderer
            tr: ``Transform``de l'entité
            pipeline: ``Pipeline``de rendu courant
        """
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
        """Crée ou met à jour le renderer de sprite de l'entité

        Args:
            entity: ``Entity`` possédant le renderer
            tr: ``Transform``de l'entité
            pipeline: ``Pipeline``de rendu courant
        """
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
        """Crée ou met à jour le renderer de label de l'entité
        
        Args:
            entity: ``Entity`` possédant le renderer
            tr: ``Transform``de l'entité
            pipeline: ``Pipeline``de rendu courant
        """
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

    # ======================================== _sync_trail ========================================
    def _sync_trail(self, entity: Entity, tr: Transform, pipeline: Pipeline) -> None:
        """Crée ou met à jour le renderer de trail de l'entité

        Args:
            entity: ``Entity`` possédant le renderer
            tr: ``Transform`` de l'entité
            pipeline: ``Pipeline`` de rendu courant
        """
        tc: TrailRenderer = entity.get(TrailRenderer)
        eid = entity.id

        if not tc.is_visible():
            if eid in self._trails:
                self._trails[eid].visible = False
            return

        # Recréation si le mode image a changé
        existing = self._trails.get(eid)
        if existing is not None and existing.textured != (tc.image is not None):
            existing.delete()
            del self._trails[eid]

        if eid not in self._trails:
            self._trails[eid] = PygletTrailRenderer(
                max_points=TrailRenderer._MAX_POINTS,
                image=tc.image,
            )
            entity.on_kill(self._make_clear_trail_func(eid))

        renderer = self._trails[eid]
        renderer.visible = True
        renderer.update(
            points=tc.points,
            width=tc.width,
            duration=tc.duration,
            color=tc.color,
            opacity=tc.opacity,
            width_easing=tc.width_easing,
            smooth=tc.smooth,
            pipeline=pipeline,
        )
        renderer.draw(pipeline, tc.color)

    # ======================================== INTERNALS ========================================
    def _make_clear_geometry_func(self, eid: int) -> Callable[[], None]:
        """Construit un token de suppresion d'une géométrie
        
        Args:
            eid: identifiant de l'entité
        """

        def clear_geometry() -> None:
            self._geometries_cache.pop(eid, None)
            self._geometries_keys.pop(eid, None)

        return clear_geometry
    
    def _make_clear_trail_func(self, eid: int) -> Callable[[], None]:
        """Construit un token de suppression d'un trail

        Args:
            eid: identifiant de l'entité
        """
        def clear_trail() -> None:
            renderer = self._trails.pop(eid, None)
            if renderer is not None:
                renderer.delete()
        return clear_trail
    
# ======================================== EXPORTS ========================================
__all__ = [
    "RenderSystem",
]