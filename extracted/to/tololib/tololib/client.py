"""TOLO Client."""

from __future__ import annotations

import logging
import socket
from select import select
from time import time
from typing import Any, Generator, Tuple

from .const import DEFAULT_PORT, DEFAULT_RETRY_COUNT, DEFAULT_RETRY_TIMEOUT, KEEP_ALIVE
from .enums import AromaTherapySlot, Command, LampMode
from .message import Message
from .state import ToloSettings, ToloStatus

logger = logging.getLogger(__name__)


class ToloCommunicationError(BaseException):
    pass


class ToloClient(object):
    def __init__(
        self,
        address: str,
        port: int = DEFAULT_PORT,
        retry_timeout: float = DEFAULT_RETRY_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
    ):
        self._address = address
        self._port = port
        self._retry_timeout = retry_timeout
        self._retry_count = retry_count
        self._socket: socket.socket | None = None

        self._socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self._socket.settimeout(self._retry_timeout)

    @property
    def address(self) -> str:
        return self._address

    @property
    def port(self) -> int:
        return self._port

    @property
    def retry_timeout(self) -> float:
        return self._retry_timeout

    @property
    def retry_count(self) -> int:
        return self._retry_count

    def get_status(self) -> ToloStatus:
        """
        Return the full status of the TOLO device.

        :return: Current status of the TOLO device.
        """
        response = self._communicate(Message(Command.GET_STATUS, b"\x11", b"\xff"))
        return ToloStatus.from_bytes(response.extra)

    def get_settings(self) -> ToloSettings:
        """
        Return the settings of a TOLO device.

        :return: Current settings of the TOLO device.
        """
        response = self._communicate(Message(Command.GET_SETTINGS, b"\x08", b"\xff"))
        return ToloSettings.from_bytes(response.extra)

    def set_power_on(self, power_on: bool) -> bool:
        """
        Power the TOLO device on or off.

        :param power_on: New power state of the TOLO device (on or off).
        :return: Success of the set operation.
        """
        return self._send_set_command(Command.SET_POWER_ON, power_on)

    def set_fan_on(self, fan_on: bool) -> bool:
        """
        Power the fan controlled by the TOLO device on or off.

        :param fan_on: New power state of the fan controlled by the TOLO device (on or off).
        :return: Success of the set operation.
        """
        return self._send_set_command(Command.SET_FAN_ON, fan_on)

    def set_aroma_therapy_on(self, aroma_therapy_on: bool) -> bool:
        """
        Enable or disable aroma therapy.

        If enabled, aroma pump will be activated every 5 minutes for 5 seconds.
        These values are hardcoded by the TOLO device and cannot be changed.

        :param aroma_therapy_on: New aroma therapy state (on or off).
        :return: Success of the set operation.
        """
        return self._send_set_command(Command.SET_AROMA_THERAPY_ON, aroma_therapy_on)

    def poke_aroma_therapy(self) -> bool:
        """
        Disable and directly enable aroma therapy again.
        Can be used to manually trigger the aroma therapy pump which usually is automatically triggered every 5 minutes
        (fixed value).

        :return: Success of the operation
        """
        if not self._send_set_command(Command.SET_AROMA_THERAPY_ON, False):
            return False
        return self._send_set_command(Command.SET_AROMA_THERAPY_ON, True)

    def set_lamp_on(self, lamp_on: bool) -> bool:
        """
        Power on the RGB lamp connected to the TOLO device.

        If LampMode is set to AUTOMATIC, the RGB lamp will change its color slowly and continuously without any further
        interaction by the user.
        If LampMode is set to MANUAL, the RGB lamp will start up with the latest color.
        Using `lamp_change_color` the lamp color can be changed to the next color in the color loop.
        The color loop can not be changed.
        Use `set_lamp_mode` to set the LampMode.

        :param lamp_on: New state of the RGB lamp (on or off).
        :return: Success of the set operation.
        """
        return self._send_set_command(Command.SET_LAMP_ON, lamp_on)

    def set_sweep_on(self, sweep_on: bool) -> bool:
        return self._send_set_command(Command.SET_SWEEP_ON, sweep_on)

    def set_salt_bath_on(self, salt_bath_on: bool) -> bool:
        return self._send_set_command(Command.SET_SALT_BATH_ON, salt_bath_on)

    def set_target_temperature(self, target_temperature: int) -> bool:
        return self._send_set_command(Command.SET_TARGET_TEMPERATURE, target_temperature)

    def set_target_humidity(self, target_humidity: int) -> bool:
        return self._send_set_command(Command.SET_TARGET_HUMIDITY, target_humidity)

    def set_power_timer(self, power_timer: int | None) -> bool:
        return self._send_set_command(Command.SET_POWER_TIMER, power_timer)

    def set_salt_bath_timer(self, salt_bath_timer: int | None) -> bool:
        return self._send_set_command(Command.SET_SALT_BATH_TIMER, salt_bath_timer)

    def set_aroma_therapy_slot(self, aroma_therapy_slot: AromaTherapySlot) -> bool:
        return self._send_set_command(Command.SET_AROMA_THERAPY_SLOT, aroma_therapy_slot)

    def set_sweep_timer(self, sweep_timer: int | None) -> bool:
        return self._send_set_command(Command.SET_SWEEP_TIMER, sweep_timer)

    def set_lamp_mode(self, lamp_mode: LampMode) -> bool:
        """
        Set the LampMode for the device controlled RGB lamp.

        Mode can be either AUTOMATIC or MANUAL.

        :param lamp_mode: New LampMode to be set.
        :return: Success of the set operation.
        """
        return self._send_set_command(Command.SET_LAMP_MODE, lamp_mode)

    def set_fan_timer(self, fan_timer: int | None) -> bool:
        return self._send_set_command(Command.SET_FAN_TIMER, fan_timer)

    def lamp_change_color(self) -> bool:
        """
        Change the RGB lamp's color to the next color in the color loop.

        Only possible when LampMode is set to MANUAL.

        :return: Return if changing the color was successful.
        """
        return self._send_set_command(Command.LAMP_CHANGE_COLOR, 1)

    def get_aroma_therapy_slot(self) -> AromaTherapySlot:
        """
        Return the currently selected slot for aroma therapy.

        :return: Currently selected slot for aroma therapy.
        """
        result = self._send_get_command(Command.GET_AROMA_THERAPY_SLOT)
        if isinstance(result, AromaTherapySlot):
            return result
        raise ValueError(f"unexpected type f{type(result)}, expecting AromaTherapySlot")

    def get_fan_timer(self) -> int | None:
        """
        Return the remaining time of the running fan timer (in minutes).

        :return: Remaining time of the running fan timer (in minutes) or None if currently not active.
        """
        result = self._send_get_command(Command.GET_FAN_TIMER)
        if result is None or isinstance(result, int):
            return result
        raise ValueError(f"unexpected type f{type(result)}, expecting int | None")

    def get_salt_bath_timer(self) -> int | None:
        """
        Return the remaining time of the running salt bath timer (in minutes).

        :return: Remaining time of the running salt bath timer (in minutes) or None if currently not active.
        """
        result = self._send_get_command(Command.GET_SALT_BATH_TIMER)
        if result is None or isinstance(result, int):
            return result
        raise ValueError(f"unexpected type f{type(result)}, expecting int | None")

    def get_lamp_mode(self) -> LampMode:
        """
        Return the current LampMode configured on the TOLO device.

        :return: Currently configured LampMode.
        """
        result = self._send_get_command(Command.GET_LAMP_MODE)
        if isinstance(result, LampMode):
            return result
        raise ValueError(f"unexpected type f{type(result)}, expecting LampMode")

    def get_sweep_timer(self) -> int | None:
        """
        Return the remaining time of the running sweep timer (in hours).

        :return: Remaining time of the running sweep timer (in hours) or None if currently not active.
        """
        result = self._send_get_command(Command.GET_SWEEP_TIMER)
        if result is None or isinstance(result, int):
            return result
        raise ValueError(f"unexpected type f{type(result)}, expecting int | None")

    def _send_set_command(self, command: Command, value: Any) -> bool:
        """
        Shorthand method for sending messages changing the state of the TOLO device.

        This method sends a message to the TOLO device in order to update a status or setting value.
        The method returns when the update has been confirmed by the device.

        :param command: TOLO Command according to the value to be changed.
        :param value: Value to be set.
        :return: Success of the set operation.
        """
        message = Message(command, command.value_handler.native2byte(value), b"\xff")
        response = self._communicate(message)
        return response.extra == b"\x00"

    def _send_get_command(self, command: Command) -> Any:
        """
        Shorthand method for sending messages requesting (single) values from the TOLO device.

        This method will send the request, wait for the response and converts the device return value to native Python
        types.

        :param command: TOLO Command according to the value to be requested.
        :return: Value as requested and sent by the TOLO device.
        """
        message = Message(command, b"\x00", b"\xff")
        response = self._communicate(message)
        return command.value_handler.byte2native(response.command_value)

    def _communicate(self, message: Message) -> Message:
        """
        Internal method for actual device communication.

        This method implements some retry logic, since sending UDP messages is unreliable.
        If a timeout has passed without a reply, the method re-sends the message.

        :param message: Message to be sent to the TOLO device.
        :return: Message returned by the TOLO device.
        """
        if self._socket is None:
            raise ToloCommunicationError("socket not initialized")

        for attempt in range(self._retry_count):
            logger.debug(
                f"sending message with"
                f" command '{message.command.name}',"
                f" value '{message.command_value.hex()}'"
                f" and extra data '{message.extra.hex()}',"
                f" attempt {attempt + 1}..."
            )
            self._socket.sendto(message.to_bytes(), (self._address, self._port))
            try:
                # receive packages
                response_bytes, sender = self._socket.recvfrom(4096)
                logger.debug(f"got response '{response_bytes.hex()}' from {sender}")

                # check if it is a keep-alive package
                if response_bytes == KEEP_ALIVE:
                    logger.debug("received keep alive response, ignoring")
                    continue

                # parse response
                response_message = Message.from_bytes(response_bytes)
                if response_message.command == message.command:
                    return response_message
            except (TimeoutError, socket.timeout):  # Python <= 3.9: socket.timeout, >= 3.10: TimeoutError
                continue

        raise ToloCommunicationError(f"failed to send message after {self._retry_count} attempts")

    @staticmethod
    def discover(
        broadcast_address: str = "255.255.255.255",
        port: int = DEFAULT_PORT,
        timeout: float = DEFAULT_RETRY_TIMEOUT,
        max_retries: int = DEFAULT_RETRY_COUNT,
    ) -> Generator[Tuple[Tuple[str, int], ToloStatus], None, None]:
        """
        Discover available TOLO devices.

        :param broadcast_address: To which address discovery probes should be sent.
        :param port: To which port discovery probes should be sent.
        :param timeout: Maximum wait timeout for devices to reply to discovery probes (in seconds).
        :param max_retries: Maximum amount of retries if after timeout no device has been reporting back.
        :return: Generator returning discovered TOLO devices.
        """
        discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        for _ in range(max_retries):
            discovery_socket.sendto(Message(Command.GET_STATUS, b"\x00", b"\xff").to_bytes(), (broadcast_address, port))
            wait_for_response_timeout = time() + timeout
            while time() < wait_for_response_timeout:
                select_event = select([discovery_socket], [], [], wait_for_response_timeout - time())
                if select_event[0]:
                    raw_bytes, sender = discovery_socket.recvfrom(4096)
                    message = Message.from_bytes(raw_bytes)
                    status = ToloStatus.from_bytes(message.extra)
                    yield sender, status
                else:
                    discovery_socket.close()
                    return

        discovery_socket.close()
        return

    def __del__(self) -> None:
        """
        De-initialize the client.

        Automatically called by the interpreter when the object is about to be deleted.
        """
        if self._socket is not None:
            self._socket.close()
