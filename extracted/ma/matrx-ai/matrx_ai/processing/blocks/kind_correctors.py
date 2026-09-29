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

import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

#: Block metadata key carrying the corrections made to a kind's value.
KIND_CORRECTIONS_KEY = "kindCorrections"

#: value -> (corrected value, one plain-English line per change). Must not mutate its input.
KindCorrector = Callable[[dict[str, Any]], tuple[dict[str, Any], list[str]]]

_correctors: dict[str, KindCorrector] = {}


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


__all__ = [
    "KIND_CORRECTIONS_KEY",
    "KindCorrector",
    "correct_kind_value",
    "has_kind_corrector",
    "register_kind_corrector",
    "unregister_kind_corrector",
]
