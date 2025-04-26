# -*- mode: python -*-
"""PdbSelect tests."""
from __future__ import unicode_literals

import io
import os
import socket

try:
    from test.support.socket_helper import find_unused_port
except ImportError:
    from test.support import find_unused_port

import pytest

from context import pdb_socket


def _server():
    port = find_unused_port()
    sock = socket.socket()
    sock.bind(("localhost", port))
    sock.listen(0)
    return (port, sock)


def _socketpair():
    """Fallback for missing `socket.socketpair`."""
    port, serv = _server()
    sock1 = socket.create_connection(("localhost", port))
    sock2, _ = serv.accept()
    return sock1, sock2


if not hasattr(socket, "socketpair"):
    socket.socketpair = _socketpair


@pytest.fixture()
def server():
    """Return a port and a socket server listening on that port."""
    return _server()


# TODO: test how trace function handles exceptions raised during normal runtime
