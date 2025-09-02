import logging
import socket
from threading import Thread

from .const import DEFAULT_PORT
from .enums import Command
from .message import Message

logger = logging.getLogger(__name__)


class ToloDeviceSimulator(Thread):
    def __init__(self, address: str = "localhost", port: int = DEFAULT_PORT) -> None:
        super().__init__()

        self._address = address
        self._port = port

        self._status = bytearray(17)
        self._settings = bytearray(8)

        self._keep_running = False

    def start(self) -> None:
        self._keep_running = True
        super().start()

    def run(self) -> None:
        logger.info("starting up")
        server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        server_socket.bind((self._address, self._port))
        server_socket.settimeout(0.2)
        logger.info("ready for incoming messages")

        # listen and answer messages
        while self._keep_running:
            # listen and answer messages
            try:
                data, sender = server_socket.recvfrom(4096)
            except socket.timeout:
                continue

            request = Message.from_bytes(data)
            logger.debug(f"received message {request} from {sender}")

            try:
                response = self._handle_message(request)
            except ValueError as e:
                logger.warning(f"could not generate response message: {e}")
                continue

            logger.debug(f"sending {response} to {sender}")
            server_socket.sendto(response.to_bytes(), sender)

        # close socket
        server_socket.close()

    @staticmethod
    def _handle_set(message: Message, field: bytearray, index: int) -> Message:
        field[index] = int.from_bytes(message.command_value, "big", signed=False)
        return Message(message.command, message.command_value, b"\x00")

    @staticmethod
    def _handle_get(message: Message, field: bytearray, index: int) -> Message:
        return Message(message.command, field[index].to_bytes(1, "big", signed=False), b"\x00")

    def _handle_message(self, message: Message) -> Message:
        if message.command == Command.GET_STATUS:
            return Message(message.command, b"\x11", self._status)

        elif message.command == Command.GET_SETTINGS:
            return Message(message.command, b"\x08", self._settings)

        elif message.command == Command.SET_TARGET_TEMPERATURE:
            return self._handle_set(message, self._settings, 0)

        elif message.command == Command.SET_POWER_TIMER:
            self._status[2] = int.from_bytes(message.command_value, "big", signed=False)
            return self._handle_set(message, self._settings, 1)

        elif message.command == Command.SET_POWER_ON:
            return self._handle_set(message, self._status, 0)

        elif message.command == Command.SET_AROMA_THERAPY_ON:
            return self._handle_set(message, self._status, 4)

        elif message.command == Command.SET_AROMA_THERAPY_SLOT:
            return self._handle_set(message, self._settings, 2)

        elif message.command == Command.GET_AROMA_THERAPY_SLOT:
            return self._handle_get(message, self._settings, 2)

        elif message.command == Command.SET_SWEEP_TIMER:
            self._status[6] = int.from_bytes(message.command_value, "big", signed=False)
            return self._handle_set(message, self._settings, 3)

        elif message.command == Command.SET_LAMP_ON:
            return self._handle_set(message, self._status, 7)

        elif message.command == Command.SET_FAN_ON:
            return self._handle_set(message, self._status, 9)

        elif message.command == Command.SET_FAN_TIMER:
            self._status[10] = int.from_bytes(message.command_value, "big", signed=False)
            return self._handle_set(message, self._settings, 4)

        elif message.command == Command.SET_TARGET_HUMIDITY:
            return self._handle_set(message, self._settings, 5)

        elif message.command == Command.SET_SWEEP_ON:
            return self._handle_set(message, self._status, 5)

        elif message.command == Command.GET_FAN_TIMER:
            return self._handle_get(message, self._status, 10)

        elif message.command == Command.SET_SALT_BATH_ON:
            return self._handle_set(message, self._status, 15)

        elif message.command == Command.SET_SALT_BATH_TIMER:
            self._status[16] = int.from_bytes(message.command_value, "big", signed=False)
            return self._handle_set(message, self._settings, 6)

        elif message.command == Command.GET_SALT_BATH_TIMER:
            return self._handle_get(message, self._status, 16)

        elif message.command == Command.SET_LAMP_MODE:
            return self._handle_set(message, self._settings, 7)

        elif message.command == Command.GET_LAMP_MODE:
            return self._handle_get(message, self._settings, 7)

        elif message.command == Command.GET_SWEEP_TIMER:
            return self._handle_get(message, self._status, 6)

        elif message.command == Command.LAMP_CHANGE_COLOR:
            return Message(message.command, message.command_value, b"\x00")

        else:
            raise ValueError(f"unrecognized message {message}")

    def stop(self) -> None:
        logger.info("shutting down")
        self._keep_running = False
