"""
Type stubs for Vortex producer client.
"""

from __future__ import annotations

import threading
from enum import Enum
from queue import Queue
from typing import Optional

import google.protobuf.message
import requests
from dbtlabs.proto.public.v1.events.vortex_pb2 import VortexMessage, VortexMessageBatch

class ErrorMode(Enum):
    LOG_AND_CONTINUE = "log_and_continue"
    LOG_AND_RAISE = "log_and_raise"

def log_proto(
    message: google.protobuf.message.Message,
    error_mode: ErrorMode = ErrorMode.LOG_AND_CONTINUE,
    wait_seconds: float = 0.0,
) -> None: ...
def shutdown(timeout_seconds: float = 10.0) -> None: ...

class VortexProducerClient:
    queue: Queue[Optional[VortexMessage]]
    thread: threading.Thread
    initialized: bool
    queue_closed: bool
    logs_suppressed: bool

    @classmethod
    def log_proto(
        cls,
        message: google.protobuf.message.Message,
        error_mode: ErrorMode = ErrorMode.LOG_AND_CONTINUE,
        wait_seconds: float = 0.0,
    ) -> None: ...
    @classmethod
    def shutdown(cls, timeout_seconds: float = 10.0) -> None: ...
    @classmethod
    def _initialize(cls, max_queue_size: int = 10000) -> None: ...
    @classmethod
    def _reset(cls) -> None: ...
    @classmethod
    def _send_proto(cls, message: VortexMessageBatch) -> requests.Response: ...
    @classmethod
    def _worker(cls) -> None: ...
