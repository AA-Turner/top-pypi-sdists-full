"""Vision models on the AI tab: deploy a catalog model into a cube's vision gateway
(docs/ai-reactor-deploy-spec.md §12).

The LLM side installs one Apollo entity per model and wires it into LiteLLM. Here there
is ONE entity, `esai-vision-gateway`, and a model is an entry in its `models` value, so a
deploy is either "install the gateway with this entry" or one config write adding it, and
a remove is one config write taking it out. The marker rules are the LLM gateway's
(`override.with_models` with `key="models"`): the console only ever adds, changes or
removes entries carrying `managedBy: edgeport`, and never takes over an alias someone
else wrote.

Whether a model is actually serving is something only the gateway knows (it loads models
one at a time, and one can fail, e.g. a class name the model does not have). So the state
also reads the gateway's own `GET /v1/vision/models`, through the Kubernetes API's service
proxy as the caller's Teleport identity (the GPU read's pattern). The path is built from
the CATALOG's namespace, service and port, never from the request.

Like `service`, callers pass an environment they have already authorized, and logging is
by exception class only.
"""

from __future__ import annotations

import asyncio
import copy
import functools
import json
import logging
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from cube_common.apollo_client import ApolloClient, ApolloError
from cube_cloud.reactor import override as ov
from cube_cloud.reactor import service as svc
from cube_cloud.reactor import state as st

logger = logging.getLogger(__name__)

VISION_CATALOG_PATH = Path(__file__).with_name("vision_catalog.yaml")
MODELS_KEY = "models"

_ID_RE = re.compile(r"^[a-z0-9][a-z0-9.-]{0,62}$")
_DNS_LABEL_RE = re.compile(r"^[a-z]([a-z0-9-]{0,61}[a-z0-9])?$")
_PRODUCT_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+:[A-Za-z0-9_.-]+$")
_VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
# `face-embedding` turns a face found by a detector into a vector (gateway
# POST /v1/vision/embed; SFace). It is useless without a face detector beside it, which
# its catalog entry names in `requires`.
TASKS = frozenset({"detection", "face-embedding"})
# The gateway's own model-entry keys (vision_gateway/config.py). An entry with any other
# key is refused here, so the catalog cannot smuggle something the gateway would ignore.
_ENTRY_KEYS = frozenset({"task", "backend", "path", "source", "revision", "precision",
                         "device", "classes", "scoreThreshold"})


# ---------------------------------------------------------------------------
# Catalog
# ---------------------------------------------------------------------------

class VisionCatalogError(ValueError):
    pass


@dataclass(frozen=True)
class VisionGatewaySpec:
    product_id: str
    entity_name: str
    namespace: str
    service: str
    port: int
    config_block_version: str
    release_channel: str | None
    base_overrides: dict

    @property
    def endpoint(self) -> str:
        """Where apps on the cube call it."""
        return f"http://{self.service}.{self.namespace}.svc.cluster.local:{self.port}"


@dataclass(frozen=True)
class VisionModelSpec:
    id: str
    display_name: str
    description: str
    task: str
    detects: str
    entry: dict = field(compare=False, hash=False)
    # Catalog ids this model cannot work without, deployed with it in the same gateway
    # write when missing (an embedder needs a face detector: sface requires yunet-face).
    requires: tuple[str, ...] = ()

    @property
    def backend(self) -> str:
        return self.entry.get("backend", "")

    @property
    def device(self) -> str:
        return self.entry.get("device", "cpu")

    @property
    def tags(self) -> tuple[str, ...]:
        """What it finds, as tags: the entry's class allowlist when it has one, else the
        catalog's own `detects` words as a single tag."""
        classes = self.entry.get("classes")
        return tuple(classes) if classes else (self.detects,)


@dataclass(frozen=True)
class VisionCatalog:
    gateway: VisionGatewaySpec
    models: tuple[VisionModelSpec, ...]

    def model(self, model_id: str) -> VisionModelSpec | None:
        return next((m for m in self.models if m.id == model_id), None)


def _req(raw: dict, key: str, kind: type, where: str):
    value = raw.get(key)
    if not isinstance(value, kind) or (isinstance(value, bool) and kind is not bool):
        raise VisionCatalogError(f"{where}: '{key}' must be a {kind.__name__}")
    if isinstance(value, str) and not value.strip():
        raise VisionCatalogError(f"{where}: '{key}' must not be empty")
    return value


def _match(value: str, pattern: re.Pattern, where: str, key: str) -> str:
    if not pattern.match(value):
        raise VisionCatalogError(f"{where}: '{key}' has an invalid value {value!r}")
    return value


def _entry(raw: object, where: str) -> dict:
    if not isinstance(raw, dict):
        raise VisionCatalogError(f"{where}: 'entry' must be a mapping")
    extra = set(raw) - _ENTRY_KEYS
    if extra:
        raise VisionCatalogError(f"{where}: entry keys {sorted(extra)} are not gateway model keys")
    if raw.get("task", "detection") not in TASKS:
        raise VisionCatalogError(f"{where}: entry task must be one of {sorted(TASKS)}")
    backend = raw.get("backend")
    if backend == "onnx":
        _req(raw, "path", str, where)
    elif backend == "hf":
        _req(raw, "source", str, where)
    else:
        raise VisionCatalogError(f"{where}: entry backend must be onnx or hf")
    if raw.get("device", "cpu") not in ("cpu", "gpu"):
        raise VisionCatalogError(f"{where}: entry device must be cpu or gpu")
    classes = raw.get("classes", [])
    if not isinstance(classes, list) or not all(isinstance(c, str) and c for c in classes):
        raise VisionCatalogError(f"{where}: entry classes must be a list of label names")
    return copy.deepcopy(raw)


def parse_vision_catalog(text: str) -> VisionCatalog:
    try:
        raw = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise VisionCatalogError(f"vision catalog is not valid YAML ({type(e).__name__})") from None
    if not isinstance(raw, dict) or raw.get("version") != 1:
        raise VisionCatalogError("vision catalog must be a mapping with version 1")
    g = raw.get("gateway")
    if not isinstance(g, dict):
        raise VisionCatalogError("'gateway' must be a mapping")
    base = _req(g, "base_overrides", dict, "gateway")
    if base.get(MODELS_KEY) != []:
        raise VisionCatalogError("gateway: base_overrides.models must be an empty list")
    channel = g.get("release_channel")
    if channel is not None and (not isinstance(channel, str) or not channel.strip()):
        raise VisionCatalogError("gateway: 'release_channel' must be null or a channel name")
    gateway = VisionGatewaySpec(
        product_id=_match(_req(g, "product_id", str, "gateway"), _PRODUCT_ID_RE, "gateway", "product_id"),
        entity_name=_req(g, "entity_name", str, "gateway"),
        namespace=_match(_req(g, "namespace", str, "gateway"), _DNS_LABEL_RE, "gateway", "namespace"),
        service=_match(_req(g, "service", str, "gateway"), _DNS_LABEL_RE, "gateway", "service"),
        port=_req(g, "port", int, "gateway"),
        config_block_version=_match(_req(g, "config_block_version", str, "gateway"), _VERSION_RE,
                                    "gateway", "config_block_version"),
        release_channel=channel,
        base_overrides=base,
    )
    models_raw = raw.get("models")
    if not isinstance(models_raw, list) or not models_raw:
        raise VisionCatalogError("'models' must be a non-empty list")
    models = []
    for i, m in enumerate(models_raw):
        where = f"models[{i}]"
        if not isinstance(m, dict):
            raise VisionCatalogError(f"{where} must be a mapping")
        task = _req(m, "task", str, where)
        if task not in TASKS:
            raise VisionCatalogError(f"{where}: 'task' must be one of {sorted(TASKS)}")
        entry = _entry(m.get("entry"), where)
        if entry.get("task", "detection") != task:
            raise VisionCatalogError(f"{where}: 'task' and entry task must agree")
        requires = m.get("requires", [])
        if not isinstance(requires, list) or not all(isinstance(r, str) for r in requires):
            raise VisionCatalogError(f"{where}: 'requires' must be a list of catalog ids")
        models.append(VisionModelSpec(
            id=_match(_req(m, "id", str, where), _ID_RE, where, "id"),
            display_name=_req(m, "display_name", str, where),
            description=_req(m, "description", str, where),
            task=task,
            detects=_req(m, "detects", str, where),
            entry=entry,
            requires=tuple(requires),
        ))
    ids = [m.id for m in models]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise VisionCatalogError(f"models: duplicate id {dupes}")
    for m in models:
        missing = [r for r in m.requires if r not in ids or r == m.id]
        if missing:
            raise VisionCatalogError(f"{m.id}: 'requires' names {missing}, not other catalog models")
    return VisionCatalog(gateway=gateway, models=tuple(models))


@functools.lru_cache(maxsize=1)
def load_vision_catalog() -> VisionCatalog:
    return parse_vision_catalog(VISION_CATALOG_PATH.read_text(encoding="utf-8"))


def marked_entry(model: VisionModelSpec) -> dict:
    """The `models` entry the console writes: the catalog's entry, named and marked."""
    return {"name": model.id, **copy.deepcopy(model.entry), ov.MARKER_KEY: ov.MARKER_VALUE}


# ---------------------------------------------------------------------------
# The gateway's own view: GET /v1/vision/models through the service proxy
# ---------------------------------------------------------------------------

LIVE_TIMEOUT_SECONDS = 15.0
LIVE_CACHE_SECONDS = 5.0
# A failed read is remembered for longer than the tab's 15 s poll (AiTab.tsx AI_POLL_MS), so an
# unresponsive gateway costs one shell-out a minute rather than one per poll per viewer.
LIVE_FAILURE_CACHE_SECONDS = 60.0
# How long a page load or a write's re-read waits for the gateway before carrying on without its
# view ("could not ask"); the read finishes in the background into the cache. The same rule as
# the GPU read beside it (service.GPU_WAIT_ON_READ_SECONDS, AGENTS.md AI-tab item 8).
LIVE_WAIT_ON_READ_SECONDS = 4.0
_DEFAULT_WAIT = object()          # LIVE_WAIT_ON_READ_SECONDS, read when called rather than when defined
LIVE_ERROR_MAX_CHARS = 300
LIVE_LABELS_MAX = 200
LIVE_LABEL_MAX_CHARS = 60
LIVE_IMAGE_MAX_CHARS = 300
# What one model contributes from the gateway's answer. Everything else it says (paths,
# sources, input geometry) stays server-side. Labels, the display name and the image are
# kept because a model outside the catalog has no catalog text to describe it, and they
# come from the model's own card, which the cube's operator wrote.
_LIVE_STATUSES = frozenset({"loading", "ready", "error"})
# A model image reference as the gateway reports it: `<registry>/<path>:<tag>@sha256:...`
# or a tag alone. Anything else is dropped rather than shown.
_IMAGE_RE = re.compile(r"^[a-z0-9.-]+(:[0-9]+)?/[a-z0-9._/-]+(:[A-Za-z0-9_.-]{1,128})?(@sha256:[0-9a-f]{64})?$")


@dataclass(frozen=True)
class LiveModel:
    status: str              # loading | ready | error
    error: str = ""
    runtime: str = ""
    device: str = ""
    display_name: str = ""
    labels: tuple[str, ...] = ()     # the first LIVE_LABELS_MAX
    label_count: int = 0             # how many the gateway listed
    image: str = ""


_live_cache: dict[tuple[str, str], tuple[float, dict[str, LiveModel] | None]] = {}
# One gateway read in flight per (route, profile, cluster): concurrent viewers share it.
_live_inflight: dict[tuple[str, str, str], asyncio.Task] = {}


@dataclass(frozen=True)
class LiveStreams:
    """The gateway's camera streams, reduced to two counts: no camera id, model or error
    text crosses to the browser."""
    cameras: int          # distinct cameras with a connected stream and a subscriber
    subscriptions: int    # subscribers across every stream


_streams_cache: dict[tuple[str, str], tuple[float, LiveStreams | None]] = {}


def parse_streams(text: str) -> LiveStreams | None:
    """The gateway's `/v1/vision/streams` answer as counts. None when it is not the shape
    the gateway sends."""
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return None
    streams = data.get("streams") if isinstance(data, dict) else None
    if not isinstance(streams, list):
        return None
    cameras, subscriptions = set(), 0
    for s in streams:
        if not isinstance(s, dict):
            continue
        subs = s.get("subscribers")
        subs = subs if isinstance(subs, int) and not isinstance(subs, bool) and subs > 0 else 0
        subscriptions += subs
        if subs and s.get("state") == "connected" and isinstance(s.get("camera"), str):
            cameras.add(s["camera"])
    return LiveStreams(cameras=len(cameras), subscriptions=subscriptions)


def parse_live(text: str) -> dict[str, LiveModel] | None:
    """The gateway's `/v1/vision/models` answer, reduced to an allowlist per model. None
    when it is not the shape the gateway sends."""
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return None
    models = data.get("models") if isinstance(data, dict) else None
    if not isinstance(models, list):
        return None
    out: dict[str, LiveModel] = {}
    for m in models:
        if not isinstance(m, dict) or not isinstance(m.get("name"), str):
            continue
        status = m.get("status") if m.get("status") in _LIVE_STATUSES else "loading"
        error = str(m.get("error") or "")[:LIVE_ERROR_MAX_CHARS] if status == "error" else ""
        labels = m.get("labels") if isinstance(m.get("labels"), list) else []
        out[m["name"]] = LiveModel(status=status, error=error,
                                   runtime=str(m.get("runtime") or "")[:80],
                                   device=str(m.get("device") or "")[:40],
                                   display_name=_text(m.get("display_name"), 120),
                                   labels=tuple(_text(x, LIVE_LABEL_MAX_CHARS)
                                                for x in labels[:LIVE_LABELS_MAX] if isinstance(x, str)),
                                   label_count=sum(isinstance(x, str) for x in labels),
                                   image=_image(m.get("image")))
    return out


def _text(value: object, cap: int) -> str:
    """A one-line string from the gateway: control characters dropped, capped."""
    if not isinstance(value, str):
        return ""
    return "".join(ch for ch in value if ch.isprintable()).strip()[:cap]


def _image(value: object) -> str:
    return value if isinstance(value, str) and len(value) <= LIVE_IMAGE_MAX_CHARS and _IMAGE_RE.match(value) else ""


async def _read_gateway(cluster: str, profile: str, gateway: VisionGatewaySpec, route: str,
                        parse, cache: dict, what: str, wait=_DEFAULT_WAIT):
    """One GET through the Kubernetes service proxy to the gateway, parsed, cached per
    (profile, cluster): briefly on success, LIVE_FAILURE_CACHE_SECONDS on failure. One read
    per (route, profile, cluster) is in flight at a time. With `wait`, None is returned after
    that many seconds and the read finishes in the background, so a slow gateway never holds
    a page load or a write's response. None when it could not be read. Never raises."""
    if wait is _DEFAULT_WAIT:
        wait = LIVE_WAIT_ON_READ_SECONDS
    key = (profile, cluster)
    hit = cache.get(key)
    if hit and hit[0] > time.monotonic():
        return hit[1]
    fkey = (route, profile, cluster)
    task = _live_inflight.get(fkey)
    if task is None or task.done() or task.get_loop() is not asyncio.get_running_loop():
        task = asyncio.get_running_loop().create_task(
            _fetch_gateway(cluster, profile, gateway, route, parse, cache, what))
        _live_inflight[fkey] = task
        task.add_done_callback(lambda t, k=fkey: _live_inflight.pop(k, None) if _live_inflight.get(k) is t else None)
    if wait is None:
        return await asyncio.shield(task)
    try:
        return await asyncio.wait_for(asyncio.shield(task), timeout=wait)
    except asyncio.TimeoutError:
        return None                     # not cached: the read itself caches what it finds


async def _fetch_gateway(cluster: str, profile: str, gateway: VisionGatewaySpec, route: str,
                         parse, cache: dict, what: str):
    key = (profile, cluster)
    from cube_cloud.teleport.kubeconfig import run_kubectl

    path = (f"/api/v1/namespaces/{gateway.namespace}/services/"
            f"{gateway.service}:{gateway.port}/proxy{route}")
    result = None
    try:
        out, rc = await asyncio.wait_for(
            run_kubectl(["get", "--raw", path], cluster=cluster, profile=profile,
                        timeout=LIVE_TIMEOUT_SECONDS),
            timeout=LIVE_TIMEOUT_SECONDS + 5,
        )
        if rc == 0:
            result = parse(out)
        else:
            logger.info("vision: gateway %s unavailable on %s (rc %s)", what, cluster, rc)
    except Exception as e:  # noqa: BLE001 -- class only
        logger.warning("vision: gateway %s read on %s failed (%s)", what, cluster, type(e).__name__)
    ttl = LIVE_CACHE_SECONDS if result is not None else LIVE_FAILURE_CACHE_SECONDS
    cache[key] = (time.monotonic() + ttl, result)
    return result


async def read_live(cluster: str, profile: str, gateway: VisionGatewaySpec,
                    wait=_DEFAULT_WAIT) -> dict[str, LiveModel] | None:
    """The gateway's per-model state, or None when it could not be read (not installed
    yet, restarting, kubectl failed, or not within `wait`). Never raises."""
    return await _read_gateway(cluster, profile, gateway, "/v1/vision/models", parse_live,
                               _live_cache, "model list", wait)


async def read_streams(cluster: str, profile: str, gateway: VisionGatewaySpec,
                       wait=_DEFAULT_WAIT) -> LiveStreams | None:
    """How many cameras the gateway is streaming detections for, or None. Never raises."""
    return await _read_gateway(cluster, profile, gateway, "/v1/vision/streams", parse_streams,
                               _streams_cache, "stream list", wait)


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

# Model statuses: the LLM side's where they mean the same thing, plus two of its own.
AVAILABLE, SUBMITTED, INSTALLING, STARTING, READY = (
    st.AVAILABLE, st.SUBMITTED, st.INSTALLING, st.STARTING, st.READY)
NEEDS_ATTENTION, OUTSIDE = st.NEEDS_ATTENTION, st.OUTSIDE
CONFIGURED = "configured"   # in the gateway's config; the gateway's own view is unreadable
FAILED = "failed"           # the gateway says it could not load the model


@dataclass
class VisionModelState:
    spec: VisionModelSpec
    status: str
    owner: str | None = None          # edgeport | outside | None
    actions: list[str] = field(default_factory=list)
    live: LiveModel | None = None


# Who put a model outside the catalog on the gateway, read off its entry's marker.
SOURCE_REGISTERED = "registered"      # `registeredBy: model_tools` (model_tools register)
SOURCE_EDGEPORT = "edgeport"          # the console's marker on a model no longer in the catalog
SOURCE_OUTSIDE = "outside"            # anything else: by hand, or unknown
REGISTERED_KEY, REGISTERED_VALUE = "registeredBy", "model_tools"
# The console's own mark on a model it registered through an upload. `registeredBy:
# model_tools` is the gateway product's marker and is also written by an operator's
# `model_tools register` on the cube, so it cannot say who added an entry; only an entry
# carrying THIS key is one the console may remove (AGENTS.md AI-tab item 2: the console never
# removes an entry it did not write).
UPLOADED_KEY, UPLOADED_VALUE = "uploadedBy", "edgeport"
OTHER_MODELS_MAX = 50


@dataclass
class OtherModel:
    """A model the gateway serves that is not a catalog card. Shown, and acted on only when
    `removable`: a model the console itself uploaded (UPLOADED_KEY)."""
    name: str
    status: str                       # ready | starting | failed | configured
    source: str
    device: str = ""                  # the entry's request, cpu | gpu, when the config was read
    live: LiveModel | None = None
    image: str = ""
    removable: bool = False


@dataclass
class VisionState:
    gateway: st.GatewayState
    models: list[VisionModelState]
    can_write: bool
    saturated: bool
    live_available: bool
    endpoint: str
    others: list[OtherModel] = field(default_factory=list)
    streams: LiveStreams | None = None

    def model(self, model_id: str) -> VisionModelState | None:
        return next((m for m in self.models if m.spec.id == model_id), None)


def compute_gateway(catalog: VisionCatalog, entities: list[dict], detail: st.GatewayDetail | None,
                    detail_failed: bool, pending: bool) -> st.GatewayState:
    """The vision gateway's state: the LLM gateway's rules minus the LiteLLM-specific
    ones (database mode, credentials in the override) that this chart does not have."""
    found = [e for e in entities if st.entity_product(e) == catalog.gateway.product_id]
    if not found:
        return st.GatewayState(status=st.GATEWAY_ABSENT)
    if len(found) > 1:
        return st.GatewayState(status=st.GATEWAY_READ_ONLY, reason=st.REASON_MULTIPLE, entity=found[0])
    entity = found[0]
    if detail_failed or detail is None:
        return st.GatewayState(status=st.GATEWAY_UNKNOWN, entity=entity)
    gw = st.GatewayState(status=st.GATEWAY_MANAGEABLE, entity=entity, mode="config",
                         release_channel=detail.release_channel)
    if detail.module_coordinate:
        gw.status, gw.reason = st.GATEWAY_READ_ONLY, st.REASON_MODULE
        return gw
    try:
        block = ov.parse_declared_config(detail.config, catalog.gateway.config_block_version)
    except ov.OverrideUnreadable as e:
        gw.status, gw.reason = st.GATEWAY_READ_ONLY, e.reason
        return gw
    gw.block = block
    gw.console_installed = ov.gateway_is_marked(block.overrides)
    if st._pending(entity) or pending:
        gw.status, gw.reason = st.GATEWAY_READ_ONLY, st.REASON_PENDING
    return gw


def compute_state(catalog: VisionCatalog, entities: list[dict], detail: st.GatewayDetail | None,
                  detail_failed: bool = False, *, can_write: bool = True, saturated: bool = False,
                  live: dict[str, LiveModel] | None = None, recent: dict[str, str] | None = None,
                  gateway_pending: bool = False) -> VisionState:
    """Pure: what each catalog model's status is and which actions are open."""
    recent = recent or {}
    gw = compute_gateway(catalog, entities, detail, detail_failed, gateway_pending)
    # Serving: Apollo says HEALTHY, or the gateway itself answered. Apollo's status lags a
    # serving pod by minutes (the LLM side's ACTIVE_PLAN case; seen here too on
    # cube-66odzn95, 2026-10-08: "Vision gateway: starting" beside a model reading Ready).
    gw.ready = gw.health == "HEALTHY" or (live is not None and gw.status != st.GATEWAY_ABSENT)
    can_write = can_write and not saturated
    writable = can_write and gw.status in (st.GATEWAY_ABSENT, st.GATEWAY_MANAGEABLE)
    overrides = gw.block.overrides if gw.block else {}
    entries = [e for e in ov.local_models(overrides, MODELS_KEY) if isinstance(e, dict)]
    models = []
    for spec in catalog.models:
        named = [e for e in entries if e.get("name") == spec.id]
        marked = any(ov.is_marked(e) for e in named)
        lv = (live or {}).get(spec.id)
        owner = "edgeport" if marked else ("outside" if named else None)
        if gw.status == st.GATEWAY_UNKNOWN:
            status = CONFIGURED if gw.entity else AVAILABLE
            owner = None
        elif not named:
            status = AVAILABLE
        elif not marked:
            status = OUTSIDE
        elif gw.lifecycle == st.PENDING_INSTALL:
            status = INSTALLING
        elif lv is None:
            # In the config, but the gateway does not list it (yet) or could not be read.
            status = STARTING if live is not None or gw.status == st.GATEWAY_READ_ONLY else CONFIGURED
        elif lv.status == "ready":
            status = READY
        elif lv.status == "error":
            status = FAILED
        else:
            status = STARTING
        op = recent.get(spec.id)
        if (op == "deploy" and not marked) or (op == "remove" and marked):
            status = SUBMITTED
        actions: list[str] = []
        if writable and status != SUBMITTED and len(named) <= 1:
            if status == AVAILABLE:
                actions = ["deploy"]
            elif owner == "edgeport":
                actions = ["remove"]
        models.append(VisionModelState(spec=spec, status=status, owner=owner, actions=actions, live=lv))
    return VisionState(gateway=gw, models=models, can_write=can_write, saturated=saturated,
                       live_available=live is not None, endpoint=catalog.gateway.endpoint,
                       others=other_models(catalog, gw, entries, live))


def other_models(catalog: VisionCatalog, gw: st.GatewayState, entries: list[dict],
                 live: dict[str, LiveModel] | None) -> list[OtherModel]:
    """Every model on the gateway that is not a catalog card: registered customer models,
    hand-added ones, and console entries whose catalog model was since withdrawn. From the
    config when it was read, and from the gateway's own list, so a model shows when either
    names it. Read-only: the console never edits an entry it did not write."""
    if gw.status == st.GATEWAY_ABSENT:
        return []
    catalog_ids = {m.id for m in catalog.models}
    names: list[str] = []
    by_name: dict[str, dict] = {}
    for e in entries:
        name = e.get("name")
        if isinstance(name, str) and name not in catalog_ids and name not in by_name:
            by_name[name] = e
            names.append(name)
    names += [n for n in (live or {}) if n not in catalog_ids and n not in by_name]
    out = []
    for name in names[:OTHER_MODELS_MAX]:
        e = by_name.get(name, {})
        lv = (live or {}).get(name)
        if lv is not None:
            status = {"ready": READY, "error": FAILED}.get(lv.status, STARTING)
        else:
            status = STARTING if live is not None else CONFIGURED
        if ov.is_marked(e):
            source = SOURCE_EDGEPORT
        elif e.get(REGISTERED_KEY) == REGISTERED_VALUE:
            source = SOURCE_REGISTERED
        else:
            source = SOURCE_OUTSIDE
        device = e.get("device") if e.get("device") in ("cpu", "gpu") else ""
        out.append(OtherModel(name=_text(name, 80), status=status, source=source, device=device,
                              live=lv, image=(lv.image if lv and lv.image else _image(e.get("image"))),
                              removable=source == SOURCE_REGISTERED and e.get(UPLOADED_KEY) == UPLOADED_VALUE))
    return out


_recent: dict[tuple[str, str], tuple[str, float]] = {}
_pending_gateway: dict[str, tuple[dict, float]] = {}


def _recent_for(env_id: str) -> dict[str, str]:
    now = time.monotonic()
    for k in [k for k, (_, exp) in _recent.items() if exp <= now]:
        del _recent[k]
    return {m: op for (e, m), (op, _) in _recent.items() if e == env_id}


def _gateway_pending(env_id: str, current: dict | None) -> bool:
    entry = _pending_gateway.get(env_id)
    if entry is None:
        return False
    want, expires = entry
    if time.monotonic() >= expires or current == want:
        _pending_gateway.pop(env_id, None)
        return False
    return True


async def read_state(client: ApolloClient, env: dict, can_write: bool, *, profile: str | None = None,
                     catalog: VisionCatalog | None = None) -> VisionState:
    """The vision side of one authorized cube. Raises like `service.read_state` when the
    entity list cannot be read; the gateway's own view is optional (`live_available`)."""
    catalog = catalog or load_vision_catalog()
    env_id = env.get("id") or ""
    entities, saturated = await svc._entities(client, env_id)
    found = [e for e in entities if st.entity_product(e) == catalog.gateway.product_id]
    detail, detail_failed = None, False
    if len(found) == 1:
        detail = await svc._gateway_detail(client, env_id, found[0].get("id") or "")
        detail_failed = detail is None
    current = None
    if detail is not None:
        try:
            current = ov.parse_declared_config(detail.config, "0.0.0").overrides
        except ov.OverrideUnreadable:
            current = None
    live = streams = None
    if profile and len(found) == 1 and (found[0].get("lifecycleStatus") or "") == st.INSTALLED:
        live, streams = await asyncio.gather(
            read_live(env.get("name") or "", profile, catalog.gateway),
            read_streams(env.get("name") or "", profile, catalog.gateway))
    state = compute_state(catalog, entities, detail, detail_failed, can_write=can_write,
                          saturated=saturated, live=live, recent=_recent_for(env_id),
                          gateway_pending=_gateway_pending(env_id, current))
    state.streams = streams
    for m in state.models:
        if m.status != SUBMITTED:
            _recent.pop((env_id, m.spec.id), None)
    return state


async def safe_read_state(client: ApolloClient, env: dict, can_write: bool, *,
                          profile: str | None = None) -> VisionState | None:
    """`read_state`, or None on any failure: the vision section must never take down the
    rest of the AI tab."""
    try:
        return await read_state(client, env, can_write, profile=profile)
    except Exception as e:  # noqa: BLE001 -- class only
        logger.warning("vision: state read failed (%s)", type(e).__name__)
        return None


# ---------------------------------------------------------------------------
# Writes
# ---------------------------------------------------------------------------

async def _write_models(client: ApolloClient, env: dict, gw: st.GatewayState,
                        add: list[VisionModelSpec], remove: list[str],
                        deadline: svc._Deadline) -> tuple[bool, str]:
    """ONE config write to the gateway's `models`. (wrote, request_status)."""
    assert gw.block is not None and gw.entity is not None
    merged = ov.with_models(gw.block.overrides, add=[marked_entry(m) for m in add],
                            remove=remove, key=MODELS_KEY)
    return await _write_merged(client, env, gw, merged, deadline)


async def _write_merged(client: ApolloClient, env: dict, gw: st.GatewayState, merged: dict,
                        deadline: svc._Deadline) -> tuple[bool, str]:
    """ONE config write of `merged` to the gateway, then wait for it like any other."""
    assert gw.block is not None and gw.entity is not None
    if merged == gw.block.overrides:
        return False, ""
    result = await svc._write_config(client, env, gw.entity["id"], ov.ConfigBlock(gw.block.version, merged))
    if result.error:
        raise svc._StepRefused(result.error)
    if result.no_changes:
        return False, ""
    landed = False
    if not svc._pending_approval(result.request_status):
        landed = await svc._await_config(client, env["id"], gw.entity["id"], merged, deadline)
    if not landed:
        _pending_gateway[env["id"]] = (merged, time.monotonic() + svc.RECENT_SECONDS)
    return True, result.request_status


def _refusal(state: VisionState) -> str | None:
    gw = state.gateway
    if gw.status == st.GATEWAY_UNKNOWN:
        return "The console could not read this cube's vision gateway, so nothing was changed."
    if gw.status == st.GATEWAY_READ_ONLY:
        return {
            st.REASON_MODULE: "This cube's vision gateway is managed by an Apollo module, so the console leaves it alone.",
            st.REASON_MULTIPLE: "This cube has more than one vision gateway, so the console won't guess which to change.",
            st.REASON_PENDING: "A change to this cube's vision gateway is waiting to be applied. Try again once it has.",
        }.get(gw.reason or "", "This cube's vision gateway config was edited by hand in a form the console won't rewrite.")
    if state.saturated:
        return svc.TOO_MANY
    return None


async def _locked(env: dict, op):
    deadline = svc._Deadline(svc.CALL_BUDGET_SECONDS)
    lock = svc._cube_lock(env.get("id") or "")          # shared with the LLM side
    if not await svc._acquire(lock, deadline):
        return svc._refused(svc.BUSY)
    try:
        return await op(deadline)
    finally:
        lock.release()


def _done(pending: bool, message: str, state: VisionState | None, steps: list[str]) -> svc.WriteResult:
    if pending:
        return svc.WriteResult(True, svc.SUBMITTED, message + " Apollo is applying the change; on a cube where "
                               "changes need approval, it waits for that first.", state, steps)
    return svc.WriteResult(True, svc.APPLIED, message, state, steps)


async def deploy(client: ApolloClient, env: dict, model_id: str, *, can_write: bool,
                 profile: str | None = None, catalog: VisionCatalog | None = None) -> svc.WriteResult:
    catalog = catalog or load_vision_catalog()
    spec = catalog.model(model_id)
    if spec is None:
        return svc._refused("That model is not in the vision catalog.")
    if not can_write:
        return svc._refused(svc.NOT_ALLOWED)

    async def op(deadline):
        state = await read_state(client, env, True, profile=profile, catalog=catalog)
        model = state.model(spec.id)
        assert model is not None
        if model.status == SUBMITTED:
            return svc.WriteResult(True, svc.APPLIED, f"{spec.display_name} was just submitted. Apollo is applying it.", state)
        if (refusal := _refusal(state)) is not None:
            return svc._refused(refusal, state)
        if "deploy" not in model.actions:
            if model.owner == "edgeport":
                return svc.WriteResult(True, svc.APPLIED, f"{spec.display_name} is already on this cube.", state)
            if model.status == OUTSIDE:
                return svc._refused(f"This cube's vision gateway already has a model named {spec.id} that "
                                    "Edgeport did not add, so the console leaves it alone.", state)
            return svc._refused(f"{spec.display_name} can't be deployed right now.", state)
        steps: list[str] = []
        pending = False
        # What it requires and the gateway lacks goes in the SAME write (one gateway write
        # per operation: two pending config changes merge badly, service._pending_gateway).
        # A required model already there, by Edgeport or by hand, is left as it is.
        needed = [
            catalog.model(r) for r in spec.requires
            if (have := state.model(r)) is not None and have.status == AVAILABLE
        ]
        adds = [spec, *[n for n in needed if n is not None]]
        for m in adds:
            _recent[(env["id"], m.id)] = ("deploy", time.monotonic() + svc.RECENT_SECONDS)
        try:
            if state.gateway.status == st.GATEWAY_ABSENT:
                overrides = copy.deepcopy(catalog.gateway.base_overrides)
                overrides[ov.MARKER_KEY] = ov.MARKER_VALUE
                overrides[MODELS_KEY] = [marked_entry(m) for m in adds]
                status = await svc._install(
                    client, env, entity_name=catalog.gateway.entity_name,
                    product_id=catalog.gateway.product_id, namespace=catalog.gateway.namespace,
                    block=ov.ConfigBlock(catalog.gateway.config_block_version, overrides),
                    release_channel=catalog.gateway.release_channel,
                )
                steps.append("vision gateway install requested")
                pending = svc._pending_approval(status)
            else:
                wrote, status = await _write_models(client, env, state.gateway, adds, [], deadline)
                if wrote:
                    steps.append("vision gateway models updated")
                    pending = svc._pending_approval(status)
        except (ApolloError, svc._StepRefused, ov.OverrideUnreadable) as e:
            for m in adds:
                _recent.pop((env["id"], m.id), None)
            logger.error("vision deploy of %s on %s refused (%s)", spec.id, env.get("name"), type(e).__name__)
            if isinstance(e, ov.OverrideUnreadable) and e.reason == "name_taken":
                return svc._refused(f"This cube's vision gateway already has a model named {spec.id}.", state)
            return svc._refused("Apollo refused the change. Nothing was written.",
                                await safe_read_state(client, env, True, profile=profile))
        except BaseException:
            for m in adds:
                _recent.pop((env["id"], m.id), None)
            raise
        if not steps:
            for m in adds:
                _recent.pop((env["id"], m.id), None)
        after = await safe_read_state(client, env, True, profile=profile)
        first = ("The gateway starts first, then loads it." if state.gateway.status == st.GATEWAY_ABSENT
                 else "The gateway restarts to load it.")
        if spec.backend == "hf":
            first += " Its first start downloads the model from Hugging Face."
        with_it = (f" with {', '.join(n.display_name for n in adds[1:])}, which it needs"
                   if len(adds) > 1 else "")
        return _done(pending, f"Deploying {spec.display_name}{with_it}. {first}", after, steps)

    return await _locked(env, op)


async def remove(client: ApolloClient, env: dict, model_id: str, *, can_write: bool,
                 profile: str | None = None, catalog: VisionCatalog | None = None) -> svc.WriteResult:
    catalog = catalog or load_vision_catalog()
    spec = catalog.model(model_id)
    if spec is None:
        return svc._refused("That model is not in the vision catalog.")
    if not can_write:
        return svc._refused(svc.NOT_ALLOWED)

    async def op(deadline):
        state = await read_state(client, env, True, profile=profile, catalog=catalog)
        model = state.model(spec.id)
        assert model is not None
        if model.status == SUBMITTED:
            return svc.WriteResult(True, svc.APPLIED, f"A change to {spec.display_name} was just submitted.", state)
        if (refusal := _refusal(state)) is not None:
            return svc._refused(refusal, state)
        if model.owner != "edgeport":
            if model.status == AVAILABLE:
                return svc.WriteResult(True, svc.APPLIED, f"{spec.display_name} is not on this cube.", state)
            return svc._refused(f"{spec.display_name} was added to the gateway outside Edgeport, so the console won't remove it.", state)
        _recent[(env["id"], spec.id)] = ("remove", time.monotonic() + svc.RECENT_SECONDS)
        try:
            wrote, status = await _write_models(client, env, state.gateway, [], [spec.id], deadline)
        except (ApolloError, svc._StepRefused, ov.OverrideUnreadable) as e:
            _recent.pop((env["id"], spec.id), None)
            logger.error("vision remove of %s on %s refused (%s)", spec.id, env.get("name"), type(e).__name__)
            return svc._refused("Apollo refused the change. Nothing was written.",
                                await safe_read_state(client, env, True, profile=profile))
        except BaseException:
            _recent.pop((env["id"], spec.id), None)
            raise
        if not wrote:
            _recent.pop((env["id"], spec.id), None)
        after = await safe_read_state(client, env, True, profile=profile)
        return _done(svc._pending_approval(status), f"Removing {spec.display_name}. The gateway restarts without it.",
                     after, ["vision gateway models updated"] if wrote else [])

    return await _locked(env, op)


# ---------------------------------------------------------------------------
# Registered (custom) models: the console's upload flow (reactor/vision_upload.py)
# ---------------------------------------------------------------------------
#
# The console only ever writes entries it can name the writer of: `managedBy: edgeport`
# for catalog models (above), and `uploadedBy: edgeport` (beside the gateway's own
# `registeredBy: model_tools`) for a model registered through an upload. Everything else on a
# gateway, a model an operator registered with `model_tools register` included, stays read-only.

def with_registered(overrides: dict, entry: dict) -> dict:
    """The overrides with a registered `entry` added; every other entry kept verbatim.
    A name already on the gateway, from any writer, is refused (`name_taken`)."""
    current = [e for e in ov.local_models(overrides, MODELS_KEY)]
    if any(isinstance(e, dict) and e.get("name") == entry["name"] for e in current):
        raise ov.OverrideUnreadable("name_taken")
    out = copy.deepcopy(overrides)
    out[MODELS_KEY] = current + [copy.deepcopy(entry)]
    return out


def without_registered(overrides: dict, name: str) -> dict:
    """The overrides with the uploaded entry `name` taken out. An entry of that name that
    the console's upload flow did not write is left alone (`not_registered`)."""
    current = list(ov.local_models(overrides, MODELS_KEY))
    named = [e for e in current if isinstance(e, dict) and e.get("name") == name]
    if any(e.get(REGISTERED_KEY) != REGISTERED_VALUE or e.get(UPLOADED_KEY) != UPLOADED_VALUE for e in named):
        raise ov.OverrideUnreadable("not_registered")
    out = copy.deepcopy(overrides)
    out[MODELS_KEY] = [e for e in current if not (isinstance(e, dict) and e.get("name") == name)]
    return out


async def add_registered(client: ApolloClient, env: dict, entry: dict, *, profile: str | None = None,
                         catalog: VisionCatalog | None = None) -> svc.WriteResult:
    """Put a registered model's `entry` on the cube's vision gateway: one config write, or
    the gateway's install with it when the cube has none. Same lock and refusals as a
    catalog deploy."""
    catalog = catalog or load_vision_catalog()
    if catalog.model(entry["name"]) is not None:
        return svc._refused(f"{entry['name']} is a catalog model's name; choose another.")

    async def op(deadline):
        state = await read_state(client, env, True, profile=profile, catalog=catalog)
        if (refusal := _refusal(state)) is not None:
            return svc._refused(refusal, state)
        try:
            if state.gateway.status == st.GATEWAY_ABSENT:
                overrides = copy.deepcopy(catalog.gateway.base_overrides)
                overrides[ov.MARKER_KEY] = ov.MARKER_VALUE
                overrides[MODELS_KEY] = [copy.deepcopy(entry)]
                status = await svc._install(
                    client, env, entity_name=catalog.gateway.entity_name,
                    product_id=catalog.gateway.product_id, namespace=catalog.gateway.namespace,
                    block=ov.ConfigBlock(catalog.gateway.config_block_version, overrides),
                    release_channel=catalog.gateway.release_channel,
                )
                return _done(svc._pending_approval(status), f"Installing the vision gateway with {entry['name']}.",
                             None, ["vision gateway install requested"])
            merged = with_registered(state.gateway.block.overrides, entry)
            wrote, status = await _write_merged(client, env, state.gateway, merged, deadline)
        except ov.OverrideUnreadable as e:
            if e.reason == "name_taken":
                return svc._refused(f"This cube's vision gateway already has a model named {entry['name']}.", state)
            return svc._refused("The vision gateway's config could not be read, so nothing was written.", state)
        except (ApolloError, svc._StepRefused) as e:
            logger.error("vision register of %s on %s refused (%s)", entry["name"], env.get("name"), type(e).__name__)
            return svc._refused("Apollo refused the change. Nothing was written.", state)
        return _done(svc._pending_approval(status), f"Adding {entry['name']}. The gateway restarts to load it.",
                     None, ["vision gateway models updated"] if wrote else [])

    return await _locked(env, op)


async def remove_registered(client: ApolloClient, env: dict, name: str, *, can_write: bool,
                            profile: str | None = None, catalog: VisionCatalog | None = None) -> svc.WriteResult:
    """Take an uploaded model off the gateway. Only an entry the console's upload flow wrote."""
    catalog = catalog or load_vision_catalog()
    if not can_write:
        return svc._refused(svc.NOT_ALLOWED)

    async def op(deadline):
        state = await read_state(client, env, True, profile=profile, catalog=catalog)
        if (refusal := _refusal(state)) is not None:
            return svc._refused(refusal, state)
        other = next((o for o in state.others if o.name == name), None)
        if other is None:
            return svc._refused("That model is not on this cube's vision gateway.", state)
        if not other.removable:
            return svc._refused(f"{name} was added outside the console, so the console won't remove it.", state)
        try:
            merged = without_registered(state.gateway.block.overrides, name)
            wrote, status = await _write_merged(client, env, state.gateway, merged, deadline)
        except (ApolloError, svc._StepRefused, ov.OverrideUnreadable) as e:
            logger.error("vision remove of registered %s on %s refused (%s)", name, env.get("name"), type(e).__name__)
            return svc._refused("Apollo refused the change. Nothing was written.",
                                await safe_read_state(client, env, True, profile=profile))
        after = await safe_read_state(client, env, True, profile=profile)
        return _done(svc._pending_approval(status), f"Removing {name}. The gateway restarts without it.",
                     after, ["vision gateway models updated"] if wrote else [])

    return await _locked(env, op)


def is_registered_here(state: VisionState | None, name: str) -> bool:
    return bool(state) and any(o.name == name and o.removable for o in state.others)

