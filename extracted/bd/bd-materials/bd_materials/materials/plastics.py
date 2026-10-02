"""Typical-value property ranges for plastics.

A ``PlasticMaterial`` holds a single representative ``density`` plus min-max ``Range``
bands for the mechanical/thermal properties. The set adds
``glass_transition_temperature`` (the transition that governs polymer service, in place
of a melting point), ``heat_deflection_temperature``, ``elongation_at_break`` and a
Shore ``hardness`` on its ``hardness_scale`` ("Shore D" for rigid grades, "Shore A" for
elastomers).

For a brittle thermoplastic or short-fiber grade that fractures with little yielding,
``yield_strength`` ~equals ``tensile_strength``. A field is ``NOT_SUITABLE`` where the
property does not apply (an elastomer's yield or heat-deflection, a laminate's isotropic
yield) and ``None`` where a value is simply not filled in.
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
class PlasticMaterial(PolymerMaterial):
    """A plastic: the shared polymer ranges (from ``PolymerMaterial``) plus a Shore
    hardness. ``family`` is the PBR/identity key; ``transparent`` is True for clear
    grades (PMMA, PC). A part's color lives on ``FinishedMaterial``, not here.
    """

    category: ClassVar[str] = "plastic"
    hardness: Range | None  # on the `hardness_scale` scale
    hardness_scale: str  # "Shore D", "Shore A", ...


# --- PLA ---------------------------------------------------------------------
class PLA(Enum):
    GENERIC = auto()
    CARBON_FILLED = auto()


PLA_MATERIALS: dict[PLA, PlasticMaterial] = {
    PLA.GENERIC: PlasticMaterial(
        # identity
        name="PLA_GENERIC",
        family="PLA",
        # mechanical properties
        density=1240,
        elongation_at_break=Range(3, 7),
        hardness=Range(78, 85),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(3.0, 3.9),
        poisson_ratio=Range(0.35, 0.40),
        shear_modulus=Range(1.2, 1.5),
        shear_strength=Range(30, 55),
        tensile_strength=Range(45, 70),
        yield_strength=Range(45, 60),
        # thermal properties
        glass_transition_temperature=Range(55, 65),
        heat_deflection_temperature=Range(50, 60),
        max_service_temp=Range(50, 60),
        specific_heat_capacity=Range(1800, 1900),
        thermal_conductivity=Range(0.11, 0.16),
        thermal_expansion=Range(60e-6, 90e-6),
    ),
    PLA.CARBON_FILLED: PlasticMaterial(
        # identity
        name="PLA_CARBON_FILLED",
        family="PLA",
        # mechanical properties
        density=1250,
        elongation_at_break=Range(1, 3),
        hardness=Range(80, 88),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(4.0, 7.0),
        poisson_ratio=Range(0.35, 0.40),
        shear_modulus=Range(2.0, 3.5),
        shear_strength=Range(30, 50),
        tensile_strength=Range(40, 65),
        yield_strength=Range(40, 55),
        # thermal properties
        glass_transition_temperature=Range(55, 65),
        heat_deflection_temperature=Range(55, 70),
        max_service_temp=Range(55, 65),
        specific_heat_capacity=Range(1500, 1700),
        thermal_conductivity=Range(0.15, 0.30),
        thermal_expansion=Range(25e-6, 50e-6),
    ),
}


def pla(
    grade: PLA = PLA.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """PLA as a ``FinishedMaterial``.

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
        with_density(PLA_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- ABS ---------------------------------------------------------------------
class ABS(Enum):
    GENERIC = auto()
    FLAME_RETARDANT = auto()


ABS_MATERIALS: dict[ABS, PlasticMaterial] = {
    # density 1050 is vendor-representative; filament ABS runs ~1020-1090 (SunLu 1020,
    # eSun/Flashforge 1040-1060, Anycubic 1050, Elegoo 1090). For a specific spool
    # (e.g. SunLu's 1020) pass density= rather than changing this default.
    ABS.GENERIC: PlasticMaterial(
        # identity
        name="ABS_GENERIC",
        family="ABS",
        # mechanical properties
        density=1050,
        elongation_at_break=Range(5, 25),
        hardness=Range(70, 80),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(1.8, 2.5),
        poisson_ratio=Range(0.35, 0.40),
        shear_modulus=Range(0.7, 0.9),
        shear_strength=Range(20, 35),
        tensile_strength=Range(30, 50),
        yield_strength=Range(30, 45),
        # thermal properties
        glass_transition_temperature=Range(100, 110),
        heat_deflection_temperature=Range(75, 95),
        max_service_temp=Range(60, 80),
        specific_heat_capacity=Range(1300, 1500),
        thermal_conductivity=Range(0.15, 0.20),
        thermal_expansion=Range(80e-6, 110e-6),
    ),
    ABS.FLAME_RETARDANT: PlasticMaterial(
        # identity
        name="ABS_FLAME_RETARDANT",
        family="ABS",
        # mechanical properties
        density=1200,
        elongation_at_break=Range(5, 20),
        hardness=Range(72, 82),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(2.0, 2.6),
        poisson_ratio=Range(0.35, 0.40),
        shear_modulus=Range(0.75, 0.95),
        shear_strength=Range(22, 38),
        tensile_strength=Range(30, 45),
        yield_strength=Range(30, 42),
        # thermal properties
        glass_transition_temperature=Range(100, 110),
        heat_deflection_temperature=Range(75, 90),
        max_service_temp=Range(60, 75),
        specific_heat_capacity=Range(1300, 1500),
        thermal_conductivity=Range(0.15, 0.22),
        thermal_expansion=Range(80e-6, 110e-6),
    ),
}


def abs_(
    grade: ABS = ABS.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """ABS as a ``FinishedMaterial``.

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
        with_density(ABS_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- Nylon (PA) --------------------------------------------------------------
class Nylon(Enum):
    PA6 = auto()
    PA12 = auto()
    PA12_SINTERED = auto()
    PA12_GF35 = auto()


NYLON_MATERIALS: dict[Nylon, PlasticMaterial] = {
    Nylon.PA6: PlasticMaterial(
        # identity
        name="Nylon_PA6",
        family="PA",
        # mechanical properties
        density=1140,
        elongation_at_break=Range(20, 300),
        hardness=Range(75, 85),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(1.9, 3.5),
        poisson_ratio=Range(0.38, 0.42),
        shear_modulus=Range(0.8, 1.3),
        shear_strength=Range(30, 60),
        tensile_strength=Range(50, 90),
        yield_strength=Range(45, 85),
        # thermal properties
        glass_transition_temperature=Range(45, 60),
        heat_deflection_temperature=Range(60, 100),
        max_service_temp=Range(80, 130),
        specific_heat_capacity=Range(1600, 1700),
        thermal_conductivity=Range(0.24, 0.31),
        thermal_expansion=Range(70e-6, 100e-6),
    ),
    Nylon.PA12: PlasticMaterial(
        # identity
        name="Nylon_PA12",
        family="PA",
        # mechanical properties
        density=1010,
        elongation_at_break=Range(5, 300),
        hardness=Range(70, 80),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(1.2, 1.8),
        poisson_ratio=Range(0.38, 0.42),
        shear_modulus=Range(0.5, 0.8),
        shear_strength=Range(25, 40),
        tensile_strength=Range(30, 55),
        yield_strength=Range(30, 50),
        # thermal properties
        glass_transition_temperature=Range(40, 50),
        heat_deflection_temperature=Range(45, 80),
        max_service_temp=Range(70, 95),
        specific_heat_capacity=Range(1700, 1800),
        thermal_conductivity=Range(0.23, 0.28),
        thermal_expansion=Range(100e-6, 150e-6),
    ),
    Nylon.PA12_SINTERED: PlasticMaterial(
        # identity
        name="Nylon_PA12_SINTERED",
        family="PA",
        # mechanical properties
        density=1000,
        elongation_at_break=Range(5, 25),
        hardness=Range(70, 80),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(1.5, 1.9),
        poisson_ratio=Range(0.38, 0.42),
        shear_modulus=Range(0.5, 0.75),
        shear_strength=Range(25, 40),
        tensile_strength=Range(45, 50),
        yield_strength=Range(40, 48),
        # thermal properties
        glass_transition_temperature=Range(40, 50),
        heat_deflection_temperature=Range(70, 95),
        max_service_temp=Range(80, 110),
        specific_heat_capacity=Range(1700, 1800),
        thermal_conductivity=Range(0.2, 0.3),
        thermal_expansion=Range(90e-6, 150e-6),
    ),
    Nylon.PA12_GF35: PlasticMaterial(
        # identity
        name="Nylon_PA12_GF35",
        family="PA",
        # mechanical properties
        density=1300,
        elongation_at_break=Range(3, 10),
        hardness=Range(78, 85),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(2.5, 4.5),
        poisson_ratio=Range(0.38, 0.42),
        shear_modulus=Range(1.0, 1.8),
        shear_strength=Range(30, 50),
        tensile_strength=Range(40, 70),
        yield_strength=Range(40, 65),
        # thermal properties
        glass_transition_temperature=Range(40, 50),
        heat_deflection_temperature=Range(140, 175),
        max_service_temp=Range(100, 140),
        specific_heat_capacity=Range(1200, 1400),
        thermal_conductivity=Range(0.25, 0.40),
        thermal_expansion=Range(40e-6, 80e-6),
    ),
}


def nylon(
    grade: Nylon = Nylon.PA12,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """Nylon (PA) as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to PA12.
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
        with_density(NYLON_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- PEEK --------------------------------------------------------------------
class Peek(Enum):
    MOLDED = auto()
    PRINTED = auto()


PEEK_MATERIALS: dict[Peek, PlasticMaterial] = {
    Peek.MOLDED: PlasticMaterial(
        # identity
        name="Peek_MOLDED",
        family="PEEK",
        # mechanical properties
        density=1300,
        elongation_at_break=Range(20, 100),
        hardness=Range(85, 90),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(3.5, 4.2),
        poisson_ratio=Range(0.38, 0.42),
        shear_modulus=Range(1.3, 1.6),
        shear_strength=Range(50, 75),
        tensile_strength=Range(90, 110),
        yield_strength=Range(90, 100),
        # thermal properties
        glass_transition_temperature=Range(143, 150),
        heat_deflection_temperature=Range(140, 160),
        max_service_temp=Range(240, 260),
        specific_heat_capacity=Range(1300, 1400),
        thermal_conductivity=Range(0.24, 0.29),
        thermal_expansion=Range(45e-6, 60e-6),
    ),
    Peek.PRINTED: PlasticMaterial(
        # identity
        name="Peek_PRINTED",
        family="PEEK",
        # mechanical properties
        density=1300,
        elongation_at_break=Range(5, 30),
        hardness=Range(85, 90),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(3.5, 4.2),
        poisson_ratio=Range(0.38, 0.42),
        shear_modulus=Range(1.3, 1.6),
        shear_strength=Range(45, 70),
        tensile_strength=Range(80, 120),
        yield_strength=Range(80, 105),
        # thermal properties
        glass_transition_temperature=Range(143, 150),
        heat_deflection_temperature=Range(140, 160),
        max_service_temp=Range(160, 250),
        specific_heat_capacity=Range(1300, 1400),
        thermal_conductivity=Range(0.24, 0.29),
        thermal_expansion=Range(45e-6, 60e-6),
    ),
}


def peek(
    grade: Peek = Peek.MOLDED,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """PEEK as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to moulded.
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
        with_density(PEEK_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- TPU ---------------------------------------------------------------------
class TPU(Enum):
    SHORE_95A = auto()
    SINTERED = auto()


TPU_MATERIALS: dict[TPU, PlasticMaterial] = {
    TPU.SHORE_95A: PlasticMaterial(
        # identity
        name="TPU_SHORE_95A",
        family="TPU",
        # mechanical properties
        density=1200,
        elongation_at_break=Range(300, 700),
        hardness=Range(93, 97),
        hardness_scale="Shore A",
        modulus_of_elasticity=Range(0.007, 0.10),
        poisson_ratio=Range(0.45, 0.49),
        shear_modulus=Range(0.002, 0.035),
        shear_strength=Range(10, 30),
        tensile_strength=Range(25, 55),
        yield_strength=NOT_SUITABLE,
        # thermal properties
        glass_transition_temperature=Range(-40, -20),
        heat_deflection_temperature=NOT_SUITABLE,
        max_service_temp=Range(70, 90),
        specific_heat_capacity=Range(1700, 1900),
        thermal_conductivity=Range(0.15, 0.25),
        thermal_expansion=Range(120e-6, 200e-6),
    ),
    TPU.SINTERED: PlasticMaterial(
        # identity
        name="TPU_SINTERED",
        family="TPU",
        # mechanical properties
        density=1200,
        elongation_at_break=Range(100, 400),
        hardness=Range(88, 92),
        hardness_scale="Shore A",
        modulus_of_elasticity=Range(0.02, 0.1),
        poisson_ratio=Range(0.45, 0.49),
        shear_modulus=Range(0.007, 0.03),
        shear_strength=Range(5, 20),
        tensile_strength=Range(10, 25),
        yield_strength=NOT_SUITABLE,
        # thermal properties
        glass_transition_temperature=Range(-40, -20),
        heat_deflection_temperature=NOT_SUITABLE,
        max_service_temp=Range(70, 90),
        specific_heat_capacity=Range(1700, 1900),
        thermal_conductivity=Range(0.15, 0.25),
        thermal_expansion=Range(120e-6, 200e-6),
    ),
}


def tpu(
    grade: TPU = TPU.SHORE_95A,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """TPU as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to Shore 95A.
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
        with_density(TPU_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- PC (polycarbonate) ------------------------------------------------------
class PC(Enum):
    GENERIC = auto()


PC_MATERIALS: dict[PC, PlasticMaterial] = {
    PC.GENERIC: PlasticMaterial(
        # identity
        name="PC_GENERIC",
        family="PC",
        transparent=True,
        # mechanical properties
        density=1200,
        elongation_at_break=Range(80, 130),
        hardness=Range(75, 85),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(2.2, 2.5),
        poisson_ratio=Range(0.37, 0.42),
        shear_modulus=Range(0.8, 0.95),
        shear_strength=Range(35, 50),
        tensile_strength=Range(55, 75),
        yield_strength=Range(55, 70),
        # thermal properties
        glass_transition_temperature=Range(145, 150),
        heat_deflection_temperature=Range(125, 140),
        max_service_temp=Range(115, 145),
        specific_heat_capacity=Range(1150, 1250),
        thermal_conductivity=Range(0.19, 0.22),
        thermal_expansion=Range(65e-6, 75e-6),
    ),
}


def pc(
    grade: PC = PC.GENERIC,
    color: Color | None = None,
    thickness_mm: float | None = None,
    opacity: float | None = None,
    roughness: float | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """Polycarbonate (PC) as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic.
        color: Base color for the part -- a build123d ``ColorLike``: a CSS3/palette
            name, a ``#rrggbb`` hex, a ``0xRRGGBB`` int, an RGB(A) tuple, or a
            ``Color``.
        thickness_mm: Pane thickness in mm; used for the transmissive look (the material
            is transparent).
        opacity: How see-through this part is, ``0.0`` (clear) to ``1.0`` (opaque);
            ``None`` keeps the clear look. Set it for a translucent part -- a milky
            white V-wheel on a CNC rail is roughly ``0.65``.
        roughness: Surface roughness, ``0.0`` (glossy) to ``1.0`` (matte / frosted);
            ``None`` keeps the factory value. Independent of ``opacity`` -- a molded
            V-wheel is glossy, an etched pane is rough.
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
        with_density(PC_MATERIALS[grade], density),
        finish,
        color=color,
        thickness_mm=thickness_mm,
        opacity=opacity,
        roughness=roughness,
        process=process,
    )


# --- PP (polypropylene) ------------------------------------------------------
class PP(Enum):
    GENERIC = auto()


PP_MATERIALS: dict[PP, PlasticMaterial] = {
    PP.GENERIC: PlasticMaterial(
        # identity
        name="PP_GENERIC",
        family="PP",
        # mechanical properties
        density=905,
        elongation_at_break=Range(10, 600),
        hardness=Range(70, 80),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(1.1, 1.8),
        poisson_ratio=Range(0.40, 0.45),
        shear_modulus=Range(0.4, 0.7),
        shear_strength=Range(15, 30),
        tensile_strength=Range(25, 40),
        yield_strength=Range(25, 38),
        # thermal properties
        glass_transition_temperature=Range(-20, -10),
        heat_deflection_temperature=Range(50, 65),
        max_service_temp=Range(80, 130),
        specific_heat_capacity=Range(1800, 2000),
        thermal_conductivity=Range(0.11, 0.27),
        thermal_expansion=Range(100e-6, 180e-6),
    ),
}


def pp(
    grade: PP = PP.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """Polypropylene (PP) as a ``FinishedMaterial``.

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
        with_density(PP_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- POM (acetal) ------------------------------------------------------------
class POM(Enum):
    GENERIC = auto()


POM_MATERIALS: dict[POM, PlasticMaterial] = {
    POM.GENERIC: PlasticMaterial(
        # identity
        name="POM_GENERIC",
        family="POM",
        # mechanical properties
        density=1410,
        elongation_at_break=Range(10, 45),
        hardness=Range(80, 90),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(2.8, 4.0),
        poisson_ratio=Range(0.35, 0.40),
        shear_modulus=Range(1.0, 1.4),
        shear_strength=Range(35, 55),
        tensile_strength=Range(60, 90),
        yield_strength=Range(60, 73),
        # thermal properties
        glass_transition_temperature=Range(-60, -50),
        heat_deflection_temperature=Range(90, 110),
        max_service_temp=Range(90, 105),
        specific_heat_capacity=Range(1400, 1500),
        thermal_conductivity=Range(0.30, 0.40),
        thermal_expansion=Range(80e-6, 140e-6),
    ),
}


def pom(
    grade: POM = POM.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """Acetal (POM) as a ``FinishedMaterial``.

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
        with_density(POM_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- PTFE --------------------------------------------------------------------
class PTFE(Enum):
    GENERIC = auto()


PTFE_MATERIALS: dict[PTFE, PlasticMaterial] = {
    PTFE.GENERIC: PlasticMaterial(
        # identity
        name="PTFE_GENERIC",
        family="PTFE",
        # mechanical properties
        density=2170,
        elongation_at_break=Range(200, 400),
        hardness=Range(50, 65),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(0.4, 0.75),
        poisson_ratio=Range(0.42, 0.47),
        shear_modulus=Range(0.15, 0.28),
        shear_strength=Range(10, 20),
        tensile_strength=Range(20, 35),
        yield_strength=Range(15, 25),
        # thermal properties
        glass_transition_temperature=NOT_SUITABLE,
        heat_deflection_temperature=Range(50, 80),
        max_service_temp=Range(250, 270),
        specific_heat_capacity=Range(1000, 1050),
        thermal_conductivity=Range(0.23, 0.27),
        thermal_expansion=Range(100e-6, 200e-6),
    ),
}


def ptfe(
    grade: PTFE = PTFE.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """PTFE as a ``FinishedMaterial``.

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
        with_density(PTFE_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- PMMA (acrylic) ----------------------------------------------------------
class PMMA(Enum):
    GENERIC = auto()


PMMA_MATERIALS: dict[PMMA, PlasticMaterial] = {
    PMMA.GENERIC: PlasticMaterial(
        # identity
        name="PMMA_GENERIC",
        family="PMMA",
        transparent=True,
        # mechanical properties
        density=1180,
        elongation_at_break=Range(2, 6),
        hardness=Range(85, 90),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(2.4, 3.3),
        poisson_ratio=Range(0.35, 0.40),
        shear_modulus=Range(0.9, 1.2),
        shear_strength=Range(30, 50),
        tensile_strength=Range(50, 83),
        yield_strength=Range(50, 80),
        # thermal properties
        glass_transition_temperature=Range(100, 110),
        heat_deflection_temperature=Range(85, 105),
        max_service_temp=Range(65, 80),
        specific_heat_capacity=Range(1400, 1500),
        thermal_conductivity=Range(0.17, 0.21),
        thermal_expansion=Range(60e-6, 90e-6),
    ),
}


def pmma(
    grade: PMMA = PMMA.GENERIC,
    color: Color | None = None,
    thickness_mm: float | None = None,
    opacity: float | None = None,
    roughness: float | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """Acrylic (PMMA) as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic.
        color: Base color for the part -- a build123d ``ColorLike``: a CSS3/palette
            name, a ``#rrggbb`` hex, a ``0xRRGGBB`` int, an RGB(A) tuple, or a
            ``Color``.
        thickness_mm: Pane thickness in mm; used for the transmissive look (the material
            is transparent).
        opacity: How see-through this part is, ``0.0`` (clear) to ``1.0`` (opaque);
            ``None`` keeps the clear look. Set it for a translucent / frosted part.
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
        with_density(PMMA_MATERIALS[grade], density),
        finish,
        color=color,
        thickness_mm=thickness_mm,
        opacity=opacity,
        roughness=roughness,
        process=process,
    )


# --- PE (polyethylene) -------------------------------------------------------
class PE(Enum):
    HDPE = auto()


PE_MATERIALS: dict[PE, PlasticMaterial] = {
    PE.HDPE: PlasticMaterial(
        # identity
        name="PE_HDPE",
        family="PE",
        # mechanical properties
        density=960,
        elongation_at_break=Range(100, 700),
        hardness=Range(55, 65),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(0.8, 1.3),
        poisson_ratio=Range(0.40, 0.46),
        shear_modulus=Range(0.3, 0.5),
        shear_strength=Range(12, 25),
        tensile_strength=Range(20, 35),
        yield_strength=Range(20, 31),
        # thermal properties
        glass_transition_temperature=Range(-120, -100),
        heat_deflection_temperature=Range(40, 55),
        max_service_temp=Range(60, 110),
        specific_heat_capacity=Range(1800, 2100),
        thermal_conductivity=Range(0.35, 0.51),
        thermal_expansion=Range(100e-6, 200e-6),
    ),
}


def pe(
    grade: PE = PE.HDPE,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """Polyethylene (PE) as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to HDPE.
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
        with_density(PE_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- Phenolic ----------------------------------------------------------------
class Phenolic(Enum):
    BAKELITE = auto()


PHENOLIC_MATERIALS: dict[Phenolic, PlasticMaterial] = {
    Phenolic.BAKELITE: PlasticMaterial(
        # identity
        name="Phenolic_BAKELITE",
        family="phenolic",
        # mechanical properties
        density=1300,
        elongation_at_break=Range(0.5, 2),
        hardness=Range(88, 95),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(5, 9),
        poisson_ratio=Range(0.30, 0.40),
        shear_modulus=Range(2.0, 3.5),
        shear_strength=Range(25, 45),
        tensile_strength=Range(40, 70),
        yield_strength=NOT_SUITABLE,
        # thermal properties
        glass_transition_temperature=Range(150, 200),
        heat_deflection_temperature=Range(150, 200),
        max_service_temp=Range(120, 180),
        specific_heat_capacity=Range(1200, 1600),
        thermal_conductivity=Range(0.15, 0.30),
        thermal_expansion=Range(30e-6, 50e-6),
    ),
}


def phenolic(
    grade: Phenolic = Phenolic.BAKELITE,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """Phenolic as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to Bakelite.
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
        with_density(PHENOLIC_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- Rubber ------------------------------------------------------------------
class Rubber(Enum):
    GENERIC = auto()


RUBBER_MATERIALS: dict[Rubber, PlasticMaterial] = {
    Rubber.GENERIC: PlasticMaterial(
        # identity
        name="Rubber_GENERIC",
        family="rubber",
        # mechanical properties
        density=1200,
        elongation_at_break=Range(100, 700),
        hardness=Range(40, 80),
        hardness_scale="Shore A",
        modulus_of_elasticity=Range(0.001, 0.01),
        poisson_ratio=Range(0.48, 0.50),
        shear_modulus=Range(0.0003, 0.003),
        shear_strength=Range(5, 15),
        tensile_strength=Range(10, 25),
        yield_strength=NOT_SUITABLE,
        # thermal properties
        glass_transition_temperature=Range(-70, -40),
        heat_deflection_temperature=NOT_SUITABLE,
        max_service_temp=Range(60, 100),
        specific_heat_capacity=Range(1800, 2000),
        thermal_conductivity=Range(0.13, 0.30),
        thermal_expansion=Range(100e-6, 200e-6),
    ),
}


def rubber(
    grade: Rubber = Rubber.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """Rubber as a ``FinishedMaterial``.

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
        with_density(RUBBER_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- PETG --------------------------------------------------------------------
class PETG(Enum):
    GENERIC = auto()
    CF = auto()


PETG_MATERIALS: dict[PETG, PlasticMaterial] = {
    PETG.GENERIC: PlasticMaterial(
        # identity
        name="PETG_GENERIC",
        family="PETG",
        # mechanical properties
        density=1270,
        elongation_at_break=Range(50, 120),
        hardness=Range(75, 82),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(2.0, 2.2),
        poisson_ratio=Range(0.38, 0.43),
        shear_modulus=Range(0.7, 0.85),
        shear_strength=Range(30, 40),
        tensile_strength=Range(45, 55),
        yield_strength=Range(45, 53),
        # thermal properties
        glass_transition_temperature=Range(75, 85),
        heat_deflection_temperature=Range(65, 75),
        max_service_temp=Range(60, 70),
        specific_heat_capacity=Range(1200, 1400),
        thermal_conductivity=Range(0.15, 0.25),
        thermal_expansion=Range(60e-6, 80e-6),
    ),
    PETG.CF: PlasticMaterial(
        # identity
        name="PETG_CF",
        family="PETG",
        # mechanical properties
        density=1320,
        elongation_at_break=Range(2, 6),
        hardness=Range(78, 85),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(3, 6),
        poisson_ratio=Range(0.37, 0.42),
        shear_modulus=Range(1.2, 2.3),
        shear_strength=Range(25, 45),
        tensile_strength=Range(40, 60),
        yield_strength=Range(40, 55),
        # thermal properties
        glass_transition_temperature=Range(75, 85),
        heat_deflection_temperature=Range(65, 80),
        max_service_temp=Range(60, 75),
        specific_heat_capacity=Range(1100, 1300),
        thermal_conductivity=Range(0.2, 0.4),
        thermal_expansion=Range(30e-6, 60e-6),
    ),
}


def petg(
    grade: PETG = PETG.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """PETG as a ``FinishedMaterial``.

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
        with_density(PETG_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- ASA ---------------------------------------------------------------------
class Asa(Enum):
    GENERIC = auto()


# Weathering-resistant amorphous thermoplastic, a UV-stable relative of ABS; the
# property bands are typical for the class.
ASA_MATERIALS: dict[Asa, PlasticMaterial] = {
    Asa.GENERIC: PlasticMaterial(
        # identity
        name="Asa_GENERIC",
        family="ASA",
        # mechanical properties
        density=1070,
        elongation_at_break=Range(10, 40),
        hardness=Range(70, 80),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(1.9, 2.6),
        poisson_ratio=Range(0.35, 0.40),
        shear_modulus=Range(0.7, 0.95),
        shear_strength=Range(25, 38),
        tensile_strength=Range(40, 55),
        yield_strength=Range(40, 50),
        # thermal properties
        glass_transition_temperature=Range(100, 110),
        heat_deflection_temperature=Range(85, 100),
        max_service_temp=Range(65, 85),
        specific_heat_capacity=Range(1300, 1500),
        thermal_conductivity=Range(0.15, 0.20),
        thermal_expansion=Range(80e-6, 100e-6),
    ),
}


def asa(
    grade: Asa = Asa.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """ASA as a ``FinishedMaterial``.

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
        with_density(ASA_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- PPS ---------------------------------------------------------------------
class PPS(Enum):
    CF = auto()


PPS_MATERIALS: dict[PPS, PlasticMaterial] = {
    PPS.CF: PlasticMaterial(
        # identity
        name="PPS_CF",
        family="PPS",
        # mechanical properties
        density=1400,
        elongation_at_break=Range(1, 3),
        hardness=Range(85, 92),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(7, 20),
        poisson_ratio=Range(0.36, 0.40),
        shear_modulus=Range(2.5, 7),
        shear_strength=Range(45, 90),
        tensile_strength=Range(80, 150),
        yield_strength=Range(80, 140),
        # thermal properties
        # Tg ~85-105 but HDT 200-270: reinforced semi-crystalline HDT tracks Tm (~280), not Tg
        glass_transition_temperature=Range(85, 105),
        heat_deflection_temperature=Range(200, 270),
        max_service_temp=Range(200, 240),
        specific_heat_capacity=Range(1000, 1200),
        thermal_conductivity=Range(0.25, 0.45),
        thermal_expansion=Range(20e-6, 50e-6),
    ),
}


def pps(
    grade: PPS = PPS.CF,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """PPS as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to carbon-filled.
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
        with_density(PPS_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- FR4 ---------------------------------------------------------------------
class FR4(Enum):
    GENERIC = auto()


FR4_MATERIALS: dict[FR4, PlasticMaterial] = {
    FR4.GENERIC: PlasticMaterial(
        # identity
        name="FR4_GENERIC",
        family="FR4",
        # mechanical properties
        density=1850,
        elongation_at_break=Range(1, 3),
        hardness=Range(85, 90),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(18, 24),
        # FR4's Poisson ratio is genuinely this low for the anisotropic laminate
        poisson_ratio=Range(0.11, 0.18),
        shear_modulus=Range(3, 7),
        shear_strength=Range(60, 120),
        tensile_strength=Range(260, 340),
        yield_strength=NOT_SUITABLE,
        # thermal properties
        glass_transition_temperature=Range(130, 180),
        heat_deflection_temperature=Range(130, 180),
        max_service_temp=Range(120, 160),
        specific_heat_capacity=Range(600, 900),
        thermal_conductivity=Range(0.25, 0.35),
        thermal_expansion=Range(12e-6, 18e-6),
    ),
}


def fr4(
    grade: FR4 = FR4.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """FR4 as a ``FinishedMaterial``.

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
        with_density(FR4_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- CFRP --------------------------------------------------------------------
class CFRP(Enum):
    PLATE = auto()


CFRP_MATERIALS: dict[CFRP, PlasticMaterial] = {
    CFRP.PLATE: PlasticMaterial(
        # identity
        name="CFRP_PLATE",
        family="CFRP",
        # mechanical properties
        density=1600,
        elongation_at_break=Range(0.5, 2),
        hardness=Range(85, 90),
        hardness_scale="Shore D",
        modulus_of_elasticity=Range(50, 180),
        poisson_ratio=Range(0.05, 0.15),
        shear_modulus=Range(3, 8),
        shear_strength=Range(30, 90),
        tensile_strength=Range(600, 2500),
        yield_strength=NOT_SUITABLE,
        # thermal properties
        glass_transition_temperature=Range(100, 200),
        heat_deflection_temperature=Range(100, 200),
        max_service_temp=Range(100, 180),
        specific_heat_capacity=Range(800, 1100),
        thermal_conductivity=Range(0.5, 10),
        thermal_expansion=Range(0, 10e-6),
    ),
}


def cfrp(
    grade: CFRP = CFRP.PLATE,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    """CFRP as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to plate.
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
        with_density(CFRP_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


ALL_PLASTICS = (
    *PLA_MATERIALS.values(),
    *ABS_MATERIALS.values(),
    *NYLON_MATERIALS.values(),
    *PEEK_MATERIALS.values(),
    *TPU_MATERIALS.values(),
    *PC_MATERIALS.values(),
    *PP_MATERIALS.values(),
    *POM_MATERIALS.values(),
    *PTFE_MATERIALS.values(),
    *PMMA_MATERIALS.values(),
    *PE_MATERIALS.values(),
    *PHENOLIC_MATERIALS.values(),
    *RUBBER_MATERIALS.values(),
    *PETG_MATERIALS.values(),
    *ASA_MATERIALS.values(),
    *PPS_MATERIALS.values(),
    *FR4_MATERIALS.values(),
    *CFRP_MATERIALS.values(),
)


def custom_plastic(
    name: str,
    density: float,
    *,
    family: str = "PLA",
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
) -> FinishedMaterial[PlasticMaterial]:
    """Define a custom plastic and return it as a ``FinishedMaterial``.

    Each property value may be a ``Range``, a bare number (an exact value, ``min ==
    max``), or ``None`` (missing); ``NOT_SUITABLE`` marks a property that does not
    apply. The property keyword args are the ``PlasticMaterial`` fields.

    Args:
        name: Identifier for the material.
        density: Single representative density (kg/m³).
        family: PBR look key (e.g. ``"ABS"``); an unknown key falls back per the PBR
            bridge. Defaults to ``"PLA"``.
        transparent: Intrinsic see-through flag; set for a transmissive plastic (uses
            ``thickness_mm``). Default ``False``.
        hardness_scale: Scale for ``hardness`` (``"Shore D"`` / ``"Shore A"``).
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
        A ``FinishedMaterial`` wrapping the custom plastic.
    """
    return FinishedMaterial(
        PlasticMaterial(
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
    print(f"plastics: {len(ALL_PLASTICS)}")
    print()
    print(PLA_MATERIALS[PLA.GENERIC])
    print(PC_MATERIALS[PC.GENERIC])
    print(TPU_MATERIALS[TPU.SHORE_95A])
