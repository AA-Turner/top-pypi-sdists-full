"""Typical-value property ranges for photopolymer resins (SLA / DLP).

Resins are modelled as functional families (standard, tough, high-temp, flexible, ...),
one family per resin type. Each carries the polymer property set --
``glass_transition_temperature``, ``heat_deflection_temperature``,
``elongation_at_break`` and a Shore ``hardness`` on its ``hardness_scale`` ("Shore D"
for rigid resins, "Shore A" for flexible/elastomeric ones). ``yield_strength`` ~equals
``tensile_strength`` for the rigid families and is ``NOT_SUITABLE`` for the flexible one.

For rigid photopolymers Tg and HDT bands nearly coincide: these resins are tested near
Tg, so HDT (usually ~5-15C below Tg) overlaps it -- not a duplication.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, ClassVar

from ..finished import Color, FinishedMaterial, FinishSpec
from ..processes import ProcessSpec
from ..core import (
    NOT_SUITABLE,
    PolymerMaterial,
    Range,
    RangeInput,
    as_range,
    with_density,
)

if TYPE_CHECKING:
    from threejs_materials import PbrProperties


@dataclass(frozen=True, kw_only=True)
class ResinMaterial(PolymerMaterial):
    """A photopolymer resin: the shared polymer ranges (from ``PolymerMaterial``) plus
    a Shore hardness. ``hardness_scale`` is "Shore D" for rigid resins, "Shore A" for
    flexible ones. ``transparent`` is True for the clear resin; a part's color lives
    on the ``FinishedMaterial``.
    """

    category: ClassVar[str] = "resin"
    hardness: Range | None  # on the `hardness_scale` scale
    hardness_scale: str  # "Shore D" (rigid) / "Shore A" (flexible)


# --- Standard ----------------------------------------------------------------
class Standard(Enum):
    GENERIC = auto()


STANDARD_MATERIALS: dict[Standard, ResinMaterial] = {
    Standard.GENERIC: ResinMaterial(
        # identity
        name="Standard_GENERIC",
        family="resin",
        # mechanical properties
        density=1150,
        elongation_at_break=Range(5, 12),
        hardness=Range(80, 86),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(2.4, 3.2),
        poisson_ratio=Range(0.38, 0.42),
        shear_modulus=Range(0.85, 1.15),
        shear_strength=Range(27, 36),
        tensile_strength=Range(45, 60),
        yield_strength=Range(42, 55),
        # thermal properties
        glass_transition_temperature=Range(50, 65),
        heat_deflection_temperature=Range(50, 65),
        max_service_temp=Range(45, 55),
        specific_heat_capacity=Range(1400, 1600),
        thermal_conductivity=Range(0.18, 0.25),
        thermal_expansion=Range(80e-6, 130e-6),
    ),
}


def standard(
    grade: Standard = Standard.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[ResinMaterial]:
    """Standard resin as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic.
        color: Base color for the part -- a build123d ``ColorLike``: a CSS3/palette
            name, a ``#rrggbb`` hex, a ``0xRRGGBB`` int, an RGB(A) tuple, or a
            ``Color``.
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
        with_density(STANDARD_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- Tough -------------------------------------------------------------------
class Tough(Enum):
    GENERIC = auto()


TOUGH_MATERIALS: dict[Tough, ResinMaterial] = {
    Tough.GENERIC: ResinMaterial(
        # identity
        name="Tough_GENERIC",
        family="resin",
        # mechanical properties
        density=1150,
        elongation_at_break=Range(20, 60),
        hardness=Range(78, 84),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(2.0, 2.8),
        poisson_ratio=Range(0.38, 0.42),
        shear_modulus=Range(0.7, 1.0),
        shear_strength=Range(24, 33),
        tensile_strength=Range(40, 55),
        yield_strength=Range(35, 48),
        # thermal properties
        glass_transition_temperature=Range(45, 60),
        heat_deflection_temperature=Range(45, 58),
        max_service_temp=Range(40, 55),
        specific_heat_capacity=Range(1400, 1600),
        thermal_conductivity=Range(0.18, 0.25),
        thermal_expansion=Range(90e-6, 150e-6),
    ),
}


def tough(
    grade: Tough = Tough.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[ResinMaterial]:
    """Tough resin as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic.
        color: Base color for the part -- a build123d ``ColorLike``: a CSS3/palette
            name, a ``#rrggbb`` hex, a ``0xRRGGBB`` int, an RGB(A) tuple, or a
            ``Color``.
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
        with_density(TOUGH_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- High-temp ---------------------------------------------------------------
class HighTemp(Enum):
    GENERIC = auto()


HIGH_TEMP_MATERIALS: dict[HighTemp, ResinMaterial] = {
    HighTemp.GENERIC: ResinMaterial(
        # identity
        name="HighTemp_GENERIC",
        family="resin",
        # mechanical properties
        density=1300,
        elongation_at_break=Range(1, 10),
        hardness=Range(80, 86),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(2.8, 3.6),
        poisson_ratio=Range(0.38, 0.42),
        shear_modulus=Range(1.0, 1.3),
        shear_strength=Range(24, 33),
        tensile_strength=Range(40, 55),
        yield_strength=Range(38, 50),
        # thermal properties
        glass_transition_temperature=Range(110, 245),
        heat_deflection_temperature=Range(100, 230),
        max_service_temp=Range(100, 200),
        specific_heat_capacity=Range(1400, 1600),
        thermal_conductivity=Range(0.18, 0.25),
        thermal_expansion=Range(70e-6, 120e-6),
    ),
}


def high_temp(
    grade: HighTemp = HighTemp.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[ResinMaterial]:
    """High-temperature resin as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic.
        color: Base color for the part -- a build123d ``ColorLike``: a CSS3/palette
            name, a ``#rrggbb`` hex, a ``0xRRGGBB`` int, an RGB(A) tuple, or a
            ``Color``.
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
        with_density(HIGH_TEMP_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- Ceramic -----------------------------------------------------------------
class Ceramic(Enum):
    GENERIC = auto()


CERAMIC_MATERIALS: dict[Ceramic, ResinMaterial] = {
    Ceramic.GENERIC: ResinMaterial(
        # identity
        name="Ceramic_GENERIC",
        family="resin",
        # mechanical properties
        density=1650,
        elongation_at_break=Range(1, 3),
        hardness=Range(88, 95),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(5, 9),
        poisson_ratio=Range(0.30, 0.35),
        shear_modulus=Range(3.0, 4.5),
        shear_strength=Range(36, 48),
        tensile_strength=Range(60, 80),
        yield_strength=Range(55, 72),
        # thermal properties
        glass_transition_temperature=Range(150, 250),
        # ceramic-filled: HDT is filler-controlled and can exceed the matrix Tg (not an inversion)
        heat_deflection_temperature=Range(200, 280),
        max_service_temp=Range(150, 220),
        specific_heat_capacity=Range(1100, 1300),
        thermal_conductivity=Range(0.2, 0.5),
        thermal_expansion=Range(30e-6, 70e-6),
    ),
}


def ceramic(
    grade: Ceramic = Ceramic.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[ResinMaterial]:
    """Ceramic-filled resin as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic.
        color: Base color for the part -- a build123d ``ColorLike``: a CSS3/palette
            name, a ``#rrggbb`` hex, a ``0xRRGGBB`` int, an RGB(A) tuple, or a
            ``Color``.
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
        with_density(CERAMIC_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- Castable ----------------------------------------------------------------
class Castable(Enum):
    GENERIC = auto()


CASTABLE_MATERIALS: dict[Castable, ResinMaterial] = {
    Castable.GENERIC: ResinMaterial(
        # identity
        name="Castable_GENERIC",
        family="resin",
        # mechanical properties
        density=1150,
        elongation_at_break=Range(3, 10),
        hardness=Range(76, 83),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(2.2, 3.0),
        poisson_ratio=Range(0.38, 0.42),
        shear_modulus=Range(0.8, 1.1),
        shear_strength=Range(21, 30),
        tensile_strength=Range(35, 50),
        yield_strength=Range(32, 45),
        # thermal properties
        glass_transition_temperature=Range(48, 62),
        heat_deflection_temperature=Range(48, 62),
        max_service_temp=Range(40, 55),
        specific_heat_capacity=Range(1400, 1600),
        thermal_conductivity=Range(0.18, 0.25),
        thermal_expansion=Range(90e-6, 150e-6),
    ),
}


def castable(
    grade: Castable = Castable.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[ResinMaterial]:
    """Castable resin as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic.
        color: Base color for the part -- a build123d ``ColorLike``: a CSS3/palette
            name, a ``#rrggbb`` hex, a ``0xRRGGBB`` int, an RGB(A) tuple, or a
            ``Color``.
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
        with_density(CASTABLE_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- ESD ---------------------------------------------------------------------
class Esd(Enum):
    GENERIC = auto()


ESD_MATERIALS: dict[Esd, ResinMaterial] = {
    Esd.GENERIC: ResinMaterial(
        # identity
        name="Esd_GENERIC",
        family="resin",
        # mechanical properties
        density=1300,
        elongation_at_break=Range(5, 15),
        # hardness is approximate: ESD-resin datasheets rarely quote a Shore value
        hardness=Range(80, 88),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(1.6, 2.4),
        poisson_ratio=Range(0.38, 0.42),
        shear_modulus=Range(0.55, 0.85),
        shear_strength=Range(23, 30),
        tensile_strength=Range(38, 50),
        yield_strength=Range(35, 46),
        # thermal properties
        glass_transition_temperature=Range(55, 70),
        heat_deflection_temperature=Range(55, 70),
        max_service_temp=Range(45, 60),
        specific_heat_capacity=Range(1400, 1600),
        thermal_conductivity=Range(0.18, 0.25),
        thermal_expansion=Range(80e-6, 130e-6),
    ),
}


def esd(
    grade: Esd = Esd.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[ResinMaterial]:
    """ESD (static-dissipative) resin as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic.
        color: Base color for the part -- a build123d ``ColorLike``: a CSS3/palette
            name, a ``#rrggbb`` hex, a ``0xRRGGBB`` int, an RGB(A) tuple, or a
            ``Color``.
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
        with_density(ESD_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- Transparent -------------------------------------------------------------
class Transparent(Enum):
    GENERIC = auto()


TRANSPARENT_MATERIALS: dict[Transparent, ResinMaterial] = {
    Transparent.GENERIC: ResinMaterial(
        # identity
        name="Transparent_GENERIC",
        family="resin",
        transparent=True,
        # mechanical properties
        density=1300,
        elongation_at_break=Range(5, 15),
        hardness=Range(80, 88),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(1.6, 2.4),
        poisson_ratio=Range(0.38, 0.42),
        shear_modulus=Range(0.55, 0.85),
        shear_strength=Range(23, 31),
        tensile_strength=Range(38, 52),
        yield_strength=Range(35, 48),
        # thermal properties
        glass_transition_temperature=Range(45, 62),
        heat_deflection_temperature=Range(45, 60),
        max_service_temp=Range(40, 55),
        specific_heat_capacity=Range(1400, 1600),
        thermal_conductivity=Range(0.18, 0.25),
        thermal_expansion=Range(80e-6, 130e-6),
    ),
}


def transparent(
    grade: Transparent = Transparent.GENERIC,
    color: Color | None = None,
    thickness_mm: float | None = None,
    opacity: float | None = None,
    roughness: float | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[ResinMaterial]:
    """Transparent resin as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic.
        color: Base color for the part -- a build123d ``ColorLike``: a CSS3/palette
            name, a ``#rrggbb`` hex, a ``0xRRGGBB`` int, an RGB(A) tuple, or a
            ``Color``.
        thickness_mm: Pane thickness in mm; used for the transmissive look (the material
            is transparent).
        opacity: How see-through this part is, ``0.0`` (clear) to ``1.0`` (opaque);
            ``None`` keeps the clear look. Set it for a translucent / tinted cast part.
        roughness: Surface roughness, ``0.0`` (glossy) to ``1.0`` (matte / frosted);
            ``None`` keeps the factory value. Independent of ``opacity``.
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
        with_density(TRANSPARENT_MATERIALS[grade], density),
        finish,
        color=color,
        thickness_mm=thickness_mm,
        opacity=opacity,
        roughness=roughness,
        process=process,
    )


# --- Flexible ----------------------------------------------------------------
class Flexible(Enum):
    GENERIC = auto()


FLEXIBLE_MATERIALS: dict[Flexible, ResinMaterial] = {
    Flexible.GENERIC: ResinMaterial(
        # identity
        name="Flexible_GENERIC",
        family="resin",
        # mechanical properties
        density=1150,
        elongation_at_break=Range(25, 120),
        hardness=Range(55, 85),
        hardness_scale="Shore A",
        modulus_of_elasticity=Range(0.001, 0.5),
        poisson_ratio=Range(0.40, 0.49),
        shear_modulus=Range(0.0003, 0.17),
        shear_strength=Range(3, 18),
        tensile_strength=Range(5, 30),
        yield_strength=NOT_SUITABLE,
        # thermal properties
        glass_transition_temperature=Range(-20, 25),
        heat_deflection_temperature=NOT_SUITABLE,
        max_service_temp=Range(40, 70),
        specific_heat_capacity=Range(1400, 1600),
        thermal_conductivity=Range(0.15, 0.25),
        thermal_expansion=Range(100e-6, 200e-6),
    ),
}


def flexible(
    grade: Flexible = Flexible.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[ResinMaterial]:
    """Flexible resin as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic.
        color: Base color for the part -- a build123d ``ColorLike``: a CSS3/palette
            name, a ``#rrggbb`` hex, a ``0xRRGGBB`` int, an RGB(A) tuple, or a
            ``Color``.
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
        with_density(FLEXIBLE_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


ALL_RESINS = (
    *STANDARD_MATERIALS.values(),
    *TOUGH_MATERIALS.values(),
    *HIGH_TEMP_MATERIALS.values(),
    *CERAMIC_MATERIALS.values(),
    *CASTABLE_MATERIALS.values(),
    *ESD_MATERIALS.values(),
    *TRANSPARENT_MATERIALS.values(),
    *FLEXIBLE_MATERIALS.values(),
)


def custom_resin(
    name: str,
    density: float,
    *,
    family: str = "resin",
    transparent: bool = False,
    tensile_strength: RangeInput = None,
    yield_strength: RangeInput = None,
    shear_strength: RangeInput = None,
    modulus_of_elasticity: RangeInput = None,
    shear_modulus: RangeInput = None,
    poisson_ratio: RangeInput = None,
    elongation_at_break: RangeInput = None,
    hardness: RangeInput = None,
    hardness_scale: str = "Shore D",
    glass_transition_temperature: RangeInput = None,
    heat_deflection_temperature: RangeInput = None,
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
) -> FinishedMaterial[ResinMaterial]:
    """Define a custom resin and return it as a ``FinishedMaterial``.

    Each property value may be a ``Range``, a bare number (an exact value, ``min ==
    max``), or ``None`` (missing); ``NOT_SUITABLE`` marks a property that does not
    apply. The property keyword args are the ``ResinMaterial`` fields.

    Args:
        name: Identifier for the material.
        density: Single representative density (kg/m³).
        family: PBR look key; an unknown key falls back per the PBR bridge. Defaults to
            ``"resin"``.
        transparent: Intrinsic see-through flag; set for a clear resin (uses
            ``thickness_mm``). Default ``False``.
        hardness_scale: Shore scale for ``hardness`` (``"Shore D"`` rigid / ``"Shore A"``
            flexible).
        color: Selectable base color -- a build123d ``ColorLike`` (name, hex,
            ``0xRRGGBB`` int, RGB(A) tuple, or a ``Color``).
        thickness_mm: Pane thickness in mm, meaningful only when ``transparent``.
        opacity: How see-through the part is, ``0.0`` (clear) to ``1.0`` (opaque);
            meaningful only when ``transparent``. ``None`` keeps the clear look.
        roughness: Surface roughness ``0.0`` (glossy) to ``1.0`` (matte / frosted);
            meaningful only when ``transparent``. ``None`` keeps the factory value.
        finish: Surface finish -- mutually exclusive with ``process`` and ``pbr``.
        process: As-made surface hint -- mutually exclusive with ``finish`` and ``pbr``.
        pbr: A ready-made three.js look; overrides the resolved one.

    Returns:
        A ``FinishedMaterial`` wrapping the custom resin.
    """
    return FinishedMaterial(
        ResinMaterial(
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
            yield_strength=as_range(yield_strength),
            shear_strength=as_range(shear_strength),
            elongation_at_break=as_range(elongation_at_break),
            glass_transition_temperature=as_range(glass_transition_temperature),
            heat_deflection_temperature=as_range(heat_deflection_temperature),
            hardness=as_range(hardness),
            hardness_scale=hardness_scale,
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
    print(f"resins: {len(ALL_RESINS)}")
    print()
    print(STANDARD_MATERIALS[Standard.GENERIC])
    print(CERAMIC_MATERIALS[Ceramic.GENERIC])
