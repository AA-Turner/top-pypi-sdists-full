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
uniform float u_amplitude;
uniform float u_time;
in vec2 v_uv;
out vec4 out_color;

{GLSL_MASK}

float rand(float x) {{
    return fract(sin(x * 127.1) * 43758.5453);
}}

void main() {{
    vec4 orig = texture(u_texture, v_uv);
    float mask = compute_mask();
    // Variation rapide et irrégulière
    float t = floor(u_time * 24.0);
    float flicker = 1.0 - u_amplitude * rand(t);
    out_color = vec4(mix(orig.rgb, orig.rgb * flicker, mask), orig.a);
}}
"""

# ======================================== EFFECT ========================================
@dataclass(slots=True, frozen=True)
class Flicker(PostFxEffect):
    """Effet post-processing: scintillement de luminosité

    Fait varier aléatoirement la luminosité du framebuffer à haute fréquence, simulant une source lumineuse instable (néon, torche, écran défaillant).

    Args:
        amplitude: amplitude de la variation *[0, 1]* (0 = aucun scintillement)
        speed: fréquence de renouvellement en Hz *(> 0)*
    """
    amplitude: Real = 0.15
    speed: Real = 1.0

    _ID: ClassVar[str] = "flicker"

    def __post_init__(self) -> None:
        object.__setattr__(self, "amplitude", float(self.amplitude))
        object.__setattr__(self, "speed", float(self.speed))

        if __debug__:
            clamped(self.amplitude)
            over(self.speed, 0, include=False)

# ======================================== RENDERER ========================================
class FlickerPostFxRenderer(SpecializedPostFxRenderer):
    """Renderer spécialisé pour l'effet ``Flicker``"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[type[PostFxEffect]]] = frozenset({Flicker})
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

    def apply(self, pipeline: Pipeline, effect: Flicker, mask: MaskData) -> None:
        pipeline.apply_shader(
            self._get_program(),
            u_amplitude=effect.amplitude,
            u_time=self._time * effect.speed,
            **mask.as_uniforms(),
        )

# ======================================== EXPORTS ========================================
__all__ = [
    "Flicker",
    "FlickerPostFxRenderer",
]