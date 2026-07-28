from dataclasses import dataclass, field
from multiprocessing.connection import Connection
from typing import List, Optional

from abstra_internals.entities.execution_context import ClientContext
from abstra_internals.utils.serializable import Serializable


class PreExecution(Serializable):
    stage_id: str
    context: ClientContext
    execution_id: str
    user_jwt: Optional[str] = None
    send_queue: Optional[str] = None
    recv_queue: Optional[str] = None
    queue_expire_ms: Optional[int] = None


class ControlMessage(Serializable):
    type: str
    correlation_id: Optional[str] = None


class StopExecutionPayload(Serializable):
    execution_id: str


class RunSnippetPayload(Serializable):
    code: str
    title: str = "Debug Snippet"
    # Packages the snippet needs, installed into the isolated Smart Chat overlay
    # (never the project's requirements.txt).
    requirements: List[str] = field(default_factory=list)


class StopExecutionMessage(ControlMessage):
    type: str = "stop"
    payload: StopExecutionPayload

    @staticmethod
    def create(execution_id: str) -> "StopExecutionMessage":
        return StopExecutionMessage(
            payload=StopExecutionPayload(execution_id=execution_id),
        )


class StopAllExecutionsMessage(ControlMessage):
    type: str = "stop_all"


class RunSnippetMessage(ControlMessage):
    type: str = "run_snippet"
    payload: RunSnippetPayload
    connection: Optional[Connection] = field(default=None, metadata={"exclude": True})

    @staticmethod
    def create(
        code: str,
        title: str = "Debug Snippet",
        requirements: Optional[List[str]] = None,
    ) -> "RunSnippetMessage":
        return RunSnippetMessage(
            payload=RunSnippetPayload(
                code=code, title=title, requirements=requirements or []
            ),
        )


class RunSnippetSandboxedMessage(ControlMessage):
    type: str = "run_snippet_sandboxed"
    payload: RunSnippetPayload
    connection: Optional[Connection] = field(default=None, metadata={"exclude": True})
    # Publisher's reply-queue x-expires; the worker must redeclare with the exact
    # same value or RabbitMQ 406s (see consumer._send_snippet_result).
    queue_expire_ms: Optional[int] = None
    # Execution budget; worker kills at this point, cloud-api waits past it.
    # None → worker's own hard cap.
    timeout_ms: Optional[int] = None

    @staticmethod
    def create(
        code: str,
        title: str = "Debug Snippet",
        queue_expire_ms: Optional[int] = None,
        timeout_ms: Optional[int] = None,
        requirements: Optional[List[str]] = None,
    ) -> "RunSnippetSandboxedMessage":
        return RunSnippetSandboxedMessage(
            payload=RunSnippetPayload(
                code=code, title=title, requirements=requirements or []
            ),
            queue_expire_ms=queue_expire_ms,
            timeout_ms=timeout_ms,
        )


class PingMessage(ControlMessage):
    type: str = "ping"


@dataclass
class QueueMessage:
    preexecution: PreExecution
    delivery_tag: int
    redelivered: bool = False
    connection: Optional[Connection] = None  # For local execution only


@dataclass
class ControlQueueMessage:
    message: ControlMessage
    delivery_tag: int
    redelivered: bool = False
    connection: Optional[Connection] = None
