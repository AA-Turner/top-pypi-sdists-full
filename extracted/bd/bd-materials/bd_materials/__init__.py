"""Range-based engineering-materials catalog for build123d.

Typical-value **ranges** (min-max) for the properties, not single points -- they
reflect the real spread across temper, product form and process. Materials are
reached through category namespaces; a family function returns a
:class:`FinishedMaterial`: ``.material`` is the physics (a shared, immutable range
table), ``.pbr`` is the three.js look.

    from bd_materials import metals, plastics, finishes
    from bd_materials.materials.metals import Alu

    metals.aluminum()                                  # FinishedMaterial (6061 default)
    metals.aluminum(Alu.G7075_T6, finishes.anodize("champagne"))
    plastics.pla(color="red")                          # selectable color
    plastics.pmma(color="clear", thickness_mm=3)       # transparent -> pane thickness

    print(metals.aluminum().material)                  # typical-value dump (__str__)
    metals.aluminum().pbr                              # resolved three.js look

Materials are also reachable **by name**, for consumers that assign one as a string::

    resolve("aluminum")                                # == metals.aluminum()
    resolve("Alu_G7075_T6")                            # a specific grade
    factory("aluminum")(finish=finishes.anodize("blue"))   # with per-part arguments
    material_names()                                   # every accepted name

Intrinsic identity (``family``, ``category``, ``transparent``) lives on the
``Material``; per-part choices (``color``, ``thickness_mm``, ``finish``,
``process``) live on the ``FinishedMaterial`` (``finish`` and ``process`` are
mutually exclusive). Each category exposes grade enums + family functions +
``ALL_<CATEGORY>`` + its ``<Cat>Material`` class. Shared primitives (``Range``,
``NOT_SUITABLE``, ``PROPERTY_UNITS``, ``RangeMaterial``) live in ``core``.
"""

from __future__ import annotations

from . import applicability, core, finishes, processes, registry
from .applicability import typical_finishes, typical_materials
from .finished import FinishedMaterial
from .processes import AppliedProcess, Process
from .registry import canonical_name, factory, material_names, resolve
from .materials import (
    glass,
    metals,
    paper,
    plastics,
    resins,
    textile,
    wood,
)

__all__ = [
    # category namespaces (the catalog)
    "metals",
    "plastics",
    "resins",
    "glass",
    "wood",
    "paper",
    "textile",
    # finishes / processes + shared core primitives
    "finishes",
    "processes",
    "core",
    # material<->finish applicability (advisory hints)
    "applicability",
    "typical_finishes",
    "typical_materials",
    # name -> material lookup (assign a material by string)
    "registry",
    "resolve",
    "factory",
    "material_names",
    "canonical_name",
    # user-facing types
    "FinishedMaterial",
    "AppliedProcess",
    "Process",
]
