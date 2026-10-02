"""Typical-value property ranges for textiles (woven fabric, felt, leather).

Textiles are **areal goods**: the primary mass metric is grammage (``areal_density``,
g/m2), not volumetric density; the ``density`` field is only the effective bulk value.
``tensile_strength`` is the in-plane value and is approximate for these flexible
materials, so treat all values as rough typicals. (Leather isn't strictly a textile but
is grouped here as a soft areal good.)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, ClassVar

from ..finished import Color, FinishedMaterial, FinishSpec
from ..processes import ProcessSpec
from ..core import ArealMaterial, Range, RangeInput, as_range, with_density

if TYPE_CHECKING:
    from threejs_materials import PbrProperties


@dataclass(frozen=True, kw_only=True)
class TextileMaterial(ArealMaterial):
    """A textile: the shared areal ranges (from ``ArealMaterial``). ``family`` is the
    three.js textile factory key; a part's color lives on the ``FinishedMaterial``.
    """

    category: ClassVar[str] = "textile"


# --- Woven -------------------------------------------------------------------
class Woven(Enum):
    GENERIC = auto()


WOVEN_MATERIALS: dict[Woven, TextileMaterial] = {
    Woven.GENERIC: TextileMaterial(
        # identity
        name="Woven_GENERIC",
        family="fabric_weave",
        # mechanical properties
        areal_density=Range(150, 300),
        density=500,
        tensile_strength=Range(10, 50),
        thickness=Range(0.3, 0.6),
        # thermal properties
        specific_heat_capacity=Range(1300, 1700),
        thermal_conductivity=Range(0.03, 0.07),
    ),
}


def woven(
    grade: Woven = Woven.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
    scale: tuple[float, float] = (1.0, 1.0),
    rotation: float = 0.0,
) -> FinishedMaterial[TextileMaterial]:
    """Woven fabric as a ``FinishedMaterial``.

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
        scale: Texture UV scale ``(u, v)`` for the substrate texture (grain/weave);
            ``(2, 2)`` tiles it twice as fine. Default ``(1, 1)``.
        rotation: Texture rotation in degrees (counterclockwise). Default ``0``.

    Returns:
        A ``FinishedMaterial`` for the selected grade.
    """
    return FinishedMaterial(
        with_density(WOVEN_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
        scale=scale,
        rotation=rotation,
    )


# --- Felt --------------------------------------------------------------------
class Felt(Enum):
    GENERIC = auto()


FELT_MATERIALS: dict[Felt, TextileMaterial] = {
    Felt.GENERIC: TextileMaterial(
        # identity
        name="Felt_GENERIC",
        family="felt",
        # mechanical properties
        areal_density=Range(200, 400),
        density=120,
        tensile_strength=Range(2, 10),
        thickness=Range(2, 4),
        # thermal properties
        specific_heat_capacity=Range(1300, 1700),
        thermal_conductivity=Range(0.04, 0.08),
    ),
}


def felt(
    grade: Felt = Felt.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
    scale: tuple[float, float] = (1.0, 1.0),
    rotation: float = 0.0,
) -> FinishedMaterial[TextileMaterial]:
    """Felt as a ``FinishedMaterial``.

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
        scale: Texture UV scale ``(u, v)`` for the substrate texture (grain/weave);
            ``(2, 2)`` tiles it twice as fine. Default ``(1, 1)``.
        rotation: Texture rotation in degrees (counterclockwise). Default ``0``.

    Returns:
        A ``FinishedMaterial`` for the selected grade.
    """
    return FinishedMaterial(
        with_density(FELT_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
        scale=scale,
        rotation=rotation,
    )


# --- Leather -----------------------------------------------------------------
class Leather(Enum):
    GENERIC = auto()


LEATHER_MATERIALS: dict[Leather, TextileMaterial] = {
    Leather.GENERIC: TextileMaterial(
        # identity
        name="Leather_GENERIC",
        family="leather",
        # mechanical properties
        areal_density=Range(800, 1600),
        density=950,
        tensile_strength=Range(10, 30),
        thickness=Range(1, 3),
        # thermal properties
        specific_heat_capacity=Range(1500, 2000),
        thermal_conductivity=Range(0.14, 0.20),
    ),
}


def leather(
    grade: Leather = Leather.GENERIC,
    color: Color | None = None,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
    scale: tuple[float, float] = (1.0, 1.0),
    rotation: float = 0.0,
) -> FinishedMaterial[TextileMaterial]:
    """Leather as a ``FinishedMaterial``.

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
        scale: Texture UV scale ``(u, v)`` for the substrate texture (grain/weave);
            ``(2, 2)`` tiles it twice as fine. Default ``(1, 1)``.
        rotation: Texture rotation in degrees (counterclockwise). Default ``0``.

    Returns:
        A ``FinishedMaterial`` for the selected grade.
    """
    return FinishedMaterial(
        with_density(LEATHER_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
        scale=scale,
        rotation=rotation,
    )


ALL_TEXTILES = (
    *WOVEN_MATERIALS.values(),
    *FELT_MATERIALS.values(),
    *LEATHER_MATERIALS.values(),
)


def custom_textile(
    name: str,
    density: float,
    *,
    family: str = "fabric_weave",
    transparent: bool = False,
    areal_density: RangeInput = None,
    thickness: RangeInput = None,
    tensile_strength: RangeInput = None,
    thermal_conductivity: RangeInput = None,
    specific_heat_capacity: RangeInput = None,
    color: Color | None = None,
    scale: tuple[float, float] = (1.0, 1.0),
    rotation: float = 0.0,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    pbr: PbrProperties | None = None,
) -> FinishedMaterial[TextileMaterial]:
    """Define a custom textile and return it as a ``FinishedMaterial``.

    Each property value may be a ``Range``, a bare number (an exact value, ``min ==
    max``), or ``None`` (missing). The property keyword args are the ``TextileMaterial``
    fields (areal: grammage-sized planar goods).

    Args:
        name: Identifier for the material.
        density: Apparent single representative density (kg/m³).
        family: PBR look key (e.g. ``"felt"`` / ``"leather"``); an unknown key falls
            back to a woven weave. Defaults to ``"fabric_weave"``.
        transparent: Intrinsic see-through flag. Default ``False``.
        color: Selectable base color -- a build123d ``ColorLike`` (name, hex,
            ``0xRRGGBB`` int, RGB(A) tuple, or a ``Color``).
        scale: Texture UV scale ``(u, v)``; ``(2, 2)`` tiles the weave twice as fine.
        rotation: Weave texture rotation in degrees (counterclockwise).
        finish: Surface finish -- mutually exclusive with ``process`` and ``pbr``.
        process: As-made surface hint -- mutually exclusive with ``finish`` and ``pbr``.
        pbr: A ready-made three.js look; overrides the resolved one.

    Returns:
        A ``FinishedMaterial`` wrapping the custom textile.
    """
    return FinishedMaterial(
        TextileMaterial(
            name=name,
            density=density,
            family=family,
            transparent=transparent,
            areal_density=as_range(areal_density),
            thickness=as_range(thickness),
            tensile_strength=as_range(tensile_strength),
            thermal_conductivity=as_range(thermal_conductivity),
            specific_heat_capacity=as_range(specific_heat_capacity),
        ),
        finish,
        color=color,
        scale=scale,
        rotation=rotation,
        process=process,
        pbr=pbr,
    )


if __name__ == "__main__":
    print(f"textiles: {len(ALL_TEXTILES)}")
    print()
    for _t in ALL_TEXTILES:
        print(_t)
        print()
