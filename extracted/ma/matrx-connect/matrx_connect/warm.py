"""Warm-up registry: prepare what a person is about to need, the moment they land on a page.

Router-free. A host registers warmers at boot (``register_warmer``) and mounts its own
endpoint, which calls ``run_warm(items)`` and answers at once. ``run_warm`` sorts the items into
accepted / unknown, applies a per-person per-item throttle, and runs the accepted warmers
concurrently in ONE detached task that carries the caller's AppContext (``detached_task``
carries it; the request's transaction state is left behind). Each warmer is bounded by its
timeout; failures are logged, never raised — warming is an optimization, never a dependency.

FAN-OUT. A warmer that fills only THIS process's memory (``fill="process"`` — an ORM
definition cache, a resolver cache) helps one server in N. When ``run_warm`` schedules such an
item it also publishes it on ``mx:warm:fanout`` (the shared tier's pub/sub, ``matrx_utils.cache``)
with the caller's user and organization; every other process runs that warmer under
``system_app_context`` for that person, applying its own throttle. The publishing process skips
its own message. ``fill="shared"`` warmers (they fill the shared cache) never fan out.

Contract: common-docs/systems/architecture/warm-cache/CONTRACT.md.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from collections import Counter
from collections.abc import Awaitable, Callable, Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any, Literal

from matrx_utils.ids import new_hex
from matrx_utils.utils.detached_task import detached_task

from matrx_connect.context.app_context import (
    AppContext,
    clear_app_context,
    set_app_context,
    try_get_app_context,
)

logger = logging.getLogger("matrx_connect.warm")

#: Who a warmed result belongs to — decides the throttle key.
#:   person       — the person's own data (throttle per person per item)
#:   organization — the person's data in their active organization (per person + org per item)
#:   shared       — the same for everyone (one warm per item per process per window)
WarmScope = Literal["person", "organization", "shared"]
#: Where a warmer's result lives: ``shared`` = a cache every server reads (no fan-out);
#: ``process`` = this process's memory only (fanned out to every server).
WarmFill = Literal["shared", "process"]
WarmFn = Callable[[str | None], Awaitable[Any]]

DEFAULT_THROTTLE_S = 60.0
DEFAULT_WARMER_TIMEOUT_S = 15.0
FANOUT_CHANNEL = "mx:warm:fanout"
#: This process on the fan-out channel — its own messages are skipped.
_PROCESS_ID = new_hex()
_THROTTLE_MAX_ENTRIES = 50_000


@dataclass(frozen=True)
class Warmer:
    key: str
    fn: WarmFn
    scope: WarmScope
    needs_id: bool
    timeout_s: float
    fill: WarmFill = "shared"


@dataclass(frozen=True)
class WarmItem:
    key: str
    id: str | None = None

    def as_dict(self) -> dict[str, str]:
        return {"key": self.key, **({"id": self.id} if self.id else {})}


@dataclass
class WarmResult:
    accepted: list[WarmItem] = field(default_factory=list)
    unknown: list[WarmItem] = field(default_factory=list)
    #: Accepted, but warmed for this person within the throttle window — nothing re-run.
    throttled: list[WarmItem] = field(default_factory=list)
    #: Accepted, but past this person's cap on NEW ids per minute — not run, not fanned out.
    limited: list[WarmItem] = field(default_factory=list)
    task: asyncio.Task[None] | None = None


_registry: dict[str, Warmer] = {}
_last_warmed: dict[tuple[str, ...], float] = {}
_background: set[asyncio.Task[Any]] = set()
_stats: Counter[str] = Counter()
_by_reason: Counter[str] = Counter()
_by_key: Counter[str] = Counter()
#: person → monotonic times a NEW id was scheduled for them (abuse bound, see run_warm).
_new_ids: dict[str, list[float]] = {}
_NEW_ID_WINDOW_S = 60.0
#: Used when the host passes no cap. aidream passes its knob (platform.warm).
DEFAULT_MAX_NEW_IDS_PER_MINUTE = 30


def warm_stats() -> dict[str, Any]:
    """Counters (scheduled, throttled, limited, unknown, fanout_*, failures, timeouts) plus
    requested warms per ``reason`` and accepted items per ``key``."""
    return {**dict(_stats), "by_reason": dict(_by_reason), "by_key": dict(_by_key)}


def register_warmer(
    item_key: str,
    fn: WarmFn,
    *,
    scope: WarmScope = "person",
    needs_id: bool = False,
    timeout_s: float = DEFAULT_WARMER_TIMEOUT_S,
    fill: WarmFill = "shared",
) -> None:
    """Register ``fn(item_id)`` as the warmer for ``item_key`` (re-registering replaces it).

    ``fn`` runs under the caller's AppContext (read it with ``get_app_context()``) in a fresh
    task — it opens any database session it needs itself.
    """
    if scope not in ("person", "organization", "shared"):
        raise ValueError(f"unknown warm scope {scope!r}")
    if fill not in ("shared", "process"):
        raise ValueError(f"unknown warm fill {fill!r}")
    _registry[item_key] = Warmer(item_key, fn, scope, needs_id, float(timeout_s), fill)


def unregister_warmer(item_key: str) -> bool:
    return _registry.pop(item_key, None) is not None


def registered_warmers() -> dict[str, Warmer]:
    return dict(_registry)


def reset_warm_throttle() -> None:
    _last_warmed.clear()
    _new_ids.clear()


def _coerce(items: Iterable[WarmItem | Mapping[str, Any]]) -> list[WarmItem]:
    out: list[WarmItem] = []
    for item in items:
        if isinstance(item, WarmItem):
            out.append(item)
            continue
        key = str(item.get("key") or "").strip()
        raw_id = item.get("id")
        out.append(WarmItem(key, str(raw_id).strip() or None if raw_id is not None else None))
    return out


def _throttle_key(warmer: Warmer, item: WarmItem, ctx: Any) -> tuple[str, ...]:
    if warmer.scope == "shared":
        return ("shared", item.key, item.id or "")
    user = str(getattr(ctx, "user_id", "") or "")
    if warmer.scope == "organization":
        org = str(getattr(ctx, "organization_id", "") or "")
        return ("organization", user, org, item.key, item.id or "")
    return ("person", user, item.key, item.id or "")


def _prune(now: float, window: float) -> None:
    if len(_last_warmed) < _THROTTLE_MAX_ENTRIES:
        return
    for k, at in list(_last_warmed.items()):
        if now - at >= window:
            del _last_warmed[k]
    while len(_last_warmed) >= _THROTTLE_MAX_ENTRIES:
        _last_warmed.pop(next(iter(_last_warmed)))


def _due(warmer: Warmer, item: WarmItem, ctx: Any, now: float, window: float) -> bool:
    last = _last_warmed.get(_throttle_key(warmer, item, ctx))
    return last is None or now - last >= window


def _claim(warmer: Warmer, item: WarmItem, ctx: Any, now: float, window: float) -> bool:
    """True when this process should run ``item`` now (and records it); False = throttled."""
    if not _due(warmer, item, ctx, now, window):
        return False
    _last_warmed[_throttle_key(warmer, item, ctx)] = now
    return True


def _new_id_allowed(user_id: str, now: float, cap: int) -> bool:
    times = [t for t in _new_ids.get(user_id, ()) if now - t < _NEW_ID_WINDOW_S]
    if len(times) >= cap:
        _new_ids[user_id] = times
        return False
    times.append(now)
    _new_ids[user_id] = times
    if len(_new_ids) > _THROTTLE_MAX_ENTRIES:
        _new_ids.pop(next(iter(_new_ids)))
    return True


def run_warm(
    items: Iterable[WarmItem | Mapping[str, Any]],
    *,
    ctx: AppContext | None = None,
    reason: str = "unspecified",
    throttle_s: float = DEFAULT_THROTTLE_S,
    max_new_ids_per_minute: int = DEFAULT_MAX_NEW_IDS_PER_MINUTE,
) -> WarmResult:
    """Sort ``items``, schedule the accepted ones, return immediately. Never raises.

    Unknown keys (and items missing a required id) are reported, never an error. Must be called
    inside a running event loop; the warm task carries ``ctx`` (default: the ambient AppContext).

    ABUSE BOUND: an item WITH an id that is due to run counts against the person's
    ``max_new_ids_per_minute``; past it the item is reported in ``limited`` and neither runs
    nor fans out — so a stream of fresh ids cannot slip under the per-item throttle.
    """
    result = WarmResult()
    ctx = ctx if ctx is not None else try_get_app_context()
    user_id = str(getattr(ctx, "user_id", "") or "")
    now = time.monotonic()
    _by_reason[str(reason or "unspecified")[:64]] += 1
    to_run: list[tuple[Warmer, WarmItem]] = []
    seen: set[tuple[str, str | None]] = set()
    for item in _coerce(items):
        warmer = _registry.get(item.key)
        if warmer is None or (warmer.needs_id and not item.id):
            result.unknown.append(item)
            continue
        if (item.key, item.id) in seen:
            continue
        seen.add((item.key, item.id))
        result.accepted.append(item)
        _by_key[item.key] += 1
        if not _due(warmer, item, ctx, now, throttle_s):
            result.throttled.append(item)
            continue
        if item.id and not _new_id_allowed(user_id, now, max_new_ids_per_minute):
            result.limited.append(item)
            continue
        _claim(warmer, item, ctx, now, throttle_s)
        to_run.append((warmer, item))
    _prune(now, throttle_s)
    _stats["unknown"] += len(result.unknown)
    _stats["throttled"] += len(result.throttled)
    _stats["limited"] += len(result.limited)
    _stats["scheduled"] += len(to_run)
    if result.accepted or result.unknown:
        logger.info(
            "[matrx_connect.warm] reason=%s user=%s accepted=%s scheduled=%d throttled=%d limited=%d unknown=%s",
            reason,
            user_id or "-",
            [i.as_dict() for i in result.accepted],
            len(to_run),
            len(result.throttled),
            len(result.limited),
            [i.key for i in result.unknown],
        )
    fan_out = [item for warmer, item in to_run if warmer.fill == "process"]
    if fan_out:
        start_warm_fanout()
    if to_run:
        token = set_app_context(ctx) if ctx is not None and ctx is not try_get_app_context() else None
        try:
            task = detached_task(_run_all(to_run, fan_out, ctx), name="matrx_warm")
        except RuntimeError as exc:  # no running loop — nothing to warm into
            logger.warning("[matrx_connect.warm] not scheduled: %s", exc)
            return result
        finally:
            if token is not None:
                clear_app_context(token)
        _background.add(task)
        task.add_done_callback(_background.discard)
        result.task = task
    return result


async def _run_one(warmer: Warmer, item: WarmItem) -> None:
    started = time.monotonic()
    try:
        await asyncio.wait_for(warmer.fn(item.id), warmer.timeout_s)
    except TimeoutError:
        _stats["timeouts"] += 1
        logger.warning(
            "[matrx_connect.warm] %s timed out after %.1fs (id=%s)", warmer.key, warmer.timeout_s, item.id
        )
    except asyncio.CancelledError:
        raise
    except Exception as exc:  # noqa: BLE001 — a warm failure never reaches anyone
        _stats["failures"] += 1
        logger.warning(
            "[matrx_connect.warm] %s failed (id=%s): %s: %s", warmer.key, item.id, type(exc).__name__, exc
        )
    else:
        logger.debug("[matrx_connect.warm] %s warmed in %.0fms", warmer.key, (time.monotonic() - started) * 1000)


async def _run_all(
    pairs: list[tuple[Warmer, WarmItem]], fan_out: list[WarmItem] | None = None, ctx: Any = None
) -> None:
    if fan_out:
        await _publish_fanout(fan_out, ctx)
    await asyncio.gather(*(_run_one(w, i) for w, i in pairs))


async def stop_warm(timeout_s: float = 2.0) -> None:
    """Shutdown: let in-flight warms finish (bounded), cancel the rest. Call before the host
    closes its DB pool so no warmer is cut off mid-query."""
    tasks = [t for t in _background if not t.done()]
    if not tasks:
        return
    _done, pending = await asyncio.wait(tasks, timeout=timeout_s)
    for task in pending:
        task.cancel()
    if pending:
        await asyncio.gather(*pending, return_exceptions=True)


# ── fan-out ───────────────────────────────────────────────────────────────────


def start_warm_fanout() -> bool:
    """Hear other processes' process-fill warms (idempotent). A host calls it at boot so a
    server that never receives a warm request still warms what its peers were asked for."""
    try:
        from matrx_utils.cache import subscribe_bus_channel
    except ImportError:  # pragma: no cover - matrx-utils without the cache module
        return False
    return subscribe_bus_channel(FANOUT_CHANNEL, _on_fanout)


async def _publish_fanout(items: list[WarmItem], ctx: Any) -> None:
    from matrx_utils.cache import publish_bus

    message = {
        "o": _PROCESS_ID,
        "u": str(getattr(ctx, "user_id", "") or "") or None,
        "g": str(getattr(ctx, "organization_id", "") or "") or None,
        "items": [i.as_dict() for i in items],
    }
    if await publish_bus(FANOUT_CHANNEL, json.dumps(message).encode()):
        _stats["fanout_published"] += len(items)


class _Principal:
    __slots__ = ("organization_id", "user_id")

    def __init__(self, user_id: str | None, organization_id: str | None) -> None:
        self.user_id = user_id
        self.organization_id = organization_id


def _on_fanout(raw: bytes) -> None:
    try:
        message = json.loads(raw)
        origin = message.get("o")
        user_id = message.get("u") or None
        organization_id = message.get("g") or None
        items = _coerce(message.get("items") or [])
    except Exception:  # noqa: BLE001 — a garbled message is ignored
        logger.warning("[matrx_connect.warm] ignored a malformed fan-out message")
        return
    if origin == _PROCESS_ID:
        _stats["fanout_own_skipped"] += len(items)
        return
    _stats["fanout_received"] += len(items)
    principal = _Principal(user_id, organization_id)
    now = time.monotonic()
    pairs: list[tuple[Warmer, WarmItem]] = []
    for item in items:
        warmer = _registry.get(item.key)
        if warmer is None or warmer.fill != "process" or (warmer.needs_id and not item.id):
            continue
        if not _claim(warmer, item, principal, now, DEFAULT_THROTTLE_S):
            _stats["fanout_throttled"] += 1
            continue
        pairs.append((warmer, item))
    if not pairs:
        return
    _stats["fanout_ran"] += len(pairs)
    task = detached_task(_run_fanned(pairs, user_id, organization_id), name="matrx_warm_fanout")
    _background.add(task)
    task.add_done_callback(_background.discard)


async def _run_fanned(pairs: list[tuple[Warmer, WarmItem]], user_id: str | None, organization_id: str | None) -> None:
    if user_id and organization_id:
        from matrx_connect.context.app_context import system_app_context

        async with system_app_context("warm_fanout", user_id=user_id, organization_id=organization_id):
            await asyncio.gather(*(_run_one(w, i) for w, i in pairs))
        return
    # No person on the message: only work that needs nobody (a shared agent definition) runs.
    await asyncio.gather(*(_run_one(w, i) for w, i in pairs if w.scope == "shared"))


__all__ = [
    "DEFAULT_MAX_NEW_IDS_PER_MINUTE",
    "DEFAULT_THROTTLE_S",
    "FANOUT_CHANNEL",
    "WarmFill",
    "WarmFn",
    "WarmItem",
    "WarmResult",
    "WarmScope",
    "Warmer",
    "register_warmer",
    "registered_warmers",
    "reset_warm_throttle",
    "run_warm",
    "start_warm_fanout",
    "stop_warm",
    "warm_stats",
    "unregister_warmer",
]
