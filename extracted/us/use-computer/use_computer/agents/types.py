"""Shared runner types for internal values."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Any, cast


class Platform(str, Enum):
    MACOS = "macos"

    @property
    def display_name(self) -> str:
        return {
            Platform.MACOS: "macOS",
        }[self]

    @classmethod
    def parse(cls, value: object, default: Platform | None = None) -> Platform:
        if isinstance(value, cls):
            return value
        raw = getattr(value, "value", value)
        try:
            return cls(str(raw).lower())
        except ValueError:
            return default or cls.MACOS


class DesktopAction(str, Enum):
    CLICK = "click"
    LEFT_CLICK = "left_click"
    RIGHT_CLICK = "right_click"
    DOUBLE_CLICK = "double_click"
    TRIPLE_CLICK = "triple_click"
    MIDDLE_CLICK = "middle_click"
    TYPE = "type"
    KEY = "key"
    SCROLL = "scroll"
    MOVE = "move"
    DRAG = "drag"
    WAIT = "wait"
    SCREENSHOT = "screenshot"

    @classmethod
    def parse(cls, value: object) -> DesktopAction | None:
        if isinstance(value, cls):
            return value
        raw = getattr(value, "value", value)
        try:
            return cls(str(raw))
        except ValueError:
            return None


class MouseButton(str, Enum):
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"


class ScrollDirection(str, Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    @classmethod
    def parse(cls, value: object) -> ScrollDirection:
        if isinstance(value, cls):
            return value
        raw = getattr(value, "value", value)
        try:
            return cls(str(raw))
        except ValueError:
            return cls.DOWN


class CoordinateMode(str, Enum):
    API_PIXEL = "api_pixel"
    NORMALIZED_1000 = "normalized_1000"


class LLMBackend(str, Enum):
    LITELLM = "litellm"
    TINKER = "tinker"


@dataclass(frozen=True)
class Point:
    x: int = 0
    y: int = 0

    @classmethod
    def from_value(cls, value: object) -> Point | None:
        if not isinstance(value, (list, tuple)) or len(value) < 2:
            return None
        items = cast(list[Any] | tuple[Any, ...], value)
        return cls(int(items[0]), int(items[1]))

    def as_list(self) -> list[int]:
        return [self.x, self.y]


@dataclass(frozen=True)
class DesktopCommand:
    label: str
    action: DesktopAction | None
    coordinate: Point | None = None
    start_coordinate: Point | None = None
    text: str = ""
    key: str = ""
    direction: ScrollDirection = ScrollDirection.DOWN
    amount: int = 3
    duration: float = 1.0

    @classmethod
    def create(
        cls,
        action: DesktopAction,
        *,
        coordinate: Point | None = None,
        start_coordinate: Point | None = None,
        text: str = "",
        key: str = "",
        direction: ScrollDirection = ScrollDirection.DOWN,
        amount: int = 3,
        duration: float = 1.0,
    ) -> DesktopCommand:
        return cls(
            label=action.value,
            action=action,
            coordinate=coordinate,
            start_coordinate=start_coordinate,
            text=text,
            key=key,
            direction=direction,
            amount=amount,
            duration=duration,
        )

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> DesktopCommand:
        label = str(data.get("action", ""))
        direction = _scroll_direction(data.get("direction", ScrollDirection.DOWN.value))
        return cls(
            label=label,
            action=DesktopAction.parse(label),
            coordinate=Point.from_value(data.get("coordinate")),
            start_coordinate=Point.from_value(data.get("start_coordinate")),
            text=str(data.get("text", "")),
            key=str(data.get("key", "")),
            direction=direction,
            amount=int(data.get("amount", 3)),
            duration=float(data.get("duration", 1.0)),
        )

    @property
    def point(self) -> Point:
        return self.coordinate or Point()

    @property
    def start_point(self) -> Point:
        return self.start_coordinate or Point()

    def to_mapping(self) -> dict[str, Any]:
        data: dict[str, Any] = {"action": self.label}
        if self.coordinate is not None:
            data["coordinate"] = self.coordinate.as_list()
        if self.start_coordinate is not None:
            data["start_coordinate"] = self.start_coordinate.as_list()
        if self.text:
            data["text"] = self.text
        if self.key:
            data["key"] = self.key
        if self.action is DesktopAction.SCROLL:
            data["direction"] = self.direction.value
            data["amount"] = self.amount
        if self.action is DesktopAction.WAIT:
            data["duration"] = self.duration
        return data


def _scroll_direction(value: object) -> ScrollDirection:
    return ScrollDirection.parse(value)
