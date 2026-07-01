# SPDX-License-Identifier: MIT
# Copyright (c) 2021-2026
"""
Shared data-point categorization enums.

``DataPointCategory`` and ``DataPointType`` are the values Home Assistant
filters on when spawning entities. The daemon ships these strings on the wire
and aiohomematic exposes the same enums, so they must stay byte-identical
across both backends — hence they live in the shared contract package.
"""

from enum import StrEnum, unique

__all__ = ["DataPointCategory", "DataPointType"]


class DataPointCategory(StrEnum):
    """Enum with data point types."""

    ACTION = "action"
    ACTION_NUMBER = "action_number"
    ACTION_SELECT = "action_select"
    BINARY_SENSOR = "binary_sensor"
    BUTTON = "button"
    CLIMATE = "climate"
    COVER = "cover"
    EVENT = "event"
    EVENT_GROUP = "event_group"
    HUB_BINARY_SENSOR = "hub_binary_sensor"
    HUB_BUTTON = "hub_button"
    HUB_NUMBER = "hub_number"
    HUB_SELECT = "hub_select"
    HUB_SENSOR = "hub_sensor"
    HUB_SWITCH = "hub_switch"
    HUB_TEXT = "hub_text"
    HUB_UPDATE = "hub_update"
    LIGHT = "light"
    LOCK = "lock"
    NUMBER = "number"
    SCHEDULE_SWITCH = "schedule_switch"
    SELECT = "select"
    SENSOR = "sensor"
    SIREN = "siren"
    SWITCH = "switch"
    TEXT = "text"
    TEXT_DISPLAY = "text_display"
    UNDEFINED = "undefined"
    UPDATE = "update"
    VALVE = "valve"
    WEEK_PROFILE = "week_profile"


@unique
class DataPointType(StrEnum):
    """
    Canonical data point type for downstream consumers.

    Maps each data point to a functional type (sensor, switch, climate, etc.)
    that downstream projects can use for entity/device routing without
    isinstance checks or custom mapping logic.
    """

    BINARY_SENSOR = "binary_sensor"
    BUTTON = "button"
    CLIMATE = "climate"
    COVER = "cover"
    EVENT = "event"
    LIGHT = "light"
    LOCK = "lock"
    NUMBER = "number"
    SELECT = "select"
    SENSOR = "sensor"
    SIREN = "siren"
    SWITCH = "switch"
    TEXT = "text"
    UPDATE = "update"
    VALVE = "valve"
