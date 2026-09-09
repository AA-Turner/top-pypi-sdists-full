"""Wire-name conversion — the provider-safe serialization of tool names.

Tier-1 pure leaf (stdlib only — safe to import from anywhere, including
``config`` modules and provider translators).

The platform's canonical tool names are namespaced with a colon or, for
external MCP tools, dots (``bundle:list_supabase``, ``matrx-ai:shell``,
``mcp.docker-hub.listRepositoryTags`` — see
docs/cx_chat/TOOL_REGISTRY_REDESIGN.md §4 "Naming conventions"). Every
provider rejects ``:`` in a tool name (OpenAI/Anthropic enforce
``^[a-zA-Z0-9_-]{1,64}$``; Gemini is similarly strict), so a third name
layer exists purely for provider serialization:

    Canonical/Exposed  ``bundle:list_supabase``   (internal identity)
    Wire               ``bundle__list_supabase``  (what the model sees)

``:`` / ``.`` → ``__`` at serialization; the reverse mapping happens at dispatch
(``ToolExecutor``) by comparing the model-called name against the wire
form of every candidate internal name — never by naive string surgery,
so legitimate ``__`` in plain names can't be corrupted.

The conversion is applied at exactly two seams:
  - Outbound: ``BaseTranslator.build_provider_tools`` (declarations) and
    the ``ToolCallContent`` / ``ToolResultContent`` history serializers
    (replayed ``tool_use`` / ``functionCall`` / ``functionResponse``
    blocks — Gemini requires functionResponse.name to equal the
    functionCall name, i.e. the wire form).
  - Inbound: ``ToolExecutor.execute`` normalizes the model-called name
    back to the internal name before the allowlist/dispatch pipeline.

Everything between those seams — registry, alias map, config.tools,
persistence, traces — speaks internal names only.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

# The strictest provider constraint (OpenAI + Anthropic function names).
WIRE_SAFE_RE = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")

# One namespace separator on the internal plane; its wire spelling.
CANONICAL_SEPS = (":", ".")
WIRE_SEP = "__"


def to_wire_name(name: str) -> str:
    """Return the provider-safe wire form of an internal tool name.

    Idempotent: a name with no canonical separator is returned unchanged, so calling
    this on an already-wire-safe name (or twice) is a no-op.
    """
    wire = name
    for separator in CANONICAL_SEPS:
        wire = wire.replace(separator, WIRE_SEP)
    return wire


def is_wire_safe(name: str) -> bool:
    """True when ``name`` may be sent to a provider as-is."""
    return bool(WIRE_SAFE_RE.match(name))


def resolve_wire_name(called_name: str, candidates: Iterable[str]) -> str | None:
    """Reverse the wire transform: find the internal name among
    ``candidates`` whose wire form equals ``called_name``.

    Only separator-bearing candidates are considered — a candidate without a
    colon has an identical wire form and would already have matched by
    direct lookup, so re-matching it here would only mask lookup bugs.

    Returns the first match or ``None``. Ambiguity (two internal names
    sharing one wire form) is guarded at three layers: the merge primitive
    rejects inline specs that wire-collide with a registry tool
    (``_reject_wire_squatter``), ``ToolRegistry.ensure_registered`` refuses
    wire-colliding dynamic registrations, and the outbound seam screams and
    drops a same-request declaration collision. None of these covers two
    colliding CANONICAL rows loaded from the DB — the registry screams on
    that at load (see ``_load_rows``) but keeps both; the first match here
    is then order-dependent, which is why colliding canonical names must
    never be created.
    """
    if WIRE_SEP not in called_name:
        return None
    for candidate in candidates:
        if (
            any(separator in candidate for separator in CANONICAL_SEPS)
            and to_wire_name(candidate) == called_name
        ):
            return candidate
    return None
