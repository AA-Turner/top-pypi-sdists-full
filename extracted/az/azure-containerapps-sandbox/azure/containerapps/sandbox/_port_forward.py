"""Owned synchronous WebSocket transport for ACA Sandboxes TCP forwarding."""

from __future__ import annotations

from collections.abc import Iterator
from threading import Lock, Timer
from typing import Any

from websockets.exceptions import ConnectionClosed, ConnectionClosedOK, InvalidHandshake, InvalidStatus
from websockets.sync.client import ClientConnection, connect

from azure.containerapps.sandbox._port_forward_helpers import (
    PortForwardError,
    _binary_payload,
    _check_control_message,
    _connection_options,
    _start_message,
    _validate_timeout,
)


class PortForwardSession:
    """Owned, context-managed binary TCP tunnel.

    Reads/iteration reassemble binary messages up to 1 MiB with bounded
    buffering; ``None`` is clean EOF, not ``b""``. One reader and one writer
    may operate concurrently. Use ``with`` or ``close()``; closing or timing
    out affects only this WebSocket, never the HTTP pipeline or credential.
    """

    def __init__(self, connection: ClientConnection) -> None:
        self._connection = connection
        self._closed = False
        self._close_lock = Lock()

    @property
    def closed(self) -> bool:
        """Whether the session has been closed or has reached EOF."""
        return self._closed

    def write(self, data: bytes | bytearray | memoryview) -> None:
        """Write raw TCP bytes in a binary message, including any zero bytes.

        :raises TypeError: If data is not bytes-like.
        :raises ValueError: If the session is already closed.
        :raises PortForwardError: If the connection closes during the write.
        """
        payload = _binary_payload(data)
        if self._closed:
            raise ValueError("Port-forward session is closed.")
        try:
            self._connection.send(payload)
        except ConnectionClosed as exc:
            self.close()
            raise PortForwardError("Port-forward connection closed during write.") from exc

    def read(self, *, timeout: float | None = None) -> bytes | None:
        """Read binary TCP data, returning ``None`` only at clean EOF.

        :keyword float timeout: Optional positive read timeout in seconds.
            A timeout closes the tunnel and raises ``TimeoutError``.
        :raises PortForwardError: On server errors, unexpected text, or
            abnormal WebSocket closure.
        """
        if timeout is not None:
            _validate_timeout(timeout, "timeout")
        if self._closed:
            return None
        try:
            message = self._connection.recv(timeout=timeout)
        except TimeoutError:
            self.close()
            raise
        except ConnectionClosedOK as exc:
            self.close()
            if exc.rcvd is None or exc.rcvd.code not in (1000, 1005):
                raise PortForwardError("Port-forward connection closed abnormally.") from exc
            return None
        except ConnectionClosed as exc:
            self.close()
            raise PortForwardError("Port-forward connection closed abnormally.") from exc
        if isinstance(message, bytes):
            return message
        try:
            _check_control_message(message, handshake=False)
        finally:
            self.close()
        raise PortForwardError("Expected binary port-forward data.")

    def close(self) -> None:
        """Gracefully close this tunnel; abort its socket at the close timeout."""
        with self._close_lock:
            if self._closed:
                return
            self._closed = True

        deadline = None
        if self._connection.close_timeout is not None:
            # A blocked send can hold the protocol lock before close's own timeout.
            deadline = Timer(self._connection.close_timeout, self._connection.close_socket)
            deadline.daemon = True
            try:
                deadline.start()
            except RuntimeError:
                self._connection.close_socket()
                raise
        try:
            self._connection.close()
        except BaseException:
            self._connection.close_socket()
            raise
        finally:
            if deadline is not None:
                deadline.cancel()
                deadline.join()

    def __enter__(self) -> PortForwardSession:
        if self._closed:
            raise ValueError("Port-forward session is closed.")
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __iter__(self) -> Iterator[bytes]:
        while (message := self.read()) is not None:
            yield message


def _open_port_forward(
    url: str,
    token: str,
    port: int,
    *,
    connect_timeout: float,
    handshake_timeout: float,
    close_timeout: float,
) -> PortForwardSession:
    # The sync connector rejects non-101 responses, including all redirects.
    try:
        connection = connect(
            url,
            **_connection_options(
                token,
                connect_timeout=connect_timeout,
                close_timeout=close_timeout,
            ),
        )
    except InvalidStatus as exc:
        raise PortForwardError(f"WebSocket upgrade failed (HTTP {exc.response.status_code}).") from exc
    except TimeoutError:
        raise
    except (InvalidHandshake, OSError) as exc:
        raise PortForwardError("Unable to open port-forward WebSocket.") from exc
    session = PortForwardSession(connection)
    try:
        connection.send(_start_message(port))
        _check_control_message(connection.recv(timeout=handshake_timeout), handshake=True)
        return session
    except ConnectionClosed as exc:
        session.close()
        raise PortForwardError("Port-forward connection closed before connected.") from exc
    except BaseException:
        session.close()
        raise
