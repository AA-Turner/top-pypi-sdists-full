from __future__ import annotations

from tololib.command_value_handler import CommandValueHandler
from tololib.enums import AromaTherapySlot, Calefaction, LampMode, Model


class ToloStatus(object):
    """A class reflecting the current status of a TOLO device."""

    def __init__(
        self,
        power_on: bool,
        current_temperature: int,
        power_timer: int | None,
        flow_in: bool,
        flow_out: bool,
        calefaction: Calefaction,
        aroma_therapy_on: bool,
        sweep_on: bool,
        sweep_timer: int,
        lamp_on: bool,
        water_level: int,
        fan_on: bool,
        fan_timer: int | None,
        current_humidity: int,
        tank_temperature: int,
        model: Model,
        salt_bath_on: bool,
        salt_bath_timer: int | None,
    ) -> None:
        self.power_on = power_on
        self.current_temperature = current_temperature
        self.power_timer = power_timer
        self.flow_in = flow_in
        self.flow_out = flow_out
        self.calefaction = calefaction
        self.aroma_therapy_on = aroma_therapy_on
        self.sweep_on = sweep_on
        self.sweep_timer = sweep_timer
        self.lamp_on = lamp_on
        self.water_level = water_level
        self.fan_on = fan_on
        self.fan_timer = fan_timer
        self.current_humidity = current_humidity
        self.tank_temperature = tank_temperature
        self.model = model
        self.salt_bath_on = salt_bath_on
        self.salt_bath_timer = salt_bath_timer

    @property
    def water_level_percent(self) -> int:
        if self.water_level == 0:
            return 0
        elif self.water_level == 1:
            return 33
        elif self.water_level == 2:
            return 66
        elif self.water_level == 3:
            return 100
        raise ValueError(f"unsupported water level {self.water_level}")

    @staticmethod
    def from_bytes(data: bytes) -> "ToloStatus":
        """
        Create a TOLO Status NamedTuple from a binary status message (17 bytes)

         0: {0, 1} reflecting if the power is on
         1: current temperature
         2: 61 if power timer is disabled, else duration (1..60) in minutes
         3: (64 if flow in else 0) + (16 if flow out else 0) + Calefaction state (0..3)
         4: {0, 1} reflecting if aroma therapy is on
         5: {0, 1} reflecting if sweep is on
         6: sweep timer remaining (1..8) in hours or 0 when off
         7: {0, 1} reflecting if lamp is on
         8: water level (0..3)
         9: {0, 1} reflecting if fan is on
        10: 61 if self._fan_timer is None else self._fan_timer,
        11: self._current_humidity,
        12: self._tank_temperature,
        13: 0,  # TODO unused?
        14: self._model.value,
        15: self._salt_bath_on,
        16: 0 if self._salt_bath_timer is None else self._salt_bath_timer

        :param data: payload bytes of device response
        :return: NamedTuple reflecting the TOLO device status
        """
        return ToloStatus(
            # data[0]
            power_on=bool(data[0]),
            # data[1]
            current_temperature=data[1],
            # data[2]
            power_timer=CommandValueHandler[int](none_equivalent=b"\x3d").byte2native(bytes([data[2]])),
            # data[3]
            calefaction=Calefaction(data[3] & 3),
            flow_in=bool(data[3] & 64),
            flow_out=bool(data[3] & 16),
            # data[4]
            aroma_therapy_on=bool(data[4]),
            # data[5]
            sweep_on=bool(data[5]),
            # data[6]
            sweep_timer=data[6],
            # data[7]
            lamp_on=bool(data[7]),
            # data[8]
            water_level=data[8],
            # data[9]
            fan_on=bool(data[9]),
            # data[10]
            fan_timer=CommandValueHandler[int](none_equivalent=b"\x3d").byte2native(bytes([data[10]])),
            # data[11]
            current_humidity=data[11],
            # data[12]
            tank_temperature=data[12],
            # data[13]
            # TODO unused?
            # data[14]
            model=Model(data[14]),
            # data[15]
            salt_bath_on=bool(data[15]),
            # data[16]
            salt_bath_timer=CommandValueHandler[int](none_equivalent=b"\x00").byte2native(bytes([data[16]])),
        )


class ToloSettings(object):
    """A class reflecting the current settings of a TOLO device."""

    def __init__(
        self,
        target_temperature: int,
        power_timer: int | None,
        aroma_therapy_slot: AromaTherapySlot,
        sweep_timer: int | None,
        fan_timer: int | None,
        target_humidity: int,
        salt_bath_timer: int | None,
        lamp_mode: LampMode,
    ) -> None:
        self.target_temperature = target_temperature
        self.power_timer = power_timer
        self.aroma_therapy_slot = aroma_therapy_slot
        self.sweep_timer = sweep_timer
        self.fan_timer = fan_timer
        self.target_humidity = target_humidity
        self.salt_bath_timer = salt_bath_timer
        self.lamp_mode = lamp_mode

    @staticmethod
    def from_bytes(data: bytes) -> "ToloSettings":
        """
        Create a TOLO Settings NamedTuple from a binary status message (8 bytes)

        0: self._target_temperature,
        1: 255 if self._power_timer is None else self._power_timer,
        2: self._aroma_therapy.value,
        3: self._sweep_timer,
        4: 61 if self._fan_timer is None else self._fan_timer,
        5: self._target_humidity,
        6: 255 if self._salt_bath_timer is None else self._salt_bath_timer,
        7: self._lamp_mode.value

        :param data: payload bytes of device response
        :return: NamedTuple reflecting the TOLO device settings
        """

        # data[0]
        target_temperature = data[0]

        # data[1]
        power_timer = CommandValueHandler[int](none_equivalent=b"\xff").byte2native(bytes([data[1]]))

        # data[2]
        aroma_therapy_slot = AromaTherapySlot(data[2])

        # data[3]
        sweep_timer = CommandValueHandler[int](none_equivalent=b"\x00").byte2native(bytes([data[3]]))

        # data[4]
        fan_timer = CommandValueHandler[int](none_equivalent=b"\x3d").byte2native(bytes([data[4]]))

        # data[5]
        target_humidity = data[5]

        # data[6]
        salt_bath_timer = CommandValueHandler[int](none_equivalent=b"\xff").byte2native(bytes([data[6]]))

        # data[7]
        try:
            lamp_mode = LampMode(data[7])
        except IndexError:
            lamp_mode = LampMode.MANUAL

        # return result
        return ToloSettings(
            target_temperature=target_temperature,
            power_timer=power_timer,
            aroma_therapy_slot=aroma_therapy_slot,
            sweep_timer=sweep_timer,
            fan_timer=fan_timer,
            target_humidity=target_humidity,
            salt_bath_timer=salt_bath_timer,
            lamp_mode=lamp_mode,
        )
