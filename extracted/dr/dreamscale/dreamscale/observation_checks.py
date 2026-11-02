"""Observation checks shared by the robot helpers: run before any network call, and every
message names the field, what was given and what the model expects, with units."""

from __future__ import annotations

import math
import time
from collections.abc import Sequence
from typing import Any

import numpy as np

from dreamscale.errors import observation_error

EXPECTED_FRAME = "an RGB image, H×W×3 uint8"


def describe(value: Any) -> str:
    """What was passed, in the words the error uses: ``480×640×4 uint8`` or ``list``."""
    if isinstance(value, np.ndarray):
        shape = "×".join(str(dim) for dim in value.shape) or "scalar"
        return f"{shape} {value.dtype}"
    return type(value).__name__


def check_frame(name: str, frame: Any) -> np.ndarray:
    if not isinstance(frame, np.ndarray):
        raise observation_error(name, describe(frame), EXPECTED_FRAME)
    if frame.ndim != 3 or frame.shape[2] != 3 or frame.dtype != np.uint8:
        raise observation_error(name, describe(frame), EXPECTED_FRAME)
    if frame.shape[0] <= 0 or frame.shape[1] <= 0:
        raise observation_error(name, describe(frame), EXPECTED_FRAME)
    return frame


def check_values(name: str, values: Any, count: int, expected: str) -> tuple[float, ...]:
    """``count`` finite numbers; ``expected`` says what they are, in order, with units."""
    if isinstance(values, (str, bytes)) or not isinstance(values, (Sequence, np.ndarray)):
        raise observation_error(name, describe(values), f"{count} values: {expected}")
    raw = tuple(values)
    if len(raw) != count:
        raise observation_error(name, f"{len(raw)} values", f"{count} values: {expected}")
    if any(isinstance(value, (bool, np.bool_)) for value in raw):
        raise observation_error(name, "booleans", f"{count} numbers: {expected}")
    try:
        converted = tuple(float(value) for value in raw)
    except (TypeError, ValueError, OverflowError):
        raise observation_error(
            name, "non-numeric values", f"{count} numbers: {expected}"
        ) from None
    if any(not math.isfinite(value) for value in converted):
        raise observation_error(name, "non-finite values", f"{count} finite numbers: {expected}")
    return converted


def check_actions_remaining(actions_remaining: Any) -> int:
    if isinstance(actions_remaining, bool) or not isinstance(actions_remaining, int):
        raise TypeError("actions_remaining must be a nonnegative integer")
    if actions_remaining < 0:
        raise ValueError("actions_remaining must be a nonnegative integer")
    return actions_remaining


EXPECTED_CAPTURE_TIME = "when the frames were captured: this computer's time.time_ns(), not later"


def check_capture_time_ns(capture_time_ns: Any) -> int | None:
    """When the frames and state were captured, on this computer's ``time.time_ns()`` clock
    (the requests' clock). None stamps the moment the request is built."""
    if capture_time_ns is None:
        return None
    if isinstance(capture_time_ns, (bool, np.bool_)) or not isinstance(
        capture_time_ns, (int, np.integer)
    ):
        raise observation_error(
            "capture_time_ns", describe(capture_time_ns), f"an integer: {EXPECTED_CAPTURE_TIME}"
        )
    value = int(capture_time_ns)
    if value <= 0 or value > time.time_ns():
        raise observation_error("capture_time_ns", str(value), EXPECTED_CAPTURE_TIME)
    return value
