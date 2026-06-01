"""Enforce alphabetical-by-name ordering on every handwritten SDK enum.

Generated enums under ``smplkit._generated`` are out of our hands — they
mirror the OpenAPI spec verbatim. Anything in the handwritten wrapper
layer is ours to police, and we want a single declared ordering rule
so customers see consistent autocomplete order across the SDK.

Enums whose members have a meaningful natural order — severity, time,
sequence, etc. — are listed in :data:`_ORDERED_BY_DOMAIN` and exempted
from the alphabetical rule. Each exemption has its own dedicated test
elsewhere in the suite that pins down the domain ordering it should
follow.
"""

from __future__ import annotations

import enum
import importlib
import pkgutil

import pytest

import smplkit
from smplkit import LogLevel


# Enums whose declared order encodes a domain meaning. ``LogLevel`` is
# declared in ascending order of severity (TRACE → SILENT) so the
# autocomplete order matches the conceptual progression — and the
# canonical ordering is independently asserted below.
_ORDERED_BY_DOMAIN: frozenset[type[enum.Enum]] = frozenset({LogLevel})


def _handwritten_enums():
    """Yield every Enum subclass declared in the handwritten wrapper layer."""
    seen: set[type[enum.Enum]] = set()
    # Include the package's own __init__.py (e.g. ``LogLevel``) plus every
    # non-_generated submodule.
    module_names = ["smplkit"] + [
        m.name for m in pkgutil.walk_packages(smplkit.__path__, prefix="smplkit.") if "_generated" not in m.name
    ]
    for name in module_names:
        try:
            module = importlib.import_module(name)
        except Exception:
            continue
        for attr in vars(module).values():
            if (
                isinstance(attr, type)
                and issubclass(attr, enum.Enum)
                and attr is not enum.Enum
                and attr.__module__ == name
                and attr not in seen
            ):
                seen.add(attr)
                yield attr


_ENUM_PARAMS = sorted(_handwritten_enums(), key=lambda e: f"{e.__module__}.{e.__name__}")


@pytest.mark.parametrize("enum_cls", _ENUM_PARAMS, ids=lambda e: f"{e.__module__}.{e.__name__}")
def test_enum_members_are_alphabetical(enum_cls):
    if enum_cls in _ORDERED_BY_DOMAIN:
        pytest.skip(f"{enum_cls.__name__} is domain-ordered; see _ORDERED_BY_DOMAIN")
    names = [m.name for m in enum_cls]
    assert names == sorted(names), (
        f"{enum_cls.__module__}.{enum_cls.__name__} members are not alphabetical: "
        f"declared {names}, should be {sorted(names)}"
    )


def test_at_least_one_enum_discovered():
    # Sanity: the walker found the enums we know about; if not, the test
    # above would pass vacuously.
    assert len(_ENUM_PARAMS) >= 4


def test_log_level_is_ordered_by_ascending_severity():
    """``LogLevel`` declaration order must match Python ``logging`` severity.

    Iteration over ``LogLevel`` returns members in declared order, and
    customer code (severity comparisons, dropdown UIs, ``min``/``max``
    over enabled levels) reads this order as the canonical progression
    from least to most restrictive.
    """
    from smplkit.logging._levels import SMPL_TO_PYTHON

    declared = [m.name for m in LogLevel]
    expected = sorted(declared, key=lambda name: SMPL_TO_PYTHON[name])
    assert declared == expected, (
        f"LogLevel members are not in ascending severity order: declared {declared}, should be {expected}"
    )
