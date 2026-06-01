"""Loader for the frozen KSI starfield layout.

The starfield's node positions are computed ONCE (phyllotaxis theme
anchors + a light force-directed pass — see `scripts/build_starfield_layout.py`)
and FROZEN to a shipped data file, so the map is stable across runs and
platforms (spatial memory, consistent screenshots) and doesn't depend on
a float-sensitive layout sim reproducing identically everywhere. Positions
are normalized to [0, 1]; a renderer maps them onto its canvas.

Regenerate the data file when the KSI catalog changes:
    uv run python scripts/build_starfield_layout.py
"""

from __future__ import annotations

import importlib.resources
import json
from dataclasses import dataclass

_LAYOUT_PKG = "efterlev.studio"
LAYOUT_FILENAME = "starfield_layout.json"


@dataclass(frozen=True)
class StarNode:
    """One KSI's frozen position on the starfield."""

    ksi: str
    theme: str
    x: float  # normalized [0, 1]
    y: float  # normalized [0, 1]


@dataclass(frozen=True)
class StarfieldLayout:
    """The frozen layout: baseline + per-KSI star positions."""

    baseline: str
    nodes: dict[str, StarNode]

    def __len__(self) -> int:
        return len(self.nodes)


def load_starfield_layout() -> StarfieldLayout:
    """Read the bundled frozen layout. Works with no workspace."""
    raw = (
        importlib.resources.files(_LAYOUT_PKG).joinpath(LAYOUT_FILENAME).read_text(encoding="utf-8")
    )
    data = json.loads(raw)
    nodes = {
        ksi: StarNode(ksi=ksi, theme=n["theme"], x=float(n["x"]), y=float(n["y"]))
        for ksi, n in data["nodes"].items()
    }
    return StarfieldLayout(baseline=str(data["baseline"]), nodes=nodes)
