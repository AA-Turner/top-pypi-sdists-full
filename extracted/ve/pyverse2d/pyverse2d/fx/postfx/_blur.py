# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import over
from ..._rendering import Pipeline
from ...abc import PostFxEffect

from ._specialized_renderer import SpecializedPostFxRenderer
from ._mask import MaskData, GLSL_MASK

from pyglet.graphics.shader import Shader, ShaderProgram

from dataclasses import dataclass
from numbers import Real, Integral
from typing import ClassVar

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
uniform vec2 u_direction;
uniform vec2 u_texel;
uniform float u_radius;
in vec2 v_uv;
out vec4 out_color;

{GLSL_MASK}

void main() {{
    vec3 result = vec3(0.0);
    float total = 0.0;
    int steps = int(u_radius);
    vec2 step_uv = u_direction * u_texel;
    for (int i = -steps; i <= steps; i++) {{
        float t = float(i) / max(u_radius, 1.0);
        float w = exp(-t * t * 4.5);
        result += texture(u_texture, v_uv + step_uv * float(i)).rgb * w;
        total  += w;
    }}
    vec4 original = texture(u_texture, v_uv);
    float mask = compute_mask();
    out_color = vec4(mix(original.rgb, result / total, mask), original.a);
}}
"""

# ======================================== EFFECT ========================================
@dataclass(slots=True, frozen=True)
class Blur(PostFxEffect):
    """Effet post-processing: flou gaussien

    Args:
        radius: rayon du noyau en pixels *(> 0)*
        passes: nombre d'itérations du flou *(>= 1)*
    """
    radius: Real = 4.0
    passes: Integral = 1

    _ID: ClassVar[str] = "blur"

    def __post_init__(self) -> None:
        """Transtypage et vérifications"""
        object.__setattr__(self, "radius", float(self.radius))
        object.__setattr__(self, "passes", int(self.passes))

        if __debug__:
            over(self.radius, 0, include=False)
            over(self.passes, 1, include=True)

# ======================================== RENDERER ========================================
class BlurPostFxRenderer(SpecializedPostFxRenderer):
    """Renderer spécialisé pour l'effet ``Blur``"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[type[PostFxEffect]]] = frozenset({Blur})

    _program: ClassVar[ShaderProgram | None] = None

    @classmethod
    def _get_program(cls) -> ShaderProgram:
        """Retourne *(en le créant si nécessaire)* le shader de flou gaussien"""
        if cls._program is None:
            cls._program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG, 'fragment'))
        return cls._program

    @classmethod
    def clear_shader_cache(cls) -> None:
        """Libère le ``ShaderProgram`` mis en cache"""
        cls._program = None

    def apply(self, pipeline: Pipeline, effect: Blur, mask: MaskData) -> None:
        """Applique le flou gaussien séparable multi-passes

        Args:
            pipeline: ``Pipeline`` de rendu courant
            effect: paramètres du flou
            mask: données de masque spatial
        """
        fbo = pipeline.fbo
        texel = (1.0 / fbo.width, 1.0 / fbo.height)
        program = self._get_program()
        mask_uniforms = mask.as_uniforms()

        for _ in range(effect.passes):
            pipeline.apply_shader(program,
                u_direction=(1.0, 0.0),
                u_texel=texel,
                u_radius=effect.radius,
                **mask_uniforms,
            )
            pipeline.apply_shader(program,
                u_direction=(0.0, 1.0),
                u_texel=texel,
                u_radius=effect.radius,
                **mask_uniforms,
            )

# ======================================== EXPORTS ========================================
__all__ = [
    "Blur",
    "BlurPostFxRenderer",
]