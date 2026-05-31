import json
import os
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, TypedDict, cast

from abstra_internals.cloud_api.http_client import HTTPClient
from abstra_internals.consts.filepaths import LOCAL_LOGS_DIR_PATH
from abstra_internals.logger import AbstraLogger
from abstra_internals.utils import serialize
from abstra_internals.utils.datetime import from_utc_iso_string, to_utc_iso_string

if TYPE_CHECKING:
    from typing_extensions import LiteralString


@dataclass
class LogEntry:
    execution_id: str
    stage_id: str
    created_at: datetime
    event: Literal["stderr", "stdout"]
    payload: Dict[Literal["text"], str]
    sequence: int

    def to_dto(self) -> Dict[str, Any]:
        return {
            "executionId": self.execution_id,
            "stageId": self.stage_id,
            "createdAt": to_utc_iso_string(self.created_at),
            "event": self.event,
            "payload": self.payload,
            "sequence": self.sequence,
        }

    @staticmethod
    def from_dto(dto: Dict) -> "LogEntry":
        if dto.get("event") == "stdout" or dto.get("event") == "stderr":
            return LogEntry(
                execution_id=dto["executionId"],
                stage_id=dto["stageId"],
                created_at=from_utc_iso_string(dto["createdAt"]),
                event=dto["event"],
                payload=dto["payload"],
                sequence=dto["sequence"],
            )
        else:
            raise Exception("Invalid log entry type")


LogEvent = Literal["stdout", "stderr"]
LogsDTO = TypedDict("LogsDTO", {"type": str, "text": str})


class ExecutionLogsRepository(ABC):
    sequence: int

    def get_sequence(self) -> int:
        self.sequence += 1
        return self.sequence

    def insert_stdio(
        self,
        execution_id: str,
        stage_id: str,
        event: Literal["stdout", "stderr"],
        text: str,
    ):
        self.save(
            LogEntry(
                execution_id=execution_id,
                stage_id=stage_id,
                # Aware UTC — see Execution.create rationale (timestamptz on DB).
                created_at=datetime.now(timezone.utc),
                event=event,
                payload={"text": text},
                sequence=self.get_sequence(),
            )
        )

    @abstractmethod
    def save(self, log_entry: LogEntry) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get(
        self,
        execution_id: str,
        event: Optional[LogEvent] = None,
    ) -> List[LogEntry]:
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        raise NotImplementedError()

    def final_flush(self) -> None:
        """Drain any buffered writes (e.g. at the end of an execution).

        No-op for the file/HTTP-backed repositories; overridden by the buffered
        PostgreSQL repository. Typed on the ABC so callers (e.g.
        ExecutionController.run) invoke it directly instead of duck-typing.
        """

    def close(self) -> None:
        """Release any background resources (flush thread, atexit). No-op by
        default; overridden by the buffered PostgreSQL repository."""


class LocalExecutionLogsRepository(ExecutionLogsRepository):
    def __init__(self):
        self.sequence = 0

    def save(self, log_entry: LogEntry) -> None:
        execution_id = log_entry.execution_id

        if not execution_id:
            return

        log_file = Path(LOCAL_LOGS_DIR_PATH) / f"{execution_id}.log"

        if not log_file.parent.exists():
            log_file.parent.mkdir(parents=True)

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(serialize(log_entry.to_dto()) + "\n")

    def get(
        self,
        execution_id: str,
        event: Optional[LogEvent] = None,
    ) -> List[LogEntry]:
        log_file = Path(LOCAL_LOGS_DIR_PATH) / f"{execution_id}.log"

        if not log_file.exists():
            return []

        try:
            with open(log_file, "r", encoding="utf-8") as f:
                logs: List[LogEntry] = []
                for line in f.readlines():
                    dto = json.loads(line)
                    if event and dto["event"] != event:
                        continue
                    logs.append(LogEntry.from_dto(dto))
                return logs
        except Exception as e:
            AbstraLogger.capture_exception(e)
            return []

    def clear(self):
        log_dir = Path(LOCAL_LOGS_DIR_PATH)
        if log_dir.exists() and log_dir.is_dir():
            for log_file in log_dir.iterdir():
                if log_file.is_file():
                    log_file.unlink()


class PgWebEditorExecutionLogsRepository(ExecutionLogsRepository):
    """PostgreSQL-backed logs repository for the web-editor DB path (decision D1).

    Writes are buffered in memory and flushed as a single multi-row INSERT every
    ``FLUSH_INTERVAL`` seconds by a daemon thread. Persistence batching is new
    infra here (the file-based path was write-a-write; only the broadcast path
    batched).

    Connection (decision D11): every flush does its own ``get_pool()`` checkout,
    so the daemon thread and the synchronous ``final_flush`` from
    ``ExecutionController.run()`` never share a connection, and a dropped
    connection is transparently reopened by the pool at the next checkout.

    Best-effort: a flush failure NEVER propagates to ``save``/the user execution —
    those logs are dropped (counted + warned) and the next flush proceeds. The
    executor is long-lived and serves several executions, so ``final_flush``
    drains the buffer WITHOUT stopping the daemon loop; the loop is only stopped
    by ``close()`` (shutdown) or the atexit handler (process exit).
    """

    FLUSH_INTERVAL = 0.2
    # Cap buffered entries so a runaway producer (or a DB outage) can't grow the
    # buffer unbounded; oldest entries are shed (deque maxlen) and counted.
    MAX_BUFFER = 100_000
    # Rows per INSERT, kept well under Postgres's 65535 bound-parameter cap
    # (6 params/row → 10922 max); large batches are chunked.
    MAX_ROWS_PER_INSERT = 5000

    def __init__(self):
        import atexit
        from collections import deque

        # psycopg imports here so the legacy path never imports psycopg (D8).
        from psycopg.rows import dict_row

        self._dict_row = dict_row
        self.sequence = 0
        self._buffer = deque(maxlen=self.MAX_BUFFER)
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._closed = False
        # Observability (§24.6): dropped logs + cumulative insert timing.
        self._dropped = 0
        self._insert_count = 0
        self._insert_seconds = 0.0
        self._flushes = 0
        self._atexit = atexit  # kept for unregister in close()
        self._flush_thread = threading.Thread(
            target=self._flush_loop, daemon=True, name="PgLogsFlush"
        )
        self._flush_thread.start()
        atexit.register(self._on_process_exit)

    def _connection(self):
        from abstra_internals.services.db.connection import get_pool

        return get_pool().connection()

    @staticmethod
    def _sanitize(text: str) -> str:
        # Postgres text cannot store NUL (0x00); strip it so one binary line
        # can't fail the whole batch. Cheap and only on the DB path.
        return text.replace("\x00", "�") if "\x00" in text else text

    def save(self, log_entry: LogEntry) -> None:
        if not log_entry.execution_id:
            return
        log_entry.payload["text"] = self._sanitize(log_entry.payload["text"])
        with self._lock:
            if len(self._buffer) >= self.MAX_BUFFER:
                # deque(maxlen) will shed the oldest on append; count the loss.
                self._dropped += 1
            self._buffer.append(log_entry)

    def _flush_loop(self) -> None:
        while not self._stop.wait(self.FLUSH_INTERVAL):
            self._flush()
            self._flushes += 1
            # Roughly every 30s, emit cumulative insert timing (§24.6).
            if self._flushes % max(1, int(30 / self.FLUSH_INTERVAL)) == 0 and (
                self._insert_count or self._dropped
            ):
                avg_ms = (
                    (self._insert_seconds / self._insert_count * 1000)
                    if self._insert_count
                    else 0.0
                )
                AbstraLogger.info(
                    "[db.logs] stats",
                    {
                        "inserts": self._insert_count,
                        "avgInsertMs": round(avg_ms, 2),
                        "dropped": self._dropped,
                    },
                )
                # Also surface pool health from this (worker/executor) process —
                # the poller's log_pool_stats only runs in the editor pod.
                try:
                    from abstra_internals.services.db.connection import log_pool_stats

                    log_pool_stats()
                except Exception:
                    pass

    def _flush(self) -> None:
        with self._lock:
            if not self._buffer:
                return
            batch = list(self._buffer)
            self._buffer.clear()
        # The whole connection-acquire + insert is the best-effort boundary: a
        # dead/unreachable DB must never propagate. The pool reopens broken
        # connections on the next checkout (no manual reconnect).
        try:
            self._insert_batch(batch)
        except Exception as e:
            self._dropped += len(batch)
            # Data-loss event — warn immediately (don't wait for the 30s tick;
            # a short execution may exit before then).
            AbstraLogger.warning(
                f"[db.logs] dropped {len(batch)} log lines on flush failure"
            )
            AbstraLogger.capture_exception(e)

    def final_flush(self) -> None:
        """Drain the buffer now (e.g. at the end of an execution).

        Does NOT stop the daemon loop — the same repo instance serves later
        executions in the long-lived executor process.
        """
        self._flush()

    def close(self) -> None:
        """Stop the flush daemon and drain once. Idempotent. Safe to call from
        any thread except the flush thread itself (guarded)."""
        if self._closed:
            return
        self._closed = True
        self._stop.set()
        if threading.current_thread() is not self._flush_thread:
            self._flush_thread.join(timeout=2.0)
        try:
            self._atexit.unregister(self._on_process_exit)
        except Exception:
            pass
        self._flush()

    def _on_process_exit(self) -> None:
        # Final drain at interpreter exit. Stop the loop and flush once; guarded
        # so a flush already in progress on the daemon isn't double-run here.
        self._stop.set()
        if not self._closed:
            self._flush()

    def _insert_batch(self, batch) -> None:
        if not batch:
            return
        # Multi-row INSERT: one statement / one round-trip per chunk. NOT
        # executemany (one statement per row — far slower). Chunked to stay under
        # the 65535 bound-parameter wire cap.
        for start in range(0, len(batch), self.MAX_ROWS_PER_INSERT):
            chunk = batch[start : start + self.MAX_ROWS_PER_INSERT]
            values_template = ",".join(["(%s,%s,%s,%s,%s,%s)"] * len(chunk))
            params: list = []
            for e in chunk:
                params.extend(
                    [
                        e.execution_id,
                        e.stage_id,
                        e.event,
                        e.payload["text"],
                        e.sequence,
                        e.created_at,
                    ]
                )
            sql = (
                "INSERT INTO execution_logs "
                "(execution_id, stage_id, event, text, sequence, created_at) "
                "VALUES " + values_template
            )
            started = time.monotonic()
            with self._connection() as conn, conn.cursor() as cur:
                # Only the (%s,...) placeholder count is dynamic; values via params.
                cur.execute(cast("LiteralString", sql), params)
            self._insert_seconds += time.monotonic() - started
            self._insert_count += 1

    def get(
        self,
        execution_id: str,
        event: Optional[LogEvent] = None,
    ) -> List[LogEntry]:
        sql = (
            "SELECT execution_id, stage_id, event, text, sequence, created_at "
            "FROM execution_logs WHERE execution_id=%s"
        )
        params: list = [execution_id]
        if event is not None:
            sql += " AND event=%s"
            params.append(event)
        sql += " ORDER BY id"
        with self._connection() as conn, conn.cursor(row_factory=self._dict_row) as cur:
            cur.execute(sql, params)
            return [
                LogEntry(
                    execution_id=row["execution_id"],
                    stage_id=row["stage_id"],
                    created_at=row["created_at"],
                    event=row["event"],
                    payload={"text": row["text"]},
                    sequence=row["sequence"],
                )
                for row in cur.fetchall()
            ]

    def clear(self):
        with self._connection() as conn, conn.cursor() as cur:
            cur.execute("TRUNCATE execution_logs")


class ProductionExecutionLogsRepository(ExecutionLogsRepository):
    # Thread-local reentry guard — see save() below for why.
    _saving = threading.local()

    def __init__(self, client: "HTTPClient"):
        self.sequence = 0
        self.client = client

    def save(self, log_entry: LogEntry) -> None:
        # In prod, logs are captured by the cluster's log collector (Fluentbit/Filebeat)
        # and this is a no-op. In local-player mode there is no log collector, so we
        # forward the entry over HTTP and let cloud-api index it into ES directly.
        if os.getenv("ABSTRA_LOCAL_LOGS") != "true":
            return

        # The HTTP stack (urllib3, OTel requests instrumentation, etc.) emits lines on
        # stdout/stderr that abstra's stdio capture hooks and feeds back into this same
        # save() — infinite recursion. Guard re-entry so nested calls are dropped.
        if getattr(self._saving, "active", False):
            return
        self._saving.active = True
        try:
            dto = log_entry.to_dto()
            body = {
                "createdAt": dto["createdAt"],
                "event": dto["event"],
                "payload": dto["payload"],
                "sequence": dto["sequence"],
            }
            response = self.client.post(
                f"/executions/{log_entry.execution_id}/logs", json=body
            )
            response.raise_for_status()
        except Exception as e:
            AbstraLogger.capture_exception(e)
        finally:
            self._saving.active = False

    def get(
        self,
        execution_id: str,
        event: Optional[LogEvent] = None,
    ) -> List[LogEntry]:
        response = self.client.get(
            f"/executions/{execution_id}/logs",
            params={"event": event} if event else None,
        )

        response.raise_for_status()

        return [LogEntry.from_dto(log) for log in response.json()]

    def clear(self):
        raise NotImplementedError()
