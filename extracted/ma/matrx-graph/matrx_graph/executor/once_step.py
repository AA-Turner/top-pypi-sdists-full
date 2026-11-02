"""The scheduler's half of run once per key (``data.once``): decide before paying, settle after.

Called from ``Scheduler._execute_invocation_body`` at exactly two points and cleaned up by
``Scheduler._execute_invocation``:

* :func:`decide` — after the step's inputs are resolved and validated, before ``node_started``.
  Reuses a stored success (records the ``reused`` outcome, emits ``node_completed`` with
  ``source="reused"``, returns True), or holds the key's claim for this invocation (returns
  False — the step runs), or waits while another invocation holds it. Anything that makes the
  key unusable (a missing key part, no organization, an AI step that cannot name its version, a
  store error) runs the step normally and says why — a review flag on the step, never silence.
  Only the store's own calls fall back like that; a failure of the run's machinery while reusing
  (emit, record the outcome) propagates like any step's. A reused result that holds values on the
  server (``hold_on_server``) brings them into this run, or is a miss when they are gone.
* :func:`settle` — after the success outcome is recorded: the result is stored under the claim.
* :func:`finish` — always (``finally``): stops the lease renewer; a claim never settled (failure,
  interrupt, cancel, routable failure, unstorable result) is released so the next run pays.

Pure orchestration over ``matrx_graph.once`` — the store owns every compare-and-swap.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from matrx_graph.once import (
    Claim,
    ClaimPosition,
    Hit,
    StepResultKey,
    StepResultStoreError,
    StoredResult,
    Wait,
    acquire,
    file_ids_in,
    get_file_identity_resolver,
    get_step_result_store,
    input_digest,
    result_key,
    settings_digest,
)
from matrx_graph.types.primitives import NodeCategory

if TYPE_CHECKING:
    from matrx_graph.executor.scheduler import Invocation, Scheduler, _StepResult

logger = logging.getLogger(__name__)

#: Step categories whose answer depends on something outside their inputs (an agent, a model, a
#: prompt, the child workflow a ``subgraph.call`` runs). Such a step reuses only when its executor
#: names that version (``result_version``).
_VERSIONED_CATEGORIES = (NodeCategory.AGENT, NodeCategory.LLM, NodeCategory.SUBGRAPH)


@dataclass(slots=True)
class OnceSlot:
    """Per-invocation state, created by ``Scheduler._execute_invocation``."""

    decided: bool = False
    claim: Claim | None = None
    key: StepResultKey | None = None
    digest: str | None = None


async def _flag(
    scheduler: Scheduler, run_id: str, invocation: Invocation, *, step: int, attempt: int,
    label: str, message: str, payload: dict[str, Any] | None = None,
) -> None:
    await scheduler._raise_review(
        run_id, invocation, step=step, attempt=attempt, label=label, message=message,
        category="unexpected_path", payload=payload,
    )


def _scope_id(scheduler: Scheduler, scope: str, run_id: str, organization_id: str) -> str | None:
    if scope == "run":
        return run_id
    if scope == "organization":
        return organization_id
    return scheduler.definition_id or None


async def _store_failed(
    scheduler: Scheduler, run_id: str, invocation: Invocation, *, step: int, attempt: int, exc: BaseException,
) -> bool:
    """The step-result store failed: the step runs (pay rather than block the run) and the run
    SAYS so — a review flag on the step, never only a server log line."""
    logger.error("[wf:%s node=%s] run once per key FAILED to decide — running the step: %s: %s",
                 run_id[:8], invocation.node_id, type(exc).__name__, exc, exc_info=exc)
    await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label="engine.once_unavailable",
                message=f"Run once per key could not reach its saved results ({type(exc).__name__}); the step ran",
                payload={"error": f"{type(exc).__name__}: {str(exc)[:300]}"})
    return False


async def _renew_forever(claim: Claim, lease_seconds: int) -> None:
    key, token = claim.key, claim.token
    store = get_step_result_store()
    interval = max(lease_seconds / 3.0, 0.05)
    while True:
        await asyncio.sleep(interval)
        try:
            ok = await store.renew(
                key, token=token, lease_until=datetime.now(UTC) + timedelta(seconds=lease_seconds)
            )
        except Exception:  # noqa: BLE001 — keep trying; the lease is the safety net
            logger.exception("[wf once] lease renewal failed for %s/%s", key.step_type, key.result_key[:12])
            continue
        if not ok and (claim.settling or claim.settled):
            return  # the result landed under this claim — that cleared it, nobody took it over
        if not ok:
            logger.error(
                "[wf once] LOST the claim on %s key %s — its lease expired and another run took it "
                "over. This invocation keeps running; its result will not be stored.",
                key.step_type, key.result_key[:12],
            )
            return


async def decide(
    scheduler: Scheduler,
    slot: OnceSlot,
    *,
    run_id: str,
    step: int,
    attempt: int,
    invocation: Invocation,
    node: Any,
    spec: Any,
    executor: Any,
    ctx: Any,
    inputs_model: Any,
    digest_inputs: dict[str, Any],
    config_model: Any,
    config_dump: dict[str, Any],
    started_inputs: dict[str, Any],
    result: _StepResult,
    invocation_count: int,
    organization_id: str | None = None,
) -> bool:
    """True when a stored result was reused (the caller returns without executing).

    ``organization_id`` is the organization the step works in when ``data.in_organization`` moves
    it (already admitted by the scheduler); None = the run's. A saved result never crosses
    organizations, so it is keyed to the one the step actually ran in."""
    from matrx_graph.knobs import once_knobs

    slot.decided = True
    policy = node.once
    organization_id = organization_id or str(getattr(scheduler.app, "organization_id", "") or "")
    if not organization_id:
        logger.error(
            "[wf:%s node=%s] run once per key is OFF for this step: the run carries no "
            "organization, and a stored result never crosses organizations.",
            run_id[:8], invocation.node_id,
        )
        await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label="engine.once_unavailable",
                    message="Run once per key could not apply: the run has no organization")
        return False
    scope_id = _scope_id(scheduler, policy.scope, run_id, organization_id)
    if not scope_id:
        await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label="engine.once_unavailable",
                    message=f"Run once per key could not apply: scope '{policy.scope}' has no id in this run")
        return False
    actor = str(getattr(scheduler.app, "user_id", "") or "")
    key_value, missing = result_key(
        spec.node_type, policy, digest_inputs,
        settings=settings_digest(config_dump, node.output_kind), actor=actor,
    )
    if key_value is None:
        await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label="engine.once_key_missing",
                    message=f"Run once per key could not build a key: missing {', '.join(missing)}",
                    payload={"missing": missing})
        return False

    version_fn = getattr(executor, "result_version", None)
    version: str | None = None
    if callable(version_fn):
        try:
            version = await version_fn(ctx, inputs_model, config_model)
        except Exception as exc:  # noqa: BLE001 — the step itself will surface a real problem
            logger.warning("[wf:%s node=%s] result_version failed (%s) — running without reuse",
                           run_id[:8], invocation.node_id, exc)
            await _flag(scheduler, run_id, invocation, step=step, attempt=attempt,
                        label="engine.once_unversioned",
                        message=f"Run once per key could not tell which version would answer ({exc}); the step ran",
                        payload={"error": f"{type(exc).__name__}: {str(exc)[:300]}"})
            return False
    elif spec.category in _VERSIONED_CATEGORIES:
        await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label="engine.once_unversioned",
                    message=(f"'{spec.node_type}' cannot say which agent or model version answers it, so "
                             "a saved result is never reused for it; the step ran"))
        return False

    file_identities = await _file_identities(
        scheduler, run_id, invocation, step=step, attempt=attempt,
        file_ids=file_ids_in(digest_inputs), organization_id=organization_id,
    )
    if file_identities is None:
        return False
    digest = input_digest(
        inputs=digest_inputs, config=config_dump, output_kind=node.output_kind,
        step_version=str(getattr(spec, "version", "") or ""), result_version=version,
        file_identities=file_identities,
    )
    key = StepResultKey(
        organization_id=organization_id, scope=policy.scope, scope_id=str(scope_id),
        step_type=spec.node_type, result_key=key_value,
    )
    slot.key, slot.digest = key, digest
    knobs = await once_knobs()
    store = get_step_result_store()
    position = ClaimPosition(run_id=run_id, node_id=invocation.node_id,
                             dispatch_id=invocation.dispatch_id, item_index=invocation.item_index)
    bypass = bool(invocation.bypass_once)
    # A stored result this invocation found unusable (values gone, shape changed): only THAT one
    # is ignored from here on, so a fresh result another run settles meanwhile is reused.
    unusable_at: datetime | None = None
    announced_wait = False
    # Only the STORE's calls fall back to running the step. A failure of the run's own machinery
    # while reusing (emitting, recording the outcome) propagates like it does for any step —
    # answering it by paying for the step announced it completed twice and paid anyway.
    while True:
        try:
            decision = await acquire(
                store, key, digest=digest, position=position, lease_seconds=knobs.lease_seconds,
                reuse_changed=policy.on_changed_inputs == "reuse_and_flag", bypass=bypass,
                unusable_at=unusable_at,
            )
        except Exception as exc:  # noqa: BLE001 — the store is down: pay rather than block the run
            return await _store_failed(scheduler, run_id, invocation, step=step, attempt=attempt, exc=exc)
        if isinstance(decision, Wait):
            if not announced_wait:
                announced_wait = True
                holder = decision.holder
                logger.info(
                    "[wf:%s node=%s] waiting: run %s step %s is producing the same %s result",
                    run_id[:8], invocation.node_id, (holder.run_id[:8] if holder else "?"),
                    (holder.node_id if holder else "?"), spec.node_type,
                )
            try:
                await store.wait(key, float(knobs.wait_poll_seconds))
            except Exception as exc:  # noqa: BLE001
                return await _store_failed(scheduler, run_id, invocation, step=step, attempt=attempt, exc=exc)
            continue
        if isinstance(decision, Hit):
            try:
                reused = await _reuse(
                    scheduler, decision, run_id=run_id, step=step, attempt=attempt, invocation=invocation,
                    node=node, spec=spec, started_inputs=started_inputs, result=result,
                    invocation_count=invocation_count,
                )
            except StepResultStoreError as exc:
                return await _store_failed(scheduler, run_id, invocation, step=step, attempt=attempt, exc=exc)
            if reused:
                return True
            unusable_at = decision.result.succeeded_at
            continue
        slot.claim = decision
        decision.renewer = asyncio.create_task(
            _renew_forever(decision, knobs.lease_seconds),
            name=f"wf-once-lease:{invocation.node_id}",
        )
        replacing = decision.replacing
        changed = replacing is not None and replacing.input_digest != digest
        if not invocation.bypass_once and (replacing is None or changed):
            # This step ran before in this scope (under this key or any other) and its saved answer
            # was not reused: say which upstream step changed its input. A true first run is silent.
            if await _explain_miss(scheduler, run_id, invocation, node=node, step=step, attempt=attempt,
                                   key=key, replacing=replacing, inputs=digest_inputs,
                                   limit=knobs.miss_compare_limit):
                return False
        if changed and not invocation.bypass_once:
            await _flag(
                scheduler, run_id, invocation, step=step, attempt=attempt, label="engine.once_inputs_changed",
                message=("Same key, different inputs: the saved result was produced from other inputs, "
                         "so the step ran again and its result replaces the saved one"),
                payload={"origin_run_id": replacing.origin_run_id, "origin_node_id": replacing.origin_node_id},
            )
        return False


MISSED_UPSTREAM_LABEL = "engine.once_missed_upstream"


def _run_input_digest(scheduler: Scheduler) -> str | None:
    """What this run was started with — its subject (inputs, per-step inputs, the input surface,
    run variables). None on a leg that did not start the run (a resume): unknown, never guessed."""
    started = getattr(scheduler, "_once_run_inputs", None)
    if not isinstance(started, dict):
        return None
    from matrx_graph.once import _sha

    return _sha({**started, "surface": getattr(scheduler, "_run_inputs", {}),
                 "variables": getattr(scheduler, "_run_variables", {})})


def _reused_in_run(scheduler: Scheduler) -> set[str]:
    """Steps of this run whose answer was a reused saved result (not paid for here)."""
    found = getattr(scheduler, "_once_reused_node_ids", None)
    if found is None:
        found = set()
        scheduler._once_reused_node_ids = found  # type: ignore[attr-defined]
    return found


def _differing_fields(mine: dict[str, Any], theirs: dict[str, Any]) -> list[str]:
    from matrx_graph.once import _canonical

    return sorted(k for k in set(mine) | set(theirs)
                  if k not in mine or k not in theirs or _canonical(mine[k]) != _canonical(theirs[k]))


def _fresh_answerers(scheduler: Scheduler, start: str) -> set[str] | None:
    """The nearest steps at or above ``start`` that answered in THIS run without reusing and can
    answer the same input differently (anything but a PURE step). None when there are none."""
    from matrx_graph.types.primitives import ActionTier

    graph, reused = scheduler.graph, _reused_in_run(scheduler)
    found: set[str] = set()
    seen: set[str] = set()
    stack = [start]
    while stack:
        nid = stack.pop()
        if nid in seen or nid not in graph.nodes:
            continue
        seen.add(nid)
        node = graph.nodes[nid]
        try:
            pure = scheduler.registry.get(node.spec_type).spec.determinism is ActionTier.PURE
        except Exception:  # noqa: BLE001 — an unknown step is not blamed
            pure = True
        if not pure and nid not in reused:
            found.add(nid)
            continue
        stack.extend(graph.edges[e].source_node_id for e in node.incoming_edge_ids if e in graph.edges)
    return found or None


async def _explain_miss(
    scheduler: Scheduler, run_id: str, invocation: Invocation, *, node: Any, step: int, attempt: int,
    key: StepResultKey, replacing: StoredResult | None, inputs: dict[str, Any], limit: int,
) -> bool:
    """This step has an earlier saved answer in its scope (under this key, else under any key)
    that was not reused: when every field that differs from the closest earlier input arrives over
    a connection from a step that ran fresh here and is not PURE, say so on the step (one flag per
    step per run) and return True. No earlier saved answer (a true first run), a field the step set
    itself, or one no fresh step feeds: False, nothing said here. Never raises."""
    try:
        graph = scheduler.graph
        subject = _run_input_digest(scheduler)
        if limit <= 0 or subject is None or not node.incoming_edge_ids:
            return False
        if not any(_fresh_answerers(scheduler, graph.edges[e].source_node_id)
                   for e in node.incoming_edge_ids if e in graph.edges):
            return False  # nothing above this step paid for a fresh answer
        if replacing is not None:
            priors = [replacing]
        else:
            recent = getattr(get_step_result_store(), "recent_results", None)
            priors = await recent(key, node_id=invocation.node_id, limit=limit) if recent is not None else []
        best: tuple[list[str], str] | None = None
        for prior in priors:
            # Only an answer saved by a run started with the SAME inputs (same brand, topic, child
            # input) is one this run could have reused; another subject's answer is not a miss.
            if prior.origin_run_id == run_id or prior.run_input_digest != subject:
                continue
            outcome = await scheduler.checkpointer.get_outcome(
                prior.origin_run_id, prior.origin_step, prior.origin_node_id, prior.origin_attempt,
                prior.origin_dispatch_id, prior.origin_item_index,
            )
            if outcome is None or not isinstance(outcome.inputs, dict):
                continue
            fields = _differing_fields(inputs, outcome.inputs)
            if fields and (best is None or len(fields) < len(best[0])):
                best = (fields, prior.origin_run_id)
        if best is None:
            return False  # no earlier saved answer for this step: a true first run
        fields, compared_run_id = best
        culprits: set[str] = set()
        for name in fields:
            sources = []
            for eid in node.incoming_edge_ids:
                edge = graph.edges.get(eid)
                if edge is None:
                    continue
                carried = set(edge.mappings) if edge.mappings else (
                    {edge.target_handle} if edge.target_handle in inputs else None)
                if carried is None or name in carried:
                    sources.append(edge.source_node_id)
            blamed = set().union(*(_fresh_answerers(scheduler, s) or set() for s in sources))
            if not blamed:
                return False  # this field changed for a reason other than a fresh upstream answer
            culprits |= blamed
        upstream = sorted(culprits)

        def _name(nid: str) -> str:
            return graph.nodes[nid].label or nid

        mine = node.label or invocation.node_id
        names = ", ".join(_name(n) for n in upstream)
        message = (f"Run once missed: {mine} got a different input because {names} ran fresh "
                   f"in this run, so its saved answer was not reused.")
        from matrx_graph.executor.review_flags import ReviewFlag

        await scheduler._review.raise_flag(
            run_id,
            ReviewFlag(
                node_id=invocation.node_id, step=step, attempt=attempt, label=MISSED_UPSTREAM_LABEL,
                message=message, category="unexpected_path", source="engine",
                payload={"upstream": upstream, "fields": fields, "compared_run_id": compared_run_id},
                occurrence_key=f"{MISSED_UPSTREAM_LABEL}|{invocation.node_id}",
            ),
        )
        return True
    except Exception:  # noqa: BLE001 — explaining a miss never fails the step
        logger.exception("[wf:%s node=%s] could not explain a run-once miss", run_id[:8], invocation.node_id)
        return False


async def _file_identities(
    scheduler: Scheduler, run_id: str, invocation: Invocation, *, step: int, attempt: int,
    file_ids: set[str], organization_id: str,
) -> dict[str, str] | None:
    """Each referenced file's CONTENT identity (never its id alone), or None — the step then
    runs, never reuses, and is flagged — when any file cannot be identified."""
    if not file_ids:
        return {}
    resolver = get_file_identity_resolver()
    reason: str | None = None
    found: dict[str, str | None] = {}
    if resolver is None:
        reason = "this server cannot tell what a file contains"
    else:
        try:
            found = await resolver(set(file_ids), organization_id)
        except Exception as exc:  # noqa: BLE001 — never reuse what we cannot identify
            logger.exception("[wf:%s node=%s] reading file identities failed", run_id[:8], invocation.node_id)
            reason = f"reading the files failed ({type(exc).__name__})"
    unknown = sorted(f for f in file_ids if not found.get(f))
    if reason is None and unknown:
        reason = f"{len(unknown)} file(s) have no content hash or version"
    if reason is not None:
        await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label="engine.once_unversioned",
                    message=f"Run once per key never reuses this step: {reason}; the step ran",
                    payload={"files": unknown[:20]})
        return None
    return {f: str(found[f]) for f in sorted(file_ids)}


def not_saved_reason(
    slot: OnceSlot, *, result: _StepResult, output_dump: Any, ctx_channel_writes: int, warning_count: int,
    output_kind_ok: bool | None, output_kind_degraded: str | None,
) -> str | None:
    """Why this success will NOT be saved for reuse (None = it will). Topology (Sends, channel
    writes) is not a value; a DEGRADED result — the step warned or raised a review flag, its
    output failed its shape check, or the check could not run — is never reused."""
    if slot.claim is None or slot.digest is None:
        return None
    if result.sends or ctx_channel_writes:
        return "the step dispatched work or wrote channels (run topology, not a value)"
    if not isinstance(output_dump, dict):
        return "the step's output is not an object"
    if warning_count:
        return f"the step reported {warning_count} warning(s) or review flag(s)"
    said_failed = next((k for k in ("failed", "error")
                        if isinstance(output_dump.get(k), str) and output_dump[k].strip()), None)
    run_meta = output_dump.get("metadata")
    if said_failed is None and isinstance(run_meta, dict):
        # An AI step's run metadata carries its own verdict (2026-10-27, run 477536f8: a provider 503
        # through every retry rode in ``metadata.status``/``metadata.error`` of a "successful" result,
        # was saved, and the next run reused it in 1 s). Any recorded error or failed/suspended status
        # is not a result worth reusing, whichever step produced it.
        status = str(run_meta.get("status") or "")
        if isinstance(run_meta.get("error"), str) and run_meta["error"].strip():
            said_failed = "metadata.error"
        elif status == "failed" or status.startswith("suspended"):
            said_failed = f"metadata.status={status}"
    if said_failed:
        # A fail-soft step's own "it did not work" sentence is not a result: saved, it was replayed for a day.
        # A count (scrape_many's ``failed: 2``) is a tally, not a verdict, and does not stop saving.
        return f"the step's output says it did not work ('{said_failed}')"
    if output_kind_ok is False:
        return "the output did not match its declared shape"
    if output_kind_degraded:
        return f"the output's shape could not be checked ({output_kind_degraded})"
    return None


def _held_refs(value: Any) -> set[str]:
    from matrx_graph.checkpoint.value_store import held_hash

    found: set[str] = set()
    stack = [value]
    while stack:
        item = stack.pop()
        ref = held_hash(item)
        if ref:
            found.add(ref)
        elif isinstance(item, dict):
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    return found


async def _carry_held_values(scheduler: Scheduler, stored: StoredResult, run_id: str, output: Any) -> None:
    """A held value (``hold_on_server``) lives in its ORIGIN run's value store and every reader
    resolves it against ITS OWN run — so a result reused in another run brings its held values
    with it. Raises ``LookupError`` when the origin's values are gone (the reuse is then a miss)."""
    from matrx_graph.checkpoint import value_store

    refs = _held_refs(output)
    if not refs or stored.origin_run_id == run_id:
        return
    values = await value_store.load_run_values(stored.origin_run_id, refs)
    missing = refs - set(values)
    if missing:
        raise LookupError(f"{len(missing)} value(s) the saved result holds on the server are gone")
    organization_id = str(getattr(scheduler.app, "organization_id", "") or "") or None
    await value_store.store_run_values(run_id, values, organization_id=organization_id)


async def _reuse(
    scheduler: Scheduler, hit: Hit, *, run_id: str, step: int, attempt: int, invocation: Invocation,
    node: Any, spec: Any, started_inputs: dict[str, Any], result: _StepResult, invocation_count: int,
) -> bool:
    from matrx_graph.checkpoint.protocol import NodeOutcome
    from matrx_graph.executor.scheduler import _coerce_replayed_output
    from matrx_graph.types.events import NodeCompletedEvent

    stored = hit.result
    store = get_step_result_store()
    try:
        output = await store.resolve_output(stored)
        await _carry_held_values(scheduler, stored, run_id, output)
    except LookupError as exc:
        logger.warning("[wf:%s node=%s] saved result is no longer readable (%s) — running the step",
                       run_id[:8], invocation.node_id, exc)
        await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label="engine.once_not_reusable",
                    message=f"Run once per key could not read the saved result ({exc}); the step ran and pays again",
                    payload={"origin_run_id": stored.origin_run_id, "reason": "unreadable"})
        return False
    except Exception as exc:  # noqa: BLE001 — reading the saved result failed: the store's failure
        raise StepResultStoreError(f"reading the saved result failed: {type(exc).__name__}: {exc}") from exc
    try:
        model = _coerce_replayed_output(spec.output_schema, dict(output))
    except Exception as exc:  # noqa: BLE001 — the step's output shape changed since it was saved
        logger.warning("[wf:%s node=%s] saved result no longer fits %s (%s) — running the step",
                       run_id[:8], invocation.node_id, spec.output_schema.__name__, exc)
        # Never silent (2026-10-27: a saved agent_result whose final_text came back as an object
        # re-ran — and paid — on every rerun with no word on the step).
        await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label="engine.once_not_reusable",
                    message=(f"Run once per key could not reuse the saved result: it no longer fits "
                             f"{spec.output_schema.__name__}; the step ran and pays again"),
                    payload={"origin_run_id": stored.origin_run_id, "reason": "shape",
                             "error": f"{type(exc).__name__}: {str(exc)[:300]}"})
        return False
    reused_from = {
        "run_id": stored.origin_run_id,
        "node_id": stored.origin_node_id,
        "step": stored.origin_step,
        "dispatch_id": stored.origin_dispatch_id,
        "item_index": stored.origin_item_index,
        "attempt": stored.origin_attempt,
        "at": stored.succeeded_at.isoformat(),
    }
    verdict = stored.verdict or {}
    _reused_in_run(scheduler).add(invocation.node_id)
    result.output = model
    result.settled_dump = dict(output)
    result.reused = True
    result.sends = []
    result.emissions = dict(stored.emissions or {})
    result.channel_writes = [(node.output_channel, dict(output))] if node.output_channel else []
    wrapper: dict[str, Any] | None = None
    try:
        from matrx_graph.content_ir.runtime_view import OUTPUT_REF_OUTPUT, node_outcome_view

        now = datetime.now(UTC).isoformat()
        wrapper = node_outcome_view(
            run_id=run_id, node_id=invocation.node_id, workflow_id=scheduler.definition_id or None,
            step=step, attempt=attempt, status="completed", output_kind=stored.output_kind,
            output_kind_ok=verdict.get("output_kind_ok"), output_kind_errors=verdict.get("output_kind_errors"),
            duration_ms=0, started_at=now, ended_at=now, output_ref=OUTPUT_REF_OUTPUT,
        )
    except Exception:  # noqa: BLE001 — never load-bearing (same posture as a live completion)
        logger.error("[wf:%s node=%s] node_outcome wrapper assembly FAILED for a reused result",
                     run_id[:8], invocation.node_id, exc_info=True)
    await scheduler._emit(
        NodeCompletedEvent(
            run_id=run_id, step=step, node_id=invocation.node_id, spec_type=spec.node_type, attempt=attempt,
            dispatch_id=invocation.dispatch_id, item_index=invocation.item_index,
            invocation_count=invocation_count, duration_ms=0, output=dict(output),
            output_kind=stored.output_kind, output_kind_ok=verdict.get("output_kind_ok"),
            output_kind_errors=verdict.get("output_kind_errors"),
            output_kind_version=verdict.get("output_kind_version"),
            output_kind_degraded=verdict.get("output_kind_degraded"),
            wrapper=wrapper, source="reused", reused_from=reused_from,
        )
    )
    await scheduler.checkpointer.record_outcome(
        NodeOutcome(
            run_id=run_id, step=step, node_id=invocation.node_id, attempt=attempt,
            dispatch_id=invocation.dispatch_id, item_index=invocation.item_index,
            output=dict(output), inputs=started_inputs, input_kind=node.input_kind,
            metadata={"reused_from": reused_from}, channel_writes=result.channel_writes,
            emissions=result.emissions, duration_ms=0, source="reused",
            output_kind=stored.output_kind, output_kind_ok=verdict.get("output_kind_ok"),
            output_kind_errors=verdict.get("output_kind_errors"),
            output_kind_version=verdict.get("output_kind_version"),
            output_kind_degraded=verdict.get("output_kind_degraded"),
        )
    )
    if hit.digest_changed:
        await _flag(
            scheduler, run_id, invocation, step=step, attempt=attempt, label="engine.once_inputs_changed",
            message=("Same key, different inputs: the saved result was reused because this step "
                     "is set to reuse and flag"),
            payload={"origin_run_id": stored.origin_run_id, "origin_node_id": stored.origin_node_id},
        )
    return True


async def settle(
    slot: OnceSlot,
    scheduler: Scheduler,
    *,
    run_id: str,
    step: int,
    attempt: int,
    invocation: Invocation,
    node: Any,
    result: _StepResult,
    output_dump: Any,
    verdict: dict[str, Any],
    output_kind: str | None,
    not_saved: str | None = None,
) -> None:
    """Store the success this invocation produced under its claim. Never raises. ``not_saved``
    (:func:`not_saved_reason`, already written on the outcome) → the claim is released instead."""
    from matrx_graph.knobs import once_knobs

    claim = slot.claim
    if claim is None or claim.settled or slot.digest is None:
        return
    if not_saved:
        logger.warning("[wf:%s node=%s] run once per key: result not saved — %s",
                       run_id[:8], invocation.node_id, not_saved)
        # The author asked for this step to run once; a result that can never be saved means
        # every re-run pays again. Say so on the step (2026-10-27: Prepare Documents re-read
        # every page on each re-run because of an unread channel write, and nothing said why).
        await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label="engine.once_not_saved",
                    message=f"Run once per key could not save this step's result ({not_saved}); the next run pays again",
                    payload={"reason": not_saved})
        return
    try:
        policy = node.once
        now = datetime.now(UTC)
        days = (await once_knobs()).keep_days_default if policy.keep_days_from_knob else policy.keep_days
        stored = StoredResult(
            input_digest=slot.digest, output=dict(output_dump), output_kind=output_kind, verdict=verdict,
            emissions=dict(result.emissions or {}), origin_run_id=run_id, origin_node_id=invocation.node_id,
            origin_step=step, origin_dispatch_id=invocation.dispatch_id, origin_item_index=invocation.item_index,
            origin_attempt=attempt, succeeded_at=now,
            expires_at=(now + timedelta(days=days)) if days else None,
            run_input_digest=_run_input_digest(scheduler),
            origin_organization_id=str(getattr(scheduler.app, "organization_id", "") or "") or None,
        )
        claim.settling = True
        if await get_step_result_store().settle(claim.key, token=claim.token, result=stored):
            claim.settled = True
            return
        logger.error("[wf:%s node=%s] run once per key: the claim was lost before settling — "
                     "this result is not saved", run_id[:8], invocation.node_id)
        await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label="engine.once_unavailable",
                    message=("Run once per key lost this step's claim while it ran (its lease ran out), so "
                             "another run may have paid for the same work; this result was not saved"))
    except Exception as exc:  # noqa: BLE001 — the run already succeeded; only the reuse is lost
        logger.exception("[wf:%s node=%s] run once per key: saving the result FAILED",
                         run_id[:8], invocation.node_id)
        await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label="engine.once_unavailable",
                    message=f"Run once per key could not save this result ({type(exc).__name__}); the next run pays",
                    payload={"error": f"{type(exc).__name__}: {str(exc)[:300]}"})


async def finish(slot: OnceSlot) -> None:
    """Stop the renewer; release an unsettled claim. Never raises."""
    claim = slot.claim
    if claim is None:
        return
    renewer, claim.renewer = claim.renewer, None
    if renewer is not None:
        renewer.cancel()
        # Wait for it to actually stop (asyncio.wait never raises the task's own cancellation),
        # so no renewal outlives the invocation that held the claim.
        await asyncio.wait({renewer})
    if claim.settled:
        return
    try:
        await get_step_result_store().release(claim.key, token=claim.token)
    except Exception:  # noqa: BLE001 — the lease expires on its own
        logger.exception("[wf once] releasing an unsettled claim failed; its lease will expire")
