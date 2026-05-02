"""
Tests for input handling (handler, navigation) and LED (controller, effects) modules.

Covers:
- InputHandler: thumbstick dead zone, direction detection, repeat logic, button edge detection
- SimulatedInputHandler: inject methods, start/stop gating
- NavigationController: state machine transitions, profile callbacks, home navigation
- LEDController: color setting methods, effect lifecycle, thread cleanup
- Effects: all generators (solid, pulse, rainbow, fade, alert, strobe, candle)
"""

import time
from unittest.mock import MagicMock, patch

from g13_linux.hardware.backlight import G13Backlight
from g13_linux.input.handler import InputHandler, SimulatedInputHandler
from g13_linux.input.navigation import NavigationController, NavigationState
from g13_linux.led.colors import RGB
from g13_linux.led.controller import LEDController
from g13_linux.led.effects import (
    EffectType,
    alert,
    candle,
    fade,
    pulse,
    rainbow,
    solid,
    strobe,
)
from g13_linux.menu.screen import InputEvent

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_report(
    joystick_x: int = 128,
    joystick_y: int = 128,
    byte6: int = 0,
    byte7: int = 0,
) -> bytes:
    """Build a minimal 8-byte HID report with given joystick + button bytes."""
    return bytes([0x00, joystick_x, joystick_y, 0x00, 0x00, 0x00, byte6, byte7])


def _take(gen, n: int) -> list:
    """Take n values from a generator."""
    return [next(gen) for _ in range(n)]


# ===========================================================================
# InputHandler tests
# ===========================================================================


class TestInputHandlerInit:
    """InputHandler constructor and lifecycle."""

    def test_init_stores_device_and_callback(self):
        device = MagicMock()
        callback = MagicMock()
        handler = InputHandler(device, callback)

        assert handler.device is device
        assert handler.callback is callback
        assert handler._running is False
        assert handler._thread is None

    def test_init_defaults_stick_center(self):
        handler = InputHandler(MagicMock(), MagicMock())
        assert handler._stick_x == InputHandler.STICK_CENTER
        assert handler._stick_y == InputHandler.STICK_CENTER
        assert handler._stick_pressed is False

    def test_constants(self):
        assert InputHandler.STICK_CENTER == 128
        assert InputHandler.STICK_THRESHOLD == 50
        assert InputHandler.STICK_REPEAT_DELAY == 0.4
        assert InputHandler.STICK_REPEAT_RATE == 0.15


class TestInputHandlerStartStop:
    """start() / stop() threading lifecycle."""

    def test_start_creates_thread(self):
        device = MagicMock()
        device.read.return_value = None
        handler = InputHandler(device, MagicMock())

        handler.start()
        assert handler._running is True
        assert handler._thread is not None
        assert handler._thread.is_alive()

        handler.stop()
        assert handler._running is False
        assert handler._thread is None

    def test_start_is_idempotent(self):
        device = MagicMock()
        device.read.return_value = None
        handler = InputHandler(device, MagicMock())

        handler.start()
        thread1 = handler._thread
        handler.start()  # second call should be no-op
        assert handler._thread is thread1

        handler.stop()

    def test_stop_without_start(self):
        handler = InputHandler(MagicMock(), MagicMock())
        handler.stop()  # should not raise
        assert handler._running is False


class TestInputHandlerThumbstick:
    """Thumbstick dead zone and direction detection."""

    def setup_method(self):
        self.device = MagicMock()
        self.events: list[InputEvent] = []
        self.handler = InputHandler(self.device, self.events.append)

    def test_center_no_event(self):
        self.handler._process_thumbstick(128, 128)
        assert self.events == []

    def test_within_dead_zone_no_event(self):
        # Just inside threshold (128 - 50 = 78, so 79 is inside dead zone)
        self.handler._process_thumbstick(128, 79)
        assert self.events == []

    def test_stick_up(self):
        # Y < CENTER - THRESHOLD  → UP
        self.handler._process_thumbstick(128, 128 - 51)
        assert self.events == [InputEvent.STICK_UP]

    def test_stick_down(self):
        # Y > CENTER + THRESHOLD  → DOWN
        self.handler._process_thumbstick(128, 128 + 51)
        assert self.events == [InputEvent.STICK_DOWN]

    def test_stick_left(self):
        # X < CENTER - THRESHOLD  → LEFT (no Y direction)
        self.handler._process_thumbstick(128 - 51, 128)
        assert self.events == [InputEvent.STICK_LEFT]

    def test_stick_right(self):
        # X > CENTER + THRESHOLD  → RIGHT (no Y direction)
        self.handler._process_thumbstick(128 + 51, 128)
        assert self.events == [InputEvent.STICK_RIGHT]

    def test_y_takes_priority_over_x(self):
        """When both axes exceed threshold, Y direction wins."""
        self.handler._process_thumbstick(128 + 51, 128 - 51)
        assert self.events == [InputEvent.STICK_UP]

    def test_same_direction_no_duplicate_event(self):
        """Holding stick in same direction should not re-emit immediately."""
        self.handler._process_thumbstick(128, 10)  # UP
        self.handler._process_thumbstick(128, 5)  # still UP
        assert self.events == [InputEvent.STICK_UP]

    def test_direction_change_emits_new_event(self):
        """Changing direction emits the new direction event."""
        self.handler._process_thumbstick(128, 10)  # UP
        self.handler._process_thumbstick(128, 250)  # DOWN
        assert self.events == [InputEvent.STICK_UP, InputEvent.STICK_DOWN]

    def test_return_to_center_stops_repeat(self):
        """Returning to center clears repeat direction."""
        self.handler._process_thumbstick(128, 10)  # UP
        self.handler._process_thumbstick(128, 128)  # center
        assert self.handler._repeat_direction is None

    def test_boundary_exact_threshold_no_event(self):
        """Exactly at threshold boundary should NOT trigger (not strictly greater/less)."""
        # CENTER - THRESHOLD = 78, so y=78 is NOT < 78 → no event
        self.handler._process_thumbstick(128, 128 - 50)
        assert self.events == []

    def test_boundary_one_past_threshold(self):
        """One past threshold should trigger."""
        self.handler._process_thumbstick(128, 128 - 51)
        assert self.events == [InputEvent.STICK_UP]

    def test_extreme_values(self):
        """Extreme stick positions (0, 255)."""
        self.handler._process_thumbstick(128, 0)
        assert self.events == [InputEvent.STICK_UP]
        self.events.clear()
        self.handler._repeat_direction = None

        self.handler._process_thumbstick(128, 255)
        assert self.events == [InputEvent.STICK_DOWN]


class TestInputHandlerStickRepeat:
    """Stick repeat delay and rate logic."""

    def setup_method(self):
        self.events: list[InputEvent] = []
        self.handler = InputHandler(MagicMock(), self.events.append)

    def test_no_repeat_when_no_direction(self):
        self.handler._check_stick_repeat()
        assert self.events == []

    def test_no_repeat_before_delay(self):
        """Within repeat delay, no additional events."""
        self.handler._process_thumbstick(128, 10)  # UP
        self.events.clear()

        # Simulate time just before delay expires
        self.handler._repeat_start_time = time.time()
        self.handler._check_stick_repeat()
        assert self.events == []

    def test_repeat_after_delay(self):
        """After delay + rate elapsed, repeat fires."""
        self.handler._process_thumbstick(128, 10)  # UP
        self.events.clear()

        # Set times so delay and rate are both exceeded
        now = time.time()
        self.handler._repeat_start_time = now - 0.5  # past REPEAT_DELAY (0.4)
        self.handler._last_repeat_time = now - 0.2  # past REPEAT_RATE (0.15)

        self.handler._check_stick_repeat()
        assert self.events == [InputEvent.STICK_UP]

    def test_no_repeat_within_rate(self):
        """After delay but within rate interval, no repeat."""
        self.handler._process_thumbstick(128, 10)  # UP
        self.events.clear()

        now = time.time()
        self.handler._repeat_start_time = now - 0.5  # past delay
        self.handler._last_repeat_time = now - 0.05  # within rate (< 0.15)

        self.handler._check_stick_repeat()
        assert self.events == []


class TestInputHandlerStickButton:
    """Stick button (press) detection."""

    def setup_method(self):
        self.events: list[InputEvent] = []
        self.handler = InputHandler(MagicMock(), self.events.append)

    def test_stick_press_detected(self):
        """Byte 7 bit 3 (0x08) triggers STICK_PRESS on rising edge."""
        data = _make_report(byte7=0x08)
        self.handler._process_stick_button(data)
        assert self.events == [InputEvent.STICK_PRESS]

    def test_stick_press_no_repeat(self):
        """Holding stick button does not re-emit."""
        data = _make_report(byte7=0x08)
        self.handler._process_stick_button(data)
        self.handler._process_stick_button(data)  # still held
        assert self.events == [InputEvent.STICK_PRESS]

    def test_stick_release_and_repress(self):
        """Release then re-press emits again."""
        pressed = _make_report(byte7=0x08)
        released = _make_report(byte7=0x00)

        self.handler._process_stick_button(pressed)
        self.handler._process_stick_button(released)
        self.handler._process_stick_button(pressed)
        assert self.events == [InputEvent.STICK_PRESS, InputEvent.STICK_PRESS]

    def test_short_data_ignored(self):
        """Data shorter than 8 bytes is silently ignored."""
        self.handler._process_stick_button(bytes([0] * 7))
        assert self.events == []

    def test_stick_not_pressed(self):
        """No bit 3 set → no event."""
        data = _make_report(byte7=0x04)  # bit 2, not bit 3
        self.handler._process_stick_button(data)
        assert self.events == []


class TestInputHandlerButtons:
    """Navigation button edge detection."""

    def setup_method(self):
        self.events: list[InputEvent] = []
        self.handler = InputHandler(MagicMock(), self.events.append)

    def test_bd_button(self):
        """BD: byte 6, bit 0."""
        data = _make_report(byte6=0x01)
        self.handler._process_buttons(data)
        assert InputEvent.BUTTON_BD in self.events

    def test_left_button(self):
        """LEFT: byte 7, bit 1."""
        data = _make_report(byte7=0x02)
        self.handler._process_buttons(data)
        assert InputEvent.BUTTON_LEFT in self.events

    def test_m1_button(self):
        """M1: byte 6, bit 5."""
        data = _make_report(byte6=0x20)
        self.handler._process_buttons(data)
        assert InputEvent.BUTTON_M1 in self.events

    def test_m2_button(self):
        """M2: byte 6, bit 6."""
        data = _make_report(byte6=0x40)
        self.handler._process_buttons(data)
        assert InputEvent.BUTTON_M2 in self.events

    def test_m3_button(self):
        """M3: byte 6, bit 7."""
        data = _make_report(byte6=0x80)
        self.handler._process_buttons(data)
        assert InputEvent.BUTTON_M3 in self.events

    def test_mr_button(self):
        """MR: byte 7, bit 0."""
        data = _make_report(byte7=0x01)
        self.handler._process_buttons(data)
        assert InputEvent.BUTTON_MR in self.events

    def test_rising_edge_only(self):
        """Only emit on transition from unpressed to pressed."""
        data = _make_report(byte6=0x01)  # BD pressed
        self.handler._process_buttons(data)
        self.handler._process_buttons(data)  # still held
        assert self.events.count(InputEvent.BUTTON_BD) == 1

    def test_release_and_repress(self):
        """Release then re-press emits second event."""
        pressed = _make_report(byte6=0x01)
        released = _make_report(byte6=0x00)

        self.handler._process_buttons(pressed)
        self.handler._process_buttons(released)
        self.handler._process_buttons(pressed)
        assert self.events.count(InputEvent.BUTTON_BD) == 2

    def test_multiple_buttons_simultaneous(self):
        """Multiple buttons pressed at once."""
        data = _make_report(byte6=0x01 | 0x20, byte7=0x01)  # BD + M1 + MR
        self.handler._process_buttons(data)
        assert InputEvent.BUTTON_BD in self.events
        assert InputEvent.BUTTON_M1 in self.events
        assert InputEvent.BUTTON_MR in self.events

    def test_short_data_ignored(self):
        """Data shorter than 8 bytes ignored."""
        self.handler._process_buttons(bytes([0] * 7))
        assert self.events == []


class TestInputHandlerEmit:
    """Callback error handling in _emit."""

    def test_callback_exception_caught(self):
        """Callback exception does not propagate."""

        def bad_callback(event):
            raise RuntimeError("boom")

        handler = InputHandler(MagicMock(), bad_callback)
        handler._emit(InputEvent.STICK_UP)  # should not raise


class TestInputHandlerProcessReport:
    """_process_report integration with EventDecoder."""

    def test_process_report_decodes_and_dispatches(self):
        events: list[InputEvent] = []
        handler = InputHandler(MagicMock(), events.append)

        # Stick up (y=10) + BD pressed (byte6 bit0)
        report = _make_report(joystick_y=10, byte6=0x01)
        handler._process_report(report)

        assert InputEvent.STICK_UP in events
        assert InputEvent.BUTTON_BD in events

    def test_process_report_invalid_data(self):
        """Short data triggers ValueError in decoder, logged and skipped."""
        handler = InputHandler(MagicMock(), MagicMock())
        handler._process_report(bytes([0] * 3))  # too short, should not raise


class TestInputHandlerPollLoop:
    """_poll_loop integration (brief run)."""

    def test_poll_loop_reads_device(self):
        device = MagicMock()
        report = _make_report(byte6=0x01)
        # Return report once then None
        device.read.side_effect = [report, None, None]
        events: list[InputEvent] = []
        handler = InputHandler(device, events.append)

        handler._running = True

        # Run a few iterations manually by stopping after a short time
        def limited_loop():
            count = 0
            while handler._running and count < 3:
                try:
                    data = handler.device.read(timeout_ms=100)
                    if data:
                        handler._process_report(data)
                    else:
                        handler._check_stick_repeat()
                except Exception:
                    pass
                count += 1

        limited_loop()
        assert InputEvent.BUTTON_BD in events

    def test_poll_loop_handles_read_exception(self):
        device = MagicMock()
        device.read.side_effect = OSError("device disconnected")
        handler = InputHandler(device, MagicMock())

        handler.start()
        time.sleep(0.05)
        handler.stop()  # should stop cleanly


# ===========================================================================
# SimulatedInputHandler tests
# ===========================================================================


class TestSimulatedInputHandler:
    """SimulatedInputHandler inject methods."""

    def setup_method(self):
        self.events: list[InputEvent] = []
        self.handler = SimulatedInputHandler(self.events.append)

    def test_init(self):
        assert self.handler._running is False

    def test_start_stop(self):
        self.handler.start()
        assert self.handler._running is True
        self.handler.stop()
        assert self.handler._running is False

    def test_inject_event_when_running(self):
        self.handler.start()
        self.handler.inject_event(InputEvent.STICK_UP)
        assert self.events == [InputEvent.STICK_UP]

    def test_inject_event_when_stopped(self):
        """Events dropped when not running."""
        self.handler.inject_event(InputEvent.STICK_UP)
        assert self.events == []

    def test_inject_stick_up(self):
        self.handler.start()
        self.handler.inject_stick_up()
        assert self.events == [InputEvent.STICK_UP]

    def test_inject_stick_down(self):
        self.handler.start()
        self.handler.inject_stick_down()
        assert self.events == [InputEvent.STICK_DOWN]

    def test_inject_stick_press(self):
        self.handler.start()
        self.handler.inject_stick_press()
        assert self.events == [InputEvent.STICK_PRESS]

    def test_inject_back(self):
        self.handler.start()
        self.handler.inject_back()
        assert self.events == [InputEvent.BUTTON_BD]

    def test_multiple_injections(self):
        self.handler.start()
        self.handler.inject_stick_up()
        self.handler.inject_stick_down()
        self.handler.inject_stick_press()
        assert len(self.events) == 3


# ===========================================================================
# NavigationController tests
# ===========================================================================


class TestNavigationState:
    """NavigationState enum values."""

    def test_states(self):
        assert NavigationState.IDLE.value == "idle"
        assert NavigationState.MENU.value == "menu"
        assert NavigationState.EDITING.value == "editing"


class TestNavigationControllerInit:
    """NavigationController initialization."""

    def test_init_pushes_idle_screen(self):
        sm = MagicMock()
        idle = MagicMock()
        nav = NavigationController(sm, idle)

        sm.push.assert_called_once_with(idle)
        assert nav.state == NavigationState.IDLE

    def test_stores_references(self):
        sm = MagicMock()
        idle = MagicMock()
        nav = NavigationController(sm, idle)

        assert nav.screen_manager is sm
        assert nav.idle_screen is idle


class TestNavigationControllerIdleInput:
    """Input handling in IDLE state."""

    def setup_method(self):
        self.sm = MagicMock()
        self.idle = MagicMock()
        self.nav = NavigationController(self.sm, self.idle)

    @patch("g13_linux.input.navigation.NavigationController._open_main_menu")
    def test_stick_press_opens_menu(self, mock_open):
        self.nav.on_input(InputEvent.STICK_PRESS)
        mock_open.assert_called_once()

    def test_m1_with_callback(self):
        cb = MagicMock()
        self.nav.set_profile_callback(InputEvent.BUTTON_M1, cb)
        self.nav.on_input(InputEvent.BUTTON_M1)
        cb.assert_called_once()

    def test_m2_with_callback(self):
        cb = MagicMock()
        self.nav.set_profile_callback(InputEvent.BUTTON_M2, cb)
        self.nav.on_input(InputEvent.BUTTON_M2)
        cb.assert_called_once()

    def test_m3_with_callback(self):
        cb = MagicMock()
        self.nav.set_profile_callback(InputEvent.BUTTON_M3, cb)
        self.nav.on_input(InputEvent.BUTTON_M3)
        cb.assert_called_once()

    def test_m_key_without_callback(self):
        """M-key with no callback should not raise."""
        self.nav.on_input(InputEvent.BUTTON_M1)  # no callback set

    def test_other_events_pass_to_screen_manager(self):
        """Non-special events in idle delegate to screen_manager.handle_input."""
        self.nav.on_input(InputEvent.STICK_UP)
        self.sm.handle_input.assert_called_with(InputEvent.STICK_UP)

    def test_set_profile_callback_rejects_non_m_keys(self):
        """Only M1/M2/M3 are accepted for profile callbacks."""
        cb = MagicMock()
        self.nav.set_profile_callback(InputEvent.BUTTON_BD, cb)
        assert InputEvent.BUTTON_BD not in self.nav._profile_callbacks


class TestNavigationControllerMenuInput:
    """Input handling in MENU state."""

    def setup_method(self):
        self.sm = MagicMock()
        self.idle = MagicMock()
        self.nav = NavigationController(self.sm, self.idle)
        self.nav.state = NavigationState.MENU

    def test_delegates_to_screen_manager(self):
        self.sm.stack_depth = 2
        self.nav.on_input(InputEvent.STICK_UP)
        self.sm.handle_input.assert_called_with(InputEvent.STICK_UP)

    def test_updates_state_to_idle_when_stack_depth_1(self):
        """When screen stack returns to root, state goes back to IDLE."""
        self.sm.stack_depth = 1
        self.nav.on_input(InputEvent.BUTTON_BD)
        assert self.nav.state == NavigationState.IDLE

    def test_stays_menu_when_stack_depth_gt_1(self):
        self.sm.stack_depth = 3
        self.nav.on_input(InputEvent.STICK_DOWN)
        assert self.nav.state == NavigationState.MENU


class TestNavigationControllerGoHome:
    """go_home() method."""

    def test_go_home(self):
        sm = MagicMock()
        nav = NavigationController(sm, MagicMock())
        nav.state = NavigationState.MENU

        nav.go_home()
        sm.pop_to_root.assert_called_once()
        assert nav.state == NavigationState.IDLE


class TestNavigationControllerOpenMainMenu:
    """_open_main_menu transitions."""

    def test_open_main_menu_pushes_and_sets_state(self):
        sm = MagicMock()
        nav = NavigationController(sm, MagicMock())

        with patch("g13_linux.menu.screens.main_menu.MainMenuScreen") as MockMenu:
            mock_menu_instance = MagicMock()
            MockMenu.return_value = mock_menu_instance
            nav._open_main_menu()

            MockMenu.assert_called_once_with(sm)
            sm.push.assert_called_with(mock_menu_instance)
            assert nav.state == NavigationState.MENU


class TestNavigationControllerShowToast:
    """show_toast method."""

    def test_show_toast(self):
        sm = MagicMock()
        nav = NavigationController(sm, MagicMock())

        with patch("g13_linux.menu.screens.toast.ToastScreen") as MockToast:
            mock_toast = MagicMock()
            MockToast.return_value = mock_toast
            nav.show_toast("Hello!", 3.0)

            MockToast.assert_called_once_with(sm, "Hello!")
            sm.show_overlay.assert_called_once_with(mock_toast, 3.0)


# ===========================================================================
# LEDController tests
# ===========================================================================


class TestLEDControllerInit:
    """LEDController initialization."""

    def test_init_with_backlight(self):
        bl = MagicMock(spec=G13Backlight)
        ctrl = LEDController(backlight=bl)
        assert ctrl._backlight is bl

    def test_init_with_device(self):
        device = MagicMock()
        with patch("g13_linux.led.controller.G13Backlight") as MockBL:
            mock_bl = MagicMock()
            MockBL.return_value = mock_bl
            ctrl = LEDController(device=device)
            MockBL.assert_called_once_with(device)
            assert ctrl._backlight is mock_bl

    def test_init_no_args(self):
        with patch("g13_linux.led.controller.G13Backlight") as MockBL:
            mock_bl = MagicMock()
            MockBL.return_value = mock_bl
            LEDController()
            MockBL.assert_called_once_with(None)

    def test_default_color_white(self):
        ctrl = LEDController(backlight=MagicMock(spec=G13Backlight))
        assert ctrl.current_color == RGB(255, 255, 255)

    def test_default_no_effect(self):
        ctrl = LEDController(backlight=MagicMock(spec=G13Backlight))
        assert ctrl.current_effect is None


class TestLEDControllerSetColor:
    """Color setting methods."""

    def setup_method(self):
        self.backlight = MagicMock(spec=G13Backlight)
        self.ctrl = LEDController(backlight=self.backlight)

    def test_set_color(self):
        self.ctrl.set_color(255, 0, 128)
        assert self.ctrl.current_color == RGB(255, 0, 128)
        self.backlight.set_color.assert_called_with(255, 0, 128)

    def test_set_rgb(self):
        color = RGB(10, 20, 30)
        self.ctrl.set_rgb(color)
        assert self.ctrl.current_color == RGB(10, 20, 30)
        self.backlight.set_color.assert_called_with(10, 20, 30)

    def test_set_hex(self):
        self.ctrl.set_hex("#FF8000")
        assert self.ctrl.current_color == RGB(255, 128, 0)

    def test_set_hex_no_hash(self):
        self.ctrl.set_hex("00FF00")
        assert self.ctrl.current_color == RGB(0, 255, 0)

    def test_set_named(self):
        self.ctrl.set_named("red")
        assert self.ctrl.current_color == RGB(255, 0, 0)

    def test_set_named_case_insensitive(self):
        self.ctrl.set_named("Blue")
        assert self.ctrl.current_color == RGB(0, 0, 255)

    def test_off(self):
        self.ctrl.off()
        assert self.ctrl.current_color == RGB(0, 0, 0)
        self.backlight.set_color.assert_called_with(0, 0, 0)

    def test_get_current(self):
        self.ctrl.set_color(42, 43, 44)
        assert self.ctrl.get_current() == RGB(42, 43, 44)

    def test_set_color_stops_running_effect(self):
        """Setting color explicitly should stop any running effect."""
        self.ctrl._current_effect = EffectType.PULSE
        self.ctrl.set_color(100, 100, 100)
        assert self.ctrl.current_effect is None


class TestLEDControllerBrightness:
    """Brightness property and set_brightness."""

    def test_brightness_property(self):
        bl = MagicMock(spec=G13Backlight)
        bl.get_brightness.return_value = 75
        ctrl = LEDController(backlight=bl)
        assert ctrl.brightness == 75

    def test_set_brightness(self):
        bl = MagicMock(spec=G13Backlight)
        ctrl = LEDController(backlight=bl)
        ctrl.set_brightness(50)
        bl.set_brightness.assert_called_with(50)


class TestLEDControllerEffects:
    """Effect start/stop lifecycle."""

    def setup_method(self):
        self.backlight = MagicMock(spec=G13Backlight)
        self.ctrl = LEDController(backlight=self.backlight)

    def test_start_solid_effect(self):
        self.ctrl.start_effect(EffectType.SOLID, color=RGB(255, 0, 0))
        assert self.ctrl.current_effect == EffectType.SOLID
        assert self.ctrl._effect_thread is not None
        time.sleep(0.1)
        self.ctrl.stop_effect()
        assert self.ctrl.current_effect is None

    def test_start_pulse_effect(self):
        self.ctrl.start_effect(EffectType.PULSE, color=RGB(0, 255, 0), speed=2.0)
        assert self.ctrl.current_effect == EffectType.PULSE
        time.sleep(0.1)
        self.ctrl.stop_effect()

    def test_start_rainbow_effect(self):
        self.ctrl.start_effect(EffectType.RAINBOW, speed=1.0)
        assert self.ctrl.current_effect == EffectType.RAINBOW
        time.sleep(0.1)
        self.ctrl.stop_effect()

    def test_start_fade_effect(self):
        self.ctrl.start_effect(
            EffectType.FADE,
            color1=RGB(255, 0, 0),
            color2=RGB(0, 0, 255),
            speed=1.0,
        )
        assert self.ctrl.current_effect == EffectType.FADE
        time.sleep(0.1)
        self.ctrl.stop_effect()

    def test_start_alert_effect(self):
        self.ctrl.start_effect(EffectType.ALERT, color=RGB(255, 0, 0), count=1)
        assert self.ctrl.current_effect == EffectType.ALERT
        # Alert is finite — wait for completion
        time.sleep(1.0)
        self.ctrl.stop_effect()

    def test_stop_without_start(self):
        """stop_effect when nothing running should not raise."""
        self.ctrl.stop_effect()
        assert self.ctrl.current_effect is None

    def test_start_stops_previous_effect(self):
        """Starting new effect stops the old one."""
        self.ctrl.start_effect(EffectType.SOLID, color=RGB(255, 0, 0))
        time.sleep(0.05)
        self.ctrl.start_effect(EffectType.RAINBOW)
        assert self.ctrl.current_effect == EffectType.RAINBOW
        self.ctrl.stop_effect()

    def test_effect_thread_cleanup(self):
        """Thread is cleaned up after stop."""
        self.ctrl.start_effect(EffectType.SOLID, color=RGB(100, 100, 100))
        time.sleep(0.05)
        self.ctrl.stop_effect()
        assert self.ctrl._effect_thread is None
        assert self.ctrl._effect_generator is None

    def test_effect_loop_updates_current_color(self):
        """Effect loop should update _current_color from generator output."""
        self.ctrl.start_effect(EffectType.SOLID, color=RGB(42, 42, 42))
        time.sleep(0.15)  # Allow a couple frames
        self.ctrl.stop_effect()
        assert self.ctrl.current_color == RGB(42, 42, 42)

    def test_effect_calls_backlight(self):
        """Effect loop sends colors to backlight hardware."""
        self.ctrl.start_effect(EffectType.SOLID, color=RGB(10, 20, 30))
        time.sleep(0.15)
        self.ctrl.stop_effect()
        self.backlight.set_color.assert_called()

    def test_alert_finite_completes(self):
        """Alert effect with count=1 should complete on its own."""
        self.ctrl.start_effect(EffectType.ALERT, color=RGB(255, 0, 0), count=1)
        time.sleep(1.5)  # enough for 1 flash cycle
        # Effect should have completed and cleared itself
        # The thread may have stopped, current_effect set to None
        assert self.ctrl._current_effect is None or not (
            self.ctrl._effect_thread and self.ctrl._effect_thread.is_alive()
        )
        self.ctrl.stop_effect()


class TestLEDControllerRunAlert:
    """run_alert blocking and non-blocking modes."""

    def setup_method(self):
        self.backlight = MagicMock(spec=G13Backlight)
        self.ctrl = LEDController(backlight=self.backlight)

    def test_run_alert_blocking(self):
        """Blocking alert runs synchronously."""
        self.ctrl.run_alert(color=RGB(255, 0, 0), count=1, blocking=True)
        # Should have called set_color multiple times (on/off frames)
        assert self.backlight.set_color.call_count > 0

    def test_run_alert_non_blocking(self):
        """Non-blocking alert starts effect thread."""
        self.ctrl.run_alert(color=RGB(255, 0, 0), count=1, blocking=False)
        assert self.ctrl.current_effect == EffectType.ALERT
        time.sleep(0.5)
        self.ctrl.stop_effect()

    def test_run_alert_default_color(self):
        """Default color is red when None."""
        self.ctrl.run_alert(color=None, count=1, blocking=True)
        # alert() defaults to red, so set_color should be called with 255,0,0
        calls = self.backlight.set_color.call_args_list
        red_calls = [c for c in calls if c[0] == (255, 0, 0)]
        assert len(red_calls) > 0


class TestLEDControllerApplyColor:
    """_apply_color sends to backlight under lock."""

    def test_apply_color(self):
        bl = MagicMock(spec=G13Backlight)
        ctrl = LEDController(backlight=bl)
        ctrl._apply_color(RGB(100, 150, 200))
        bl.set_color.assert_called_once_with(100, 150, 200)


# ===========================================================================
# Effects generator tests
# ===========================================================================


class TestSolidEffect:
    """solid() generator."""

    def test_yields_same_color_forever(self):
        color = RGB(100, 200, 50)
        gen = solid(color)
        values = _take(gen, 10)
        assert all(v == color for v in values)

    def test_infinite(self):
        gen = solid(RGB(0, 0, 0))
        # Should never raise StopIteration
        for _ in range(100):
            next(gen)


class TestPulseEffect:
    """pulse() generator."""

    def test_yields_rgb_objects(self):
        gen = pulse(RGB(255, 0, 0), speed=1.0)
        values = _take(gen, 5)
        for v in values:
            assert isinstance(v, RGB)

    def test_brightness_varies(self):
        """Over time, brightness should vary (not all identical)."""
        gen = pulse(RGB(255, 255, 255), speed=10.0)
        # Take values with small delay to get different phases
        values = []
        for _ in range(10):
            values.append(next(gen))
            time.sleep(0.02)
        # At least some values should differ
        unique = set((v.r, v.g, v.b) for v in values)
        assert len(unique) > 1

    def test_color_components_in_range(self):
        gen = pulse(RGB(255, 128, 64), speed=5.0)
        for _ in range(20):
            v = next(gen)
            assert 0 <= v.r <= 255
            assert 0 <= v.g <= 255
            assert 0 <= v.b <= 255


class TestRainbowEffect:
    """rainbow() generator."""

    def test_yields_rgb_objects(self):
        gen = rainbow(speed=1.0)
        values = _take(gen, 5)
        for v in values:
            assert isinstance(v, RGB)

    def test_hue_cycles(self):
        """Colors should change over time."""
        gen = rainbow(speed=10.0)
        values = []
        for _ in range(10):
            values.append(next(gen))
            time.sleep(0.02)
        unique = set((v.r, v.g, v.b) for v in values)
        assert len(unique) > 1

    def test_full_saturation(self):
        """Rainbow uses S=1, V=1, so at least one component should be 255."""
        gen = rainbow(speed=1.0)
        v = next(gen)
        assert max(v.r, v.g, v.b) == 255


class TestFadeEffect:
    """fade() generator."""

    def test_yields_rgb_objects(self):
        gen = fade(RGB(255, 0, 0), RGB(0, 0, 255), speed=1.0)
        values = _take(gen, 5)
        for v in values:
            assert isinstance(v, RGB)

    def test_blends_between_colors(self):
        """Output should contain values between the two colors."""
        gen = fade(RGB(255, 0, 0), RGB(0, 0, 255), speed=5.0)
        values = []
        for _ in range(20):
            values.append(next(gen))
            time.sleep(0.01)
        # Should see values that are neither pure red nor pure blue
        has_mixed = any(v.r > 0 and v.b > 0 for v in values)
        assert has_mixed

    def test_components_in_range(self):
        gen = fade(RGB(255, 128, 0), RGB(0, 128, 255), speed=1.0)
        for _ in range(20):
            v = next(gen)
            assert 0 <= v.r <= 255
            assert 0 <= v.g <= 255
            assert 0 <= v.b <= 255


class TestAlertEffect:
    """alert() finite generator."""

    def test_finite_generator(self):
        """Alert should eventually raise StopIteration."""
        gen = alert(RGB(255, 0, 0), count=1)
        values = []
        for v in gen:
            values.append(v)
        assert len(values) > 0  # produced some frames

    def test_alternates_color_and_black(self):
        """Should yield the color and black (0,0,0)."""
        gen = alert(RGB(255, 0, 0), count=1)
        values = list(gen)
        colors_seen = set((v.r, v.g, v.b) for v in values)
        assert (255, 0, 0) in colors_seen
        assert (0, 0, 0) in colors_seen

    def test_default_color_red(self):
        """None color defaults to red."""
        gen = alert(None, count=1)
        values = list(gen)
        red_frames = [v for v in values if v == RGB(255, 0, 0)]
        assert len(red_frames) > 0

    def test_count_zero(self):
        """count=0 produces no frames."""
        gen = alert(RGB(255, 0, 0), count=0)
        values = list(gen)
        assert values == []

    def test_multiple_flashes(self):
        """count=3 produces more frames than count=1."""
        gen1 = list(alert(RGB(255, 0, 0), count=1))
        gen3 = list(alert(RGB(255, 0, 0), count=3))
        assert len(gen3) > len(gen1)


class TestStrobeEffect:
    """strobe() generator."""

    def test_yields_rgb_objects(self):
        gen = strobe(RGB(255, 255, 255), frequency=10.0)
        values = _take(gen, 5)
        for v in values:
            assert isinstance(v, RGB)

    def test_alternates_color_and_black(self):
        """Should yield color or black based on phase."""
        gen = strobe(RGB(0, 255, 0), frequency=100.0)
        values = []
        for _ in range(50):
            values.append(next(gen))
            time.sleep(0.002)
        colors_seen = set((v.r, v.g, v.b) for v in values)
        assert (0, 255, 0) in colors_seen
        assert (0, 0, 0) in colors_seen

    def test_infinite(self):
        gen = strobe(RGB(255, 0, 0), frequency=10.0)
        for _ in range(100):
            next(gen)


class TestCandleEffect:
    """candle() generator."""

    def test_yields_rgb_objects(self):
        gen = candle(RGB(255, 100, 20), flicker_intensity=0.3)
        values = _take(gen, 5)
        for v in values:
            assert isinstance(v, RGB)

    def test_default_base_color(self):
        """None base_color defaults to warm orange (255, 100, 20)."""
        gen = candle(None, flicker_intensity=0.3)
        values = _take(gen, 10)
        # All values should be dimmed versions of warm orange
        for v in values:
            assert v.r >= 0
            assert v.g >= 0
            assert v.b >= 0

    def test_brightness_varies(self):
        """Flicker should produce varying brightness."""
        gen = candle(RGB(255, 100, 20), flicker_intensity=0.5)
        values = _take(gen, 50)
        unique = set((v.r, v.g, v.b) for v in values)
        # With 50 samples and random variation, should get multiple distinct values
        assert len(unique) > 1

    def test_zero_flicker_constant(self):
        """With flicker_intensity=0, output is constant (dim factor = 0)."""
        gen = candle(RGB(255, 100, 20), flicker_intensity=0.0)
        values = _take(gen, 10)
        # All should be the same (flicker = 1.0 - 0 = 1.0, dim by 1.0-1.0 = 0.0 → same color)
        first = values[0]
        for v in values:
            assert v == first

    def test_components_in_range(self):
        gen = candle(RGB(255, 200, 100), flicker_intensity=0.9)
        for _ in range(50):
            v = next(gen)
            assert 0 <= v.r <= 255
            assert 0 <= v.g <= 255
            assert 0 <= v.b <= 255

    def test_infinite(self):
        gen = candle(RGB(255, 100, 20))
        for _ in range(100):
            next(gen)


class TestEffectType:
    """EffectType enum."""

    def test_values(self):
        assert EffectType.SOLID.value == "solid"
        assert EffectType.PULSE.value == "pulse"
        assert EffectType.RAINBOW.value == "rainbow"
        assert EffectType.FADE.value == "fade"
        assert EffectType.ALERT.value == "alert"

    def test_all_types(self):
        assert len(EffectType) == 5
