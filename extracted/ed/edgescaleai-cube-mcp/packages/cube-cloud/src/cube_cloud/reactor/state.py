"""The checks behind every AI Reactor read and write (docs/ai-reactor-deploy-spec.md §4).

Pure: `compute_state` takes what Apollo returned and decides what is installed, who
owns it, whether the gateway may be edited, and which actions are open. Both the
status read and every write call it, so a write never trusts what a browser saw.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from cube_cloud.reactor import override as ov
from cube_cloud.reactor.catalog import Catalog, ModelSpec
from cube_cloud.reactor.gpu import UNKNOWN as GPU_UNKNOWN, GpuState
from cube_cloud.tools.health_checks import FAULT_STATUSES

# ApolloEntityLifecycleStatus, verified by introspection 2026-10-06.
PENDING_INSTALL = "PENDING_INSTALL"
INSTALLED = "INSTALLED"
REMOVING_LIFECYCLES = frozenset({"MARKED_FOR_DELETION", "DELETED"})

# Gateway states.
GATEWAY_ABSENT = "absent"            # Deploy installs one
GATEWAY_MANAGEABLE = "manageable"    # the console may edit its localModels
GATEWAY_READ_ONLY = "read_only"      # shown, never edited; `reason` says why
GATEWAY_UNKNOWN = "unknown"          # the gateway read failed

# Why a gateway is read-only. Stable codes; the UI words them.
REASON_MODULE = "module_owned"
REASON_DATABASE = "database_mode"
REASON_SECRETS = "secrets_in_override"
REASON_MULTIPLE = "multiple_gateways"
REASON_PENDING = "change_pending"
# Plus override.OverrideUnreadable reasons: "multiple_blocks", "has_comments",
# "unreadable", "ambiguous_values".

# Model statuses.
AVAILABLE = "available"
INSTALLING = "installing"
STARTING = "starting"
READY = "ready"
NEEDS_ATTENTION = "needs_attention"
REMOVING = "removing"
# No longer produced for LLM models (decided 2026-10-13: a model beside a gateway is
# shown as served by it). Kept because the vision side (feature/console-ai-vision,
# reactor/vision.py) still uses it for its own models.
OUTSIDE = "installed_outside"
OUT_OF_SYNC = "out_of_sync"
# The console submitted a change for this model moments ago and Apollo does not show
# it yet. Every change request starts PENDING_APPROVALS, even on cubes that approve
# automatically, and nothing readable lists an environment's open requests, so the
# console remembers what it just sent (service._recent) rather than offering the same
# action again and submitting a duplicate.
SUBMITTED = "submitted"

TRANSITIONAL = frozenset({SUBMITTED, INSTALLING, STARTING, REMOVING})


@dataclass(frozen=True)
class GatewayDetail:
    """What the gateway entity read returned. `config` is the raw declaredState.config."""
    config: list
    release_channel: str | None
    module_coordinate: str | None


@dataclass
class GatewayState:
    status: str
    reason: str | None = None
    mode: str = "unknown"                  # config | database | unknown
    entity: dict | None = None             # the raw entity row, server-side only
    block: ov.ConfigBlock | None = None    # parsed override, server-side only
    console_installed: bool = False
    release_channel: str | None = None
    ready: bool = False                    # HEALTHY, or a clean health report (see compute_state)

    @property
    def lifecycle(self) -> str:
        return (self.entity or {}).get("lifecycleStatus") or ""

    @property
    def health(self) -> str:
        return ((self.entity or {}).get("reportedStatus") or {}).get("healthStatus") or ""


@dataclass
class ModelState:
    spec: ModelSpec
    status: str
    entity: dict | None = None
    owner: str | None = None               # edgeport | outside | None
    wired: str = "no"                      # yes | no | unknown
    actions: list[str] = field(default_factory=list)
    fits: str = "unknown"                  # yes | no | unknown: one of the cube's GPUs is big enough

    @property
    def lifecycle(self) -> str:
        return (self.entity or {}).get("lifecycleStatus") or ""

    @property
    def health(self) -> str:
        return ((self.entity or {}).get("reportedStatus") or {}).get("healthStatus") or ""


@dataclass
class ReactorState:
    gateway: GatewayState
    models: list[ModelState]
    gpu_likely_taken: bool = False
    # The single-page entity read came back full: something may be on page two, so
    # no write is offered (CONSOLE_ENTITIES_PAGE_SIZE).
    saturated: bool = False
    can_write: bool = False
    gpu: GpuState = GPU_UNKNOWN

    def model(self, model_id: str) -> ModelState | None:
        return next((m for m in self.models if m.spec.id == model_id), None)


def entity_product(entity: dict) -> str:
    return ((entity.get("product") or {}).get("productId")) or ""


def _pending(entity: dict | None) -> bool:
    status = (entity or {}).get("planStatus") or {}
    return "Blocked" in (status.get("__typename") or "") and bool(status.get("blockedChangesCount"))


def gateway_entities(catalog: Catalog, entities: list[dict]) -> list[dict]:
    return [e for e in entities if entity_product(e) == catalog.gateway.product_id]


def compute_gateway(
    catalog: Catalog, entities: list[dict], detail: GatewayDetail | None, detail_failed: bool,
    pending: bool = False,
) -> GatewayState:
    found = gateway_entities(catalog, entities)
    if not found:
        return GatewayState(status=GATEWAY_ABSENT)
    if len(found) > 1:
        return GatewayState(status=GATEWAY_READ_ONLY, reason=REASON_MULTIPLE, entity=found[0])
    entity = found[0]
    if detail_failed or detail is None:
        return GatewayState(status=GATEWAY_UNKNOWN, entity=entity)
    state = GatewayState(
        status=GATEWAY_MANAGEABLE, entity=entity, release_channel=detail.release_channel,
    )
    if detail.module_coordinate:
        state.status, state.reason = GATEWAY_READ_ONLY, REASON_MODULE
        return state
    try:
        block = ov.parse_declared_config(detail.config, catalog.gateway.config_block_version)
    except ov.OverrideUnreadable as e:
        state.status, state.reason = GATEWAY_READ_ONLY, e.reason
        return state
    overrides = block.overrides
    database = overrides.get("database") if isinstance(overrides.get("database"), dict) else {}
    state.mode = "database" if database.get("enabled") is True else "config"
    secrets = overrides.get("apolloSecrets") if isinstance(overrides.get("apolloSecrets"), dict) else {}
    if secrets.get("enabled") is not True:
        # The override may hold literal credentials. Keep nothing parsed from it.
        state.status, state.reason, state.mode = GATEWAY_READ_ONLY, REASON_SECRETS, "unknown"
        return state
    state.block = block
    state.console_installed = ov.gateway_is_marked(overrides)
    if state.mode == "database":
        state.status, state.reason = GATEWAY_READ_ONLY, REASON_DATABASE
    elif _pending(entity) or pending:
        state.status, state.reason = GATEWAY_READ_ONLY, REASON_PENDING
    return state


def _healthy(entity: dict | None, ready_ids: frozenset[str]) -> bool:
    if not entity:
        return False
    health = ((entity.get("reportedStatus") or {}).get("healthStatus")) or ""
    if health == "HEALTHY":
        return True
    return health not in FAULT_STATUSES and (entity.get("id") or "") in ready_ids


def needs_health_check(entity: dict) -> bool:
    """Whether Apollo's status may be hiding a ready entity: installed, not HEALTHY,
    and not asserting a fault."""
    health = ((entity.get("reportedStatus") or {}).get("healthStatus")) or ""
    return (
        (entity.get("lifecycleStatus") or "") == INSTALLED
        and health != "HEALTHY" and health not in FAULT_STATUSES
    )


def _model_status(entity: dict, wired: bool, gateway_healthy: bool, healthy: bool) -> str:
    lifecycle = entity.get("lifecycleStatus") or ""
    health = ((entity.get("reportedStatus") or {}).get("healthStatus")) or ""
    if lifecycle in REMOVING_LIFECYCLES:
        return REMOVING
    if lifecycle == PENDING_INSTALL:
        return INSTALLING
    if health in FAULT_STATUSES:
        return NEEDS_ATTENTION
    if healthy:
        return READY if wired and gateway_healthy else STARTING
    return STARTING


def _wired(
    gateway: GatewayState, overrides: dict, spec: ModelSpec, namespace: str, is_marked: bool,
) -> str:
    """Whether the gateway routes to this model: yes, no, or unknown.

    A database-mode gateway keeps most of its catalog in Postgres, which the console
    cannot read, so anything not marked there is `unknown`, never `no`.
    """
    if gateway.status == GATEWAY_ABSENT:
        return "no"
    if gateway.block is None:
        return "unknown"
    if is_marked:
        return "yes"
    if gateway.mode == "database":
        return "unknown"
    api_base = spec.api_base(namespace)
    for entry in ov.local_models(overrides):
        if isinstance(entry, dict) and (entry.get("name") == spec.id or entry.get("apiBase") == api_base):
            return "yes"
    return "no"


def compute_state(
    catalog: Catalog, entities: list[dict], detail: GatewayDetail | None,
    detail_failed: bool = False, can_write: bool = True, saturated: bool = False,
    gpu: GpuState = GPU_UNKNOWN, recent: dict[str, str] | None = None,
    ready_ids: frozenset[str] = frozenset(), gateway_pending: bool = False,
) -> ReactorState:
    """`recent` maps a model id to the operation ("deploy" or "remove") the console
    submitted for it moments ago; a model whose state has not caught up yet is shown
    as SUBMITTED with no actions.

    `ready_ids` are entities whose own health report is clean (every container live
    and ready, nothing failing) while Apollo's status still says otherwise: on
    cube-m9u9i4lc a serving model read ACTIVE_PLAN for 20+ minutes after its plan
    succeeded. They count as healthy unless their status asserts a fault."""
    recent = recent or {}
    gateway = compute_gateway(catalog, entities, detail, detail_failed, pending=gateway_pending)
    can_write = can_write and not saturated
    overrides = gateway.block.overrides if gateway.block else {}
    marked = set(ov.marked_names(overrides))
    gateway.ready = _healthy(gateway.entity, ready_ids)
    gateway_healthy = gateway.ready
    writable = can_write and gateway.status in (GATEWAY_ABSENT, GATEWAY_MANAGEABLE)
    namespace = catalog.gateway.namespace

    models: list[ModelState] = []
    for spec in catalog.models:
        found = [e for e in entities if entity_product(e) == spec.product_id]
        entity = found[0] if found else None
        is_marked = spec.id in marked
        wired = _wired(gateway, overrides, spec, namespace, is_marked)
        if entity is None:
            status = OUT_OF_SYNC if is_marked else AVAILABLE
            owner = "edgeport" if is_marked else None
        elif is_marked:
            status = _model_status(entity, True, gateway_healthy, _healthy(entity, ready_ids))
            owner = "edgeport"
        else:
            # Installed without our marker (by hand, or behind a database-mode gateway
            # whose catalog the console cannot read). Decided 2026-10-13: a model
            # installed beside a gateway is SHOWN as served by the AI Reactor, status
            # from its own health, never as "installed outside Edgeport". The owner
            # stays "outside" so the console still never edits or removes it.
            status = _model_status(entity, True, gateway_healthy or gateway.status == GATEWAY_ABSENT,
                                   _healthy(entity, ready_ids))
            owner = "outside"
            if gateway.status != GATEWAY_ABSENT:
                wired = "yes"
        if _still_submitted(recent.get(spec.id), status, entity):
            status = SUBMITTED
        fits = gpu.fits(spec.min_vram_gb)
        actions: list[str] = []
        if writable and len(found) <= 1 and status != SUBMITTED:
            if status == AVAILABLE:
                # A GPU known to be too small never offers Deploy; an unknown one does.
                actions = ["deploy"] if fits != "no" else []
            elif status == OUT_OF_SYNC:
                actions = ["deploy", "remove"]
            elif owner == "edgeport" and status != REMOVING:
                actions = ["remove"]
        models.append(ModelState(
            spec=spec, status=status, entity=entity, owner=owner, wired=wired, actions=actions,
            fits=fits,
        ))

    # Display-only models (catalog `other_models`) appear only when installed, with
    # nothing to click, served by the gateway like any other.
    for shown in catalog.shown:
        entity = next((e for e in entities if entity_product(e) == shown.product_id), None)
        if entity is None:
            continue
        models.append(ModelState(
            spec=shown,  # type: ignore[arg-type]  # same display fields as ModelSpec
            status=_model_status(entity, True, gateway_healthy or gateway.status == GATEWAY_ABSENT,
                                 _healthy(entity, ready_ids)),
            entity=entity, owner="outside",
            wired="yes" if gateway.status != GATEWAY_ABSENT else "no",
        ))

    if gpu.available and gpu.total and gpu.usage_known:
        taken = gpu.free == 0
    else:
        taken = any(
            m.entity is not None and m.status != REMOVING and m.spec.gpu_count > 0 for m in models
        )
    return ReactorState(
        gateway=gateway, models=models, gpu_likely_taken=taken, saturated=saturated,
        can_write=can_write, gpu=gpu,
    )


def _still_submitted(op: str | None, status: str, entity: dict | None) -> bool:
    """Whether a change the console just submitted is still invisible in Apollo."""
    if op == "deploy":
        return entity is None
    if op == "remove":
        # The uninstall may land before the marker's removal does: until both have,
        # the model would otherwise read as out of sync and offer Deploy again.
        return (entity is not None and status != REMOVING) or status == OUT_OF_SYNC
    return False
