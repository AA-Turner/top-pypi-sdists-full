"""Dummy implementation of PowerStrip."""
from __future__ import annotations

import random

from pyegps.powerstrip import PowerStrip


class FakePowerStrip(PowerStrip):
    """Dummy PowerStrip Device."""

    DEVICES: list[FakePowerStrip] = []

    def __init__(self, devId: str, number_of_sockets: int):
        """Initiate new DummyDevice."""
        self._devId = devId
        self._numberOfSockets = number_of_sockets
        self._status = [random.randint(0, 1) for _ in range(number_of_sockets)]

    # PowerStrip implementations
    @property
    def numberOfSockets(self):
        return self._numberOfSockets

    def switch_on(self, socket: int) -> None:
        super().switch_on(socket)
        self._status[socket] = 1

    def switch_off(self, socket: int) -> None:
        super().switch_off(socket)
        self._status[socket] = 0

    def get_status(self, socket: int) -> bool:
        super().get_status(socket)
        return self._status[socket] == 1

    # Device implementations
    @property
    def uid(self) -> str:
        """Return an identifier among DummyPowerStrip devices."""
        return self._devId

    @property
    def manufacturer(self) -> str:
        """Return the device manufacturer."""
        return "DummyDevices"

    @property
    def name(self) -> str:
        """Return the product name."""
        return "DummyPowerStrip"

    @classmethod
    def get_implementation_id(cls) -> str:
        """Return an identifier for this implementation."""
        return "DYPS"

    @classmethod
    def search_for_devices(cls) -> list[FakePowerStrip]:
        """Return the dummy devices, create new if necessary."""
        if len(cls.DEVICES) == 0:
            cls.DEVICES += [
                cls(devId, sockets)
                for devId, sockets in [("AA:BB:CC", 4), ("00:11:22", 2)]
            ]

        return cls.DEVICES
