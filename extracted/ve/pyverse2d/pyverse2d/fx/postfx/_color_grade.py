# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import clamped, over
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
uniform float u_brightness;
uniform float u_contrast;
uniform float u_saturation;
uniform vec3 u_tint;
in vec2 v_uv;
out vec4 out_color;

{GLSL_MASK}

vec3 apply_grade(vec3 color) {{
    // Brightness
    color = color + u_brightness;
    // Contrast
    color = (color - 0.5) * u_contrast + 0.5;
    // Saturation
    float lum = dot(color, vec3(0.2126, 0.7152, 0.0722));
    color = mix(vec3(lum), color, u_saturation);
    // Tint
    color = color * u_tint;
    return clamp(color, 0.0, 1.0);
}}

void main() {{
    vec4 orig = texture(u_texture, v_uv);
    float mask = compute_mask();
    vec3 graded = apply_grade(orig.rgb);
    out_color = vec4(mix(orig.rgb, graded, mask), orig.a);
}}
"""

# ======================================== EFFECT ========================================
@dataclass(slots=True, frozen=True)
class ColorGrade(PostFxEffect):
    """Effet post-processing: correction colorimétrique

    Args:
        brightness: décalage de luminosité *[-1, 1]* (0 = neutre)
        contrast: facteur de contraste *(>= 0)* (1 = neutre)
        saturation: facteur de saturation *(>= 0)* (1 = neutre, 0 = niveaux de gris)
        tint: teinte multiplicative RGB *(chaque composante >= 0)* ((1,1,1) = neutre)
    """
    brightness: Real = 0.0
    contrast: Real = 1.0
    saturation: Real = 1.0
    tint: Color = (1.0, 1.0, 1.0)

    _ID: ClassVar[str] = "color_grade"

    def __post_init__(self) -> None:
        object.__setattr__(self, "brightness", float(self.brightness))
        object.__setattr__(self, "contrast", float(self.contrast))
        object.__setattr__(self, "saturation", float(self.saturation))
        object.__setattr__(self, "tint", Color(self.tint))

        if __debug__:
            clamped(self.brightness, min=-1.0, max=1.0)
            over(self.contrast, 0, include=True)
            over(self.saturation, 0, include=True)

# ======================================== RENDERER ========================================
class ColorGradePostFxRenderer(SpecializedPostFxRenderer):
    """Renderer spécialisé pour l'effet ``ColorGrade``"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[type[PostFxEffect]]] = frozenset({ColorGrade})
    _program: ClassVar[ShaderProgram | None] = None

    @classmethod
    def _get_program(cls) -> ShaderProgram:
        if cls._program is None:
            cls._program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG, 'fragment'))
        return cls._program

    @classmethod
    def clear_shader_cache(cls) -> None:
        cls._program = None

    def apply(self, pipeline: Pipeline, effect: ColorGrade, mask: MaskData) -> None:
        pipeline.apply_shader(
            self._get_program(),
            u_brightness=effect.brightness,
            u_contrast=effect.contrast,
            u_saturation=effect.saturation,
            u_tint=effect.tint.rgb,
            **mask.as_uniforms(),
        )

# ======================================== EXPORTS ========================================
__all__ = [
    "ColorGrade",
    "ColorGradePostFxRenderer",
]