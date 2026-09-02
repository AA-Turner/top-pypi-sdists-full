"""Kinds for the ``random_wheel`` tool result.

Ledger row (KIND_TOOL_LEDGER, agent ``lead-w2b``): ``random_wheel``.

WHY ``wheel_image`` IS NOT ``stock_image``. A registered ``stock_image`` kind
exists (family ``media``, declared in ``aidream/kinds/media.py``), but a
package may never import aidream (``check_package_boundaries.py``), and
re-declaring the same slug here would fork the declaration. More to the point,
the wheel does not RETURN a stock image — its resolver deliberately projects a
narrower display payload (one url + thumb + attribution) out of the full
Unsplash record. That projection is its own honest shape, named for what it is.

``chosen.value`` is ``Any`` by design: in ``list`` mode it is the caller's own
item value, in ``web`` mode a fresh search digest, in ``image`` mode a caption
— the resolver contract (``SeedResolution.value``) is open, and declaring it
narrower would be a lie about the extension point.

All PLACEHOLDER tier: the spin envelope is fully captured; the one opaque
field (``chosen.value``) is opaque by contract, not by neglect.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "wheel_choice",
    label="Wheel Choice",
    family="tool_execution",
    example={"label": "The contrarian view", "value": "The contrarian view"},
    maturity="placeholder",
)
class WheelChoice(KindModel):
    """The face the wheel landed on, and what that face resolved to."""

    label: str = ""
    #: list mode: the item's own value · web mode: the fetched digest ·
    #: image mode: a display caption. Open by resolver contract.
    value: Any | None = None


@kind(
    "wheel_image",
    label="Wheel Image",
    family="tool_execution",
    example={
        "url": "https://images.unsplash.com/photo-abc?w=1080",
        "thumb": "https://images.unsplash.com/photo-abc?w=200",
        "photographer_name": "Jane Doe",
        "photographer_url": "https://unsplash.com/@janedoe",
        "description": "Northern lights over a fjord",
        "source": "unsplash",
    },
    maturity="placeholder",
)
class WheelImage(KindModel):
    """The wheel's display projection of the randomly-picked stock photo."""

    url: str = ""
    thumb: str = ""
    photographer_name: str | None = None
    photographer_url: str | None = None
    description: str | None = None
    source: str = ""


@kind(
    "wheel_spin_result",
    label="Wheel Spin",
    family="tool_execution",
    example={
        "mode": "list",
        "title": "Spin the wheel",
        "chosen": {
            "__kind": "wheel_choice",
            "label": "The contrarian view",
            "value": "The contrarian view",
        },
        "candidates": ["The contrarian view", "A lesson from nature"],
        "winner_index": 0,
        "pool_size": 30,
        "display_count": 2,
        "spin_duration_ms": 2400,
        "seed": None,
        "sources": None,
        "image": None,
    },
    maturity="placeholder",
)
class WheelSpinResult(KindModel):
    """One true-random wheel spin: the faces shown, the winner, the resolution."""

    mode: str = ""
    title: str = ""
    chosen: WheelChoice = WheelChoice()
    candidates: list[str] = []
    winner_index: int = 0
    #: Size of the FULL pool the faces were sampled from (>= len(candidates)).
    pool_size: int = 0
    display_count: int = 0
    spin_duration_ms: int = 0
    #: web/image modes only: the seed phrase the winning face carried.
    seed: str | None = None
    #: Reserved by the resolver contract (``SeedResolution.sources``); today's
    #: resolvers return None or [] — declared so a future resolver's citations
    #: are not a validation failure.
    sources: list[Any] | None = None
    #: image mode only.
    image: WheelImage | None = None
