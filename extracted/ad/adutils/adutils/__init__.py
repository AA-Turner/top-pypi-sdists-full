"""adutils - helper functions for AppDaemon apps

  @benleb / https://github.com/benleb/adutils
"""

from __future__ import annotations

# from datetime import datetime, timedelta, timezone
from importlib.metadata import version
from sys import version_info
from typing import Any

from appdaemon.appdaemon import AppDaemon
from statistics import fmean


__version__ = version(__name__)

# version checks
py3_or_higher = version_info.major >= 3
py37_or_higher = py3_or_higher and version_info.minor >= 7
py38_or_higher = py3_or_higher and version_info.minor >= 8
py39_or_higher = py3_or_higher and version_info.minor >= 9

# timing
SECONDS_PER_MIN: int = 60


def hl(text: int | float | str) -> str:
    return f"\033[1m{text}\033[0m"


def hl_entity(entity: str) -> str:
    domain, entity = entity.split(".")
    return f"{domain}.{hl(entity)}"


def natural_time(duration: int | float) -> str:

    duration_min, duration_sec = divmod(duration, float(SECONDS_PER_MIN))

    # append suitable unit
    if duration >= SECONDS_PER_MIN:
        if duration_sec < 10 or duration_sec > 50:
            natural = f"{hl(int(duration_min))}min"
        else:
            natural = f"{hl(int(duration_min))}min {hl(int(duration_sec))}sec"
    else:
        natural = f"{hl(int(duration_sec))}sec"

    return natural


class Room:
    """Class for keeping track of a room."""

    def __init__(
        self,
        name: str,
        room_lights: set[str] = set(),
        motion: set[str] = set(),
        door_window: set[str] = set(),
        temperature: set[str] = set(),
        push_data: dict[str, dict[str, int | str]] = {},
        appdaemon: AppDaemon = None
    ) -> None:

        self.name: str = name

        # all lights in the room
        self.room_lights: set[str] = room_lights

        # motion sensors of the room
        self.motion: set[str] = motion
        # door/window sensors of the room
        self.door_window: set[str] = door_window
        # temperature sensors of the room
        self.temperature: set[str] = temperature

        # reminder notification callback handles
        self.handles: dict[str, str] = {}
        # ios push settings
        self.push_data: dict[str, dict[str, int | str]] = push_data

        # callback handles to switch off the lights
        self.handles_automoli: set[str] = set()
        # callback handles for notifreeze notifications
        self.handles_notifreeze: set[str] = set()

        # appdaemon instance
        self._ad = appdaemon

    @property
    def lights_dimmable(self) -> list[str]:
        """Stupid but currently suitable separation..."""
        return [light for light in self.room_lights if light.startswith("light.")]

    @property
    def lights_undimmable(self) -> list[str]:
        """Stupid but currently suitable separation..."""
        return [light for light in self.room_lights if light.startswith("switch.")]

    async def indoor(self, nf: Any) -> float | None:
        indoor_temperatures = set()
        invalid_sensors = {}

        for sensor in self.temperature:
            try:
                indoor_temperatures.add(float(await nf.get_state(sensor)))
            except (ValueError, TypeError):
                invalid_sensors[sensor] = await nf.get_state(sensor)
                continue

        if indoor_temperatures:
            return fmean(indoor_temperatures)

        nf.lg(f"{self.name}: No valid values ¯\\_(ツ)_/¯ {invalid_sensors = }")

        return None

    async def difference(self, outdoor: float, nf: Any) -> float | None:
        return round(outdoor - indoor, 2) if (indoor := await self.indoor(nf)) else None
