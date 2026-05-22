# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import clamped, over
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
uniform float u_spacing;
uniform float u_strength;
uniform float u_softness;
in vec2 v_uv;
out vec4 out_color;

{GLSL_MASK}

void main() {{
    vec4 orig = texture(u_texture, v_uv);
    float mask = compute_mask();
    float line = abs(sin(gl_FragCoord.y * 3.14159 / u_spacing));
    float dim = 1.0 - u_strength * pow(1.0 - line, 1.0 / max(u_softness, 0.001));
    out_color = vec4(mix(orig.rgb, orig.rgb * dim, mask), orig.a);
}}
"""

# ======================================== EFFECT ========================================
@dataclass(slots=True, frozen=True)
class Scanlines(PostFxEffect):
    """Effet post-processing: lignes de balayage CRT

    Args:
        spacing: espacement entre les lignes en unités monde *(> 0)*
        strength: intensité de l'assombrissement *[0, 1]*
        softness: douceur du bord de chaque ligne *(> 0)* (1 = linéaire, < 1 = plus dur)
    """
    spacing: Real = 3.0
    strength: Real = 0.4
    softness: Real = 0.5

    _ID: ClassVar[str] = "scanlines"

    def __post_init__(self) -> None:
        object.__setattr__(self, "spacing", float(self.spacing))
        object.__setattr__(self, "strength", float(self.strength))
        object.__setattr__(self, "softness", float(self.softness))

        if __debug__:
            over(self.spacing, 0, include=False)
            clamped(self.strength)
            over(self.softness, 0, include=False)

# ======================================== RENDERER ========================================
class ScanlinesPostFxRenderer(SpecializedPostFxRenderer):
    """Renderer spécialisé pour l'effet ``Scanlines``"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[type[PostFxEffect]]] = frozenset({Scanlines})
    _program: ClassVar[ShaderProgram | None] = None

    @classmethod
    def _get_program(cls) -> ShaderProgram:
        if cls._program is None:
            cls._program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG, 'fragment'))
        return cls._program

    @classmethod
    def clear_shader_cache(cls) -> None:
        cls._program = None

    def apply(self, pipeline: Pipeline, effect: Scanlines, mask: MaskData) -> None:
        spacing = pipeline.scale_to_framebuffer(height=effect.spacing)
        
        pipeline.apply_shader(
            self._get_program(),
            u_spacing=spacing,
            u_strength=effect.strength,
            u_softness=effect.softness,
            **mask.as_uniforms(),
        )

# ======================================== EXPORTS ========================================
__all__ = [
    "Scanlines",
    "ScanlinesPostFxRenderer",
]