"""Define an object to interact with the BlueCurrent websocket api."""

import logging
from datetime import timedelta
from typing import Any
from collections.abc import Callable, Coroutine
from dataclasses import asdict

from .utils import get_next_reset_delta, join_numbers_with_commas
from .types import OverrideCurrentPayload
from .websocket import Websocket

LOGGER = logging.getLogger(__package__)
DELAY = 10


class Client:
    """Api Client for the BlueCurrent Websocket Api."""

    def __init__(self) -> None:
        """Initialize the Client."""
        self.websocket = Websocket()

    def is_connected(self) -> bool:
        """Return the connection status"""
        return self.websocket.connected.is_set()

    async def wait_for_charge_points(self) -> None:
        """Wait for next response."""
        await self.websocket.received_charge_points.wait()

    async def validate_api_token(self, api_token: str) -> str:
        """Validate an api_token and return customer id."""
        return await self.websocket.validate_api_token(api_token)

    async def get_email(self) -> str:
        """Get user email."""
        return await self.websocket.get_email()

    async def _on_open(
        self,
        on_open: Callable[[], Coroutine[Any, Any, None]],
    ) -> None:
        """Send requests when connected."""
        await self.websocket.send_request(
            {
                "command": "HELLO",
                "header": "homeassistant",
            }
        )
        await on_open()

    def get_next_reset_delta(self) -> timedelta:
        """Returns the timedelta until the websocket limits are reset."""
        return get_next_reset_delta()

    async def connect(
        self,
        receiver: Callable[[dict[str, Any]], Coroutine[Any, Any, None]],
        on_open: Callable[[], Coroutine[Any, Any, None]],
    ) -> None:
        """Connect to the websocket."""
        await self.websocket.start(receiver, lambda: self._on_open(on_open))

    async def disconnect(self) -> None:
        """Disconnect the websocket."""
        await self.websocket.disconnect()

    async def get_charge_cards(self) -> None:
        """Get the charge cards."""
        await self.websocket.send_request({"command": "GET_CHARGE_CARDS", "limit": 100})

    async def get_charge_points(self) -> None:
        """Get the charge points."""
        request = self._create_request("GET_CHARGE_POINTS")
        await self.websocket.send_request(request)

    async def get_status(self, evse_id: str) -> None:
        """Get the status of a charge point."""
        request = self._create_request("GET_CH_STATUS", evse_id=evse_id)
        await self.websocket.send_request(request)

    async def get_settings(self, evse_id: str) -> None:
        """Get the settings of a charge point."""
        request = self._create_request("GET_CH_SETTINGS", evse_id=evse_id)
        await self.websocket.send_request(request)

    async def get_grid_status(self, evse_id: str) -> None:
        """Get the grid status of a charge point."""
        request = self._create_request("GET_GRID_STATUS", evse_id=evse_id)
        await self.websocket.send_request(request)

    async def set_linked_charge_cards_only(self, evse_id: str, value: bool) -> None:
        """Set public_charging of a charge point to a value."""
        request = self._create_request(
            "SET_PUBLIC_CHARGING", evse_id=evse_id, value=not value
        )
        await self.websocket.send_request(request)

    async def set_plug_and_charge(self, evse_id: str, value: bool) -> None:
        """Set plug_and_charge of a charge point to a value."""
        request = self._create_request(
            "SET_PLUG_AND_CHARGE", evse_id=evse_id, value=value
        )
        await self.websocket.send_request(request)

    async def block(self, evse_id: str, value: bool) -> None:
        """Set available of a charge point to a value."""
        command = "SET_OPERATIVE"
        if value is True:
            command = "SET_INOPERATIVE"
        request = self._create_request(command, evse_id=evse_id)
        await self.websocket.send_request(request)

    async def reset(self, evse_id: str) -> None:
        """Reset a charge point."""
        request = self._create_request("SOFT_RESET", evse_id=evse_id)
        await self.websocket.send_request(request)

    async def reboot(self, evse_id: str) -> None:
        """Reboot a charge point."""
        request = self._create_request("REBOOT", evse_id=evse_id)
        await self.websocket.send_request(request)

    async def start_session(self, evse_id: str, session_token: str) -> None:
        """Start a charge session at a charge point.
        session_token = card_uuid"""
        request = self._create_request(
            "START_SESSION", evse_id=evse_id, session_token=session_token
        )
        await self.websocket.send_request(request)

    async def stop_session(self, evse_id: str) -> None:
        """Stop a charge session at a charge point."""
        request = self._create_request("STOP_SESSION", evse_id=evse_id)
        await self.websocket.send_request(request)

    async def set_delayed_charging(self, evse_id: str, value: bool) -> None:
        """Turn smart charging profile on/off and set the profile to delayed charging."""
        request = self._create_request(
            "SET_DELAYED_CHARGING", evse_id=evse_id, value=value
        )
        await self.websocket.send_request(request)

    async def set_delayed_charging_settings(
        self, evse_id: str, days: list[int], start_time: str, end_time: str
    ) -> None:
        """Send the selected settings in order to schedule delayed charging."""
        days_str = join_numbers_with_commas(days)
        request = self._create_request(
            "SAVE_SCHEDULE_DELAYED_CHARGING",
            evse_id=evse_id,
            days=days_str,
            start_time=start_time,
            end_time=end_time,
        )
        await self.websocket.send_request(request)

    async def set_price_based_charging(self, evse_id: str, value: bool) -> None:
        """Turn smart charging profile on/off and set the profile to price based charging."""
        request = self._create_request(
            "SET_PRICE_BASED_CHARGING", evse_id=evse_id, value=value
        )
        await self.websocket.send_request(request)

    async def set_price_based_settings(
        self,
        evse_id: str,
        expected_departure_time: str,
        expected_kwh: float,
        minimum_kwh: float,
    ) -> None:
        """Set the price based charging settings."""
        request = self._create_request(
            "SET_PRICE_BASED_SETTINGS",
            evse_id=evse_id,
            expected_departure_time=expected_departure_time,
            expected_kwh=str(expected_kwh),
            minimum_kwh=str(minimum_kwh),
        )
        await self.websocket.send_request(request)

    async def override_price_based_charging_profile(
        self, evse_id: str, value: bool
    ) -> None:
        """Override the settings set up by the price based charging profile."""
        request = self._create_request(
            "OVERRIDE_CHARGING_PROFILES", evse_id=evse_id, value=value
        )
        await self.websocket.send_request(request)

    async def override_delayed_charging_profile(
        self, evse_id: str, value: bool
    ) -> None:
        """Override the timeout set by the delayed charging profile."""
        request = self._create_request(
            "OVERRIDE_DELAYED_CHARGING_TIMEOUT", evse_id=evse_id, value=value
        )
        await self.websocket.send_request(request)

    async def get_user_override_currents_list(self) -> None:
        """Get a list with current override values and scheduling data set by the user."""
        request = self._create_request("LIST_OVERRIDE_CURRENT")
        await self.websocket.send_request(request)

    async def set_user_override_current(self, payload: OverrideCurrentPayload) -> None:
        """
        Schedules an override of the electricity current that chargepoints are allowed
         to use when charging.

        Args:
            payload (OverrideCurrentPayload): The override configuration.
             See dataclass fields for details.

        Note: day fields in the payload(`overridestartdays`, `overridestopdays`) must use
        2-letter weekday codes:
        'MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'.
        """
        request = self._create_request("POST_SET_OVERRIDE_CURRENT", **asdict(payload))
        await self.websocket.send_request(request)

    async def clear_user_override_current(self, schedule_id: str) -> None:
        """Clears a previously set user override using the given schedule ID."""
        request = self._create_request(
            "POST_CLEAR_OVERRIDE_CURRENT", schedule_id=int(schedule_id)
        )
        await self.websocket.send_request(request)

    async def edit_user_override_current(
        self, schedule_id: str, payload: OverrideCurrentPayload
    ) -> None:
        """
        Lets the user edit a scheduled override of the electricity current that chargepoints
         are allowed to use when charging.

        Args:
            schedule_id (str): The schedule's ID which is it be edited.
            payload (OverrideCurrentPayload): The override configuration.
            See dataclass fields for details.

        Note: day fields in the payload (`overridestartdays`, `overridestopdays`) must use
        2-letter weekday codes:
        'MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'.
        """
        request = self._create_request(
            "POST_EDIT_OVERRIDE_CURRENT", schedule_id=schedule_id, **asdict(payload)
        )
        await self.websocket.send_request(request)

    def _create_request(self, command: str, **kwargs: Any) -> dict[str, Any]:
        """Creates the JSON for the websocket request."""
        request = {"command": command}
        request.update({k: v for k, v in kwargs.items() if v is not None})
        return request
