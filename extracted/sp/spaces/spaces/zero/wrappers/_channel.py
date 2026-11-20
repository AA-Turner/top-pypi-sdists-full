"""
"""
from __future__ import annotations

import pickle as pkl
import socket
from dataclasses import dataclass
from multiprocessing import Pipe
from multiprocessing.connection import Connection
from multiprocessing.reduction import ForkingPickler
from traceback import format_exception
from typing import Generic
from typing import TypeVar


T = TypeVar('T')
Send = TypeVar('Send')
Recv = TypeVar('Recv')


@dataclass
class Received(Generic[T]):
    value: T

@dataclass
class Failure:
    cause: Exception
    @property
    def traceback(self):
        return ''.join(format_exception(type(self.cause), self.cause, self.cause.__traceback__))

@dataclass
class PicklingFailure(Failure):
    pass

@dataclass
class UnpicklingFailure(Failure):
    pass

@dataclass
class Closed:
    """
    The other end is gone or one of the ends has been shut down
    """


class Channel(Generic[Send, Recv]):
    """
    One end of a bidirectional pipe between forked processes (the other one is a `Channel[Recv, Send]`)
    `send` and `recv` never raise: all possible outcomes are returned
    """

    def __init__(self, connection: Connection[bytes, bytes]):
        self.connection = connection

    @classmethod
    def pair(cls) -> tuple[Channel[Send, Recv], Channel[Recv, Send]]:
        local, remote = Pipe(duplex=True)
        return Channel(local), Channel(remote)

    def send(self, obj: Send):
        try:
            data = ForkingPickler.dumps(obj)
        except Exception as e:
            return PicklingFailure(e)
        try:
            self.connection.send_bytes(data)
        except OSError:
            return Closed()

    def recv(self):
        try:
            data = self.connection.recv_bytes()
        except (EOFError, OSError):
            return Closed()
        try:
            value: Recv = pkl.loads(data)
        except Exception as e:
            return UnpicklingFailure(e)
        return Received(value)

    def pending(self) -> bool:
        """
        Whether something is waiting to be received (unlike `Connection.poll`, a closed pipe is not)
        """
        with socket.fromfd(self.connection.fileno(), socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            try:
                return len(sock.recv(1, socket.MSG_PEEK | socket.MSG_DONTWAIT)) > 0
            except OSError:
                return False

    def shutdown(self, how: int = socket.SHUT_RDWR):
        """
        Unlike `close`, acts on the pipe itself: seen by both ends, whoever else holds them
        """
        with socket.fromfd(self.connection.fileno(), socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.shutdown(how)

    def close(self):
        self.connection.close()
