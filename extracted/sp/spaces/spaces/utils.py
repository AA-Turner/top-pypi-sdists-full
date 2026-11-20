"""
"""
from functools import partial

import pickle as pkl
import socket
import tempfile
from threading import Thread
from typing import Any
from typing import Callable
from typing import Generic
from typing import TypeVar

from typing_extensions import ParamSpec


GRADIO_VERSION_ERROR_MESSAGE = "Make sure Gradio version is at least 3.46"


T = TypeVar('T')
P = ParamSpec('P')


class ShmFdQueue(Generic[T]):
    def __init__(self):
        self._rx, self._tx = socket.socketpair(socket.AF_UNIX, socket.SOCK_DGRAM)

    def close(self): # pragma: no cover
        self._rx.close()
        self._tx.close()

    def get(self) -> T:
        _, (fd,), _, _ = socket.recv_fds(self._rx, 1, 1)
        with open(fd, "rb") as f:
            f.seek(0)
            return pkl.load(f)

    def put(self, obj: T):
        with tempfile.TemporaryFile(dir="/dev/shm") as f:
            pkl.dump(obj, f)
            f.flush()
            socket.send_fds(self._tx, [b"\0"], [f.fileno()])


def drop_params(fn: Callable[[], T]) -> Callable[..., T]:
    def drop(*args):
        return fn()
    return drop


debug = partial(print, 'SPACES_ZERO_GPU_DEBUG')


# Type-safe threads
def create_thread(fn: Callable[P, Any], *args: P.args, **kwargs: P.kwargs) -> Thread:
    return Thread(target=fn, args=args, kwargs=kwargs)

def create_thread_daemon(fn: Callable[P, Any], *args: P.args, **kwargs: P.kwargs) -> Thread:
    return Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
