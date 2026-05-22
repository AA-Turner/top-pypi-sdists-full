# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import over
from ..._rendering import Pipeline
from ...abc import PostFxEffect

from ._specialized_renderer import SpecializedPostFxRenderer
from ._mask import MaskData, GLSL_MASK

from dataclasses import dataclass
from numbers import Integral
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
uniform float u_levels;
in vec2 v_uv;
out vec4 out_color;

{GLSL_MASK}

void main() {{
    vec4 orig = texture(u_texture, v_uv);
    float mask = compute_mask();
    vec3 posterized = floor(orig.rgb * u_levels) / u_levels;
    out_color = vec4(mix(orig.rgb, posterized, mask), orig.a);
}}
"""

# ======================================== EFFECT ========================================
@dataclass(slots=True, frozen=True)
class Posterize(PostFxEffect):
    """Effet post-processing: postérisation

    Réduit le nombre de niveaux de couleur par canal, produisant un rendu
    cartoon ou cel-shading.

    Args:
        levels: nombre de niveaux par canal *(>= 2)*
    """
    levels: Integral = 8

    _ID: ClassVar[str] = "posterize"

    def __post_init__(self) -> None:
        object.__setattr__(self, "levels", int(self.levels))
        
        if __debug__:
            over(self.levels, 2, include=True)

# ======================================== RENDERER ========================================
class PosterizePostFxRenderer(SpecializedPostFxRenderer):
    """Renderer spécialisé pour l'effet ``Posterize``"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[type[PostFxEffect]]] = frozenset({Posterize})
    _program: ClassVar[ShaderProgram | None] = None

    @classmethod
    def _get_program(cls) -> ShaderProgram:
        if cls._program is None:
            cls._program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG, 'fragment'))
        return cls._program

    @classmethod
    def clear_shader_cache(cls) -> None:
        cls._program = None

    def apply(self, pipeline: Pipeline, effect: Posterize, mask: MaskData) -> None:
        pipeline.apply_shader(
            self._get_program(),
            u_levels=float(effect.levels),
            **mask.as_uniforms(),
        )

# ======================================== EXPORTS ========================================
__all__ = [
    "Posterize",
    "PosterizePostFxRenderer",
]