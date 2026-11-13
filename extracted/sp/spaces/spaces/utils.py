"""
"""
from functools import partial

import multiprocessing
import pickle as pkl
import socket
import tempfile
from multiprocessing.queues import SimpleQueue as _SimpleQueue
from pickle import PicklingError
from threading import Thread
from typing import Any
from typing import Callable
from typing import Generic
from typing import TypeVar

from typing_extensions import ParamSpec


GRADIO_VERSION_ERROR_MESSAGE = "Make sure Gradio version is at least 3.46"


T = TypeVar('T')
P = ParamSpec('P')


class SimpleQueue(_SimpleQueue[T]):
    def __init__(self, *args):
        super().__init__(*args, ctx=multiprocessing.get_context('fork'))
    def put(self, obj: T):
        try:
            super().put(obj)
        except PicklingError:
            raise # pragma: no cover
        # https://bugs.python.org/issue29187
        except Exception as e:
            # Always assume a PicklingError
            raise PicklingError from e
    def wlock_release(self):
        if (lock := getattr(self, '_wlock', None)) is None:
            return # pragma: no cover
        try:
            lock.release()
        except ValueError:
            pass


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
