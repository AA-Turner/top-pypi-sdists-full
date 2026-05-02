# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._rendering import Pipeline
from ._point import PointLight
from ._cone import ConeLight

import ctypes
import math
import pyglet.gl as gl
from pyglet.graphics.shader import Shader, ShaderProgram

# ======================================== CONSTANTS ========================================
_BUCKETS = (8, 16, 32, 64, 128)
_LUT_SIZE = 256

# ======================================== BUCKET SYSTEM ========================================
def _get_bucket(count: int) -> int:
    """Retourne la taille de bucket GLSL la plus proche supérieure ou égale à count

    Args:
        count: Nombre de lumières actives
    """
    for bucket in _BUCKETS:
        if count <= bucket:
            return bucket
    return count

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

_FRAG_AMBIENT = """
#version 330 core
uniform sampler2D u_texture;
uniform float u_ambient;
uniform vec3 u_ambient_color;
uniform float u_gamma;
in vec2 v_uv;
out vec4 out_color;
void main() {
    vec4 pixel = texture(u_texture, v_uv);
    vec3 light = u_ambient_color * u_ambient;
    light = pow(max(light, vec3(0.0)), vec3(1.0 / u_gamma));
    out_color = vec4(pixel.rgb * light, pixel.a);
}
"""

_FRAG_TINT = """
#version 330 core
uniform sampler2D u_texture;
uniform vec3 u_tint;
uniform float u_strength;
in vec2 v_uv;
out vec4 out_color;
void main() {
    vec4 pixel = texture(u_texture, v_uv);
    out_color = vec4(mix(pixel.rgb, pixel.rgb * u_tint, u_strength), pixel.a);
}
"""

_FRAG_VIGNETTE = """
#version 330 core
uniform sampler2D u_texture;
uniform float u_strength;
uniform float u_radius;
uniform vec3 u_color;
in vec2 v_uv;
out vec4 out_color;
void main() {
    vec4 pixel = texture(u_texture, v_uv);
    float d = length(v_uv - vec2(0.5)) / u_radius;
    float t = smoothstep(0.0, 1.0, d * d * d);
    float vignette = 1.0 - u_strength * t;
    out_color = vec4(mix(pixel.rgb * vignette, pixel.rgb * u_color, u_strength * t), pixel.a);
}
"""

_GLSL_TONEMAP = """
vec3 tonemap(vec3 ambient, vec3 light_accum, float exposure) {
    vec3 total = ambient + light_accum * exposure;
    float lum = dot(total, vec3(0.2126, 0.7152, 0.0722));
    float lum_tm = lum / (1.0 + lum);
    return total * (lum_tm / max(lum, 0.0001));
}
"""


def _build_frag_points(max_lights: int) -> str:
    """Génère le fragment shader GLSL pour un rendu de lumières ponctuelles uniquement.

    Accumulation additive des contributions. u_exposure ne scale que les lumières
    dynamiques — l'ambient reste indépendant. Tonemapping Reinhard sur la luminance
    perceptuelle pour préserver la teinte. Correction gamma en sortie.

    Args:
        max_lights: Taille du tableau GLSL (doit correspondre au bucket actif).

    Returns:
        Le source GLSL du fragment shader sous forme de chaîne.
    """
    return f"""
#version 330 core
uniform sampler2D u_texture;
uniform float u_ambient;
uniform vec3 u_ambient_color;
uniform float u_exposure;
uniform float u_gamma;
uniform int u_count;
uniform vec2 u_positions[{max_lights}];
uniform float u_radii[{max_lights}];
uniform vec3 u_colors[{max_lights}];
uniform float u_intensities[{max_lights}];
uniform sampler2D u_lut;

in vec2 v_uv;
out vec4 out_color;

{_GLSL_TONEMAP}

void main() {{
    vec4 pixel = texture(u_texture, v_uv);
    vec2 frag = gl_FragCoord.xy;
    vec3 light_accum = vec3(0.0);

    for (int i = 0; i < u_count; i++) {{
        float dist = distance(frag, u_positions[i]);
        float normalized = clamp(dist / u_radii[i], 0.0, 1.0);
        float row = (float(i) + 0.5) / float({max_lights});
        float falloff = texture(u_lut, vec2(1.0 - normalized, row)).r;
        light_accum += u_colors[i] * u_intensities[i] * falloff;
    }}

    vec3 light = tonemap(u_ambient_color * u_ambient, light_accum, u_exposure);
    light = pow(max(light, vec3(0.0)), vec3(1.0 / u_gamma));
    out_color = vec4(pixel.rgb * light, pixel.a);
}}
"""


def _build_frag_cones(max_lights: int) -> str:
    """Génère le fragment shader GLSL pour un rendu de lumières coniques uniquement.

    Combine falloff radial (via LUT atlas) et falloff angulaire (smoothstep entre
    inner/outer angle). Accumulation additive, tonemapping Reinhard sur luminance,
    correction gamma en sortie.

    Args:
        max_lights: Taille du tableau GLSL (doit correspondre au bucket actif).

    Returns:
        Le source GLSL du fragment shader sous forme de chaîne.
    """
    return f"""
#version 330 core
uniform sampler2D u_texture;
uniform float u_ambient;
uniform vec3 u_ambient_color;
uniform float u_exposure;
uniform float u_gamma;
uniform int u_count;
uniform vec2 u_positions[{max_lights}];
uniform vec2 u_directions[{max_lights}];
uniform float u_radii[{max_lights}];
uniform float u_inner_angles[{max_lights}];
uniform float u_outer_angles[{max_lights}];
uniform vec3 u_colors[{max_lights}];
uniform float u_intensities[{max_lights}];
uniform sampler2D u_lut;

in vec2 v_uv;
out vec4 out_color;

{_GLSL_TONEMAP}

void main() {{
    vec4 pixel = texture(u_texture, v_uv);
    vec2 frag = gl_FragCoord.xy;
    vec3 light_accum = vec3(0.0);

    for (int i = 0; i < u_count; i++) {{
        vec2 to_frag = frag - u_positions[i];
        float dist = length(to_frag);

        float row = (float(i) + 0.5) / float({max_lights});
        float radial_falloff;

        if (u_radii[i] <= 0.0001) {{
            radial_falloff = 1.0;
        }} else {{
            float t = clamp(dist / u_radii[i], 0.0, 1.0);
            radial_falloff = texture(u_lut, vec2(1.0 - t, row)).r;
        }}

        vec2 dir = (dist > 0.0001) ? to_frag / dist : vec2(0.0);
        float cos_angle = dot(dir, u_directions[i]);
        float cos_inner = cos(u_inner_angles[i]);
        float cos_outer = cos(u_outer_angles[i]);

        float angular_falloff = smoothstep(cos_outer, cos_inner, cos_angle);

        light_accum += u_colors[i] * u_intensities[i] * radial_falloff * angular_falloff;
    }}

    vec3 light = tonemap(u_ambient_color * u_ambient, light_accum, u_exposure);
    light = pow(max(light, vec3(0.0)), vec3(1.0 / u_gamma));
    out_color = vec4(pixel.rgb * light, pixel.a);
}}
"""


def _build_frag_points_cones(max_points: int, max_cones: int) -> str:
    """Génère le fragment shader GLSL pour un rendu mixte points + cônes.

    Chaque type de lumière dispose de son propre LUT atlas (u_point_lut sur TEXTURE1,
    u_cone_lut sur TEXTURE2). Les deux contributions sont accumulées additivement dans
    un accumulateur commun avant le tonemapping Reinhard sur la luminance et la
    correction gamma.

    Args:
        max_points: Taille du tableau GLSL pour les point lights (bucket actif).
        max_cones:  Taille du tableau GLSL pour les cone lights (bucket actif).

    Returns:
        Le source GLSL du fragment shader sous forme de chaîne.
    """
    return f"""
#version 330 core
uniform sampler2D u_texture;
uniform float u_ambient;
uniform vec3 u_ambient_color;
uniform float u_exposure;
uniform float u_gamma;

uniform int u_point_count;
uniform vec2 u_point_positions[{max_points}];
uniform float u_point_radii[{max_points}];
uniform vec3 u_point_colors[{max_points}];
uniform float u_point_intensities[{max_points}];
uniform sampler2D u_point_lut;

uniform int u_cone_count;
uniform vec2 u_cone_positions[{max_cones}];
uniform vec2 u_cone_directions[{max_cones}];
uniform float u_cone_radii[{max_cones}];
uniform float u_cone_inner_angles[{max_cones}];
uniform float u_cone_outer_angles[{max_cones}];
uniform vec3 u_cone_colors[{max_cones}];
uniform float u_cone_intensities[{max_cones}];
uniform sampler2D u_cone_lut;

in vec2 v_uv;
out vec4 out_color;

{_GLSL_TONEMAP}

void main() {{
    vec4 pixel = texture(u_texture, v_uv);
    vec2 frag = gl_FragCoord.xy;
    vec3 light_accum = vec3(0.0);

    for (int i = 0; i < u_point_count; i++) {{
        float dist = distance(frag, u_point_positions[i]);
        float normalized = clamp(dist / u_point_radii[i], 0.0, 1.0);
        float row = (float(i) + 0.5) / float({max_points});
        float falloff = texture(u_point_lut, vec2(1.0 - normalized, row)).r;
        light_accum += u_point_colors[i] * u_point_intensities[i] * falloff;
    }}

    for (int i = 0; i < u_cone_count; i++) {{
        vec2 to_frag = frag - u_cone_positions[i];
        float dist = length(to_frag);
        float row = (float(i) + 0.5) / float({max_cones});
        float radial_falloff;

        if (u_cone_radii[i] <= 0.0001) {{
            radial_falloff = 1.0;
        }} else {{
            float t = clamp(dist / u_cone_radii[i], 0.0, 1.0);
            radial_falloff = texture(u_cone_lut, vec2(1.0 - t, row)).r;
        }}

        vec2 dir = (dist > 0.0001) ? to_frag / dist : vec2(0.0);
        float cos_angle = dot(dir, u_cone_directions[i]);
        float cos_inner = cos(u_cone_inner_angles[i]);
        float cos_outer = cos(u_cone_outer_angles[i]);

        float angular_falloff = smoothstep(cos_outer, cos_inner, cos_angle);

        light_accum += u_cone_colors[i] * u_cone_intensities[i] * radial_falloff * angular_falloff;
    }}

    vec3 light = tonemap(u_ambient_color * u_ambient, light_accum, u_exposure);
    light = pow(max(light, vec3(0.0)), vec3(1.0 / u_gamma));
    out_color = vec4(pixel.rgb * light, pixel.a);
}}
"""

# ======================================== RENDERER ========================================
class LightRenderer:
    """Renderer de lumière 2D"""

    __slots__ = ("_active_points", "_active_cones")

    _tint_program: ShaderProgram = None
    _ambient_only_program: ShaderProgram = None
    _vignette_program: ShaderProgram = None
    _point_programs: dict[int, ShaderProgram] = {}
    _cone_programs: dict[int, ShaderProgram] = {}
    _point_cone_programs: dict[tuple[int, int], ShaderProgram] = {}

    _lut_cache: dict[tuple, gl.GLuint] = {}

    _vec2_pool:  dict[tuple[int, int], list] = {}
    _vec3_pool:  dict[tuple[int, int], list] = {}
    _float_pool: dict[tuple[int, int], list] = {}

    def __init__(self):
        self._active_points: list[PointLight] = []
        self._active_cones: list[ConeLight] = []

    # ======================================== SHADER CACHE ========================================
    @classmethod
    def _get_tint_program(cls) -> ShaderProgram:
        """Retourne (en le créant si nécessaire) le shader de tint coloré."""
        if cls._tint_program is None:
            cls._tint_program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG_TINT, 'fragment'))
        return cls._tint_program

    @classmethod
    def _get_ambient_only_program(cls) -> ShaderProgram:
        """Retourne (en le créant si nécessaire) le shader d'ambient seul"""
        if cls._ambient_only_program is None:
            cls._ambient_only_program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG_AMBIENT, 'fragment'))
        return cls._ambient_only_program

    @classmethod
    def _get_vignette_program(cls) -> ShaderProgram:
        """Retourne (en le créant si nécessaire) le shader de vignette"""
        if cls._vignette_program is None:
            cls._vignette_program = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_FRAG_VIGNETTE, 'fragment'))
        return cls._vignette_program

    @classmethod
    def _get_point_program(cls, max_lights: int) -> ShaderProgram:
        """Retourne (en le créant si nécessaire) le shader de point lights pour un bucket donné

        Args:
            max_lights: Taille du bucket GLSL (tableau de lumières dans le shader)
        """
        if max_lights not in cls._point_programs:
            cls._point_programs[max_lights] = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_build_frag_points(max_lights), 'fragment'))
        return cls._point_programs[max_lights]

    @classmethod
    def _get_cone_program(cls, max_lights: int) -> ShaderProgram:
        """Retourne (en le créant si nécessaire) le shader de cone lights pour un bucket donné

        Args:
            max_lights: Taille du bucket GLSL (tableau de lumières dans le shader)
        """
        if max_lights not in cls._cone_programs:
            cls._cone_programs[max_lights] = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_build_frag_cones(max_lights), 'fragment'))
        return cls._cone_programs[max_lights]

    @classmethod
    def _get_point_cone_program(cls, max_points: int, max_cones: int) -> ShaderProgram:
        """Retourne (en le créant si nécessaire) le shader mixte points + cônes

        Args:
            max_points: Taille du bucket GLSL pour les point lights
            max_cones: Taille du bucket GLSL pour les cone lights
        """
        key = (max_points, max_cones)
        if key not in cls._point_cone_programs:
            cls._point_cone_programs[key] = ShaderProgram(Shader(_VERT, 'vertex'), Shader(_build_frag_points_cones(max_points, max_cones), 'fragment'))
        return cls._point_cone_programs[key]

    @classmethod
    def clear_shader_cache(cls) -> None:
        """Libère tous les ShaderPrograms et textures LUT mis en cache.

        À appeler lors d'un changement de contexte OpenGL ou d'un hot-reload.
        """
        cls._tint_program = None
        cls._ambient_only_program = None
        cls._vignette_program = None
        cls._point_programs.clear()
        cls._cone_programs.clear()
        cls._point_cone_programs.clear()
        for tex in cls._lut_cache.values():
            gl.glDeleteTextures(1, ctypes.byref(tex))
        cls._lut_cache.clear()

    # ======================================== BUFFER POOLS ========================================
    @classmethod
    def _vec2(cls, bucket: int, slot: int) -> list:
        """Retourne (en le créant si nécessaire) une liste pré-allouée de bucket tuples (x, y)

        Args:
            bucket: nombre d'entrées (nombre de lumières dans le bucket)
            slot: indice de slot pour éviter les collisions entre buffers de même taille
        """
        key = (bucket, slot)
        if key not in cls._vec2_pool:
            cls._vec2_pool[key] = [(0.0, 0.0)] * bucket
        return cls._vec2_pool[key]

    @classmethod
    def _vec3(cls, bucket: int, slot: int) -> list:
        """Retourne (en le créant si nécessaire) une liste pré-allouée de bucket tuples (x, y, z)

        Args:
            bucket: nombre d'entrées (nombre de lumières dans le bucket)
            slot: indice de slot pour éviter les collisions entre buffers de même taille
        """
        key = (bucket, slot)
        if key not in cls._vec3_pool:
            cls._vec3_pool[key] = [(0.0, 0.0, 0.0)] * bucket
        return cls._vec3_pool[key]

    @classmethod
    def _floats(cls, bucket: int, slot: int) -> list:
        """Retourne (en le créant si nécessaire) une liste pré-allouée de bucket floats

        Args:
            bucket: nombre d'entrées (nombre de lumières dans le bucket)
            slot: indice de slot pour éviter les collisions entre buffers de même taille
        """
        key = (bucket, slot)
        if key not in cls._float_pool:
            cls._float_pool[key] = [0.0] * bucket
        return cls._float_pool[key]

    # ======================================== LUT ATLAS ========================================
    @staticmethod
    def _lut_key(lights: list, bucket: int) -> tuple:
        """Calcule la clé de cache pour un LUT atlas.
    
        Args:
            lights: Liste de lumières dont construire la clé
            bucket: Taille du bucket (nombre de lignes de la texture)
        """
        return (bucket, tuple((id(light), id(light.falloff)) for light in lights))

    @classmethod
    def _get_lut_atlas(cls, lights: list, bucket: int) -> gl.GLuint:
        """Retourne le LUT atlas pour les lumières données, en le (re)construisant si nécessaire

        Args:
            lights: Liste de lumières dont extraire le falloff
            bucket: Nombre de lignes de la texture
        """
        key = cls._lut_key(lights, bucket)
        if key in cls._lut_cache:
            return cls._lut_cache[key]

        atlas = (ctypes.c_float * (_LUT_SIZE * bucket))()
        for i, light in enumerate(lights):
            for j in range(_LUT_SIZE):
                t = j / (_LUT_SIZE - 1)
                atlas[i * _LUT_SIZE + j] = (1.0 - t) if light.falloff is None else light.falloff(t)

        tex = gl.GLuint()
        gl.glGenTextures(1, ctypes.byref(tex))
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_R32F, _LUT_SIZE, bucket, 0, gl.GL_RED, gl.GL_FLOAT, atlas)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

        cls._lut_cache[key] = tex
        return tex

    # ======================================== RENDER AMBIENT ========================================
    def render_ambient(
        self,
        pipeline: Pipeline,
        ambient: float,
        exposure: float,
        points: list[PointLight],
        cones: list[ConeLight],
        *,
        ambient_color: tuple[float, float, float] = (1.0, 1.0, 1.0),
        gamma: float = 1.0,
    ) -> None:
        """Point d'entrée principal du rendu de lumière pour une frame
    
        Args:
            pipeline: Pipeline de rendu courant
            ambient: Niveau de lumière ambiante globale [0.0, 1.0]
            exposure: Facteur d'exposition appliqué uniquement aux lumières dynamiques
            points: Liste des point lights actives pour cette frame
            cones: Liste des cone lights actives pour cette frame
            ambient_color: Teinte de l'ambient en RGB normalisé
            gamma: Exposant de correction gamma appliqué en sortie du tonemapping
        """
        has_points = bool(points)
        has_cones = bool(cones)

        if not has_points and not has_cones:
            if ambient < 1.0 or ambient_color != (1.0, 1.0, 1.0) or gamma != 1.0:
                pipeline.apply_shader(
                    self._get_ambient_only_program(),
                    u_ambient=ambient,
                    u_ambient_color=ambient_color,
                    u_gamma=gamma,
                )
            return

        if has_points and has_cones:
            self._render_points_cones(pipeline, ambient, exposure, points, cones, ambient_color=ambient_color, gamma=gamma)
        elif has_points:
            self._render_points(pipeline, ambient, exposure, points, ambient_color=ambient_color, gamma=gamma)
        else:
            self._render_cones(pipeline, ambient, exposure, cones, ambient_color=ambient_color, gamma=gamma)

    # ======================================== POINTS ONLY ========================================
    def _render_points(
        self,
        pipeline: Pipeline,
        ambient: float,
        exposure: float,
        points: list[PointLight],
        *,
        ambient_color: tuple[float, float, float],
        gamma: float,
    ) -> None:
        """Effectue le rendu des point lights seules via leur shader dédié.

        Args:
            pipeline: Pipeline de rendu courant
            ambient: Niveau de lumière ambiante globale [0.0, 1.0]
            exposure: Exposition pour les lumières dynamiques uniquement
            points: Liste des point lights à rendre
            ambient_color: Teinte RGB de l'ambient
            gamma: Correction gamma de sortie
        """
        bucket   = _get_bucket(len(points))
        program  = self._get_point_program(bucket)

        pos_buf = self._vec2(bucket, 0)
        col_buf = self._vec3(bucket, 0)
        rad_buf = self._floats(bucket, 0)
        int_buf = self._floats(bucket, 1)

        for i, light in enumerate(points):
            fx, fy = pipeline.world_to_framebuffer(light.x, light.y)
            pos_buf[i] = (fx, fy)
            col_buf[i] = light.color.rgb
            rad_buf[i] = pipeline.scale_to_framebuffer(light.radius)
            int_buf[i] = light.intensity

        atlas_tex = self._get_lut_atlas(points, bucket)
        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, atlas_tex)

        pipeline.apply_shader(program,
            u_ambient=ambient,
            u_ambient_color=ambient_color,
            u_exposure=exposure,
            u_gamma=gamma,
            u_count=len(points),
            u_positions=pos_buf,
            u_radii=rad_buf,
            u_colors=col_buf,
            u_intensities=int_buf,
            u_lut=1,
        )

    # ======================================== CONES ONLY ========================================
    def _render_cones(
        self,
        pipeline: Pipeline,
        ambient: float,
        exposure: float,
        cones: list[ConeLight],
        *,
        ambient_color: tuple[float, float, float],
        gamma: float,
    ) -> None:
        """Effectue le rendu des cone lights seules via leur shader dédié

        Args:
            pipeline: Pipeline de rendu courant
            ambient: Niveau de lumière ambiante globale [0.0, 1.0]
            exposure: Exposition pour les lumières dynamiques uniquement
            cones: Liste des cone lights à rendre
            ambient_color: Teinte RGB de l'ambient
            gamma: Correction gamma de sortie
        """
        bucket   = _get_bucket(len(cones))
        program  = self._get_cone_program(bucket)

        pos_buf = self._vec2(bucket, 1)
        dir_buf = self._vec2(bucket, 2)
        col_buf = self._vec3(bucket, 1)
        rad_buf = self._floats(bucket, 2)
        int_buf = self._floats(bucket, 3)
        inn_buf = self._floats(bucket, 4)
        out_buf = self._floats(bucket, 5)

        for i, light in enumerate(cones):
            fx, fy   = pipeline.world_to_framebuffer(light.x, light.y)
            dfx, dfy = pipeline.world_to_framebuffer(light.direction.x, light.direction.y, vector=True)
            norm = (dfx**2 + dfy**2)**0.5
            if norm != 0.0:
                dfx /= norm
                dfy /= norm
            pos_buf[i] = (fx, fy)
            dir_buf[i] = (dfx, dfy)
            col_buf[i] = light.color.rgb
            rad_buf[i] = pipeline.scale_to_framebuffer(light.radius)
            int_buf[i] = light.intensity
            inn_buf[i] = math.radians(light.get_inner_angle())
            out_buf[i] = math.radians(light.get_outer_angle())

        atlas_tex = self._get_lut_atlas(cones, bucket)
        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, atlas_tex)

        pipeline.apply_shader(program,
            u_ambient=ambient,
            u_ambient_color=ambient_color,
            u_exposure=exposure,
            u_gamma=gamma,
            u_count=len(cones),
            u_positions=pos_buf,
            u_directions=dir_buf,
            u_radii=rad_buf,
            u_inner_angles=inn_buf,
            u_outer_angles=out_buf,
            u_colors=col_buf,
            u_intensities=int_buf,
            u_lut=1,
        )

    # ======================================== POINTS + CONES ========================================
    def _render_points_cones(
        self,
        pipeline: Pipeline,
        ambient: float,
        exposure: float,
        points: list[PointLight],
        cones: list[ConeLight],
        *,
        ambient_color: tuple[float, float, float],
        gamma: float,
    ) -> None:
        """Effectue le rendu mixte point lights + cone lights

        Args:
            pipeline: Pipeline de rendu courant
            ambient: Niveau de lumière ambiante globale [0.0, 1.0]
            exposure: Exposition pour les lumières dynamiques uniquement
            points: Liste des point lights à rendre
            cones: Liste des cone lights à rendre
            ambient_color: Teinte RGB de l'ambient
            gamma: Correction gamma de sortie
        """
        bp = _get_bucket(len(points))
        bc = _get_bucket(len(cones))
        program  = self._get_point_cone_program(bp, bc)

        p_pos = self._vec2(bp, 0)
        p_col = self._vec3(bp, 0)
        p_rad = self._floats(bp, 0)
        p_int = self._floats(bp, 1)

        for i, light in enumerate(points):
            fx, fy = pipeline.world_to_framebuffer(light.x, light.y)
            p_pos[i] = (fx, fy)
            p_col[i] = light.color.rgb
            p_rad[i] = pipeline.scale_to_framebuffer(light.radius)
            p_int[i] = light.intensity

        c_pos = self._vec2(bc, 1)
        c_dir = self._vec2(bc, 2)
        c_col = self._vec3(bc, 1)
        c_rad = self._floats(bc, 2)
        c_int = self._floats(bc, 3)
        c_inn = self._floats(bc, 4)
        c_out = self._floats(bc, 5)

        for i, light in enumerate(cones):
            fx, fy = pipeline.world_to_framebuffer(light.x, light.y)
            dfx, dfy = pipeline.world_to_framebuffer(light.direction.x, light.direction.y, vector=True)
            norm = (dfx**2 + dfy**2)**0.5
            if norm != 0.0:
                dfx /= norm
                dfy /= norm
            c_pos[i] = (fx, fy)
            c_dir[i] = (dfx, dfy)
            c_col[i] = light.color.rgb
            c_rad[i] = pipeline.scale_to_framebuffer(light.radius)
            c_int[i] = light.intensity
            c_inn[i] = math.radians(light.get_inner_angle())
            c_out[i] = math.radians(light.get_outer_angle())

        point_atlas = self._get_lut_atlas(points, bp)
        cone_atlas  = self._get_lut_atlas(cones, bc)

        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, point_atlas)
        gl.glActiveTexture(gl.GL_TEXTURE2)
        gl.glBindTexture(gl.GL_TEXTURE_2D, cone_atlas)

        pipeline.apply_shader(program,
            u_ambient=ambient,
            u_ambient_color=ambient_color,
            u_exposure=exposure,
            u_gamma=gamma,
            u_point_count=len(points),
            u_cone_count=len(cones),
            u_point_positions=p_pos,
            u_point_radii=p_rad,
            u_point_colors=p_col,
            u_point_intensities=p_int,
            u_cone_positions=c_pos,
            u_cone_directions=c_dir,
            u_cone_radii=c_rad,
            u_cone_inner_angles=c_inn,
            u_cone_outer_angles=c_out,
            u_cone_colors=c_col,
            u_cone_intensities=c_int,
            u_point_lut=1,
            u_cone_lut=2,
        )

    # ======================================== TINT ========================================
    def render_tint(
        self,
        pipeline: Pipeline,
        tint: tuple[float, float, float],
        strength: float,
    ) -> None:
        """Applique un tint coloré sur le framebuffer courant

        Args:
            pipeline: Pipeline de rendu courant
            tint: Couleur du tint en RGB normalisé
            strength: Intensité du tint [0.0 = aucun effet, 1.0 = tint total]
        """
        pipeline.apply_shader(self._get_tint_program(), u_tint=tint, u_strength=strength)

    # ======================================== VIGNETTE ========================================
    def render_vignette(
        self,
        pipeline: Pipeline,
        strength: float = 0.5,
        radius: float = 0.6,
        color: tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> None:
        """Applique une vignette sur le framebuffer courant

        Args:
            pipeline: Pipeline de rendu courant
            strength: Intensité de l'effet [0.0 = aucun effet, 1.0 = vignette totale]
            radius: Rayon de la zone centrale non affectée, en proportion de la diagonale
            color: Couleur de la vignette en RGB normalisé. (0, 0, 0) pour le noir
        """
        pipeline.apply_shader(
            self._get_vignette_program(),
            u_strength=strength,
            u_radius=radius,
            u_color=color,
        )