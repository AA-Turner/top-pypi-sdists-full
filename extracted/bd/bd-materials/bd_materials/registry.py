"""Name -> material lookup: the string entry point to the catalog.

Lets a consumer assign a material by name -- ``part.material = "aluminum"`` -- without
importing a category module or a grade enum. :func:`resolve` turns that string into a
fresh :class:`~bd_materials.finished.FinishedMaterial`; :func:`canonical_name` turns one
back into a string, so an assignment round-trips through serialization.

:func:`factory` returns the family function *un-called* instead, for a caller that wants
the per-part arguments too -- ``factory("aluminum")(finish=anodize("blue"))``. Every
entry is a family function (with the grade pre-bound for a grade name), so the same
arguments work whichever name was used.

Two disjoint key sets, both **derived** from the catalog -- there is no hand-maintained
name table, so a new family function or grade is addressable by string the day it lands:

- **family names** -- every public family/species function of a catalog module
  (``aluminum``, ``mild_steel``, ``oak``, ``felt``, ``pla``, ...), resolving to that
  family's *default* grade. ``abs_`` is keyed ``abs`` (the trailing underscore only
  dodges the builtin).
- **grade names** -- every material's own ``name`` (``alu_g7075_t6``, ``hardwood_oak``,
  ``petg_cf``, ...), resolving to that exact grade.

Names are matched case-insensitively, with spaces and hyphens read as underscores
(``"Mild Steel"`` == ``"mild-steel"`` == ``"mild_steel"``).

The registry stores **factories, not instances**: a ``FinishedMaterial`` is mutable
(``.color``, ``.pbr``, ...), so a shared instance handed to every part would let one
part's tweak leak into another. Each :func:`resolve` call builds a new one.
"""

from __future__ import annotations

import difflib
import inspect
from collections.abc import Callable, Iterator
from functools import partial
from types import ModuleType
from typing import Any

from .core import RangeMaterial
from .finished import FinishedMaterial
from . import materials

# One catalog entry: a family function -- with its grade pre-bound when the key names a
# grade rather than a family. Callable with no arguments (every parameter is defaulted)
# and with the family function's per-part arguments (finish, color, density, ...).
Factory = Callable[..., "FinishedMaterial[Any]"]


def _normalize(name: str) -> str:
    """Fold a user-supplied name to its registry key (case/space/hyphen-insensitive)."""
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def _catalog_modules() -> tuple[ModuleType, ...]:
    """The category modules of the ``materials`` package, in declaration order."""
    return tuple(
        mod
        for name in materials.__all__
        if isinstance(mod := getattr(materials, name), ModuleType)
    )


def _family_functions() -> Iterator[tuple[str, Factory]]:
    """Yield every family/species function of the catalog, as ``(name, function)``.

    A catalog module's public functions *are* the family API: each takes only defaulted
    arguments and returns a ``FinishedMaterial``. ``custom_<category>`` is excluded --
    it builds a user-defined material and requires ``name``/``density``.

    Yields:
        The function's own name and the function.
    """
    for mod in _catalog_modules():
        for attr, fn in vars(mod).items():
            if attr.startswith("_") or attr.startswith("custom_"):
                continue
            # module-local functions only -- skip names imported from elsewhere
            if not inspect.isfunction(fn) or fn.__module__ != mod.__name__:
                continue
            yield attr, fn


def _family_factories() -> dict[str, Factory]:
    """Map each family/species function name to the function itself.

    Returns:
        Family name (trailing ``_`` removed) -> the family function.
    """
    return {_normalize(name.removesuffix("_")): fn for name, fn in _family_functions()}


def _functions_by_grade_enum() -> dict[type, Factory]:
    """Map each grade enum class to the family function that selects with it.

    Derived from the ``grade`` parameter's default (e.g. ``Alu.G6061_T6`` -> ``Alu``),
    so a grade name can bind the same function a family name does. Species shortcuts
    (``oak``, ``mdf``, ...) have no ``grade`` parameter -- their grade is already bound,
    and the family function they delegate to supplies the mapping.

    Returns:
        Grade enum class -> the family function taking it.
    """
    by_enum: dict[type, Factory] = {}
    for _name, fn in _family_functions():
        grade = inspect.signature(fn).parameters.get("grade")
        if grade is None:
            continue
        by_enum[type(grade.default)] = fn
    return by_enum


def _grade_factories() -> dict[str, Factory]:
    """Map each material's own ``name`` to its family function with the grade bound.

    Read off the ``<XXX>_MATERIALS`` dicts, which are keyed by grade -- so a grade name
    resolves through the same function (and accepts the same per-part arguments) as its
    family name.

    Returns:
        Normalized material name -> the family function with its grade pre-bound.

    Raises:
        ValueError: If a grade enum has no family function taking it.
    """
    by_enum = _functions_by_grade_enum()
    factories: dict[str, Factory] = {}
    for mod in _catalog_modules():
        for attr, table in vars(mod).items():
            if not attr.endswith("_MATERIALS") or not isinstance(table, dict):
                continue
            for grade, material in table.items():
                fn = by_enum.get(type(grade))
                if fn is None:
                    raise ValueError(
                        f"grade {grade!r} ({material.name}) has no family function -- "
                        "every grade enum must be some family function's grade default"
                    )
                # grade is the family functions' first positional parameter
                factories[_normalize(material.name)] = partial(fn, grade)
    return factories


def _build_registry() -> dict[str, Factory]:
    """Merge the family and grade key sets, rejecting collisions and gaps.

    Returns:
        The complete name -> factory registry.

    Raises:
        ValueError: If a family name and a grade name normalize to the same key (a
            name must have one meaning), or if some catalog material got no key.
    """
    families = _family_factories()
    grades = _grade_factories()
    if clashes := sorted(families.keys() & grades.keys()):
        raise ValueError(
            f"material name collision between a family function and a grade: {clashes}"
        )
    if missing := sorted(
        m.name for m in materials.ALL_MATERIALS if _normalize(m.name) not in grades
    ):
        raise ValueError(
            f"catalog materials unreachable by name: {missing} -- every material must "
            "live in a <XXX>_MATERIALS dict keyed by its grade"
        )
    return families | grades


# Built once at import: cheap (it stores functions, constructs no materials) and it
# fails loudly here rather than at the first lookup if the catalog grows a collision.
_REGISTRY: dict[str, Factory] = _build_registry()


def material_names() -> tuple[str, ...]:
    """Every name :func:`resolve` accepts, sorted.

    Returns:
        The family names (default grade) and grade names, as one sorted tuple.
    """
    return tuple(sorted(_REGISTRY))


def factory(name: str) -> Factory:
    """Look up the family function a material name stands for, un-called.

    The customizable counterpart to :func:`resolve`: it hands back the family function
    itself, so the per-part arguments can be passed as usual. A grade name yields the
    same function with its grade pre-bound, so both key sets take the same arguments::

        factory("aluminum")(finish=anodize("blue"))
        factory("Alu_G7075_T6")(density=2790)

    Args:
        name: A material name -- see :func:`material_names`; matched
            case-insensitively, with spaces/hyphens read as underscores.

    Returns:
        The family function for that name, callable with no arguments.

    Raises:
        TypeError: If ``name`` is not a string.
        ValueError: If the name is not in the catalog (the message lists the closest
            known names).
    """
    if not isinstance(name, str):
        raise TypeError(f"material name must be a string, not {type(name).__name__}")
    key = _normalize(name)
    entry = _REGISTRY.get(key)
    if entry is None:
        suggestions = difflib.get_close_matches(key, _REGISTRY, n=3)
        hint = ""
        if len(suggestions) > 0:
            hint = f" -- did you mean {' / '.join(suggestions)}?"
        raise ValueError(
            f"unknown material {name!r}{hint} "
            f"(bd_materials.material_names() lists all {len(_REGISTRY)})"
        )
    return entry


def resolve(
    material: str | FinishedMaterial[Any] | RangeMaterial,
) -> FinishedMaterial[Any]:
    """Resolve a material name to a fresh ``FinishedMaterial``.

    The string entry point to the catalog -- ``resolve("aluminum")`` is
    ``metals.aluminum()``, ``resolve("Alu_G7075_T6")`` is that specific grade. A
    ``FinishedMaterial`` passes through unchanged and a bare ``Material`` is wrapped,
    so a caller accepting "a material" in any of the three forms normalizes it with
    one call. Use :func:`factory` instead to pass per-part arguments.

    Every string lookup builds a new ``FinishedMaterial``, so per-part changes
    (``color``, ``pbr``, ...) never leak between parts.

    Args:
        material: A material name (see :func:`material_names`; matched
            case-insensitively, with spaces/hyphens read as underscores), an
            already-built ``FinishedMaterial``, or a bare range ``Material``.

    Returns:
        The ``FinishedMaterial`` for that material.

    Raises:
        TypeError: If ``material`` is not a string, ``FinishedMaterial`` or
            ``Material``.
        ValueError: If the name is not in the catalog (the message lists the
            closest known names).
    """
    if isinstance(material, FinishedMaterial):
        return material
    if isinstance(material, RangeMaterial):
        return FinishedMaterial(material)
    if not isinstance(material, str):
        raise TypeError(
            "material must be a name, a FinishedMaterial or a Material, not "
            f"{type(material).__name__}"
        )
    return factory(material)()


def canonical_name(material: FinishedMaterial[Any] | RangeMaterial) -> str:
    """The catalog name of a material, as accepted back by :func:`resolve`.

    Names the **material** only -- the per-part choices of a ``FinishedMaterial``
    (color, finish, process, thickness) are not encoded and are lost by a
    name round-trip. Always the *grade* name (``"Alu_G6061_T6"``), never the family
    name, so it stays exact if a family's default grade ever changes.

    Args:
        material: A ``FinishedMaterial`` or a bare range ``Material``.

    Returns:
        The material's catalog name.

    Raises:
        TypeError: If ``material`` is not a ``FinishedMaterial`` or ``Material``.
        ValueError: If the material is not in the catalog (a ``custom_*`` material
            has no registry entry, so its name would not resolve).
    """
    if not isinstance(material, FinishedMaterial | RangeMaterial):
        raise TypeError(
            "material must be a FinishedMaterial or a Material, not "
            f"{type(material).__name__}"
        )
    name = material.name  # both carry the material's catalog name
    if _normalize(name) not in _REGISTRY:
        raise ValueError(
            f"{name!r} is not a catalog material (user-defined materials have no "
            "registry entry), so it has no name resolve() would accept"
        )
    return name
