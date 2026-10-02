"""Typical-value property ranges for metals.

A ``MetalMaterial`` holds a single representative ``density`` plus min-max ``Range``
bands for each mechanical/thermal property, capturing the typical spread across temper,
product form and process. On top of the shared solid-material fields, metals add
``yield_strength``, ``shear_strength``, ``hardness`` (read on its ``hardness_scale`` --
HB / HRC / HV) and a ``melting_temperature``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, ClassVar

from ..finished import FinishedMaterial, FinishSpec
from ..processes import ProcessSpec
from ..core import Range, RangeInput, SolidMaterial, as_range, with_density

if TYPE_CHECKING:
    from threejs_materials import PbrProperties


@dataclass(frozen=True, kw_only=True)
class MetalMaterial(SolidMaterial):
    """A metal: the shared solid ranges (from ``SolidMaterial``) plus yield,
    shear strength, hardness (HB/HRC/HV), and a melting range.

    ``family`` is the PBR/identity key; metals are opaque (``transparent`` False)
    and have no ``color`` -- a metal's color comes from a finish.
    """

    category: ClassVar[str] = "metal"
    yield_strength: Range | None  # MPa
    shear_strength: Range | None  # MPa
    hardness: Range | None  # on the `hardness_scale` scale
    hardness_scale: str  # "HB", "HRC", "HV", ...
    melting_temperature: Range | None  # °C


# --- Aluminum ---------------------------------------------------------------
class Alu(Enum):
    G6061_T6 = auto()
    G7075_T6 = auto()
    G5052_H32 = auto()
    G2A12_T4 = auto()
    ALSI10MG_AS_BUILT = auto()
    G2024_AEROSPACE = auto()


ALU_MATERIALS: dict[Alu, MetalMaterial] = {
    Alu.G6061_T6: MetalMaterial(
        # identity
        name="Alu_G6061_T6",
        family="aluminum",
        # mechanical properties
        density=2700,
        hardness=Range(85, 100),
        hardness_scale="HB",
        modulus_of_elasticity=Range(66, 70),
        poisson_ratio=Range(0.32, 0.35),
        shear_modulus=Range(25, 28),
        shear_strength=Range(200, 210),
        tensile_strength=Range(290, 320),
        yield_strength=Range(240, 280),
        # thermal properties
        max_service_temp=Range(80, 120),
        melting_temperature=Range(570, 660),
        specific_heat_capacity=Range(875, 950),
        thermal_conductivity=Range(130, 180),
        thermal_expansion=Range(22e-6, 24e-6),
    ),
    Alu.G7075_T6: MetalMaterial(
        # identity
        name="Alu_G7075_T6",
        family="aluminum",
        # mechanical properties
        density=2810,
        hardness=Range(135, 160),
        hardness_scale="HB",
        modulus_of_elasticity=Range(68, 72),
        poisson_ratio=Range(0.32, 0.35),
        shear_modulus=Range(25, 28),
        shear_strength=Range(330, 350),
        tensile_strength=Range(540, 600),
        yield_strength=Range(480, 510),
        # thermal properties
        max_service_temp=Range(80, 120),
        melting_temperature=Range(480, 640),
        specific_heat_capacity=Range(875, 950),
        thermal_conductivity=Range(130, 180),
        thermal_expansion=Range(22e-6, 24e-6),
    ),
    Alu.G5052_H32: MetalMaterial(
        # identity
        name="Alu_G5052_H32",
        family="aluminum",
        # mechanical properties
        density=2680,
        hardness=Range(60, 80),
        hardness_scale="HB",
        modulus_of_elasticity=Range(68, 72),
        poisson_ratio=Range(0.32, 0.35),
        shear_modulus=Range(25, 28),
        shear_strength=Range(120, 160),
        tensile_strength=Range(215, 250),
        yield_strength=Range(160, 195),
        # thermal properties
        max_service_temp=Range(80, 120),
        melting_temperature=Range(570, 660),
        specific_heat_capacity=Range(875, 950),
        thermal_conductivity=Range(130, 180),
        thermal_expansion=Range(22e-6, 24e-6),
    ),
    Alu.G2A12_T4: MetalMaterial(
        # identity
        name="Alu_G2A12_T4",
        family="aluminum",
        # mechanical properties
        density=2800,
        hardness=Range(95, 120),
        hardness_scale="HB",
        modulus_of_elasticity=Range(68, 72),
        poisson_ratio=Range(0.32, 0.35),
        shear_modulus=Range(25, 28),
        shear_strength=Range(240, 310),
        tensile_strength=Range(430, 480),
        yield_strength=Range(300, 340),
        # thermal properties
        max_service_temp=Range(80, 120),
        melting_temperature=Range(570, 660),
        specific_heat_capacity=Range(875, 950),
        thermal_conductivity=Range(120, 190),
        thermal_expansion=Range(22e-6, 24e-6),
    ),
    Alu.ALSI10MG_AS_BUILT: MetalMaterial(
        # identity
        name="Alu_ALSI10MG_AS_BUILT",
        family="aluminum",
        # mechanical properties
        density=2670,
        hardness=Range(80, 110),
        hardness_scale="HB",
        modulus_of_elasticity=Range(65, 72),
        poisson_ratio=Range(0.32, 0.35),
        shear_modulus=Range(25, 28),
        shear_strength=Range(140, 215),
        tensile_strength=Range(250, 330),
        yield_strength=Range(160, 250),
        # thermal properties
        max_service_temp=Range(80, 150),
        melting_temperature=Range(570, 600),
        specific_heat_capacity=Range(875, 950),
        thermal_conductivity=Range(100, 150),
        thermal_expansion=Range(20e-6, 22e-6),
    ),
    Alu.G2024_AEROSPACE: MetalMaterial(
        # identity
        name="Alu_G2024_AEROSPACE",
        family="aluminum",
        # mechanical properties
        density=2780,
        hardness=Range(95, 120),
        hardness_scale="HB",
        modulus_of_elasticity=Range(70, 73),
        poisson_ratio=Range(0.32, 0.35),
        shear_modulus=Range(26, 28),
        shear_strength=Range(230, 280),
        tensile_strength=Range(420, 470),
        yield_strength=Range(260, 320),
        # thermal properties
        max_service_temp=Range(80, 120),
        melting_temperature=Range(500, 650),
        specific_heat_capacity=Range(875, 950),
        thermal_conductivity=Range(120, 130),
        thermal_expansion=Range(21e-6, 24e-6),
    ),
}


def aluminum(
    grade: Alu = Alu.G6061_T6,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[MetalMaterial]:
    """Aluminum as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to 6061-T6.
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
        with_density(ALU_MATERIALS[grade], density),
        finish,
        process=process,
    )


# --- Stainless steel ---------------------------------------------------------
class Stainless(Enum):
    G304_ANNEALED = auto()
    G316L_ANNEALED = auto()
    G316L_AS_BUILT = auto()
    G303_ANNEALED = auto()
    G430_ANNEALED = auto()
    G430_COLD_WORKED = auto()
    G201_ANNEALED = auto()


STAINLESS_MATERIALS: dict[Stainless, MetalMaterial] = {
    Stainless.G304_ANNEALED: MetalMaterial(
        # identity
        name="Stainless_G304_ANNEALED",
        family="stainless",
        # mechanical properties
        density=7930,
        hardness=Range(150, 200),
        hardness_scale="HB",
        modulus_of_elasticity=Range(190, 200),
        poisson_ratio=Range(0.29, 0.31),
        shear_modulus=Range(75, 82),
        shear_strength=Range(280, 350),
        tensile_strength=Range(515, 620),
        yield_strength=Range(205, 240),
        # thermal properties
        max_service_temp=Range(400, 600),
        melting_temperature=Range(1400, 1450),
        specific_heat_capacity=Range(480, 500),
        thermal_conductivity=Range(14, 17),
        thermal_expansion=Range(16e-6, 18e-6),
    ),
    Stainless.G316L_ANNEALED: MetalMaterial(
        # identity
        name="Stainless_G316L_ANNEALED",
        family="stainless",
        # mechanical properties
        density=8000,
        hardness=Range(150, 200),
        hardness_scale="HB",
        modulus_of_elasticity=Range(190, 200),
        poisson_ratio=Range(0.29, 0.31),
        shear_modulus=Range(75, 82),
        shear_strength=Range(280, 350),
        tensile_strength=Range(480, 620),
        yield_strength=Range(170, 310),
        # thermal properties
        max_service_temp=Range(400, 600),
        melting_temperature=Range(1375, 1450),
        specific_heat_capacity=Range(480, 500),
        thermal_conductivity=Range(14, 17),
        thermal_expansion=Range(16e-6, 18e-6),
    ),
    Stainless.G316L_AS_BUILT: MetalMaterial(
        # identity
        name="Stainless_G316L_AS_BUILT",
        family="stainless",
        # mechanical properties
        density=7990,
        hardness=Range(200, 250),
        hardness_scale="HB",
        modulus_of_elasticity=Range(185, 200),
        poisson_ratio=Range(0.29, 0.31),
        shear_modulus=Range(75, 82),
        shear_strength=Range(330, 420),
        tensile_strength=Range(550, 700),
        yield_strength=Range(450, 550),
        # thermal properties
        max_service_temp=Range(400, 600),
        melting_temperature=Range(1375, 1450),
        specific_heat_capacity=Range(480, 500),
        thermal_conductivity=Range(14, 16),
        thermal_expansion=Range(16e-6, 18e-6),
    ),
    Stainless.G303_ANNEALED: MetalMaterial(
        # identity
        name="Stainless_G303_ANNEALED",
        family="stainless",
        # mechanical properties
        density=8030,
        hardness=Range(150, 200),
        hardness_scale="HB",
        modulus_of_elasticity=Range(190, 200),
        poisson_ratio=Range(0.29, 0.31),
        shear_modulus=Range(75, 82),
        shear_strength=Range(275, 360),
        tensile_strength=Range(500, 625),
        yield_strength=Range(205, 290),
        # thermal properties
        max_service_temp=Range(400, 600),
        melting_temperature=Range(1400, 1450),
        specific_heat_capacity=Range(480, 500),
        thermal_conductivity=Range(14, 17),
        thermal_expansion=Range(16e-6, 18e-6),
    ),
    Stainless.G430_ANNEALED: MetalMaterial(
        # identity
        name="Stainless_G430_ANNEALED",
        family="stainless",
        # mechanical properties
        density=7750,
        hardness=Range(150, 190),
        hardness_scale="HB",
        modulus_of_elasticity=Range(190, 205),
        poisson_ratio=Range(0.27, 0.3),
        shear_modulus=Range(75, 82),
        shear_strength=Range(250, 300),
        tensile_strength=Range(450, 500),
        yield_strength=Range(275, 310),
        # thermal properties
        max_service_temp=Range(400, 600),
        melting_temperature=Range(1425, 1510),
        specific_heat_capacity=Range(480, 500),
        thermal_conductivity=Range(25, 30),
        thermal_expansion=Range(11e-6, 12e-6),
    ),
    Stainless.G430_COLD_WORKED: MetalMaterial(
        # identity
        name="Stainless_G430_COLD_WORKED",
        family="stainless",
        # mechanical properties
        density=7750,
        hardness=Range(185, 230),
        hardness_scale="HB",
        modulus_of_elasticity=Range(190, 205),
        poisson_ratio=Range(0.27, 0.3),
        shear_modulus=Range(75, 82),
        shear_strength=Range(300, 400),
        tensile_strength=Range(500, 650),
        yield_strength=Range(350, 550),
        # thermal properties
        max_service_temp=Range(400, 600),
        melting_temperature=Range(1425, 1510),
        specific_heat_capacity=Range(480, 500),
        thermal_conductivity=Range(25, 30),
        thermal_expansion=Range(11e-6, 12e-6),
    ),
    Stainless.G201_ANNEALED: MetalMaterial(
        # identity
        name="Stainless_G201_ANNEALED",
        family="stainless",
        # mechanical properties
        density=7860,
        hardness=Range(180, 230),
        hardness_scale="HB",
        modulus_of_elasticity=Range(190, 200),
        poisson_ratio=Range(0.27, 0.31),
        shear_modulus=Range(75, 82),
        shear_strength=Range(380, 515),
        tensile_strength=Range(600, 760),
        yield_strength=Range(275, 450),
        # thermal properties
        max_service_temp=Range(400, 600),
        melting_temperature=Range(1400, 1450),
        specific_heat_capacity=Range(480, 500),
        thermal_conductivity=Range(14, 16),
        thermal_expansion=Range(16e-6, 18e-6),
    ),
}


def stainless(
    grade: Stainless = Stainless.G304_ANNEALED,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[MetalMaterial]:
    """Stainless steel as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to 304 annealed.
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
        with_density(STAINLESS_MATERIALS[grade], density),
        finish,
        process=process,
    )


# --- Mild steel --------------------------------------------------------------
class MildSteel(Enum):
    PLAIN_CARBON_GENERIC = auto()
    G1018_COLD_DRAWN = auto()
    G1045_COLD_DRAWN = auto()
    GA36_HOT_ROLLED = auto()


MILD_STEEL_MATERIALS: dict[MildSteel, MetalMaterial] = {
    # Generic plain (low)-carbon steel -- deliberately wide bands that bracket the common
    # "Plain Carbon Steel" reference (SolidWorks default: E 210, yield 220, tensile 400,
    # density 7800). shear_strength is a derived estimate.
    MildSteel.PLAIN_CARBON_GENERIC: MetalMaterial(
        # identity
        name="MildSteel_PLAIN_CARBON_GENERIC",
        family="mild_steel",
        # mechanical properties
        density=7800,
        hardness=Range(110, 200),
        hardness_scale="HB",
        modulus_of_elasticity=Range(195, 210),
        poisson_ratio=Range(0.27, 0.31),
        shear_modulus=Range(75, 82),
        shear_strength=Range(220, 350),
        tensile_strength=Range(350, 600),
        yield_strength=Range(200, 400),
        # thermal properties
        max_service_temp=Range(200, 500),
        melting_temperature=Range(1450, 1530),
        specific_heat_capacity=Range(440, 500),
        thermal_conductivity=Range(40, 60),
        thermal_expansion=Range(11e-6, 13e-6),
    ),
    MildSteel.G1018_COLD_DRAWN: MetalMaterial(
        # identity
        name="MildSteel_G1018_COLD_DRAWN",
        family="mild_steel",
        # mechanical properties
        density=7850,
        hardness=Range(120, 160),
        hardness_scale="HB",
        modulus_of_elasticity=Range(200, 210),
        poisson_ratio=Range(0.28, 0.3),
        shear_modulus=Range(80, 81),
        shear_strength=Range(250, 275),
        tensile_strength=Range(440, 480),
        yield_strength=Range(345, 410),
        # thermal properties
        max_service_temp=Range(200, 500),
        melting_temperature=Range(1450, 1530),
        specific_heat_capacity=Range(460, 490),
        thermal_conductivity=Range(45, 55),
        thermal_expansion=Range(11e-6, 13e-6),
    ),
    MildSteel.G1045_COLD_DRAWN: MetalMaterial(
        # identity
        name="MildSteel_G1045_COLD_DRAWN",
        family="mild_steel",
        # mechanical properties
        density=7850,
        hardness=Range(170, 210),
        hardness_scale="HB",
        modulus_of_elasticity=Range(200, 210),
        poisson_ratio=Range(0.28, 0.3),
        shear_modulus=Range(80, 81),
        shear_strength=Range(355, 395),
        tensile_strength=Range(620, 690),
        yield_strength=Range(480, 600),
        # thermal properties
        max_service_temp=Range(200, 500),
        melting_temperature=Range(1450, 1530),
        specific_heat_capacity=Range(460, 490),
        thermal_conductivity=Range(45, 55),
        thermal_expansion=Range(11e-6, 13e-6),
    ),
    MildSteel.GA36_HOT_ROLLED: MetalMaterial(
        # identity
        name="MildSteel_GA36_HOT_ROLLED",
        family="mild_steel",
        # mechanical properties
        density=7850,
        hardness=Range(120, 180),
        hardness_scale="HB",
        modulus_of_elasticity=Range(200, 210),
        poisson_ratio=Range(0.28, 0.3),
        shear_modulus=Range(79, 81),
        shear_strength=Range(230, 315),
        tensile_strength=Range(400, 550),
        yield_strength=Range(250, 350),
        # thermal properties
        max_service_temp=Range(200, 500),
        melting_temperature=Range(1450, 1530),
        specific_heat_capacity=Range(460, 490),
        thermal_conductivity=Range(45, 55),
        thermal_expansion=Range(11e-6, 13e-6),
    ),
}


def mild_steel(
    grade: MildSteel = MildSteel.PLAIN_CARBON_GENERIC,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[MetalMaterial]:
    """Mild steel as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic plain (low)-carbon steel.
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
        with_density(MILD_STEEL_MATERIALS[grade], density),
        finish,
        process=process,
    )


# --- Alloy steel -------------------------------------------------------------
class AlloySteel(Enum):
    G4140_QUENCHED_TEMPERED = auto()
    G4340_QUENCHED_TEMPERED = auto()
    G1215_COLD_DRAWN = auto()
    G52100_HARDENED_LOW_TEMPERED = auto()


ALLOY_STEEL_MATERIALS: dict[AlloySteel, MetalMaterial] = {
    AlloySteel.G4140_QUENCHED_TEMPERED: MetalMaterial(
        # identity
        name="AlloySteel_G4140_QUENCHED_TEMPERED",
        family="alloy_steel",
        # mechanical properties
        density=7850,
        hardness=Range(28, 40),
        hardness_scale="HRC",
        modulus_of_elasticity=Range(200, 210),
        poisson_ratio=Range(0.28, 0.3),
        shear_modulus=Range(80, 81),
        shear_strength=Range(455, 630),
        tensile_strength=Range(800, 1150),
        yield_strength=Range(650, 950),
        # thermal properties
        max_service_temp=Range(200, 500),
        melting_temperature=Range(1450, 1530),
        specific_heat_capacity=Range(460, 490),
        thermal_conductivity=Range(30, 45),
        thermal_expansion=Range(11e-6, 13e-6),
    ),
    AlloySteel.G4340_QUENCHED_TEMPERED: MetalMaterial(
        # identity
        name="AlloySteel_G4340_QUENCHED_TEMPERED",
        family="alloy_steel",
        # mechanical properties
        density=7850,
        hardness=Range(35, 45),
        hardness_scale="HRC",
        modulus_of_elasticity=Range(200, 215),
        poisson_ratio=Range(0.28, 0.3),
        shear_modulus=Range(80, 81),
        shear_strength=Range(560, 780),
        tensile_strength=Range(980, 1200),
        yield_strength=Range(850, 1080),
        # thermal properties
        max_service_temp=Range(200, 500),
        melting_temperature=Range(1450, 1530),
        specific_heat_capacity=Range(460, 490),
        thermal_conductivity=Range(30, 45),
        thermal_expansion=Range(11e-6, 13e-6),
    ),
    AlloySteel.G1215_COLD_DRAWN: MetalMaterial(
        # identity
        name="AlloySteel_G1215_COLD_DRAWN",
        family="alloy_steel",
        # mechanical properties
        density=7850,
        hardness=Range(120, 160),
        hardness_scale="HB",
        modulus_of_elasticity=Range(200, 210),
        poisson_ratio=Range(0.28, 0.3),
        shear_modulus=Range(80, 81),
        shear_strength=Range(250, 315),
        tensile_strength=Range(440, 550),
        yield_strength=Range(340, 420),
        # thermal properties
        max_service_temp=Range(200, 500),
        melting_temperature=Range(1450, 1530),
        specific_heat_capacity=Range(460, 490),
        thermal_conductivity=Range(45, 55),
        thermal_expansion=Range(11e-6, 13e-6),
    ),
    AlloySteel.G52100_HARDENED_LOW_TEMPERED: MetalMaterial(
        # identity
        name="AlloySteel.G52100_HARDENED_LOW_TEMPERED",
        family="alloy_steel",
        # mechanical properties
        density=7810,
        hardness=Range(60, 65),
        hardness_scale="HRC",
        modulus_of_elasticity=Range(190, 210),
        poisson_ratio=Range(0.27, 0.30),
        shear_modulus=Range(80, 80),
        shear_strength=Range(1300, 1400),
        tensile_strength=Range(2200, 2300),
        yield_strength=Range(1700, 2000),
        # thermal properties
        max_service_temp=Range(120, 150),
        melting_temperature=Range(1420, 1460),
        specific_heat_capacity=Range(460, 480),
        thermal_conductivity=Range(40, 47),
        thermal_expansion=Range(11.9e-6, 12e-6),
    ),
}


def alloy_steel(
    grade: AlloySteel = AlloySteel.G4140_QUENCHED_TEMPERED,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[MetalMaterial]:
    """Alloy steel as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to 4140 quenched & tempered.
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
        with_density(ALLOY_STEEL_MATERIALS[grade], density),
        finish,
        process=process,
    )


# --- Spring steel ------------------------------------------------------------
class SpringSteel(Enum):
    GENERIC_QUENCHED_TEMPERED = auto()


SPRING_STEEL_MATERIALS: dict[SpringSteel, MetalMaterial] = {
    SpringSteel.GENERIC_QUENCHED_TEMPERED: MetalMaterial(
        # identity
        name="SpringSteel_GENERIC_QUENCHED_TEMPERED",
        family="spring_steel",
        # mechanical properties
        density=7850,
        hardness=Range(40, 55),
        hardness_scale="HRC",
        modulus_of_elasticity=Range(200, 210),
        poisson_ratio=Range(0.28, 0.3),
        shear_modulus=Range(80, 81),
        shear_strength=Range(570, 855),
        tensile_strength=Range(980, 1500),
        yield_strength=Range(780, 1350),
        # thermal properties
        max_service_temp=Range(150, 300),
        melting_temperature=Range(1450, 1530),
        specific_heat_capacity=Range(460, 490),
        thermal_conductivity=Range(30, 45),
        thermal_expansion=Range(11e-6, 13e-6),
    ),
}


def spring_steel(
    grade: SpringSteel = SpringSteel.GENERIC_QUENCHED_TEMPERED,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[MetalMaterial]:
    """Spring steel as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic quenched & tempered.
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
        with_density(SPRING_STEEL_MATERIALS[grade], density),
        finish,
        process=process,
    )


# --- Tool steel --------------------------------------------------------------
class ToolSteel(Enum):
    D2_HARDENED = auto()
    A2_HARDENED = auto()
    O1_HARDENED = auto()
    A3_HARDENED = auto()
    S7_HARDENED = auto()
    H13_HARDENED = auto()
    GENERIC_AS_BUILT = auto()


TOOL_STEEL_MATERIALS: dict[ToolSteel, MetalMaterial] = {
    ToolSteel.D2_HARDENED: MetalMaterial(
        # identity
        name="ToolSteel_D2_HARDENED",
        family="tool_steel",
        # mechanical properties
        density=7700,
        hardness=Range(55, 62),
        hardness_scale="HRC",
        modulus_of_elasticity=Range(200, 215),
        poisson_ratio=Range(0.27, 0.3),
        shear_modulus=Range(80, 83),
        shear_strength=Range(855, 1140),
        tensile_strength=Range(1500, 2200),
        yield_strength=Range(1300, 2000),
        # thermal properties
        max_service_temp=Range(200, 350),
        melting_temperature=Range(1450, 1520),
        specific_heat_capacity=Range(460, 500),
        thermal_conductivity=Range(18, 32),
        thermal_expansion=Range(12e-6, 13e-6),
    ),
    ToolSteel.A2_HARDENED: MetalMaterial(
        # identity
        name="ToolSteel_A2_HARDENED",
        family="tool_steel",
        # mechanical properties
        density=7860,
        hardness=Range(55, 60),
        hardness_scale="HRC",
        modulus_of_elasticity=Range(200, 220),
        poisson_ratio=Range(0.27, 0.3),
        shear_modulus=Range(80, 83),
        shear_strength=Range(800, 1085),
        tensile_strength=Range(1400, 1900),
        yield_strength=Range(1200, 1700),
        # thermal properties
        max_service_temp=Range(200, 350),
        melting_temperature=Range(1450, 1520),
        specific_heat_capacity=Range(460, 500),
        thermal_conductivity=Range(20, 28),
        thermal_expansion=Range(12e-6, 13e-6),
    ),
    ToolSteel.O1_HARDENED: MetalMaterial(
        # identity
        name="ToolSteel_O1_HARDENED",
        family="tool_steel",
        # mechanical properties
        density=7830,
        hardness=Range(55, 60),
        hardness_scale="HRC",
        modulus_of_elasticity=Range(200, 220),
        poisson_ratio=Range(0.27, 0.3),
        shear_modulus=Range(80, 83),
        shear_strength=Range(800, 1085),
        tensile_strength=Range(1400, 1900),
        yield_strength=Range(1200, 1700),
        # thermal properties
        max_service_temp=Range(200, 350),
        melting_temperature=Range(1450, 1520),
        specific_heat_capacity=Range(460, 500),
        thermal_conductivity=Range(30, 40),
        thermal_expansion=Range(12e-6, 13e-6),
    ),
    ToolSteel.A3_HARDENED: MetalMaterial(
        # identity
        name="ToolSteel_A3_HARDENED",
        family="tool_steel",
        # mechanical properties
        density=7860,
        hardness=Range(55, 60),
        hardness_scale="HRC",
        modulus_of_elasticity=Range(200, 215),
        poisson_ratio=Range(0.27, 0.3),
        shear_modulus=Range(80, 83),
        shear_strength=Range(800, 1085),
        tensile_strength=Range(1400, 1900),
        yield_strength=Range(1200, 1700),
        # thermal properties
        max_service_temp=Range(200, 350),
        melting_temperature=Range(1450, 1520),
        specific_heat_capacity=Range(460, 500),
        thermal_conductivity=Range(32, 40),
        thermal_expansion=Range(12e-6, 13e-6),
    ),
    ToolSteel.S7_HARDENED: MetalMaterial(
        # identity
        name="ToolSteel_S7_HARDENED",
        family="tool_steel",
        # mechanical properties
        density=7830,
        hardness=Range(50, 56),
        hardness_scale="HRC",
        modulus_of_elasticity=Range(200, 215),
        poisson_ratio=Range(0.27, 0.3),
        shear_modulus=Range(80, 83),
        shear_strength=Range(800, 1025),
        tensile_strength=Range(1400, 1900),
        yield_strength=Range(1200, 1700),
        # thermal properties
        max_service_temp=Range(200, 350),
        melting_temperature=Range(1450, 1520),
        specific_heat_capacity=Range(460, 500),
        thermal_conductivity=Range(30, 40),
        thermal_expansion=Range(12e-6, 13e-6),
    ),
    ToolSteel.H13_HARDENED: MetalMaterial(
        # identity
        name="ToolSteel_H13_HARDENED",
        family="tool_steel",
        # mechanical properties
        density=7800,
        hardness=Range(44, 52),
        hardness_scale="HRC",
        modulus_of_elasticity=Range(200, 215),
        poisson_ratio=Range(0.27, 0.3),
        shear_modulus=Range(80, 83),
        shear_strength=Range(740, 912),
        tensile_strength=Range(1300, 1600),
        yield_strength=Range(1100, 1500),
        # thermal properties
        max_service_temp=Range(500, 650),
        melting_temperature=Range(1450, 1520),
        specific_heat_capacity=Range(460, 500),
        thermal_conductivity=Range(22, 28),
        thermal_expansion=Range(12e-6, 13e-6),
    ),
    ToolSteel.GENERIC_AS_BUILT: MetalMaterial(
        # identity
        name="ToolSteel_GENERIC_AS_BUILT",
        family="tool_steel",
        # mechanical properties
        density=7800,
        hardness=Range(45, 60),
        hardness_scale="HRC",
        modulus_of_elasticity=Range(200, 215),
        poisson_ratio=Range(0.27, 0.3),
        shear_modulus=Range(80, 83),
        shear_strength=Range(570, 800),
        tensile_strength=Range(1000, 1400),
        yield_strength=Range(850, 1300),
        # thermal properties
        max_service_temp=Range(200, 350),
        melting_temperature=Range(1450, 1520),
        specific_heat_capacity=Range(460, 500),
        thermal_conductivity=Range(18, 28),
        thermal_expansion=Range(12e-6, 13e-6),
    ),
}


def tool_steel(
    grade: ToolSteel = ToolSteel.D2_HARDENED,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[MetalMaterial]:
    """Tool steel as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to D2 hardened.
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
        with_density(TOOL_STEEL_MATERIALS[grade], density),
        finish,
        process=process,
    )


# --- Titanium ----------------------------------------------------------------
class Titanium(Enum):
    GR5_ANNEALED = auto()
    TC4_AS_BUILT = auto()


TITANIUM_MATERIALS: dict[Titanium, MetalMaterial] = {
    Titanium.GR5_ANNEALED: MetalMaterial(
        # identity
        name="Titanium_GR5_ANNEALED",
        family="titanium",
        # mechanical properties
        density=4430,
        hardness=Range(30, 38),
        hardness_scale="HRC",
        modulus_of_elasticity=Range(110, 120),
        poisson_ratio=Range(0.29, 0.32),
        shear_modulus=Range(42, 45),
        shear_strength=Range(500, 570),
        tensile_strength=Range(900, 1000),
        yield_strength=Range(830, 960),
        # thermal properties
        max_service_temp=Range(300, 400),
        melting_temperature=Range(1600, 1660),
        specific_heat_capacity=Range(520, 560),
        thermal_conductivity=Range(6, 9),
        thermal_expansion=Range(8.5e-6, 9.5e-6),
    ),
    Titanium.TC4_AS_BUILT: MetalMaterial(
        # identity
        name="Titanium_TC4_AS_BUILT",
        family="titanium",
        # mechanical properties
        density=4430,
        hardness=Range(32, 40),
        hardness_scale="HRC",
        modulus_of_elasticity=Range(110, 120),
        poisson_ratio=Range(0.29, 0.32),
        shear_modulus=Range(42, 45),
        shear_strength=Range(525, 660),
        tensile_strength=Range(950, 1100),
        yield_strength=Range(860, 1000),
        # thermal properties
        max_service_temp=Range(250, 350),
        melting_temperature=Range(1600, 1660),
        specific_heat_capacity=Range(520, 560),
        thermal_conductivity=Range(6, 9),
        thermal_expansion=Range(8.5e-6, 9.5e-6),
    ),
}


def titanium(
    grade: Titanium = Titanium.GR5_ANNEALED,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[MetalMaterial]:
    """Titanium as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to Grade 5 annealed.
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
        with_density(TITANIUM_MATERIALS[grade], density),
        finish,
        process=process,
    )


# --- Brass -------------------------------------------------------------------
class Brass(Enum):
    C360_HALF_HARD = auto()
    C360_SOFT_ANNEALED = auto()


BRASS_MATERIALS: dict[Brass, MetalMaterial] = {
    Brass.C360_HALF_HARD: MetalMaterial(
        # identity
        name="Brass_C360_HALF_HARD",
        family="brass",
        # mechanical properties
        density=8500,
        hardness=Range(90, 120),
        hardness_scale="HB",
        modulus_of_elasticity=Range(100, 110),
        poisson_ratio=Range(0.32, 0.35),
        shear_modulus=Range(37, 40),
        shear_strength=Range(210, 270),
        tensile_strength=Range(380, 450),
        yield_strength=Range(200, 250),
        # thermal properties
        max_service_temp=Range(150, 250),
        melting_temperature=Range(880, 950),
        specific_heat_capacity=Range(380, 390),
        thermal_conductivity=Range(110, 130),
        thermal_expansion=Range(19e-6, 21e-6),
    ),
    Brass.C360_SOFT_ANNEALED: MetalMaterial(
        # identity
        name="Brass_C360_SOFT_ANNEALED",
        family="brass",
        # mechanical properties
        density=8500,
        hardness=Range(50, 75),
        hardness_scale="HB",
        modulus_of_elasticity=Range(97, 110),
        poisson_ratio=Range(0.32, 0.35),
        shear_modulus=Range(37, 40),
        shear_strength=Range(180, 230),
        tensile_strength=Range(300, 360),
        yield_strength=Range(100, 160),
        # thermal properties
        max_service_temp=Range(150, 250),
        melting_temperature=Range(880, 950),
        specific_heat_capacity=Range(380, 390),
        thermal_conductivity=Range(110, 130),
        thermal_expansion=Range(19e-6, 21e-6),
    ),
}


def brass(
    grade: Brass = Brass.C360_HALF_HARD,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[MetalMaterial]:
    """Brass as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to C360 half-hard.
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
        with_density(BRASS_MATERIALS[grade], density),
        finish,
        process=process,
    )


# --- Copper ------------------------------------------------------------------
class Copper(Enum):
    C110_ANNEALED = auto()


COPPER_MATERIALS: dict[Copper, MetalMaterial] = {
    Copper.C110_ANNEALED: MetalMaterial(
        # identity
        name="Copper_C110_ANNEALED",
        family="copper",
        # mechanical properties
        density=8900,
        hardness=Range(40, 60),
        hardness_scale="HB",
        modulus_of_elasticity=Range(115, 130),
        poisson_ratio=Range(0.34, 0.36),
        shear_modulus=Range(44, 48),
        shear_strength=Range(110, 150),
        tensile_strength=Range(200, 250),
        yield_strength=Range(50, 70),
        # thermal properties
        max_service_temp=Range(150, 250),
        melting_temperature=Range(1080, 1085),
        specific_heat_capacity=Range(380, 390),
        thermal_conductivity=Range(390, 400),
        thermal_expansion=Range(16e-6, 17e-6),
    ),
}


def copper(
    grade: Copper = Copper.C110_ANNEALED,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[MetalMaterial]:
    """Copper as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to C110 annealed.
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
        with_density(COPPER_MATERIALS[grade], density),
        finish,
        process=process,
    )


# --- Magnesium ---------------------------------------------------------------
class Magnesium(Enum):
    GENERIC_STRUCTURAL = auto()


MAGNESIUM_MATERIALS: dict[Magnesium, MetalMaterial] = {
    Magnesium.GENERIC_STRUCTURAL: MetalMaterial(
        # identity
        name="Magnesium_GENERIC_STRUCTURAL",
        family="magnesium",
        # mechanical properties
        density=1810,
        hardness=Range(60, 80),
        hardness_scale="HB",
        modulus_of_elasticity=Range(43, 45),
        poisson_ratio=Range(0.33, 0.37),
        shear_modulus=Range(16, 18),
        shear_strength=Range(120, 170),
        tensile_strength=Range(200, 280),
        yield_strength=Range(130, 200),
        # thermal properties
        max_service_temp=Range(80, 150),
        melting_temperature=Range(430, 630),
        specific_heat_capacity=Range(1000, 1100),
        thermal_conductivity=Range(70, 120),
        thermal_expansion=Range(25e-6, 27e-6),
    ),
}


def magnesium(
    grade: Magnesium = Magnesium.GENERIC_STRUCTURAL,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[MetalMaterial]:
    """Magnesium as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic structural.
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
        with_density(MAGNESIUM_MATERIALS[grade], density),
        finish,
        process=process,
    )


# --- Bronze ------------------------------------------------------------------
class Bronze(Enum):
    C51000_PHOSPHOR = auto()
    C90500_TIN = auto()
    C93200_BEARING = auto()


BRONZE_MATERIALS: dict[Bronze, MetalMaterial] = {
    # Wrought phosphor bronze (C51000): springs, bushings, fasteners. Bands span temper
    # (annealed -> hard); shear_strength is a derived estimate and the melting band is
    # the broad solidus->liquidus range.
    Bronze.C51000_PHOSPHOR: MetalMaterial(
        # identity
        name="Bronze_C51000_PHOSPHOR",
        family="bronze",
        # mechanical properties
        density=8800,
        hardness=Range(70, 200),
        hardness_scale="HB",
        modulus_of_elasticity=Range(100, 120),
        poisson_ratio=Range(0.33, 0.35),
        shear_modulus=Range(40, 44),
        shear_strength=Range(220, 360),
        tensile_strength=Range(300, 550),
        yield_strength=Range(130, 450),
        # thermal properties
        max_service_temp=Range(150, 250),
        melting_temperature=Range(900, 1000),
        specific_heat_capacity=Range(370, 380),
        thermal_conductivity=Range(50, 75),
        thermal_expansion=Range(17e-6, 19e-6),
    ),
    # Cast tin bronze / "gunmetal" (C90500, ~88Cu-10Sn-2Zn): valves, gears, bushings.
    # shear_strength derived; melting is the solidus->liquidus band.
    Bronze.C90500_TIN: MetalMaterial(
        # identity
        name="Bronze_C90500_TIN",
        family="bronze",
        # mechanical properties
        density=8800,
        hardness=Range(65, 110),
        hardness_scale="HB",
        modulus_of_elasticity=Range(95, 110),
        poisson_ratio=Range(0.33, 0.35),
        shear_modulus=Range(38, 44),
        shear_strength=Range(180, 280),
        tensile_strength=Range(275, 380),
        yield_strength=Range(130, 200),
        # thermal properties
        max_service_temp=Range(150, 250),
        melting_temperature=Range(850, 1000),
        specific_heat_capacity=Range(370, 380),
        thermal_conductivity=Range(65, 75),
        thermal_expansion=Range(17e-6, 19e-6),
    ),
    # Cast leaded bearing bronze (C93200 / SAE 660, ~83Cu-7Sn-7Pb-3Zn): sleeve bearings,
    # bushings. shear_strength derived; melting is the solidus->liquidus band.
    Bronze.C93200_BEARING: MetalMaterial(
        # identity
        name="Bronze_C93200_BEARING",
        family="bronze",
        # mechanical properties
        density=8900,
        hardness=Range(55, 75),
        hardness_scale="HB",
        modulus_of_elasticity=Range(90, 105),
        poisson_ratio=Range(0.33, 0.35),
        shear_modulus=Range(36, 42),
        shear_strength=Range(160, 240),
        tensile_strength=Range(240, 310),
        yield_strength=Range(110, 150),
        # thermal properties
        max_service_temp=Range(150, 250),
        melting_temperature=Range(850, 980),
        specific_heat_capacity=Range(370, 380),
        thermal_conductivity=Range(45, 60),
        thermal_expansion=Range(17e-6, 19e-6),
    ),
}


def bronze(
    grade: Bronze = Bronze.C51000_PHOSPHOR,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[MetalMaterial]:
    """Bronze as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to C51000 phosphor bronze.
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
        with_density(BRONZE_MATERIALS[grade], density),
        finish,
        process=process,
    )


# --- Gold --------------------------------------------------------------------
class Gold(Enum):
    PURE = auto()


GOLD_MATERIALS: dict[Gold, MetalMaterial] = {
    # Pure gold (Au 99.9%); bands span annealed (very soft) -> cold-worked. Gold is a
    # precious metal used structurally only in niche cases (contacts, jewelry); as a
    # coating it is the ``gold_plate`` finish. shear_strength + max_service_temp are
    # derived/nominal estimates.
    Gold.PURE: MetalMaterial(
        # identity
        name="Gold_PURE",
        family="gold",
        # mechanical properties
        density=19300,
        hardness=Range(25, 60),
        hardness_scale="HB",
        modulus_of_elasticity=Range(77, 79),
        poisson_ratio=Range(0.42, 0.44),
        shear_modulus=Range(26, 28),
        shear_strength=Range(70, 110),
        tensile_strength=Range(100, 220),
        yield_strength=Range(30, 200),
        # thermal properties
        max_service_temp=Range(200, 400),
        melting_temperature=Range(1063, 1064),
        specific_heat_capacity=Range(128, 130),
        thermal_conductivity=Range(315, 320),
        thermal_expansion=Range(14e-6, 14.5e-6),
    ),
}


def gold(
    grade: Gold = Gold.PURE,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[MetalMaterial]:
    """Gold as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to pure gold.
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
        with_density(GOLD_MATERIALS[grade], density),
        finish,
        process=process,
    )


# --- Silver ------------------------------------------------------------------
class Silver(Enum):
    PURE = auto()


SILVER_MATERIALS: dict[Silver, MetalMaterial] = {
    # Pure silver (Ag 99.9%); bands span annealed -> cold-worked. Like gold, a precious
    # metal used structurally only in niche cases; as a coating it is the ``silver_plate``
    # finish. shear_strength + max_service_temp are derived/nominal estimates.
    Silver.PURE: MetalMaterial(
        # identity
        name="Silver_PURE",
        family="silver",
        # mechanical properties
        density=10490,
        hardness=Range(25, 70),
        hardness_scale="HB",
        modulus_of_elasticity=Range(76, 83),
        poisson_ratio=Range(0.36, 0.38),
        shear_modulus=Range(29, 31),
        shear_strength=Range(100, 140),
        tensile_strength=Range(125, 200),
        yield_strength=Range(40, 140),
        # thermal properties
        max_service_temp=Range(200, 400),
        melting_temperature=Range(961, 962),
        specific_heat_capacity=Range(233, 236),
        thermal_conductivity=Range(420, 430),
        thermal_expansion=Range(18.5e-6, 19.5e-6),
    ),
}


def silver(
    grade: Silver = Silver.PURE,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
) -> FinishedMaterial[MetalMaterial]:
    """Silver as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to pure silver.
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
        with_density(SILVER_MATERIALS[grade], density),
        finish,
        process=process,
    )


ALL_METALS = (
    *ALU_MATERIALS.values(),
    *STAINLESS_MATERIALS.values(),
    *MILD_STEEL_MATERIALS.values(),
    *ALLOY_STEEL_MATERIALS.values(),
    *SPRING_STEEL_MATERIALS.values(),
    *TOOL_STEEL_MATERIALS.values(),
    *TITANIUM_MATERIALS.values(),
    *BRASS_MATERIALS.values(),
    *COPPER_MATERIALS.values(),
    *MAGNESIUM_MATERIALS.values(),
    *BRONZE_MATERIALS.values(),
    *GOLD_MATERIALS.values(),
    *SILVER_MATERIALS.values(),
)


def custom_metal(
    name: str,
    density: float,
    *,
    family: str = "stainless",
    transparent: bool = False,
    tensile_strength: RangeInput = None,
    yield_strength: RangeInput = None,
    shear_strength: RangeInput = None,
    modulus_of_elasticity: RangeInput = None,
    shear_modulus: RangeInput = None,
    poisson_ratio: RangeInput = None,
    hardness: RangeInput = None,
    hardness_scale: str = "HB",
    max_service_temp: RangeInput = None,
    melting_temperature: RangeInput = None,
    specific_heat_capacity: RangeInput = None,
    thermal_conductivity: RangeInput = None,
    thermal_expansion: RangeInput = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    pbr: PbrProperties | None = None,
) -> FinishedMaterial[MetalMaterial]:
    """Define a custom metal and return it as a ``FinishedMaterial``.

    Each property value may be a ``Range``, a bare number (an exact value, ``min ==
    max``), or ``None`` (missing); ``NOT_SUITABLE`` marks a property that does not
    apply. The property keyword args are the ``MetalMaterial`` fields.

    Args:
        name: Identifier for the material.
        density: Single representative density (kg/m³).
        family: PBR look key (e.g. ``"titanium"``); an unknown key falls back per the
            PBR bridge. Defaults to ``"stainless"``.
        transparent: Intrinsic see-through flag (metals are opaque). Default ``False``.
        hardness_scale: Scale for ``hardness`` (``"HB"`` / ``"HRC"`` / ``"HV"``).
        finish: Surface finish -- an ``AppliedFinish`` or a list of them. Mutually
            exclusive with ``process`` and ``pbr``.
        process: As-made surface hint. Mutually exclusive with ``finish`` and ``pbr``.
        pbr: A ready-made three.js look; overrides the resolved one (and cannot be
            combined with ``finish`` / ``process``).

    Returns:
        A ``FinishedMaterial`` wrapping the custom metal.
    """
    return FinishedMaterial(
        MetalMaterial(
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
            hardness=as_range(hardness),
            hardness_scale=hardness_scale,
            melting_temperature=as_range(melting_temperature),
        ),
        finish,
        process=process,
        pbr=pbr,
    )


if __name__ == "__main__":
    print(f"metals: {len(ALL_METALS)}")
    _families = {
        "aluminum": ALU_MATERIALS,
        "stainless": STAINLESS_MATERIALS,
        "mild_steel": MILD_STEEL_MATERIALS,
        "alloy_steel": ALLOY_STEEL_MATERIALS,
        "spring_steel": SPRING_STEEL_MATERIALS,
        "tool_steel": TOOL_STEEL_MATERIALS,
        "titanium": TITANIUM_MATERIALS,
        "brass": BRASS_MATERIALS,
        "copper": COPPER_MATERIALS,
        "magnesium": MAGNESIUM_MATERIALS,
    }
    for _fam, _dct in _families.items():
        print(f"  {_fam:12s}: {len(_dct)}")
    print()
    print(ALU_MATERIALS[Alu.G6061_T6])
    print(TITANIUM_MATERIALS[Titanium.GR5_ANNEALED])
