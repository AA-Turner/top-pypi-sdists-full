"""Catalog + PBR smoke tests.

The dataclass constructors already validate the data at import: ``Range.__post_init__``
rejects inverted bands and ``RangeMaterial.__init_subclass__`` rejects unknown
categories. These tests target what those do *not* cover:

- the catalog stays the expected size with unique names,
- ``mass()`` scales linearly with volume,
- the ``FinishedMaterial`` guard rails raise, and
- (the main event) every material resolves a three.js PBR look across the
  color / finish / process paths -- the branch-per-category logic in ``pbr.py``,
  which nothing else exercises. These are skipped when ``threejs_materials`` is absent.
"""

import warnings

import pytest

from bd_materials import finishes
from bd_materials.core import ALLOWED_CATEGORIES, NOT_SUITABLE, Range
from bd_materials.finished import FinishedMaterial
from bd_materials.processes import (
    AppliedProcess,
    Process,
    fdm,
    fdm_skin,
    machined,
    mjf,
    molded,
    slm,
    sls,
)
from bd_materials.finishes import Sheen
from bd_materials.materials import (
    ALL_MATERIALS,
    glass,
    metals,
    paper,
    plastics,
    resins,
    textile,
    wood,
)

try:  # the PBR tests need the viz stack; the rest run without it
    import threejs_materials  # noqa: F401

    HAS_THREEJS = True
except ImportError:
    HAS_THREEJS = False

requires_threejs = pytest.mark.skipif(
    not HAS_THREEJS, reason="threejs_materials not installed"
)


def test_catalog_size_and_unique_names():
    """The catalog holds the expected 95 materials, each with a unique name."""
    assert len(ALL_MATERIALS) == 95
    names = [m.name for m in ALL_MATERIALS]
    assert len(names) == len(set(names))


@pytest.mark.parametrize("material", ALL_MATERIALS, ids=lambda m: m.name)
def test_category_in_taxonomy(material):
    """Every material's category is a member of the allowed taxonomy."""
    assert material.category in ALLOWED_CATEGORIES


@pytest.mark.parametrize("material", ALL_MATERIALS, ids=lambda m: m.name)
def test_mass_scales_linearly_with_volume(material):
    """``mass()`` is positive and linear in volume (m = rho * V)."""
    assert material.mass(1000) > 0
    assert material.mass(2000) == pytest.approx(2 * material.mass(1000))


def test_family_function_returns_finished_material():
    """A family function returns a ``FinishedMaterial`` wrapping its material."""
    fm = metals.aluminum()
    assert isinstance(fm, FinishedMaterial)
    assert fm.material.category == "metal"
    assert fm.material.family == "aluminum"


def test_density_override_is_per_part_and_cast_free():
    """``density=`` overrides the part copy without touching the shared catalog entry."""
    default = metals.aluminum().material.density
    overridden = metals.aluminum(density=1234).material
    assert overridden.density == 1234
    assert metals.aluminum().material.density == default  # catalog entry unchanged


def test_finish_and_process_are_mutually_exclusive():
    """Passing both ``finish`` and ``process`` raises (a finish defines the surface)."""
    with pytest.raises(ValueError):
        metals.aluminum(finish=finishes.anodize("black"), process=machined())


@requires_threejs
def test_pbr_override_excludes_other_look_inputs():
    """``pbr=`` is a full override and cannot be combined with per-part look inputs."""
    look = metals.aluminum().pbr  # a real resolved PbrProperties
    with pytest.raises(ValueError):
        FinishedMaterial(metals.aluminum().material, color="red", pbr=look)


# --- PBR resolution: every material + a spread of finish/color/process paths ---

# One case per branch in pbr.py's dispatch and per surface handler in _SURFACE.
_PBR_CASES = {
    # bare substrates (case-1 / case-2 color, transmissive, composite)
    "alu_bare": lambda: metals.aluminum(),
    "pla_color_fdm": lambda: plastics.pla(color="red", process=fdm()),
    "pmma_clear_pane": lambda: plastics.pmma(color="clear", thickness_mm=3),
    "pc_pane": lambda: plastics.pc(thickness_mm=4),
    "pc_translucent": lambda: plastics.pc(color="white", opacity=0.65, roughness=0.3),
    "cfrp": lambda: plastics.cfrp(),
    "boro_pane": lambda: glass.borosilicate(color="green", thickness_mm=5),
    "oak": lambda: wood.hardwood(),
    "paper": lambda: paper.paper(),
    "cardboard": lambda: paper.cardboard(),
    "woven_color": lambda: textile.woven(color="blue"),
    # texture (mechanical) finishes
    "alu_brushed": lambda: metals.aluminum(finish=finishes.brushed()),
    "alu_bead_blast": lambda: metals.aluminum(finish=finishes.bead_blast()),
    "steel_slm_rough": lambda: metals.mild_steel(process=slm()),
    # surface (color) finishes -- one per _SURFACE handler
    "alu_anodize": lambda: metals.aluminum(finish=finishes.anodize("blue")),
    "steel_black_oxide": lambda: metals.mild_steel(finish=finishes.black_oxide()),
    "alu_dye": lambda: metals.aluminum(finish=finishes.dye("red")),
    "nylon_dye": lambda: plastics.nylon(finish=finishes.dye("blue")),
    "ss_pvd_clear": lambda: metals.stainless(finish=finishes.pvd()),
    "ss_pvd_gold": lambda: metals.stainless(finish=finishes.pvd("gold")),
    "ss_chrome": lambda: metals.stainless(finish=finishes.chrome()),
    "brass_gold": lambda: metals.brass(finish=finishes.gold_plate()),
    "copper_silver": lambda: metals.copper(finish=finishes.silver_plate()),
    "copper_nickel": lambda: metals.copper(finish=finishes.nickel_plate()),
    "copper_tin": lambda: metals.copper(finish=finishes.tin_plate()),
    "steel_zinc": lambda: metals.mild_steel(finish=finishes.zinc_plate("yellow")),
    "ti_vacuum": lambda: metals.titanium(finish=finishes.vacuum_plating("black")),
    "steel_powder": lambda: metals.mild_steel(finish=finishes.powder_coat("red")),
    "alu_spray_matte": lambda: metals.aluminum(
        finish=finishes.spray_paint("green", Sheen.MATTE)
    ),
    "steel_ecoat": lambda: metals.mild_steel(finish=finishes.electrophoresis()),
    "steel_ecoat_white": lambda: metals.mild_steel(
        finish=finishes.electrophoresis("white")
    ),
    "alu_brushed_ecoat": lambda: metals.aluminum(
        finish=[finishes.brushed(), finishes.electrophoresis()]
    ),
    # anodize on a brushed substrate (recolor-keeping-relief branch)
    "alu_brushed_anodize": lambda: metals.aluminum(
        finish=[finishes.brushed(), finishes.anodize("black")]
    ),
    # texture UV transform: substrate (family fn) and finish
    "oak_scaled": lambda: wood.hardwood(wood.Hardwood.OAK, scale=(2, 2), rotation=30),
    "woven_scaled": lambda: textile.woven(scale=(2, 2)),
    "alu_brushed_scaled": lambda: metals.aluminum(
        finish=finishes.brushed(scale=(3, 1), rotation=90)
    ),
}


@requires_threejs
@pytest.mark.parametrize("material", ALL_MATERIALS, ids=lambda m: m.name)
def test_every_material_resolves_a_pbr_look(material):
    """Each catalog material resolves a three.js look through its category branch."""
    fm = FinishedMaterial(material, thickness_mm=3 if material.transparent else None)
    assert fm.pbr is not None


@requires_threejs
@pytest.mark.parametrize("build", _PBR_CASES.values(), ids=list(_PBR_CASES))
def test_finish_color_process_paths_resolve(build):
    """Every finish / color / process path in pbr.py resolves without error."""
    assert build().pbr is not None


# --- the process axis: the as-made surface a production route leaves behind ---

# the filament families, which all print on the same FDM route
_FDM_FAMILIES = [
    plastics.pla,
    plastics.abs_,
    plastics.asa,
    plastics.petg,
    plastics.tpu,
    plastics.nylon,
    plastics.pp,
]


@requires_threejs
@pytest.mark.parametrize("family", _FDM_FAMILIES, ids=lambda f: f.__name__)
def test_fdm_process_renders_layer_lines(family):
    """``fdm()`` renders any filament family as printed layer lines."""
    assert family(process=fdm()).pbr.name == "plastic_fdm"


@requires_threejs
@pytest.mark.parametrize("rotation", [0, 90, 45], ids=["flat", "quarter", "diagonal"])
def test_fdm_keeps_its_millimetre_true_uv_transform(rotation):
    """The printed pitch survives resolution, rotated or not.

    ``plastic_fdm``'s map is authored at a real-world scale (a 6.4 mm tile of 0.2 mm
    layers) and ships ``normalize_uvs=False``. Rotating it -- the whole point of
    ``fdm(rotation=...)``, which lays the layer lines parallel to the base plate -- must
    not hand the pitch back to the bounding box, which is what the ``fixed=True``
    default of ``PbrProperties.scale`` would do.
    """
    look = plastics.pla(color="red", process=fdm(rotation=rotation)).pbr
    assert look.normalize_uvs is False
    assert tuple(look.texture_repeat) == pytest.approx((1 / 6.4, 1 / 6.4))
    assert (look.texture_rotation or 0) == rotation


@requires_threejs
@pytest.mark.parametrize(
    ("layer_height_mm", "tile_mm"), [(0.2, 6.4), (0.1, 3.2), (0.3, 9.6)]
)
def test_fdm_layer_height_scales_the_authored_tile(layer_height_mm, tile_mm):
    """``layer_height_mm`` scales the tile by the same ratio -- half the pitch, half the tile."""
    look = plastics.pla(process=fdm(layer_height_mm=layer_height_mm)).pbr
    assert look.normalize_uvs is False
    assert tuple(look.texture_repeat) == pytest.approx((1 / tile_mm, 1 / tile_mm))


@requires_threejs
@pytest.mark.parametrize("mm_per_uv", [1.0, 10.0, 25.0], ids=["metric", "r10", "r25"])
def test_mm_per_uv_corrects_a_non_metric_parameterization(mm_per_uv):
    """``mm_per_uv`` divides the authored tile, so the printed pitch survives raw UVs.

    The map is sampled in surface-parameter space. Where that space is metric along the
    build axis (planes, a cylinder's lateral face) one UV unit is one mm and the default
    ``1`` is right; where it is angular (a sphere's latitude, spanning pi radians at any
    size) one UV unit is the radius, and without saying so every sphere renders the same
    fixed layer count.
    """
    look = plastics.asa(process=fdm(mm_per_uv=mm_per_uv)).pbr
    assert look.normalize_uvs is False
    assert tuple(look.texture_repeat) == pytest.approx(
        (mm_per_uv / 6.4, mm_per_uv / 6.4)
    )


@requires_threejs
def test_mm_per_uv_composes_with_layer_height():
    """The two corrections are independent ratios on the same tile."""
    look = plastics.asa(process=fdm(layer_height_mm=0.1, mm_per_uv=10)).pbr
    # tile = 6.4 * (0.1 / 0.2) / 10
    assert tuple(look.texture_repeat) == pytest.approx((1 / 0.32, 1 / 0.32))


@requires_threejs
def test_fdm_skin_renders_the_solid_infill_surface():
    """``fdm_skin()`` is the same route as ``fdm()`` -- a different face of the print."""
    skin = plastics.asa(color="red", process=fdm_skin())
    assert skin.pbr.name == "plastic_fdm_skin"
    assert skin.process.process is Process.FDM  # still an FDM part
    assert skin.process.skin is True


@requires_threejs
@pytest.mark.parametrize("rotation", [45, -45, 0], ids=["top", "bottom", "axis"])
def test_fdm_skin_rotation_selects_the_infill_direction(rotation):
    """The authored 45 deg is a baked UV rotation; ``-45`` is the bottom face."""
    look = plastics.asa(process=fdm_skin(rotation=rotation)).pbr
    assert look.normalize_uvs is False
    assert tuple(look.texture_repeat) == pytest.approx((1 / 6.4, 1 / 6.4))
    assert (look.texture_rotation or 0) == rotation


@requires_threejs
@pytest.mark.parametrize(
    ("line_width_mm", "tile_mm"), [(0.4, 6.4), (0.2, 3.2), (0.6, 9.6)]
)
def test_fdm_skin_line_width_scales_the_authored_tile(line_width_mm, tile_mm):
    """The skin's pitch is the extrusion width (0.4 authored), not the layer height."""
    look = plastics.asa(process=fdm_skin(line_width_mm=line_width_mm)).pbr
    assert tuple(look.texture_repeat) == pytest.approx((1 / tile_mm, 1 / tile_mm))


@requires_threejs
def test_fdm_wall_and_skin_pitches_are_measured_separately():
    """The two maps share a tile but not a pitch, so equal numbers must differ in tile.

    The wall is authored at a 0.2 mm layer height and the skin at a 0.4 mm extrusion
    width, so asking both for 0.4 must scale the wall's tile and leave the skin's alone.
    """
    wall = plastics.asa(process=fdm(layer_height_mm=0.4)).pbr
    skin = plastics.asa(process=fdm_skin(line_width_mm=0.4)).pbr
    assert tuple(wall.texture_repeat) == pytest.approx((1 / 12.8, 1 / 12.8))
    assert tuple(skin.texture_repeat) == pytest.approx((1 / 6.4, 1 / 6.4))


@requires_threejs
def test_fdm_skin_on_metal_falls_back_to_matte():
    """Extruded filament surfaces have no metal map -- both FDM faces degrade together."""
    assert metals.aluminum(process=fdm_skin()).pbr.name == "aluminum_matte"


@requires_threejs
def test_powder_bed_scale_is_a_plain_multiplier():
    """An isotropic sintered surface tiles like any other texture -- no baked transform."""
    look = plastics.nylon(process=sls(scale=(2, 2))).pbr
    assert look.normalize_uvs is True
    assert tuple(look.texture_repeat) == pytest.approx((0.5, 0.5))


@requires_threejs
def test_bare_process_enum_is_deprecated_but_still_resolves():
    """The pre-process-function spelling warns, and reads as that route's defaults."""
    with pytest.warns(DeprecationWarning, match=r"process=fdm\(\)"):
        deprecated = plastics.pla(color="red", process=Process.FDM)
    assert deprecated.process == AppliedProcess(Process.FDM)
    assert deprecated.pbr.name == plastics.pla(color="red", process=fdm()).pbr.name


@requires_threejs
def test_process_function_does_not_warn():
    """The supported spelling is warning-free."""
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        assert plastics.pla(process=fdm(rotation=90)).pbr is not None


@requires_threejs
@pytest.mark.parametrize("process", [sls(), mjf()], ids=["sls", "mjf"])
def test_powder_bed_processes_render_rough(process):
    """The polymer powder-bed routes render as the as-built matte, not layer lines."""
    assert plastics.nylon(process=process).pbr.name == "plastic_rough"


@requires_threejs
@pytest.mark.parametrize(
    "process",
    [None, molded(), machined()],
    ids=["none", "molded", "machined"],
)
def test_smooth_processes_keep_the_clean_base(process):
    """Routes with no as-made relief keep the untextured plastic base."""
    look = plastics.pla(color="red", process=process).pbr
    assert look.name == "plastic"
    assert look.maps.normal is None  # no relief grafted on


@requires_threejs
def test_fdm_process_on_metal_falls_back_to_matte():
    """Layer lines are a filament surface: a metal asked for FDM gets the sintered matte."""
    assert metals.aluminum(process=fdm()).pbr.name == "aluminum_matte"


@requires_threejs
@pytest.mark.parametrize(
    "build",
    [
        lambda o: plastics.pc(color="white", opacity=o),
        lambda o: plastics.pmma(opacity=o),
        lambda o: glass.borosilicate(opacity=o),
    ],
    ids=["pc", "pmma", "boro"],
)
@pytest.mark.parametrize("opacity", [0.0, 0.35, 1.0])
def test_opacity_maps_to_transmission(build, opacity):
    """A transparent part's ``opacity`` dials three.js ``transmission`` = 1 - opacity."""
    assert build(opacity).pbr.values.transmission == pytest.approx(1.0 - opacity)


@requires_threejs
def test_opacity_none_keeps_intrinsic_clear_look():
    """Omitting ``opacity`` leaves the intrinsic fully-transmissive look untouched."""
    assert plastics.pc().pbr.values.transmission == pytest.approx(1.0)


@requires_threejs
@pytest.mark.parametrize(
    "build",
    [
        lambda r: plastics.pc(roughness=r),
        lambda r: plastics.pmma(roughness=r),
        lambda r: glass.borosilicate(roughness=r),
    ],
    ids=["pc", "pmma", "boro"],
)
@pytest.mark.parametrize("roughness", [0.0, 0.3, 1.0])
def test_roughness_overrides_transmissive_surface(build, roughness):
    """A transparent part's ``roughness`` overrides the factory surface value."""
    assert build(roughness).pbr.values.roughness == pytest.approx(roughness)


@requires_threejs
def test_opacity_and_roughness_are_independent():
    """``opacity`` and ``roughness`` set transmission and surface separately."""
    v = plastics.pc(color="white", opacity=0.45, roughness=0.3).pbr.values
    assert v.transmission == pytest.approx(0.55)  # opacity-driven
    assert v.roughness == pytest.approx(0.3)  # roughness-driven


@requires_threejs
def test_pbr_setter_pins_a_tuned_look():
    """Assigning ``.pbr`` pins a tuned look while the field-derived values persist."""
    m = plastics.pc(color="white", thickness_mm=2, opacity=0.45)
    m.pbr = m.pbr.override(roughness=0.45)  # resolve -> tune -> store back
    v = m.pbr.values
    assert v.roughness == pytest.approx(0.45)  # the override
    assert v.transmission == pytest.approx(0.55)  # opacity-derived, preserved
    assert v.thickness == pytest.approx(2)  # thickness_mm, preserved
    assert m.opacity == 0.45  # per-part fields stay as provenance


# --- color input (ColorLike) normalization ---------------------------------


@requires_threejs
@pytest.mark.parametrize(
    "color,expected",
    [
        (None, None),
        ("white", "#ffffff"),  # bd_materials/CSS name -> literal
        ("#ff8800", "#ff8800"),  # hex passthrough
        ("dodgerblue", "#1e90ff"),  # any CSS3 name resolves via webcolors
        ("chrome", "#c8ccce"),  # bd_materials material-appearance name
        ("notacolorname", "notacolorname"),  # unrecognized name passes through
        ("  Red ", "#ff0000"),  # name is trimmed + case-folded, then resolved
        (0xFF8800, "#ff8800"),  # packed 0xRRGGBB int
        ((1.0, 0.5, 0.0), (1.0, 0.5, 0.0)),  # rgb tuple
        ((1.0, 0.5, 0.0, 0.3), (1.0, 0.5, 0.0)),  # rgba -> alpha dropped
        (("red", 0.5), "#ff0000"),  # (name, alpha)
        ((0xFF8800, 0x80), "#ff8800"),  # (packed, alpha)
    ],
)
def test_normalize_color_shapes(color, expected):
    """Every accepted ColorLike shape coerces to a hex string or a 0..1 RGB triple."""
    from bd_materials.pbr import _normalize_color

    assert _normalize_color(color) == expected


@requires_threejs
def test_normalize_color_rejects_bool():
    """A bool is not a valid color (guarded because bool is a subclass of int)."""
    from bd_materials.pbr import _normalize_color

    with pytest.raises(TypeError):
        _normalize_color(True)


@requires_threejs
def test_normalize_color_accepts_build123d_color():
    """A build123d ``Color`` (Iterable[float]) is accepted structurally, no import."""
    b3d = pytest.importorskip("build123d")
    from bd_materials.pbr import _normalize_color

    r, g, b = _normalize_color(b3d.Color(0.2, 0.4, 0.6))
    assert (round(r, 3), round(g, 3), round(b, 3)) == (0.2, 0.4, 0.6)


@requires_threejs
@pytest.mark.parametrize("name", ["white", "black", "red", "green", "blue", "gold"])
def test_named_color_matches_build123d_literal(name):
    """A named palette color resolves to the same value as build123d's ``Color(name)``."""
    b3d = pytest.importorskip("build123d")
    from bd_materials.pbr import _normalize_color

    hex_str = _normalize_color(name)
    r, g, b, _ = tuple(b3d.Color(name))
    literal = f"#{round(r * 255):02x}{round(g * 255):02x}{round(b * 255):02x}"
    assert hex_str == literal


@requires_threejs
def test_normalize_color_accepts_ocp_quantity_colorrgba():
    """A raw OCP ``Quantity_ColorRGBA`` is accepted by duck typing (GetRGB)."""
    q_mod = pytest.importorskip("OCP.Quantity")
    from bd_materials.pbr import _normalize_color

    srgb = q_mod.Quantity_TypeOfColor.Quantity_TOC_sRGB
    q = q_mod.Quantity_ColorRGBA(q_mod.Quantity_Color(0.1, 0.2, 0.3, srgb), 1.0)
    r, g, b = _normalize_color(q)
    assert (round(r, 3), round(g, 3), round(b, 3)) == (0.1, 0.2, 0.3)


@requires_threejs
def test_texture_scale_and_rotation_apply():
    """scale/rotation reach the resolved texture UV; a finish's transform wins."""
    # default: no UV transform
    assert wood.hardwood(wood.Hardwood.OAK).pbr.texture_repeat is None
    # substrate texture, via the family function (scale(2,2) -> repeat (0.5, 0.5))
    oak = wood.hardwood(wood.Hardwood.OAK, scale=(2, 2), rotation=30).pbr
    assert oak.texture_repeat == (0.5, 0.5)
    assert oak.texture_rotation == 30
    # finish texture, via the textured verb
    assert metals.aluminum(
        finish=finishes.brushed(scale=(4, 4))
    ).pbr.texture_repeat == (
        0.25,
        0.25,
    )
    # precedence: a textured finish's transform wins over the material's
    both = wood.hardwood(scale=(2, 2), finish=finishes.brushed(scale=(4, 4))).pbr
    assert both.texture_repeat == (0.25, 0.25)


# --- custom_<category> user-defined materials ---

_CUSTOM_BUILDERS = {
    "metal": lambda: metals.custom_metal(name="X", density=4500, tensile_strength=900),
    "plastic": lambda: plastics.custom_plastic(name="X", density=1100, color="red"),
    "resin": lambda: resins.custom_resin(
        name="X", density=1150, hardness=80, hardness_scale="Shore A"
    ),
    "glass": lambda: glass.custom_glass(name="X", density=2500, thickness_mm=6),
    "wood": lambda: wood.custom_wood(
        name="X", density=650, janka_hardness=4000, scale=(2, 2)
    ),
    "paper": lambda: paper.custom_paper(name="X", density=700, areal_density=250),
    "textile": lambda: textile.custom_textile(name="X", density=400, color="blue"),
}


@pytest.mark.parametrize(
    "category,build", list(_CUSTOM_BUILDERS.items()), ids=list(_CUSTOM_BUILDERS)
)
def test_custom_material_builds(category, build):
    """Each custom_<category> returns a FinishedMaterial of the right category."""
    fm = build()
    assert isinstance(fm, FinishedMaterial)
    assert fm.material.category == category
    assert fm.material.mass(1_000_000) > 0


def test_custom_scalar_becomes_exact_range():
    """A scalar property is read as an exact value (min == max); Range/NOT_SUITABLE/None
    pass through."""
    m = metals.custom_metal(
        name="C",
        density=8000,
        tensile_strength=500,  # scalar -> exact Range(500, 500)
        yield_strength=Range(300, 420),  # Range kept as-is
        hardness=NOT_SUITABLE,  # n/a passes through (same sentinel)
        shear_strength=None,  # missing
    ).material
    assert m.tensile_strength == Range(500, 500)
    assert m.yield_strength == Range(300, 420)
    assert m.shear_strength is None
    assert m.hardness is NOT_SUITABLE


def test_custom_matches_direct_dataclass_construction():
    """custom_metal builds the same MetalMaterial as constructing the dataclass."""
    built = metals.custom_metal(
        name="C", density=8000, tensile_strength=500, yield_strength=Range(300, 420)
    ).material
    direct = metals.MetalMaterial(
        name="C",
        density=8000,
        family="stainless",
        tensile_strength=Range(500, 500),
        yield_strength=Range(300, 420),
        shear_strength=None,
        modulus_of_elasticity=None,
        shear_modulus=None,
        poisson_ratio=None,
        specific_heat_capacity=None,
        max_service_temp=None,
        thermal_expansion=None,
        thermal_conductivity=None,
        hardness=None,
        hardness_scale="HB",
        melting_temperature=None,
    )
    assert repr(built) == repr(direct)


@requires_threejs
@pytest.mark.parametrize(
    "build", list(_CUSTOM_BUILDERS.values()), ids=list(_CUSTOM_BUILDERS)
)
def test_custom_material_resolves_pbr(build):
    """Each custom material resolves a three.js look via its category branch."""
    assert build().pbr is not None


@requires_threejs
def test_custom_material_accepts_pbr_override():
    """A custom function passes a ready-made pbr straight through as the override."""
    look = metals.aluminum().pbr
    assert wood.custom_wood(name="W", density=650, pbr=look).pbr is look
