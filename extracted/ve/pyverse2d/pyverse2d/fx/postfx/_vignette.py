# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import clamped, positive
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
uniform float u_strength;
uniform float u_radius;
uniform float u_softness;
uniform vec3 u_color;
in vec2 v_uv;
out vec4 out_color;

{GLSL_MASK}

void main() {{
    vec4 orig = texture(u_texture, v_uv);
    float mask = compute_mask();
    float d = length(v_uv - vec2(0.5));
    float vignette = 1.0 - smoothstep(u_radius, u_radius + u_softness, d) * u_strength;
    vec3 vignetted = orig.rgb * mix(vec3(1.0), u_color, 1.0 - vignette);
    out_color = vec4(mix(orig.rgb, vignetted, mask), orig.a);
}}
"""

# ======================================== EFFECT ========================================
@dataclass(slots=True, frozen=True)
class Vignette(PostFxEffect):
    """Effet post-processing: vignette

    Assombrit les bords du framebuffer vers une couleur cible.

    Args:
        strength: intensité de la vignette *[0, 1]*
        radius: rayon intérieur en unités monde *(>= 0)*
        softness: largeur du fondu en unités monde *(>= 0)*
        color: couleur de la vignette RGB (défaut noir)
    """
    strength: Real = 0.8
    radius: Real = 100
    softness: Real = 30
    color: Color = (0.0, 0.0, 0.0)

    _ID: ClassVar[str] = "vignette"

    def __post_init__(self) -> None:
        object.__setattr__(self, "strength", float(self.strength))
        object.__setattr__(self, "radius", float(self.radius))
        object.__setattr__(self, "softness", float(self.softness))
        object.__setattr__(self, "color", Color(self.color))

        if __debug__:
            clamped(self.strength)
            positive(self.radius)
            positive(self.softness)

# ======================================== RENDERER ========================================
class VignettePostFxRenderer(SpecializedPostFxRenderer):
    """Renderer spécialisé pour l'effet ``Vignette``"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[type[PostFxEffect]]] = frozenset({Vignette})
    _program: ClassVar[ShaderProgram | None] = None

    @classmethod
    def _get_program(cls) -> ShaderProgram:
        if cls._program is None:
            cls._program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG, 'fragment'))
        return cls._program

    @classmethod
    def clear_shader_cache(cls) -> None:
        cls._program = None

    def apply(self, pipeline: Pipeline, effect: Vignette, mask: MaskData) -> None:
        radius, softness = pipeline.scale_to_framebuffer(effect.radius, effect.softness)
        radius /= pipeline.fbo.width
        softness /= pipeline.fbo.width
        
        pipeline.apply_shader(
            self._get_program(),
            u_strength=effect.strength,
            u_radius=radius,
            u_softness=softness,
            u_color=effect.color.rgb,
            **mask.as_uniforms(),
        )

# ======================================== EXPORTS ========================================
__all__ = [
    "Vignette",
    "VignettePostFxRenderer",
]