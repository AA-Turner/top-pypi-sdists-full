"""Kind correctors: a registered kind's value made to agree with its own rules, at PARSE time.

Some kinds carry a number the model states AND the inputs that number is derived from —
the Tough Editor's ``draft_critique`` states ``points``/``score``/``verdict`` beside the
rubric criteria they come from, and the brief says "the scale mapping is applied by code
from the points, so the score can never disagree with the rubric". A renderer must never
be the place that fixes it: there are several (a compiled bridge, a db component, the
generic fallback, the persisted-record view), and any one that forgets shows the person
the model's arithmetic.

So the correction happens once, where the kind's value is parsed
(``StreamBlockProcessor._run_parser`` for a complete ``kind`` block), BEFORE the ``__ir``
envelope is built from it — every renderer then routes by an envelope that already carries
the corrected value. The package holds only the registry; the host registers each
corrector (a package cannot import its host).

NEVER SILENT. Every change a corrector makes comes back as a plain-English line and rides
the block as ``metadata[KIND_CORRECTIONS_KEY]`` for the renderer to show, and is logged. A
corrector that cannot run leaves the value exactly as the model wrote it and says that it
could not be checked — it never blocks the render.
"""

from __future__ import annotations

import json
import logging
import re
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

#: Block metadata key carrying the corrections made to a kind's value.
KIND_CORRECTIONS_KEY = "kindCorrections"

#: value -> (corrected value, one plain-English line per change). Must not mutate its input.
KindCorrector = Callable[[dict[str, Any]], tuple[dict[str, Any], list[str]]]

_correctors: dict[str, KindCorrector] = {}

#: (answer text, the kind's CORRECTED value) -> (text with its prose agreeing, notes).
#: A kind whose value states a number the model may ALSO state in prose (a critique's
#: "6/10" beside a scorecard saying 7) registers one: the value is the authority, and
#: the prose's disagreeing number is rewritten and flagged. Must touch only prose.
KindProseCorrector = Callable[[str, dict[str, Any]], tuple[str, list[str]]]

_prose_correctors: dict[str, KindProseCorrector] = {}


def register_kind_prose_corrector(slug: str, corrector: KindProseCorrector) -> None:
    """Register (or replace) the prose corrector for one kind slug. Idempotent."""
    _prose_correctors[slug] = corrector


def unregister_kind_prose_corrector(slug: str) -> None:
    _prose_correctors.pop(slug, None)


def register_kind_corrector(slug: str, corrector: KindCorrector) -> None:
    """Register (or replace) the corrector for one kind slug. Idempotent."""
    _correctors[slug] = corrector


def unregister_kind_corrector(slug: str) -> None:
    _correctors.pop(slug, None)


def has_kind_corrector(slug: str) -> bool:
    return slug in _correctors


def correct_kind_value(value: Any) -> tuple[Any, list[str]]:
    """Apply the corrector registered for ``value["__kind"]``, if any.

    Returns ``(value, [])`` when there is nothing to do. A corrector that raises returns
    the original value and ONE line saying it could not be checked — loud, never blocking.
    """
    if not isinstance(value, dict):
        return value, []
    slug = value.get("__kind")
    corrector = _correctors.get(slug) if isinstance(slug, str) else None
    if corrector is None:
        return value, []
    try:
        corrected, notes = corrector(value)
    except Exception as exc:
        logger.error("kind corrector for %r failed: %s — value left as written", slug, exc)
        return value, [f"{slug} could not be checked against its own rules ({exc}); shown as written"]
    if notes:
        logger.warning("kind %r corrected at parse: %s", slug, "; ".join(notes))
    return corrected, list(notes)


# A JSON object the answer TEXT carries: a fenced ```json block or a bare ``` block
# (whose content must still parse as a registered kind's JSON), the body of an
# ``<artifact …>`` tag, or the whole text (structured-output mode answers bare JSON).
# Every fence is matched, so fences pair up left to right; only a json-labelled or
# unlabelled one is read — ```python and friends are left as written.
_FENCED = re.compile(r"(```([^\n`]*)\n)(.*?)(\n?```)", re.DOTALL)


def _fence_reads_as_json(label: str) -> bool:
    words = label.strip().lower().split()
    return not words or words[0] == "json"
_ARTIFACT = re.compile(r"(<artifact\b[^>]*>)(.*?)(</artifact>)", re.DOTALL | re.IGNORECASE)


def _correct_json_region(body: str, notes: list[str], seen: list[dict[str, Any]] | None = None) -> str:
    stripped = body.strip()
    if not stripped.startswith("{"):
        return body
    try:
        value = json.loads(stripped)
    except (ValueError, TypeError):
        return body
    corrected, changes = correct_kind_value(value)
    if seen is not None and isinstance(corrected, dict):
        seen.append(corrected)
    if not changes or corrected is value:
        return body
    notes.extend(changes)
    one_line = "\n" not in stripped
    rendered = json.dumps(corrected, ensure_ascii=False, separators=(",", ":")) if one_line else json.dumps(
        corrected, ensure_ascii=False, indent=2
    )
    lead = body[: len(body) - len(body.lstrip())]
    trail = body[len(body.rstrip()) :]
    return f"{lead}{rendered}{trail}"


def correct_kind_regions_in_text(text: str) -> tuple[str, list[str]]:
    """Correct every registered kind the answer TEXT carries, in place.

    ``correct_kind_value`` at parse time fixes the block a live stream renders, but the
    stored assistant text is what outlives the run, and some paths show that text as
    written (an artifact's source view, a copy of the raw answer, any consumer that
    re-parses it). So the same correction is applied to the durable text before it is
    written: fenced ```json blocks, ``<artifact>`` bodies, and a bare-JSON answer.
    Then the PROSE: for every kind value found (corrected or already consistent) whose
    kind registered a prose corrector, the text around the blocks is made to agree with
    the value — the value is the authority (``register_kind_prose_corrector``).
    Returns ``(text, [])`` when nothing changed. Never raises.
    """
    if not isinstance(text, str) or "__kind" not in text or not _correctors:
        return text, []
    notes: list[str] = []
    seen: list[dict[str, Any]] = []
    try:
        out = _FENCED.sub(
            lambda m: m.group(1) + _correct_json_region(m.group(3), notes, seen) + m.group(4)
            if _fence_reads_as_json(m.group(2))
            else m.group(0),
            text,
        )
        out = _ARTIFACT.sub(lambda m: m.group(1) + _correct_json_region(m.group(2), notes, seen) + m.group(3), out)
        if out.strip().startswith("{"):
            out = _correct_json_region(out, notes, seen)
        for value in seen:
            slug = value.get("__kind")
            prose = _prose_correctors.get(slug) if isinstance(slug, str) else None
            if prose is None:
                continue
            aligned, prose_notes = prose(out, value)
            if prose_notes and isinstance(aligned, str):
                out = aligned
                notes.extend(prose_notes)
    except Exception as exc:  # noqa: BLE001 — never block a write over a correction
        logger.error("kind text correction failed: %s — text left as written", exc)
        return text, []
    return out, notes


__all__ = [
    "KIND_CORRECTIONS_KEY",
    "correct_kind_regions_in_text",
    "KindCorrector",
    "KindProseCorrector",
    "correct_kind_value",
    "has_kind_corrector",
    "register_kind_corrector",
    "register_kind_prose_corrector",
    "unregister_kind_corrector",
    "unregister_kind_prose_corrector",
]
