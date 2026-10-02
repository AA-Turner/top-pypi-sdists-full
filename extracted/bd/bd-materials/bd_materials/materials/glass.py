"""Typical-value property ranges for glass.

Glass is an amorphous, brittle inorganic solid, so the field set is tailored: it omits
``yield_strength``, ``shear_strength``, ``elongation_at_break`` and
``heat_deflection_temperature`` (a brittle solid has no ductile yield or elongation, and
HDT is a polymer test). ``tensile_strength`` is the practical **flaw-limited** annealed
strength -- surface flaws dominate, so pristine fiber is far higher. ``hardness`` is on
the Vickers (HV) scale. A ``glass_transition_temperature`` and a ``melting_temperature``
are both carried; the latter is the furnace-melt range (glass has no sharp melt point),
not a service limit -- use ``max_service_temp`` for that.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, ClassVar

from ..finished import Color, FinishedMaterial, FinishSpec
from ..processes import ProcessSpec
from ..core import Range, RangeInput, SolidMaterial, as_range, with_density

if TYPE_CHECKING:
    from threejs_materials import PbrProperties


@dataclass(frozen=True, kw_only=True)
class GlassMaterial(SolidMaterial):
    """A glass: the shared solid ranges (from ``SolidMaterial``; ``tensile_strength``
    is flaw-limited, annealed) plus Vickers hardness, a glass-transition and a
    furnace-melt range (see below). Brittle, so no yield/shear-strength fields.

    Glass is ``transparent``; the optional color + pane ``thickness_mm`` are
    per-part and live on the ``FinishedMaterial``.
    """

    category: ClassVar[str] = "glass"
    hardness: Range | None  # on the `hardness_scale` scale
    hardness_scale: str  # "HV" (Vickers)
    glass_transition_temperature: Range | None  # °C
    melting_temperature: Range | None  # °C -- furnace-melt range, not a service
    # limit (glass softens far lower, ~730/820C -- see max_service_temp)


# --- Soda-lime ---------------------------------------------------------------
class SodaLime(Enum):
    GENERIC = auto()


SODA_LIME_MATERIALS: dict[SodaLime, GlassMaterial] = {
    SodaLime.GENERIC: GlassMaterial(
        # identity
        name="SodaLime_GENERIC",
        family="soda_lime",
        transparent=True,
        # mechanical properties
        density=2500,
        hardness=Range(470, 570),
        hardness_scale="HV",
        modulus_of_elasticity=Range(68, 74),
        poisson_ratio=Range(0.21, 0.24),
        shear_modulus=Range(26, 30),
        tensile_strength=Range(30, 90),
        # thermal properties
        glass_transition_temperature=Range(520, 570),
        max_service_temp=Range(150, 300),
        melting_temperature=Range(1400, 1600),
        specific_heat_capacity=Range(750, 880),
        thermal_conductivity=Range(0.9, 1.1),
        thermal_expansion=Range(8.5e-6, 9.5e-6),
    ),
}


def soda_lime(
    grade: SodaLime = SodaLime.GENERIC,
    color: Color | None = None,
    thickness_mm: float | None = None,
    opacity: float | None = None,
    roughness: float | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[GlassMaterial]:
    """Soda-lime glass as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic.
        color: Base color for the part -- a build123d ``ColorLike``: a CSS3/palette
            name, a ``#rrggbb`` hex, a ``0xRRGGBB`` int, an RGB(A) tuple, or a
            ``Color``.
        thickness_mm: Pane thickness in mm; used for the transmissive look (the material
            is transparent).
        opacity: How see-through this part is, ``0.0`` (clear) to ``1.0`` (opaque);
            ``None`` keeps the clear look. Set it for a frosted / etched pane.
        roughness: Surface roughness, ``0.0`` (glossy) to ``1.0`` (matte / frosted);
            ``None`` keeps the factory value. Raise it together with ``opacity`` for an
            etched pane.
        finish: Surface finish -- an ``AppliedFinish`` or a list of them. Mutually
            exclusive with ``process``.
        process: How the part was made, from a process function (e.g. ``fdm()``).
            Mutually exclusive with
            ``finish``.
        density: Override the material's single representative density (kg/m³) for this
            part.

    Returns:
        A ``FinishedMaterial`` for the selected grade.
    """
    return FinishedMaterial(
        with_density(SODA_LIME_MATERIALS[grade], density),
        finish,
        color=color,
        thickness_mm=thickness_mm,
        opacity=opacity,
        roughness=roughness,
        process=process,
    )


# --- Borosilicate ------------------------------------------------------------
class Borosilicate(Enum):
    GENERIC = auto()


BOROSILICATE_MATERIALS: dict[Borosilicate, GlassMaterial] = {
    Borosilicate.GENERIC: GlassMaterial(
        # identity
        name="Borosilicate_GENERIC",
        family="borosilicate",
        transparent=True,
        # mechanical properties
        density=2230,
        hardness=Range(480, 600),
        hardness_scale="HV",
        modulus_of_elasticity=Range(60, 66),
        poisson_ratio=Range(0.19, 0.22),
        shear_modulus=Range(24, 28),
        tensile_strength=Range(30, 90),
        # thermal properties
        glass_transition_temperature=Range(490, 565),
        max_service_temp=Range(230, 400),
        melting_temperature=Range(1500, 1650),
        specific_heat_capacity=Range(750, 830),
        thermal_conductivity=Range(1.0, 1.2),
        thermal_expansion=Range(3.0e-6, 3.5e-6),
    ),
}


def borosilicate(
    grade: Borosilicate = Borosilicate.GENERIC,
    color: Color | None = None,
    thickness_mm: float | None = None,
    opacity: float | None = None,
    roughness: float | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[GlassMaterial]:
    """Borosilicate glass as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic.
        color: Base color for the part -- a build123d ``ColorLike``: a CSS3/palette
            name, a ``#rrggbb`` hex, a ``0xRRGGBB`` int, an RGB(A) tuple, or a
            ``Color``.
        thickness_mm: Pane thickness in mm; used for the transmissive look (the material
            is transparent).
        opacity: How see-through this part is, ``0.0`` (clear) to ``1.0`` (opaque);
            ``None`` keeps the clear look. Set it for a frosted / etched pane.
        roughness: Surface roughness, ``0.0`` (glossy) to ``1.0`` (matte / frosted);
            ``None`` keeps the factory value. Raise it together with ``opacity`` for an
            etched pane.
        finish: Surface finish -- an ``AppliedFinish`` or a list of them. Mutually
            exclusive with ``process``.
        process: How the part was made, from a process function (e.g. ``fdm()``).
            Mutually exclusive with
            ``finish``.
        density: Override the material's single representative density (kg/m³) for this
            part.

    Returns:
        A ``FinishedMaterial`` for the selected grade.
    """
    return FinishedMaterial(
        with_density(BOROSILICATE_MATERIALS[grade], density),
        finish,
        color=color,
        thickness_mm=thickness_mm,
        opacity=opacity,
        roughness=roughness,
        process=process,
    )


ALL_GLASSES = (
    *SODA_LIME_MATERIALS.values(),
    *BOROSILICATE_MATERIALS.values(),
)


def custom_glass(
    name: str,
    density: float,
    *,
    family: str = "glass",
    transparent: bool = True,
    tensile_strength: RangeInput = None,
    modulus_of_elasticity: RangeInput = None,
    shear_modulus: RangeInput = None,
    poisson_ratio: RangeInput = None,
    hardness: RangeInput = None,
    hardness_scale: str = "HV",
    glass_transition_temperature: RangeInput = None,
    melting_temperature: RangeInput = None,
    max_service_temp: RangeInput = None,
    specific_heat_capacity: RangeInput = None,
    thermal_conductivity: RangeInput = None,
    thermal_expansion: RangeInput = None,
    color: Color | None = None,
    thickness_mm: float | None = None,
    opacity: float | None = None,
    roughness: float | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    pbr: PbrProperties | None = None,
) -> FinishedMaterial[GlassMaterial]:
    """Define a custom glass and return it as a ``FinishedMaterial``.

    Each property value may be a ``Range``, a bare number (an exact value, ``min ==
    max``), or ``None`` (missing); ``NOT_SUITABLE`` marks a property that does not
    apply. The property keyword args are the ``GlassMaterial`` fields.

    Args:
        name: Identifier for the material.
        density: Single representative density (kg/m³).
        family: PBR look key; glass renders category-first, so this is mostly identity.
            Defaults to ``"glass"``.
        transparent: Intrinsic see-through flag (glass is transmissive). Default
            ``True``; ``thickness_mm`` sets the pane thickness.
        hardness_scale: Scale for ``hardness`` (``"HV"`` Vickers).
        color: Optional glass tint -- a build123d ``ColorLike`` (name, hex,
            ``0xRRGGBB`` int, RGB(A) tuple, or a ``Color``).
        thickness_mm: Pane thickness in mm for the transmissive look.
        opacity: How see-through the part is, ``0.0`` (clear) to ``1.0`` (opaque);
            meaningful only when ``transparent``. ``None`` keeps the clear look.
        roughness: Surface roughness ``0.0`` (glossy) to ``1.0`` (matte / frosted);
            meaningful only when ``transparent``. ``None`` keeps the factory value.
        finish: Surface finish -- mutually exclusive with ``process`` and ``pbr``.
        process: As-made surface hint -- mutually exclusive with ``finish`` and ``pbr``.
        pbr: A ready-made three.js look; overrides the resolved one.

    Returns:
        A ``FinishedMaterial`` wrapping the custom glass.
    """
    return FinishedMaterial(
        GlassMaterial(
            name=name,
            density=density,
            family=family,
            transparent=transparent,
            tensile_strength=as_range(tensile_strength),
            modulus_of_elasticity=as_range(modulus_of_elasticity),
            shear_modulus=as_range(shear_modulus),
            poisson_ratio=as_range(poisson_ratio),
            specific_heat_capacity=as_range(specific_heat_capacity),
            max_service_temp=as_range(max_service_temp),
            thermal_expansion=as_range(thermal_expansion),
            thermal_conductivity=as_range(thermal_conductivity),
            hardness=as_range(hardness),
            hardness_scale=hardness_scale,
            glass_transition_temperature=as_range(glass_transition_temperature),
            melting_temperature=as_range(melting_temperature),
        ),
        finish,
        color=color,
        thickness_mm=thickness_mm,
        opacity=opacity,
        roughness=roughness,
        process=process,
        pbr=pbr,
    )


if __name__ == "__main__":
    print(f"glasses: {len(ALL_GLASSES)}")
    print()
    for _g in ALL_GLASSES:
        print(_g)
        print()
