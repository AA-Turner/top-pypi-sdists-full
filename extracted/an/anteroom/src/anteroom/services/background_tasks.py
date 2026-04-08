"""Background task manager — tracks detached shell commands (#1311).

Manages in-process subprocess handles and persists task state to SQLite.
Completion events are published via the event bus so both CLI and web UI
can surface notifications.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection
    from .event_bus import EventBus

logger = logging.getLogger(__name__)

_MAX_PREVIEW_BYTES = 2048
_MAX_PER_CONVERSATION = 5
_MAX_GLOBAL = 20


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _compute_duration(started_at: str | None, completed_at: str | None) -> float:
    """Compute elapsed seconds between two ISO-8601 timestamps.

    Returns 0.0 if either timestamp is missing or unparseable.
    """
    if not started_at or not completed_at:
        return 0.0
    try:
        t0 = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
        t1 = datetime.fromisoformat(completed_at.replace("Z", "+00:00"))
        return round((t1 - t0).total_seconds(), 2)
    except Exception:
        return 0.0


class BackgroundTaskManager:
    """Manages background shell tasks for a single process."""

    def __init__(
        self,
        *,
        db: ThreadSafeConnection,
        data_dir: Path,
        event_bus: EventBus | None = None,
    ) -> None:
        self._db = db
        self._data_dir = data_dir
        self._event_bus = event_bus
        self._tasks: dict[str, asyncio.Task[None]] = {}
        self._global_count = 0
        self._last_poll_time: str | None = None

    def start_task(
        self,
        conversation_id: str,
        command: str,
        *,
        timeout: float = 600,
        env: dict[str, str] | None = None,
        cwd: str | None = None,
        db: Any = None,
        sandbox_config: Any = None,
    ) -> dict[str, Any]:
        """Launch a background subprocess and return immediately.

        Returns a task dict with ``id``, ``status``, ``pid``.
        Raises ``ValueError`` if concurrency caps are exceeded.

        *db* overrides the default DB connection (used by the web path
        where the request may target a non-default database).
        """
        db = db or self._db

        # Enforce caps
        conv_count = self._count_running(conversation_id, db=db)
        if conv_count >= _MAX_PER_CONVERSATION:
            raise ValueError(f"Too many background tasks for this conversation ({conv_count}/{_MAX_PER_CONVERSATION})")
        if self._global_count >= _MAX_GLOBAL:
            raise ValueError(f"Too many background tasks globally ({self._global_count}/{_MAX_GLOBAL})")

        task_id = _uuid()
        now = _now()

        # Build subprocess environment (match foreground bash path)
        import os

        subprocess_env = {**os.environ, **env} if env else None

        # Insert DB record
        db.execute(
            "INSERT INTO background_tasks (id, conversation_id, command, status, started_at) "
            "VALUES (?, ?, ?, 'running', ?)",
            (task_id, conversation_id, command, now),
        )
        db.commit()

        # Determine if Win32 OS sandbox should be applied (match foreground bash)
        import sys

        _use_os_sandbox = (
            sys.platform == "win32"
            and sandbox_config is not None
            and hasattr(sandbox_config, "sandbox")
            and sandbox_config.sandbox.is_enabled
        )

        # Spawn collector coroutine
        async def _collect() -> None:
            from .task_result import TaskResult

            job_handle: int | None = None
            start_ts = time.monotonic()
            try:
                # Match foreground bash: stdin=DEVNULL, cwd from working dir
                proc = await asyncio.create_subprocess_shell(
                    command,
                    stdin=asyncio.subprocess.DEVNULL,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=cwd,
                    env=subprocess_env,
                )
                pid = proc.pid

                # Assign to Win32 Job Object for kernel-level resource limits
                if _use_os_sandbox and pid is not None:
                    try:
                        from anteroom.tools.sandbox_win32 import setup_job_for_process

                        job_handle = setup_job_for_process(sandbox_config.sandbox, pid)
                    except Exception:
                        logger.debug("Win32 Job Object setup failed for bg task %s", task_id[:8])

                # Update PID in DB
                db.execute(
                    "UPDATE background_tasks SET pid = ? WHERE id = ?",
                    (pid, task_id),
                )
                db.commit()

                # Wait for completion with timeout
                try:
                    stdout_bytes, stderr_bytes = await asyncio.wait_for(proc.communicate(), timeout=timeout)
                except asyncio.TimeoutError:
                    if job_handle is not None:
                        try:
                            from anteroom.tools.sandbox_win32 import terminate_job

                            terminate_job(job_handle)
                        except Exception:
                            pass
                    proc.kill()
                    await proc.wait()
                    stdout_bytes, stderr_bytes = b"", b""
                    elapsed = time.monotonic() - start_ts
                    timeout_msg = f"Command timed out after {timeout}s"
                    timeout_result = TaskResult.from_shell_task(-1, "", timeout_msg, elapsed, task_id)
                    db.execute(
                        "UPDATE background_tasks SET status = 'failed', exit_code = -1, "
                        "completed_at = ?, stderr_preview = ?, metadata_json = ? WHERE id = ?",
                        (_now(), timeout_msg, json.dumps({"task_result": timeout_result.to_dict()}), task_id),
                    )
                    db.commit()
                    if self._event_bus:
                        elapsed = round(time.monotonic() - start_ts, 2)
                        await self._event_bus.publish(
                            f"conversation:{conversation_id}",
                            {
                                "type": "task_completed",
                                "data": {
                                    "task_id": task_id,
                                    "command": command[:80],
                                    "status": "failed",
                                    "exit_code": -1,
                                    "duration_seconds": elapsed,
                                },
                            },
                        )
                    return

                exit_code = proc.returncode or 0
                status = "completed" if exit_code == 0 else "failed"
                completed_at = _now()
                elapsed = time.monotonic() - start_ts

                # Capture previews (last 2KB)
                stdout_str = stdout_bytes.decode("utf-8", errors="replace")
                stderr_str = stderr_bytes.decode("utf-8", errors="replace")
                stdout_preview = stdout_str[-_MAX_PREVIEW_BYTES:]
                stderr_preview = stderr_str[-_MAX_PREVIEW_BYTES:]

                task_result = TaskResult.from_shell_task(exit_code, stdout_str, stderr_str, elapsed, task_id)

                db.execute(
                    "UPDATE background_tasks SET status = ?, exit_code = ?, completed_at = ?, "
                    "stdout_preview = ?, stderr_preview = ?, metadata_json = ? WHERE id = ?",
                    (
                        status,
                        exit_code,
                        completed_at,
                        stdout_preview,
                        stderr_preview,
                        json.dumps({"task_result": task_result.to_dict()}),
                        task_id,
                    ),
                )
                db.commit()

                # Publish completion event
                if self._event_bus:
                    elapsed = round(time.monotonic() - start_ts, 2)
                    await self._event_bus.publish(
                        f"conversation:{conversation_id}",
                        {
                            "type": "task_completed",
                            "data": {
                                "task_id": task_id,
                                "command": command[:80],
                                "status": status,
                                "exit_code": exit_code,
                                "duration_seconds": elapsed,
                            },
                        },
                    )

            except Exception:
                logger.warning("Background task %s collector failed", task_id[:8], exc_info=True)
                try:
                    db.execute(
                        "UPDATE background_tasks SET status = 'failed', completed_at = ? WHERE id = ?",
                        (_now(), task_id),
                    )
                    db.commit()
                except Exception:
                    pass
            finally:
                # Clean up Win32 Job Object handle
                if job_handle is not None:
                    try:
                        from anteroom.tools.sandbox_win32 import close_job

                        close_job(job_handle)
                    except Exception:
                        pass
                self._tasks.pop(task_id, None)
                self._global_count = max(0, self._global_count - 1)

        loop = asyncio.get_running_loop()
        collector = loop.create_task(_collect())
        self._tasks[task_id] = collector
        self._global_count += 1

        # Publish start event (fire-and-forget — task ref kept to suppress warnings)
        if self._event_bus:
            _start_evt = loop.create_task(
                self._event_bus.publish(
                    f"conversation:{conversation_id}",
                    {
                        "type": "task_started",
                        "data": {
                            "task_id": task_id,
                            "command": command[:80],
                        },
                    },
                )
            )
            _start_evt.add_done_callback(lambda t: t.exception() if not t.cancelled() else None)

        return {
            "task_id": task_id,
            "status": "running",
            "command": command[:80],
        }

    def get_task(self, task_id: str, *, db: Any = None) -> dict[str, Any] | None:
        """Read a task record from DB."""
        db = db or self._db
        row = db.execute_fetchone("SELECT * FROM background_tasks WHERE id = ?", (task_id,))
        if not row:
            return None
        return self._deserialize(dict(row))

    def list_tasks(self, conversation_id: str, *, status: str | None = None, db: Any = None) -> list[dict[str, Any]]:
        """List tasks for a conversation, optionally filtered by status."""
        db = db or self._db
        if status:
            rows = db.execute_fetchall(
                "SELECT * FROM background_tasks WHERE conversation_id = ? AND status = ? ORDER BY started_at DESC",
                (conversation_id, status),
            )
        else:
            rows = db.execute_fetchall(
                "SELECT * FROM background_tasks WHERE conversation_id = ? ORDER BY started_at DESC",
                (conversation_id,),
            )
        return [self._deserialize(dict(r)) for r in rows]

    def count_running(self, *, db: Any = None) -> int:
        """Return the number of currently running background tasks."""
        db = db or self._db
        row = db.execute_fetchone("SELECT COUNT(*) FROM background_tasks WHERE status = 'running'")
        return int(row[0]) if row else 0

    def poll_completed(self) -> list[dict[str, Any]]:
        """Return tasks that completed since the last poll.

        Used by the CLI background poller for notification rendering.
        Each result includes a ``duration_seconds`` field computed from
        ``started_at`` and ``completed_at``.
        """
        if self._last_poll_time is None:
            self._last_poll_time = _now()
            return []

        rows = self._db.execute_fetchall(
            "SELECT * FROM background_tasks WHERE completed_at > ? ORDER BY completed_at",
            (self._last_poll_time,),
        )
        self._last_poll_time = _now()
        results = []
        for r in rows:
            task = self._deserialize(dict(r))
            task["duration_seconds"] = _compute_duration(task.get("started_at"), task.get("completed_at"))
            results.append(task)
        return results

    def cancel_task(self, task_id: str) -> bool:
        """Cancel a running background task."""
        task = self.get_task(task_id)
        if not task or task["status"] != "running":
            return False

        # Kill the in-process task if it exists
        collector = self._tasks.get(task_id)
        if collector and not collector.done():
            collector.cancel()

        self._db.execute(
            "UPDATE background_tasks SET status = 'cancelled', completed_at = ? WHERE id = ?",
            (_now(), task_id),
        )
        self._db.commit()
        return True

    def _count_running(self, conversation_id: str, *, db: Any = None) -> int:
        db = db or self._db
        row = db.execute_fetchone(
            "SELECT COUNT(*) FROM background_tasks WHERE conversation_id = ? AND status = 'running'",
            (conversation_id,),
        )
        return row[0] if row else 0

    async def shutdown(self) -> None:
        """Cancel all in-flight collector tasks (for clean teardown)."""
        for task in list(self._tasks.values()):
            if not task.done():
                task.cancel()
        for task in list(self._tasks.values()):
            try:
                await task
            except (asyncio.CancelledError, Exception):
                pass
        self._tasks.clear()

    @staticmethod
    def _deserialize(d: dict[str, Any]) -> dict[str, Any]:
        raw = d.pop("metadata_json", None)
        d["metadata"] = json.loads(raw) if raw else None
        return d
