# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import clamped, over
from ..._rendering import Pipeline
from ...abc import PostFxEffect
from ...asset import Color

from ._specialized_renderer import SpecializedPostFxRenderer
from ._mask import MaskData, GLSL_MASK

from dataclasses import dataclass
from numbers import Real
from typing import ClassVar

from pyglet.graphics.shader import Shader, ShaderProgram

# ======================================== SHADERS ========================================
_VERT = """
#version 330 core
layout(location = 0) in vec2 in_position;
layout(location = 1) in vec2 in_uv;
out vec2 v_uv;
void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
    v_uv = in_uv;
}
"""

_FRAG = f"""
#version 330 core
uniform sampler2D u_texture;
uniform vec2 u_texel;
uniform float u_threshold;
uniform float u_strength;
uniform vec3 u_edge_color;
in vec2 v_uv;
out vec4 out_color;

{GLSL_MASK}

float lum(vec3 c) {{
    return dot(c, vec3(0.2126, 0.7152, 0.0722));
}}

void main() {{
    vec4 orig = texture(u_texture, v_uv);
    float mask = compute_mask();

    // Sobel 3x3
    float tl = lum(texture(u_texture, v_uv + u_texel * vec2(-1, 1)).rgb);
    float tm = lum(texture(u_texture, v_uv + u_texel * vec2( 0, 1)).rgb);
    float tr = lum(texture(u_texture, v_uv + u_texel * vec2( 1, 1)).rgb);
    float ml = lum(texture(u_texture, v_uv + u_texel * vec2(-1, 0)).rgb);
    float mr = lum(texture(u_texture, v_uv + u_texel * vec2( 1, 0)).rgb);
    float bl = lum(texture(u_texture, v_uv + u_texel * vec2(-1, -1)).rgb);
    float bm = lum(texture(u_texture, v_uv + u_texel * vec2( 0, -1)).rgb);
    float br = lum(texture(u_texture, v_uv + u_texel * vec2( 1, -1)).rgb);

    float gx = -tl - 2.0*ml - bl + tr + 2.0*mr + br;
    float gy = -tl - 2.0*tm - tr + bl + 2.0*bm + br;
    float edge = length(vec2(gx, gy));

    float detected = smoothstep(u_threshold, u_threshold + 0.1, edge) * u_strength;
    vec3 composited = mix(orig.rgb, u_edge_color, detected);
    out_color = vec4(mix(orig.rgb, composited, mask), orig.a);
}}
"""

# ======================================== EFFECT ========================================
@dataclass(slots=True, frozen=True)
class EdgeDetect(PostFxEffect):
    """Effet post-processing: détection de contours (Sobel)

    Superpose les contours détectés par un filtre Sobel 3×3 sur l'image originale.
    Utile pour des effets de vision thermique, cel-shading, ou stylisation graphique.

    Args:
        threshold: seuil de détection *(>= 0)*
        strength: opacité des contours détectés *[0, 1]*
        edge_color: couleur des contours RGB *(défaut blanc)*
    """
    threshold: Real = 0.1
    strength: Real = 1.0
    edge_color: Color = (1.0, 1.0, 1.0)

    _ID: ClassVar[str] = "edge_detect"

    def __post_init__(self) -> None:
        object.__setattr__(self, "threshold", float(self.threshold))
        object.__setattr__(self, "strength", float(self.strength))
        object.__setattr__(self, "edge_color", Color(self.edge_color))

        if __debug__:
            over(self.threshold, 0, include=True)
            clamped(self.strength)

# ======================================== RENDERER ========================================
class EdgeDetectPostFxRenderer(SpecializedPostFxRenderer):
    """Renderer spécialisé pour l'effet ``EdgeDetect``"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[type[PostFxEffect]]] = frozenset({EdgeDetect})
    _program: ClassVar[ShaderProgram | None] = None

    @classmethod
    def _get_program(cls) -> ShaderProgram:
        if cls._program is None:
            cls._program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG, 'fragment'))
        return cls._program

    @classmethod
    def clear_shader_cache(cls) -> None:
        cls._program = None

    def apply(self, pipeline: Pipeline, effect: EdgeDetect, mask: MaskData) -> None:
        fbo = pipeline.fbo
        
        pipeline.apply_shader(
            self._get_program(),
            u_texel=(1.0 / fbo.width, 1.0 / fbo.height),
            u_threshold=effect.threshold,
            u_strength=effect.strength,
            u_edge_color=effect.edge_color.rgb,
            **mask.as_uniforms(),
        )

# ======================================== EXPORTS ========================================
__all__ = [
    "EdgeDetect",
    "EdgeDetectPostFxRenderer",
]