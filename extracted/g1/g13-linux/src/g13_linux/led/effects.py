"""
LED Effects Engine

Generator-based effects for LED animations.
"""

import math
import time
from collections.abc import Generator
from enum import Enum

from .colors import RGB, blend, dim, hsv_to_rgb


class EffectType(Enum):
    """Available LED effect types."""

    SOLID = "solid"
    PULSE = "pulse"
    RAINBOW = "rainbow"
    FADE = "fade"
    ALERT = "alert"


def solid(color: RGB) -> Generator[RGB, None, None]:
    """
    Solid color effect - yields the same color forever.

    Args:
        color: The color to display

    Yields:
        The same RGB color indefinitely
    """
    while True:
        yield color


def pulse(color: RGB, speed: float = 1.0) -> Generator[RGB, None, None]:
    """
    Breathing/pulse effect - fades in and out.

    Args:
        color: Base color to pulse
        speed: Cycles per second (default 1.0)

    Yields:
        RGB colors varying in brightness
    """
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        # Sine wave oscillation between 0.2 and 1.0 brightness
        phase = (math.sin(elapsed * speed * 2 * math.pi) + 1) / 2
        brightness = 0.2 + phase * 0.8
        yield dim(color, 1.0 - brightness)


def rainbow(speed: float = 1.0) -> Generator[RGB, None, None]:
    """
    Rainbow effect - cycles through the color spectrum.

    Args:
        speed: Full cycles per second (default 1.0)

    Yields:
        RGB colors cycling through hue
    """
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        hue = (elapsed * speed) % 1.0
        yield hsv_to_rgb(hue, 1.0, 1.0)


def fade(color1: RGB, color2: RGB, speed: float = 1.0) -> Generator[RGB, None, None]:
    """
    Fade effect - transitions between two colors.

    Args:
        color1: First color
        color2: Second color
        speed: Full fade cycles per second (default 1.0)

    Yields:
        RGB colors blending between the two
    """
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        # Oscillate between 0 and 1
        phase = (math.sin(elapsed * speed * 2 * math.pi) + 1) / 2
        yield blend(color1, color2, phase)


def alert(color: RGB = None, count: int = 3) -> Generator[RGB, None, None]:
    """
    Alert effect - flashes color on/off.

    This is a finite generator that completes after count flashes.

    Args:
        color: Flash color (default red)
        count: Number of flashes (default 3)

    Yields:
        RGB colors alternating between color and black
    """
    if color is None:
        color = RGB(255, 0, 0)

    black = RGB(0, 0, 0)
    flash_duration = 0.15  # seconds

    for _ in range(count):
        # Flash on
        on_start = time.time()
        while time.time() - on_start < flash_duration:
            yield color
        # Flash off
        off_start = time.time()
        while time.time() - off_start < flash_duration:
            yield black


def strobe(color: RGB, frequency: float = 10.0) -> Generator[RGB, None, None]:
    """
    Strobe effect - rapid on/off flashing.

    Args:
        color: Strobe color
        frequency: Flashes per second (default 10)

    Yields:
        RGB colors alternating rapidly
    """
    black = RGB(0, 0, 0)
    period = 1.0 / frequency
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        # On during first half of period
        phase = (elapsed % period) / period
        yield color if phase < 0.5 else black


def candle(base_color: RGB = None, flicker_intensity: float = 0.3) -> Generator[RGB, None, None]:
    """
    Candle flicker effect - simulates flickering flame.

    Args:
        base_color: Base flame color (default warm orange)
        flicker_intensity: How much brightness varies (0.0-1.0)

    Yields:
        RGB colors simulating candle flicker
    """
    import random

    if base_color is None:
        base_color = RGB(255, 100, 20)

    while True:
        # Random brightness variation
        flicker = 1.0 - random.random() * flicker_intensity
        yield dim(base_color, 1.0 - flicker)
