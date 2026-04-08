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
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection
    from .event_bus import EventBus

logger = logging.getLogger(__name__)

_MAX_PER_CONVERSATION = 3
_MAX_GLOBAL = 10


class DetachedSubagentManager:
    """Manages detached subagent runs for a single process."""

    def __init__(
        self,
        *,
        db: ThreadSafeConnection,
        event_bus: EventBus | None = None,
    ) -> None:
        self._db = db
        self._event_bus = event_bus
        self._tasks: dict[str, asyncio.Task[None]] = {}
        self._global_count = 0
        self._last_poll_time: str | None = None

    def start(
        self,
        conversation_id: str,
        prompt: str,
        *,
        ai_service: Any,
        tool_registry: Any,
        mcp_manager: Any = None,
        cancel_event: Any = None,
        config: Any = None,
        limiter: Any = None,
        db: Any = None,
    ) -> dict[str, Any]:
        """Launch a detached subagent and return immediately.

        Returns ``{run_id, status, prompt}``.
        Raises ``ValueError`` if concurrency caps are exceeded.
        """
        from . import storage

        db = db or self._db

        # Enforce caps
        active = storage.count_active_agent_runs(db, conversation_id)
        if active >= _MAX_PER_CONVERSATION:
            raise ValueError(f"Too many detached agents for this conversation ({active}/{_MAX_PER_CONVERSATION})")
        if self._global_count >= _MAX_GLOBAL:
            raise ValueError(f"Too many detached agents globally ({self._global_count}/{_MAX_GLOBAL})")

        # Create durable run record — full prompt stored in metadata for retry
        run = storage.create_agent_run(
            db,
            conversation_id=conversation_id,
            kind="detached_subagent",
            title=prompt[:120],
            metadata={"prompt": prompt},
        )
        run_id = run["id"]
        storage.update_agent_run(db, run_id, status="running", started_at=_now())

        # Spawn collector coroutine
        async def _collect() -> None:
            from ..tools.subagent import _run_subagent

            start_ts = time.monotonic()
            try:
                result = await _run_subagent(
                    prompt=prompt,
                    model=None,
                    _ai_service=ai_service,
                    _tool_registry=tool_registry,
                    _mcp_manager=mcp_manager,
                    _cancel_event=cancel_event or asyncio.Event(),
                    _depth=0,
                    _event_sink=None,
                    _agent_id=f"detached-{run_id[:8]}",
                    _limiter=limiter,
                    _confirm_callback=None,
                    _config=config,
                )

                elapsed = time.monotonic() - start_ts
                status = "failed" if result.get("error") else "completed"
                result_with_elapsed = {**result, "elapsed_seconds": round(elapsed, 2)}
                from .task_result import TaskResult

                task_result = TaskResult.from_subagent_result(result_with_elapsed, run_id)
                metadata = {
                    "output": result.get("output", ""),
                    "tool_calls_made": result.get("tool_calls_made", []),
                    "model_used": result.get("model_used"),
                    "truncated": result.get("truncated", False),
                    "error": result.get("error"),
                    "elapsed_seconds": round(elapsed, 2),
                    "task_result": task_result.to_dict(),
                }

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
                    await self._event_bus.publish(
                        f"conversation:{conversation_id}",
                        {
                            "type": "agent_run_completed",
                            "data": {
                                "run_id": run_id,
                                "status": status,
                                "summary": (result.get("output") or "")[:200],
                                "duration_seconds": round(elapsed, 2),
                                "tool_calls_count": len(result.get("tool_calls_made", [])),
                            },
                        },
                    )

            except asyncio.CancelledError:
                storage.update_agent_run(db, run_id, status="cancelled", completed_at=_now())
            except Exception:
                logger.warning("Detached agent %s collector failed", run_id[:8], exc_info=True)
                try:
                    storage.update_agent_run(db, run_id, status="failed", completed_at=_now())
                except Exception:
                    pass
            finally:
                self._tasks.pop(run_id, None)
                self._global_count = max(0, self._global_count - 1)

        loop = asyncio.get_running_loop()
        collector = loop.create_task(_collect())
        self._tasks[run_id] = collector
        self._global_count += 1

        # Publish start event
        if self._event_bus:
            _start_evt = loop.create_task(
                self._event_bus.publish(
                    f"conversation:{conversation_id}",
                    {
                        "type": "agent_run_started",
                        "data": {
                            "run_id": run_id,
                            "prompt": prompt[:80],
                        },
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
            collector.cancel()

        storage.update_agent_run(db, run_id, status="cancelled", completed_at=_now())
        return True

    def retry(self, run_id: str, *, db: Any = None, **start_kwargs: Any) -> dict[str, Any]:
        """Retry a failed/cancelled run by creating a new run with linkage.

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
        new_run = storage.create_agent_run(
            db,
            conversation_id=original["conversation_id"],
            kind="detached_subagent",
            title=original.get("title", ""),
            parent_run_id=run_id,
            metadata={"prompt": full_prompt},
        )
        new_run_id = new_run["id"]
        storage.update_agent_run(db, new_run_id, status="running", started_at=_now())

        # Re-launch with the full original prompt (stored in metadata, not truncated title)
        prompt = full_prompt

        async def _collect() -> None:
            from ..tools.subagent import _run_subagent

            start_ts = time.monotonic()
            try:
                result = await _run_subagent(
                    prompt=prompt,
                    model=None,
                    _ai_service=start_kwargs.get("ai_service"),
                    _tool_registry=start_kwargs.get("tool_registry"),
                    _mcp_manager=start_kwargs.get("mcp_manager"),
                    _cancel_event=start_kwargs.get("cancel_event") or asyncio.Event(),
                    _depth=0,
                    _event_sink=None,
                    _agent_id=f"detached-{new_run_id[:8]}",
                    _limiter=start_kwargs.get("limiter"),
                    _confirm_callback=None,
                    _config=start_kwargs.get("config"),
                )

                elapsed = time.monotonic() - start_ts
                status = "failed" if result.get("error") else "completed"
                result_with_elapsed = {**result, "elapsed_seconds": round(elapsed, 2)}
                from .task_result import TaskResult as _TaskResult

                task_result = _TaskResult.from_subagent_result(result_with_elapsed, new_run_id)
                metadata = {
                    "output": result.get("output", ""),
                    "tool_calls_made": result.get("tool_calls_made", []),
                    "model_used": result.get("model_used"),
                    "truncated": result.get("truncated", False),
                    "error": result.get("error"),
                    "elapsed_seconds": round(elapsed, 2),
                    "task_result": task_result.to_dict(),
                }

                from . import storage as _st

                _st.update_agent_run(
                    db,
                    new_run_id,
                    status=status,
                    completed_at=_now(),
                    duration_ms=int(elapsed * 1000),
                    metadata_json=json.dumps(metadata),
                )

                if self._event_bus:
                    await self._event_bus.publish(
                        f"conversation:{original['conversation_id']}",
                        {
                            "type": "agent_run_completed",
                            "data": {
                                "run_id": new_run_id,
                                "status": status,
                                "summary": (result.get("output") or "")[:200],
                                "duration_seconds": round(elapsed, 2),
                                "tool_calls_count": len(result.get("tool_calls_made", [])),
                            },
                        },
                    )

            except asyncio.CancelledError:
                from . import storage as _st

                _st.update_agent_run(db, new_run_id, status="cancelled", completed_at=_now())
            except Exception:
                logger.warning("Detached agent retry %s failed", new_run_id[:8], exc_info=True)
                try:
                    from . import storage as _st

                    _st.update_agent_run(db, new_run_id, status="failed", completed_at=_now())
                except Exception:
                    pass
            finally:
                self._tasks.pop(new_run_id, None)
                self._global_count = max(0, self._global_count - 1)

        loop = asyncio.get_running_loop()
        collector = loop.create_task(_collect())
        self._tasks[new_run_id] = collector
        self._global_count += 1

        return {"run_id": new_run_id, "status": "running", "parent_run_id": run_id}

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
