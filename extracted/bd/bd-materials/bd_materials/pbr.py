"""Bridge from a finished material to a bundled three.js PBR material.

``get_pbr_properties(material, finish, process, color, thickness_mm, pbr)`` resolves
the right ``threejs_materials`` factory for how a part looks -- the function behind
the ``FinishedMaterial.pbr`` property (the user-facing entry, in ``finished``).

``finish`` is an ``AppliedFinish`` (from a finish function like
``spray_paint("blue")``) or a list of them; each carries its color. Finishes
split on two axes: **texture** (brushed / bead-blast -> metal relief variants)
and **surface/color** (anodize/PVD override; paint covers; plating replaces).
``process`` is an ``AppliedProcess`` (from a process function like ``fdm(rotation=90)``)
and nudges the default surface: FDM renders as printed layer lines, the powder-bed
routes as an as-built matte, everything else smooth. It carries that surface's own
texture geometry, the way a textured finish does. ``pbr`` (if given) is returned
unchanged.

Requires ``threejs_materials`` (kept out of ``bd_materials``'s core imports; only
this module and ``FinishedMaterial.pbr`` pull it in).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import webcolors
from threejs_materials import coats, glass, metal, paper, plastic, textile, wood

from . import finishes as fin
from .core import FERROUS, Color, RangeMaterial
from .finished import FinishSpec
from .finishes import AppliedFinish
from .processes import (
    AUTHORED_LAYER_HEIGHT_MM,
    AUTHORED_LINE_WIDTH_MM,
    AppliedProcess,
    Process,
)

if TYPE_CHECKING:  # real types for checkers; never imported at runtime (viz-free)
    from threejs_materials import PbrProperties

# The internal normalized color: what the bundled three.js factories accept -- a color
# name / "#rrggbb" hex string, or a 0..1 sRGB ``(r, g, b)`` tuple. ``_normalize_color``
# coerces any accepted ``Color`` input (see ``core.Color``) down to this.
_Rgb = str | tuple[float, float, float]

# as-printed / as-built routes and the relief each leaves behind. FDM is the one route
# with a surface of its own -- extruded layer lines; the powder-bed routes (SLS/MJF, and
# SLM for metal) sinter to an isotropic matte, the same relief a bead-blast leaves. The
# routes not listed (VAT, MOLDED, MACHINED, CAST, WROUGHT) stay smooth.
_PROCESS_TEXTURE = {
    Process.FDM: "fdm",
    Process.SLS: "matte",
    Process.MJF: "matte",
    Process.SLM: "matte",
}

# The two FDM reliefs and the printed pitch each bundled map is authored at. Both are
# millimetre-true (see ``_fdm_scale``), but they measure different things: the wall's
# beads are stacked, so its pitch is the layer height; the skin's sit side by side, so
# its pitch is the extrusion width.
_FDM_AUTHORED_PITCH = {
    "fdm": AUTHORED_LAYER_HEIGHT_MM,
    "fdm_skin": AUTHORED_LINE_WIDTH_MM,
}

# --- bd_materials-specific color names -> sRGB hex (None = no tint) -----------
# CSS3 named colors are NOT listed here: they are resolved by ``webcolors`` (the same
# resolver build123d + ocp-tessellate use), so a bare ``color="red"`` matches build123d's
# ``Color("red")`` exactly, and every CSS3 name works. Only what webcolors cannot express
# lives here: the no-tint sentinels (``natural`` / ``clear``), and the material-appearance
# names with no standard literal (gunmetal / nickel / chrome / rose gold / champagne). The
# "not-so-black for legibility" treatment is deliberately NOT here -- it is scoped to the
# dark *finishes* only (``_BLACK_OXIDE_GREY`` for black oxide, ``_ECOAT_CHARCOAL`` e-coat).
_COLOR_HEX: dict[str, str | None] = {
    "natural": None,  # no tint -- the factory / substrate look
    "clear": None,  # no tint
    "gunmetal": "#2a3439",
    "nickel": "#b8b8b0",
    "chrome": "#c8ccce",
    "rose gold": "#b76e79",
    "champagne": "#e6c99a",
}

# metal families with a dedicated bundled factory (else steel / stainless)
_BARE_METALS = frozenset(
    {
        "aluminum",
        "brass",
        "bronze",
        "copper",
        "stainless",
        "titanium",
        "tin",
        "gold",
        "silver",
    }
)

# mechanical finishes -> metal surface-relief variant (None elsewhere = smooth)
_MECH = fin.MECHANICAL_FINISHES
_TEXTURE = {
    _MECH[fin.Mechanical.BRUSHED]: "brushed",
    _MECH[fin.Mechanical.BEAD_BLAST]: "matte",
    _MECH[fin.Mechanical.FINE_SANDING]: "matte",
}


def _normalize_color(color: Color | None) -> _Rgb | None:
    """Coerce any accepted ``Color`` input to the internal ``_Rgb`` (hex string or RGB).

    Handles the same shapes as build123d's ``ColorLike`` (see ``core.Color``) -- a
    palette/CSS/hex name string, a packed ``0xRRGGBB`` int, a ``(name, alpha)`` pair, an
    ``(r, g, b[, a])`` iterable or a build123d ``Color`` (both ``Iterable[float]``), or a
    raw OCP ``Quantity_ColorRGBA`` (duck-typed via ``GetRGB`` so no OCP type is named or
    imported unless one is actually passed). Alpha is dropped -- transparency is the
    dedicated ``opacity`` / ``thickness_mm`` axes.

    A name string resolves in order: a bd_materials-specific name (``_COLOR_HEX`` -- the
    no-tint sentinels + material-appearance names), a ``#rrggbb`` hex (passed through),
    then any CSS3 name via ``webcolors`` (matching build123d's ``Color(name)``); an
    unrecognized name is passed through unchanged.

    Args:
        color: The color input, or ``None``.

    Returns:
        A resolved hex / pass-through name string, a ``(r, g, b)`` tuple, or ``None``.
    """
    if color is None:
        return None
    if isinstance(color, str):
        key = color.strip().lower()
        if key in _COLOR_HEX:  # sentinels (-> None) + material-appearance names
            return _COLOR_HEX[key]
        if key.startswith("#"):  # a hex literal passes through
            return color
        try:
            return webcolors.name_to_hex(key)  # CSS3 name -> literal (== Color(name))
        except ValueError:
            return color  # unrecognized name -- pass through
    if isinstance(color, bool):  # guard: bool is a subclass of int
        raise TypeError(f"invalid color: {color!r}")
    if isinstance(color, int):  # packed 0xRRGGBB
        return f"#{color & 0xFFFFFF:06x}"
    if isinstance(color, tuple) and len(color) == 2 and isinstance(color[0], str):
        return _normalize_color(color[0])  # (name, alpha) -- alpha dropped
    if hasattr(color, "GetRGB"):  # OCP Quantity_ColorRGBA, duck-typed
        return _rgb_from_ocp(color)
    seq = tuple(color)  # (0xRRGGBB, alpha) | (r, g, b[, a]) | build123d Color
    if len(seq) == 2 and isinstance(seq[0], int) and not isinstance(seq[0], bool):
        return f"#{seq[0] & 0xFFFFFF:06x}"  # (0xRRGGBB, alpha)
    ch = [float(v) for v in seq]  # rgb(a) channels; any alpha dropped below
    return (ch[0], ch[1], ch[2])


def _rgb_from_ocp(color: Any) -> tuple[float, float, float]:
    """0..1 sRGB from a duck-typed OCP ``Quantity_ColorRGBA`` (via ``GetRGB``).

    Kept as an ``Any``-typed helper so the OCP color -- which this package cannot name
    (build123d/OCP depend on us) -- is handled without a cast, and so ``OCP`` is imported
    only if a raw OCP color is actually passed.

    Args:
        color: An object exposing OCCT's ``GetRGB()`` (a ``Quantity_ColorRGBA``).

    Returns:
        The ``(r, g, b)`` sRGB triple in 0..1; alpha is ignored.
    """
    rgb = color.GetRGB()
    if hasattr(rgb, "Values"):
        from OCP.Quantity import Quantity_TypeOfColor  # lazy: only for OCP colors

        r, g, b = rgb.Values(Quantity_TypeOfColor.Quantity_TOC_sRGB)
    else:
        r, g, b = rgb.Red(), rgb.Green(), rgb.Blue()
    return (float(r), float(g), float(b))


def _metal_name(material: RangeMaterial) -> str:
    """The bundled metal-factory key for the material (a bare family, else steel/stainless)."""
    fam = material.family
    if fam in _BARE_METALS:
        return fam
    if fam in FERROUS:
        return "steel"
    return "stainless"  # last-resort fallback


def _is_carbon(material: RangeMaterial) -> bool:
    """Whether the material is the carbon-fiber (CFRP) family."""
    return material.family == "CFRP"


def _metal_tex_base(material: RangeMaterial, texture: str | None) -> PbrProperties:
    """Bare metal, optionally with a brushed/matte relief variant."""
    name = _metal_name(material)
    if texture in _FDM_AUTHORED_PITCH:
        # extruded filament surfaces; a metal has no such map (and the metal printed
        # route, SLM, is powder-bed anyway) -- fall back to the sintered matte
        texture = "matte"
    if texture is not None:
        return getattr(metal, f"{name}_{texture}")()
    return getattr(metal, name)()


def _apply_uv(
    base: PbrProperties, scale: tuple[float, float], rotation: float
) -> PbrProperties:
    """Apply the per-part texture UV transform, preserving any baked one.

    ``scale=(2, 2)`` makes the texture read twice as large; ``rotation`` turns it
    counterclockwise in degrees. Most bundled materials normalize their UVs to the
    part's bounding box, so the transform simply replaces theirs.

    A material that ships a **baked** transform instead (``normalize_uvs=False`` --
    ``plastic_fdm``, whose map is authored at a real millimetre tile so the printed
    layer pitch holds on a part of any size) must keep normalization **off**: the
    ``fixed=True`` default of ``PbrProperties.scale`` would hand the pitch back to the
    bounding box, so merely rotating a print would silently lose its 0.2 mm layers.
    For those, ``scale`` is already in the map's own authored units (see
    ``_fdm_scale``), not a multiplier.

    Args:
        base: The resolved look to transform.
        scale: The per-part UV scale ``(u, v)``.
        rotation: The per-part texture rotation in degrees (counterclockwise).

    Returns:
        A transformed copy of ``base``.
    """
    u, v = scale
    if base.normalize_uvs is False:
        return base.scale(u, v, rotation=rotation, fixed=False)
    return base.scale(u, v, rotation=rotation)


def _fdm_scale(
    base: PbrProperties,
    pitch_mm: float | None,
    texture: str,
    mm_per_uv: float = 1.0,
) -> tuple[float, float]:
    """The FDM map's tile scale for a printed pitch, in the map's own units.

    Each bundled FDM map is authored at a known printed pitch over a tile of some
    millimetre size, and carries that size baked in as its texture repeat. A part
    printed at a different pitch scales the tile by the same ratio -- half the pitch,
    half the tile -- which keeps the printed spacing true at any part size.

    The authored tile is read off the material rather than hardcoded, so a re-authored
    upstream map stays correct; only the pitch it was drawn at is fixed here.

    Args:
        base: The FDM look, carrying the baked transform.
        pitch_mm: The printed pitch in mm -- the layer height on a wall, the extrusion
            width on a skin -- or ``None`` for the authored one.
        texture: The relief key, ``"fdm"`` or ``"fdm_skin"``; selects which authored
            pitch ``pitch_mm`` is measured against.
        mm_per_uv: How many mm one UV unit spans on the face this is going onto. The
            baked tile is in millimetres but the map is sampled in raw parameter space,
            so a face whose parameter is not metric (a sphere's latitude, in radians)
            needs the tile divided by this to keep the spacing true.

    Returns:
        The ``(u, v)`` tile scale to pass to ``_apply_uv``.
    """
    repeat = base.texture_repeat
    if repeat is None:  # no baked transform (an older bundled map) -- leave it alone
        return (1.0, 1.0)
    tile_u = 1.0 / repeat[0] / mm_per_uv
    tile_v = 1.0 / repeat[1] / mm_per_uv
    if pitch_mm is None:
        return (tile_u, tile_v)
    ratio = pitch_mm / _FDM_AUTHORED_PITCH[texture]
    return (tile_u * ratio, tile_v * ratio)


def _apply_transmissive(
    base: PbrProperties, opacity: float | None, roughness: float | None
) -> PbrProperties:
    """Apply the per-part transmissive tweaks (opacity, roughness) to a clear look.

    Args:
        base: A transmissive ``PbrProperties`` (acrylic / glass).
        opacity: ``0.0`` (fully clear) to ``1.0`` (opaque), or ``None`` for no change.
            Maps to ``transmission = 1 - opacity`` -- an intermediate value reads as a
            translucent/milky part (the diffuse base color shows through in proportion).
        roughness: Surface roughness ``0.0`` (glossy) to ``1.0`` (matte/frosted), or
            ``None`` to keep the factory value. Independent of opacity: a molded part is
            glossy over a scattering interior, an etched pane is rough and translucent.

    Returns:
        The base, or a copy with the given values overridden.
    """
    overrides: dict[str, float] = {}
    if opacity is not None:
        overrides["transmission"] = 1.0 - opacity
    if roughness is not None:
        overrides["roughness"] = roughness
    if not overrides:
        return base
    return base.override(**overrides)


def _plain_base(
    material: RangeMaterial,
    texture: str | None,
    rgb: _Rgb | None,
    thickness: float | None,
    opacity: float | None = None,
    roughness: float | None = None,
) -> PbrProperties:
    """Look for a material with no covering color finish -- substrate + texture.

    Wood/paper/textile pick a bundled factory by ``family`` (the factory key),
    falling back to a generic factory for a family three.js doesn't bundle.

    Args:
        material: The material whose bare look to build.
        texture: A relief variant ("brushed" / "matte"), or ``None`` for smooth.
        rgb: The base color as hex / RGB, or ``None`` for the factory default.
        thickness: Pane thickness (mm) for transmissive materials (glass and anything
            flagged ``transparent``); ignored otherwise.
        opacity: How see-through the part is, ``0.0`` (clear) to ``1.0`` (opaque), for a
            ``transparent`` material; ``None`` keeps the intrinsic clear look. Ignored
            for non-transparent materials.
        roughness: Surface roughness ``0.0`` (glossy) to ``1.0`` (matte/frosted) for a
            ``transparent`` material; ``None`` keeps the factory value. Ignored for
            non-transparent materials.

    Returns:
        The resolved ``PbrProperties``.
    """
    cat = material.category
    fam = material.family if material.family is not None else ""
    if cat == "metal":
        return _metal_tex_base(material, texture)
    if cat == "wood":
        factory = getattr(wood, fam, None)
        return (factory if factory is not None else wood.oak)(color=rgb)
    if cat == "glass":
        return _apply_transmissive(
            glass.glass(color=rgb, thickness=thickness), opacity, roughness
        )
    if cat == "paper":
        factory = getattr(paper, fam, None)
        return (factory if factory is not None else paper.paper)(color=rgb)
    if cat == "textile":
        factory = getattr(textile, fam, None)
        return (factory if factory is not None else textile.fabric_weave)(color=rgb)
    # plastic / resin (composites stay in this branch)
    if material.transparent:
        # transmissive: refraction depends on pane thickness (three.js acrylic
        # approximates both PMMA and PC well enough); opacity dials it toward a
        # translucent/opaque part (a milky PC V-wheel rather than a clear pane) and
        # roughness tunes the surface gloss/frost.
        return _apply_transmissive(
            plastic.acrylic(color=rgb, thickness=thickness), opacity, roughness
        )
    if _is_carbon(material):
        return plastic.carbon_fiber(color=rgb)
    if texture == "fdm_skin":
        # the solid top/bottom surface: side-by-side infill beads at the extrusion width
        return plastic.plastic_fdm_skin(color=rgb)
    if texture == "fdm":
        # printed layer lines; the map is authored at a real-world scale (a 6.4 mm tile
        # of 0.2 mm layers) and carries its own millimetre-true UV transform -- see
        # ``_apply_uv``, which preserves it rather than renormalizing the UVs
        return plastic.plastic_fdm(color=rgb)
    if texture is not None:
        return plastic.plastic_rough(color=rgb)
    return plastic.plastic(color=rgb)


# Dark conversion / e-coat finishes render as a very dark neutral grey, not an
# optical-void black, so surface geometry stays legible in the viewer: black oxide
# reads as matte "tool black" (gun-blue), e-coat black as a deep charcoal. Both are
# nominal look values, tune to taste.
_BLACK_OXIDE_GREY = "#2a2a2a"
_ECOAT_CHARCOAL = "#2e2e2e"


# --- surface (color) finishes: (material, rgb, texture, sheen) -> PbrProperties ---
# All handlers share this signature; sheen (gloss/matte) is only used by the
# paint/coat handler, ignored by the rest.
def _anodized(
    m: RangeMaterial, rgb: _Rgb | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Anodized look: recolor, keeping any brushed/blasted relief."""
    if m.family == "aluminum" and texture is None:
        return metal.aluminum_anodized(color=rgb)  # tuned preset for the common case
    base = _metal_tex_base(m, texture)  # keep relief; scalar recolor
    if rgb is not None:
        return base.override(color=rgb, roughness=0.3)
    return base


def _pvd(
    m: RangeMaterial, rgb: _Rgb | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """PVD look: "clear" shows the substrate metal; a color becomes a metallic coat."""
    if rgb is None:
        return _metal_tex_base(m, texture)  # clear PVD: bright substrate metal
    if texture is not None:  # keep the brushed/blasted relief
        return _metal_tex_base(m, texture).override(color=rgb, roughness=0.15)
    return coats.metallic_coat_gloss(color=rgb)


def _black_oxide(
    m: RangeMaterial, rgb: _Rgb | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Black-oxide look: matte very-dark-grey (tool black), keeping relief or as a coat."""
    if texture is not None:  # keep the blasted/brushed relief
        return _metal_tex_base(m, texture).override(
            color=_BLACK_OXIDE_GREY, roughness=0.5
        )
    return coats.metallic_coat_matte(color=_BLACK_OXIDE_GREY)


def _dyeing(
    m: RangeMaterial, rgb: _Rgb | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Dyed look: aluminum behaves like anodize; polymers tint the base."""
    if m.family == "aluminum":
        return _anodized(m, rgb, texture, sheen)
    return _plain_base(m, texture, rgb, None)  # dyed polymer: base tinted by color


def _chrome(
    m: RangeMaterial, rgb: _Rgb | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Chrome-plated look."""
    return coats.chrome()


def _gold(
    m: RangeMaterial, rgb: _Rgb | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Gold-plated look."""
    return metal.gold()


def _silver(
    m: RangeMaterial, rgb: _Rgb | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Silver-plated look."""
    return metal.silver()


def _nickel(
    m: RangeMaterial, rgb: _Rgb | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Nickel-plated look."""
    return metal.nickel()


def _tin(
    m: RangeMaterial, rgb: _Rgb | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Tin-plated look (matte / satin)."""
    # matte tin is the solderability standard, so the matte factory, not plain tin
    return metal.tin_matte()


def _zinc(
    m: RangeMaterial, rgb: _Rgb | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Zinc-plated look (satin), optionally tinted."""
    base = metal.zinc_matte()  # zinc plating is satin, not the glossy plain zinc
    if rgb is not None:
        return base.override(color=rgb)
    return base


def _coat(
    m: RangeMaterial, rgb: _Rgb | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Painted / coated look in ``rgb``; gloss or matte per ``sheen``."""
    fn = coats.coat_matte if sheen == fin.Sheen.MATTE else coats.coat_gloss
    return fn(color=rgb)


def _ecoat(
    m: RangeMaterial, rgb: _Rgb | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Electrophoretic e-coat look, split by substrate. Deep charcoal for "black"
    (its default/common color), never pitch black; other colors pass through.

    On aluminum it is a thin semi-transparent electrophoretic lacquer over anodizing,
    so it reads as a tinted semi-gloss metallic with the metal grain showing through.
    On other metals (steel, ...) it is an opaque epoxy e-coat -- a covering satin film
    that hides the substrate texture.
    """
    if rgb is None or rgb == _normalize_color("black"):
        rgb = _ECOAT_CHARCOAL  # black (the default/common e-coat) -> deep charcoal
    if m.family == "aluminum":
        # semi-transparent: tint the metal base, keeping metalness + any relief
        return _metal_tex_base(m, texture).override(color=rgb, roughness=0.3)
    # opaque epoxy e-coat: a covering satin film (semi-gloss, not dead matte),
    # substrate texture hidden; roughness 0.4 is nominal
    return coats.coat_gloss(color=rgb).override(roughness=0.4)


_CHEM = fin.CHEMICAL_FINISHES
_PLATE = fin.METAL_PLATING_FINISHES
_COAT = fin.COATING_FINISHES
_SURFACE = {
    _CHEM[fin.Chemical.ANODIZED]: _anodized,
    _CHEM[fin.Chemical.BLACK_OXIDE]: _black_oxide,
    _CHEM[fin.Chemical.DYEING]: _dyeing,
    _PLATE[fin.MetalPlating.PVD]: _pvd,
    _PLATE[fin.MetalPlating.CHROME_PLATING]: _chrome,
    _PLATE[fin.MetalPlating.GOLD_PLATING]: _gold,
    _PLATE[fin.MetalPlating.NICKEL_PLATING]: _nickel,
    _PLATE[fin.MetalPlating.SILVER_PLATING]: _silver,
    _PLATE[fin.MetalPlating.TIN_PLATING]: _tin,
    _PLATE[fin.MetalPlating.ZINC_PLATING]: _zinc,
    _PLATE[fin.MetalPlating.VACUUM_PLATING]: _coat,
    _COAT[fin.Coating.POWDER_COAT]: _coat,
    _COAT[fin.Coating.SPRAY_PAINT]: _coat,
    _COAT[fin.Coating.ELECTROPHORESIS]: _ecoat,
}
# everything else (smooth machining, electropolished, passivation, pickling,
# chem film, conductive oxidation, laser, etch, silkscreen) leaves the look as-is.


def _normalize(finish: FinishSpec) -> list[AppliedFinish]:
    """Normalize the ``finish`` argument to a list of ``AppliedFinish``.

    Args:
        finish: ``None``, a single ``AppliedFinish``, or a list of them.

    Returns:
        A list of ``AppliedFinish`` (empty if ``finish`` is ``None``).
    """
    if finish is None:
        return []
    if isinstance(finish, AppliedFinish):
        return [finish]
    return list(finish)


def get_pbr_properties(
    material: RangeMaterial,
    finish: FinishSpec = None,
    process: AppliedProcess | None = None,
    color: Color | None = None,
    thickness_mm: float | None = None,
    opacity: float | None = None,
    roughness: float | None = None,
    scale: tuple[float, float] = (1.0, 1.0),
    rotation: float = 0.0,
    pbr: PbrProperties | None = None,
) -> PbrProperties:
    """Resolve a bundled three.js look for a finished material.

    Args:
        material: The material being rendered (dispatched on its ``category``).
        finish: An ``AppliedFinish`` (e.g. from ``spray_paint("blue")``) or a list of
            them -- each carries its own color.
        process: An ``AppliedProcess`` (e.g. from ``fdm(rotation=90)``) that nudges the
            default surface -- FDM to printed layer lines, the powder-bed routes to an
            as-built matte -- and carries that surface's per-part geometry.
        color: The material's own base color -- any build123d ``ColorLike`` -- applied
            only when no surface finish covers it (e.g. a colored filament or tinted
            resin); ignored for bare metals, whose color is intrinsic.
        thickness_mm: Pane thickness (mm) for transmissive materials.
        opacity: How see-through the part is, ``0.0`` (clear) to ``1.0`` (opaque), for a
            ``transparent`` material; ``None`` keeps the intrinsic clear look.
        roughness: Surface roughness ``0.0`` (glossy) to ``1.0`` (matte/frosted) for a
            ``transparent`` material; ``None`` keeps the factory value.
        scale: Texture UV scale ``(u, v)`` for the substrate texture; a textured
            finish's own scale takes precedence.
        rotation: Texture rotation in degrees (counterclockwise); a textured finish's
            own rotation takes precedence.
        pbr: A ready-made look, returned unchanged if given.

    Returns:
        The resolved ``PbrProperties``.
    """
    if pbr is not None:
        return pbr

    texture = None
    finish_uv = None  # (scale, rotation) from a textured finish, else None
    surface = None
    surface_color = None
    surface_sheen = None
    for af in _normalize(finish):
        f = af.finish
        if f in _TEXTURE:
            texture = _TEXTURE[f]
            finish_uv = (af.scale, af.rotation)
        elif f in _SURFACE:
            surface = f
            surface_color = af.color
            surface_sheen = af.sheen
    if texture is None and process is not None:
        texture = _PROCESS_TEXTURE.get(process.process)  # as-printed / as-built relief
        if texture == "fdm" and process.skin:
            # same route, different face: the solid top/bottom surface shows the skin,
            # not the extruded layer lines of the walls
            texture = "fdm_skin"

    if surface is None:
        # No covering/coloring finish -> the per-part color (case-2 selection);
        # bare metals pass color=None and render their intrinsic look.
        result = _plain_base(
            material, texture, _normalize_color(color), thickness_mm, opacity, roughness
        )
    else:
        rgb = _normalize_color(surface_color)
        result = _SURFACE[surface](material, rgb, texture, surface_sheen)

    # texture UV transform: the transform of whatever created the texture -- a textured
    # finish or the process -- wins over the material's own. (finish and process are
    # mutually exclusive, so at most one of these applies.)
    if finish_uv is not None and finish_uv != ((1.0, 1.0), 0.0):
        scale, rotation = finish_uv
    elif process is not None:
        if texture is not None and texture in _FDM_AUTHORED_PITCH:
            # the extrusion maps are authored in millimetres, so the per-part scale is
            # the tile size the printed pitch implies, not a multiplier. The rotation
            # they are authored at is read off the material (the skin bakes 45 deg, the
            # wall none), so a face that asks for exactly that keeps the plain id.
            baked_rotation = (
                0.0 if result.texture_rotation is None else result.texture_rotation
            )
            process_uv = (
                _fdm_scale(result, process.pitch_mm, texture, process.mm_per_uv),
                process.rotation,
            )
            as_authored = (_fdm_scale(result, None, texture), baked_rotation)
        else:
            process_uv = (process.scale, process.rotation)
            as_authored = ((1.0, 1.0), 0.0)
        if process_uv != as_authored:  # else the look already carries this transform
            scale, rotation = process_uv
    if scale != (1.0, 1.0) or rotation != 0.0:
        result = _apply_uv(result, scale, rotation)
    return result


__all__ = ["get_pbr_properties"]
