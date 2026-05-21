# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import over
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
uniform vec2 u_block;
in vec2 v_uv;
out vec4 out_color;

{GLSL_MASK}

void main() {{
    vec2 snapped = floor(v_uv / u_block) * u_block + u_block * 0.5;
    vec4 pixelated = texture(u_texture, snapped);
    vec4 original = texture(u_texture, v_uv);
    float mask = compute_mask();
    out_color = mix(original, pixelated, mask);
}}
"""

# ======================================== EFFECT ========================================
@dataclass(slots=True, frozen=True)
class Pixelate(PostFxEffect):
    """Effet post-processing: pixelisation

    Args:
        block_size: taille d'un bloc en pixels *(> 0)*
    """
    block_size: Real = 8.0

    _ID: ClassVar[str] = "pixelate"

    def __post_init__(self) -> None:
        object.__setattr__(self, "block_size", float(self.block_size))
        if __debug__:
            over(self.block_size, 0, include=False)

# ======================================== RENDERER ========================================
class PixelatePostFxRenderer(SpecializedPostFxRenderer):
    """Renderer spécialisé pour l'effet ``Pixelate``"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[type[PostFxEffect]]] = frozenset({Pixelate})

    _program: ClassVar[ShaderProgram | None] = None

    @classmethod
    def _get_program(cls) -> ShaderProgram:
        """Retourne *(en le créant si nécessaire)* le shader de pixelisation"""
        if cls._program is None:
            cls._program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG, 'fragment'))
        return cls._program

    @classmethod
    def clear_shader_cache(cls) -> None:
        """Libère le ``ShaderProgram`` mis en cache"""
        cls._program = None

    def apply(self, pipeline: Pipeline, effect: Pixelate, mask: MaskData) -> None:
        """Applique la pixelisation

        Args:
            pipeline: ``Pipeline`` de rendu courant
            effect: paramètres de la pixelisation
            mask: données de masque spatial
        """
        fbo = pipeline.fbo
        bx = effect.block_size / fbo.width
        by = effect.block_size / fbo.height

        pipeline.apply_shader(
            self._get_program(),
            u_block=(bx, by),
            **mask.as_uniforms(),
        )

# ======================================== EXPORTS ========================================
__all__ = [
    "Pixelate",
    "PixelatePostFxRenderer",
]