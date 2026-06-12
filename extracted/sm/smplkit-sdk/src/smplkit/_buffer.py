"""Registration buffers backing the SDK's batched-discovery sub-clients.

Four buffer types, each owned by the sub-client that drains it:

- :class:`_ContextRegistrationBuffer`  →  ``client.platform.contexts._buffer``
- :class:`_FlagRegistrationBuffer`     →  ``client.flags._buffer``
- :class:`_ConfigRegistrationBuffer`   →  ``client.config._buffer``
- :class:`_LoggerRegistrationBuffer`   →  ``client.logging.loggers._buffer``

There is exactly one buffer + one bulk-flush implementation per resource.
"""

from __future__ import annotations

import threading
from collections import OrderedDict
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover
    from smplkit.flags.types import Context

# When the deduplication LRU exceeds this size, the oldest entry is
# evicted. The next observation of an evicted entry will re-flush.
_CONTEXT_REGISTRATION_LRU_SIZE = 10_000

# Pending-queue size that triggers an immediate background flush from
# inside ``register()``.  The periodic timer on ``SmplClient`` covers
# the tail case for low-traffic services.
_CONTEXT_BATCH_FLUSH_SIZE = 100
_FLAG_BATCH_FLUSH_SIZE = 50
_LOGGER_BATCH_FLUSH_SIZE = 50
_CONFIG_BATCH_FLUSH_SIZE = 50


class _ContextRegistrationBuffer:
    """Thread-safe batch buffer for context registration."""

    def __init__(self) -> None:
        self._seen: OrderedDict[tuple[str, str], dict[str, Any]] = OrderedDict()
        self._pending: list[dict[str, Any]] = []
        self._lock = threading.Lock()

    def observe(self, contexts: list[Context]) -> None:
        """Queue any unseen contexts."""
        with self._lock:
            for ctx in contexts:
                cache_key = (ctx.type, ctx.key)
                if cache_key not in self._seen:
                    if len(self._seen) >= _CONTEXT_REGISTRATION_LRU_SIZE:
                        self._seen.popitem(last=False)
                    self._seen[cache_key] = ctx.attributes
                    self._pending.append(
                        {
                            "type": ctx.type,
                            "key": ctx.key,
                            "attributes": dict(ctx.attributes),
                        }
                    )

    def drain(self) -> list[dict[str, Any]]:
        """Return and clear the current pending batch."""
        with self._lock:
            batch = list(self._pending)
            self._pending.clear()
            return batch

    @property
    def pending_count(self) -> int:
        with self._lock:
            return len(self._pending)


class _FlagRegistrationBuffer:
    """Thread-safe batch buffer for flag declarations.

    Use ``peek()`` + ``commit(ids)`` for the send path so a failed POST
    leaves declarations queued for the next attempt; the legacy
    ``drain()`` is unconditional and used only by tests.
    """

    def __init__(self) -> None:
        self._seen: OrderedDict[str, bool] = OrderedDict()
        self._pending: list[dict[str, Any]] = []
        self._lock = threading.Lock()

    def add(
        self,
        flag_id: str,
        flag_type: str,
        default: Any,
        service: str | None,
        environment: str | None,
    ) -> None:
        """Queue a flag declaration for registration if not already seen."""
        with self._lock:
            if flag_id not in self._seen:
                self._seen[flag_id] = True
                item: dict[str, Any] = {
                    "id": flag_id,
                    "type": flag_type,
                    "default": default,
                }
                if service is not None:
                    item["service"] = service
                if environment is not None:
                    item["environment"] = environment
                self._pending.append(item)

    def peek(self) -> list[dict[str, Any]]:
        """Return a snapshot of the pending batch without removing items."""
        with self._lock:
            return list(self._pending)

    def commit(self, ids: list[str]) -> None:
        """Remove items by id from the pending batch (call after a successful send)."""
        if not ids:
            return
        committed = set(ids)
        with self._lock:
            self._pending = [item for item in self._pending if item["id"] not in committed]

    def drain(self) -> list[dict[str, Any]]:
        """Return and clear the pending batch."""
        with self._lock:
            batch = self._pending
            self._pending = []
            return batch

    @property
    def pending_count(self) -> int:
        with self._lock:
            return len(self._pending)


class _ConfigRegistrationBuffer:
    """Thread-safe batch buffer for config declarations.

    Configs differ from flags/loggers because each entry carries a
    nested ``items`` dict that grows incrementally as the customer's
    code touches more typed getters on a declared handle. The buffer
    therefore stores per-config metadata permanently (so post-flush
    deltas can be re-attributed to the right service/environment) and
    dedups items per ``(config_id, item_key)`` so we never re-send an
    item that the server has already accepted.

    Call sites:

    - :meth:`declare` once per ``client.config.bind(id, ...)``.
    - :meth:`add_item` for every Pydantic-introspected leaf field, or
      anything else the runtime client observes. Repeated calls with the
      same ``(config_id, item_key)`` after a successful flush are no-ops.
    - :meth:`drain` returns the pending payload list, clears the
      pending buffer, and records what was sent.

    The buffer never drops metadata — only ``_pending`` is cleared on
    flush. If the customer's code declares new items via typed getters
    after a flush, a fresh pending entry is created using the stored
    metadata so the server can route the delta to the right source row.
    """

    def __init__(self) -> None:
        # Pending payloads keyed by config id — drained on flush.
        self._pending: OrderedDict[str, dict[str, Any]] = OrderedDict()
        # Per-config metadata (service/environment/parent/name/description).
        # Kept across flushes so post-flush deltas carry the right attribution.
        self._meta: OrderedDict[str, dict[str, Any]] = OrderedDict()
        # Permanent dedup of items already sent at least once.
        self._sent_items: set[tuple[str, str]] = set()
        self._lock = threading.Lock()

    def declare(
        self,
        config_id: str,
        *,
        service: str | None,
        environment: str | None,
        parent: str | None = None,
        name: str | None = None,
        description: str | None = None,
    ) -> None:
        """Register a configuration. Idempotent within a process."""
        with self._lock:
            if config_id in self._meta:
                # Already known — keep the original metadata.
                return
            self._meta[config_id] = {
                "service": service,
                "environment": environment,
                "parent": parent,
                "name": name,
                "description": description,
            }
            self._pending[config_id] = self._build_entry(config_id, items={})

    def add_item(
        self,
        config_id: str,
        item_key: str,
        item_type: str,
        default: Any,
        description: str | None = None,
    ) -> None:
        """Queue an item declaration if not already sent.

        Must be preceded by :meth:`declare` for the same ``config_id``;
        otherwise the call is dropped (no implicit declaration).
        """
        with self._lock:
            if config_id not in self._meta:
                return
            if (config_id, item_key) in self._sent_items:
                return
            entry = self._pending.get(config_id)
            if entry is None:
                # Post-flush delta — rebuild a pending entry from stored metadata.
                entry = self._build_entry(config_id, items={})
                self._pending[config_id] = entry
            if item_key in entry["items"]:
                return
            item_def: dict[str, Any] = {"value": default, "type": item_type}
            if description is not None:
                item_def["description"] = description
            entry["items"][item_key] = item_def

    def _build_entry(self, config_id: str, items: dict[str, Any]) -> dict[str, Any]:
        meta = self._meta[config_id]
        entry: dict[str, Any] = {"id": config_id, "items": items}
        for key in ("service", "environment", "parent", "name", "description"):
            value = meta.get(key)
            if value is not None:
                entry[key] = value
        return entry

    def drain(self) -> list[dict[str, Any]]:
        """Return and clear the pending batch; record sent items."""
        with self._lock:
            entries = list(self._pending.values())
            for entry in entries:
                cid = entry["id"]
                for item_key in entry["items"]:
                    self._sent_items.add((cid, item_key))
            self._pending.clear()
            return entries

    @property
    def pending_count(self) -> int:
        with self._lock:
            return sum(1 for _ in self._pending)


class _LoggerRegistrationBuffer:
    """Thread-safe batch buffer for logger discovery."""

    def __init__(self) -> None:
        self._seen: OrderedDict[str, str] = OrderedDict()  # normalized_id → resolved_level
        self._pending: list[dict[str, Any]] = []
        self._lock = threading.Lock()

    def add(
        self,
        normalized_id: str,
        smpl_level: str | None,
        smpl_resolved_level: str,
        service: str | None,
        environment: str | None,
    ) -> None:
        """Queue a discovered logger if not already seen."""
        with self._lock:
            if normalized_id not in self._seen:
                self._seen[normalized_id] = smpl_resolved_level
                item: dict[str, Any] = {"id": normalized_id, "resolved_level": smpl_resolved_level}
                if smpl_level is not None:
                    item["level"] = smpl_level
                if service is not None:
                    item["service"] = service
                if environment is not None:
                    item["environment"] = environment
                self._pending.append(item)

    def drain(self) -> list[dict[str, Any]]:
        """Return and clear the pending batch."""
        with self._lock:
            batch = self._pending
            self._pending = []
            return batch

    @property
    def pending_count(self) -> int:
        with self._lock:
            return len(self._pending)
