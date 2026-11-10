"""Pins: what a project's Pinned area can hold, read from `pins.json` (codegen draws the server's,
CLI's and dashboard's enums from it; `ref_key_vectors.json` pins every side's ref key). Stdlib only."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

PINS_PATH = Path(__file__).with_name("pins.json")
REF_KEY_VECTORS_PATH = Path(__file__).with_name("ref_key_vectors.json")


@dataclass(frozen=True)
class PinTerm:
    """One named member of a list (a kind, a code), with why it exists."""

    name: str
    doc: str


@dataclass(frozen=True)
class PinKindSpec:
    """One pin kind and its ref's fields beside `kind` (field name -> type word)."""

    name: str
    doc: str
    ref: dict[str, str]


@dataclass(frozen=True)
class PinCap:
    """One cap: its snake_case name, its value and its unit in words."""

    name: str
    value: int
    doc: str


@dataclass(frozen=True)
class Pins:
    """The parsed `pins.json`."""

    doc: str
    kinds: tuple[PinKindSpec, ...]
    anchor_kinds: tuple[PinTerm, ...]
    metric_kinds: tuple[PinTerm, ...]
    error_codes: tuple[PinTerm, ...]
    caps: tuple[PinCap, ...]

    @classmethod
    def load(cls, path: Path = PINS_PATH) -> Pins:
        raw = json.loads(path.read_text(encoding="utf-8"))

        def read_terms(key: str) -> tuple[PinTerm, ...]:
            return tuple(PinTerm(item["name"], item["doc"]) for item in raw[key])

        return cls(
            doc=raw["doc"],
            kinds=tuple(PinKindSpec(k["name"], k["doc"], dict(k["ref"])) for k in raw["kinds"]),
            anchor_kinds=read_terms("anchor_kinds"),
            metric_kinds=read_terms("metric_kinds"),
            error_codes=read_terms("error_codes"),
            caps=tuple(PinCap(c["name"], int(c["value"]), c["doc"]) for c in raw["caps"]),
        )
