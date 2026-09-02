"""Rust (cargo) dependency-manifest parser: ``Cargo.toml``."""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover - exercised only on Python 3.10
    import tomli as tomllib


def parse_cargo(path: Path) -> list[str]:
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    names: list[str] = []
    for section in ("dependencies", "dev-dependencies", "build-dependencies"):
        names.extend((data.get(section) or {}).keys())
    return names


PARSERS: dict[str, Callable[[Path], list[str]]] = {
    "Cargo.toml": parse_cargo,
}
