"""Macro data types for G13LogitechOPS."""

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum


class MacroStepType(Enum):
    """Types of macro steps."""

    KEY_PRESS = "key_press"
    KEY_RELEASE = "key_release"
    G13_BUTTON = "g13_button"
    DELAY = "delay"


class PlaybackMode(Enum):
    """How timing is handled during playback."""

    RECORDED = "recorded"  # Use original recorded timing
    FIXED = "fixed"  # Fixed delay between steps
    AS_FAST = "as_fast"  # No delays


class InputSource(Enum):
    """What input sources to capture during recording."""

    G13_ONLY = "g13_only"
    SYSTEM_ONLY = "system_only"
    BOTH = "both"


@dataclass
class MacroStep:
    """Single step in a macro sequence."""

    step_type: MacroStepType
    value: str | int  # KEY_A, G1, or delay_ms
    is_press: bool = True  # True for press/down, False for release/up
    timestamp_ms: int = 0  # Relative time from macro start

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dict."""
        return {
            "type": self.step_type.value,
            "value": self.value,
            "is_press": self.is_press,
            "timestamp_ms": self.timestamp_ms,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MacroStep":
        """Deserialize from dict."""
        return cls(
            step_type=MacroStepType(data["type"]),
            value=data["value"],
            is_press=data.get("is_press", True),
            timestamp_ms=data.get("timestamp_ms", 0),
        )

    def __str__(self) -> str:
        action = "+" if self.is_press else "-"
        return f"{self.timestamp_ms:6d}ms {action}{self.value}"


@dataclass
class Macro:
    """Complete macro definition with metadata and steps."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Untitled Macro"
    description: str = ""
    steps: list[MacroStep] = field(default_factory=list)

    # Playback settings
    speed_multiplier: float = 1.0  # 0.5 = half speed, 2.0 = double
    repeat_count: int = 1  # 0 = infinite
    repeat_delay_ms: int = 0  # Delay between repeats
    playback_mode: PlaybackMode = PlaybackMode.RECORDED
    fixed_delay_ms: int = 10  # For FIXED playback mode

    # Assignment
    assigned_button: str | None = None  # e.g., "G5"
    global_hotkey: str | None = None  # e.g., "Ctrl+Shift+F1"

    # Metadata
    created_at: str = ""
    modified_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        if isinstance(self.playback_mode, str):
            self.playback_mode = PlaybackMode(self.playback_mode)

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dict."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "steps": [step.to_dict() for step in self.steps],
            "speed_multiplier": self.speed_multiplier,
            "repeat_count": self.repeat_count,
            "repeat_delay_ms": self.repeat_delay_ms,
            "playback_mode": self.playback_mode.value,
            "fixed_delay_ms": self.fixed_delay_ms,
            "assigned_button": self.assigned_button,
            "global_hotkey": self.global_hotkey,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Macro":
        """Deserialize from dict."""
        steps = [MacroStep.from_dict(s) for s in data.get("steps", [])]
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", "Untitled"),
            description=data.get("description", ""),
            steps=steps,
            speed_multiplier=data.get("speed_multiplier", 1.0),
            repeat_count=data.get("repeat_count", 1),
            repeat_delay_ms=data.get("repeat_delay_ms", 0),
            playback_mode=PlaybackMode(data.get("playback_mode", "recorded")),
            fixed_delay_ms=data.get("fixed_delay_ms", 10),
            assigned_button=data.get("assigned_button"),
            global_hotkey=data.get("global_hotkey"),
            created_at=data.get("created_at", ""),
            modified_at=data.get("modified_at", ""),
        )

    @property
    def duration_ms(self) -> int:
        """Total duration based on step timestamps."""
        if not self.steps:
            return 0
        return max(step.timestamp_ms for step in self.steps)

    @property
    def step_count(self) -> int:
        """Number of steps in macro."""
        return len(self.steps)

    def add_step(
        self,
        step_type: MacroStepType,
        value: str | int,
        is_press: bool = True,
        timestamp_ms: int = 0,
    ) -> MacroStep:
        """Add a step to the macro."""
        step = MacroStep(
            step_type=step_type,
            value=value,
            is_press=is_press,
            timestamp_ms=timestamp_ms,
        )
        self.steps.append(step)
        return step

    def clear_steps(self):
        """Remove all steps."""
        self.steps.clear()
