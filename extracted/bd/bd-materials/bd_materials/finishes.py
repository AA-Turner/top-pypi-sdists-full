"""Surface finishes: the finish catalog + the ergonomic finish functions.

Finishes are grouped by process into enums (:class:`Mechanical`, :class:`Chemical`,
:class:`MetalPlating`, :class:`Coating`, :class:`Marking`), each backed by a
``<GROUP>_FINISHES`` dict keyed by that enum -- the maintenance backbone. The
**public API is the flat verb functions** (``anodize("blue")``, ``powder_coat(...)``),
which bind a color (and, for paints/coatings, a :class:`Sheen`) to a finish and
return an :class:`AppliedFinish`.

A ``Finish`` is purely its intrinsic spec (name + optional notes). Where a finish is
*typically* used (its substrates) is a separate concern and lives in
:mod:`.applicability` -- one central material<->finish table.

Finishes are advisory, not gated: **any finish may be specified on any material**.

Which colors a finish is typically offered in is advisory and deliberately not
modelled on the ``Finish`` -- any color may be applied per part (a name in
``pbr._COLOR_HEX`` renders as that swatch; anything else passes through). Sheen
(matte/gloss) is a per-application choice like color -- it rides on the
``AppliedFinish``, not the ``Finish``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from .core import Color


class Sheen(Enum):
    """Surface sheen of a paint/coating -- a per-application choice like color."""

    GLOSS = auto()
    MATTE = auto()


@dataclass(frozen=True)
class Finish:
    """A surface finish's intrinsic spec (name + optional notes). Which colors a
    finish is typically offered in is advisory and not modelled here; substrate
    applicability lives in :mod:`.applicability`, not here."""

    name: str
    notes: str | None = None


# ===========================================================================
# Finish catalog: one group enum + one <GROUP>_FINISHES dict per process family.
# ===========================================================================


class Mechanical(Enum):
    BEAD_BLAST = auto()
    BRUSHED = auto()
    FINE_SANDING = auto()
    SMOOTH_MACHINING = auto()
    ELECTROPOLISHED = auto()


MECHANICAL_FINISHES: dict[Mechanical, Finish] = {
    Mechanical.BEAD_BLAST: Finish("Bead Blast"),
    Mechanical.BRUSHED: Finish("Brushed"),
    Mechanical.FINE_SANDING: Finish("Fine Sanding"),
    Mechanical.SMOOTH_MACHINING: Finish(
        "Smooth machining (Ra1.6µm)", notes="as-machined roughness spec"
    ),
    Mechanical.ELECTROPOLISHED: Finish("Electropolished"),
}


class Chemical(Enum):
    ANODIZED = auto()
    CHEM_FILM = auto()
    CONDUCTIVE_OXIDATION = auto()
    BLACK_OXIDE = auto()
    PASSIVATION = auto()
    PICKLING = auto()
    DYEING = auto()


CHEMICAL_FINISHES: dict[Chemical, Finish] = {
    Chemical.ANODIZED: Finish(
        "Anodized",
        notes=(
            "typical colors: natural, black, gray, gold, rose gold, red, blue, "
            "champagne, brown, purple, green, orange"
        ),
    ),
    Chemical.CHEM_FILM: Finish(
        "Chemical conversion coat (Chem film)", notes="typical colors: clear, gold"
    ),
    Chemical.CONDUCTIVE_OXIDATION: Finish(
        "Electrically conductive oxidation", notes="color: clear"
    ),
    Chemical.BLACK_OXIDE: Finish("Black oxide", notes="color: black"),
    Chemical.PASSIVATION: Finish("Passivation"),
    Chemical.PICKLING: Finish("Pickling"),
    Chemical.DYEING: Finish(
        "Dyeing", notes="anodized aluminum, or dyeable polymers (esp. nylon)"
    ),
}


class MetalPlating(Enum):
    CHROME_PLATING = auto()
    GOLD_PLATING = auto()
    NICKEL_PLATING = auto()
    SILVER_PLATING = auto()
    TIN_PLATING = auto()
    PVD = auto()
    ZINC_PLATING = auto()
    VACUUM_PLATING = auto()


METAL_PLATING_FINISHES: dict[MetalPlating, Finish] = {
    MetalPlating.CHROME_PLATING: Finish("Chrome plating", notes="color: chrome"),
    MetalPlating.GOLD_PLATING: Finish("Gold plating", notes="color: gold"),
    MetalPlating.NICKEL_PLATING: Finish("Nickel plating", notes="color: nickel"),
    MetalPlating.SILVER_PLATING: Finish("Silver plating", notes="color: silver"),
    MetalPlating.TIN_PLATING: Finish("Tin plating", notes="color: silver"),
    MetalPlating.PVD: Finish(
        "PVD (Physical Vapor Deposition)",
        notes="typical colors: gold, rose gold, black, gunmetal, blue",
    ),
    MetalPlating.ZINC_PLATING: Finish(
        "Zinc plating",
        notes=(
            "corrosion protection for ferrous steels; "
            "typical colors: clear, blue, yellow, black"
        ),
    ),
    MetalPlating.VACUUM_PLATING: Finish("Vacuum plating"),
}


class Coating(Enum):
    POWDER_COAT = auto()
    ELECTROPHORESIS = auto()
    SPRAY_PAINT = auto()


COATING_FINISHES: dict[Coating, Finish] = {
    Coating.POWDER_COAT: Finish("Powder coat"),
    Coating.ELECTROPHORESIS: Finish("Electrophoresis"),
    Coating.SPRAY_PAINT: Finish("Spray painting"),
}


class Marking(Enum):
    LASER_ENGRAVING = auto()
    ETCHING = auto()
    SILKSCREEN = auto()


MARKING_FINISHES: dict[Marking, Finish] = {
    Marking.LASER_ENGRAVING: Finish("Laser engraving"),
    Marking.ETCHING: Finish("Etching"),
    Marking.SILKSCREEN: Finish("Silkscreen"),
}


# All finishes flattened; used by :mod:`.applicability`.
ALL_FINISHES = (
    *MECHANICAL_FINISHES.values(),
    *CHEMICAL_FINISHES.values(),
    *METAL_PLATING_FINISHES.values(),
    *COATING_FINISHES.values(),
    *MARKING_FINISHES.values(),
)


# ===========================================================================
# Applied finishes: the flat verb functions bind color/sheen to a finish.
# ===========================================================================


@dataclass(frozen=True)
class AppliedFinish:
    """A finish plus its per-application appearance choices (color, sheen) and, for
    textured finishes, the texture UV transform (scale, rotation) -- produced by the
    finish functions below."""

    finish: Finish
    color: Color | None = None
    sheen: Sheen | None = None  # None = finish has no sheen choice
    scale: tuple[float, float] = (1.0, 1.0)  # texture UV scale (u, v); 1 = as-authored
    rotation: float = 0.0  # texture rotation in degrees (counterclockwise)


# --- mechanical (no color) ------------------------------------------------
def bead_blast(scale: tuple[float, float] = (1.0, 1.0)) -> AppliedFinish:
    """Bead-blasted matte finish.

    Args:
        scale: Texture UV scale ``(u, v)``; ``(2, 2)`` tiles the blast grain twice as
            fine. Isotropic, so no rotation. Default ``(1, 1)`` is the as-authored size.

    Returns:
        The applied finish.
    """
    return AppliedFinish(MECHANICAL_FINISHES[Mechanical.BEAD_BLAST], scale=scale)


def brushed(
    scale: tuple[float, float] = (1.0, 1.0), rotation: float = 0.0
) -> AppliedFinish:
    """Brushed directional-satin finish.

    Args:
        scale: Texture UV scale ``(u, v)``; ``(2, 2)`` tiles the brush grain twice as
            fine. Default ``(1, 1)`` is the as-authored size.
        rotation: Texture rotation in degrees (counterclockwise), e.g. to run the brush
            lines across the part. Default ``0``.

    Returns:
        The applied finish.
    """
    return AppliedFinish(
        MECHANICAL_FINISHES[Mechanical.BRUSHED], scale=scale, rotation=rotation
    )


def fine_sanding(scale: tuple[float, float] = (1.0, 1.0)) -> AppliedFinish:
    """Fine-sanded smooth-matte finish.

    Args:
        scale: Texture UV scale ``(u, v)``; ``(2, 2)`` tiles the grain twice as fine.
            Isotropic, so no rotation. Default ``(1, 1)`` is the as-authored size.

    Returns:
        The applied finish.
    """
    return AppliedFinish(MECHANICAL_FINISHES[Mechanical.FINE_SANDING], scale=scale)


def smooth_machining() -> AppliedFinish:
    """Smooth as-machined finish (Ra 1.6 µm)."""
    return AppliedFinish(MECHANICAL_FINISHES[Mechanical.SMOOTH_MACHINING])


def electropolish() -> AppliedFinish:
    """Electropolished bright finish."""
    return AppliedFinish(MECHANICAL_FINISHES[Mechanical.ELECTROPOLISHED])


# --- chemical --------------------------------------------------------------
def anodize(color: Color) -> AppliedFinish:
    """Anodized finish in ``color``.

    Args:
        color: The anodize color -- any build123d ``ColorLike`` (name / hex / int /
            RGB tuple / ``Color``). Mandatory -- anodizing is done to add color
            ("natural" is still an explicit choice, not the absence of one).

    Returns:
        The applied finish.
    """
    return AppliedFinish(CHEMICAL_FINISHES[Chemical.ANODIZED], color)


def chem_film() -> AppliedFinish:
    """Chromate conversion coating (chem film)."""
    return AppliedFinish(CHEMICAL_FINISHES[Chemical.CHEM_FILM])


def conductive_oxidation() -> AppliedFinish:
    """Electrically-conductive oxidation coating."""
    return AppliedFinish(CHEMICAL_FINISHES[Chemical.CONDUCTIVE_OXIDATION])


def black_oxide() -> AppliedFinish:
    """Black-oxide conversion finish."""
    return AppliedFinish(CHEMICAL_FINISHES[Chemical.BLACK_OXIDE])


def passivate() -> AppliedFinish:
    """Passivation finish (stainless corrosion resistance)."""
    return AppliedFinish(CHEMICAL_FINISHES[Chemical.PASSIVATION])


def pickle() -> AppliedFinish:
    """Pickling finish (oxide / scale removal)."""
    return AppliedFinish(CHEMICAL_FINISHES[Chemical.PICKLING])


def dye(color: Color) -> AppliedFinish:
    """Dyed finish in ``color`` (anodized aluminum or dyeable polymers).

    Args:
        color: The dye color -- any build123d ``ColorLike`` (name / hex / int / RGB
            tuple / ``Color``).

    Returns:
        The applied finish.
    """
    return AppliedFinish(CHEMICAL_FINISHES[Chemical.DYEING], color)


# --- metal plating ---------------------------------------------------------
def chrome() -> AppliedFinish:
    """Chrome plating."""
    return AppliedFinish(METAL_PLATING_FINISHES[MetalPlating.CHROME_PLATING])


def gold_plate() -> AppliedFinish:
    """Gold plating."""
    return AppliedFinish(METAL_PLATING_FINISHES[MetalPlating.GOLD_PLATING])


def nickel_plate() -> AppliedFinish:
    """Nickel plating."""
    return AppliedFinish(METAL_PLATING_FINISHES[MetalPlating.NICKEL_PLATING])


def silver_plate() -> AppliedFinish:
    """Silver plating."""
    return AppliedFinish(METAL_PLATING_FINISHES[MetalPlating.SILVER_PLATING])


def tin_plate() -> AppliedFinish:
    """Tin plating (matte, solderable)."""
    return AppliedFinish(METAL_PLATING_FINISHES[MetalPlating.TIN_PLATING])


def pvd(color: Color = "clear") -> AppliedFinish:
    """PVD coating in ``color``.

    Args:
        color: "clear" (default) is bright natural PVD, with the substrate showing
            through; colors are opt-in. Any build123d ``ColorLike``.

    Returns:
        The applied finish.
    """
    return AppliedFinish(METAL_PLATING_FINISHES[MetalPlating.PVD], color)


def zinc_plate(color: Color = "clear") -> AppliedFinish:
    """Zinc plating in ``color``.

    Args:
        color: "clear" (default) is the clear/bright chromate -- the natural zinc look;
            others are chromate tints. Any build123d ``ColorLike``.

    Returns:
        The applied finish.
    """
    return AppliedFinish(METAL_PLATING_FINISHES[MetalPlating.ZINC_PLATING], color)


def vacuum_plating(color: Color, sheen: Sheen = Sheen.GLOSS) -> AppliedFinish:
    """Vacuum-metallised plating in ``color``.

    Args:
        color: The plating color -- any build123d ``ColorLike`` (name / hex / int /
            RGB tuple / ``Color``).
        sheen: Gloss (default) or matte.

    Returns:
        The applied finish.
    """
    return AppliedFinish(
        METAL_PLATING_FINISHES[MetalPlating.VACUUM_PLATING], color, sheen
    )


# --- coating / paint (sheen: gloss default, matte optional) ----------------
def powder_coat(color: Color, sheen: Sheen = Sheen.GLOSS) -> AppliedFinish:
    """Powder coat in ``color``.

    Args:
        color: The coat color (any, to spec) -- any build123d ``ColorLike``.
        sheen: Gloss (default) or matte.

    Returns:
        The applied finish.
    """
    return AppliedFinish(COATING_FINISHES[Coating.POWDER_COAT], color, sheen)


def spray_paint(color: Color, sheen: Sheen = Sheen.GLOSS) -> AppliedFinish:
    """Spray paint in ``color``.

    Args:
        color: The paint color (any, to spec) -- any build123d ``ColorLike``.
        sheen: Gloss (default) or matte.

    Returns:
        The applied finish.
    """
    return AppliedFinish(COATING_FINISHES[Coating.SPRAY_PAINT], color, sheen)


def electrophoresis(color: Color = "black") -> AppliedFinish:
    """Electrophoretic e-coat in ``color`` (automotive-style dip coat).

    Args:
        color: The e-coat color -- any build123d ``ColorLike``. Defaults to black (the
            common automotive primer); white and RAL colors are also available to spec.

    Returns:
        The applied finish.
    """
    return AppliedFinish(COATING_FINISHES[Coating.ELECTROPHORESIS], color)


# --- marking ---------------------------------------------------------------
def laser_engrave() -> AppliedFinish:
    """Laser-engraved marking."""
    return AppliedFinish(MARKING_FINISHES[Marking.LASER_ENGRAVING])


def etch() -> AppliedFinish:
    """Etched marking."""
    return AppliedFinish(MARKING_FINISHES[Marking.ETCHING])


def silkscreen(color: Color = "black") -> AppliedFinish:
    """Silkscreen marking in ``color`` (default black).

    Args:
        color: The ink color -- any build123d ``ColorLike``. Note PBR ignores markings,
            so this is metadata.

    Returns:
        The applied finish.
    """
    return AppliedFinish(MARKING_FINISHES[Marking.SILKSCREEN], color)


__all__ = [
    # types + vocab
    "Finish",
    "AppliedFinish",
    "Sheen",
    # catalog (maintenance backbone)
    "Mechanical",
    "Chemical",
    "MetalPlating",
    "Coating",
    "Marking",
    "MECHANICAL_FINISHES",
    "CHEMICAL_FINISHES",
    "METAL_PLATING_FINISHES",
    "COATING_FINISHES",
    "MARKING_FINISHES",
    "ALL_FINISHES",
    # finish functions (the public API)
    "bead_blast",
    "brushed",
    "fine_sanding",
    "smooth_machining",
    "electropolish",
    "anodize",
    "chem_film",
    "conductive_oxidation",
    "black_oxide",
    "passivate",
    "pickle",
    "dye",
    "chrome",
    "gold_plate",
    "nickel_plate",
    "silver_plate",
    "tin_plate",
    "pvd",
    "zinc_plate",
    "vacuum_plating",
    "powder_coat",
    "spray_paint",
    "electrophoresis",
    "laser_engrave",
    "etch",
    "silkscreen",
]
