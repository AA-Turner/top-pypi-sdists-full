"""
LED Settings Screens

LED color and effect configuration.
"""

from ...lcd.canvas import Canvas
from ...lcd.fonts import FONT_4X6, FONT_5X7
from ...led.colors import RGB
from ...led.effects import EffectType
from ..items import MenuItem
from ..screen import InputEvent, Screen
from .base_menu import MenuScreen
from .toast import ToastScreen


class LEDSettingsScreen(MenuScreen):
    """
    LED settings menu.

    Provides access to color, effect, and brightness settings.
    """

    def __init__(self, manager):
        """
        Initialize LED settings screen.

        Args:
            manager: ScreenManager instance
        """
        self.led = getattr(manager, "led_controller", None)

        items = [
            MenuItem(
                id="color",
                label="Color",
                value_getter=self._get_color_value,
                submenu=lambda: ColorPickerScreen(manager),
            ),
            MenuItem(
                id="brightness",
                label="Brightness",
                value_getter=self._get_brightness_value,
                submenu=lambda: BrightnessScreen(manager),
            ),
            MenuItem(
                id="effect",
                label="Effect",
                value_getter=self._get_effect_value,
                submenu=lambda: EffectSelectScreen(manager),
            ),
            MenuItem(
                id="off",
                label="Turn Off",
                action=self._turn_off,
            ),
        ]
        super().__init__(manager, "LED SETTINGS", items)

    def _get_color_value(self) -> str:
        """Get current color as hex string."""
        if self.led:
            return self.led.current_color.to_hex()
        return "#FFFFFF"

    def _get_brightness_value(self) -> str:
        """Get current brightness as percentage."""
        if self.led:
            return f"{self.led.brightness}%"
        return "100%"

    def _get_effect_value(self) -> str:
        """Get current effect name."""
        if self.led and self.led.current_effect:
            return self.led.current_effect.value
        return "None"

    def _turn_off(self):
        """Turn LED off."""
        if self.led:
            self.led.off()
        toast = ToastScreen(self.manager, "LED Off")
        self.manager.show_overlay(toast, duration=1.5)
        self.mark_dirty()


class ColorPickerScreen(Screen):
    """
    Color picker with preset colors.

    Navigate through preset colors with left/right.
    """

    PRESETS = [
        ("Red", RGB(255, 0, 0)),
        ("Orange", RGB(255, 128, 0)),
        ("Yellow", RGB(255, 255, 0)),
        ("Green", RGB(0, 255, 0)),
        ("Cyan", RGB(0, 255, 255)),
        ("Blue", RGB(0, 0, 255)),
        ("Purple", RGB(128, 0, 255)),
        ("Magenta", RGB(255, 0, 255)),
        ("Pink", RGB(255, 105, 180)),
        ("White", RGB(255, 255, 255)),
    ]

    def __init__(self, manager):
        """
        Initialize color picker.

        Args:
            manager: ScreenManager instance
        """
        super().__init__(manager)
        self.selected = 0
        self.led = getattr(manager, "led_controller", None)

        # Find current color in presets
        if self.led:
            current = self.led.current_color
            for i, (name, color) in enumerate(self.PRESETS):
                if color.r == current.r and color.g == current.g and color.b == current.b:
                    self.selected = i
                    break

    def on_input(self, event: InputEvent) -> bool:
        """Handle navigation input."""
        if event == InputEvent.STICK_LEFT:
            self.selected = (self.selected - 1) % len(self.PRESETS)
            self._preview_color()
            return True
        elif event == InputEvent.STICK_RIGHT:
            self.selected = (self.selected + 1) % len(self.PRESETS)
            self._preview_color()
            return True
        elif event == InputEvent.STICK_PRESS:
            self._apply_color()
            self.manager.pop()
            return True
        elif event == InputEvent.BUTTON_BD:
            self.manager.pop()
            return True
        return False

    def _preview_color(self):
        """Apply color preview."""
        if self.led:
            _, color = self.PRESETS[self.selected]
            self.led.set_rgb(color)
        self.mark_dirty()

    def _apply_color(self):
        """Apply selected color permanently."""
        if self.led:
            self.led.stop_effect()  # Stop any running effect
            name, color = self.PRESETS[self.selected]
            self.led.set_rgb(color)
            toast = ToastScreen(self.manager, f"Color: {name}")
            self.manager.show_overlay(toast, duration=1.5)

    def render(self, canvas: Canvas):
        """Render color picker."""
        canvas.draw_text(0, 0, "SELECT COLOR", FONT_5X7)
        canvas.draw_hline(0, 9, canvas.WIDTH)

        name, color = self.PRESETS[self.selected]

        # Draw color name large
        canvas.draw_text_centered(18, name, FONT_5X7)

        # Draw hex value and navigation hints
        hint = f"< {color.to_hex()} >"
        canvas.draw_text_centered(30, hint, FONT_4X6)

        # Color indicator (simple bar showing approximate color)
        bar_y = 38
        bar_height = 4
        # Draw proportional RGB bars
        r_width = color.r * 50 // 255
        g_width = color.g * 50 // 255
        b_width = color.b * 50 // 255

        canvas.draw_rect(10, bar_y, r_width, bar_height, filled=True)
        canvas.draw_rect(60, bar_y, g_width, bar_height, filled=True)
        canvas.draw_rect(110, bar_y, b_width, bar_height, filled=True)


class EffectSelectScreen(MenuScreen):
    """
    Effect selection screen.
    """

    def __init__(self, manager):
        """
        Initialize effect selector.

        Args:
            manager: ScreenManager instance
        """
        self.led = getattr(manager, "led_controller", None)

        items = [
            MenuItem(
                id="solid",
                label="Solid",
                action=lambda: self._set_effect(EffectType.SOLID),
            ),
            MenuItem(
                id="pulse",
                label="Pulse",
                action=lambda: self._set_effect(EffectType.PULSE),
            ),
            MenuItem(
                id="rainbow",
                label="Rainbow",
                action=lambda: self._set_effect(EffectType.RAINBOW),
            ),
            MenuItem(
                id="fade",
                label="Fade",
                action=lambda: self._set_effect(EffectType.FADE),
            ),
            MenuItem(
                id="none",
                label="Stop Effect",
                action=self._stop_effect,
            ),
        ]
        super().__init__(manager, "EFFECTS", items)

    def _set_effect(self, effect: EffectType):
        """
        Set LED effect.

        Args:
            effect: Effect type to start
        """
        if not self.led:
            return

        effect_name = "Solid"
        if effect == EffectType.SOLID:
            self.led.stop_effect()
        elif effect == EffectType.PULSE:
            self.led.start_effect(EffectType.PULSE, speed=1.0)
            effect_name = "Pulse"
        elif effect == EffectType.RAINBOW:
            self.led.start_effect(EffectType.RAINBOW, speed=0.5)
            effect_name = "Rainbow"
        elif effect == EffectType.FADE:
            self.led.start_effect(
                EffectType.FADE,
                color1=RGB(255, 0, 0),
                color2=RGB(0, 0, 255),
                speed=0.5,
            )
            effect_name = "Fade"

        self.manager.pop()
        toast = ToastScreen(self.manager, f"Effect: {effect_name}")
        self.manager.show_overlay(toast, duration=1.5)

    def _stop_effect(self):
        """Stop current effect."""
        if self.led:
            self.led.stop_effect()
        self.manager.pop()
        toast = ToastScreen(self.manager, "Effect stopped")
        self.manager.show_overlay(toast, duration=1.5)


class BrightnessScreen(Screen):
    """
    Brightness adjustment screen.

    Adjust brightness with left/right, in 10% increments.
    """

    def __init__(self, manager):
        """
        Initialize brightness screen.

        Args:
            manager: ScreenManager instance
        """
        super().__init__(manager)
        self.led = getattr(manager, "led_controller", None)
        self.brightness = 100
        if self.led:
            self.brightness = self.led.brightness

    def on_input(self, event: InputEvent) -> bool:
        """Handle navigation input."""
        if event == InputEvent.STICK_LEFT:
            self.brightness = max(0, self.brightness - 10)
            self._preview_brightness()
            return True
        elif event == InputEvent.STICK_RIGHT:
            self.brightness = min(100, self.brightness + 10)
            self._preview_brightness()
            return True
        elif event == InputEvent.STICK_PRESS:
            self._apply_brightness()
            self.manager.pop()
            return True
        elif event == InputEvent.BUTTON_BD:
            # Restore original brightness on cancel
            if self.led:
                self.led.set_brightness(self.led.brightness)
            self.manager.pop()
            return True
        return False

    def _preview_brightness(self):
        """Apply brightness preview."""
        if self.led:
            self.led.set_brightness(self.brightness)
        self.mark_dirty()

    def _apply_brightness(self):
        """Apply selected brightness."""
        if self.led:
            self.led.set_brightness(self.brightness)
            toast = ToastScreen(self.manager, f"Brightness: {self.brightness}%")
            self.manager.show_overlay(toast, duration=1.5)

    def render(self, canvas: Canvas):
        """Render brightness screen."""
        canvas.draw_text(0, 0, "BRIGHTNESS", FONT_5X7)
        canvas.draw_hline(0, 9, canvas.WIDTH)

        # Draw percentage large
        canvas.draw_text_centered(18, f"{self.brightness}%", FONT_5X7)

        # Draw navigation hint
        canvas.draw_text_centered(30, "< Adjust >", FONT_4X6)

        # Draw brightness bar
        bar_x = 10
        bar_y = 38
        bar_width = 140
        bar_height = 4
        fill_width = int(bar_width * self.brightness / 100)

        # Outline
        canvas.draw_rect(bar_x, bar_y, bar_width, bar_height, filled=False)
        # Fill
        if fill_width > 0:
            canvas.draw_rect(bar_x, bar_y, fill_width, bar_height, filled=True)
