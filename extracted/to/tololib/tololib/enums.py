"""TOLOlib Enums."""

from enum import Enum, IntEnum
from typing import Any

from .command_value_handler import CommandValueHandler as CVH
from .const import (
    FAN_TIMER_MAX,
    POWER_TIMER_MAX,
    SALT_BATH_TIMER_MAX,
    SWEEP_TIMER_MAX,
    TARGET_HUMIDITY_MAX,
    TARGET_HUMIDITY_MIN,
    TARGET_TEMPERATURE_MAX,
    TARGET_TEMPERATURE_MIN,
)


class AromaTherapySlot(IntEnum):
    """Aroma therapy slot."""

    A = 0
    B = 1


class Calefaction(IntEnum):
    """Calefaction status."""

    HEAT = 0
    INACTIVE = 1
    UNCLEAR = 2  # TODO find correct meaning
    KEEP = 3


class LampMode(IntEnum):
    """Mode of RGB light control."""

    MANUAL = 0
    AUTOMATIC = 1


class Model(IntEnum):
    """TOLO device model."""

    DOMESTIC = 0
    COMMERCIAL = 1


class Command(Enum):
    """Commands and their command code encoding combined with Python native type conversion information."""

    SET_TARGET_TEMPERATURE = 4, CVH[int](lambda x: TARGET_TEMPERATURE_MIN <= x <= TARGET_TEMPERATURE_MAX)
    SET_POWER_TIMER = 8, CVH[int](lambda x: 1 <= x <= POWER_TIMER_MAX, b"\xff")
    SET_POWER_ON = 14, CVH[bool]()
    SET_AROMA_THERAPY_ON = 18, CVH[bool]()
    SET_AROMA_THERAPY_SLOT = 20, CVH[AromaTherapySlot]()
    GET_AROMA_THERAPY_SLOT = 21, CVH[AromaTherapySlot]()
    SET_SWEEP_ON = 26, CVH[bool]()
    SET_SWEEP_TIMER = 28, CVH[int](lambda x: 1 <= x <= SWEEP_TIMER_MAX, b"\x00")
    SET_LAMP_ON = 30, CVH[bool]()
    SET_FAN_ON = 34, CVH[bool]()
    SET_FAN_TIMER = 36, CVH[int](lambda x: 1 <= x <= FAN_TIMER_MAX, b"\x3d")  # 0x3d == 61
    SET_TARGET_HUMIDITY = 38, CVH[int](lambda x: TARGET_HUMIDITY_MIN <= x <= TARGET_HUMIDITY_MAX)
    GET_SWEEP_TIMER = 51, CVH[int](lambda x: 0 <= x <= SWEEP_TIMER_MAX, b"\x00")
    GET_FAN_TIMER = 53, CVH[int](lambda x: 0 <= x <= FAN_TIMER_MAX, b"\x3d")  # 0x3d == 61
    SET_SALT_BATH_ON = 54, CVH[bool]()
    SET_SALT_BATH_TIMER = 56, CVH[int](lambda x: 1 <= x <= SALT_BATH_TIMER_MAX, b"\xff")
    GET_SALT_BATH_TIMER = 59, CVH[int](lambda x: 0 <= x <= SALT_BATH_TIMER_MAX, b"\xff")
    SET_LAMP_MODE = 60, CVH[LampMode]()
    GET_LAMP_MODE = 61, CVH[LampMode]()
    LAMP_CHANGE_COLOR = 62, CVH[bool](validator_function=lambda x: x == 1)
    GET_STATUS = 97, CVH[int]()
    GET_SETTINGS = 99, CVH[int]()

    def __init__(self, code: int, value_handler: CVH[Any]) -> None:
        self._code = code
        self._value_handler = value_handler

    @property
    def code(self) -> int:
        """
        Command code of the current Command instance.

        :return: Command code of the current Command instance.
        """
        return self._code

    @property
    def value_handler(self) -> CVH[Any]:
        """
        CommandValueHandler of the current Command instance.

        :return: CommandValueHandler of the current Command instance.
        """
        return self._value_handler

    @classmethod
    def from_code(cls, code: int) -> "Command":
        """
        Return the Command instance with the given command code.

        :param code: Command code in question.
        :return: Command having the given command code.
        """
        for command in cls:
            if command.code == code:
                return command
        raise ValueError(f"unknown command code {code}")

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Command) and other.code == self.code

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)
