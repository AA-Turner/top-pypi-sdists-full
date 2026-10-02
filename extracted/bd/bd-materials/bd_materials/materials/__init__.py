"""Range-based material catalogs, one module per category.

Each module exposes its grade enum(s), a public ``<XXX>_MATERIALS`` dict per family
(keyed by grade), family functions returning a ``FinishedMaterial``, an
``ALL_<CATEGORY>`` tuple, and its ``<Cat>Material`` dataclass. These modules are
re-exported at the package top level, so ``from bd_materials import metals`` works
as well as ``from bd_materials.materials import metals``.
"""

from __future__ import annotations

from . import glass, metals, paper, plastics, resins, textile, wood

# Flat registry of every catalog material -- lets top-level consumers (e.g.
# applicability queries) enumerate the whole catalog without a passed-in list.
ALL_MATERIALS = (
    *metals.ALL_METALS,
    *plastics.ALL_PLASTICS,
    *resins.ALL_RESINS,
    *glass.ALL_GLASSES,
    *wood.ALL_WOODS,
    *paper.ALL_PAPERS,
    *textile.ALL_TEXTILES,
)

__all__ = [
    "glass",
    "metals",
    "paper",
    "plastics",
    "resins",
    "textile",
    "wood",
    "ALL_MATERIALS",
]
