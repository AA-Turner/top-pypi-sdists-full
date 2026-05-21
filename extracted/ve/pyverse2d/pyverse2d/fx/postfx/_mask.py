# ======================================== IMPORTS ========================================
from __future__ import annotations

from dataclasses import dataclass

# ======================================== GLSL ========================================
GLSL_MASK: str = """
uniform int   u_mask_type;    // 0 = plein écran, 1 = cercle, 2 = rectangle
uniform vec2  u_mask_center;  // centre en pixels framebuffer
uniform float u_mask_radius;  // rayon en pixels framebuffer   (Circle)
uniform vec2  u_mask_half;    // demi-extents en pixels framebuffer (Rect)
uniform float u_mask_blend;   // largeur du fondu en pixels framebuffer

float compute_mask() {
    if (u_mask_type == 0) return 1.0;

    if (u_mask_type == 1) {
        float d = distance(gl_FragCoord.xy, u_mask_center);
        return 1.0 - smoothstep(u_mask_radius, u_mask_radius + max(u_mask_blend, 1.0), d);
    }

    // SDF rectangle
    vec2  d2   = abs(gl_FragCoord.xy - u_mask_center) - u_mask_half;
    float dist = length(max(d2, 0.0)) + min(max(d2.x, d2.y), 0.0);
    return 1.0 - smoothstep(0.0, max(u_mask_blend, 1.0), dist);
}
"""

# ======================================== MASK DATA ========================================
@dataclass(frozen=True, slots=True)
class MaskData:
    """Données de masque spatial passées aux shaders post-processing.

    Toutes les valeurs sont en **coordonnées framebuffer** (pixels).

    Args:
        type: type de masque — ``0`` plein écran, ``1`` cercle, ``2`` rectangle
        center_x: abscisse du centre
        center_y: ordonnée du centre
        radius: rayon *(Circle)*
        half_w: demi-largeur *(Rect)*
        half_h: demi-hauteur *(Rect)*
        blend: largeur du fondu de bord
    """
    type: int
    center_x: float = 0.0
    center_y: float = 0.0
    radius: float = 0.0
    half_w: float = 0.0
    half_h: float = 0.0
    blend: float = 0.0

    def as_uniforms(self) -> dict[str, object]:
        """Retourne un dict prêt à être dépaqueté dans ``pipeline.apply_shader``"""
        return {
            "u_mask_type":   self.type,
            "u_mask_center": (self.center_x, self.center_y),
            "u_mask_radius": self.radius,
            "u_mask_half":   (self.half_w, self.half_h),
            "u_mask_blend":  self.blend,
        }


# Sentinel : effet plein écran, aucun masque
MASK_FULL: MaskData = MaskData(type=0)

# ======================================== EXPORTS ========================================
__all__ = [
    "GLSL_MASK",
    "MaskData",
    "MASK_FULL",
]