# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...._internal import Processor
from ....math import Vector
from ...._core import Geometry

from ..._world import World
from ..._component import Transform, Collider, GroundSensor, RigidBody

from ._registry import dispatch, Contact
from ._spatial_hash import SpatialHash
from ._resolve import CachedContact, resolve
from ._warm_start import warm_start
from ._constants import ConstantsDataset

from dataclasses import dataclass, field
from math import sqrt

# ======================================== CONTEXTE ========================================
@dataclass(slots=True)
class UpdateContext:
    """Contexte partagé entre les étapes du update"""
    world: World
    dt: float
    hash: SpatialHash | None
    cache: dict
    geometry_cache: dict
    geometry_keys: dict
    C: ConstantsDataset
    entities: list = field(default_factory=list)
    pairs: list = field(default_factory=list)
    active_contacts: list = field(default_factory=list)
    active_keys: set = field(default_factory=set)
    max_depth: float = 0.0

    @staticmethod
    def build(
        world: World, 
        dt: float, hash: SpatialHash | None,
        cache: dict,
        geometry_cache: dict,
        geometry_keys: dict,
        C: ConstantsDataset,
    ) -> UpdateContext:
        """Construit le contexte update"""
        return UpdateContext(
            world=world,
            dt=dt,
            hash=hash,
            cache=cache,
            geometry_cache=geometry_cache,
            geometry_keys=geometry_keys,
            C=C,
        )

# ======================================== processor ========================================
update_processor = Processor("update")

@update_processor.step
def _query_entities(ctx: UpdateContext):
    ctx.entities = ctx.world.query(Collider, Transform)
    
@update_processor.step
def _update_geometries(ctx: UpdateContext):
    active_ids = {e.id for e in ctx.entities}

    # Nettoyage orphelins
    for eid in list(ctx.geometry_cache):
        if eid not in active_ids:
            del ctx.geometry_cache[eid]
            del ctx.geometry_keys[eid]
    
    # Création/mise à jour si component remplacé
    for entity in ctx.entities:
        col = entity.collider
        tr = entity.transform
        key = (id(col), id(tr))
        if ctx.geometry_keys.get(entity.id) != key:
            ctx.geometry_cache[entity.id] = Geometry(col.shape, tr, col.offset)
            ctx.geometry_keys[entity.id] = key

@update_processor.step
def _reset_sensors(ctx: UpdateContext):
    """Reset du GroundSensor avant détection"""
    for entity in ctx.entities:
        gs = entity.ground_sensor
        if gs is not None:
            gs._coyote_elapsed += ctx.dt
            if gs._coyote_elapsed >= gs._coyote_time:
                gs._grounded = False
                gs._ground_normal = None

@update_processor.step
def _broadphase(ctx: UpdateContext):
    """Génération des paires candidates"""
    if ctx.hash is not None:
        if ctx.hash._cell_size is None:
            ctx.hash.calibrate(ctx.entities, ctx.geometry_cache)
        ctx.hash.update_dynamic(ctx.entities, ctx.geometry_cache)
        ctx.pairs = ctx.hash.get_pairs()
    else:
        n = len(ctx.entities)
        ctx.pairs = [(ctx.entities[i], ctx.entities[j]) for i in range(n) for j in range(i + 1, n)]

@update_processor.step
def _reset_colliders(ctx: UpdateContext):
    """Reset des listes de contacts des colliders"""
    for entity in ctx.entities:
        entity.collider._contacts.clear()

@update_processor.step
def _narrowphase(ctx: UpdateContext):
    """Narrowphase : détection, lissage des normales, warm start"""
    for a, b in ctx.pairs:
        col_a: Collider = a.collider
        col_b: Collider = b.collider
        if not col_a.is_active() or not col_b.is_active():
            continue
        if not col_a.collides_with(col_b):
            continue

        geom_a: Geometry = ctx.geometry_cache[a.id]
        geom_b: Geometry = ctx.geometry_cache[b.id]
        contact = _detect(geom_a, geom_b)
        if contact is None:
            continue

        # Collision fantôme
        if col_a.is_trigger() or col_b.is_trigger():
            col_a._contacts[col_b] = Vector._make(0, 0)
            col_b._contacts[col_a] = Vector._make(0, 0)
            continue

        # Gestion du cache de contacts persistants
        ia, ib = id(a), id(b)
        key = (ia, ib) if ia < ib else (ib, ia)
        ctx.active_keys.add(key)
        if key not in ctx.cache:
            ctx.cache[key] = CachedContact()
        cached = ctx.cache[key]

        # Lissage de la normale entre frames
        nx, ny = contact.normal.x, contact.normal.y
        if cached.normal is not None:
            pnx, pny = cached.normal
            dot = nx * pnx + ny * pny
            if dot > 0.95:
                mix = 0.7
                mnx = nx * mix + pnx * (1.0 - mix)
                mny = ny * mix + pny * (1.0 - mix)
                n_len = sqrt(mnx * mnx + mny * mny) or 1.0
                nx, ny = mnx / n_len, mny / n_len
            elif dot < 0:
                cached.jn = 0.0
                cached.jt = 0.0
        normal = Vector._make(nx, ny)
        cached.normal = normal
        contact = Contact(normal, contact.depth)
        col_a._contacts[col_b] = normal
        col_b._contacts[col_a] = -normal

        # Actualisation du GroundSensor selon la normale du contact
        _update_ground_sensor(a, b, nx, ny)
        if contact.depth > ctx.max_depth:
            ctx.max_depth = contact.depth
        ctx.active_contacts.append((a, b, contact, cached))

        # Step climbing
        if _try_step(a, b, nx, ny, contact.depth, geom_a, geom_b):
            continue

        # Reset jt sur les contacts quasi-verticaux avant warm start
        if abs(ny) < 0.3:
            cached.jt = 0.0

        # Application du warm start
        warm_start(a, b, contact, cached, ctx.C)

@update_processor.step
def _cleanup_cache(ctx: UpdateContext):
    """Nettoyage des contacts inactifs"""
    for key in list(ctx.cache):
        if key not in ctx.active_keys:
            del ctx.cache[key]

@update_processor.step
def _wake_lost_supports(ctx: UpdateContext):
    """Réveille les RigidBody dont les contacts ont disparu"""
    for entity in ctx.entities:
        if not entity.has(RigidBody):
            continue
        rb = entity.rigid_body
        if not rb.is_sleeping():
            continue
        col = entity.collider
        if len(col._contacts) == 0:
            col._coyote_elapsed += ctx.dt
            if col._coyote_elapsed > col._COYOTE_TIME:
                rb.wake()
        else:
            col._coyote_elapsed = 0.0

@update_processor.step
def _solve(ctx: UpdateContext):
    """Résolution itérative des contacts"""
    iterations = ctx.C.ITER
    if ctx.max_depth > ctx.C.EXTRA_ITER_THRESHOLD:
        iterations += ctx.C.EXTRA_ITER
    for _ in range(iterations):
        for a, b, contact, cached in ctx.active_contacts:
            resolve(a, b, contact, cached, ctx.C, ctx.dt)

# ======================================== HELPERS ========================================
def _detect(geom_a: Geometry, geom_b: Geometry) -> Contact | None:
    """AABB broadphase puis dispatch narrowphase"""
    ax_min, ay_min, ax_max, ay_max = geom_a.world_bounding_box()
    bx_min, by_min, bx_max, by_max = geom_b.world_bounding_box()
    if ax_min > bx_max or bx_min > ax_max or ay_min > by_max or by_min > ay_max:
        return None
    return dispatch(geom_a, geom_b)

def _update_ground_sensor(a, b, nx: float, ny: float):
    """Actualisation du GroundSensor selon la normale du contact"""
    n_len = sqrt(nx * nx + ny * ny) or 1.0
    ny_norm = ny / n_len
    
    # Touche le sol
    gs = a.ground_sensor
    if ny_norm > 0 and gs is not None:
        if ny_norm >= gs._threshold:
            gs._grounded = True
            gs._coyote_elapsed = 0.0
            gs._ground_normal = Vector._make(nx / n_len, ny_norm)
    
    # Ne touche pas le sol
    gs = b.ground_sensor
    if ny_norm < 0 and gs is not None:
        if -ny_norm >= gs._threshold:
            gs._grounded = True
            gs._coyote_elapsed = 0.0
            gs._ground_normal = Vector._make(-nx / n_len, -ny_norm)

def _try_step(a, b, nx: float, ny: float, depth: float, geom_a: Geometry, geom_b: Geometry) -> bool:
    """Tente de franchir un step horizontal"""
    if abs(ny) > abs(nx):
        return False
    if abs(ny) > 0.1:
        return False

    for mover, obstacle, geom_m, geom_o in ((a, b, geom_a, geom_b), (b, a, geom_b, geom_a)):
        if not mover.has(GroundSensor):
            continue
        gs = mover.ground_sensor
        if gs.max_step_height <= 0 or not gs.is_grounded():
            continue

        _, my_min, _, _ = geom_m.world_bounding_box()
        _, _, _, oy_max = geom_o.world_bounding_box()

        step_h = oy_max - my_min
        if step_h <= 0 or step_h > gs.max_step_height:
            continue

        mover.transform.y += step_h
        return True

    return False