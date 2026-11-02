"""Capability-aware claiming — a worker only runs work whose every node type it has.

THE FAILURE THIS CLOSES (2026-10-12). Every server shares ONE database: a
developer's local server running newer code and the deployed worker fleet read
and write the same ``workflow.job`` queue. A run started on the newer build (its
graph uses a node type the fleet has not shipped yet) was picked up by a
deployed worker after the local server stopped; the deployed worker compiled the
graph, hit ``Unknown node type 'brand.setup.land_logo'`` and errored the run. The
run was perfectly healthy — it was simply on the wrong server.

THE RULE. A job carries the node types its run's graph needs
(``workflow.job.metadata.required_node_types``, stamped at enqueue). ``claim_one``
only hands a worker a job whose requirement is contained in that worker's
registry (``JsonbContainedBy``). A job a worker cannot run is never claimed by
it, never failed by it, and never errored by it; the run says so instead —
``workflow.run.metadata._awaiting_capability`` names the missing node types,
and is refreshed by every incapable worker (:func:`stamp_runs_awaiting_capability`)
so the lifecycle watchdog reads the run as honestly waiting, not stranded. The
first capable worker claims it and clears the marker.

Two belts, one rule: a job enqueued before its requirement was stamped (an older
enqueuer) or whose graph gained a node type after enqueue is caught at run time
by the host's job runner raising :class:`JobNeedsCapability`; the runner hands
the job back (:func:`defer_for_capability`) and stamps the requirement, so it is
never offered to this worker again.

Removed node types (``validation.REMOVED_NODE_TYPES``) are never a requirement:
no server will ever have them, so such a run must reach compile and fail with
its removal message instead of waiting forever.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID

if TYPE_CHECKING:
    from matrx_graph.executor.registry import NodeRegistry
    from matrx_graph.types.definition import Definition

log = logging.getLogger("matrx_graph.workers.capability")

#: The ``workflow.job.metadata`` key holding the job's requirement.
REQUIRED_NODE_TYPES_KEY = "required_node_types"
#: The ``workflow.run.metadata`` key saying "waiting for a server that supports X".
AWAITING_CAPABILITY_KEY = "_awaiting_capability"


class JobNeedsCapability(Exception):
    """Raised by a job runner that cannot execute a job's graph on this worker.

    Not a failure: the runner hands the job back for a capable worker and the
    run is marked as waiting. ``missing`` are the node types this worker lacks.
    """

    def __init__(self, *, required: Iterable[str], missing: Iterable[str]) -> None:
        self.required = sorted(set(required))
        self.missing = sorted(set(missing))
        super().__init__(
            "This worker cannot run node type(s) "
            + ", ".join(self.missing)
            + " — leaving the job for a server that supports them."
        )


def required_node_types(definition: Definition) -> list[str]:
    """The canonical node types ``definition`` needs, sorted and de-duplicated."""
    from matrx_graph.executor.registry import canonical_spec_type
    from matrx_graph.validation import REMOVED_NODE_TYPES

    types: set[str] = set()
    for node in definition.nodes:
        spec_type = str(node.spec_type or "")
        if not spec_type or spec_type in REMOVED_NODE_TYPES:
            continue
        types.add(canonical_spec_type(spec_type))
    return sorted(types)


def worker_capabilities(registry: NodeRegistry | None = None) -> list[str]:
    """Every node type this process can execute (canonical names), sorted."""
    from matrx_graph.executor.registry import default_registry

    return sorted((registry or default_registry()).all_types())


def capability_predicate(capabilities: Iterable[str], *, metadata_column: str = "metadata") -> Any:
    """The claim filter: the job's stamped requirement is contained in
    ``capabilities`` (a job with none stamped is claimable by anyone)."""
    from matrx_orm import F, JsonbContainedBy
    from matrx_orm.core.expressions import JsonPath

    return JsonbContainedBy(
        JsonPath(F(metadata_column), REQUIRED_NODE_TYPES_KEY, as_text=False),
        sorted(set(capabilities)),
        missing_as_empty=True,
    )


def missing_node_types(required: Iterable[str], registry: NodeRegistry | None = None) -> list[str]:
    """The subset of ``required`` this process's registry cannot execute."""
    from matrx_graph.executor.registry import default_registry

    reg = registry or default_registry()
    return sorted({t for t in required if not reg.has(t)})


def awaiting_capability_marker(
    *, missing: Iterable[str], worker_id: str, since: str | None = None
) -> dict[str, Any]:
    """The run-metadata marker. ``checked_at`` is a watchdog liveness signal."""
    names = sorted(set(missing))
    now = datetime.now(UTC).isoformat()
    return {
        "missing": names,
        "message": "Waiting for a server that supports " + ", ".join(names) + ".",
        "since": since or now,
        "checked_at": now,
        "checked_by": worker_id,
    }


async def required_node_types_for_run(run_id: str) -> list[str]:
    """The requirement of an existing run's graph, read from its stored definition.

    Never raises: an unreadable definition yields ``[]`` (claimable by anyone —
    the pre-capability behavior), and the run's own compile reports the defect.
    """
    try:
        from matrx_graph.db import DefinitionStore, RunStore

        run = await RunStore().load(run_id, resolve_output=False)
        if not run or not run.get("definition_id"):
            return []
        version_id = run.get("definition_version_id")
        row = await DefinitionStore().load(
            str(run["definition_id"]),
            is_version=version_id is not None,
            version_id=str(version_id) if version_id is not None else None,
        )
        return required_node_types(row.definition) if row is not None else []
    except Exception:  # noqa: BLE001 — a requirement read never blocks an enqueue
        log.warning("could not read node-type requirement for run %s", run_id, exc_info=True)
        return []


async def mark_run_awaiting_capability(run_id: str, *, missing: Iterable[str], worker_id: str) -> None:
    """Stamp (or refresh) the run's waiting marker, keeping its original ``since``."""
    from matrx_graph.db import RunStore

    store = RunStore()
    since: str | None = None
    run: dict[str, Any] | None = None
    try:
        run = await store.load(run_id, resolve_output=False)
        prior = ((run or {}).get("metadata") or {}).get(AWAITING_CAPABILITY_KEY)
        if isinstance(prior, dict) and sorted(prior.get("missing") or []) == sorted(set(missing)):
            since = prior.get("since")
    except Exception:  # noqa: BLE001 — the marker is still worth writing
        log.debug("prior awaiting marker unreadable for run %s", run_id, exc_info=True)
    marker = awaiting_capability_marker(missing=missing, worker_id=worker_id, since=since)
    await store.merge_metadata(run_id, {AWAITING_CAPABILITY_KEY: marker})
    if since is None and run is not None and run.get("organization_id"):
        # First time this run is seen waiting: one line a person reads in the run log.
        try:
            from matrx_graph.db._registry import get_model

            await get_model("WfRunLog").create_item(
                run_id=run_id,
                definition_id=str(run["definition_id"]) if run.get("definition_id") else None,
                severity="warning",
                label="run_awaiting_capability",
                message=(
                    "This run is waiting for a server that can run "
                    + ", ".join(marker["missing"])
                    + ". It continues automatically when one is available."
                ),
                payload={"missing": marker["missing"], "checked_by": worker_id},
                occurred_at=datetime.now(UTC),
                organization_id=str(run["organization_id"]),
            )
        except Exception:  # noqa: BLE001 — the marker above is the durable truth
            log.warning("could not write awaiting run-log line for run %s", run_id, exc_info=True)


async def clear_run_awaiting_capability(run: dict[str, Any] | None, run_id: str) -> None:
    """A capable worker took the run — drop the waiting marker (JSON null)."""
    if not isinstance(run, dict) or not (run.get("metadata") or {}).get(AWAITING_CAPABILITY_KEY):
        return
    from matrx_graph.db import RunStore

    await RunStore().merge_metadata(run_id, {AWAITING_CAPABILITY_KEY: None})


async def stamp_runs_awaiting_capability(
    capabilities: Iterable[str] | None = None, *, worker_id: str | None = None, limit: int = 100
) -> int:
    """Refresh the waiting marker on every run whose ready job THIS worker cannot run.

    Read-only on ``workflow.job``; writes only run metadata. Every replica may
    run it — the marker is idempotent. Returns how many runs were stamped.
    """
    from matrx_orm import F, Now
    from matrx_orm.core.expressions import Compare

    from matrx_graph.db._registry import get_model
    from matrx_graph.workers.queue import _worker_id

    caps = sorted(set(capabilities)) if capabilities is not None else worker_capabilities()
    rows = await (
        get_model("WfJob")
        .filter(
            Compare(F("visible_at"), "<=", Now()),
            ~capability_predicate(caps),
            claimed_at__isnull=True,
        )
        .limit(limit)
        .values("run_id", "metadata")
    )
    capset = set(caps)
    stamped: set[str] = set()
    for row in rows:
        run_id = str(row.get("run_id") or "")
        if not run_id or run_id in stamped:
            continue
        meta = row.get("metadata") or {}
        if isinstance(meta, str):
            import json

            meta = json.loads(meta)
        required = meta.get(REQUIRED_NODE_TYPES_KEY) or []
        missing = sorted(t for t in required if t not in capset)
        if not missing:
            continue
        try:
            await mark_run_awaiting_capability(
                str(UUID(run_id)), missing=missing, worker_id=worker_id or _worker_id()
            )
            stamped.add(run_id)
        except Exception:  # noqa: BLE001 — one run never stops the pass
            log.warning("could not stamp awaiting marker on run %s", run_id, exc_info=True)
    return len(stamped)


__all__ = [
    "AWAITING_CAPABILITY_KEY",
    "JobNeedsCapability",
    "REQUIRED_NODE_TYPES_KEY",
    "awaiting_capability_marker",
    "capability_predicate",
    "clear_run_awaiting_capability",
    "mark_run_awaiting_capability",
    "missing_node_types",
    "required_node_types",
    "required_node_types_for_run",
    "stamp_runs_awaiting_capability",
    "worker_capabilities",
]
