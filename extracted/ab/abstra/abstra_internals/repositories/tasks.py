import datetime
import json
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Union, cast
from uuid import uuid4

from abstra_internals.cloud_api.http_client import HTTPClient
from abstra_internals.consts.filepaths import TASKS_DIR_PATH
from abstra_internals.contracts_generated import (
    CloudApiCliTasksUpdateTaskRequest,
    CloudApiConsoleWorkflowUpdateTaskRequestCompleted,
    CloudApiConsoleWorkflowUpdateTaskRequestLocked,
)
from abstra_internals.environment import WORKER_LOG_TO_QUEUE
from abstra_internals.services.sql_storage import SqlStorage
from abstra_internals.utils.datetime import to_utc_iso_string
from abstra_internals.utils.serializable import Serializable

if TYPE_CHECKING:
    from typing_extensions import LiteralString

TaskStatus = Literal["pending", "locked", "completed"]
TaskPayload = Dict[str, Any]


class TaskLockFailed(Exception):
    pass


class TaskEventDetails(Serializable):
    at: str
    by_execution_id: Optional[str]
    by_stage_id: Optional[str]


class TaskDTO(Serializable):
    id: str
    type: str
    payload: dict
    status: TaskStatus
    target_stage_id: str
    created: TaskEventDetails
    locked: Optional[TaskEventDetails]
    completed: Optional[TaskEventDetails]


class ExecutionTasksResponse(Serializable):
    trigger_task: Optional[TaskDTO]
    sent_tasks: List[TaskDTO]


class TasksRepository(ABC):
    @abstractmethod
    def send_task(
        self,
        type: str,
        payload: TaskPayload,
        target_stage_id: str,
        source_stage_id: Optional[str],
        execution_id: Optional[str],
    ) -> TaskDTO:
        raise NotImplementedError()

    @abstractmethod
    def get_by_id(self, task_id: str) -> TaskDTO:
        raise NotImplementedError()

    @abstractmethod
    def lock_task(
        self, task_id: str, execution_id: Optional[str], stage_id: Optional[str]
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def complete_task(
        self, task_id: str, execution_id: Optional[str], stage_id: Optional[str]
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def set_task_to_pending(self, task_id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_pending_tasks(
        self, stage_id: str, limit: Union[int, None], offset: int, where: Dict
    ) -> List[TaskDTO]:
        raise NotImplementedError()

    @abstractmethod
    def get_sent_tasks(
        self, stage_id: str, limit: Union[int, None], offset: int, where: Dict
    ) -> List[TaskDTO]:
        raise NotImplementedError()

    @abstractmethod
    def get_stage_tasks(self, stage_id: str) -> List[TaskDTO]:
        raise NotImplementedError()

    @abstractmethod
    def get_all_tasks(self) -> List[TaskDTO]:
        raise NotImplementedError()

    @abstractmethod
    def get_execution_sent_tasks(self, execution_id: str) -> List[TaskDTO]:
        raise NotImplementedError()

    @abstractmethod
    def set_locked_tasks_to_pending(self, execution_id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        raise NotImplementedError()


class LocalTasksRepository(TasksRepository):
    def __init__(self):
        self.fs_storage = SqlStorage(directory=TASKS_DIR_PATH, model=TaskDTO)

    def _broadcast_task_if_connected(self, task: TaskDTO):
        if not WORKER_LOG_TO_QUEUE:
            return

        from abstra_internals.controllers.execution.execution_conn import (
            get_broadcast_publisher,
        )

        publisher = get_broadcast_publisher()
        if publisher is not None:
            try:
                task_msg = {"type": "task", "payload": task.dump()}
                publisher.publish(task_msg)
            except Exception:
                pass

    def clear(self):
        self.fs_storage.clear()

    def get(self, id: str) -> TaskDTO:
        task = self.fs_storage.load(id)
        if task is None:
            raise Exception(f"Task with id {id} not found")

        return task

    def send_task(
        self,
        type: str,
        payload: TaskPayload,
        target_stage_id: str,
        source_stage_id: Optional[str],
        execution_id: Optional[str],
    ) -> TaskDTO:
        id = str(uuid4())
        task = TaskDTO(
            id=id,
            type=type,
            payload=payload,
            status="pending",
            target_stage_id=target_stage_id,
            created=TaskEventDetails(
                at=to_utc_iso_string(datetime.datetime.now(datetime.timezone.utc)),
                by_execution_id=execution_id,
                by_stage_id=source_stage_id,
            ),
            locked=None,
            completed=None,
        )
        self.fs_storage.save(id, task)
        self._broadcast_task_if_connected(task)
        return task

    def lock_task(
        self, task_id: str, execution_id: Optional[str], stage_id: Optional[str]
    ) -> None:
        task = self.get(task_id)

        if task.status != "pending":
            raise TaskLockFailed(f"Task {task_id} has already {task.status}")

        task.status = "locked"
        task.locked = TaskEventDetails(
            at=to_utc_iso_string(datetime.datetime.now(datetime.timezone.utc)),
            by_execution_id=execution_id,
            by_stage_id=stage_id,
        )

        self.fs_storage.save(task_id, task)
        self._broadcast_task_if_connected(task)

    def complete_task(
        self, task_id: str, execution_id: Optional[str], stage_id: Optional[str]
    ) -> None:
        task = self.get(task_id)

        if task.status != "pending" and task.status != "locked":
            raise TaskLockFailed(f"Task {task_id} has not been pending nor locked")

        task.status = "completed"
        task.completed = TaskEventDetails(
            at=to_utc_iso_string(datetime.datetime.now(datetime.timezone.utc)),
            by_execution_id=execution_id,
            by_stage_id=stage_id,
        )

        self.fs_storage.save(task_id, task)
        self._broadcast_task_if_connected(task)

    def set_task_to_pending(self, task_id: str) -> None:
        task = self.get(task_id)

        if task.status != "completed":
            raise TaskLockFailed(f"Task {task_id} is not completed")

        task.status = "pending"

        self.fs_storage.save(task_id, task)
        self._broadcast_task_if_connected(task)

    def _where_matches(self, task: TaskDTO, where: Dict) -> bool:
        payload = task.payload
        for key, value in where.items():
            if key not in payload or payload[key] != value:
                return False
        return True

    def get_pending_tasks(
        self, stage_id: str, limit: Union[int, None], offset: int, where: Dict
    ) -> List[TaskDTO]:
        all_tasks = self.fs_storage.load_all()
        pending_tasks = [
            task
            for task in all_tasks
            if task.target_stage_id == stage_id
            and task.status == "pending"
            and self._where_matches(task, where)
        ]
        pending_tasks = sorted(
            pending_tasks, key=lambda task: task.created.at, reverse=True
        )

        if limit is None:
            return pending_tasks[offset:]
        return pending_tasks[offset : offset + limit]

    def get_sent_tasks(
        self, stage_id: str, limit: Union[int, None], offset: int, where: Dict
    ) -> List[TaskDTO]:
        all_tasks = self.fs_storage.load_all()
        sent_tasks = [
            task
            for task in all_tasks
            if task.created.by_stage_id == stage_id and self._where_matches(task, where)
        ]
        sent_tasks = sorted(sent_tasks, key=lambda task: task.created.at, reverse=True)

        if limit is None:
            return sent_tasks[offset:]
        return sent_tasks[offset : offset + limit]

    def get_stage_tasks(self, stage_id: str) -> List[TaskDTO]:
        all_tasks = self.fs_storage.load_all()
        stage_tasks = [task for task in all_tasks if task.target_stage_id == stage_id]
        return sorted(stage_tasks, key=lambda task: task.created.at, reverse=True)

    def get_by_id(self, task_id: str) -> TaskDTO:
        return self.get(task_id)

    def get_all_tasks(self) -> List[TaskDTO]:
        all_tasks = self.fs_storage.load_all()
        return sorted(all_tasks, key=lambda task: task.created.at, reverse=True)

    def get_execution_sent_tasks(self, execution_id: str) -> List[TaskDTO]:
        all_tasks = self.fs_storage.load_all()
        return [
            task for task in all_tasks if task.created.by_execution_id == execution_id
        ]

    def set_locked_tasks_to_pending(self, execution_id: str) -> None:
        all_tasks = self.fs_storage.load_all()
        for task in all_tasks:
            if (
                task.locked
                and task.locked.by_execution_id == execution_id
                and task.status == "locked"
            ):
                task.status = "pending"
                self.fs_storage.save(task.id, task)


def task_row_to_dto(row: Dict[str, Any]) -> TaskDTO:
    """Build a ``TaskDTO`` from a ``tasks`` row dict (shared by the repo and the
    editor poller). The flattened event columns are remounted into
    ``TaskEventDetails``."""
    return TaskDTO(
        id=row["id"],
        type=row["type"],
        payload=row["payload"],
        status=row["status"],
        target_stage_id=row["target_stage_id"],
        created=TaskEventDetails(
            at=to_utc_iso_string(row["created_at"]),
            by_execution_id=row["created_by_execution"],
            by_stage_id=row["created_by_stage"],
        ),
        locked=(
            TaskEventDetails(
                at=to_utc_iso_string(row["locked_at"]),
                by_execution_id=row["locked_by_execution"],
                by_stage_id=row["locked_by_stage"],
            )
            if row["locked_at"]
            else None
        ),
        completed=(
            TaskEventDetails(
                at=to_utc_iso_string(row["completed_at"]),
                by_execution_id=row["completed_by_execution"],
                by_stage_id=row["completed_by_stage"],
            )
            if row["completed_at"]
            else None
        ),
    )


class PgWebEditorTasksRepository(TasksRepository):
    """PostgreSQL-backed tasks repository for the web-editor DB path (decision D1:
    ``Pg`` prefix avoids the name collision with the file-based
    ``WebEditorExecutionRepository`` family).

    All SQL is parameterized. The three event details (created/locked/completed)
    are flattened into columns and remounted into ``TaskEventDetails`` on read.
    There is NO RabbitMQ broadcast here: the editor poller derives the ``task``
    event from the table's ``db_updated_at`` column instead.
    """

    def __init__(self):
        # psycopg imports live here (not at module top) so the legacy file-based
        # path never imports psycopg (decision D8). This class is only
        # instantiated on the DB path by the factory.
        from psycopg.rows import dict_row
        from psycopg.types.json import Jsonb

        self._dict_row = dict_row
        self._jsonb = Jsonb

    def _connection(self):
        from abstra_internals.services.db.connection import get_pool

        return get_pool().connection()

    @staticmethod
    def _now() -> datetime.datetime:
        return datetime.datetime.now(datetime.timezone.utc)

    @staticmethod
    def _where_clauses(where: Dict) -> tuple:
        """Translate the SDK ``where`` dict to per-key top-level jsonb equality,
        replicating ``LocalTasksRepository._where_matches`` exactly (full value
        equality per key, AND across keys; a missing key yields NULL → excluded).
        NOT ``@>`` containment, which would diverge for nested dicts/lists."""
        clauses = []
        params: list = []
        for key, value in where.items():
            clauses.append(" AND payload -> %s = %s::jsonb")
            params.extend([key, json.dumps(value)])
        return "".join(clauses), params

    def _apply_transition(
        self, update_sql: str, params: tuple, task_id: str, kind: str
    ):
        """Run a conditional UPDATE atomically with a read of the pre-existing
        status (single CTE, no TOCTOU). On no-match, pick the exact legacy error:
        a truly-missing row raises the same "not found" Exception as the file repo;
        a wrong-status row raises TaskLockFailed with the actual blocking status."""
        with self._connection() as conn, conn.cursor(row_factory=self._dict_row) as cur:
            cur.execute(cast("LiteralString", update_sql), params)
            row = cur.fetchone()
            if row and row["updated"] is not None:
                return
            prev = row["prev_status"] if row else None
            if prev is None:
                raise Exception(f"Task with id {task_id} not found")
            if kind == "lock":
                raise TaskLockFailed(f"Task {task_id} has already {prev}")
            if kind == "complete":
                raise TaskLockFailed(f"Task {task_id} has not been pending nor locked")
            if kind == "pending":
                raise TaskLockFailed(f"Task {task_id} is not completed")
            raise AssertionError(f"unknown kind {kind}")  # pragma: no cover

    def send_task(
        self,
        type: str,
        payload: TaskPayload,
        target_stage_id: str,
        source_stage_id: Optional[str],
        execution_id: Optional[str],
    ) -> TaskDTO:
        id = str(uuid4())
        created_at = self._now()
        with self._connection() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (id, type, status, target_stage_id, payload, "
                "created_at, created_by_execution, created_by_stage, db_updated_at) "
                "VALUES (%s, %s, 'pending', %s, %s, %s, %s, %s, now())",
                (
                    id,
                    type,
                    target_stage_id,
                    self._jsonb(payload),
                    created_at,
                    execution_id,
                    source_stage_id,
                ),
            )
        return TaskDTO(
            id=id,
            type=type,
            payload=payload,
            status="pending",
            target_stage_id=target_stage_id,
            created=TaskEventDetails(
                at=to_utc_iso_string(created_at),
                by_execution_id=execution_id,
                by_stage_id=source_stage_id,
            ),
            locked=None,
            completed=None,
        )

    def get_by_id(self, task_id: str) -> TaskDTO:
        with self._connection() as conn, conn.cursor(row_factory=self._dict_row) as cur:
            cur.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
            row = cur.fetchone()
            if row is None:
                raise Exception(f"Task with id {task_id} not found")
            return task_row_to_dto(row)

    def lock_task(
        self, task_id: str, execution_id: Optional[str], stage_id: Optional[str]
    ) -> None:
        sql = (
            "WITH prev AS (SELECT status FROM tasks WHERE id=%s), "
            "upd AS (UPDATE tasks SET status='locked', locked_at=%s, "
            "locked_by_execution=%s, locked_by_stage=%s, db_updated_at=now() "
            "WHERE id=%s AND status='pending' RETURNING id) "
            "SELECT (SELECT id FROM upd) AS updated, "
            "(SELECT status FROM prev) AS prev_status"
        )
        self._apply_transition(
            sql,
            (task_id, self._now(), execution_id, stage_id, task_id),
            task_id,
            "lock",
        )

    def complete_task(
        self, task_id: str, execution_id: Optional[str], stage_id: Optional[str]
    ) -> None:
        sql = (
            "WITH prev AS (SELECT status FROM tasks WHERE id=%s), "
            "upd AS (UPDATE tasks SET status='completed', completed_at=%s, "
            "completed_by_execution=%s, completed_by_stage=%s, db_updated_at=now() "
            "WHERE id=%s AND status IN ('pending','locked') RETURNING id) "
            "SELECT (SELECT id FROM upd) AS updated, "
            "(SELECT status FROM prev) AS prev_status"
        )
        self._apply_transition(
            sql,
            (task_id, self._now(), execution_id, stage_id, task_id),
            task_id,
            "complete",
        )

    def set_task_to_pending(self, task_id: str) -> None:
        sql = (
            "WITH prev AS (SELECT status FROM tasks WHERE id=%s), "
            "upd AS (UPDATE tasks SET status='pending', db_updated_at=now() "
            "WHERE id=%s AND status='completed' RETURNING id) "
            "SELECT (SELECT id FROM upd) AS updated, "
            "(SELECT status FROM prev) AS prev_status"
        )
        self._apply_transition(sql, (task_id, task_id), task_id, "pending")

    def _list(self, sql: str, params: list) -> List[TaskDTO]:
        with self._connection() as conn, conn.cursor(row_factory=self._dict_row) as cur:
            # Query structure is built only from fixed fragments; values go through
            # params. cast satisfies psycopg's LiteralString typing.
            cur.execute(cast("LiteralString", sql), params)
            return [task_row_to_dto(row) for row in cur.fetchall()]

    def get_pending_tasks(
        self, stage_id: str, limit: Union[int, None], offset: int, where: Dict
    ) -> List[TaskDTO]:
        where_sql, where_params = self._where_clauses(where)
        # id DESC tie-break makes pagination deterministic (created_at can tie).
        sql = (
            "SELECT * FROM tasks WHERE target_stage_id=%s AND status='pending'"
            + where_sql
            + " ORDER BY created_at DESC, id DESC "
        )
        params: list = [stage_id, *where_params]
        if limit is None:
            sql += "OFFSET %s"
            params.append(offset)
        else:
            sql += "LIMIT %s OFFSET %s"
            params.extend([limit, offset])
        return self._list(sql, params)

    def get_sent_tasks(
        self, stage_id: str, limit: Union[int, None], offset: int, where: Dict
    ) -> List[TaskDTO]:
        where_sql, where_params = self._where_clauses(where)
        sql = (
            "SELECT * FROM tasks WHERE created_by_stage=%s"
            + where_sql
            + " ORDER BY created_at DESC, id DESC "
        )
        params: list = [stage_id, *where_params]
        if limit is None:
            sql += "OFFSET %s"
            params.append(offset)
        else:
            sql += "LIMIT %s OFFSET %s"
            params.extend([limit, offset])
        return self._list(sql, params)

    def get_stage_tasks(self, stage_id: str) -> List[TaskDTO]:
        return self._list(
            "SELECT * FROM tasks WHERE target_stage_id=%s "
            "ORDER BY created_at DESC, id DESC",
            [stage_id],
        )

    def get_all_tasks(self) -> List[TaskDTO]:
        return self._list("SELECT * FROM tasks ORDER BY created_at DESC, id DESC", [])

    def get_execution_sent_tasks(self, execution_id: str) -> List[TaskDTO]:
        return self._list(
            "SELECT * FROM tasks WHERE created_by_execution=%s",
            [execution_id],
        )

    def set_locked_tasks_to_pending(self, execution_id: str) -> None:
        with self._connection() as conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET status='pending', db_updated_at=now() "
                "WHERE locked_by_execution=%s AND status='locked'",
                (execution_id,),
            )

    def clear(self):
        with self._connection() as conn, conn.cursor() as cur:
            cur.execute("TRUNCATE tasks")


class ProductionTasksRepository(TasksRepository):
    def __init__(self, client: "HTTPClient") -> None:
        self.client = client

    def send_task(
        self,
        type: str,
        payload: TaskPayload,
        target_stage_id: str,
        source_stage_id: Optional[str],
        execution_id: Optional[str],
    ) -> TaskDTO:
        r = self.client.post(
            endpoint="/tasks",
            json={
                "type": type,
                "payload": payload,
                "targetStageId": target_stage_id,
                "sourceStageId": source_stage_id,
                "createdBy": execution_id,
            },
        )

        r.raise_for_status()

        task = r.json()
        return TaskDTO(**task["dto"])

    def lock_task(
        self, task_id: str, execution_id: Optional[str], stage_id: Optional[str]
    ) -> None:
        r = self.client.patch(
            endpoint=f"/tasks/{task_id}",
            json=CloudApiCliTasksUpdateTaskRequest(
                status="locked",
                locked=CloudApiConsoleWorkflowUpdateTaskRequestLocked(
                    at=datetime.datetime.now(datetime.timezone.utc),
                    by_execution_id=execution_id,
                    by_stage_id=stage_id,
                ),
            ).to_dict(),
        )

        if r.status_code == 409:
            raise TaskLockFailed(f"Task {task_id} has already been locked")

        r.raise_for_status()

    def complete_task(
        self, task_id: str, execution_id: Optional[str], stage_id: Optional[str]
    ) -> None:
        r = self.client.patch(
            endpoint=f"/tasks/{task_id}",
            json=CloudApiCliTasksUpdateTaskRequest(
                status="completed",
                completed=CloudApiConsoleWorkflowUpdateTaskRequestCompleted(
                    at=datetime.datetime.now(datetime.timezone.utc),
                    by_execution_id=execution_id,
                    by_stage_id=stage_id,
                ),
            ).to_dict(),
        )

        if r.status_code == 409:
            raise TaskLockFailed(f"Task {task_id} has already been completed")

        r.raise_for_status()

    def set_task_to_pending(self, task_id: str) -> None:
        r = self.client.patch(
            endpoint=f"/tasks/{task_id}",
            json=CloudApiCliTasksUpdateTaskRequest(status="pending").to_dict(),
        )

        if r.status_code == 409:
            raise TaskLockFailed(f"Task {task_id} is not completed")

        r.raise_for_status()

    def get_pending_tasks(
        self, stage_id: str, limit: Union[int, None], offset: int, where: Dict
    ) -> List[TaskDTO]:
        r = self.client.get(
            endpoint="/tasks",
            params={
                "stageId": stage_id,
                "status": ["pending"],
                "sentBy": None,
                "limit": limit,
                "offset": offset,
                "where": json.dumps(where),
            },
        )
        r.raise_for_status()
        tasks = r.json()["tasks"]
        return [TaskDTO(**task) for task in tasks]

    def get_sent_tasks(
        self, stage_id: str, limit: Union[int, None], offset: int, where: Dict
    ) -> List[TaskDTO]:
        r = self.client.get(
            endpoint="/tasks",
            params={
                "stageId": None,
                "status": [],
                "sentBy": stage_id,
                "limit": limit,
                "offset": offset,
                "where": json.dumps(where),
            },
        )
        r.raise_for_status()
        tasks = r.json()["tasks"]
        return [TaskDTO(**task) for task in tasks]

    def get_stage_tasks(self, stage_id: str) -> List[TaskDTO]:
        r = self.client.get(
            endpoint="/tasks",
            params={"stageId": stage_id},
        )
        r.raise_for_status()
        tasks = r.json()["tasks"]
        return [TaskDTO(**task) for task in tasks]

    def get_by_id(self, task_id: str) -> TaskDTO:
        r = self.client.get(
            endpoint=f"/tasks/{task_id}",
        )
        r.raise_for_status()
        task = r.json()
        return TaskDTO(**task)

    def get_all_tasks(self) -> List[TaskDTO]:
        raise NotImplementedError()

    def get_execution_sent_tasks(self, execution_id: str) -> List[TaskDTO]:
        raise NotImplementedError()

    def set_locked_tasks_to_pending(self, execution_id: str) -> None:
        r = self.client.patch(
            endpoint="/tasks",
            json={"executionId": execution_id},
        )

        r.raise_for_status()

    def clear(self):
        raise NotImplementedError()
