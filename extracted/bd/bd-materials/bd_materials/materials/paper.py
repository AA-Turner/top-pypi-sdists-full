"""Typical-value property ranges for paper goods (paper, cardboard, foamboard).

These are **areal goods**: the primary mass metric is grammage (``areal_density``,
g/m2), not volumetric density -- a cut sheet's mass is grammage x area, and the
``density`` field is only the effective bulk value. ``tensile_strength`` is the in-plane
(machine-direction) value and is approximate for these layered materials; grade and
supplier variation is large, so treat all values as rough typicals.
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
class PaperMaterial(ArealMaterial):
    """A paper good: the shared areal ranges (from ``ArealMaterial``). ``family`` is
    the three.js paper factory key; a part's color lives on the ``FinishedMaterial``.
    """

    category: ClassVar[str] = "paper"


# --- Paper -------------------------------------------------------------------
class Paper(Enum):
    OFFICE = auto()


PAPER_MATERIALS: dict[Paper, PaperMaterial] = {
    Paper.OFFICE: PaperMaterial(
        # identity
        name="Paper_OFFICE",
        family="paper",
        # mechanical properties
        areal_density=Range(70, 90),
        density=800,
        tensile_strength=Range(20, 60),
        thickness=Range(0.09, 0.12),
        # thermal properties
        specific_heat_capacity=Range(1300, 1400),
        thermal_conductivity=Range(0.05, 0.10),
    ),
}


def paper(
    grade: Paper = Paper.OFFICE,
    color: Color | None = "white",
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
    scale: tuple[float, float] = (1.0, 1.0),
    rotation: float = 0.0,
) -> FinishedMaterial[PaperMaterial]:
    """Office paper as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to office.
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
        with_density(PAPER_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
        scale=scale,
        rotation=rotation,
    )


# --- Cardboard ---------------------------------------------------------------
class Cardboard(Enum):
    CORRUGATED = auto()


CARDBOARD_MATERIALS: dict[Cardboard, PaperMaterial] = {
    Cardboard.CORRUGATED: PaperMaterial(
        # identity
        name="Cardboard_CORRUGATED",
        family="corrugated_cardboard",
        # mechanical properties
        areal_density=Range(400, 700),
        # effective panel density (incl. flute voids); areal_density is the primary mass metric
        density=140,
        tensile_strength=Range(5, 25),
        thickness=Range(3, 5),
        # thermal properties
        specific_heat_capacity=Range(1300, 1400),
        thermal_conductivity=Range(0.05, 0.10),
    ),
}


def cardboard(
    grade: Cardboard = Cardboard.CORRUGATED,
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
    scale: tuple[float, float] = (1.0, 1.0),
    rotation: float = 0.0,
) -> FinishedMaterial[PaperMaterial]:
    """Corrugated cardboard as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to corrugated.
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
        with_density(CARDBOARD_MATERIALS[grade], density),
        finish,
        process=process,
        scale=scale,
        rotation=rotation,
    )


# --- Foamboard ---------------------------------------------------------------
class Foamboard(Enum):
    GENERIC = auto()


FOAMBOARD_MATERIALS: dict[Foamboard, PaperMaterial] = {
    Foamboard.GENERIC: PaperMaterial(
        # identity
        name="Foamboard_GENERIC",
        family="foamboard",
        # mechanical properties
        areal_density=Range(400, 550),
        density=120,
        tensile_strength=Range(2, 10),
        thickness=Range(3, 6),
        # thermal properties
        specific_heat_capacity=Range(1300, 1500),
        thermal_conductivity=Range(0.03, 0.06),
    ),
}


def foamboard(
    grade: Foamboard = Foamboard.GENERIC,
    color: Color | None = "white",
    finish: FinishSpec = None,
    process: ProcessSpec = None,
    density: float | None = None,
    scale: tuple[float, float] = (1.0, 1.0),
    rotation: float = 0.0,
) -> FinishedMaterial[PaperMaterial]:
    """Foamboard as a ``FinishedMaterial``.

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
        with_density(FOAMBOARD_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
        scale=scale,
        rotation=rotation,
    )


ALL_PAPERS = (
    *PAPER_MATERIALS.values(),
    *CARDBOARD_MATERIALS.values(),
    *FOAMBOARD_MATERIALS.values(),
)


def custom_paper(
    name: str,
    density: float,
    *,
    family: str = "paper",
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
) -> FinishedMaterial[PaperMaterial]:
    """Define a custom paper/board and return it as a ``FinishedMaterial``.

    Each property value may be a ``Range``, a bare number (an exact value, ``min ==
    max``), or ``None`` (missing). The property keyword args are the ``PaperMaterial``
    fields (areal: grammage-sized planar goods).

    Args:
        name: Identifier for the material.
        density: Apparent single representative density (kg/m³).
        family: PBR look key (e.g. ``"foamboard"``); an unknown key falls back to paper.
            Defaults to ``"paper"``.
        transparent: Intrinsic see-through flag (paper is opaque). Default ``False``.
        color: Selectable base color -- a build123d ``ColorLike`` (name, hex,
            ``0xRRGGBB`` int, RGB(A) tuple, or a ``Color``).
        scale: Texture UV scale ``(u, v)``; ``(2, 2)`` tiles the surface twice as fine.
        rotation: Texture rotation in degrees (counterclockwise).
        finish: Surface finish -- mutually exclusive with ``process`` and ``pbr``.
        process: As-made surface hint -- mutually exclusive with ``finish`` and ``pbr``.
        pbr: A ready-made three.js look; overrides the resolved one.

    Returns:
        A ``FinishedMaterial`` wrapping the custom paper.
    """
    return FinishedMaterial(
        PaperMaterial(
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
    print(f"papers: {len(ALL_PAPERS)}")
    print()
    for _p in ALL_PAPERS:
        print(_p)
        print()
