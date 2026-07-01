# SPDX-License-Identifier: MIT
# Copyright (c) 2021-2026
"""
Cross-implementation contracts shared by aiohomematic and py-openccu-loom-client.

This package is the single source of truth for behaviour that more than one
backend must reproduce identically. Each contract ships as:

- a golden fixture (``data/*_golden.json``) — the canonical ``input -> expected``
  cases, the authoritative artifact both consumers run; and
- a dependency-free reference implementation that the package tests validate
  against that fixture.

Currently shipped contracts:

- ``unique_id`` — the Home Assistant value-change routing key. See
  :mod:`aiohomematic_contract.unique_id`.

Load a fixture with :func:`load_golden_cases` (returns the parsed cases) or
:func:`golden_fixture_path` (returns the packaged file path). Public API of
this module is defined by ``__all__``.
"""

from importlib.resources import files
from importlib.resources.abc import Traversable
import json
from typing import Any, Final

from aiohomematic_contract.canonical import (
    LOOM_NAMESPACE,
    canonical_unique_id,
    serial_suffix,
)
from aiohomematic_contract.category import DataPointCategory, DataPointType
from aiohomematic_contract.command import CommandPriority
from aiohomematic_contract.const import VERSION
from aiohomematic_contract.slug import hub_slug
from aiohomematic_contract.unique_id import generate_channel_unique_id, generate_unique_id

__version__: Final = VERSION

__all__ = [
    "LOOM_NAMESPACE",
    "VERSION",
    "CommandPriority",
    "DataPointCategory",
    "DataPointType",
    "canonical_unique_id",
    "generate_channel_unique_id",
    "generate_unique_id",
    "golden_fixture_path",
    "hub_slug",
    "load_golden_cases",
    "serial_suffix",
]


def golden_fixture_path(name: str = "unique_id") -> Traversable:
    """Return the packaged path of the ``{name}_golden.json`` fixture."""
    return files("aiohomematic_contract.data") / f"{name}_golden.json"


def load_golden_cases(name: str = "unique_id") -> list[dict[str, Any]]:
    """Load and return the ``cases`` list from the ``{name}_golden.json`` fixture."""
    data = json.loads(golden_fixture_path(name).read_text(encoding="utf-8"))
    return list(data["cases"])
