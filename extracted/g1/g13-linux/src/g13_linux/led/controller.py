"""
LED Controller

High-level LED control with effects support.
"""

import logging
import threading
import time
from collections.abc import Generator

from ..hardware.backlight import G13Backlight
from .colors import RGB
from .effects import EffectType, alert, fade, pulse, rainbow, solid

logger = logging.getLogger(__name__)


class LEDController:
    """
    LED controller with effects engine.

    Wraps G13Backlight and adds support for animated effects.
    """

    # Effect frame rate
    FPS = 30
    FRAME_INTERVAL = 1.0 / FPS

    def __init__(self, device=None, backlight: G13Backlight = None):
        """
        Initialize LED controller.

        Args:
            device: G13 device handle (creates backlight internally)
            backlight: Existing G13Backlight instance (preferred)
        """
        if backlight:
            self._backlight = backlight
        elif device:
            self._backlight = G13Backlight(device)
        else:
            self._backlight = G13Backlight(None)

        self._current_color = RGB(255, 255, 255)
        self._current_effect: EffectType | None = None
        self._effect_thread: threading.Thread | None = None
        self._effect_stop = threading.Event()
        self._effect_generator: Generator[RGB, None, None] | None = None
        self._lock = threading.Lock()

    @property
    def current_color(self) -> RGB:
        """Get current LED color."""
        return self._current_color

    @property
    def current_effect(self) -> EffectType | None:
        """Get currently running effect type."""
        return self._current_effect

    def set_color(self, r: int, g: int, b: int):
        """
        Set LED to solid color.

        Args:
            r: Red (0-255)
            g: Green (0-255)
            b: Blue (0-255)
        """
        self.stop_effect()
        self._current_color = RGB(r, g, b)
        self._apply_color(self._current_color)

    def set_rgb(self, color: RGB):
        """
        Set LED to RGB color.

        Args:
            color: RGB color instance
        """
        self.set_color(color.r, color.g, color.b)

    def set_hex(self, hex_string: str):
        """
        Set LED from hex color string.

        Args:
            hex_string: Color in #RRGGBB format
        """
        color = RGB.from_hex(hex_string)
        self.set_rgb(color)

    def set_named(self, color_name: str):
        """
        Set LED from named color.

        Args:
            color_name: Color name (e.g., 'red', 'blue')
        """
        color = RGB.from_name(color_name)
        self.set_rgb(color)

    def off(self):
        """Turn LED off (black)."""
        self.set_color(0, 0, 0)

    def get_current(self) -> RGB:
        """Get current color."""
        return self._current_color

    @property
    def brightness(self) -> int:
        """Get current brightness (0-100)."""
        return self._backlight.get_brightness()

    def set_brightness(self, level: int):
        """
        Set brightness level.

        Args:
            level: Brightness (0-100)
        """
        self._backlight.set_brightness(level)

    def start_effect(self, effect_type: EffectType, **params):
        """
        Start an LED effect.

        Args:
            effect_type: Type of effect to run
            **params: Effect-specific parameters
        """
        self.stop_effect()

        # Create generator for effect
        if effect_type == EffectType.SOLID:
            color = params.get("color", self._current_color)
            self._effect_generator = solid(color)
        elif effect_type == EffectType.PULSE:
            color = params.get("color", self._current_color)
            speed = params.get("speed", 1.0)
            self._effect_generator = pulse(color, speed)
        elif effect_type == EffectType.RAINBOW:
            speed = params.get("speed", 1.0)
            self._effect_generator = rainbow(speed)
        elif effect_type == EffectType.FADE:
            color1 = params.get("color1", RGB(255, 0, 0))
            color2 = params.get("color2", RGB(0, 0, 255))
            speed = params.get("speed", 1.0)
            self._effect_generator = fade(color1, color2, speed)
        elif effect_type == EffectType.ALERT:
            color = params.get("color", RGB(255, 0, 0))
            count = params.get("count", 3)
            self._effect_generator = alert(color, count)
        else:
            logger.warning(f"Unknown effect type: {effect_type}")
            return

        self._current_effect = effect_type
        self._effect_stop.clear()
        self._effect_thread = threading.Thread(
            target=self._effect_loop, daemon=True, name="LEDEffect"
        )
        self._effect_thread.start()
        logger.debug(f"Started effect: {effect_type.value}")

    def stop_effect(self):
        """Stop any running effect."""
        if self._effect_thread and self._effect_thread.is_alive():
            self._effect_stop.set()
            self._effect_thread.join(timeout=1.0)
            self._effect_thread = None

        self._current_effect = None
        self._effect_generator = None
        logger.debug("Effect stopped")

    def run_alert(self, color: RGB = None, count: int = 3, blocking: bool = True):
        """
        Run alert effect.

        Args:
            color: Flash color (default red)
            count: Number of flashes
            blocking: If True, wait for completion
        """
        if blocking:
            # Run synchronously
            gen = alert(color, count)
            for rgb in gen:
                self._apply_color(rgb)
                time.sleep(self.FRAME_INTERVAL)
        else:
            self.start_effect(EffectType.ALERT, color=color, count=count)

    def _effect_loop(self):
        """Background thread for running effects."""
        while not self._effect_stop.is_set():
            try:
                if self._effect_generator:
                    color = next(self._effect_generator)
                    self._apply_color(color)
                    self._current_color = color
                time.sleep(self.FRAME_INTERVAL)
            except StopIteration:
                # Finite effect completed
                logger.debug("Effect completed")
                self._current_effect = None
                break
            except Exception as e:
                logger.error(f"Effect error: {e}")
                break

    def _apply_color(self, color: RGB):
        """Send color to hardware."""
        with self._lock:
            self._backlight.set_color(color.r, color.g, color.b)
