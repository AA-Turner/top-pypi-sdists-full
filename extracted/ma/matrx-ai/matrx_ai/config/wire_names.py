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

import hashlib
import re
from collections.abc import Iterable

# The strictest provider constraint (OpenAI + Anthropic function names).
WIRE_SAFE_RE = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")

# The strictest provider limit, and how much of a longer name survives beside its digest.
WIRE_MAX_LEN = 64
WIRE_DIGEST_LEN = 8

# One namespace separator on the internal plane; its wire spelling.
CANONICAL_SEPS = (":", ".")
WIRE_SEP = "__"


def to_wire_name(name: str) -> str:
    """Return the provider-safe wire form of an internal tool name.

    Idempotent: a name with no canonical separator that fits is returned unchanged, so
    calling this on an already-wire-safe name (or twice) is a no-op.

    A form past the provider limit keeps its start and ends in a digest of the whole form.
    Connector tools carry names from someone else's server, so "rename it" is not available
    to them, and the digest keeps two long names with one prefix as two tools.
    """
    wire = name
    for separator in CANONICAL_SEPS:
        wire = wire.replace(separator, WIRE_SEP)
    if len(wire) > WIRE_MAX_LEN:
        digest = hashlib.sha256(wire.encode("utf-8")).hexdigest()[:WIRE_DIGEST_LEN]
        wire = f"{wire[: WIRE_MAX_LEN - WIRE_DIGEST_LEN - 1]}_{digest}"
    return wire


def is_wire_safe(name: str) -> bool:
    """True when ``name`` may be sent to a provider as-is."""
    return bool(WIRE_SAFE_RE.match(name))


def resolve_wire_name(called_name: str, candidates: Iterable[str]) -> str | None:
    """Reverse the wire transform: find the internal name among
    ``candidates`` whose wire form equals ``called_name``.

    Only candidates whose wire form differs from their name are considered — any
    other candidate would already have matched by direct lookup, so re-matching
    it here would only mask lookup bugs.

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
    for candidate in candidates:
        wire = to_wire_name(candidate)
        if wire != candidate and wire == called_name:
            return candidate
    return None


#: Namespaces a provider's model writes in FRONT of a function name when it names a tool inside an
#: argument (a gateway's ``job_key``) instead of calling it: OpenAI's models say ``functions.skill``
#: (measured 2026-11-19, chat-agent-skills FINDINGS 14). Never part of a tool's own name.
PROVIDER_NAMESPACES: tuple[str, ...] = ("functions",)


def strip_provider_namespace(reference: str) -> str:
    """``reference`` without one leading provider namespace (``functions.skill`` / ``functions__skill`` →
    ``skill``), stripped of whitespace; unchanged when it carries none."""
    ref = (reference or "").strip()
    wire = to_wire_name(ref)
    for namespace in PROVIDER_NAMESPACES:
        prefix = f"{namespace}{WIRE_SEP}"
        if wire.startswith(prefix) and len(wire) > len(prefix):
            return ref[len(namespace) + (1 if ref[len(namespace) : len(namespace) + 1] in CANONICAL_SEPS else 2) :]
    return ref


def resolve_tool_reference(reference: str, candidates: Iterable[str]) -> str | None:
    """The candidate (an internal name) a model meant by ``reference`` — the plain name, its wire name,
    or either behind a provider namespace — or ``None``. Exact identity wins, then the same wire form,
    then the same after one provider namespace is taken off. Never guesses beyond the candidates."""
    ref = (reference or "").strip()
    if not ref:
        return None
    names = list(candidates)
    for form in dict.fromkeys((ref, strip_provider_namespace(ref))):
        if form in names:
            return form
        wire = to_wire_name(form)
        for candidate in names:
            if to_wire_name(candidate) == wire:
                return candidate
    return None
