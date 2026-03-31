from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from multiprocessing.connection import Connection

    from abstra_internals.entities.execution_context import ClientContext
    from abstra_internals.repositories.project.project import StageWithFile


class ExecutorCommand(str, Enum):
    WARMUP = "warmup"
    EXECUTE = "execute"
    RUN_SNIPPET = "run_snippet"
    SHUTDOWN = "shutdown"


@dataclass
class WarmupRequest:
    command: ExecutorCommand = ExecutorCommand.WARMUP


@dataclass
class ExecuteRequest:
    command: ExecutorCommand
    worker_id: str
    execution_id: str
    stage: StageWithFile
    request: ClientContext
    connection: Optional[Connection]
    rabbitmq_params: Optional[RabbitMQParams]
    user_jwt: Optional[str] = None


@dataclass
class RunSnippetRequest:
    command: ExecutorCommand
    code: str
    worker_id: str
    title: str = "Debug Snippet"


@dataclass
class ShutdownRequest:
    command: ExecutorCommand = ExecutorCommand.SHUTDOWN


@dataclass
class RabbitMQParams:
    connection_uri: str
    execution_id: str
    send_queue: Optional[str] = None
    recv_queue: Optional[str] = None
    queue_expire_ms: Optional[int] = None


@dataclass
class ExecutorResponse:
    success: bool
    execution_id: Optional[str] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    logs: Optional[List[Dict[str, str]]] = None
