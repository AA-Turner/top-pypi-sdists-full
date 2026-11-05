"""Take a request's open files over SCM_RIGHTS (plan D20): asyncio's line reader drops ancillary data,
so a request that names `fds: N` is answered by pausing that reader, sending the `fds.ready` event,
and reading the caller's one fd message on a dup of the socket. Then the reader resumes."""

from __future__ import annotations

import asyncio
import contextlib
import os
import socket

from probe.foundation.service_api.wire import FDS_READY_TOPIC, MAX_FDS, Method, event, invalid_params

#: The methods that take fds (`cli.run` joins them with A2).
FD_METHODS = frozenset({Method.API_CALL, Method.FILES_HASH})
#: What a caller has to send its fds after `fds.ready`.
FDS_WAIT_S = 10.0


def need_fd_count(method: str, value: object) -> int:
    """The number of fds a request says follow it: 1 to MAX_FDS, for an FD_METHODS method."""
    if method not in FD_METHODS:
        raise invalid_params(f"{method} takes no fds")
    if not isinstance(value, int) or isinstance(value, bool) or not 0 < value <= MAX_FDS:
        raise invalid_params(f"fds must be a count of 1 to {MAX_FDS}")
    return value


async def receive_fds(writer: asyncio.StreamWriter, request_id: object, count: int) -> list[int]:
    """Exactly `count` fds from the caller of `writer`'s connection, sent after `fds.ready`;
    ConnectionError when it closes or sends another number, TimeoutError past FDS_WAIT_S. The
    caller owns (and closes) what this returns."""
    transport = writer.transport
    sock = writer.get_extra_info("socket")
    if sock is None or not hasattr(socket, "recv_fds"):
        raise ConnectionError("this connection cannot pass files")
    loop = asyncio.get_running_loop()
    # The reader is the transport's; its fd may not be watched twice: a dup is ours to watch.
    raw = socket.socket(fileno=os.dup(sock.fileno()))
    raw.setblocking(False)
    done: asyncio.Future = loop.create_future()

    def receive_now() -> None:
        if done.done():
            return
        try:
            data, fds, _flags, _addr = socket.recv_fds(raw, 16, count)
        except (BlockingIOError, InterruptedError):
            return
        except OSError as exc:
            done.set_exception(exc)
            return
        done.set_result((data, fds))

    transport.pause_reading()
    loop.add_reader(raw.fileno(), receive_now)
    try:
        writer.write(_encode_ready(request_id))
        await writer.drain()
        data, fds = await asyncio.wait_for(done, FDS_WAIT_S)
    finally:
        loop.remove_reader(raw.fileno())
        raw.close()
        if not transport.is_closing():
            transport.resume_reading()
    if not data or len(fds) != count:
        for fd in fds:
            with contextlib.suppress(OSError):
                os.close(fd)
        raise ConnectionError(f"expected {count} fds, got {len(fds)}")
    return list(fds)


def _encode_ready(request_id: object) -> bytes:
    from probe.foundation.service_api.wire import encode

    return encode(event(FDS_READY_TOPIC, {"id": request_id}))


def close_fds(fds: list[int]) -> None:
    for fd in fds:
        with contextlib.suppress(OSError):
            os.close(fd)
    fds.clear()
