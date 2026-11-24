"""THE CATALOG WALK for Gemini picture counts (CGU-10 IMG9 #6).

The class a Gemini's picture lands in is decided from its own facts (``vision_classes``: generation +
``capabilities.output``). This module walks a LOADED catalog — the server's, never a frozen list —
and checks every picture-reading Gemini row against what Google was measured to count, so a row the
catalog gains is checked the day it appears instead of never.

* ``MEASURED`` — Google's ``countTokens`` for one 1,536² picture at the model's default resolution
  (2026-11-11, AND-IMG8/AND-V IMG9 probes). Evidence, not the rule: the rule never reads it.
* A picture-reading row that is neither measured nor socket-only is a FINDING ("unmeasured"): measure
  it (``matrx_ai.providers.google.picture_count.measure_picture_tokens``) and add it here.
* SOCKET-ONLY models (``-live``, ``native-audio``, ``-streaming`` — e.g. ``gemini-3.8-live``,
  ``gemini-3.8-live-extended-thinking``, ``gemini-robotics-er-2-streaming-preview``) answer only over
  the Live socket: ``countTokens`` refuses them, so their count cannot be measured this way. They are
  classed by the same rule as every other row — a 3.x text/audio maker counts by resolution
  (``gemini3_high``) — which is INFERRED, not measured. If Google in fact counts them flat, the
  estimate is high (the safe direction: a fit is never promised that the provider refuses), and the
  Live setup carries resolution per SESSION, never per part, so no per-part ``mediaResolution`` 400
  is possible there. Row 213's camera turn is "measured" only once a live-socket probe confirms it.

Opt-in live re-measure: ``MATRX_LIVE_GEMINI=1`` with ``GEMINI_API_KEY`` (free ``countTokens``).
"""

from __future__ import annotations

import re
from typing import Any

#: Google's count for one 1,536² picture (default resolution). 258 = the flat class.
MEASURED: dict[str, int] = {
    "gemini-2.5-flash": 258,
    "gemini-2.5-pro": 258,
    "gemini-2.5-flash-image": 258,
    "gemini-3-flash-preview": 1_089,
    "gemini-3-pro-image": 258,
    "gemini-3.1-flash-image": 258,
    "gemini-3.1-flash-lite": 1_089,
    "gemini-3.1-flash-lite-image": 258,  # AND-V IMG9 live: 258, and 400 on a per-part mediaResolution
    "gemini-3.1-pro-preview": 1_089,
    "gemini-3.5-flash": 1_089,
    "gemini-3.5-flash-lite": 1_089,
    "gemini-3.6-flash": 1_089,
    "gemini-3.7-flash": 1_089,
    "gemini-3.8-flash": 1_089,
    "gemini-4-argon": 1_120,
    "gemini-flash-latest": 1_089,
    "gemini-flash-lite-latest": 1_089,
    "gemini-pro-latest": 1_089,
    "gemini-nano-banana-2.1": 258,
    "gemini-omni-1.1-flash": 258,
    "gemini-omni-flash-preview": 258,
    "gemini-robotics-er-2-preview": 1_089,
    # AND-IMG11, 2026-11-11: deprecated but still offered (so still walked) — 258 at 300² and 1,536².
    "gemini-3-pro-image-preview": 258,
    "gemini-3.1-flash-image-preview": 258,
    # AND-IMG10 walk, 2026-11-11 (first run over the server catalog): a 2.5 that TILES. Classed
    # ``gemini25_tiled`` by its catalog facts (2.x + ``computer_use``) since AND-IMG11; every size in
    # ``TILED_MEASURED`` below is checked against the rule.
    "gemini-2.5-computer-use-preview-10-2025": 1_290,
}
#: Google's ``countTokens`` for a TILING Gemini at many sizes (CGU-10 AND-IMG11, 2026-11-11, solid JPEGs).
#: The tiled rule must reproduce every one EXACTLY — this is the evidence it was fitted to.
TILED_MEASURED: dict[str, dict[tuple[int, int], int]] = {
    "gemini-2.5-computer-use-preview-10-2025": {
        (256, 256): 258, (384, 384): 258, (385, 385): 1_290, (384, 385): 1_290, (385, 200): 774,
        (1_000, 200): 1_548, (2_000, 300): 3_354, (600, 600): 1_290, (768, 768): 1_290,
        (1_152, 1_152): 1_290, (1_153, 1_153): 1_290, (1_536, 1_536): 1_290, (1_537, 1_537): 2_580,
        (2_304, 2_304): 2_580, (3_000, 1_000): 2_838, (1_440, 900): 1_806, (800, 1_280): 1_806,
        (1_920, 1_080): 1_806, (4_000, 4_000): 3_354, (100, 5_000): 3_354, (1_000, 100): 2_838,
        (500, 100): 1_548, (600, 150): 1_290, (2_304, 1_536): 1_806, (3_072, 1_536): 2_322,
        (3_072, 2_304): 3_354, (3_840, 2_304): 3_354, (3_840, 768): 3_354, (2_560, 1_440): 2_322,
        (1_920, 1_200): 1_806, (1_280, 720): 1_806, (1_024, 768): 1_290, (770, 770): 1_290,
        (769, 769): 1_290, (400, 100): 1_290, (300, 100): 1_032, (384, 50): 2_322, (255, 1_000): 1_290,
        # AND-IMG12, 2026-11-11: 47 sizes the rule was NOT fitted to — extreme ratios, the 384² edge, the
        # 12-tile ceiling, screenshots, and exact 2:1 pictures (770×385 … 2,000×1,000: Google FLOORS the tile).
        (1, 384): 3_354, (384, 1): 3_354, (2, 1_000): 3_354, (50, 2_000): 3_354, (8_000, 1_000): 3_354,
        (384, 386): 1_290, (383, 385): 1_290, (257, 385): 1_290, (3_000, 3_000): 3_354, (5_000, 5_000): 3_354,
        (7_680, 4_320): 3_354, (770, 385): 2_322, (1_000, 500): 2_322, (1_100, 550): 2_322, (1_540, 770): 2_322,
        (2_000, 1_000): 2_322, (1_080, 2_400): 2_322, (1_170, 2_532): 2_322, (1_290, 2_796): 2_322,
        (1_080, 1_920): 1_806, (750, 1_334): 1_806, (1_440, 3_200): 2_838, (1_179, 2_556): 2_322,
        (720, 1_600): 2_322, (1_366, 768): 1_806, (1_536, 864): 1_806, (1_680, 1_050): 1_806, (2_880, 1_800): 3_354,
        (3_024, 1_964): 3_354, (3_456, 2_234): 3_354, (2_560, 1_600): 3_354, (3_840, 2_160): 3_354,
        (1_600, 900): 1_806, (256, 512): 774, (512, 256): 774, (385, 770): 2_322, (500, 1_000): 2_322,
        (1_200, 600): 1_806, (1_500, 500): 2_838, (900, 300): 2_322, (768, 1_024): 1_290, (2_048, 1_536): 1_806,
        (4_096, 2_048): 3_354, (640, 480): 1_290, (800, 600): 1_290, (1_000, 1_000): 1_290, (1_543, 771): 2_322,
    },
}
FLAT = 258
#: The published per-picture ceiling a resolution-reading Gemini may count at its default resolution.
RESOLUTION_CEILING = 1_120
_SOCKET_ONLY = re.compile(r"(?:^|-)(?:live|native-audio|streaming)(?:-|$)")
_NOT_A_PICTURE_READER_OUTPUTS = frozenset({"embedding"})


def is_socket_only(name: str) -> bool:
    """A Gemini that answers only over the Live socket (``countTokens`` refuses it)."""
    return bool(_SOCKET_ONLY.search(name))


def _still_offered(catalog: Any, model_id: Any) -> bool:
    """A deprecated row is still callable while the catalog routes it to an available offering."""
    try:
        return bool(model_id) and bool(catalog.offerings_for(str(model_id)))
    except Exception:  # noqa: BLE001 — a catalog that cannot say is treated as "not offered"
        return False


def picture_reading_geminis(catalog: Any) -> list[dict[str, Any]]:
    """Every CALLABLE Gemini row the catalog says reads pictures and makes something other than an
    embedding, by name (``google/`` / ``models/`` stripped), sorted. Callable = not retired, and either
    not deprecated or still holding an available offering (CGU-10 AND-IMG11: a deprecated row a person
    can still run — ``gemini-3.1-flash-image-preview`` — still gets pictures, so it is still walked)."""
    rows: dict[str, dict[str, Any]] = {}
    for row in (catalog.model_states() or {}).values():
        name = str(row.get("name") or "").strip().lower().removeprefix("models/").removeprefix("google/")
        if not name.startswith("gemini-") or row.get("retired_at"):
            continue
        if row.get("is_deprecated") and not _still_offered(catalog, row.get("id")):
            continue
        caps = row.get("capabilities") or {}
        inputs = {str(i).lower() for i in caps.get("input") or ()}
        outputs = {str(o).lower() for o in caps.get("output") or ()}
        if "image" not in inputs or (outputs and outputs <= _NOT_A_PICTURE_READER_OUTPUTS):
            continue
        rows[name] = {"name": name, "outputs": sorted(outputs), "id": row.get("id")}
    return [rows[n] for n in sorted(rows)]


def expected_count(name: str) -> tuple[str, int, int]:
    """What the RULE says a 1,536² picture costs on ``name`` (read through the process catalog):
    ``(class name, estimate, by_resolution as 0/1)``."""
    from matrx_ai.processing.vision.image_tokens import image_tokens
    from matrx_ai.processing.vision.vision_classes import (
        gemini_reads_by_resolution,
        resolve_vision_class,
    )

    cls = resolve_vision_class(name, "google_chat")
    return cls.name, image_tokens(1536, 1536, cls, name), int(gemini_reads_by_resolution(name))


def walk_findings(catalog: Any, *, measured: dict[str, int] | None = None) -> tuple[list[str], dict[str, str]]:
    """Walk every picture-reading Gemini in ``catalog`` (which must be the process catalog the rule
    reads, or one with the same rows). Returns ``(findings, notes)``: a finding is a measured row the
    rule classes against Google's count, or a row nobody measured; a note is a socket-only row's
    inferred class."""
    measured = MEASURED if measured is None else measured
    findings: list[str] = []
    notes: dict[str, str] = {}
    for row in picture_reading_geminis(catalog):
        name = row["name"]
        cls_name, estimate, by_resolution = expected_count(name)
        if name in measured:
            count = measured[name]
            if count == FLAT and (by_resolution or estimate != FLAT):
                findings.append(f"{name}: Google counts a flat {FLAT}; the rule classes it {cls_name} ({estimate})")
            elif cls_name == "gemini25_tiled":
                if by_resolution or estimate != count:
                    findings.append(f"{name}: Google counts {count} by tiles; the rule classes it {cls_name} ({estimate})")
            elif count != FLAT and not (by_resolution and count <= estimate <= RESOLUTION_CEILING):
                findings.append(f"{name}: Google counts {count} by resolution; the rule classes it {cls_name} ({estimate})")
        elif is_socket_only(name):
            notes[name] = f"socket-only: classed {cls_name} ({estimate}) from its own facts — inferred, not measured"
        else:
            findings.append(
                f"{name}: picture-reading Gemini nobody measured (rule: {cls_name}, {estimate}); measure it "
                "with providers.google.picture_count.measure_picture_tokens and add it to MEASURED"
            )
    return findings, notes


__all__ = [
    "FLAT",
    "MEASURED",
    "TILED_MEASURED",
    "expected_count",
    "is_socket_only",
    "picture_reading_geminis",
    "walk_findings",
]
