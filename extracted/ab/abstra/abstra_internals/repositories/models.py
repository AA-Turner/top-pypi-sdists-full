from dataclasses import dataclass
from multiprocessing.connection import Connection
from typing import Optional

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


@dataclass
class QueueMessage:
    preexecution: PreExecution
    delivery_tag: int
    connection: Optional[Connection] = None  # For local execution only


class ControlMessage(Serializable):
    type: str
    payload: dict


@dataclass
class ControlQueueMessage:
    message: ControlMessage
    delivery_tag: int
