"""Code-registered agent usages — the declaration collector.

Code-side agent references are real forward-looking usages that the platform's
Find Usages + Drift Detection system must see, but they live outside the DB.
This module is the single declaration point.

There is deliberately NO public "declare a hardcoded pin" API anymore
(``declare_pinned_agent`` / ``declare_floating_agent`` were deleted with the
pin-upgrade source-rewrite machinery, 2026-08-10). A code-side agent reference
is a MANDATE SEED: hosts declare it through the canonical slot wrapper
(aidream ``declare_mandated_agent``), which registers the mandate row AND calls
:func:`register_mandate_seed_usage` here so the Find Usages inventory stays
complete.

The declaration IS the source — registration returns the
``AgentRecordSource`` (or builtin id) the call site consumes, so the constant
and its registration can never diverge. ``source_system`` and ``code_path``
are derived from the calling module automatically.

Sync to ``public.agx_usage_registry`` happens in
``aidream/services/agent_usage/registry_sync.py`` (startup on real
deployments; ``POST /agent-usage/sync`` on demand). The registry rows feed the
``agx_usage_scan*`` RPCs as usage_type='code' and protect pinned versions from
``agx_purge_versions`` via an ON DELETE RESTRICT foreign key.

ref_kind:
    version  — pinned ``agx_version`` snapshot (drift-proof; the norm)
    agent    — floating ``agx_agent`` master (picks up every edit; drift-prone)
    builtin  — legacy prompt-system id (``Agent.from_builtin``); tracked for
               visibility only, excluded from agx drift joins.
"""

from __future__ import annotations

import inspect
from typing import Literal

from pydantic import BaseModel, ConfigDict

from matrx_ai.agents.named import AgentRecordSource


class CodeAgentUsage(BaseModel):
    """One declared code usage — mirrors a row of public.agx_usage_registry."""

    model_config = ConfigDict(frozen=True)

    usage_key: str
    source_system: Literal["matrx-ai", "aidream"]
    ref_kind: Literal["version", "agent", "builtin"]
    agent_version_id: str | None = None
    agent_id: str | None = None
    purpose: str
    code_path: str


_DECLARED: dict[str, CodeAgentUsage] = {}


def _caller_origin() -> tuple[Literal["matrx-ai", "aidream"], str]:
    """(source_system, code_path) of the first stack frame outside this module."""
    frame = inspect.currentframe()
    module = "unknown"
    while frame is not None:
        name = frame.f_globals.get("__name__", "")
        if name and name != __name__:
            module = name
            break
        frame = frame.f_back
    source: Literal["matrx-ai", "aidream"] = (
        "matrx-ai" if module.startswith("matrx_ai") else "aidream"
    )
    return source, module


def _register(usage: CodeAgentUsage) -> None:
    existing = _DECLARED.get(usage.usage_key)
    if existing is not None:
        if existing == usage:
            return  # identical re-declaration (module re-import) is a no-op
        raise ValueError(
            f"Agent usage key {usage.usage_key!r} declared twice with different "
            f"payloads:\n  existing: {existing!r}\n  new:      {usage!r}\n"
            f"Usage keys must be unique across matrx-ai and aidream."
        )
    _DECLARED[usage.usage_key] = usage


def register_mandate_seed_usage(
    usage_key: str,
    *,
    version_id: str | None = None,
    agent_id: str | None = None,
    master_agent_id: str | None = None,
    purpose: str,
) -> AgentRecordSource:
    """Register the Find Usages record for a slot's code SEED and return it.

    ONLY the canonical slot wrapper (aidream ``declare_mandated_agent``) calls
    this — it is the usage-registry half of a slot declaration, never a
    standalone way to hardcode an agent in application code. Exactly one of
    ``version_id`` (pinned ``agx_version`` snapshot) or ``agent_id`` (floating
    ``agx_agent`` master) must be given. ``master_agent_id`` is optional
    documentation for pinned seeds — the sync resolves the real master from the
    version row and screams if a provided master disagrees.
    """
    if bool(version_id) == bool(agent_id):
        raise ValueError(
            f"register_mandate_seed_usage({usage_key!r}): give exactly one of "
            f"version_id or agent_id"
        )
    source_system, code_path = _caller_origin()
    if version_id:
        _register(CodeAgentUsage(
            usage_key=usage_key,
            source_system=source_system,
            ref_kind="version",
            agent_version_id=version_id,
            agent_id=master_agent_id,
            purpose=purpose,
            code_path=code_path,
        ))
        return AgentRecordSource(agent_id=version_id, is_version=True)
    assert agent_id is not None
    _register(CodeAgentUsage(
        usage_key=usage_key,
        source_system=source_system,
        ref_kind="agent",
        agent_id=agent_id,
        purpose=purpose,
        code_path=code_path,
    ))
    return AgentRecordSource(agent_id=agent_id, is_version=False)



def declared_code_usages() -> tuple[CodeAgentUsage, ...]:
    """Every usage declared by modules imported so far (import order)."""
    return tuple(_DECLARED.values())


def declared_record_source_ids() -> set[str]:
    """All agx ids (version + master) declared so far — used by the sync's
    cross-check that no ``AgentRecordSource`` constant bypasses declaration."""
    ids: set[str] = set()
    for usage in _DECLARED.values():
        if usage.agent_version_id:
            ids.add(usage.agent_version_id)
        if usage.agent_id:
            ids.add(usage.agent_id)
    return ids
