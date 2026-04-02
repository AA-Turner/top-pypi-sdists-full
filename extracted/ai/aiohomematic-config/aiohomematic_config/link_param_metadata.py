"""Metadata classification for link paramset parameters."""

from dataclasses import dataclass
from enum import StrEnum, unique
import math
from typing import Final


@unique
class LinkParamCategory(StrEnum):
    """Functional category of a link parameter."""

    TIME = "time"
    LEVEL = "level"
    JUMP_TARGET = "jump_target"
    CONDITION = "condition"
    ACTION = "action"
    OTHER = "other"


@unique
class KeypressGroup(StrEnum):
    """Keypress duration group for SHORT/LONG partitioning."""

    SHORT = "short"
    LONG = "long"
    COMMON = "common"


@unique
class TimeSelectorType(StrEnum):
    """Type of time selector preset list."""

    TIME_ON_OFF = "timeOnOff"
    DELAY = "delay"
    RAMP_ON_OFF = "rampOnOff"


@dataclass(frozen=True)
class TimePreset:
    """A single preset option in a time selector."""

    base: int
    factor: int
    label_en: str
    label_de: str


@dataclass(frozen=True)
class LinkParamMeta:
    """Metadata for a single link parameter."""

    category: LinkParamCategory
    keypress_group: KeypressGroup
    display_as_percent: bool = False
    has_last_value: bool = False
    hidden_by_default: bool = False
    time_pair_id: str | None = None
    time_selector_type: TimeSelectorType | None = None


# TIME_BASE unit multipliers: base_value -> seconds_per_unit
_TIME_BASE_UNITS: Final[dict[int, float]] = {
    0: 0.1,
    1: 1.0,
    2: 5.0,
    3: 10.0,
    4: 60.0,
    5: 300.0,
    6: 600.0,
    7: 3600.0,
}

_TIME_ON_OFF_PRESETS: Final[tuple[TimePreset, ...]] = (
    TimePreset(0, 0, "Not active", "Nicht aktiv"),
    TimePreset(0, 1, "100 ms", "100 ms"),
    TimePreset(1, 1, "1 s", "1 s"),
    TimePreset(1, 2, "2 s", "2 s"),
    TimePreset(1, 3, "3 s", "3 s"),
    TimePreset(2, 1, "5 s", "5 s"),
    TimePreset(3, 1, "10 s", "10 s"),
    TimePreset(3, 3, "30 s", "30 s"),
    TimePreset(4, 1, "1 min", "1 min"),
    TimePreset(4, 2, "2 min", "2 min"),
    TimePreset(5, 1, "5 min", "5 min"),
    TimePreset(6, 1, "10 min", "10 min"),
    TimePreset(6, 3, "30 min", "30 min"),
    TimePreset(7, 1, "1 h", "1 h"),
    TimePreset(7, 2, "2 h", "2 h"),
    TimePreset(7, 3, "3 h", "3 h"),
    TimePreset(7, 5, "5 h", "5 h"),
    TimePreset(7, 8, "8 h", "8 h"),
    TimePreset(7, 12, "12 h", "12 h"),
    TimePreset(7, 24, "24 h", "24 h"),
    TimePreset(7, 31, "Permanent", "Permanent"),
)

_DELAY_PRESETS: Final[tuple[TimePreset, ...]] = (
    TimePreset(0, 0, "Not active", "Nicht aktiv"),
    TimePreset(2, 1, "5 s", "5 s"),
    TimePreset(3, 1, "10 s", "10 s"),
    TimePreset(3, 3, "30 s", "30 s"),
    TimePreset(4, 1, "1 min", "1 min"),
    TimePreset(4, 2, "2 min", "2 min"),
    TimePreset(5, 1, "5 min", "5 min"),
    TimePreset(6, 1, "10 min", "10 min"),
    TimePreset(6, 3, "30 min", "30 min"),
    TimePreset(7, 1, "1 h", "1 h"),
)

_RAMP_ON_OFF_PRESETS: Final[tuple[TimePreset, ...]] = (
    TimePreset(0, 0, "Not active", "Nicht aktiv"),
    TimePreset(0, 2, "200 ms", "200 ms"),
    TimePreset(0, 5, "500 ms", "500 ms"),
    TimePreset(1, 1, "1 s", "1 s"),
    TimePreset(1, 2, "2 s", "2 s"),
    TimePreset(1, 5, "5 s", "5 s"),
    TimePreset(1, 10, "10 s", "10 s"),
    TimePreset(1, 20, "20 s", "20 s"),
    TimePreset(1, 30, "30 s", "30 s"),
)

PRESETS_BY_TYPE: Final[dict[TimeSelectorType, tuple[TimePreset, ...]]] = {
    TimeSelectorType.TIME_ON_OFF: _TIME_ON_OFF_PRESETS,
    TimeSelectorType.DELAY: _DELAY_PRESETS,
    TimeSelectorType.RAMP_ON_OFF: _RAMP_ON_OFF_PRESETS,
}

_BASE_SUFFIX = "_BASE"
_FACTOR_SUFFIX = "_FACTOR"
_TIME_SUFFIXES = ("_TIME_BASE", "_TIME_FACTOR")
_JT_MARKER = "JT_"
_CT_MARKER = "CT_"
_LEVEL_SUFFIXES = ("_LEVEL", "_DIM_MIN_LEVEL", "_DIM_MAX_LEVEL")
_ACTION_SUFFIXES = ("_ACTION_TYPE", "_MULTIEXECUTE")

_TIME_TYPE_MAP: Final[dict[str, TimeSelectorType]] = {
    "ON_TIME": TimeSelectorType.TIME_ON_OFF,
    "OFF_TIME": TimeSelectorType.TIME_ON_OFF,
    "ONDELAY_TIME": TimeSelectorType.DELAY,
    "OFFDELAY_TIME": TimeSelectorType.DELAY,
    "ON_DELAY_TIME": TimeSelectorType.DELAY,
    "OFF_DELAY_TIME": TimeSelectorType.DELAY,
    "RAMP_ON_TIME": TimeSelectorType.RAMP_ON_OFF,
    "RAMP_OFF_TIME": TimeSelectorType.RAMP_ON_OFF,
    "RAMPON_TIME": TimeSelectorType.RAMP_ON_OFF,
    "RAMPOFF_TIME": TimeSelectorType.RAMP_ON_OFF,
}


def _strip_keypress_prefix(*, param_upper: str) -> tuple[KeypressGroup, str]:
    """Strip SHORT_/LONG_ prefix and return group and remainder."""
    if param_upper.startswith("SHORT_"):
        return KeypressGroup.SHORT, param_upper[6:]
    if param_upper.startswith("LONG_"):
        return KeypressGroup.LONG, param_upper[5:]
    return KeypressGroup.COMMON, param_upper


def classify_link_parameter(*, parameter_id: str) -> LinkParamMeta:
    """Classify a single link parameter and return its metadata."""
    upper = parameter_id.upper()
    keypress_group, suffix = _strip_keypress_prefix(param_upper=upper)

    # TIME_BASE / TIME_FACTOR pairs
    # Suffix examples: ON_TIME_BASE, ONDELAY_TIME_FACTOR, RAMP_ON_TIME_BASE
    if suffix.endswith((_BASE_SUFFIX, _FACTOR_SUFFIX)):
        # Check if this is a *_TIME_BASE or *_TIME_FACTOR
        is_time_base = suffix.endswith("_TIME_BASE")
        is_time_factor = suffix.endswith("_TIME_FACTOR")
        if is_time_base or is_time_factor:
            # Strip _BASE or _FACTOR to get the time stem (e.g. ON_TIME)
            time_stem = suffix[: -len(_BASE_SUFFIX)] if is_time_base else suffix[: -len(_FACTOR_SUFFIX)]

            time_pair_id = (
                f"{keypress_group.value.upper()}_{time_stem}" if keypress_group != KeypressGroup.COMMON else time_stem
            )
            selector_type = _TIME_TYPE_MAP.get(time_stem)

            return LinkParamMeta(
                category=LinkParamCategory.TIME,
                keypress_group=keypress_group,
                time_pair_id=time_pair_id,
                time_selector_type=selector_type,
            )

    # Jump targets: contains "JT_" (e.g. JT_ON, JT_OFF, JT_ONDELAY)
    if _JT_MARKER in suffix:
        return LinkParamMeta(
            category=LinkParamCategory.JUMP_TARGET,
            keypress_group=keypress_group,
            hidden_by_default=True,
        )

    # Condition transitions: contains "CT_" (e.g. CT_ON, CT_OFF)
    if _CT_MARKER in suffix:
        return LinkParamMeta(
            category=LinkParamCategory.CONDITION,
            keypress_group=keypress_group,
            hidden_by_default=True,
        )

    # Level parameters
    if any(suffix.endswith(s) for s in _LEVEL_SUFFIXES) or suffix == "LEVEL":
        return LinkParamMeta(
            category=LinkParamCategory.LEVEL,
            keypress_group=keypress_group,
            display_as_percent=True,
            has_last_value=True,
        )

    # Action type
    if any(suffix.endswith(s) for s in _ACTION_SUFFIXES) or suffix == "MULTIEXECUTE":
        return LinkParamMeta(
            category=LinkParamCategory.ACTION,
            keypress_group=keypress_group,
            hidden_by_default=True,
        )

    return LinkParamMeta(
        category=LinkParamCategory.OTHER,
        keypress_group=keypress_group,
    )


def get_time_presets(
    *,
    selector_type: TimeSelectorType,
    locale: str = "en",
) -> list[dict[str, int | str]]:
    """Return preset options for a time selector type."""
    presets = PRESETS_BY_TYPE.get(selector_type, ())
    result: list[dict[str, int | str]] = []
    for preset in presets:
        label = preset.label_de if locale == "de" else preset.label_en
        result.append({"base": preset.base, "factor": preset.factor, "label": label})
    return result


def decode_time_value(*, base: int, factor: int) -> float:
    """Convert base+factor pair to seconds."""
    unit = _TIME_BASE_UNITS.get(base, 1.0)
    return unit * factor


def encode_time_value(*, seconds: float, selector_type: TimeSelectorType) -> tuple[int, int]:
    """Find the closest preset base+factor pair for a given duration in seconds."""
    presets = PRESETS_BY_TYPE.get(selector_type, ())
    best_base, best_factor = 0, 0
    best_diff = math.inf
    for preset in presets:
        preset_seconds = decode_time_value(base=preset.base, factor=preset.factor)
        if (diff := abs(preset_seconds - seconds)) < best_diff:
            best_diff = diff
            best_base = preset.base
            best_factor = preset.factor
    return best_base, best_factor
