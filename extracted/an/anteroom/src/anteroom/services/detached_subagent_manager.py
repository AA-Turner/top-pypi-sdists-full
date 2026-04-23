"""Detached subagent manager — tracks async AI work units (#1314).

Manages in-process subagent tasks that run independently of the parent
turn.  Persists state to the ``agent_runs`` table and publishes lifecycle
events via the event bus.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import TYPE_CHECKING, Any, cast

from .lineage import emit_subagent_lifecycle

if TYPE_CHECKING:
    from ..config import SubagentConfig
    from ..db import ThreadSafeConnection
    from .audit import AuditWriter
    from .event_bus import EventBus

logger = logging.getLogger(__name__)


class DetachedSubagentManager:
    """Manages detached subagent runs for a single process."""

    # TODO(#1464): extract shared collector helper — start()._collect and
    # retry()._collect are near-duplicates that diverge only in run_id,
    # prompt source, and parent_run_id threading.

    def __init__(
        self,
        *,
        db: ThreadSafeConnection,
        event_bus: EventBus | None = None,
        config: SubagentConfig | None = None,
        audit_writer: AuditWriter | None = None,
    ) -> None:
        from ..config import SubagentConfig as _SubagentConfig

        self._db = db
        self._event_bus = event_bus
        self._config = config if config is not None else _SubagentConfig()
        self._audit_writer = audit_writer
        self._tasks: dict[str, asyncio.Task[None]] = {}
        self._global_count = 0
        self._last_poll_time: str | None = None
        # Tracks operator-initiated cancellations so the collector's
        # CancelledError branch can skip duplicate DB writes + audit emits.
        self._operator_cancelled: set[str] = set()

    def start(
        self,
        conversation_id: str,
        prompt: str,
        *,
        model: str | None = None,
        description: str | None = None,
        ai_service: Any,
        tool_registry: Any,
        mcp_manager: Any = None,
        cancel_event: Any = None,
        config: Any = None,
        limiter: Any = None,
        db: Any = None,
        hooks_config: Any = None,
        audit_writer: Any = None,
        parent_conversation_id: str = "",
        parent_tool_call_id: str = "",
    ) -> dict[str, Any]:
        """Launch a detached subagent and return immediately.

        ``hooks_config`` is the already-resolved hook config snapshot captured
        at launch time (#1493).  Later config changes do not affect this
        in-flight run — the snapshot is passed directly to ``_run_subagent``
        without reloading from disk or the DB.

        ``parent_conversation_id`` and ``parent_tool_call_id`` are recorded in
        hook audit events for correlation across the parent/child boundary.

        Returns ``{run_id, status, prompt}``.
        Raises ``ValueError`` if concurrency caps are exceeded.
        """
        from . import storage

        db = db or self._db

        # Enforce caps — now sourced from config so operators can tune via SubagentConfig.
        active = storage.count_active_agent_runs(db, conversation_id)
        max_per_conv = self._config.max_concurrent
        max_global = self._config.max_total
        if active >= max_per_conv:
            raise ValueError(f"Too many detached agents for this conversation ({active}/{max_per_conv})")
        if self._global_count >= max_global:
            raise ValueError(f"Too many detached agents globally ({self._global_count}/{max_global})")

        # Build initial metadata — full prompt and model stored for retry.
        # description is stored here when provided, enabling stable labels in run lists.
        initial_metadata: dict[str, Any] = {"prompt": prompt, "model": model}
        if description is not None:
            initial_metadata["description"] = description

        # Create durable run record — full prompt and requested model stored in metadata for retry.
        run = storage.create_agent_run(
            db,
            conversation_id=conversation_id,
            kind="detached_subagent",
            title=prompt[:120],
            metadata=initial_metadata,
        )
        run_id = run["id"]
        storage.update_agent_run(db, run_id, status="running", started_at=_now())

        emit_subagent_lifecycle(
            self._audit_writer,
            "spawned",
            run_id=run_id,
            conversation_id=conversation_id,
            model=model or "",
        )

        # Capture correlation metadata for hook audit entries.
        _parent_conv_id = parent_conversation_id or conversation_id
        _parent_tc_id = parent_tool_call_id

        # Spawn collector coroutine
        async def _collect() -> None:
            from ..tools.subagent import _run_subagent

            start_ts = time.monotonic()
            try:
                result = await _run_subagent(
                    prompt=prompt,
                    model=model,
                    _ai_service=ai_service,
                    _tool_registry=tool_registry,
                    _mcp_manager=mcp_manager,
                    _cancel_event=cancel_event or asyncio.Event(),
                    _depth=0,
                    _event_sink=None,
                    _agent_id=f"detached-{run_id[:8]}",
                    _parent_tool_call_id=_parent_tc_id,
                    _limiter=limiter,
                    _confirm_callback=None,
                    _config=config,
                    # Snapshot hook config (#1493): use the already-resolved config
                    # captured at launch; do not reload from disk/DB.
                    _hooks_config=hooks_config,
                    _audit_writer=audit_writer,
                    _parent_conversation_id=_parent_conv_id,
                    _detached_run_id=run_id,
                )

                elapsed = time.monotonic() - start_ts
                status = "failed" if result.get("error") else "completed"
                result_with_elapsed = {**result, "elapsed_seconds": round(elapsed, 2)}
                from .task_result import TaskResult

                task_result = TaskResult.from_subagent_result(result_with_elapsed, run_id)
                metadata: dict[str, Any] = {
                    "output": result.get("output", ""),
                    "tool_calls_made": result.get("tool_calls_made", []),
                    "model": model,
                    "model_used": result.get("model_used"),
                    "truncated": result.get("truncated", False),
                    "error": result.get("error"),
                    "elapsed_seconds": round(elapsed, 2),
                    "task_result": task_result.to_dict(),
                }
                if description is not None:
                    metadata["description"] = description

                storage.update_agent_run(
                    db,
                    run_id,
                    status=status,
                    completed_at=_now(),
                    duration_ms=int(elapsed * 1000),
                    metadata_json=json.dumps(metadata),
                )

                # Publish completion event
                if self._event_bus:
                    completion_payload: dict[str, Any] = {
                        "run_id": run_id,
                        "status": status,
                        "summary": (result.get("output") or "")[:200],
                        "duration_seconds": round(elapsed, 2),
                        "tool_calls_count": len(result.get("tool_calls_made", [])),
                    }
                    if description is not None:
                        completion_payload["description"] = description
                    await self._event_bus.publish(
                        f"conversation:{conversation_id}",
                        {"type": "agent_run_completed", "data": completion_payload},
                    )

                audit_event = "completed" if status == "completed" else "failed"
                emit_subagent_lifecycle(
                    self._audit_writer,
                    audit_event,
                    run_id=run_id,
                    conversation_id=conversation_id,
                    model=model or "",
                    details={
                        "duration_ms": int(elapsed * 1000),
                        "tool_calls": len(result.get("tool_calls_made", [])),
                    },
                )

            except asyncio.CancelledError:
                if run_id not in self._operator_cancelled:
                    # Not an operator cancel — record it ourselves.
                    storage.update_agent_run(db, run_id, status="cancelled", completed_at=_now())
                    emit_subagent_lifecycle(
                        self._audit_writer,
                        "cancelled",
                        run_id=run_id,
                        conversation_id=conversation_id,
                        model=model or "",
                    )
                # else: operator already wrote DB + emitted; don't duplicate.
            except Exception:
                logger.warning("Detached agent %s collector failed", run_id[:8], exc_info=True)
                try:
                    storage.update_agent_run(db, run_id, status="failed", completed_at=_now())
                except Exception:
                    pass
                emit_subagent_lifecycle(
                    self._audit_writer,
                    "failed",
                    run_id=run_id,
                    conversation_id=conversation_id,
                    model=model or "",
                    details={"error": "collector_exception"},
                )
            finally:
                self._tasks.pop(run_id, None)
                self._global_count = max(0, self._global_count - 1)
                self._operator_cancelled.discard(run_id)

        loop = asyncio.get_running_loop()
        collector = loop.create_task(_collect())
        self._tasks[run_id] = collector
        self._global_count += 1

        # Publish start event
        if self._event_bus:
            start_event_data: dict[str, Any] = {
                "run_id": run_id,
                "prompt": prompt[:80],
            }
            if description is not None:
                start_event_data["description"] = description
            _start_evt = loop.create_task(
                self._event_bus.publish(
                    f"conversation:{conversation_id}",
                    {
                        "type": "agent_run_started",
                        "data": start_event_data,
                    },
                )
            )
            _start_evt.add_done_callback(lambda t: t.exception() if not t.cancelled() else None)

        return {
            "run_id": run_id,
            "status": "running",
            "prompt": prompt[:80],
        }

    def get_run(self, run_id: str, *, db: Any = None) -> dict[str, Any] | None:
        """Read a detached run record."""
        from . import storage

        db = db or self._db
        run = storage.get_agent_run(db, run_id)
        if run is None or run.get("kind") != "detached_subagent":
            return None
        return run

    def list_runs(self, conversation_id: str, *, status: str | None = None, db: Any = None) -> list[dict[str, Any]]:
        """List detached runs for a conversation."""
        from . import storage

        db = db or self._db
        return storage.list_agent_runs(db, conversation_id, kind="detached_subagent", status=status)

    def poll_completed(self) -> list[dict[str, Any]]:
        """Return runs that completed since the last poll (CLI poller)."""
        from datetime import datetime, timezone

        from . import storage

        if self._last_poll_time is None:
            self._last_poll_time = datetime.now(timezone.utc).isoformat()
            return []

        rows = self._db.execute_fetchall(
            "SELECT * FROM agent_runs WHERE kind = 'detached_subagent' AND completed_at > ? ORDER BY completed_at",
            (self._last_poll_time,),
        )
        self._last_poll_time = datetime.now(timezone.utc).isoformat()
        return [storage._deserialize_agent_run(dict(r)) for r in rows]

    def cancel(self, run_id: str, *, db: Any = None) -> bool:
        """Cancel a running detached agent."""
        from . import storage

        db = db or self._db
        run = self.get_run(run_id, db=db)
        if not run or run["status"] != "running":
            return False

        collector = self._tasks.get(run_id)
        if collector and not collector.done():
            # Mark as operator-initiated BEFORE cancelling so the collector's
            # CancelledError branch can suppress its own DB write + audit emit.
            self._operator_cancelled.add(run_id)
            collector.cancel()

        storage.update_agent_run(db, run_id, status="cancelled", completed_at=_now())

        meta = run.get("metadata") or {}
        emit_subagent_lifecycle(
            self._audit_writer,
            "cancelled",
            run_id=run_id,
            conversation_id=run.get("conversation_id", ""),
            model=meta.get("model") or "",
        )
        return True

    def retry(self, run_id: str, *, db: Any = None, **start_kwargs: Any) -> dict[str, Any]:
        """Retry a failed/cancelled run by creating a new run with linkage.

        ``hooks_config`` and ``audit_writer`` in ``start_kwargs`` are forwarded
        to ``_run_subagent`` so the retry run uses the same hook semantics as
        the original.  Retries are correlated via ``parent_run_id`` in the
        audit trail (#1493).

        Returns the new run dict. The original run is preserved for audit.
        Raises ``ValueError`` if the original run is not in a terminal state.
        """
        db = db or self._db
        original = self.get_run(run_id, db=db)
        if original is None:
            raise ValueError(f"Detached run not found: {run_id}")
        if original["status"] not in ("failed", "cancelled"):
            raise ValueError(f"Can only retry failed/cancelled runs (current: {original['status']})")

        # Create new run with parent linkage
        from . import storage

        original_meta = original.get("metadata") or {}
        full_prompt = original_meta.get("prompt") or original.get("title", "")
        # Retries preserve the original model unless the caller explicitly
        # overrides. Using ``"model" in start_kwargs`` (not a truthiness check)
        # so a caller passing ``model=None`` can deliberately clear the override.
        if "model" in start_kwargs:
            model = start_kwargs.get("model")
        else:
            model = original_meta.get("model")
        # Carry forward description from original run (if present)
        retry_description: str | None = original_meta.get("description") or None
        retry_metadata: dict[str, Any] = {"prompt": full_prompt, "model": model}
        if retry_description is not None:
            retry_metadata["description"] = retry_description
        new_run = storage.create_agent_run(
            db,
            conversation_id=original["conversation_id"],
            kind="detached_subagent",
            title=original.get("title", ""),
            parent_run_id=run_id,
            metadata=retry_metadata,
        )
        new_run_id = new_run["id"]
        storage.update_agent_run(db, new_run_id, status="running", started_at=_now())

        emit_subagent_lifecycle(
            self._audit_writer,
            "spawned",
            run_id=new_run_id,
            conversation_id=original["conversation_id"],
            model=model or "",
            parent_run_id=run_id,
        )

        # Re-launch with the full original prompt (stored in metadata, not truncated title)
        prompt = full_prompt
        _retry_hooks_config = start_kwargs.get("hooks_config")
        _retry_audit_writer = start_kwargs.get("audit_writer")

        async def _collect() -> None:
            from ..tools.subagent import _run_subagent

            start_ts = time.monotonic()
            try:
                ai_service = start_kwargs.get("ai_service")
                limiter = start_kwargs.get("limiter")
                if ai_service is None:
                    raise ValueError("Retry requires ai_service start context")
                result = await _run_subagent(
                    prompt=prompt,
                    model=model,
                    _ai_service=ai_service,
                    _tool_registry=start_kwargs.get("tool_registry"),
                    _mcp_manager=start_kwargs.get("mcp_manager"),
                    _cancel_event=start_kwargs.get("cancel_event") or asyncio.Event(),
                    _depth=0,
                    _event_sink=None,
                    _agent_id=f"detached-{new_run_id[:8]}",
                    _parent_tool_call_id="",
                    _limiter=cast(Any, limiter),
                    _confirm_callback=None,
                    _config=start_kwargs.get("config"),
                    # Forward hook config snapshot and correlation context (#1493).
                    # Retries are a new run correlated via parent_run_id; they do
                    # not pretend to be the original run.
                    _hooks_config=_retry_hooks_config,
                    _audit_writer=_retry_audit_writer,
                    _parent_conversation_id=original["conversation_id"],
                    _detached_run_id=new_run_id,
                )

                elapsed = time.monotonic() - start_ts
                status = "failed" if result.get("error") else "completed"
                result_with_elapsed = {**result, "elapsed_seconds": round(elapsed, 2)}
                from .task_result import TaskResult as _TaskResult

                task_result = _TaskResult.from_subagent_result(result_with_elapsed, new_run_id)
                retry_completion_metadata: dict[str, Any] = {
                    "output": result.get("output", ""),
                    "tool_calls_made": result.get("tool_calls_made", []),
                    "model": model,
                    "model_used": result.get("model_used"),
                    "truncated": result.get("truncated", False),
                    "error": result.get("error"),
                    "elapsed_seconds": round(elapsed, 2),
                    "task_result": task_result.to_dict(),
                }
                if retry_description is not None:
                    retry_completion_metadata["description"] = retry_description

                from . import storage as _st

                _st.update_agent_run(
                    db,
                    new_run_id,
                    status=status,
                    completed_at=_now(),
                    duration_ms=int(elapsed * 1000),
                    metadata_json=json.dumps(retry_completion_metadata),
                )

                if self._event_bus:
                    retry_completion_event: dict[str, Any] = {
                        "run_id": new_run_id,
                        "status": status,
                        "summary": (result.get("output") or "")[:200],
                        "duration_seconds": round(elapsed, 2),
                        "tool_calls_count": len(result.get("tool_calls_made", [])),
                    }
                    if retry_description is not None:
                        retry_completion_event["description"] = retry_description
                    await self._event_bus.publish(
                        f"conversation:{original['conversation_id']}",
                        {"type": "agent_run_completed", "data": retry_completion_event},
                    )

                audit_event = "completed" if status == "completed" else "failed"
                emit_subagent_lifecycle(
                    self._audit_writer,
                    audit_event,
                    run_id=new_run_id,
                    conversation_id=original["conversation_id"],
                    model=model or "",
                    parent_run_id=run_id,
                    details={
                        "duration_ms": int(elapsed * 1000),
                        "tool_calls": len(result.get("tool_calls_made", [])),
                    },
                )

            except asyncio.CancelledError:
                if new_run_id not in self._operator_cancelled:
                    # Not an operator cancel — record it ourselves.
                    from . import storage as _st

                    _st.update_agent_run(db, new_run_id, status="cancelled", completed_at=_now())
                    emit_subagent_lifecycle(
                        self._audit_writer,
                        "cancelled",
                        run_id=new_run_id,
                        conversation_id=original["conversation_id"],
                        model=model or "",
                        parent_run_id=run_id,
                    )
                # else: operator already wrote DB + emitted; don't duplicate.
            except Exception:
                logger.warning("Detached agent retry %s failed", new_run_id[:8], exc_info=True)
                try:
                    from . import storage as _st

                    _st.update_agent_run(db, new_run_id, status="failed", completed_at=_now())
                except Exception:
                    pass
                emit_subagent_lifecycle(
                    self._audit_writer,
                    "failed",
                    run_id=new_run_id,
                    conversation_id=original["conversation_id"],
                    model=model or "",
                    parent_run_id=run_id,
                    details={"error": "collector_exception"},
                )
            finally:
                self._tasks.pop(new_run_id, None)
                self._global_count = max(0, self._global_count - 1)
                self._operator_cancelled.discard(new_run_id)

        loop = asyncio.get_running_loop()
        collector = loop.create_task(_collect())
        self._tasks[new_run_id] = collector
        self._global_count += 1

        return {"run_id": new_run_id, "status": "running", "parent_run_id": run_id, "model": model}

    async def shutdown(self) -> None:
        """Cancel all in-flight collector tasks."""
        for task in list(self._tasks.values()):
            if not task.done():
                task.cancel()
        for task in list(self._tasks.values()):
            try:
                await task
            except (asyncio.CancelledError, Exception):
                pass
        self._tasks.clear()


def _now() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()
