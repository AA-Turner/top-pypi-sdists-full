# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import over, clamped, positive
from ..._rendering import Pipeline
from ...abc import PostFxEffect
from ...asset import Color

from ._specialized_renderer import SpecializedPostFxRenderer
from ._mask import MaskData, GLSL_MASK

from pyglet.graphics.shader import Shader, ShaderProgram

from dataclasses import dataclass
from numbers import Real, Integral
from typing import ClassVar
import math

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
uniform vec2 u_wind;
uniform float u_time;
uniform float u_base;
uniform float u_density;
uniform float u_softness;
uniform float u_scale;
uniform float u_warp;
uniform int u_octaves;
uniform float u_lacunarity;
uniform float u_gain;
uniform vec3 u_color;
uniform mat4 u_inv_mvp;
in vec2 v_uv;
out vec4 out_color;

{GLSL_MASK}

float hash(vec2 p) {{
    p = fract(p * vec2(127.1, 311.7));
    p += dot(p, p + 19.19);
    return fract(p.x * p.y);
}}

float noise(vec2 p) {{
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));
    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}}

float fbm(vec2 p) {{
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    for (int i = 0; i < u_octaves; i++) {{
        value += amplitude * noise(p * frequency);
        frequency *= u_lacunarity;
        amplitude *= u_gain;
    }}
    return value;
}}

void main() {{
    vec4 orig = texture(u_texture, v_uv);
    float mask = compute_mask();
    float t = u_time;

    // ---- Orbite de Lissajous ----
    float w1 = t * 0.038 * u_warp;
    vec2 orbit1 = vec2(cos(w1), sin(w1 * 0.618)) * 0.28;

    float w2 = t * 0.025 * u_warp;
    vec2 orbit2 = vec2(cos(w2 * 0.618), sin(w2) ) * 0.22;

    // UV de base : dérive de vent + orbite continue
    vec2 ndc = v_uv * 2.0 - 1.0;
    vec4 world = u_inv_mvp * vec4(ndc, 0.0, 1.0);
    vec2 base_uv = (world.xy / world.w) / u_scale;

    vec2 uv1 = base_uv + u_wind * t + orbit1;
    vec2 uv2 = base_uv * 0.74 + u_wind * t * 0.58 + vec2(3.7, 1.9) + orbit2;

    float f1 = fbm(uv1);
    float f2 = fbm(uv2);
    float fog = (f1 + f2) * 0.5;

    float dynamic = smoothstep(u_density, u_density + max(u_softness, 0.001), fog);
    float alpha = u_base + (1.0 - u_base) * dynamic;

    vec3 fogged = mix(orig.rgb, u_color, alpha);
    out_color = vec4(mix(orig.rgb, fogged, mask), orig.a);
}}
"""

# ======================================== EFFECT ========================================
@dataclass(slots=True, frozen=True)
class Fog(PostFxEffect):
    """Effet post-processing: brouillard procédural animé

    Args:
        angle: angle du vent en degrés *(0 = droite)*
        velocity: vitesse de dérive globale
        base: épaisseur minimale garantie partout *[0, 1]*
        density: seuil des épaississements dynamiques *[0, 1]*
        softness: largeur du fondu des variations *(>= 0)*
        scale: zoom du bruit *(> 0)* — plus bas = structures plus larges
        warp: vitesse d'orbite *(> 0)* — contrôle l'intensité de déformation
        octaves: octaves fBm *[1, 8]*
        lacunarity: facteur de fréquence entre octaves *(> 1)*
        gain: facteur d'amplitude entre octaves *]0, 1[*
        color: couleur RGB du brouillard
    """
    angle: Real = 0.0
    velocity: Real = 1
    base: Real = 0.25
    density: Real = 0.4
    softness: Real = 0.5
    scale: Real = 10
    warp: Real = 1.0
    octaves: Integral = 4
    lacunarity: Real = 2.0
    gain: Real = 0.5
    color: Color = (1.0, 1.0, 1.0)

    _ID: ClassVar[str] = "fog"

    def __post_init__(self) -> None:
        object.__setattr__(self, "angle", float(self.angle))
        object.__setattr__(self, "velocity", float(self.velocity))
        object.__setattr__(self, "base", float(self.base))
        object.__setattr__(self, "density", float(self.density))
        object.__setattr__(self, "softness", float(self.softness))
        object.__setattr__(self, "scale", float(self.scale))
        object.__setattr__(self, "warp", float(self.warp))
        object.__setattr__(self, "octaves", int(self.octaves))
        object.__setattr__(self, "lacunarity", float(self.lacunarity))
        object.__setattr__(self, "gain", float(self.gain))
        object.__setattr__(self, "color", Color(self.color))

        if __debug__:
            clamped(self.base)
            clamped(self.density)
            positive(self.softness)
            over(self.scale, 0, include=False)
            over(self.warp, 0, include=False)
            over(self.octaves, 1, include=True)
            over(self.lacunarity, 1.0, include=False)
            clamped(self.gain, include_min=False, include_max=False)

# ======================================== RENDERER ========================================
class FogPostFxRenderer(SpecializedPostFxRenderer):
    """Renderer spécialisé pour l'effet ``Fog``"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[type[PostFxEffect]]] = frozenset({Fog})
    _REQUIRES_TIME: ClassVar[bool] = True
    _program: ClassVar[ShaderProgram | None] = None
    _time: ClassVar[float] = 0.0

    @classmethod
    def _get_program(cls) -> ShaderProgram:
        """Renvoie le programme de shader associé"""
        if cls._program is None:
            cls._program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG, 'fragment'))
        return cls._program

    @classmethod
    def clear_shader_cache(cls) -> None:
        """Nettoie le cache du programme de shader"""
        cls._program = None

    def apply(self, pipeline: Pipeline, effect: Fog, mask: MaskData) -> None:
        """Applique le brouillard procédural

        Args:
            pipeline: ``Pipeline`` de rendu courant
            effect: paramètres du brouillard
            mask: données de masque spatial
        """
        theta = math.radians(effect.angle)
        wind = (
            -math.cos(theta) * effect.velocity,
            -math.sin(theta) * effect.velocity,
        )
        density = 1 - effect.density

        pipeline.apply_shader(
            self._get_program(),
            u_wind=wind,
            u_time=self._time,
            u_base=effect.base,
            u_density=density,
            u_softness=effect.softness,
            u_scale=effect.scale,
            u_warp=effect.warp,
            u_octaves=effect.octaves,
            u_lacunarity=effect.lacunarity,
            u_gain=effect.gain,
            u_color=effect.color.rgb,
            u_inv_mvp=pipeline.inv_full_matrix,
            **mask.as_uniforms(),
        )

# ======================================== EXPORTS ========================================
__all__ = [
    "Fog",
    "FogPostFxRenderer",
]