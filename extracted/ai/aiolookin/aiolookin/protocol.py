"""The lookin integration protocol."""
from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import re
import socket
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Final

from aiohttp import ClientSession, ClientTimeout, ServerDisconnectedError

from .const import (
    COMMAND_TO_CODE,
    DEVICE_INFO_URL,
    DEVICES_INFO_URL,
    INFO_URL,
    MEDIA_SOURCE_INFO_URL,
    METEO_SENSOR_URL,
    SEND_IR_COMMAND,
    SEND_IR_COMMAND_PRONTOHEX,
    SEND_IR_COMMAND_RAW,
    UPDATE_CLIMATE_URL,
)
from .error import NoUsableService
from .models import (
    Climate,
    Device,
    MediaSource,
    MeteoSensor,
    Remote,
    UDPCommand,
    UDPCommandType,
    UDPEvent,
)

if TYPE_CHECKING:
    from aiohttp import ClientResponse

LOOKIN_PORT: Final = 61201

UDP_PATTERN = re.compile(
    r"LOOK([^:]+):(?P<command>[^!]+)!(?P<device_id>[^:]+):(?P<type_code>[^:]+):(?P<data>[^:].*)"
)

CLIENT_TIMEOUTS: Final = ClientTimeout(total=9, connect=8, sock_connect=7, sock_read=7)

LOGGER = logging.getLogger(__name__)


class IRFormat(Enum):
    Raw = "raw"
    ProntoHEX = "prontohex"


def validate_response(response: "ClientResponse") -> None:
    if response.status not in (200, 201, 204):
        raise NoUsableService


class LookinUDPSubscriptions:
    """Store Lookin subscriptions."""

    def __init__(self) -> None:
        """Init and store callbacks."""
        self._loop = asyncio.get_event_loop()
        self._event_callbacks: dict[
            tuple[str, UDPCommandType, str | None], list[Callable]
        ] = {}

    def subscribe_event(
        self,
        device_id: str,
        command_type: UDPCommandType,
        uuid: str | None,
        callback: Callable,
    ) -> Callable:
        """Subscribe to lookin sensor updates."""
        self._event_callbacks.setdefault((device_id, command_type, uuid), []).append(
            callback
        )

        def _remove_call(*_: Any) -> None:
            self._event_callbacks[(device_id, command_type, uuid)].remove(callback)

        return _remove_call

    def notify_event(self, event: UDPEvent) -> None:
        """Notify subscribers of a sensor update."""
        LOGGER.debug("Received sensor push updates: %s", event)
        for callback in self._event_callbacks.get(
            (event.device_id, event.type, event.uuid), []
        ):
            if asyncio.iscoroutinefunction(callback):
                asyncio.create_task(callback(event))
            else:
                callback(event)


class LookinUDPProtocol:
    """Implements Lookin UDP Protocol."""

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        subscriptions: LookinUDPSubscriptions,
        device_id: str,
    ) -> None:
        """Create Lookin UDP Protocol."""
        self.loop = loop
        self.subscriptions = subscriptions
        self._device_id = device_id
        self.transport: asyncio.DatagramTransport | None = None

    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        """Connect or reconnect to the device."""
        self.transport = transport

    def datagram_received(self, data: bytes, addr: Any) -> None:
        """Process incoming state changes."""
        LOGGER.debug("Received datagram: %s", data)

        if not (lookin_event := self._parse_event(data=data)):
            return

        if lookin_event.type == UDPCommandType.unknown:
            return

        self.subscriptions.notify_event(lookin_event)

    def error_received(self, exc: Exception) -> None:
        """Ignore errors."""
        return

    def connection_lost(self, exc: Exception) -> None:
        """Ignore connection lost."""
        return

    def stop(self) -> None:
        """Stop the client."""
        if self.transport:
            self.transport.close()

    @staticmethod
    def _parse_event(data: bytes) -> UDPEvent | None:
        decoded_data = data.decode()

        if not (match := UDP_PATTERN.match(decoded_data)):
            return None
        command = match.group("command").lower()
        device_id = match.group("device_id")
        type_code = match.group("type_code")
        data_package = match.group("data")

        if command == UDPCommand.updated.value:
            return UDPEvent(
                device_id=device_id,
                commnd=UDPCommand.updated,
                type_code=type_code,
                data_package=data_package,
            )

        return None


def _create_udp_socket() -> socket.socket:
    """Create a udp listener socket."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    with contextlib.suppress(Exception):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind(("", LOOKIN_PORT))
    sock.setblocking(False)
    return sock


async def start_lookin_udp(
    subscriptions: LookinUDPSubscriptions, device_id: str
) -> Callable:
    """Create the socket and protocol."""
    loop = asyncio.get_event_loop()
    _, protocol = await loop.create_datagram_endpoint(
        lambda: LookinUDPProtocol(loop, subscriptions, device_id),  # type: ignore
        sock=_create_udp_socket(),
    )
    return protocol.stop


class LookInHttpProtocol:
    def __init__(self, api_uri: str, session: ClientSession) -> None:
        self._api_uri = api_uri
        self._session = session

    async def _request(self, method: str, url: str, **kwargs: Any) -> "ClientResponse":  # type: ignore
        """Handle a request that may need to retry on disconnect."""
        for attempt in range(2):
            try:
                return await self._session.request(
                    method=method, url=url, timeout=CLIENT_TIMEOUTS, **kwargs
                )
            except ServerDisconnectedError as ex:
                LOGGER.debug(
                    "Server disconnected on attempt %s while calling %s: %s",
                    attempt,
                    url,
                    ex,
                )
                if attempt == 0:
                    continue
                raise

    async def _get(self, url: str) -> "ClientResponse":
        """Handle a get that may need to retry on disconnect."""
        return await self._request("GET", url)

    async def _post(self, url: str, data: Any) -> "ClientResponse":
        """Handle a get that may need to retry on disconnect."""
        return await self._request("POST", url, data=data)

    async def get_info(self) -> Device:
        response = await self._get(url=f"{self._api_uri}{INFO_URL}")
        validate_response(response)
        payload = await response.json()

        return Device(_data=payload)

    async def update_device_name(self, name: str) -> None:
        response = await self._post(
            url=f"{self._api_uri}{INFO_URL}", data=json.dumps({"name": name})
        )
        validate_response(response)

    async def get_meteo_sensor(self) -> MeteoSensor:
        response = await self._get(url=f"{self._api_uri}{METEO_SENSOR_URL}")

        validate_response(response)
        payload = await response.json()

        return MeteoSensor(_data=payload)

    async def get_devices(self) -> list[dict[str, Any]]:
        response = await self._get(url=f"{self._api_uri}{DEVICES_INFO_URL}")

        validate_response(response)
        payload = await response.json()

        return payload

    async def get_device(self, uuid: str) -> dict[str, Any]:
        url = f"{self._api_uri}{DEVICE_INFO_URL}"
        response = await self._get(
            url=url.format(uuid=uuid),
        )

        validate_response(response)
        payload = await response.json()

        return payload

    async def get_conditioner(self, uuid: str) -> Climate:
        payload = await self.get_device(uuid=uuid)
        return Climate(_data=payload)

    async def get_remote(self, uuid: str) -> Remote:
        payload = await self.get_device(uuid=uuid)
        return Remote(_data=payload)

    async def send_command(self, uuid: str, command: str, signal: str) -> None:
        if not (code := COMMAND_TO_CODE.get(command)):
            raise ValueError(f"{command} this is the invalid command")

        url = f"{self._api_uri}{SEND_IR_COMMAND}"
        response = await self._get(
            url=url.format(uuid=uuid, command=code, signal=signal),
        )

        validate_response(response)

    async def send_ir(self, ir_format: IRFormat, codes: str) -> None:
        if ir_format == IRFormat.ProntoHEX:
            url = f"{self._api_uri}{SEND_IR_COMMAND_PRONTOHEX}"
        elif ir_format == IRFormat.Raw:
            url = f"{self._api_uri}{SEND_IR_COMMAND_RAW}"
        else:
            raise ValueError(f"{ir_format} is not a known IRFormat")
        response = await self._get(url=url.format(codes=codes))

        validate_response(response)

    async def update_conditioner(self, uuid: str, status: str) -> None:
        """Update the conditioner from a Climate object."""
        url = f"{self._api_uri}{UPDATE_CLIMATE_URL}"
        response = await self._get(
            url=url.format(uuid=uuid, status=status),
        )

        validate_response(response)

    async def get_media_sources(self, uuid: str) -> list[MediaSource]:
        url = f"{self._api_uri}{MEDIA_SOURCE_INFO_URL}"
        response = await self._get(
            url=url.format(uuid=uuid),
        )

        validate_response(response)
        payload = await response.json()

        signals = payload.get("Signals")

        return [MediaSource(signal) for signal in signals]
