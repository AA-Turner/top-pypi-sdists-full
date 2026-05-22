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

import pyglet.gl as gl
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
uniform sampler2D u_previous;
uniform float u_strength;
in vec2 v_uv;
out vec4 out_color;

{GLSL_MASK}

void main() {{
    vec4 current = texture(u_texture, v_uv);
    vec4 previous = texture(u_previous, v_uv);
    float mask = compute_mask();
    vec3 blurred = mix(current.rgb, previous.rgb, u_strength);
    out_color = vec4(mix(current.rgb, blurred, mask), current.a);
}}
"""

# ======================================== EFFECT ========================================
@dataclass(slots=True, frozen=True)
class MotionBlur(PostFxEffect):
    """Effet post-processing: flou de mouvement par accumulation de frames

    Mélange la frame courante avec la frame précédente pour simuler une traînée temporelle.
    Plus ``strength`` est élevé, plus la traînée est longue.

    Args:
        strength: poids de la frame précédente *[0, 1[* - 0 = aucun blur, 0.9 = traînée longue
    """
    strength: Real = 0.5

    _ID: ClassVar[str] = "motion_blur"

    def __post_init__(self) -> None:
        object.__setattr__(self, "strength", float(self.strength))
        
        if __debug__:
            clamped(self.strength, include_max=False)

# ======================================== RENDERER ========================================
class MotionBlurPostFxRenderer(SpecializedPostFxRenderer):
    """Renderer spécialisé pour l'effet ``MotionBlur``"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[type[PostFxEffect]]] = frozenset({MotionBlur})
    _program: ClassVar[ShaderProgram | None] = None

    @classmethod
    def _get_program(cls) -> ShaderProgram:
        if cls._program is None:
            cls._program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG, 'fragment'))
        return cls._program

    @classmethod
    def clear_shader_cache(cls) -> None:
        cls._program = None

    def apply(self, pipeline: Pipeline, effect: MotionBlur, mask: MaskData) -> None:
        """Applique le flou de mouvement par accumulation temporelle

        Args:
            pipeline: ``Pipeline`` de rendu courant
            effect: paramètres du flou
            mask: données de masque spatial
        """
        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, pipeline.previous_fbo.texture_id)

        pipeline.apply_shader(
            self._get_program(),
            u_previous=1,
            u_strength=effect.strength,
            **mask.as_uniforms(),
        )

# ======================================== EXPORTS ========================================
__all__ = [
    "MotionBlur",
    "MotionBlurPostFxRenderer",
]