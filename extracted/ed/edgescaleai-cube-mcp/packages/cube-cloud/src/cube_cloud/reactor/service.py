"""AI Reactor reads and writes against Apollo (docs/ai-reactor-deploy-spec.md §5–6).

The shared layer under the console's AI tab (and, later, MCP tools). Callers pass an
environment they have ALREADY authorized (a row from the caller's RBAC-filtered list,
carrying `id`, `name`, `spaceId`, `namespaceId`); nothing here resolves a name or
authorizes anything.

Every operation re-runs the checks (`state.compute_state`) inside a per-cube lock and
does only what is missing, so repeating one is safe. The Edgeport marker on a
`localModels` entry is how the console knows what it started, so it is written FIRST
and removed LAST: a half-finished operation shows as out of sync instead of being lost.

Logging is by exception CLASS only. An `ApolloError` embeds the raw response body, and
these reads select a gateway's config, which on some gateways holds credentials.
"""

from __future__ import annotations

import asyncio
import copy
import logging
import os
import secrets
import time
from dataclasses import dataclass, field

from cube_common import apollo_queries as Q
from cube_common.apollo_client import ApolloClient, ApolloError
from cube_cloud.reactor import gpu as gpu_read
from cube_cloud.reactor import override as ov
from cube_cloud.reactor import state as st
from cube_cloud.reactor.catalog import Catalog, ModelSpec, load_catalog

logger = logging.getLogger(__name__)

CALL_BUDGET_SECONDS = float(os.environ.get("REACTOR_CALL_BUDGET_SECONDS", "45"))
LOCK_WAIT_SECONDS = float(os.environ.get("REACTOR_LOCK_WAIT_SECONDS", "15"))
OWN_WRITE_WAIT_SECONDS = float(os.environ.get("REACTOR_OWN_WRITE_WAIT_SECONDS", "15"))
ENTITY_APPEAR_WAIT_SECONDS = float(os.environ.get("REACTOR_ENTITY_APPEAR_WAIT_SECONDS", "15"))
POLL_SECONDS = 1.0
# How long the console remembers a change it submitted, so it neither offers the same
# action again nor submits a duplicate before Apollo shows it (state.SUBMITTED). Every
# change request starts PENDING_APPROVALS, even where approval is automatic (seen on
# cube-m9u9i4lc 2026-10-06, ~1 minute), and an environment's open requests cannot be
# listed. Per process: prod runs two tasks, so a repeat that lands on the other task
# is not caught here.
RECENT_SECONDS = float(os.environ.get("REACTOR_RECENT_SECONDS", "300"))
# Kept back from the lock wait so a caller that waited still has time to write.
_AFTER_LOCK_RESERVE_SECONDS = 20.0

# The Apollo secret the gateway chart reads its master key from (apolloSecrets), and
# the key inside it. Apollo materializes it as `<release>-gateway` before Helm runs.
GATEWAY_SECRET_NAME = "gateway"
GATEWAY_MASTER_KEY = "LITELLM_MASTER_KEY"

# CONSOLE_ENVIRONMENT_ENTITIES is single-page (200). A full page may hide a gateway or
# a model entity on page two, so a saturated read is never trusted for a write.
ENTITY_PAGE_SIZE = Q.CONSOLE_ENTITIES_PAGE_SIZE

# Write outcomes.
APPLIED = "applied"       # Apollo accepted every step; the cube is converging
SUBMITTED = "submitted"   # accepted, but at least one change waits for approval
PARTIAL = "partial"       # stopped part-way; the checks show what is left
REFUSED = "refused"       # nothing was written


@dataclass
class WriteResult:
    ok: bool
    outcome: str
    message: str
    state: st.ReactorState | None = None
    steps: list[str] = field(default_factory=list)


class _Deadline:
    def __init__(self, seconds: float):
        self._end = time.monotonic() + seconds

    def remaining(self) -> float:
        return self._end - time.monotonic()


_cube_locks: dict[str, asyncio.Lock] = {}
_recent: dict[tuple[str, str], tuple[str, float]] = {}
# The gateway override this process last wrote per cube, until Apollo shows it.
# Apollo merges a pending config change as a DIFF against the version it was based on,
# so a second write while the first is pending is merged against the same base: on
# cube-m9u9i4lc (2026-10-07) "add 30B" and "replace 4B with 30B", both pending, merged
# into the 30B listed twice. While an entry is here, the gateway reads as having a
# change pending and every write to that cube is refused.
_pending_gateway: dict[str, tuple[dict, float]] = {}


def _gateway_pending(env_id: str, current: dict | None) -> bool:
    entry = _pending_gateway.get(env_id)
    if entry is None:
        return False
    want, expires = entry
    if time.monotonic() >= expires or current == want:
        _pending_gateway.pop(env_id, None)
        return False
    return True


def _recent_for(env_id: str) -> dict[str, str]:
    now = time.monotonic()
    for key in [k for k, (_, expires) in _recent.items() if expires <= now]:
        del _recent[key]
    return {model: op for (env, model), (op, _) in _recent.items() if env == env_id}


def _remember(env_id: str, model_id: str, op: str) -> None:
    _recent[(env_id, model_id)] = (op, time.monotonic() + RECENT_SECONDS)


def _forget(env_id: str, *model_ids: str) -> None:
    for model_id in model_ids:
        _recent.pop((env_id, model_id), None)


def _cube_lock(env_id: str) -> asyncio.Lock:
    """The lock for `env_id`, replacing one bound to a dead event loop."""
    lock = _cube_locks.get(env_id)
    if lock is not None and lock.locked():
        try:
            lock._get_loop()
        except RuntimeError:
            lock = None
    if lock is None:
        lock = _cube_locks[env_id] = asyncio.Lock()
    return lock


async def _acquire(lock: asyncio.Lock, deadline: _Deadline) -> bool:
    wait = min(LOCK_WAIT_SECONDS, deadline.remaining() - _AFTER_LOCK_RESERVE_SECONDS)
    if not lock.locked():
        await lock.acquire()
        return True
    if wait <= 0:
        return False
    try:
        await asyncio.wait_for(lock.acquire(), timeout=wait)
    except asyncio.TimeoutError:
        return False
    return True


# ---------------------------------------------------------------------------
# Reads
# ---------------------------------------------------------------------------

class ReadFailed(Exception):
    """The cube's entities could not be read. Never carries Apollo's text."""


async def _entities(client: ApolloClient, env_id: str) -> tuple[list[dict], bool]:
    """Every entity on the cube, and whether the single page was saturated."""
    data = await client.graphql(Q.CONSOLE_ENVIRONMENT_ENTITIES, {"id": env_id})
    env = ((data or {}).get("apollo") or {}).get("environmentById")
    if env is None:
        raise ReadFailed("environment not returned")
    raw = (env.get("entities") or {}).get("entities") or []
    return raw, len(raw) >= ENTITY_PAGE_SIZE


async def _gateway_detail(client: ApolloClient, env_id: str, entity_id: str) -> st.GatewayDetail | None:
    """The gateway entity's declared config. None on any failure, logged by class only.

    `entity_id` must come from `env_id`'s own entity list, and the entity is refused
    unless Apollo says it is on `env_id`: `entityById` is fleet-wide.
    """
    try:
        data = await client.graphql(Q.REACTOR_GATEWAY_ENTITY, {"id": entity_id})
        entity = ((data or {}).get("apollo") or {}).get("entityById") or {}
        if ((entity.get("environment") or {}).get("id") or "") != env_id:
            logger.error("reactor: gateway entity is not on the authorized environment; refusing")
            return None
        declared = entity.get("declaredState") or {}
        module = entity.get("installedByModuleV2") or {}
        config = declared.get("config")
        return st.GatewayDetail(
            config=config if isinstance(config, list) else [],
            release_channel=declared.get("releaseChannel"),
            module_coordinate=module.get("moduleMavenCoordinate"),
        )
    except Exception as e:  # noqa: BLE001 -- class only, see module docstring
        logger.warning("reactor: gateway read failed (%s)", type(e).__name__)
        return None


# How long a page load waits for the GPU read before answering without it (the read
# finishes in the background). Writes wait for it in full, since they enforce fit.
GPU_WAIT_ON_READ_SECONDS = 4.0
GPU_WAIT_ON_WRITE_SECONDS = 12.0


async def read_state(
    client: ApolloClient, env: dict, can_write: bool, catalog: Catalog | None = None,
    profile: str | None = None, gpu_wait: float | None = None,
) -> st.ReactorState:
    """The checks for one authorized cube. Raises ApolloError / ReadFailed if the
    entity list cannot be read (the console answers 502); a failed GATEWAY read is
    reported in the state, as `unknown`, not raised. With `profile`, the cube's GPUs
    are read too (kubectl as that profile), which is what decides `fits`."""
    catalog = catalog or load_catalog()
    env_id = env.get("id") or ""
    if profile:
        (entities, saturated), gpus = await asyncio.gather(
            _entities(client, env_id), gpu_read.read_gpus(env.get("name") or "", profile, wait=gpu_wait),
        )
    else:
        (entities, saturated), gpus = await _entities(client, env_id), gpu_read.UNKNOWN
    gateways = st.gateway_entities(catalog, entities)
    detail, detail_failed = None, False
    if len(gateways) == 1:
        detail = await _gateway_detail(client, env_id, gateways[0].get("id") or "")
        detail_failed = detail is None
    if saturated:
        logger.error(
            "reactor: entity list for %s is saturated (%d rows); writes refused",
            env.get("name"), len(entities),
        )
    current = None
    if detail is not None:
        try:
            current = ov.parse_declared_config(detail.config, "0.0.0").overrides
        except ov.OverrideUnreadable:
            current = None
    state = st.compute_state(
        catalog, entities, detail, detail_failed, can_write=can_write, saturated=saturated,
        gpu=gpus, recent=_recent_for(env_id),
        ready_ids=await _ready_by_health_report(client, env_id, catalog, entities),
        gateway_pending=_gateway_pending(env_id, current),
    )
    for m in state.models:
        if m.status != st.SUBMITTED:
            _recent.pop((env_id, m.spec.id), None)
    return state


# The most entities one read will consult a health report for (the gateway plus a
# few models in practice).
MAX_HEALTH_REPORTS = 6


async def _ready_by_health_report(
    client: ApolloClient, env_id: str, catalog: Catalog, entities: list[dict],
) -> frozenset[str]:
    """Ids of reactor entities whose own health report is clean while Apollo's status
    still says otherwise (`state.compute_state`). Each id comes from this environment's
    own entity list, and `fetch_entity_health_checks` refuses one on any other
    environment; it never raises."""
    from cube_cloud.tools import health_checks

    ours = (
        {catalog.gateway.product_id} | {m.product_id for m in catalog.models}
        | {m.product_id for m in catalog.shown}
    )
    candidates = [
        e for e in entities
        if st.entity_product(e) in ours and st.needs_health_check(e) and e.get("id")
    ][:MAX_HEALTH_REPORTS]
    if not candidates:
        return frozenset()
    results = await asyncio.gather(*(
        health_checks.fetch_entity_health_checks(client, env_id, e["id"]) for e in candidates
    ))
    return frozenset(
        e["id"] for e, r in zip(candidates, results)
        if r.state == health_checks.STATE_CLEAR and r.pods > 0 and not r.truncated
    )


# ---------------------------------------------------------------------------
# Writes (each raises ApolloError on transport/GraphQL failure)
# ---------------------------------------------------------------------------

def _pending_approval(request_status: str | None) -> bool:
    return "PENDING" in (request_status or "").upper()


async def _install(
    client: ApolloClient, env: dict, *, entity_name: str, product_id: str, namespace: str,
    block: ov.ConfigBlock, release_channel: str | None,
) -> str:
    optional: dict = {"configOverrides": ov.render_config_block(block)}
    if release_channel:
        optional["releaseChannel"] = release_channel
    data = await client.graphql(Q.INSTALL_ENTITIES, {
        "envId": env.get("id"),
        "namespaceId": env.get("namespaceId"),
        "entities": {"helmCharts": [{
            "helmChartName": entity_name,
            "productId": product_id,
            "k8sNamespace": namespace,
            "entityInstallationOptionalInputs": optional,
        }]},
    })
    cr = ((data or {}).get("apollo") or {}).get("installEntitiesOnEnvironmentV2") or {}
    return cr.get("requestStatus") or ""


async def _uninstall(client: ApolloClient, env: dict, entity_id: str) -> str:
    data = await client.graphql(Q.UNINSTALL_ENTITY, {
        "namespaceId": env.get("namespaceId"), "entityId": entity_id,
    })
    cr = ((data or {}).get("apollo") or {}).get("uninstallEntityV2") or {}
    return cr.get("requestStatus") or ""


@dataclass
class _ConfigWrite:
    written: bool          # a change request was opened
    no_changes: bool       # Apollo said the config already matched
    request_status: str = ""
    error: str = ""        # typed error name when neither of the above


async def _write_config(client: ApolloClient, env: dict, entity_id: str, block: ov.ConfigBlock) -> _ConfigWrite:
    update: dict = {
        "type": {"entity": {"apolloEntityId": entity_id}},
        "content": ov.render_config_block(block),
    }
    if env.get("namespaceId"):
        update["namespaceId"] = env["namespaceId"]
    data = await client.graphql(Q.UPDATE_ENTITY_CONFIG_V2, {
        "spaceId": env.get("spaceId"), "update": update,
    })
    result = ((data or {}).get("apollo") or {}).get("updateConfigByResourceV2") or {}
    error = (result.get("error") or {}).get("__typename") or ""
    if error.endswith("_NoChanges"):
        return _ConfigWrite(written=False, no_changes=True)
    if error:
        return _ConfigWrite(written=False, no_changes=False, error=error)
    cr = result.get("changeRequest") or {}
    return _ConfigWrite(written=True, no_changes=False, request_status=cr.get("requestStatus") or "")


async def _create_gateway_key(client: ApolloClient, entity_id: str) -> None:
    """Give a new gateway its master key. The value is generated here, sent to Apollo,
    and never stored, logged or returned. Key management is a later phase: rotate with
    `update_secret` when a caller needs to know it."""
    master_key = "sk-" + secrets.token_urlsafe(32)
    await client.graphql(Q.CREATE_SECRET, {
        "entityId": entity_id,
        "secrets": [{
            "name": GATEWAY_SECRET_NAME,
            "description": "AI Reactor gateway master key (set by the Edgeport console)",
            "targetSpecification": {"multiValue": {"rawValues": [
                {"key": GATEWAY_MASTER_KEY, "rawValue": master_key},
            ]}},
        }],
    })


async def _await_config(
    client: ApolloClient, env_id: str, entity_id: str, want: dict, deadline: _Deadline,
) -> bool:
    """Poll until the gateway's declared overrides equal `want`. Without this, two
    changes a few seconds apart lose the first (Apollo applies config asynchronously;
    `expose` hit exactly this live on 2026-09-24)."""
    end = time.monotonic() + max(0.0, min(OWN_WRITE_WAIT_SECONDS, deadline.remaining() - 2))
    while True:
        detail = await _gateway_detail(client, env_id, entity_id)
        if detail is not None:
            try:
                if ov.parse_declared_config(detail.config, "0.0.0").overrides == want:
                    return True
            except ov.OverrideUnreadable:
                pass
        if time.monotonic() >= end:
            return False
        await asyncio.sleep(POLL_SECONDS)


async def _await_entity(
    client: ApolloClient, env_id: str, product_id: str, deadline: _Deadline,
) -> dict | None:
    end = time.monotonic() + max(0.0, min(ENTITY_APPEAR_WAIT_SECONDS, deadline.remaining() - 8))
    while True:
        try:
            entities, _ = await _entities(client, env_id)
            found = [e for e in entities if st.entity_product(e) == product_id]
            if len(found) == 1:
                return found[0]
        except Exception as e:  # noqa: BLE001
            logger.warning("reactor: entity re-read failed (%s)", type(e).__name__)
        if time.monotonic() >= end:
            return None
        await asyncio.sleep(POLL_SECONDS)


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------

GATEWAY_REFUSALS = {
    st.REASON_MODULE: "This cube's AI Reactor gateway is managed by an Apollo module, so the console leaves it alone.",
    st.REASON_DATABASE: "This cube's gateway keeps its model list in its own database. The console can't change it yet.",
    st.REASON_SECRETS: "This cube's gateway still keeps credentials in its Apollo config, so the console won't edit it.",
    st.REASON_MULTIPLE: "This cube has more than one AI Reactor gateway, so the console won't guess which to change.",
    st.REASON_PENDING: "A change to this cube's gateway is waiting to be applied. Try again once it has.",
    "multiple_blocks": "This cube's gateway config has more than one version block, so the console won't rewrite it.",
    "has_comments": "This cube's gateway config carries comments written by hand, which a rewrite would lose, so the console won't rewrite it.",
    "unreadable": "This cube's gateway config could not be read, so the console won't rewrite it.",
    "ambiguous_values": "This cube's gateway config has an unquoted value the console could not write back exactly as written, so it won't rewrite it.",
}
BUSY = "Another change to this cube's AI models is still being applied. Try again in a few seconds."
NOT_ALLOWED = "Your account can view this cube's AI models but not change them."
UNREADABLE = "The console could not read this cube's AI Reactor gateway, so nothing was changed."
TOO_MANY = "This cube has more entities than the console reads in one page, so nothing was changed."


def _refused(message: str, state: st.ReactorState | None = None) -> WriteResult:
    return WriteResult(ok=False, outcome=REFUSED, message=message, state=state)


def _gateway_refusal(state: st.ReactorState) -> str | None:
    gw = state.gateway
    if gw.status == st.GATEWAY_UNKNOWN:
        return UNREADABLE
    if gw.status == st.GATEWAY_READ_ONLY:
        return GATEWAY_REFUSALS.get(gw.reason or "", UNREADABLE)
    return None


def _new_gateway_block(catalog: Catalog, models: list[ModelSpec]) -> ov.ConfigBlock:
    overrides = copy.deepcopy(catalog.gateway.base_overrides)
    overrides[ov.MARKER_KEY] = ov.MARKER_VALUE
    overrides["localModels"] = [ov.marked_entry(m, catalog.gateway.namespace) for m in models]
    return ov.ConfigBlock(version=catalog.gateway.config_block_version, overrides=overrides)


class _Run:
    """Bookkeeping for one operation: the steps taken and whether any is pending approval."""

    def __init__(self, client: ApolloClient, env: dict, catalog: Catalog, deadline: _Deadline):
        self.client, self.env, self.catalog, self.deadline = client, env, catalog, deadline
        self.steps: list[str] = []
        self.pending = False
        self.unconfirmed = False
        self.block: ov.ConfigBlock | None = None
        self.gateway_id: str = ""
        self.wrote_gateway = False

    def note(self, step: str, request_status: str = "") -> None:
        self.steps.append(step)
        if _pending_approval(request_status):
            self.pending = True

    def use_gateway(self, state: st.ReactorState) -> None:
        """Start from the override this operation read. Later merges build on what
        THIS operation last wrote, never on a re-read that may not show it yet."""
        assert state.gateway.block is not None and state.gateway.entity is not None
        self.block = state.gateway.block
        self.gateway_id = state.gateway.entity["id"]

    async def set_models(self, add: list[ModelSpec], remove: list[str]) -> None:
        """Merge marked entries into the gateway's override and wait until Apollo shows it."""
        current = self.block
        assert current is not None, "use_gateway() first"
        ns = self.catalog.gateway.namespace
        merged = ov.with_models(current.overrides, add=[ov.marked_entry(m, ns) for m in add], remove=remove)
        if merged == current.overrides:
            return
        assert not self.wrote_gateway, "one gateway write per operation (see _pending_gateway)"
        block = ov.ConfigBlock(current.version, merged)
        result = await _write_config(self.client, self.env, self.gateway_id, block)
        if result.error:
            raise _StepRefused(result.error)
        self.block = block
        if result.no_changes:
            return
        self.wrote_gateway = True
        self.note("gateway models updated", result.request_status)
        landed = False
        if not _pending_approval(result.request_status):
            landed = await _await_config(self.client, self.env["id"], self.gateway_id, merged, self.deadline)
            self.unconfirmed = not landed
        if not landed:
            _pending_gateway[self.env["id"]] = (merged, time.monotonic() + RECENT_SECONDS)


class _StepRefused(Exception):
    """Apollo returned a typed error for a config write. Carries only the type name."""


def _finish(run: _Run, state: st.ReactorState, done: str) -> WriteResult:
    if run.pending:
        return WriteResult(True, SUBMITTED, (
            f"{done} Apollo is applying the change; on a cube where changes need "
            "approval, it waits for that first."
        ), state, run.steps)
    message = done
    if run.unconfirmed:
        message += " Apollo has not shown the gateway change yet; wait a few seconds before changing this cube again."
    return WriteResult(True, APPLIED, message, state, run.steps)


async def deploy(
    client: ApolloClient, env: dict, model_id: str, *, replace: str | None = None,
    can_write: bool, catalog: Catalog | None = None, profile: str | None = None,
) -> WriteResult:
    """Send `model_id` to the cube, optionally replacing an Edgeport-managed `replace`."""
    catalog = catalog or load_catalog()
    spec = catalog.model(model_id)
    if spec is None:
        return _refused("That model is not in the catalog.")
    if replace is not None and (replace == model_id or catalog.model(replace) is None):
        return _refused("The model to replace is not in the catalog.")
    if not can_write:
        return _refused(NOT_ALLOWED)
    deadline = _Deadline(CALL_BUDGET_SECONDS)
    lock = _cube_lock(env.get("id") or "")
    if not await _acquire(lock, deadline):
        return _refused(BUSY)
    try:
        return await _deploy_locked(client, env, catalog, spec, replace, deadline, profile)
    finally:
        lock.release()


async def _deploy_locked(
    client: ApolloClient, env: dict, catalog: Catalog, spec: ModelSpec,
    replace: str | None, deadline: _Deadline, profile: str | None = None,
) -> WriteResult:
    state = await read_state(
        client, env, can_write=True, catalog=catalog, profile=profile,
        gpu_wait=GPU_WAIT_ON_WRITE_SECONDS,
    )
    submitted = state.model(spec.id)
    if submitted is not None and submitted.status == st.SUBMITTED:
        return WriteResult(True, APPLIED, f"{spec.display_name} was just submitted. Apollo is applying it.", state)
    if (refusal := _gateway_refusal(state)) is not None:
        return _refused(refusal, state)
    if state.saturated:
        return _refused(TOO_MANY, state)

    run = _Run(client, env, catalog, deadline)
    # A gateway this console installed whose key may never have been set: the entity
    # did not appear in time on the first Deploy, or its install waited for approval.
    # Repaired before anything else so that re-pressing Deploy finishes the job even
    # when the model itself is already there. Creating a secret that exists fails,
    # which is fine: that means it is set.
    gw = state.gateway
    if gw.console_installed and gw.lifecycle == st.PENDING_INSTALL and gw.entity:
        try:
            await _create_gateway_key(client, gw.entity["id"])
            run.note("gateway key set")
        except ApolloError as e:
            logger.info("reactor: gateway key not created (%s); assuming it exists", type(e).__name__)

    model = state.model(spec.id)
    assert model is not None
    if "deploy" not in model.actions:
        if model.status == st.SUBMITTED:
            done = f"{spec.display_name} was just submitted. Apollo is applying it."
            return WriteResult(True, APPLIED, done, state, run.steps)
        if model.fits == "no":
            return _refused(
                f"{spec.display_name} needs a GPU with {spec.min_vram_gb} GB or more; this "
                f"cube's GPU has {state.gpu.memory_gb} GB.", state,
            )
        if model.owner == "edgeport" and model.status != st.REMOVING:
            done = f"{spec.display_name} is already on this cube."
            return WriteResult(True, APPLIED, done, await _safe_state(client, env, catalog, profile) or state, run.steps)
        if model.owner == "outside" and model.status != st.REMOVING:
            return WriteResult(True, APPLIED, f"{spec.display_name} is already on this cube.", state)
        if model.status == st.REMOVING:
            return _refused(f"{spec.display_name} is still being removed. Try again once it's gone.", state)
        return _refused(f"The console found more than one {spec.display_name} on this cube, so it won't guess which to change.", state)
    old = state.model(replace) if replace else None
    if old is not None and not (old.owner == "edgeport" and "remove" in old.actions):
        return _refused("The console can only replace a model it deployed.", state)

    # Recorded when the operation STARTS, not when its steps finish (up to the call
    # budget later): a page reloaded mid-operation reads the cube while this runs, and
    # without it showed a half-sent deploy as "out of sync" with Finish and Remove
    # offered. Dropped again below if nothing was written or a step failed.
    touched = [spec.id] + ([old.spec.id] if old is not None else [])
    _remember(env["id"], spec.id, "deploy")
    if old is not None:
        _remember(env["id"], old.spec.id, "remove")
    try:
        # 1. The marker first: the gateway learns about the model before it exists.
        if state.gateway.status == st.GATEWAY_ABSENT:
            status = await _install(
                client, env, entity_name=catalog.gateway.entity_name,
                product_id=catalog.gateway.product_id, namespace=catalog.gateway.namespace,
                block=_new_gateway_block(catalog, [spec]),
                release_channel=catalog.gateway.release_channel,
            )
            run.note("gateway install requested", status)
            if not run.pending:
                entity = await _await_entity(client, env["id"], catalog.gateway.product_id, deadline)
                if entity is not None:
                    await _create_gateway_key(client, entity["id"])
                    run.note("gateway key set")
                else:
                    run.unconfirmed = True
        else:
            # ONE write: the new marker and, for a replace, the old one's removal
            # together. Two writes in one operation are merged by Apollo as diffs
            # against the same base while the first is pending (see _pending_gateway).
            run.use_gateway(state)
            await run.set_models(add=[spec], remove=[old.spec.id] if old is not None else [])

        # 2. The model itself.
        if model.entity is None:
            status = await _install(
                client, env, entity_name=spec.entity_name, product_id=spec.product_id,
                namespace=catalog.gateway.namespace,
                block=ov.ConfigBlock(spec.config_block_version, spec.install_overrides),
                release_channel=catalog.gateway.release_channel,
            )
            run.note(f"{spec.id} install requested", status)

        # 3. Replace: remove the old model's entity (its marker went in step 1).
        if old is not None and old.entity is not None:
            run.note(f"{old.spec.id} uninstall requested", await _uninstall(client, env, old.entity["id"]))
    except (ApolloError, _StepRefused, ov.OverrideUnreadable) as e:
        logger.error("reactor deploy of %s on %s stopped after %s (%s)",
                     spec.id, env.get("name"), run.steps or "no steps", type(e).__name__)
        # A failed step must leave its repair offered, so the card reads the cube as is.
        _forget(env["id"], *touched)
        if not run.steps:
            return _refused("Apollo refused the change. Nothing was written.", await _safe_state(client, env, catalog, profile))
        return WriteResult(False, PARTIAL, "Apollo refused part of the change. The model card shows what is left to do.",
                           await _safe_state(client, env, catalog, profile), run.steps)
    except BaseException:
        # Anything else (a bug, a cancellation) must not leave the card claiming a
        # change was submitted for RECENT_SECONDS.
        _forget(env["id"], *touched)
        raise

    if run.steps:
        _remember(env["id"], spec.id, "deploy")
        if old is not None:
            _remember(env["id"], old.spec.id, "remove")
    else:
        _forget(env["id"], *touched)
    after = await _safe_state(client, env, catalog, profile)
    if state.gateway.status == st.GATEWAY_ABSENT and run.unconfirmed and not run.pending:
        return WriteResult(True, PARTIAL, (
            f"{spec.display_name} is being installed, but the new gateway did not appear in "
            "time to set its key. Press Deploy again in a minute to finish."
        ), after, run.steps)
    verb = f"Replacing {old.spec.display_name} with" if old else "Deploying"
    return _finish(run, after, f"{verb} {spec.display_name}. The first start downloads the model, which can take a while.")


async def remove(
    client: ApolloClient, env: dict, model_id: str, *, can_write: bool,
    catalog: Catalog | None = None, profile: str | None = None,
) -> WriteResult:
    """Remove an Edgeport-managed model: its entity first, its marker last."""
    catalog = catalog or load_catalog()
    spec = catalog.model(model_id)
    if spec is None:
        return _refused("That model is not in the catalog.")
    if not can_write:
        return _refused(NOT_ALLOWED)
    deadline = _Deadline(CALL_BUDGET_SECONDS)
    lock = _cube_lock(env.get("id") or "")
    if not await _acquire(lock, deadline):
        return _refused(BUSY)
    try:
        state = await read_state(
            client, env, can_write=True, catalog=catalog, profile=profile,
            gpu_wait=GPU_WAIT_ON_WRITE_SECONDS,
        )
        if (refusal := _gateway_refusal(state)) is not None:
            return _refused(refusal, state)
        if state.saturated:
            return _refused(TOO_MANY, state)
        model = state.model(model_id)
        assert model is not None
        if model.status == st.SUBMITTED:
            return WriteResult(True, APPLIED, f"A change to {spec.display_name} was just submitted. Apollo is applying it.", state)
        if model.owner != "edgeport":
            if model.status == st.AVAILABLE:
                return WriteResult(True, APPLIED, f"{spec.display_name} is not on this cube.", state)
            return _refused(f"The console can only remove a model it deployed. {spec.display_name} is left as it is.", state)
        run = _Run(client, env, catalog, deadline)
        _remember(env["id"], spec.id, "remove")  # at the start; see deploy
        try:
            if model.entity is not None and model.status != st.REMOVING:
                run.note(f"{spec.id} uninstall requested", await _uninstall(client, env, model.entity["id"]))
            run.use_gateway(state)
            await run.set_models(add=[], remove=[spec.id])
        except (ApolloError, _StepRefused, ov.OverrideUnreadable) as e:
            logger.error("reactor remove of %s on %s stopped after %s (%s)",
                         spec.id, env.get("name"), run.steps or "no steps", type(e).__name__)
            _forget(env["id"], spec.id)
            if not run.steps:
                return _refused("Apollo refused the change. Nothing was written.", await _safe_state(client, env, catalog, profile))
            # Not remembered as submitted: a step failed, and the card must offer the repair.
            return WriteResult(False, PARTIAL, "Apollo refused part of the change. The model card shows what is left to do.",
                               await _safe_state(client, env, catalog, profile), run.steps)
        except BaseException:
            _forget(env["id"], spec.id)  # see deploy
            raise
        if run.steps:
            _remember(env["id"], spec.id, "remove")
        else:
            _forget(env["id"], spec.id)
        after = await _safe_state(client, env, catalog, profile)
        return _finish(run, after, f"Removing {spec.display_name}.")
    finally:
        lock.release()


async def _safe_state(
    client: ApolloClient, env: dict, catalog: Catalog, profile: str | None = None,
) -> st.ReactorState | None:
    try:
        return await read_state(
            client, env, can_write=True, catalog=catalog, profile=profile,
            gpu_wait=GPU_WAIT_ON_READ_SECONDS,
        )
    except Exception as e:  # noqa: BLE001
        logger.warning("reactor: state re-read failed (%s)", type(e).__name__)
        return None
