"""``prompt_safe_value`` — THE prompt door (plan §4.2; round-1 F4).

A prompt is an EXTERNAL MIND: one of exactly two places where stripping the
``__kind`` discriminator remains law (the other is external egress). Round-1
adversarial review proved the door existed only on one minor path
(``AgentVariable.get_value``) while the production chat/agent path templated
variables straight through ``str(value)`` — Python repr for dicts, markers
intact. The fix is the choke point: EVERY variable that becomes prompt text
flows through ``TextContent.replace_variables``, and that flow now calls this
one function. Callers do not need to remember the law; the door enforces it.

Rules:
- ``None`` → empty string (a template hole, not the word "None").
- Structured values (dict / list / tuple / set / pydantic models) → kind
  markers stripped, then CANONICAL JSON — models never see Python repr, and
  never learn our wire vocabulary.
- Scalars → ``str()`` unchanged.
- A value already serialized to a *string* by its producer is prose by that
  producer's choice and passes through verbatim — the door governs structured
  values, it does not re-parse text.
- A value carrying a ``__kind`` whose registration declares an ``ai_view`` is
  PROJECTED to those fields first. See below.

THE AI VIEW (Arman, 2026-08-24)
--------------------------------
A workflow step emits a kind and the author binds it to an agent variable.
Without this, the model receives the ENTIRE payload: for ``scraped_page`` that
is the markdown AND two other full-text renderings AND 1,473 link records AND
158 content blocks AND a 128-value minhash vector — hundreds of kilobytes to
say what the markdown already said. *"If you overdo it, then you're killing the
model's context window."*

The kind answers it itself: ``@kind(..., ai_view=(...))`` names the fields that
matter to a model, and this door applies the projection. No workflow author has
to know, no call site has to remember, and a kind with no declaration behaves
exactly as it always did — the whole payload travels.

The projection is deliberately SHALLOW and by-name only: it selects top-level
fields, it never reshapes or summarizes. Anything cleverer would be a
transformation hiding inside a serializer.
"""

from __future__ import annotations

import json
from typing import Any

__all__ = ["prompt_safe_value"]


def _jsonable(value: Any) -> Any:
    from pydantic import BaseModel

    if isinstance(value, BaseModel):
        # KindModel dumps carry __kind by design; the strip below removes it
        # at this door only.
        return value.model_dump(mode="json") if hasattr(value, "model_dump") else value
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_jsonable(v) for v in value]
    return value


def _ai_view_fields(payload: Any) -> tuple[str, ...] | None:
    """The declared ``ai_view`` for this payload's kind, if it has one.

    Reads the PROCESS-WIDE ``@kind`` catalog — sync, in-process, and populated
    at import by whichever kind modules the host loaded. Deliberately not the
    DB registry: this door is synchronous and on the hot path of every prompt,
    and a projection is a property of the declaration, not of a row.

    Never raises. A missing catalog, an unregistered kind, or any import
    problem means "no projection" — the whole payload travels, which is the
    behaviour that predates this function.
    """
    if not isinstance(payload, dict):
        return None
    slug = payload.get("__kind")
    if not isinstance(slug, str) or not slug:
        return None
    try:
        from matrx_graph.content_ir.sdk import kind_catalog

        registration = kind_catalog().get(slug)
    except Exception:
        return None
    return getattr(registration, "ai_view", None) or None


def _project(payload: Any) -> Any:
    """Apply a declared ``ai_view`` to one payload, and to nested kind items.

    A collection kind (``scraper_batch_result``) is mostly a list of item
    kinds, so projecting only the root would leave every page inside it at full
    size — the exact blow-up this exists to prevent. Recursion is one level per
    container, following the data, and any kind without a declaration is left
    untouched.
    """
    if isinstance(payload, list):
        return [_project(item) for item in payload]
    if not isinstance(payload, dict):
        return payload
    fields = _ai_view_fields(payload)
    source = payload if fields is None else {
        key: payload[key] for key in ("__kind", *fields) if key in payload
    }
    return {key: _project(inner) for key, inner in source.items()}


def prompt_safe_value(value: Any) -> str:
    """Render one variable value as prompt-safe text. See module doc."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (dict, list, tuple, set, frozenset)) or hasattr(
        value, "model_dump"
    ):
        from matrx_graph.content_ir.markers import strip_kind_markers

        try:
            return json.dumps(
                strip_kind_markers(_project(_jsonable(value))),
                ensure_ascii=False,
                default=str,
            )
        except (TypeError, ValueError):
            # Unserializable exotics: last-resort str(), which cannot carry a
            # structured marker anyway.
            return str(value)
    return str(value)
