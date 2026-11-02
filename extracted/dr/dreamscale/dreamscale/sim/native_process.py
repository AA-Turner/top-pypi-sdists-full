"""Bounded IPC between trusted local simulator parent/child processes.

Never use these pickle messages for model responses or network inputs.
"""

from __future__ import annotations

import pickle
import select
import struct
import time

MAX_MESSAGE_BYTES = 16 * 1024 * 1024


def read_message(stream, *, timeout_s=None):
    deadline = None if timeout_s is None else time.monotonic() + timeout_s

    def read_exact(length):
        data = bytearray()
        while len(data) < length:
            if deadline is not None:
                remaining = deadline - time.monotonic()
                if remaining <= 0 or not select.select([stream], [], [], remaining)[0]:
                    raise TimeoutError("Native simulator did not respond in time")
            block = stream.read(length - len(data))
            if not block:
                raise EOFError("simulator pipe closed")
            data.extend(block)
        return data

    header = read_exact(4)
    if not header:
        raise EOFError("simulator pipe closed")
    if len(header) != 4:
        raise EOFError("incomplete simulator header")
    length = struct.unpack("!I", header)[0]
    if not 0 < length <= MAX_MESSAGE_BYTES:
        raise ValueError("invalid simulator message size")
    return pickle.loads(read_exact(length))


def write_message(stream, value):
    data = pickle.dumps(value, protocol=5)
    if len(data) > MAX_MESSAGE_BYTES:
        raise ValueError("simulator message too large")
    stream.write(struct.pack("!I", len(data)))
    stream.write(data)
    stream.flush()
