"""Main DoorBirdPy module."""

from __future__ import annotations
import aiohttp
import re
import asyncio
from typing import Any
from contextlib import suppress
from typing import Callable
from urllib.parse import urlencode
from functools import cached_property
from aiohttp.client import ClientSession
from tenacity import retry, wait_exponential, stop_before_delay

from doorbirdpy.schedule_entry import (
    DoorBirdScheduleEntry,
    DoorBirdScheduleEntryOutput,
    DoorBirdScheduleEntrySchedule,
)

__all__ = [
    "DoorBird",
    "DoorBirdScheduleEntry",
    "DoorBirdScheduleEntryOutput",
    "DoorBirdScheduleEntrySchedule",
]

_retry_kwargs = dict(wait=wait_exponential(min=1, max=10), stop=stop_before_delay(60), reraise=True)


class DoorBird:
    """Represent a doorbell unit."""

    _monitor_timeout = 45  # seconds to wait for a monitor update
    _monitor_max_failures = 4

    def __init__(
        self,
        ip: str,
        username: str,
        password: str,
        http_session: ClientSession | None = None,
        secure: bool = False,
        port: int | None = None,
        timeout: float = 10.0,
    ) -> None:
        """
        Initializes the options for subsequent connections to the unit.

        :param ip: The IP address of the unit
        :param username: The username (with sufficient privileges) of the unit
        :param password: The password for the provided username
        :param secure: set to True to use https instead of http for URLs
        :param port: override the HTTP port (defaults to 443 if secure = True, otherwise 80)
        :param timeout: The timeout for the HTTP requests
        """
        self._ip = ip
        self._credentials = username, password
        self._http = http_session or ClientSession()
        self._secure = secure
        self._timeout = timeout

        if port:
            self._port = port
        else:
            self._port = 443 if self._secure else 80

        self._monitor_task: asyncio.Task[None] | None = None

    async def close(self) -> None:
        """
        Close the connection to the device.
        """
        if self._http:
            await self._http.close()

    async def get_image(self, url: str, timeout: float | None = None) -> bytes:
        """
        Perform a GET request to the given URL on the device
        and return the raw image data.

        :param url: The full URL to the API call
        :param timeout: The timeout for the request
        :return: The response object
        """
        response = await self._http.get(url, timeout=timeout or self._timeout)
        response.raise_for_status()
        return await response.read()

    async def _get(
        self, url: str, timeout: float | None = None
    ) -> aiohttp.ClientResponse:
        """
        Perform a GET request to the given URL on the device.

        :param url: The full URL to the API call
        :param timeout: The timeout for the request
        :return: The response object
        """
        return await self._http.get(url, timeout=timeout or self._timeout)

    async def ready(self) -> tuple[bool, int]:
        """
        Test the connection to the device.

        :return: A tuple containing the ready status (True/False) and the HTTP
        status code returned by the device or 0 for no status
        """
        url = self._url("/bha-api/info.cgi", auth=True)
        try:
            response = await self._get(url)
            data = await response.json()
            code = data["BHA"]["RETURNCODE"]
            return int(code) == 1, int(response.status)
        except ValueError:
            return False, int(response.status)

    @cached_property
    def live_video_url(self) -> str:
        """
        A multipart JPEG live video stream with the default resolution and
        compression as defined in the system configuration.

        :return: The URL of the stream
        """
        return self._url("/bha-api/video.cgi")

    @cached_property
    def live_image_url(self) -> str:
        """
        A JPEG file with the default resolution and compression as
        defined in the system configuration.

        :return: The URL of the image
        """
        return self._url("/bha-api/image.cgi")

    @retry(**_retry_kwargs)
    async def energize_relay(self, relay: int | str = 1) -> bool:
        """
        Energize a door opener/alarm output/etc relay of the device.

        :return: True if OK, False if not
        """
        data = await self._get_json(
            self._url("/bha-api/open-door.cgi", {"r": relay}, auth=True)
        )
        return int(data["BHA"]["RETURNCODE"]) == 1

    @retry(**_retry_kwargs)
    async def turn_light_on(self) -> bool:
        """
        Turn on the IR lights.

        :return: JSON
        """
        data = await self._get_json(self._url("/bha-api/light-on.cgi", auth=True))
        code = data["BHA"]["RETURNCODE"]
        return int(code) == 1

    def history_image_url(self, index: int, event: str) -> str:
        """
        A past image stored in the cloud.

        :param index: Index of the history images, where 1 is the latest history image
        :return: The URL of the image.
        """
        return self._url("/bha-api/history.cgi", {"index": index, "event": event})

    async def schedule(self) -> list[DoorBirdScheduleEntry]:
        """
        Get schedule settings.

        :return: A list of DoorBirdScheduleEntry objects
        """
        data = await self._get_json(self._url("/bha-api/schedule.cgi", auth=True))
        return DoorBirdScheduleEntry.parse_all(data)

    async def get_schedule_entry(
        self, sensor: str, param: str = ""
    ) -> DoorBirdScheduleEntry:
        """
        Find the schedule entry that matches the provided sensor and parameter
        or create a new one that does if none exists.

        :return: A DoorBirdScheduleEntry
        """
        entries = await self.schedule()

        for entry in entries:
            if entry.input == sensor and entry.param == param:
                return entry

        return DoorBirdScheduleEntry(sensor, param)

    @retry(**_retry_kwargs)
    async def change_schedule(self, entry: DoorBirdScheduleEntry) -> tuple[bool, int]:
        """
        Add or replace a schedule entry.

        :param entry: A DoorBirdScheduleEntry object to replace on the device
        :return: A tuple containing the success status (True/False) and the HTTP response code
        """
        url = self._url("/bha-api/schedule.cgi", auth=True)
        response = await self._http.post(
            url,
            json=entry.export,
            timeout=self._timeout,
            headers={"Content-Type": "application/json"},
        )
        return int(response.status) == 200, response.status

    @retry(**_retry_kwargs)
    async def delete_schedule(self, event: str, param: str = "") -> bool:
        """
        Delete a schedule entry.

        :param event: Event type (doorbell, motion, rfid, input)
        :param param: param value of schedule entry to delete
        :return: True if OK, False if not
        """
        url = self._url(
            "/bha-api/schedule.cgi",
            {"action": "remove", "input": event, "param": param},
            auth=True,
        )
        response = await self._get(url)
        return int(response.status) == 200

    async def _monitor_doorbird(
        self, on_event: Callable[[str], None], on_error: Callable[[Exception], None]
    ) -> None:
        """
        Method to use by the monitoring thread
        """
        url = self._url(
            "/bha-api/monitor.cgi", {"ring": "doorbell,motionsensor"}, auth=True
        )
        states = {"doorbell": "L", "motionsensor": "L"}
        failures = 0

        while True:
            try:
                response = await self._http.get(url, timeout=self._monitor_timeout)
                reader = aiohttp.MultipartReader.from_response(response)
                while True:
                    if (part := await reader.next()) is None:
                        break
                    if not isinstance(part, aiohttp.BodyPartReader):
                        continue
                    line = await part.text(encoding="utf-8")
                    failures = 0  # reset the failure count on each successful response
                    if match := re.match(r"(doorbell|motionsensor):(H|L)", line):
                        event, value = match.group(1), match.group(2)
                        if states[event] != value:
                            states[event] = value
                            if value == "H":
                                on_event(event)

            except Exception as e:
                if failures >= self._monitor_max_failures:
                    return on_error(e)

                failures += 1
                await asyncio.sleep(2**failures)

    async def start_monitoring(
        self, on_event: Callable[[str], None], on_error: Callable[[Exception], None]
    ) -> None:
        """
        Start monitoring for doorbird events

        :param on_event: A callback function, which takes the event name as its only parameter.
        The possible events are "doorbell" and "motionsensor"
        :param on_error: An error function, which will be called with an error if the thread fails.
        """
        if self._monitor_task:
            await self.stop_monitoring()
        self._monitor_task = asyncio.create_task(
            self._monitor_doorbird(on_event, on_error)
        )

    async def stop_monitoring(self) -> None:
        """
        Stop monitoring for doorbird events
        """
        if not self._monitor_task:
            return

        self._monitor_task.cancel()
        with suppress(asyncio.CancelledError):
            await self._monitor_task
        self._monitor_task = None

    async def doorbell_state(self) -> bool:
        """
        The current state of the doorbell.

        :return: True for pressed, False for idle
        """
        url = self._url("/bha-api/monitor.cgi", {"check": "doorbell"}, auth=True)
        response = await self._get(url)
        response.raise_for_status()

        try:
            return int((await response.text()).split("=")[1]) == 1
        except IndexError:
            return False

    async def motion_sensor_state(self) -> bool:
        """
        The current state of the motion sensor.

        :return: True for motion, False for idle
        """
        url = self._url("/bha-api/monitor.cgi", {"check": "motionsensor"}, auth=True)
        response = await self._get(url)
        response.raise_for_status()

        try:
            return int((await response.text()).split("=")[1]) == 1
        except IndexError:
            return False

    async def info(self) -> dict[str, Any]:
        """
        Get information about the device.

        .. note:

           Unlike other API calls, this will not automatically be retried if it fails.

        :return: A dictionary of the device information:
        - FIRMWARE
        - BUILD_NUMBER
        - WIFI_MAC_ADDR (if the device is connected via WiFi)
        - RELAYS list (if firmware version >= 000108)
        - DEVICE-TYPE (if firmware version >= 000108)
        """
        url = self._url("/bha-api/info.cgi", auth=True)
        response = await self._get(url)
        response.raise_for_status()
        data = await response.json()
        return data["BHA"]["VERSION"][0]

    async def favorites(self) -> dict[str, dict[str, Any]]:
        """
        Get all saved favorites.

        :return: dict, as defined by the API.
        Top level items will be the favorite types (http, sip),
        which each reference another dict that maps ID
        to a dict with title and value keys.
        """
        return await self._get_json(self._url("/bha-api/favorites.cgi", auth=True))

    @retry(**_retry_kwargs)
    async def change_favorite(
        self, fav_type: str, title: str, value: str, fav_id: str | None = None
    ) -> bool:
        """
        Add a new saved favorite or change an existing one.

        :param fav_type: sip or http
        :param title: Short description
        :param value: URL including protocol and credentials
        :param fav_id: The ID of the favorite, only used when editing existing favorites
        :return: successful, True or False
        """
        args: dict[str, Any] = {
            "action": "save",
            "type": fav_type,
            "title": title,
            "value": value,
        }

        if fav_id:
            args["id"] = int(fav_id)

        url = self._url("/bha-api/favorites.cgi", args, auth=True)
        response = await self._get(url)
        return int(response.status) == 200

    @retry(**_retry_kwargs)
    async def delete_favorite(self, fav_type: str, fav_id: str) -> bool:
        """
        Delete a saved favorite.

        :param fav_type: sip or http
        :param fav_id: The ID of the favorite
        :return: successful, True or False
        """
        url = self._url(
            "/bha-api/favorites.cgi",
            {"action": "remove", "type": fav_type, "id": fav_id},
            auth=True,
        )

        response = await self._get(url)
        return int(response.status) == 200

    @retry(**_retry_kwargs)
    async def restart(self) -> bool:
        """
        Restart the device.

        :return: successful, True or False
        """
        url = self._url("/bha-api/restart.cgi")
        response = await self._get(url)
        return int(response.status) == 200

    @cached_property
    def rtsp_live_video_url(self) -> str:
        """
        Live video request over RTSP.

        :return: The URL for the MPEG H.264 live video stream
        """
        return self._url("/mpeg/media.amp", port=554, protocol="rtsp")

    @cached_property
    def rtsp_over_http_live_video_url(self) -> str:
        """
        Live video request using RTSP over HTTP.

        :return: The URL for the MPEG H.264 live video stream
        """
        return self._url("/mpeg/media.amp", port=8557, protocol="rtsp")

    @cached_property
    def html5_viewer_url(self) -> str:
        """
        The HTML5 viewer for interaction from other platforms.

        :return: The URL of the viewer
        """
        return self._url("/bha-api/view.html")

    def _url(
        self,
        path: str,
        args: dict[str, Any] | None = None,
        port: int | None = None,
        auth: bool = True,
        protocol: str | None = None,
    ) -> str:
        """
        Create a URL for accessing the device.

        :param path: The endpoint to call
        :param args: A dictionary of query parameters
        :param port: The port to use (defaults to 80)
        :param auth: Set to False to remove the URL authentication
        :param protocol: Allow protocol override (defaults to "http")
        :return: The full URL
        """
        if not port:
            port = self._port

        if not protocol:
            protocol = "https" if self._secure else "http"

        query = urlencode(args) if args else ""

        if auth:
            user = ":".join(self._credentials)
            url = f"{protocol}://{user}@{self._ip}:{port}{path}"
        else:
            url = f"{protocol}://{self._ip}:{port}{path}"

        if query:
            url = f"{url}?{query}"

        return url

    async def _get_json(self, url: str) -> dict:
        """
        Perform a GET request to the given URL on the device.

        :param url: The full URL to the API call
        :return: The JSON-decoded data sent by the device
        """
        response = await self._get(url)
        response.raise_for_status()
        return await response.json()
