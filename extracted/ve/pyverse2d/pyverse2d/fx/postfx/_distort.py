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

_FRAG_SWIRL = f"""
#version 330 core
uniform sampler2D u_texture;
uniform vec2 u_center;
uniform float u_angle;
uniform float u_falloff;
in vec2 v_uv;
out vec4 out_color;

{GLSL_MASK}

void main() {{
    vec2 delta = v_uv - u_center;
    float dist = length(delta);
    float norm = clamp(1.0 - dist / max(u_falloff, 0.0001), 0.0, 1.0);
    float theta = u_angle * norm * norm;
    float c = cos(theta);
    float s = sin(theta);
    vec2 rotated = vec2(c * delta.x - s * delta.y, s * delta.x + c * delta.y);
    vec2 distorted = clamp(u_center + rotated, 0.0, 1.0);

    float mask = compute_mask();
    vec4 orig = texture(u_texture, v_uv);
    vec4 warped = texture(u_texture, mix(v_uv, distorted, mask));
    out_color = vec4(warped.rgb, orig.a);
}}
"""

_FRAG_SQUEEZE = f"""
#version 330 core
uniform sampler2D u_texture;
uniform vec2 u_center;
uniform float u_strength_x;
uniform float u_strength_y;
uniform float u_falloff;
in vec2 v_uv;
out vec4 out_color;

{GLSL_MASK}

void main() {{
    vec2 delta = v_uv - u_center;
    float norm = clamp(length(delta) / max(u_falloff, 0.0001), 0.0, 1.0);
    float wx = 1.0 + u_strength_x * (1.0 - norm);
    float wy = 1.0 + u_strength_y * (1.0 - norm);
    vec2 distorted = clamp(u_center + delta * vec2(wx, wy), 0.0, 1.0);

    float mask = compute_mask();
    vec4 orig = texture(u_texture, v_uv);
    vec4 warped = texture(u_texture, mix(v_uv, distorted, mask));
    out_color = vec4(warped.rgb, orig.a);
}}
"""

_FRAG_RIPPLE = f"""
#version 330 core
uniform sampler2D u_texture;
uniform vec2 u_center;
uniform float u_amplitude;
uniform float u_frequency;
uniform float u_time;
uniform float u_falloff;
in vec2 v_uv;
out vec4 out_color;

{GLSL_MASK}

void main() {{
    const float TAU = 6.28318530718;
    vec2 delta = v_uv - u_center;
    float dist = length(delta);
    float norm = clamp(1.0 - dist / max(u_falloff, 0.0001), 0.0, 1.0);
    vec2 dir = (dist > 0.0001) ? delta / dist : vec2(0.0);
    float wave = u_amplitude * norm * sin(dist * u_frequency * TAU - u_time);
    vec2 distorted = clamp(v_uv + dir * wave, 0.0, 1.0);

    float mask = compute_mask();
    vec4 orig = texture(u_texture, v_uv);
    vec4 warped = texture(u_texture, mix(v_uv, distorted, mask));
    out_color = vec4(warped.rgb, orig.a);
}}
"""

# ======================================== SWIRL ========================================
@dataclass(slots=True, frozen=True)
class DistortSwirl(PostFxEffect):
    """Effet post-processing: distorsion en vortex

    Applique une rotation dont l'angle décroît depuis le centre vers les bords.
    Animer ``angle`` produit un effet de portail ou d'étourdissement.

    Args:
        angle: angle de rotation au centre en radians
        falloff: rayon de normalisation en unités mondes *(> 0)*
    """
    angle: Real = 1.0
    falloff: Real = 10

    _ID: ClassVar[str] = "distort_swirl"

    def __post_init__(self) -> None:
        object.__setattr__(self, "angle", float(self.angle))
        object.__setattr__(self, "falloff", float(self.falloff))
        
        if __debug__:
            over(self.falloff, 0, include=False)

# ======================================== SQUEEZE ========================================
@dataclass(slots=True, frozen=True)
class DistortSqueeze(PostFxEffect):
    """Effet post-processing: étirement directionnel asymétrique

    Déforme les pixels avec un facteur d'échelle indépendant sur X et Y, décroissant depuis le centre.
    Valeurs positives étirent, négatives compriment.

    Args:
        strength_x: intensité horizontale *(>-1 pour éviter l'inversion)*
        strength_y: intensité verticale *(>-1 pour éviter l'inversion)*
        falloff: rayon de normalisation en unités monde *(> 0)*
    """
    strength_x: Real = 10
    strength_y: Real = -10
    falloff: Real = 0.5

    _ID: ClassVar[str] = "distort_squeeze"

    def __post_init__(self) -> None:
        object.__setattr__(self, "strength_x", float(self.strength_x))
        object.__setattr__(self, "strength_y", float(self.strength_y))
        object.__setattr__(self, "falloff", float(self.falloff))

        if __debug__:
            over(self.falloff, 0, include=False)
            over(self.strength_x, -1.0, include=False)
            over(self.strength_y, -1.0, include=False)


# ======================================== RIPPLE ========================================
@dataclass(slots=True, frozen=True)
class DistortRipple(PostFxEffect):
    """Effet post-processing: onde concentrique

    Propage une onde radiale depuis le centre de la zone.
    Contrairement à ``Wave`` (cartésien), la propagation est circulaire.

    Args:
        amplitude: déplacement maximal en unités monde *(>= 0)*
        frequency: nombre de cycles visibles dans le rayon *(> 0)*
        speed: vitesse d'animation en cycles par seconde *(> 0)*
        falloff: rayon de normalisation en unités monde *(> 0)*
    """
    amplitude: Real = 10
    frequency: Real = 12.0
    speed: Real = 1.0
    falloff: Real = 0.5

    _ID: ClassVar[str] = "distort_ripple"

    def __post_init__(self) -> None:
        object.__setattr__(self, "amplitude", float(self.amplitude))
        object.__setattr__(self, "frequency", float(self.frequency))
        object.__setattr__(self, "speed", float(self.speed))
        object.__setattr__(self, "falloff", float(self.falloff))

        if __debug__:
            positive(self.amplitude)
            over(self.frequency, 0, include=False)
            over(self.speed, 0, include=False)
            over(self.falloff, 0, include=False)

# ======================================== HELPERS ========================================
def _center_from_mask(mask: MaskData, fbo) -> tuple[float, float]:
    """Dérive le centre UV depuis le MaskData ou fallback au centre du framebuffer"""
    if mask.type == 0:
        return 0.5, 0.5
    return mask.center_x / fbo.width, mask.center_y / fbo.height

# ======================================== RENDERERS ========================================
class DistortSwirlPostFxRenderer(SpecializedPostFxRenderer):
    """Renderer spécialisé pour l'effet ``DistortSwirl``"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[type[PostFxEffect]]] = frozenset({DistortSwirl})
    _program: ClassVar[ShaderProgram | None] = None

    @classmethod
    def _get_program(cls) -> ShaderProgram:
        if cls._program is None:
            cls._program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG_SWIRL, 'fragment'))
        return cls._program

    @classmethod
    def clear_shader_cache(cls) -> None:
        cls._program = None

    def apply(self, pipeline: Pipeline, effect: DistortSwirl, mask: MaskData) -> None:
        cx, cy = _center_from_mask(mask, pipeline.fbo)
        falloff = pipeline.scale_to_framebuffer(falloff)

        pipeline.apply_shader(
            self._get_program(),
            u_center=(cx, cy),
            u_angle=effect.angle,
            u_falloff=falloff,
            **mask.as_uniforms(),
        )


class DistortSqueezePostFxRenderer(SpecializedPostFxRenderer):
    """Renderer spécialisé pour l'effet ``DistortSqueeze``"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[type[PostFxEffect]]] = frozenset({DistortSqueeze})
    _program: ClassVar[ShaderProgram | None] = None

    @classmethod
    def _get_program(cls) -> ShaderProgram:
        if cls._program is None:
            cls._program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG_SQUEEZE, 'fragment'))
        return cls._program

    @classmethod
    def clear_shader_cache(cls) -> None:
        cls._program = None

    def apply(self, pipeline: Pipeline, effect: DistortSqueeze, mask: MaskData) -> None:
        cx, cy = _center_from_mask(mask, pipeline.fbo)
        sx, sy = pipeline.scale_to_framebuffer(effect.strength_x, effect.strength_y)
        falloff = pipeline.scale_to_framebuffer(falloff)

        pipeline.apply_shader(
            self._get_program(),
            u_center=(cx, cy),
            u_strength_x=sx,
            u_strength_y=sy,
            u_falloff=falloff,
            **mask.as_uniforms(),
        )

class DistortRipplePostFxRenderer(SpecializedPostFxRenderer):
    """Renderer spécialisé pour l'effet ``DistortRipple``"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[type[PostFxEffect]]] = frozenset({DistortRipple})
    _REQUIRES_TIME: ClassVar[bool] = True
    _program: ClassVar[ShaderProgram | None] = None
    _time: ClassVar[float] = 0.0

    @classmethod
    def _get_program(cls) -> ShaderProgram:
        if cls._program is None:
            cls._program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG_RIPPLE, 'fragment'))
        return cls._program

    @classmethod
    def clear_shader_cache(cls) -> None:
        cls._program = None

    def apply(self, pipeline: Pipeline, effect: DistortRipple, mask: MaskData) -> None:
        cx, cy = _center_from_mask(mask, pipeline.fbo)
        amplitude, falloff = pipeline.scale_to_framebuffer(amplitude, falloff)
        
        pipeline.apply_shader(
            self._get_program(),
            u_center=(cx, cy),
            u_amplitude=amplitude,
            u_frequency=effect.frequency,
            u_time=self._time * effect.speed,
            u_falloff=falloff,
            **mask.as_uniforms(),
        )

# ======================================== EXPORTS ========================================
__all__ = [
    "DistortSwirl",
    "DistortSqueeze",
    "DistortRipple",

    "DistortSwirlPostFxRenderer",
    "DistortSqueezePostFxRenderer",
    "DistortRipplePostFxRenderer",
]