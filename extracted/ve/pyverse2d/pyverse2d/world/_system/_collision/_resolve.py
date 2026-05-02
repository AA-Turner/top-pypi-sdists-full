# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...._internal import Processor
from ....math import Vector
from ....abc import Shape

from ..._component import Transform, RigidBody

from ._registry import Contact
from ._constants import ConstantsDataset

from dataclasses import dataclass

# ======================================== CACHED CONTACT ========================================
class CachedContact:
    """Impulsions accumulées + normale lissée pour une paire de contacts persistante

    Args:
        jn: impulsion normale accumulée (>= 0)
        jt: impulsion tangentielle accumulée (cône de Coulomb)
        normal: normale lissée entre frames
    """
    __slots__ = ("jn", "jt", "normal")

    def __init__(self):
        self.jn: float = 0.0
        self.jt: float = 0.0
        self.normal: tuple | None = None

# ======================================== CONTEXTE ========================================
@dataclass(slots=True)
class ResolveContext:
    """Contexte partagé entre les étapes du solver"""
    a: Shape
    b: Shape
    contact: Contact
    cached: CachedContact
    C: ConstantsDataset
    dt: float
    has_rb_a: bool = False
    has_rb_b: bool = False
    rb_a: RigidBody | None = None
    rb_b: RigidBody | None = None
    static_a: bool = False
    static_b: bool = False
    inv_a: float = 0.0
    inv_b: float = 0.0
    inv_sum: float = 0.0
    tr_a: Transform | None = None
    tr_b: Transform | None = None
    nx: float = 0.0
    ny: float = 0.0
    tx: float = 0.0
    ty: float = 0.0
    depth: float = 0.0
    rel_vx: float = 0.0
    rel_vy: float = 0.0
    vel_along: float = 0.0
    j_delta_n: float = 0.0
    j_delta_t: float = 0.0

    @staticmethod
    def build(a, b, contact, cached: CachedContact, C: ConstantsDataset, dt: float) -> ResolveContext | None:
        """Construit le contexte"""
        has_rb_a = a.has(RigidBody)
        has_rb_b = b.has(RigidBody)
        rb_a = a.rigid_body if has_rb_a else None
        rb_b = b.rigid_body if has_rb_b else None
        static_a = (not has_rb_a) or rb_a.is_static()
        static_b = (not has_rb_b) or rb_b.is_static()
        if static_a and static_b:
            return None
        nx, ny = contact.normal.x, contact.normal.y
        depth = contact.depth
        inv_a = inv_b = inv_sum = 0.0
        rel_vx = rel_vy = vel_along = 0.0
        if has_rb_a and has_rb_b:
            inv_a = 0.0 if static_a else 1.0 / rb_a.mass
            inv_b = 0.0 if static_b else 1.0 / rb_b.mass
            inv_sum = inv_a + inv_b
            vax = rb_a.velocity.x + (rb_a._acceleration.x * dt if not static_a else 0.0)
            vay = rb_a.velocity.y + (rb_a._acceleration.y * dt if not static_a else 0.0)
            vbx = rb_b.velocity.x + (rb_b._acceleration.x * dt if not static_b else 0.0)
            vby = rb_b.velocity.y + (rb_b._acceleration.y * dt if not static_b else 0.0)
            rel_vx = vax - vbx
            rel_vy = vay - vby
            vel_along = rel_vx * nx + rel_vy * ny
        return ResolveContext(
            a=a, b=b, contact=contact, cached=cached, C=C, dt=dt,
            has_rb_a=has_rb_a, has_rb_b=has_rb_b,
            rb_a=rb_a, rb_b=rb_b,
            static_a=static_a, static_b=static_b,
            inv_a=inv_a, inv_b=inv_b, inv_sum=inv_sum,
            tr_a=a.transform, tr_b=b.transform,
            nx=nx, ny=ny, tx=-ny, ty=nx, depth=depth,
            rel_vx=rel_vx, rel_vy=rel_vy, vel_along=vel_along,
        )

# ======================================== processor ========================================
resolve_processor = Processor("resolve")

@resolve_processor.step
def _wake(ctx: ResolveContext):
    """Réveil des corps endormis uniquement si l'impact est significatif"""
    if ctx.vel_along >= -ctx.C.VEL_ALONG_WAKE_TRESHOLD:
        return
    if ctx.has_rb_a and ctx.rb_a.is_sleeping():
        ctx.rb_a.wake()
    if ctx.has_rb_b and ctx.rb_b.is_sleeping():
        ctx.rb_b.wake()

@resolve_processor.step
def _position_only(ctx: ResolveContext):
    """Cas sans RigidBody des deux côtés : correction de position uniquement"""
    if ctx.has_rb_a and ctx.has_rb_b:
        return
    correction = min(max(ctx.depth - ctx.C.SLOP, 0.0) * ctx.C.BAUMGARTE, ctx.C.MAX_CORRECTION)
    if correction > 0:
        if ctx.static_a:
            ctx.tr_b.x -= ctx.nx * correction
            ctx.tr_b.y -= ctx.ny * correction
        else:
            ctx.tr_a.x += ctx.nx * correction
            ctx.tr_a.y += ctx.ny * correction
    return False

@resolve_processor.step
def _check_inv_sum(ctx: ResolveContext):
    """Court-circuit si masses infinies des deux côtés"""
    if ctx.inv_sum == 0:
        return False

@resolve_processor.step
def _baumgarte(ctx: ResolveContext):
    """Correction de position Baumgarte si les objets se rapprochent"""
    if ctx.vel_along >= 0:
        return
    correction = min(max(ctx.depth - ctx.C.SLOP, 0.0) * ctx.C.BAUMGARTE, ctx.C.MAX_CORRECTION)
    if correction <= 0:
        return
    if ctx.static_a:
        ctx.tr_b.x -= ctx.nx * correction
        ctx.tr_b.y -= ctx.ny * correction
    elif ctx.static_b:
        ctx.tr_a.x += ctx.nx * correction
        ctx.tr_a.y += ctx.ny * correction
    else:
        # ra + rb == 1.0 naturellement, pas besoin de cap
        ra = ctx.inv_a / ctx.inv_sum
        rb = ctx.inv_b / ctx.inv_sum
        ctx.tr_a.x += ctx.nx * correction * ra
        ctx.tr_a.y += ctx.ny * correction * ra
        ctx.tr_b.x -= ctx.nx * correction * rb
        ctx.tr_b.y -= ctx.ny * correction * rb

@resolve_processor.step
def _normal_impulse(ctx: ResolveContext):
    """Calcul et clamping de l'impulsion normale avec restitution"""
    if not ctx.static_a and not ctx.static_b:
        restitution = min(ctx.rb_a.restitution, ctx.rb_b.restitution)
    elif ctx.static_a:
        restitution = ctx.rb_b.restitution
    else:
        restitution = ctx.rb_a.restitution

    if ctx.vel_along < -ctx.C.RESTITUTION_THRESHOLD:
        t = min((-ctx.vel_along - ctx.C.RESTITUTION_THRESHOLD) / (ctx.C.RESTITUTION_MAX_VEL - ctx.C.RESTITUTION_THRESHOLD), 1.0)
        j_delta_n = -(1.0 + restitution * t) * ctx.vel_along / ctx.inv_sum
    elif ctx.vel_along < 0:
        j_delta_n = -ctx.vel_along / ctx.inv_sum
    else:
        j_delta_n = 0.0

    if abs(j_delta_n) < 1e-3:
        j_delta_n = 0.0

    old_jn = ctx.cached.jn
    ctx.cached.jn = max(0.0, old_jn + j_delta_n)
    ctx.j_delta_n = ctx.cached.jn - old_jn

@resolve_processor.step
def _friction(ctx: ResolveContext):
    """Calcul de la friction tangentielle"""
    # Surface quasi-verticale : pas de friction tangentielle
    if abs(ctx.ny) < 0.3:
        ctx.cached.jt = 0.0
        ctx.j_delta_t = 0.0
        return

    # Friction effective = combinaison des deux matériaux
    if not ctx.static_a and not ctx.static_b:
        friction_dynamic = (ctx.rb_a.friction + ctx.rb_b.friction) * 0.5
    elif ctx.static_a:
        friction_dynamic = ctx.rb_b.friction
    else:
        friction_dynamic = ctx.rb_a.friction

    # Ratio standard (Box2D) : static légèrement supérieur au dynamique
    friction_static = friction_dynamic * 1.5

    vel_tan = ctx.rel_vx * ctx.tx + ctx.rel_vy * ctx.ty
    j_delta_t_needed = -vel_tan / ctx.inv_sum
    old_jt = ctx.cached.jt

    # Cône de Coulomb : statique si dans le cône, dynamique sinon
    limit_s = friction_static  * ctx.cached.jn
    limit_d = friction_dynamic * ctx.cached.jn
    if abs(old_jt + j_delta_t_needed) <= limit_s:
        ctx.cached.jt = max(-limit_s, min(limit_s, old_jt + j_delta_t_needed))
    else:
        ctx.cached.jt = max(-limit_d, min(limit_d, old_jt + j_delta_t_needed))
    ctx.j_delta_t = ctx.cached.jt - old_jt

@resolve_processor.step
def _apply(ctx: ResolveContext):
    """Application des impulsions normale et tangentielle"""
    ix = ctx.nx * ctx.j_delta_n + ctx.tx * ctx.j_delta_t
    iy = ctx.ny * ctx.j_delta_n + ctx.ty * ctx.j_delta_t
    if not ctx.static_a:
        ctx.rb_a.velocity = Vector._make(ctx.rb_a.velocity.x + ix * ctx.inv_a, ctx.rb_a.velocity.y + iy * ctx.inv_a)
    if not ctx.static_b:
        ctx.rb_b.velocity = Vector._make(ctx.rb_b.velocity.x - ix * ctx.inv_b, ctx.rb_b.velocity.y - iy * ctx.inv_b)

# ======================================== FACADE ========================================
def resolve(a: Shape, b: Shape, contact: Contact, cached: CachedContact, C: ConstantsDataset, dt: float):
    """Sequential Impulse Solver avec vitesse prédictive"""
    ctx = ResolveContext.build(a, b, contact, cached, C, dt)
    if ctx is None:
        return
    resolve_processor(ctx)