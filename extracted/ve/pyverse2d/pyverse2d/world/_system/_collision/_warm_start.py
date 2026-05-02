# ======================================== IMPORTS ========================================
from __future__ import annotations

from dataclasses import dataclass

from ...._internal import Processor
from ....math import Vector
from ....abc import Shape

from ..._component import RigidBody

from ._constants import ConstantsDataset
from ._registry import Contact
from ._resolve import CachedContact

# ======================================== CONTEXTE ========================================
@dataclass(slots=True)
class WarmStartContext:
    """Contexte partagé entre les étapes du warm start"""
    a: Shape
    b: Shape
    contact: Contact
    cached: CachedContact
    C: ConstantsDataset
    rb_a: RigidBody | None = None
    rb_b: RigidBody | None = None
    static_a: bool = False
    static_b: bool = False
    inv_a: float = 0.0
    inv_b: float = 0.0
    nx: float = 0.0
    ny: float = 0.0
    tx: float = 0.0
    ty: float = 0.0
    vel_along: float = 0.0
    _jn: float = 0.0
    _jt: float = 0.0

    @staticmethod
    def build(a: Shape, b: Shape, contact: Contact, cached: CachedContact, C: ConstantsDataset) -> WarmStartContext | None:
        """Construit le contexte — retourne None si la paire est non résoluble"""
        if not a.has(RigidBody) or not b.has(RigidBody):
            return None
        rb_a = a.get(RigidBody)
        rb_b = b.get(RigidBody)
        static_a = rb_a.is_static()
        static_b = rb_b.is_static()
        if static_a and static_b:
            return None
        nx, ny = contact.normal.x, contact.normal.y
        inv_a = 0.0 if static_a else 1.0 / rb_a.mass
        inv_b = 0.0 if static_b else 1.0 / rb_b.mass
        rel_vx = rb_a.velocity.x - rb_b.velocity.x
        rel_vy = rb_a.velocity.y - rb_b.velocity.y
        return WarmStartContext(
            a=a, b=b, contact=contact, cached=cached, C=C,
            rb_a=rb_a, rb_b=rb_b,
            static_a=static_a, static_b=static_b,
            inv_a=inv_a, inv_b=inv_b,
            nx=nx, ny=ny, tx=-ny, ty=nx,
            vel_along=rel_vx * nx + rel_vy * ny,
        )

# ======================================== processor ========================================
warm_start_processor = Processor("warm_start")

@warm_start_processor.step
def _check_impulses(ctx: WarmStartContext):
    """Skip si impulsions négligeables pour ne pas perturber les objets au repos"""
    jn = ctx.cached.jn * ctx.C.WARM_BIAS
    jt = ctx.cached.jt * ctx.C.WARM_BIAS
    if abs(jn) < 1e-2 and abs(jt) < 1e-2:
        return False
    ctx._jn = jn
    ctx._jt = jt

@warm_start_processor.step
def _check_separation(ctx: WarmStartContext):
    """Skip warm start si les objets s'éloignent : rebond en cours"""
    if ctx.vel_along > 0:
        ctx.cached.jn = 0.0
        ctx.cached.jt = 0.0
        return False

@warm_start_processor.step
def _apply(ctx: WarmStartContext):
    """Application des impulsions précédentes"""
    ix = ctx.nx * ctx._jn + ctx.tx * ctx._jt
    iy = ctx.ny * ctx._jn + ctx.ty * ctx._jt
    if not ctx.static_a:
        ctx.rb_a.velocity = Vector._make(ctx.rb_a.velocity.x + ix * ctx.inv_a, ctx.rb_a.velocity.y + iy * ctx.inv_a)
    if not ctx.static_b:
        ctx.rb_b.velocity = Vector._make(ctx.rb_b.velocity.x - ix * ctx.inv_b, ctx.rb_b.velocity.y - iy * ctx.inv_b)

# ======================================== FACADE ========================================
def warm_start(a: Shape, b: Shape, contact: Contact, cached: CachedContact, C: ConstantsDataset):
    """Ré-applique les impulsions précédentes pour accélérer la convergence"""
    ctx = WarmStartContext.build(a, b, contact, cached, C)
    if ctx is None:
        return
    warm_start_processor(ctx)