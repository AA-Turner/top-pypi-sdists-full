"""
"""

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Callable
from typing import Iterable
from typing import Literal
from typing import TypedDict
from uuid import UUID

from .types import Picklable


class GlobalContext:
    server_ports: dict[UUID, int] = {}


class ZeroGPULog(TypedDict):
    title: str
    message: str
    level: Literal['info', 'warning', 'success']


def log_emitter_default(log: ZeroGPULog):
    print(f"ZeroGPU {log['level']}: {log['message']}")


class WorkerContextualizerDefault:
    def __init__(self):
        pass
    def __call__(self):
        pass


class ConnectionState:
    def __init__(self) -> None:
        self.alive = True


class ZeroGPUContext:
    def __init__(
        self,
        log_emitter: Callable[[ZeroGPULog], None] | None = None,
        worker_contextualizer: Callable[[], Picklable[Callable[[], None]]] | None = None,
        disconnect_detector: Callable[[], bool] | None = None,
        connection_state: ConnectionState | None = None,
        server_ports: Iterable[int] | None = None,
        headers: dict[str, str] | None = None,
    ):
        self.log_emitter = log_emitter or log_emitter_default
        self.worker_contextualizer = worker_contextualizer or WorkerContextualizerDefault
        self.disconnect_detector = disconnect_detector
        self.connection_state = connection_state
        self.server_ports = set(server_ports) if server_ports is not None else set()
        self.headers = headers or {}

    def info(self, title: str, message: str):
        self.log_emitter(ZeroGPULog(title=title, message=message, level='info'))

    def warning(self, title: str, message: str):
        self.log_emitter(ZeroGPULog(title=title, message=message, level='warning'))

    def success(self, title: str, message: str):
        self.log_emitter(ZeroGPULog(title=title, message=message, level='success'))

    def get_server_ports(self):
        return self.server_ports | set(GlobalContext.server_ports.values())

    def disconnected(self):
        if self.disconnect_detector is not None: # pragma: no cover
            return self.disconnect_detector()
        if self.connection_state is not None:
            return not self.connection_state.alive
        return False


_context_var: ContextVar[ZeroGPUContext] = ContextVar('zerogpu_context', default=ZeroGPUContext())


def get():
    return _context_var.get()


@contextmanager
def set_context_var(value: ZeroGPUContext):
    token = _context_var.set(value)
    try:
        yield
    finally:
        _context_var.reset(token)
