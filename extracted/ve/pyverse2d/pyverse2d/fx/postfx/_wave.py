# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import positive, over
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
uniform float u_amplitude_x;
uniform float u_amplitude_y;
uniform float u_frequency_x;
uniform float u_frequency_y;
uniform float u_time;
in vec2 v_uv;
out vec4 out_color;

{GLSL_MASK}

void main() {{
    const float TAU = 6.28318530718;
    float mask = compute_mask();
    float dx = u_amplitude_x * mask * sin(v_uv.y * u_frequency_x * TAU + u_time);
    float dy = u_amplitude_y * mask * sin(v_uv.x * u_frequency_y * TAU + u_time);
    vec2 distorted = clamp(v_uv + vec2(dx, dy), 0.0, 1.0);
    out_color = texture(u_texture, distorted);
}}
"""

# ======================================== EFFECT ========================================
@dataclass(slots=True, frozen=True)
class Wave(PostFxEffect):
    """Effet post-processing: distorsion ondulatoire

    Args:
        amplitude_x: amplitude horizontale en fraction de l'écran *[0, 1]*
        amplitude_y: amplitude verticale en fraction de l'écran *[0, 1]*
        frequency_x: fréquence spatiale horizontale *(cycles par écran)*
        frequency_y: fréquence spatiale verticale *(cycles par écran)*
        speed: vitesse d'animation en cycles par seconde *(> 0)*
    """
    amplitude_x: Real = 0.01
    amplitude_y: Real = 0.0
    frequency_x: Real = 8.0
    frequency_y: Real = 8.0
    speed: Real = 1.0

    _ID: ClassVar[str] = "wave"

    def __post_init__(self) -> None:
        object.__setattr__(self, "amplitude_x", float(self.amplitude_x))
        object.__setattr__(self, "amplitude_y", float(self.amplitude_y))
        object.__setattr__(self, "frequency_x", float(self.frequency_x))
        object.__setattr__(self, "frequency_y", float(self.frequency_y))
        object.__setattr__(self, "speed", float(self.speed))

        if __debug__:
            positive(self.amplitude_x)
            positive(self.amplitude_y)
            over(self.frequency_x, 0, include=False)
            over(self.frequency_y, 0, include=False)
            over(self.speed, 0, include=False)

# ======================================== RENDERER ========================================
class WavePostFxRenderer(SpecializedPostFxRenderer):
    """Renderer spécialisé pour l'effet ``Wave``"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[type[PostFxEffect]]] = frozenset({Wave})

    _program: ClassVar[ShaderProgram | None] = None
    _time: ClassVar[float] = 0.0

    @classmethod
    def tick(cls, dt: float) -> None:
        """Avance l'horloge interne partagée entre toutes les instances

        Args:
            dt: delta-time en secondes
        """
        cls._time += dt

    @classmethod
    def _get_program(cls) -> ShaderProgram:
        """Retourne (en le créant si nécessaire) le shader de distorsion ondulatoire"""
        if cls._program is None:
            cls._program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG, 'fragment'))
        return cls._program

    @classmethod
    def clear_shader_cache(cls) -> None:
        """Libère le ``ShaderProgram`` mis en cache"""
        cls._program = None

    def apply(self, pipeline: Pipeline, effect: Wave, mask: MaskData) -> None:
        """Applique la distorsion ondulatoire

        Args:
            pipeline: ``Pipeline`` de rendu courant
            effect: paramètres de l'onde
            mask: données de masque spatial
        """
        pipeline.apply_shader(
            self._get_program(),
            u_amplitude_x=effect.amplitude_x,
            u_amplitude_y=effect.amplitude_y,
            u_frequency_x=effect.frequency_x,
            u_frequency_y=effect.frequency_y,
            u_time=self._time * effect.speed,
            **mask.as_uniforms(),
        )

# ======================================== EXPORTS ========================================
__all__ = [
    "Wave",
    "WavePostFxRenderer",
]