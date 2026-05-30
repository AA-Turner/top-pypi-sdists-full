from dataclasses import dataclass
from multiprocessing.connection import Connection
from typing import Optional

from pydantic import ConfigDict, Field

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
    model_config = ConfigDict(arbitrary_types_allowed=True)

    type: str = "run_snippet"
    payload: RunSnippetPayload
    connection: Optional[Connection] = Field(default=None, exclude=True)

    @staticmethod
    def create(code: str, title: str = "Debug Snippet") -> "RunSnippetMessage":
        return RunSnippetMessage(
            payload=RunSnippetPayload(code=code, title=title),
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
    connection: Optional[Connection] = None
