"""Owned asyncio WebSocket transport for ACA Sandboxes TCP forwarding."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from typing import Any

from websockets.asyncio.client import ClientConnection, connect
from websockets.exceptions import ConnectionClosed, ConnectionClosedOK, InvalidHandshake, InvalidStatus

from azure.containerapps.sandbox._port_forward_helpers import (
    PortForwardError,
    _binary_payload,
    _check_control_message,
    _connection_options,
    _start_message,
    _validate_timeout,
)


class _NoRedirectConnect(connect):
    def process_redirect(self, exc: Exception) -> Exception:
        # Never replay the authenticated upgrade, even to a same-origin URL.
        return exc


class PortForwardSession:
    """Owned, async-context-managed binary TCP tunnel.

    Reads/async iteration reassemble messages up to 1 MiB with bounded
    buffering; ``None`` is clean EOF, not ``b""``. One reader and one writer
    may operate concurrently. Use ``async with`` or await ``close()``.
    Cancellation/timeouts close only this WebSocket, never the HTTP pipeline
    or credential, before propagating the exception.
    """

    def __init__(self, connection: ClientConnection) -> None:
        self._connection = connection
        self._closed = False

    @property
    def closed(self) -> bool:
        """Whether the session has been closed or has reached EOF."""
        return self._closed

    async def write(self, data: bytes | bytearray | memoryview) -> None:
        """Write bytes-like data as a binary message, preserving zero bytes.

        :raises TypeError: If data is not bytes-like.
        :raises ValueError: If the session is already closed.
        :raises PortForwardError: If the connection closes during the write.
        """
        payload = _binary_payload(data)
        if self._closed:
            raise ValueError("Port-forward session is closed.")
        try:
            await self._connection.send(payload)
        except asyncio.CancelledError:
            await self.close()
            raise
        except ConnectionClosed as exc:
            await self.close()
            raise PortForwardError("Port-forward connection closed during write.") from exc

    async def read(self, *, timeout: float | None = None) -> bytes | None:
        """Read binary data, or ``None`` at clean EOF.

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
            async with asyncio.timeout(timeout):
                message = await self._connection.recv()
        except asyncio.CancelledError:
            await self.close()
            raise
        except TimeoutError:
            await self.close()
            raise
        except ConnectionClosedOK as exc:
            await self.close()
            if exc.rcvd is None or exc.rcvd.code not in (1000, 1005):
                raise PortForwardError("Port-forward connection closed abnormally.") from exc
            return None
        except ConnectionClosed as exc:
            await self.close()
            raise PortForwardError("Port-forward connection closed abnormally.") from exc
        if isinstance(message, bytes):
            return message
        try:
            _check_control_message(message, handshake=False)
        finally:
            await self.close()
        raise PortForwardError("Expected binary port-forward data.")

    async def close(self) -> None:
        """Close only this tunnel, idempotently, within its close timeout."""
        if not self._closed:
            self._closed = True
            try:
                await self._connection.close()
            except BaseException:
                # Cancellation must not leave a socket or keepalive task alive.
                self._connection.transport.abort()
                raise

    async def __aenter__(self) -> PortForwardSession:
        if self._closed:
            raise ValueError("Port-forward session is closed.")
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def __aiter__(self) -> AsyncIterator[bytes]:
        while (message := await self.read()) is not None:
            yield message


async def _open_port_forward(
    url: str,
    token: str,
    port: int,
    *,
    connect_timeout: float,
    handshake_timeout: float,
    close_timeout: float,
) -> PortForwardSession:
    try:
        connection = await _NoRedirectConnect(
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
        async with asyncio.timeout(handshake_timeout):
            await connection.send(_start_message(port))
            _check_control_message(await connection.recv(), handshake=True)
        return session
    except ConnectionClosed as exc:
        await session.close()
        raise PortForwardError("Port-forward connection closed before connected.") from exc
    except BaseException:
        await session.close()
        raise
