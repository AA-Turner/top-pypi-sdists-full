"""Definition of the base class for alle devices."""
from __future__ import annotations

import abc

from typing import TypeVar

T = TypeVar("T", bound="Device")


class Device(abc.ABC):
    """Abstract base class for all devices."""

    def release(self) -> None:
        """Free any resources if needed."""

    @property
    def device_id(self) -> str:
        """Return a unique identifier among all devices of any type."""
        return f"{self.get_implementation_id()}:{self.uid}"

    @classmethod
    def is_responsible(cls, device_id: str) -> bool:
        """Check if the given device_id is handled by this device implementation."""
        return device_id.split(":")[0] == cls.get_implementation_id()

    @classmethod
    def get_device(cls, device_id: str) -> Device | None:
        """Get the device for the given device_id."""
        if not cls.is_responsible(device_id):
            return None

        devices = cls.search_for_devices()
        for d in devices:
            if d.device_id == device_id:
                return d
        return None

    @property
    @abc.abstractmethod
    def uid(self) -> str:
        """Return an identifier within the implementation context."""

    @staticmethod
    @abc.abstractmethod
    def get_device_type() -> str:
        """Return the implemented device type."""

    @property
    @abc.abstractmethod
    def manufacturer(self) -> str:
        """Return the device manufacturer."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Return the product name."""

    @classmethod
    @abc.abstractmethod
    def get_implementation_id(cls) -> str:
        """Return an identifier for this implementation."""

    @classmethod
    @abc.abstractmethod
    def search_for_devices(cls: type[T]) -> list[T]:
        """Search for supported devices."""

    @abc.abstractmethod
    def summary(self) -> str:
        """Return a summary of the device and current status."""

    def __repr__(self) -> str:
        return f"{self.get_device_type()}: {self.device_id}"
