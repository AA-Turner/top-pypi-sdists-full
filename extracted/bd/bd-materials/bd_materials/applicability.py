"""The material<->finish applicability relation, in one place.

Which finishes are *typically* used on which materials is advisory (never a
constraint -- any finish may be applied to any material). Rather than scatter that
across each ``Finish``, it lives here as one central table, :data:`TYPICAL_SUBSTRATES`,
keyed by finish enum member. Two queries read it, one per direction:

    typical_finishes(material)  -> the finishes typically used on that material
    typical_materials(finish)   -> the catalog materials that finish is typical on

A finish's substrate set holds ``category`` names ("metal") and/or ``family`` names
("stainless"); a material matches when its ``category`` **or** ``family`` is listed.

This module sees both ``finishes`` and the material catalog, so it sits above them
(the material modules import from ``finishes``; this closes the loop without a cycle).
"""

from __future__ import annotations

from enum import Enum

from . import finishes as fin
from .core import COATABLE_POLY, EVERYTHING, FERROUS, METAL, PAINTABLE, RangeMaterial
from .materials import ALL_MATERIALS

# One place: finish -> the substrate keys (category and/or family) it's typical on.
# The substrate shorthands (METAL, PAINTABLE, ...) come from core, next to FERROUS.
TYPICAL_SUBSTRATES: dict[Enum, frozenset[str]] = {
    fin.Mechanical.BEAD_BLAST: frozenset({"metal", "plastic"}),
    fin.Mechanical.BRUSHED: METAL,
    fin.Mechanical.FINE_SANDING: frozenset({"metal", "plastic", "wood"}),
    fin.Mechanical.SMOOTH_MACHINING: frozenset({"metal", "plastic", "wood"}),
    fin.Mechanical.ELECTROPOLISHED: frozenset({"stainless", "titanium"}),
    fin.Chemical.ANODIZED: frozenset({"aluminum", "titanium"}),
    fin.Chemical.CHEM_FILM: frozenset({"aluminum"}),
    fin.Chemical.CONDUCTIVE_OXIDATION: frozenset({"aluminum"}),
    fin.Chemical.BLACK_OXIDE: FERROUS | frozenset({"stainless", "copper", "brass"}),
    fin.Chemical.PASSIVATION: frozenset({"stainless", "titanium"}),
    fin.Chemical.PICKLING: FERROUS | frozenset({"stainless"}),
    fin.Chemical.DYEING: frozenset({"plastic", "resin", "aluminum"}),
    fin.MetalPlating.CHROME_PLATING: METAL,
    fin.MetalPlating.GOLD_PLATING: METAL,
    fin.MetalPlating.NICKEL_PLATING: METAL,
    fin.MetalPlating.SILVER_PLATING: METAL,
    fin.MetalPlating.TIN_PLATING: METAL,
    fin.MetalPlating.PVD: METAL,
    fin.MetalPlating.ZINC_PLATING: FERROUS,
    fin.MetalPlating.VACUUM_PLATING: COATABLE_POLY,
    fin.Coating.POWDER_COAT: METAL,
    fin.Coating.ELECTROPHORESIS: METAL,
    fin.Coating.SPRAY_PAINT: PAINTABLE,
    fin.Marking.LASER_ENGRAVING: EVERYTHING,
    fin.Marking.ETCHING: frozenset({"metal", "glass"}),
    fin.Marking.SILKSCREEN: frozenset({"metal", "plastic", "resin", "glass"}),
}

# enum member -> Finish, and its inverse, to translate between the table keys and
# the Finish objects that AppliedFinish / the verb functions carry.
_FINISH_BY_KEY: dict[Enum, fin.Finish] = {
    **fin.MECHANICAL_FINISHES,
    **fin.CHEMICAL_FINISHES,
    **fin.METAL_PLATING_FINISHES,
    **fin.COATING_FINISHES,
    **fin.MARKING_FINISHES,
}
_KEY_BY_FINISH: dict[fin.Finish, Enum] = {v: k for k, v in _FINISH_BY_KEY.items()}


def _substrate_key(finish) -> Enum:
    """Resolve a finish to its ``TYPICAL_SUBSTRATES`` key.

    Args:
        finish: A finish enum member, a ``Finish``, or an ``AppliedFinish``.

    Returns:
        The finish enum member used as the table key.
    """
    if isinstance(finish, fin.AppliedFinish):
        finish = finish.finish
    if isinstance(finish, fin.Finish):
        return _KEY_BY_FINISH[finish]
    return finish  # already a finish enum member


def _matches(material: RangeMaterial, substrates: frozenset[str]) -> bool:
    """Whether ``material``'s category or family is in the substrate set."""
    return material.category in substrates or material.family in substrates


def typical_finishes(material: RangeMaterial) -> list[fin.Finish]:
    """The finishes typically used on a material (advisory, not a constraint).

    Args:
        material: The material to look up (matched by its ``category`` / ``family``).

    Returns:
        The finishes ``TYPICAL_SUBSTRATES`` marks as typical for it (possibly empty).
    """
    return [
        _FINISH_BY_KEY[key]
        for key, subs in TYPICAL_SUBSTRATES.items()
        if _matches(material, subs)
    ]


def typical_materials(finish) -> list[RangeMaterial]:
    """The catalog materials a finish is typically used on (advisory).

    Args:
        finish: A finish enum member (e.g. ``Chemical.ANODIZED``), a ``Finish``, or an
            ``AppliedFinish``.

    Returns:
        The catalog materials ``TYPICAL_SUBSTRATES`` marks as typical for it.
    """
    subs = TYPICAL_SUBSTRATES[_substrate_key(finish)]
    return [m for m in ALL_MATERIALS if _matches(m, subs)]


__all__ = ["TYPICAL_SUBSTRATES", "typical_finishes", "typical_materials"]
