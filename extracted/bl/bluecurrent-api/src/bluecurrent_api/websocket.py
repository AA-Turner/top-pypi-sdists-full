"""Define an object that handles the connection to the Websocket"""

import json
from asyncio import Event, timeout
import logging
from typing import Any, cast
from collections.abc import Callable, Coroutine

from websockets.asyncio.client import ClientConnection, connect
from websockets.exceptions import (
    ConnectionClosedError,
    InvalidStatus,
    WebSocketException,
)

from .exceptions import (
    AlreadyConnected,
    InvalidApiToken,
    RequestLimitReached,
    WebsocketError,
)
from .utils import (
    get_exception,
    handle_charge_points,
    handle_grid,
    handle_session_messages,
    handle_setting_change,
    handle_settings,
    handle_status,
)

URL = "wss://motown.bluecurrent.nl/haserver"
BUTTONS = ("START_SESSION", "STOP_SESSION", "SOFT_RESET", "REBOOT")
LOGGER = logging.getLogger(__package__)


class Websocket:
    """Class for handling requests and responses for the BlueCurrent Websocket Api."""

    def __init__(self) -> None:
        self.conn: ClientConnection | None = None
        self.auth_token: str | None = None
        self.connected = Event()
        self.received_charge_points = Event()

    async def start(
        self,
        receiver: Callable[[dict[str, Any]], Coroutine[Any, Any, None]],
        on_open: Callable[[], Coroutine[Any, Any, None]],
    ) -> None:
        """Opens the connection"""

        if not self.auth_token:
            raise WebsocketError("token not validated.")

        try:
            await self._loop(receiver, on_open)
        except WebSocketException as err:
            self.raise_correct_exception(err)

    async def _loop(
        self,
        receiver: Callable[[dict[str, Any]], Coroutine[Any, Any, None]],
        on_open: Callable[[], Coroutine[Any, Any, None]],
    ) -> None:
        """listens for incoming messages"""
        async with connect(URL) as websocket:
            try:
                LOGGER.debug("connected")
                self.conn = websocket
                self.connected.set()
                await on_open()
                async for message in websocket:
                    await self._message_handler(json.loads(message), receiver)
            except WebSocketException as err:
                self.conn = None
                self.connected.clear()
                self.received_charge_points.set()
                self.received_charge_points.clear()
                self.raise_correct_exception(err)

    async def _send_recv_single_message(self, message_object: dict) -> dict:
        """Send and recv single message."""
        message = json.dumps(message_object)
        try:
            async with connect(URL) as websocket:
                await websocket.send(message)
                async with timeout(5):
                    res = await websocket.recv()
                    return cast(dict, json.loads(res))
        except WebSocketException as err:
            self.raise_correct_exception(err)
            # unreachable since raise_correct_exception will always return an error
            # added for type hints.
            return {}

    async def validate_api_token(self, api_token: str) -> str:
        """Validate an api token."""
        res = await self._send_recv_single_message(
            {"command": "VALIDATE_API_TOKEN", "token": api_token}
        )

        if res["object"] == "ERROR":
            raise get_exception(res)

        if not res.get("success"):
            raise InvalidApiToken()

        self.auth_token = "Token " + res["token"]
        return cast(str, res["customer_id"])

    async def get_email(self) -> str:
        """Return the user email"""
        if not self.auth_token:
            raise WebsocketError("token not set")

        res = await self._send_recv_single_message(
            {"command": "GET_ACCOUNT", "Authorization": self.auth_token}
        )

        if res["object"] == "ERROR":
            raise get_exception(res)

        if not res.get("login"):
            raise WebsocketError("No email found")
        return cast(str, res["login"])

    async def send_request(self, request: dict[str, Any]) -> None:
        """Add authorization and send request."""

        if not self.auth_token:
            raise WebsocketError("Token not set")

        await self.connected.wait()

        request["Authorization"] = self.auth_token
        await self._send(request)

    async def _message_handler(
        self,
        message: dict[str, Any],
        receiver: Callable[[dict[str, Any]], Coroutine[Any, Any, None]],
    ) -> None:
        """Handle message and pass to receiver."""

        object_name = message.get("object")

        if not object_name:
            raise WebsocketError("Received message has no object.")

        LOGGER.debug("Received %s", object_name)

        # handle ERROR object
        if object_name == "ERROR":
            raise get_exception(message)

        # if object other than ERROR has an error key it will be sent to the receiver.
        error = message.get("error")

        # ignored objects
        if (
            ("RECEIVED" in object_name and not error)
            or object_name == "HELLO"
            or "OPERATIVE" in object_name
        ):
            return

        if object_name == "CHARGE_POINTS":
            handle_charge_points(message)
        elif object_name == "CH_STATUS":
            handle_status(message)
        elif object_name == "CH_SETTINGS":
            handle_settings(message)
        elif object_name == "CHARGE_CARDS":
            pass
        elif "GRID" in object_name:
            handle_grid(message)
        elif object_name in (
            "STATUS_SET_PUBLIC_CHARGING",
            "STATUS_SET_PLUG_AND_CHARGE",
        ):
            handle_setting_change(message)
        elif any(button in object_name for button in BUTTONS):
            handle_session_messages(message)
        else:
            return

        await receiver(message)

        if object_name == "CHARGE_POINTS":
            self.received_charge_points.set()

    async def _send(self, data: dict[str, Any]) -> None:
        """Send data to the websocket."""
        if self.conn:
            LOGGER.debug("Sending %s.", data["command"])
            data_str = json.dumps(data)
            await self.conn.send(data_str)
        else:
            raise WebsocketError("Connection is closed.")

    async def disconnect(self) -> None:
        """Disconnect from de websocket."""
        if not self.conn:
            raise WebsocketError("Connection is already closed.")
        await self.conn.close()

    @staticmethod
    def raise_correct_exception(err: Exception) -> None:
        """Check if the client was rejected by the server"""

        if isinstance(err, InvalidStatus):
            reason = err.response.headers.get("x-websocket-reject-reason")
            if reason is not None:
                if "Request limit reached" in reason:
                    raise RequestLimitReached("Request limit reached") from err
                if "Already connected" in reason:
                    raise AlreadyConnected("Already connected")
        if isinstance(err, ConnectionClosedError):
            if err.rcvd and err.rcvd.code == 4001:
                raise RequestLimitReached("Request limit reached") from err

        raise WebsocketError from err
