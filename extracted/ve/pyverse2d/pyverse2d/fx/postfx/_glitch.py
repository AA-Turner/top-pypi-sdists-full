# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import clamped, over, positive
from ..._rendering import Pipeline
from ...abc import PostFxEffect

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
uniform float u_strength;
uniform float u_density;
uniform float u_time;
in vec2 v_uv;
out vec4 out_color;

{GLSL_MASK}

float rand(vec2 co) {{
    return fract(sin(dot(co, vec2(127.1, 311.7))) * 43758.5453);
}}

void main() {{
    float mask = compute_mask();

    // Bandes horizontales aléatoires
    float band_y = floor(v_uv.y * 64.0) / 64.0;
    float r = rand(vec2(band_y, floor(u_time * 12.0)));
    float active = step(1.0 - u_density, r);
    float shift = (rand(vec2(band_y, u_time)) * 2.0 - 1.0) * u_strength * active;

    vec2 uv_r = clamp(vec2(v_uv.x + shift * 1.2, v_uv.y), 0.0, 1.0);
    vec2 uv_g = clamp(vec2(v_uv.x + shift, v_uv.y), 0.0, 1.0);
    vec2 uv_b = clamp(vec2(v_uv.x + shift * 0.8, v_uv.y), 0.0, 1.0);

    vec4 orig = texture(u_texture, v_uv);
    float cr = texture(u_texture, uv_r).r;
    float cg = texture(u_texture, uv_g).g;
    float cb = texture(u_texture, uv_b).b;

    out_color = vec4(mix(orig.rgb, vec3(cr, cg, cb), mask), orig.a);
}}
"""

# ======================================== EFFECT ========================================
@dataclass(slots=True, frozen=True)
class Glitch(PostFxEffect):
    """Effet post-processing: corruption vidéo

    Décale des bandes horizontales aléatoires avec une aberration chromatique intégrée, produisant un effet de corruption numérique.

    Args:
        strength: amplitude du décalage horizontal en unités monde *(>= 0)*
        density: densité des bandes affectées *[0, 1]*
        speed: vitesse de renouvellement des bandes *(> 0)*
    """
    strength: Real = 30
    density: Real = 0.2
    speed: Real = 1.0

    _ID: ClassVar[str] = "glitch"

    def __post_init__(self) -> None:
        object.__setattr__(self, "strength", float(self.strength))
        object.__setattr__(self, "density", float(self.density))
        object.__setattr__(self, "speed", float(self.speed))

        if __debug__:
            positive(self.strength)
            clamped(self.density)
            over(self.speed, 0, include=False)

# ======================================== RENDERER ========================================
class GlitchPostFxRenderer(SpecializedPostFxRenderer):
    """Renderer spécialisé pour l'effet ``Glitch``"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[type[PostFxEffect]]] = frozenset({Glitch})
    _REQUIRES_TIME: ClassVar[bool] = True
    _program: ClassVar[ShaderProgram | None] = None
    _time: ClassVar[float] = 0.0

    @classmethod
    def _get_program(cls) -> ShaderProgram:
        if cls._program is None:
            cls._program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG, 'fragment'))
        return cls._program

    @classmethod
    def clear_shader_cache(cls) -> None:
        cls._program = None

    def apply(self, pipeline: Pipeline, effect: Glitch, mask: MaskData) -> None:
        strength = pipeline.scale_to_framebuffer(effect.strength)
        
        pipeline.apply_shader(
            self._get_program(),
            u_strength=strength,
            u_density=effect.density,
            u_time=self._time * effect.speed,
            **mask.as_uniforms(),
        )

# ======================================== EXPORTS ========================================
__all__ = [
    "Glitch",
    "GlitchPostFxRenderer",
]