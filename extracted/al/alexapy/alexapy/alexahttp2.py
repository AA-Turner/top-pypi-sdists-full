"""Python Package for controlling Alexa devices (echo dot, etc) programmatically.

SPDX-License-Identifier: Apache-2.0

Websocket library.

This library is based on MIT code from https://github.com/Apollon77/alexa-remote.

For more details about this api, please refer to the documentation at
https://gitlab.com/keatontaylor/alexapy
"""

import asyncio
import contextlib
import datetime
import json
import logging
import ssl
from collections.abc import Callable, Coroutine
from typing import Any

import certifi
import httpx

from alexapy.const import HTTP2_AUTHORITY, HTTP2_DEFAULT
from alexapy.errors import AlexapyLoginError

from .alexalogin import AlexaLogin


def _create_ssl_context():
    """Create SSL context."""
    context = ssl.create_default_context(
        purpose=ssl.Purpose.SERVER_AUTH, cafile=certifi.where()
    )
    return context


_SSL_CONTEXT = _create_ssl_context()
_LOGGER = logging.getLogger(__name__)


class HTTP2EchoClient:
    """HTTP2 Client Class for Echo Devices.

    Based on code from openHAB:
    https://github.com/Apollon77/alexa-remote/blob/bc687b9e36da7c2318c56b4e1bec677c7198dbd4/alexa-http2push.js
    """

    def __init__(
        self,
        login: AlexaLogin,
        msg_callback: Callable[[Any], Coroutine[Any, Any, None]],
        open_callback: Callable[[], Coroutine[Any, Any, None]],
        close_callback: Callable[[], Coroutine[Any, Any, None]],
        error_callback: Callable[[str], Coroutine[Any, Any, None]],
        loop: asyncio.AbstractEventLoop | None = None,
        *,
        read_timeout: float | None = 300,
    ) -> None:
        """Init for threading and HTTP2 Push Connection.

        Args:
            login: Authenticated AlexaLogin whose session opens the
                directives stream.
            msg_callback: Coroutine invoked with each directive message
                parsed from the stream.
            open_callback: Coroutine invoked once the HTTP2 stream has been
                accepted and opened.
            close_callback: Coroutine invoked when the stream is closed.
            error_callback: Coroutine invoked with an error message when the
                connection fails.
            loop: Event loop to schedule tasks on; defaults to the running
                loop when omitted.
            read_timeout: Maximum seconds to wait between chunks of data on
                the directives stream before treating the connection as stale
                and closing it. A healthy stream carries multipart keepalive
                traffic well inside this window; a stream that has gone silent
                without a transport-level close delivers nothing and would
                otherwise hang forever without any error. Pass None to disable
                the check (previous behavior).
        """
        assert login.session is not None
        if read_timeout is not None and read_timeout <= 0:
            raise ValueError("read_timeout must be positive or None")
        self._options = {
            "method": "GET",
            "path": "/v20160207/directives",
            "authority": HTTP2_AUTHORITY.get(
                login.url.replace("amazon", ""), HTTP2_DEFAULT
            ),
            "scheme": "https",
            "authorization": f"Bearer {login.access_token}",
        }
        self.open_callback: Callable[[], Coroutine[Any, Any, None]] = open_callback
        self.msg_callback: Callable[[Any], Coroutine[Any, Any, None]] = msg_callback
        self.close_callback: Callable[[], Coroutine[Any, Any, None]] = close_callback
        self.error_callback: Callable[[str], Coroutine[Any, Any, None]] = error_callback
        self._http2url: str = (
            f"https://{self._options['authority']}{self._options['path']}"
        )
        self.client = httpx.AsyncClient(http2=True, verify=_SSL_CONTEXT)
        self.boundary: str = ""
        self._login = login
        self._loop: asyncio.AbstractEventLoop = (
            loop if loop else asyncio.get_event_loop()
        )
        self._last_ping = datetime.datetime(1, 1, 1)
        self._last_activity: datetime.datetime | None = None
        self._read_timeout = read_timeout
        self._tasks = set()
        self._opened: asyncio.Event = asyncio.Event()
        self._closing: bool = False

    @property
    def last_activity(self) -> datetime.datetime | None:
        """Return when data last arrived on the directives stream.

        Any traffic counts, including multipart keepalive boundaries, not
        only parsed directives. None until the first chunk arrives.
        """
        return self._last_activity

    async def async_run(self) -> None:
        """Start Async WebSocket Listener.

        This method returns only after the HTTP2 stream is verified as open
        (i.e., the server accepted the request and `open_callback` has been
        invoked), or if the connection fails.
        """
        process_task = self._loop.create_task(self.process_messages())
        process_task.add_done_callback(self.on_close)
        self._tasks.add(process_task)

        ping_task = self._loop.create_task(self.manage_pings())
        ping_task.add_done_callback(self.on_close)
        self._tasks.add(ping_task)

        open_wait_task = self._loop.create_task(self._opened.wait())
        try:
            done, _pending = await asyncio.wait(
                {process_task, open_wait_task},
                timeout=15,
                return_when=asyncio.FIRST_COMPLETED,
            )

            # If the message task finishes before we ever mark the connection open,
            # treat that as a failed connection attempt.
            if process_task in done and not self._opened.is_set():
                exc = process_task.exception()
                if exc:
                    raise exc
                raise AlexapyLoginError("HTTP2 stream closed before opening")

            if not self._opened.is_set():
                raise AlexapyLoginError("HTTP2 open timeout")
        finally:
            if not open_wait_task.done():
                open_wait_task.cancel()

    async def process_messages(self) -> None:
        """Start Async WebSocket Listener."""
        _LOGGER.debug("Starting message parsing loop.")
        _LOGGER.debug("Connecting to %s with %s", self._http2url, self._options)
        try:
            async with self.client.stream(
                self._options["method"],
                self._http2url,
                headers={
                    "authorization": self._options["authorization"],
                },
                # Never time out the overall stream, but bound the gap between
                # chunks: the server sends keepalive boundaries continuously,
                # so a long silent gap means the connection is dead even if
                # the transport still looks open.
                timeout=httpx.Timeout(None, read=self._read_timeout),
            ) as response:
                # Validate the stream was accepted before reporting "open" upstream.
                if response.status_code in (401, 403):
                    body = (await response.aread()).decode(errors="ignore")
                    msg = body or f"HTTP2 status {response.status_code}"
                    _LOGGER.debug("HTTP2 login error: %s", msg)
                    self.on_close("HTTP2 unauthorized (401/403)")
                    await self.handle_login_error(msg)
                    return

                if not self._opened.is_set():
                    _LOGGER.debug(
                        "HTTP2 directives stream accepted (status=%s)",
                        response.status_code,
                    )
                    await self.async_on_open()
                    self._opened.set()

                async for data in response.aiter_text():
                    await self.on_message(data)
        except httpx.RemoteProtocolError as exception_:
            # Remote terminated the stream.
            self.on_close(f"Disconnect detected: {exception_}")

            # If we never reached "open", treat as a failed connect.
            if not self._opened.is_set():
                raise

            # Otherwise, normal disconnect.
            return
        except httpx.ReadTimeout:
            # No data (not even keepalives) inside the read window: the
            # stream has gone silent without a transport-level close. Handle
            # it so the consumer reconnects instead of hanging forever.
            _LOGGER.debug(
                "HTTP2 stream silent for %ss; closing stale connection",
                self._read_timeout,
            )

            # If we never reached "open", propagate so the caller waiting on
            # open sees a failed connect. The shared finally below still
            # notifies close once, as it does for the other error paths.
            if not self._opened.is_set():
                raise

            # Otherwise, treat like a normal disconnect so reconnect runs.
            self.on_close(f"HTTP2 stream silent for {self._read_timeout}s")
            return
        except Exception as exception_:
            # Surface unexpected failures so callers waiting for open can fail fast.
            _LOGGER.debug("HTTP2 exception: %s", exception_)
            self.on_close(f"HTTP2 exception: {exception_}")
            raise
        finally:
            # Ensure we always notify close if the stream ends cleanly.
            if not self._closing:
                self.on_close("HTTP2 stream ended")

    async def on_message(self, message: str) -> None:
        """Handle New Message."""
        reauth_required = "Unable to authenticate the request. Please provide a valid authorization token."  # noqa: E501
        _LOGGER.debug("Received raw message: %s", message)
        self._last_activity = datetime.datetime.now(datetime.UTC)
        for line in message.splitlines():
            if line.startswith("------"):
                if not self.boundary:  # set boundary character
                    self.boundary = line
            elif line.startswith(reauth_required):
                _LOGGER.debug("HTTP2 login error: %s", message)
                await self.handle_login_error("HTTP2 Message Parsing reauth")
            elif line.startswith("Content-Type:"):
                continue
            elif line and not line.startswith(self.boundary):
                with contextlib.suppress(json.decoder.JSONDecodeError):
                    self._schedule(self.msg_callback(json.loads(line)))

    def _schedule(self, coro: Coroutine[Any, Any, Any]) -> None:
        """Schedule a coroutine on the target loop safely."""
        try:
            running = asyncio.get_running_loop()
        except RuntimeError:
            running = None
        if running and running == self._loop:
            self._loop.create_task(coro)
        else:
            asyncio.run_coroutine_threadsafe(coro, self._loop)

    def on_error(self, error: str = "Unspecified") -> None:
        """Handle HTTP2 Error."""
        _LOGGER.debug("HTTP2 Error: %s", error)
        self._schedule(self.error_callback(error))

    def on_close(self, _future: object | None = None) -> None:
        """Handle HTTP2 Close."""
        if self._closing:
            return
        self._closing = True

        _LOGGER.debug("HTTP2 Connection Closed.")
        try:
            for task in list(self._tasks):
                if task.done():
                    exc = task.exception()
                    if exc:
                        self.on_error(str(exc))
                else:
                    task.remove_done_callback(self.on_close)
                    task.cancel()
        except BaseException:
            pass

        # Close the underlying client to ensure sockets are released.
        self._schedule(self.client.aclose())

        # Notify upstream that the connection is closed.
        self._schedule(self.close_callback())

    async def async_on_open(self) -> None:
        """Handle Async WebSocket Open."""
        await self.open_callback()

    async def manage_pings(self) -> None:
        """Manage Pings."""
        while not self._closing:
            await self.ping()
            await asyncio.sleep(299)

    async def ping(self) -> None:
        """Ping."""
        url = f"https://{self._options['authority']}/ping"
        _LOGGER.debug("Preparing ping to %s", url)
        response = await self.client.get(
            url,
            headers={
                "authorization": self._options["authorization"],
            },
        )
        self._last_ping = datetime.datetime.now()
        _LOGGER.debug(
            "Received response: %s:%s",
            response.status_code,
            response.text,
        )
        if response.status_code in (401, 403):
            _LOGGER.debug("Detected ping 401/403")
            await self.handle_login_error(response.text)

    async def handle_login_error(self, message: str = "") -> None:
        """Handle login error.

        Attempt to relogin otherwise raise login error.
        """
        if not await self._login.test_loggedin():
            raise AlexapyLoginError(message)

    async def test_close(self, delay: int = 30, raise_exception: bool = False) -> None:
        """Test close."""
        await asyncio.sleep(delay)
        if raise_exception:
            raise AlexapyLoginError(f"Raised exception after {delay}")
