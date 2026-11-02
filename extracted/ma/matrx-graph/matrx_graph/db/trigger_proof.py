"""Proof that a REAL RECORD CHANGE started a run — and that it is still that run.

WHY (lane 11 rounds 2–3, 2026-10-02). ``workflow.run`` metadata, status, input and
definition_version_id are writable by the run's owner through PostgREST; so are
``workflow.trigger_fire`` and ``workflow.trigger_event`` (measured on the clone). So
``metadata.trigger_id`` — and ``metadata.stopped`` / ``status`` — are DISPLAY VALUES the owner
can write, never authority. What the owner cannot write: ``workflow.trigger`` and the store's
outbox ``custom.io_outbox``.

THE PROOF. Only the EventWatcher's store-trigger fire stamps ``metadata.trigger_proof`` — an
HMAC over ``run_id | trigger_id | definition_id | definition_version_id | definition_hash |
organization_id | owner | change_id | input_hash`` under a key derived from the platform secret
(``matrx_orm.secrets_battery.keyed_digest``). ``input_hash`` is sha256 of the canonical JSON of
``run.input`` plus the execution keys of ``metadata._settings`` (:func:`input_hash`). A manual
fire or "Test with a record" never gets one (it runs as the caller). Key material:
``CREDENTIALS_ENCRYPTION_KEY`` when set, else the battery's documented fallback to
``SUPABASE_SECRET_KEY`` — so a server cannot prove (and standing-rule writes are held) only when
NEITHER is configured.

WHAT THE PROOF IS FOR NOW (round 5). It marks which runs a verified store fire created, so
:func:`prior_proven_run` can refuse a second run for one change. It is NOT what decides a
standing-rule write: persisted engine state is owner-writable (WF-028), so
:func:`standing_rule` decides from memory — the :class:`StandingLeg` token the host's fire
enters around the one leg it starts in-process, the scheduler's in-memory record of that leg
(fresh, the compiled graph's hash, no replayed steps), the trigger and outbox row re-read
through the server, and deny-by-default lineage over the graph actually running.
"""

from __future__ import annotations

import hmac
import json
import logging
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

#: The keyed-digest purpose. A constant: changing it invalidates every stamped proof.
TRIGGER_PROOF_PURPOSE = "workflow.run.store_change.v3"
#: Where the server stamps it on ``workflow.run.metadata``.
TRIGGER_PROOF_KEY = "trigger_proof"


def _message(**fields: Any) -> str:
    order = (
        "run_id",
        "trigger_id",
        "definition_id",
        "definition_version_id",
        "definition_hash",
        "organization_id",
        "owner_id",
        "change_id",
        "input_hash",
    )
    return "|".join(str(fields.get(k) or "") for k in order)


def trigger_proof(
    *,
    run_id: str,
    trigger_id: str,
    definition_id: str,
    definition_version_id: str | None,
    definition_hash: str,
    organization_id: str,
    owner_id: str,
    change_id: str,
    input_hash: str,
) -> str:
    """The hex proof stamped on a run a real store change started. Raises when no platform
    secret can be derived — a run is never stamped with a proof nobody can check."""
    from matrx_orm.secrets_battery import keyed_digest

    return keyed_digest(
        TRIGGER_PROOF_PURPOSE,
        _message(
            run_id=run_id,
            trigger_id=trigger_id,
            definition_id=definition_id,
            definition_version_id=definition_version_id,
            definition_hash=definition_hash,
            organization_id=organization_id,
            owner_id=owner_id,
            change_id=change_id,
            input_hash=input_hash,
        ),
    ).hex()


def proof_matches(proof: Any, **fields: Any) -> bool:
    """Constant-time check of a stamped proof against the fields it must bind."""
    if not isinstance(proof, str) or not proof:
        return False
    try:
        expected = trigger_proof(**fields)
    except Exception:  # noqa: BLE001 — no platform secret: nothing can be proven
        logger.warning("trigger proof: no platform secret to check a proof against; refusing")
        return False
    return hmac.compare_digest(proof, expected)


def _json(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except ValueError:
            return value
    return value


#: The run.metadata._settings keys that feed what a run executes (the worker and the
#: awaiting_input resume read them). Bound with run.input in the input hash.
EXECUTION_SETTINGS = ("input_values", "node_inputs", "initial_variables")


def _canonical_numbers(value: Any) -> Any:
    """Numbers as JSONB gives them back: an integral float is an int (``1e20`` → ``10**20``,
    ``-0.0`` → ``0``), so a value that survives the round trip hashes the same."""
    if isinstance(value, bool):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, dict):
        return {str(k): _canonical_numbers(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_canonical_numbers(v) for v in value]
    return value


def input_hash(run_input: Any, metadata: Any) -> str:
    """sha256 of the canonical JSON (sorted keys) of what the run executes on: ``run.input``
    plus the execution keys of ``metadata._settings``. Any resume or restart that changes
    either — an awaiting_input resume writes ``_settings.input_values`` — changes it."""
    import hashlib

    meta = _json(metadata) or {}
    settings = (meta.get("_settings") if isinstance(meta, dict) else None) or {}
    body = {
        "input": _json(run_input) or {},
        "settings": {k: settings.get(k) for k in EXECUTION_SETTINGS},
    }
    canonical = json.dumps(_canonical_numbers(body), sort_keys=True, separators=(",", ":"),
                           default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _run_proof_fields(run: dict[str, Any], trigger: Any, change_id: str) -> dict[str, Any]:
    return {
        "run_id": str(run.get("id")),
        "trigger_id": str(trigger.id),
        "definition_id": str(run.get("definition_id") or ""),
        "definition_version_id": run.get("definition_version_id"),
        "definition_hash": str(run.get("definition_hash") or ""),
        "organization_id": str(run.get("organization_id") or ""),
        "owner_id": str(run.get("created_by") or ""),
        "change_id": change_id,
        "input_hash": input_hash(run.get("input"), run.get("metadata")),
    }


def _trigger_backs_run(trigger: Any, run: dict[str, Any]) -> bool:
    if trigger is None or not trigger.is_active or trigger.kind != "event":
        return False
    if (trigger.event_source or {}).get("source") != "store":
        return False
    if str(trigger.created_by or "") != str(run.get("created_by") or ""):
        return False
    if str(trigger.definition_id) != str(run.get("definition_id") or ""):
        return False
    return str(trigger.organization_id or "") == str(run.get("organization_id") or "")


# ─── The standing leg (lane 11 round 5) ─────────────────────────────────────────────────
#
# TRUST NOTHING PERSISTED. Checkpoints, node outcomes, run input and metadata are writable by
# the run's owner (WF-028), and the recovery doors (retry with inputs / config_override,
# manual-result, resume, resume-paused) feed them back into a run. So a write is the owner's
# standing rule ONLY inside the one leg the host's verified store fire started in THIS process:
# the host enters :func:`standing_leg` around that leg (never persisted, never read back),
# and the scheduler's own in-memory record of the leg (``executor.execution``) says it is a
# FRESH leg on the graph the fire compiled, with no step filled from a stored outcome. Every
# other leg — any resume, retry, manual result, recovery sweep, timer wake, or a leg on
# another process — has no token, and its writes follow the organization's approval setting.

#: The sentence a write step carries when it ran outside the standing leg.
# ─── THE KILL SWITCH (lane 11 round 8) ─────────────────────────────────────────────────
#
# OFF. The round-7 verifier BLOCKED the standing-rule exemption: workflow.trigger's columns
# (event_source, definition_version_id, is_active, default_inputs, max_steps) are
# client-updatable, so a co-editor or the owner's own session can re-point what a "standing
# rule" runs. Until the exemption is re-built on the platform's approval mechanism and an
# independent verify passes, EVERY standing-rule write follows the organization's hold.
# A code constant on purpose — never an env var, a knob, or anything a client can reach.
# Turning it on is the coordinator's call after that verify.
STANDING_RULE_ENABLED = False

#: The one run-log sentence while the switch is off.
NOT_YET_APPROVED = "Workflow writes ask first until this workflow is approved."

RESUMED_LEG = (
    "this part of the run was resumed, retried or restarted, so its writes follow the "
    "approval setting"
)


@dataclass(frozen=True)
class StandingLeg:
    run_id: str
    trigger_id: str
    change_id: str
    owner_id: str
    definition_hash: str
    #: The compiled graph the fire built, handed to the leg in memory (never re-read).
    graph: Any = field(default=None, compare=False, repr=False)


_standing_leg: ContextVar[StandingLeg | None] = ContextVar("matrx_standing_leg", default=None)


def current_standing_leg() -> StandingLeg | None:
    return _standing_leg.get()


@contextmanager
def standing_leg(leg: StandingLeg) -> Iterator[StandingLeg]:
    """Entered ONLY by the host's verified store fire, around the leg it starts in-process."""
    token = _standing_leg.set(leg)
    try:
        yield leg
    finally:
        _standing_leg.reset(token)


# ─── Lineage: deny-by-default (``NodeSpec.values_are``) ─────────────────────────────────
#
# A step's output is 'deterministic', 'outside' (http: the owner's design) or 'ai' — and a
# step that never declared counts as 'ai'. ``tool.call`` is judged by the step it calls
# (``action_name``); one whose target cannot be resolved statically counts as 'ai'.
# "Upstream" is every edge ancestor plus every writer of a channel an ancestor reads; a node
# fed by a kind subscription (``trigger_kind``) can be fed by any node, so then the whole
# graph is upstream.


def _config_value(node: Any, key: str) -> Any:
    config = getattr(node, "config", None)
    value = getattr(config, key, None) if config is not None else None
    if value is None and config is not None and hasattr(config, "model_extra"):
        value = (config.model_extra or {}).get(key)
    if value is None:
        value = (getattr(node, "static_inputs", None) or {}).get(key)
    return value


def values_are(node: Any, registry: Any) -> tuple[str, str]:
    """``(value, why)`` for one compiled step."""
    spec_type = str(getattr(node, "spec_type", "") or "")
    try:
        spec = registry.get(spec_type).spec
    except Exception:  # noqa: BLE001 — unknown to this registry: cannot vouch for it
        return "ai", f"{spec_type} (a step this server does not know)"
    if spec_type == "tool.call":
        target = _config_value(node, "action_name") or _config_value(node, "tool_name")
        if not isinstance(target, str) or not registry.has(target):
            return "ai", "tool.call (its target cannot be resolved before it runs)"
        return values_are(type("_Step", (), {"spec_type": target, "config": None,
                                             "static_inputs": {}})(), registry)
    return str(spec.values_are), spec_type


#: The config field a STATIC dispatcher names its launch target in (control.map / send / loop /
#: work_queue declare it in their config schema). Read off each spec, never a list of types.
LAUNCH_TARGET_FIELD = "target_node_id"


def launches_statically(spec: Any) -> bool:
    """A spec whose config names the node it launches (no edge carries that launch)."""
    schema = getattr(spec, "config_schema", None)
    return LAUNCH_TARGET_FIELD in (getattr(schema, "model_fields", None) or {})


def launches_anything(spec: Any) -> bool:
    """A spec declared to ``ctx.send`` to targets its config does not name."""
    return bool(getattr(spec, "launches_nodes", False))


def _launch_edges(graph: Any, registry: Any) -> tuple[list[tuple[str, str]], bool]:
    """``(dispatcher, target)`` pairs from static dispatchers, and whether any node may
    launch anything at all (then every node is upstream of every node)."""
    pairs: list[tuple[str, str]] = []
    wild = False
    if registry is None:
        return pairs, wild
    for nid, node in (getattr(graph, "nodes", {}) or {}).items():
        try:
            spec = registry.get(str(getattr(node, "spec_type", "") or "")).spec
        except Exception:  # noqa: BLE001 — an unknown step may launch anything
            wild = True
            continue
        if launches_anything(spec):
            wild = True
        if launches_statically(spec):
            target = _config_value(node, LAUNCH_TARGET_FIELD)
            if isinstance(target, str) and target:
                pairs.append((nid, target))
    return pairs, wild


def upstream_of(graph: Any, node_id: str, registry: Any = None) -> set[str]:
    """Every step whose output can reach ``node_id``: edge ancestors, writers of channels an
    ancestor reads, and — round 6, B1 — LAUNCHES: a dispatcher whose config names a target
    (For Each / Send / Loop / work queue) is upstream of that target, with its own upstream;
    a node that may launch anything (``launches_nodes``) or a kind subscription makes the
    whole graph upstream."""
    nodes = getattr(graph, "nodes", {}) or {}
    edges = [(e.source_node_id, e.target_node_id)
             for e in (getattr(graph, "edges", {}) or {}).values()]
    launches, wild = _launch_edges(graph, registry)
    if wild:
        return set(nodes) - {node_id}
    edges += launches
    writers: dict[str, set[str]] = {}
    for nid, node in nodes.items():
        for channel in getattr(node, "writes_channels", ()) or ():
            writers.setdefault(channel, set()).add(nid)
    seen: set[str] = set()
    frontier = [node_id]
    while frontier:
        current = frontier.pop()
        node = nodes.get(current)
        if node is not None and getattr(node, "trigger_kind", None):
            return set(nodes) - {node_id}
        sources = {src for src, tgt in edges if tgt == current}
        for channel in (getattr(node, "reads_channels", ()) or ()) if node is not None else ():
            sources |= writers.get(channel, set())
        for source in sources - seen - {node_id}:
            seen.add(source)
            frontier.append(source)
    return seen


def ai_lineage(graph: Any, node_id: str, registry: Any) -> list[str]:
    """Every upstream step of ``node_id`` whose values are (or count as) AI."""
    nodes = getattr(graph, "nodes", {}) or {}
    found: list[str] = []
    for upstream in sorted(upstream_of(graph, node_id, registry)):
        node = nodes.get(upstream)
        value, why = values_are(node, registry) if node is not None else ("ai", "unknown")
        if value == "ai":
            found.append(f"{upstream}: {why}")
    return found


class StandingRule:
    """The verdict for one write: a trigger when it is the owner's standing rule, else the
    sentence saying why not."""

    def __init__(self, trigger: Any | None, why_not: str | None) -> None:
        self.trigger = trigger
        self.why_not = why_not


async def standing_rule(run_id: str, *, owner_id: str, write_node_id: str | None) -> StandingRule:
    """Is this write — by step ``write_node_id`` of run ``run_id`` — the owner's standing rule?

    Decided from memory, never from persisted engine state: the standing-leg token the host's
    verified fire entered, and the scheduler's record of the leg it is driving. The trigger
    and the store's outbox row are re-read through the server (neither is client-writable).
    """
    from matrx_graph import default_registry
    from matrx_graph.db.store_change import StoreChangeRefused, read_store_change, refusal_for
    from matrx_graph.db.trigger_store import TriggerStore
    from matrx_graph.executor.execution import current_execution

    if not STANDING_RULE_ENABLED:
        return StandingRule(None, NOT_YET_APPROVED)
    leg = current_standing_leg()
    execution = current_execution()
    if (
        leg is None
        or leg.run_id != str(run_id)
        or execution is None
        or execution.run_id != str(run_id)
        or not execution.fresh
    ):
        return StandingRule(None, RESUMED_LEG)
    if execution.definition_hash != leg.definition_hash:
        return StandingRule(None, "the workflow running is not the one its trigger started")
    if leg.owner_id != str(owner_id):
        return StandingRule(None, "this run does not run as the trigger's owner")
    trigger = await TriggerStore().load(leg.trigger_id)
    if (
        trigger is None
        or not trigger.is_active
        or trigger.kind != "event"
        or (trigger.event_source or {}).get("source") != "store"
        or str(trigger.created_by or "") != leg.owner_id
    ):
        return StandingRule(None, "the trigger that started this run is off or changed hands")
    try:
        row = await read_store_change(leg.change_id)
    except StoreChangeRefused:
        row = None
    if row is None or refusal_for(trigger, row, leg.change_id) is not None:
        return StandingRule(None, "the record change that started this run is not in the store")
    if execution.replayed:
        return StandingRule(
            None,
            "steps of this run were filled from stored results instead of running here: "
            + ", ".join(sorted(execution.replayed)),
        )
    nodes = getattr(execution.graph, "nodes", {}) or {}
    if not write_node_id or write_node_id not in nodes:
        return StandingRule(None, "this step is not in the workflow its trigger started")
    lineage = ai_lineage(execution.graph, write_node_id, default_registry())
    if lineage:
        return StandingRule(None, "an AI step shapes this write: " + "; ".join(lineage))
    return StandingRule(trigger, None)


async def proven_trigger(run_id: str, *, owner_id: str, write_node_id: str | None) -> Any | None:
    """The trigger when the write is the owner's standing rule, else None."""
    verdict = await standing_rule(run_id, owner_id=owner_id, write_node_id=write_node_id)
    return verdict.trigger


async def prior_proven_run(trigger: Any, change_id: str) -> str | None:
    """The run this trigger already PROVABLY made for this change, or None.

    Candidate runs are found by their metadata (which the owner can write), but one counts
    only if its proof checks out — so a forged run can never block the real one.
    """
    from matrx_orm import Compare, F, JsonPath

    from matrx_graph.db._registry import get_model

    rows = await (
        get_model("WfRun")
        .filter(
            Compare(JsonPath(F("metadata"), "trigger_id"), "=", str(trigger.id)),
            Compare(JsonPath(F("metadata"), "change_id"), "=", str(change_id)),
            deleted_at__isnull=True,
        )
        .values("id", "definition_id", "definition_version_id", "definition_hash",
                "organization_id", "created_by", "metadata", "input")
    )
    for row in rows:
        run = {
            k: (str(v) if v is not None and k not in ("metadata", "input") else v)
            for k, v in dict(row).items()
        }
        metadata = _json(run.get("metadata")) or {}
        if proof_matches(
            metadata.get(TRIGGER_PROOF_KEY), **_run_proof_fields(run, trigger, str(change_id))
        ):
            return str(run["id"])
    return None


__all__ = [
    "EXECUTION_SETTINGS",
    "NOT_YET_APPROVED",
    "RESUMED_LEG",
    "STANDING_RULE_ENABLED",
    "StandingLeg",
    "StandingRule",
    "current_standing_leg",
    "standing_leg",
    "values_are",
    "ai_lineage",
    "input_hash",
    "standing_rule",
    "upstream_of",
    "launches_anything",
    "launches_statically",
    "TRIGGER_PROOF_KEY",
    "TRIGGER_PROOF_PURPOSE",
    "prior_proven_run",
    "proof_matches",
    "proven_trigger",
    "trigger_proof",
]
