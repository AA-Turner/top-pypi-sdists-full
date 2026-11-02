"""Matrx Envelope `reference` resolution for graph data — an injection seam.

A workflow node may EMIT a Matrx Envelope reference (a pure pointer to an internal
resource — a udt table row, a file, a record) as part of its output, and a
downstream node may want that pointer RESOLVED to its live text before it acts on
it. Resolution is host-owned: the canonical `ReferenceOrchestrator` lives in the
aidream app (it knows the DB, ownership/RLS, and every resource type), which
matrx-graph must never import (package-independence rule).

So the host injects its resolver once at startup via
`configure_reference_resolver(...)`; graph code then calls `resolve_references(...)`
to materialize any embedded reference envelopes. Standalone (no host, no resolver
configured) this is a no-op passthrough — `import matrx_graph` and run a graph with
zero reference support, exactly as before.

This is deliberately OPT-IN, not an automatic "resolve every node input": a
deterministic node frequently WANTS the structured reference (the ids) to operate
on the resource directly, not a flattened text rendering. Only a node that needs the
human-readable value calls `resolve_references` on its inputs.

Detection is protocol-level (the generic `matrx_version` sentinel + `kind ==
"reference"` from docs/protocol/KIND_DIRECTIVES.md), never an aidream-specific schema
import. The injected resolver owns the actual decode + per-type dispatch + ownership
gate.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

logger = logging.getLogger(__name__)

# Signature the host registers: an async callable that takes one envelope dict and
# the acting user id and returns the resolved live text (or None when it cannot be
# honored — unknown shape, not owned, nothing to render).
ReferenceResolver = Callable[..., Awaitable[str | None]]

_resolver: ReferenceResolver | None = None

_SENTINEL = "matrx_version"  # the RETIRED shell's marker — read-only, stored content
_REFERENCE_KIND = "reference"
_KIND_KEY = "__kind"
_REFERENCE_SLUG_HEAD = "directive_v1_reference_"


def configure_reference_resolver(resolver: ReferenceResolver | None) -> None:
    """Register (or clear) the host's Matrx Envelope reference resolver.

    Called once at app startup by the host (aidream/package_integration.py) with
    `reference_orchestrator.resolve`. Passing None clears it (used by tests)."""
    global _resolver
    _resolver = resolver


def is_reference_resolver_configured() -> bool:
    return _resolver is not None


def is_reference_envelope(obj: Any) -> bool:
    """True when `obj` is a reference Kind Directive — the current two-key shell
    (`__kind: "directive_v1_reference_<noun>"`) or the RETIRED 4-key shell that
    stored content still carries. Adversarial finding F3: reading only the
    retired shell made graph-node resolution blind to every fence minted since
    the merge."""
    if not isinstance(obj, dict):
        return False
    slug = obj.get(_KIND_KEY)
    if isinstance(slug, str) and slug.startswith(_REFERENCE_SLUG_HEAD):
        return True
    return _SENTINEL in obj and obj.get("kind") == _REFERENCE_KIND


async def resolve_references(data: Any, *, user_id: str | None) -> Any:
    """Return a copy of `data` with every embedded `reference` envelope replaced by
    its live resolved text. Walks dicts and lists recursively.

    No-op passthrough when no resolver is configured (standalone) or when `data`
    carries no envelope sentinel at all (the cheap common case). An envelope that
    the resolver cannot honor (returns None / raises) is left UNCHANGED — fail open
    to the original pointer, never silently dropped."""
    if _resolver is None:
        return data
    # Cheap pre-filter: only pay the recursive walk when a sentinel is present.
    if not _contains_sentinel(data):
        return data
    return await _resolve_node(data, user_id=user_id)


def _contains_sentinel(data: Any) -> bool:
    if isinstance(data, dict):
        if _SENTINEL in data:
            return True
        slug = data.get(_KIND_KEY)
        if isinstance(slug, str) and slug.startswith(_REFERENCE_SLUG_HEAD):
            return True
        return any(_contains_sentinel(v) for v in data.values())
    if isinstance(data, list):
        return any(_contains_sentinel(v) for v in data)
    return False


async def _resolve_node(data: Any, *, user_id: str | None) -> Any:
    if is_reference_envelope(data):
        resolved = await _safe_resolve(data, user_id=user_id)
        # Keep the original envelope when nothing resolved (fail open).
        return resolved if resolved is not None else data
    if isinstance(data, dict):
        return {k: await _resolve_node(v, user_id=user_id) for k, v in data.items()}
    if isinstance(data, list):
        return [await _resolve_node(v, user_id=user_id) for v in data]
    return data


async def _safe_resolve(envelope: dict[str, Any], *, user_id: str | None) -> str | None:
    assert _resolver is not None
    try:
        return await _resolver(envelope, user_id=user_id)
    except Exception:  # noqa: BLE001 — a reference problem must never break the run.
        logger.warning(
            "reference resolution failed (type=%s) — leaving pointer unresolved",
            envelope.get("type"),
            exc_info=True,
        )
        return None
