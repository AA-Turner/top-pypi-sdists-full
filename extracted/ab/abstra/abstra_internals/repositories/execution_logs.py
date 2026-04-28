import json
import os
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, TypedDict

from abstra_internals.cloud_api.http_client import HTTPClient
from abstra_internals.consts.filepaths import LOCAL_LOGS_DIR_PATH
from abstra_internals.logger import AbstraLogger
from abstra_internals.utils import serialize
from abstra_internals.utils.datetime import from_utc_iso_string, to_utc_iso_string


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
                created_at=datetime.now(),
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
