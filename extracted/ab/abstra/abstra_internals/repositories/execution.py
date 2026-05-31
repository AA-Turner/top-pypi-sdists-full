import datetime
import os
import signal
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional, cast

from abstra_internals.cloud_api.http_client import HTTPClient
from abstra_internals.consts.filepaths import EXECUTIONS_DIR_PATH
from abstra_internals.entities.execution import Execution
from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.producer import WebEditorControlProducerRepository
from abstra_internals.services.sql_storage import SqlStorage

if TYPE_CHECKING:
    from typing_extensions import LiteralString


@dataclass
class ExecutionFilter:
    build_id: Optional[str] = None
    stage_id: Optional[str] = None
    status: Optional[str] = None
    project_id: Optional[str] = None
    offset: Optional[int] = None
    limit: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    search: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> "ExecutionFilter":
        return ExecutionFilter(
            build_id=data.get("buildId"),
            stage_id=data.get("stageId"),
            status=data.get("status"),
            project_id=data.get("projectId"),
            offset=int(data.get("offset", 0)),
            limit=int(data.get("limit", 10)),
            start_date=data.get("startDate"),
            end_date=data.get("endDate"),
            search=data.get("search"),
        )

    def to_dict(self) -> dict:
        return dict((k, v) for k, v in self.__dict__.items() if v is not None)


class ExecutionResponse:
    def __init__(self, executions: List[Execution], total_count: int):
        self.executions = executions
        self.total_count = total_count

    @staticmethod
    def from_dict(data: dict) -> "ExecutionResponse":
        return ExecutionResponse(
            executions=[Execution.create(**dto) for dto in data.get("executions", [])],
            total_count=data.get("totalCount", 0),
        )

    def to_dict(self) -> dict:
        return dict(
            executions=[execution.dump() for execution in self.executions],
            totalCount=self.total_count,
        )


class ExecutionRepository(ABC):
    @abstractmethod
    def create(self, execution: Execution) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get(self, execution_id: str) -> Execution:
        raise NotImplementedError

    @abstractmethod
    def update(self, execution: Execution) -> None:
        raise NotImplementedError()

    @abstractmethod
    def set_failure_by_id(self, execution_id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        raise NotImplementedError()

    @abstractmethod
    def list(self, filter) -> ExecutionResponse:
        raise NotImplementedError()

    @abstractmethod
    def stop_execution(self, execution_id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def stop_all_running(self) -> None:
        raise NotImplementedError()


class LocalExecutionRepository(ExecutionRepository):
    def __init__(self):
        self.fs_storage = SqlStorage(directory=EXECUTIONS_DIR_PATH, model=Execution)

    def create(self, execution: Execution) -> None:
        self.fs_storage.save(execution.id, execution)

    def update(self, execution: Execution) -> None:
        self.fs_storage.save(execution.id, execution)

    def set_failure_by_id(self, execution_id: str) -> None:
        try:
            execution = self.get(execution_id)
            execution.set_status("failed")
            self.update(execution)
        except Exception:
            pass

    def clear(self):
        self.fs_storage.clear()

    def get(self, execution_id: str) -> Execution:
        execution = self.fs_storage.load(execution_id)
        if execution is None:
            raise Exception(f"Execution with id {execution_id} not found")

        return execution

    def list(self, filter: ExecutionFilter) -> ExecutionResponse:
        executions = self.fs_storage.load_all()
        filtered_executions = [
            execution
            for execution in executions
            if (
                (not filter.build_id or execution.stage_id == filter.build_id)
                and (not filter.stage_id or execution.stage_id == filter.stage_id)
                and (not filter.status or execution.status == filter.status)
                and (not filter.project_id or execution.stage_id == filter.project_id)
                and (not filter.search or execution.id.startswith(filter.search))
                and (
                    not filter.start_date
                    or execution.created_at
                    >= datetime.datetime.fromisoformat(filter.start_date)
                )
                and (
                    not filter.end_date
                    or execution.created_at
                    <= datetime.datetime.fromisoformat(filter.end_date)
                )
            )
        ]
        sorted_executions = sorted(
            filtered_executions,
            key=lambda execution: execution.created_at,
            reverse=True,
        )
        total_count = len(sorted_executions)
        start_index = filter.offset if filter.offset else 0
        end_index = start_index + (
            filter.limit if filter.limit else len(sorted_executions)
        )

        return ExecutionResponse(
            executions=sorted_executions[start_index:end_index],
            total_count=total_count,
        )

    def stop_execution(self, execution_id: str) -> None:
        try:
            execution = self.get(execution_id)
            pid = execution.pid

            os.kill(pid, signal.SIGTERM)

            for _ in range(20):
                try:
                    os.kill(pid, 0)
                    time.sleep(0.1)
                except OSError:
                    return

            # Force kill if still alive
            os.kill(pid, signal.SIGKILL)

        except Exception:
            pass

    def stop_all_running(self) -> None:
        running = self.list(ExecutionFilter(status="running", limit=10000)).executions
        pids = [execution.pid for execution in running if execution.pid]

        for pid in pids:
            try:
                os.kill(pid, signal.SIGTERM)
            except Exception:
                pass

        # Single shared 2s budget for graceful shutdown.
        deadline = time.time() + 2.0
        survivors = list(pids)
        while survivors and time.time() < deadline:
            still_alive = []
            for pid in survivors:
                try:
                    os.kill(pid, 0)
                    still_alive.append(pid)
                except OSError:
                    pass
            survivors = still_alive
            if survivors:
                time.sleep(0.1)

        for pid in survivors:
            try:
                os.kill(pid, signal.SIGKILL)
            except Exception:
                pass


class WebEditorExecutionRepository(LocalExecutionRepository):
    def __init__(self, rabbitmq_uri: str):
        super().__init__()
        self.control_producer = WebEditorControlProducerRepository(rabbitmq_uri)

    def stop_execution(self, execution_id: str) -> None:
        try:
            self.control_producer.stop_execution(execution_id)
        except Exception:
            # Fallback to local kill if message fails? Unlikely to work but maybe safe to try?
            # No, if we are in web editor, local kill is useless.
            pass

    def stop_all_running(self) -> None:
        try:
            self.control_producer.stop_all_executions()
        except Exception:
            pass


class PgWebEditorExecutionRepository(ExecutionRepository):
    """PostgreSQL-backed execution repository for the web-editor DB path.

    Independent class (decision D1: ``Pg`` prefix) — does NOT inherit
    ``LocalExecutionRepository`` (file-based). ``stop_execution`` /
    ``stop_all_running`` stay on RabbitMQ control, identical to the file-based
    ``WebEditorExecutionRepository``.
    """

    def __init__(self, rabbitmq_uri: str):
        # psycopg imports here (not at module top) so the legacy path never
        # imports psycopg (decision D8). Only instantiated on the DB path.
        from psycopg.rows import dict_row
        from psycopg.types.json import Jsonb

        self._dict_row = dict_row
        self._jsonb = Jsonb
        self.control_producer = WebEditorControlProducerRepository(rabbitmq_uri)

    def _connection(self):
        from abstra_internals.services.db.connection import get_pool

        return get_pool().connection()

    @staticmethod
    def _row_to_execution(row: dict) -> Execution:
        # Reconstruct via the pydantic constructor (NOT Execution.create, which
        # would reset status/created_at). populate_by_name=True accepts snake_case
        # field names; the jsonb ``context`` (camelCase, as dumped) rebuilds the
        # right ClientContext subtype through its ``type`` discriminator.
        return Execution(
            id=row["id"],
            stage_id=row["stage_id"],
            status=row["status"],
            pid=row["pid"],
            worker_id=row["worker_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            context=row["context"],
        )

    def create(self, execution: Execution) -> None:
        with self._connection() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO executions (id, stage_id, status, pid, worker_id, "
                "context, created_at, updated_at, db_updated_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())",
                (
                    execution.id,
                    execution.stage_id,
                    execution.status,
                    execution.pid,
                    execution.worker_id,
                    self._jsonb(execution.context.dump()),
                    execution.created_at,
                    execution.updated_at,
                ),
            )

    def get(self, execution_id: str) -> Execution:
        with self._connection() as conn, conn.cursor(row_factory=self._dict_row) as cur:
            cur.execute("SELECT * FROM executions WHERE id=%s", (execution_id,))
            row = cur.fetchone()
            if row is None:
                raise Exception(f"Execution with id {execution_id} not found")
            return self._row_to_execution(row)

    def update(self, execution: Execution) -> None:
        with self._connection() as conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE executions SET status=%s, pid=%s, worker_id=%s, "
                "context=%s, updated_at=%s, db_updated_at=now() WHERE id=%s",
                (
                    execution.status,
                    execution.pid,
                    execution.worker_id,
                    self._jsonb(execution.context.dump()),
                    execution.updated_at,
                    execution.id,
                ),
            )

    def set_failure_by_id(self, execution_id: str) -> None:
        # Best-effort safety net, matching LocalExecutionRepository (swallows).
        # Bumps updated_at like Local's set_status does.
        try:
            with self._connection() as conn, conn.cursor() as cur:
                cur.execute(
                    "UPDATE executions SET status='failed', updated_at=now(), "
                    "db_updated_at=now() WHERE id=%s",
                    (execution_id,),
                )
        except Exception as e:
            AbstraLogger.capture_exception(e)

    def clear(self):
        with self._connection() as conn, conn.cursor() as cur:
            cur.execute("TRUNCATE executions")

    @staticmethod
    def _like_prefix(search: str) -> str:
        # Reproduce ``id.startswith(search)``: escape LIKE metacharacters so user
        # '%' / '_' match literally (default backslash escape).
        escaped = search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        return escaped + "%"

    def list(self, filter: ExecutionFilter) -> ExecutionResponse:
        clauses: List[str] = []
        params: list = []
        # NOTE: build_id and project_id filter against stage_id — replicated
        # faithfully from LocalExecutionRepository.list (pre-existing behavior).
        if filter.build_id:
            clauses.append("stage_id = %s")
            params.append(filter.build_id)
        if filter.stage_id:
            clauses.append("stage_id = %s")
            params.append(filter.stage_id)
        if filter.status:
            clauses.append("status = %s")
            params.append(filter.status)
        if filter.project_id:
            clauses.append("stage_id = %s")
            params.append(filter.project_id)
        if filter.search:
            clauses.append("id LIKE %s")
            params.append(self._like_prefix(filter.search))
        if filter.start_date:
            clauses.append("created_at >= %s::timestamptz")
            params.append(filter.start_date)
        if filter.end_date:
            clauses.append("created_at <= %s::timestamptz")
            params.append(filter.end_date)

        where_sql = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        filter_params = list(params)  # WHERE-clause params only (no limit/offset)
        # id DESC tie-break → deterministic pagination (created_at can tie).
        sql = (
            "SELECT *, count(*) OVER() AS total_count FROM executions"
            + where_sql
            + " ORDER BY created_at DESC, id DESC"
        )
        if filter.limit is not None:
            sql += " LIMIT %s"
            params.append(filter.limit)
        sql += " OFFSET %s"
        params.append(filter.offset or 0)

        with self._connection() as conn, conn.cursor(row_factory=self._dict_row) as cur:
            # Query structure built only from fixed fragments; values via params.
            cur.execute(cast("LiteralString", sql), params)
            rows = cur.fetchall()
            if rows:
                total = rows[0]["total_count"]
            else:
                # Paging past the last page returns no rows, so the window count
                # is unavailable — fetch it separately to match LocalExecutionRepo,
                # which always returns the true total regardless of offset.
                cur.execute(
                    cast(
                        "LiteralString", "SELECT count(*) FROM executions" + where_sql
                    ),
                    filter_params,
                )
                count_row = cur.fetchone()
                total = count_row["count"] if count_row else 0

        executions = []
        skipped = 0
        for row in rows:
            try:
                executions.append(self._row_to_execution(row))
            except Exception as e:
                # A single un-reconstructable context (e.g. a stale row after a
                # model change) must not 500 the whole listing — skip + report.
                skipped += 1
                AbstraLogger.capture_exception(e)
        # Keep total_count consistent with what we can actually return: count(*)
        # OVER() counted the skipped rows too, which would make a paginating
        # client read a short page as "the last page". Decrementing keeps the
        # page size and the total in agreement (skips are near-impossible anyway
        # given the 24h retention — this only bites during a context-model
        # transition, and only undercounts by this page's skips).
        return ExecutionResponse(
            executions=executions, total_count=max(0, total - skipped)
        )

    def stop_execution(self, execution_id: str) -> None:
        try:
            self.control_producer.stop_execution(execution_id)
        except Exception as e:
            # Best-effort (RabbitMQ control), but surface the failure so a
            # silently-ignored "stop" click is observable.
            AbstraLogger.capture_exception(e)

    def stop_all_running(self) -> None:
        try:
            self.control_producer.stop_all_executions()
        except Exception as e:
            AbstraLogger.capture_exception(e)


class ProductionExecutionRepository(ExecutionRepository):
    def __init__(self, client: "HTTPClient"):
        self.client = client

    def _adapt_legacy_execution_dtos(self, dtos: List[dict]) -> List[dict]:
        for dto in dtos:
            if dto.get("stage_run_id"):
                del dto["stage_run_id"]
            if dto.get("request_context"):
                dto["context"] = dto["request_context"]
                del dto["request_context"]

        return dtos

    def create(self, execution: Execution) -> None:
        request_dto = dict(
            **execution.dump(),
        )

        res = self.client.post(
            endpoint="/executions",
            json=request_dto,
        )

        res.raise_for_status()

    def update(self, execution: Execution) -> None:
        request_dto = dict(
            status=execution.status,
            context=execution.context.dump() or {},
        )

        res = self.client.patch(
            f"/executions/{execution.id}",
            json=request_dto,
        )

        res.raise_for_status()

    def set_failure_by_id(self, execution_id: str) -> None:
        res = self.client.patch(
            f"/executions/{execution_id}",
            json=dict(status="failed"),
        )

        res.raise_for_status()

    def get(self, execution_id: str) -> Execution:
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError()

    def list(self, filter: ExecutionFilter) -> ExecutionResponse:
        raise NotImplementedError()

    def stop_execution(self, execution_id: str) -> None:
        raise NotImplementedError()

    def stop_all_running(self) -> None:
        raise NotImplementedError()
