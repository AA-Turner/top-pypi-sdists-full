from __future__ import annotations

import threading
from argparse import ArgumentParser, Namespace
from signal import SIGINT
from signal import signal as register_signal_handler
from types import FrameType

from ..const import DEFAULT_PORT
from ..device_simulator import ToloDeviceSimulator
from .common import Command


class DeviceSimulatorCommand(Command):
    def __init__(self, argument_parser: ArgumentParser) -> None:
        super().__init__(argument_parser)
        argument_parser.add_argument("-l", "--listen", default="localhost", dest="address", type=str)
        argument_parser.add_argument("-p", "--port", default=DEFAULT_PORT, type=int)

        self._tolo_test_server: ToloDeviceSimulator | None = None

    def __call__(self, args: Namespace) -> int:
        if threading.main_thread():
            register_signal_handler(SIGINT, lambda signals, frame_type: self._signal_handler(signals, frame_type))

        self._tolo_test_server = ToloDeviceSimulator(args.address, args.port)
        self._tolo_test_server.start()
        self._tolo_test_server.join()
        return 0

    def _signal_handler(self, signal: int, frame_type: FrameType | None = None) -> None:
        if signal == SIGINT and self._tolo_test_server is not None:
            self._tolo_test_server.stop()
