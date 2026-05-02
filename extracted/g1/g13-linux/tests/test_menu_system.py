"""
Tests for the G13 LCD menu system.

Covers:
- Screen base class and InputEvent enum
- ScreenManager stack operations, overlays, rendering
- MenuItem, MenuSeparator, MenuGroup dataclasses
- MenuScreen navigation (up/down/wrap/scroll/selection)
- MainMenuScreen submenu creation
- ToastScreen and ConfirmDialog interaction
- MacrosScreen item building and refresh
- SettingsScreen, ClockSettingsScreen, TimeoutSettingsScreen
- InfoScreen display fields
- ProfilesScreen selection and hardware apply
- IdleScreen and ClockScreen time display
- LEDSettingsScreen, ColorPickerScreen, BrightnessScreen, EffectSelectScreen
"""

from unittest.mock import MagicMock

from g13_linux.menu.items import MenuGroup, MenuItem, MenuSeparator
from g13_linux.menu.manager import ScreenManager
from g13_linux.menu.screen import InputEvent, Screen

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class ConcreteScreen(Screen):
    """Minimal concrete Screen for testing the abstract base."""

    def __init__(self, manager):
        super().__init__(manager)
        self.input_events = []
        self.render_calls = 0
        self.enter_calls = 0
        self.exit_calls = 0

    def on_input(self, event: InputEvent) -> bool:
        self.input_events.append(event)
        return True

    def render(self, canvas):
        self.render_calls += 1

    def on_enter(self):
        self.enter_calls += 1

    def on_exit(self):
        self.exit_calls += 1


def _make_manager(**kwargs):
    """Create a ScreenManager with mocked LCD and optional injected deps."""
    lcd = MagicMock()
    mgr = ScreenManager(lcd=lcd)
    for k, v in kwargs.items():
        setattr(mgr, k, v)
    return mgr


def _mock_canvas():
    """Return a MagicMock standing in for Canvas."""
    canvas = MagicMock()
    canvas.WIDTH = 160
    canvas.HEIGHT = 43
    return canvas


# ===================================================================
# InputEvent enum
# ===================================================================


class TestInputEvent:
    def test_all_members_exist(self):
        expected = {
            "STICK_UP",
            "STICK_DOWN",
            "STICK_LEFT",
            "STICK_RIGHT",
            "STICK_PRESS",
            "BUTTON_BD",
            "BUTTON_LEFT",
            "BUTTON_M1",
            "BUTTON_M2",
            "BUTTON_M3",
            "BUTTON_MR",
        }
        assert set(InputEvent.__members__.keys()) == expected

    def test_values_are_strings(self):
        for member in InputEvent:
            assert isinstance(member.value, str)


# ===================================================================
# Screen base class
# ===================================================================


class TestScreen:
    def test_initial_dirty(self):
        mgr = _make_manager()
        s = ConcreteScreen(mgr)
        assert s.is_dirty is True

    def test_mark_dirty(self):
        mgr = _make_manager()
        s = ConcreteScreen(mgr)
        s._dirty = False
        s.mark_dirty()
        assert s.is_dirty is True

    def test_manager_reference(self):
        mgr = _make_manager()
        s = ConcreteScreen(mgr)
        assert s.manager is mgr

    def test_default_update_does_nothing(self):
        mgr = _make_manager()
        s = ConcreteScreen(mgr)
        # base Screen.update is a no-op; just confirm it doesn't raise
        s.update(0.016)

    def test_on_enter_on_exit_hooks(self):
        mgr = _make_manager()
        s = ConcreteScreen(mgr)
        s.on_enter()
        s.on_exit()
        assert s.enter_calls == 1
        assert s.exit_calls == 1


# ===================================================================
# MenuItem / MenuSeparator / MenuGroup
# ===================================================================


class TestMenuItem:
    def test_basic_fields(self):
        item = MenuItem(id="foo", label="Foo")
        assert item.id == "foo"
        assert item.label == "Foo"
        assert item.enabled is True
        assert item.action is None
        assert item.submenu is None
        assert item.value_getter is None
        assert item.icon is None
        assert item.shortcut is None

    def test_get_display_value_none_without_getter(self):
        item = MenuItem(id="a", label="A")
        assert item.get_display_value() is None

    def test_get_display_value_returns_getter_result(self):
        item = MenuItem(id="a", label="A", value_getter=lambda: "42")
        assert item.get_display_value() == "42"

    def test_get_display_value_returns_question_on_exception(self):
        def bad():
            raise RuntimeError("boom")

        item = MenuItem(id="a", label="A", value_getter=bad)
        assert item.get_display_value() == "?"

    def test_is_selectable_with_action(self):
        item = MenuItem(id="a", label="A", action=lambda: None)
        assert item.is_selectable() is True

    def test_is_selectable_with_submenu(self):
        item = MenuItem(id="a", label="A", submenu=lambda: None)
        assert item.is_selectable() is True

    def test_is_selectable_disabled(self):
        item = MenuItem(id="a", label="A", action=lambda: None, enabled=False)
        assert item.is_selectable() is False

    def test_is_selectable_no_action_no_submenu(self):
        item = MenuItem(id="a", label="A")
        assert item.is_selectable() is False


class TestMenuSeparator:
    def test_default_label(self):
        sep = MenuSeparator()
        assert sep.label == ""

    def test_custom_label(self):
        sep = MenuSeparator(label="Section")
        assert sep.label == "Section"


class TestMenuGroup:
    def test_defaults(self):
        grp = MenuGroup(title="Grp")
        assert grp.title == "Grp"
        assert grp.items == []

    def test_with_items(self):
        items = [MenuItem(id="x", label="X")]
        grp = MenuGroup(title="G", items=items)
        assert len(grp.items) == 1


# ===================================================================
# ScreenManager
# ===================================================================


class TestScreenManager:
    # -- stack basics -------------------------------------------------

    def test_initial_state(self):
        mgr = _make_manager()
        assert mgr.current is None
        assert mgr.stack_depth == 0

    def test_push(self):
        mgr = _make_manager()
        s = ConcreteScreen(mgr)
        mgr.push(s)
        assert mgr.current is s
        assert mgr.stack_depth == 1
        assert s.enter_calls == 1
        assert s.is_dirty is True

    def test_push_calls_on_exit_on_previous(self):
        mgr = _make_manager()
        s1 = ConcreteScreen(mgr)
        s2 = ConcreteScreen(mgr)
        mgr.push(s1)
        mgr.push(s2)
        assert s1.exit_calls == 1
        assert s2.enter_calls == 1
        assert mgr.stack_depth == 2

    def test_pop_empty(self):
        mgr = _make_manager()
        assert mgr.pop() is None

    def test_pop(self):
        mgr = _make_manager()
        s1 = ConcreteScreen(mgr)
        s2 = ConcreteScreen(mgr)
        mgr.push(s1)
        mgr.push(s2)
        popped = mgr.pop()
        assert popped is s2
        assert s2.exit_calls == 1
        assert mgr.current is s1
        # s1 re-entered after pop
        assert s1.enter_calls == 2

    def test_pop_to_root(self):
        mgr = _make_manager()
        screens = [ConcreteScreen(mgr) for _ in range(4)]
        for s in screens:
            mgr.push(s)
        mgr.pop_to_root()
        assert mgr.stack_depth == 1
        assert mgr.current is screens[0]
        for s in screens[1:]:
            assert s.exit_calls >= 1

    def test_pop_to_root_empty(self):
        mgr = _make_manager()
        mgr.pop_to_root()  # should not raise
        assert mgr.stack_depth == 0

    def test_replace(self):
        mgr = _make_manager()
        s1 = ConcreteScreen(mgr)
        s2 = ConcreteScreen(mgr)
        mgr.push(s1)
        mgr.replace(s2)
        assert mgr.current is s2
        assert mgr.stack_depth == 1
        assert s1.exit_calls == 1
        assert s2.enter_calls == 1

    def test_replace_empty_stack(self):
        mgr = _make_manager()
        s = ConcreteScreen(mgr)
        mgr.replace(s)
        assert mgr.current is s
        assert mgr.stack_depth == 1

    # -- overlays ----------------------------------------------------

    def test_show_overlay(self):
        mgr = _make_manager()
        s = ConcreteScreen(mgr)
        mgr.show_overlay(s)
        assert mgr._overlay is s
        assert s.enter_calls == 1

    def test_show_overlay_with_duration(self):
        mgr = _make_manager()
        s = ConcreteScreen(mgr)
        mgr.show_overlay(s, duration=5.0)
        assert mgr._overlay is s
        assert mgr._overlay_timer is not None
        mgr.dismiss_overlay()  # cleanup timer

    def test_dismiss_overlay(self):
        mgr = _make_manager()
        base = ConcreteScreen(mgr)
        overlay = ConcreteScreen(mgr)
        mgr.push(base)
        mgr.show_overlay(overlay)
        mgr.dismiss_overlay()
        assert mgr._overlay is None
        assert overlay.exit_calls == 1
        # base screen should be marked dirty after overlay dismiss
        assert base.is_dirty is True

    def test_dismiss_overlay_noop_when_none(self):
        mgr = _make_manager()
        mgr.dismiss_overlay()  # should not raise

    def test_show_overlay_replaces_previous(self):
        mgr = _make_manager()
        o1 = ConcreteScreen(mgr)
        o2 = ConcreteScreen(mgr)
        mgr.show_overlay(o1)
        mgr.show_overlay(o2)
        assert mgr._overlay is o2
        assert o1.exit_calls == 1

    # -- input routing -----------------------------------------------

    def test_handle_input_to_overlay(self):
        mgr = _make_manager()
        base = ConcreteScreen(mgr)
        overlay = ConcreteScreen(mgr)
        mgr.push(base)
        mgr.show_overlay(overlay)
        mgr.handle_input(InputEvent.STICK_PRESS)
        assert InputEvent.STICK_PRESS in overlay.input_events
        # overlay handled it, base should NOT get it
        assert InputEvent.STICK_PRESS not in base.input_events

    def test_handle_input_to_current_when_no_overlay(self):
        mgr = _make_manager()
        s = ConcreteScreen(mgr)
        mgr.push(s)
        mgr.handle_input(InputEvent.STICK_UP)
        assert InputEvent.STICK_UP in s.input_events

    def test_handle_input_empty_stack(self):
        mgr = _make_manager()
        mgr.handle_input(InputEvent.STICK_UP)  # should not raise

    # -- update ------------------------------------------------------

    def test_update_calls_current_and_overlay(self):
        mgr = _make_manager()
        base = ConcreteScreen(mgr)
        overlay = ConcreteScreen(mgr)
        mgr.push(base)
        mgr.show_overlay(overlay)
        # Patch update to record calls
        base.update = MagicMock()
        overlay.update = MagicMock()
        mgr.update(0.016)
        base.update.assert_called_once_with(0.016)
        overlay.update.assert_called_once_with(0.016)

    def test_update_empty_stack(self):
        mgr = _make_manager()
        mgr.update(0.016)  # should not raise

    # -- render ------------------------------------------------------

    def test_render_when_dirty(self):
        mgr = _make_manager()
        s = ConcreteScreen(mgr)
        mgr.push(s)
        result = mgr.render()
        assert result is True
        assert s.is_dirty is False
        mgr.lcd.write_bitmap.assert_called_once()

    def test_render_when_clean(self):
        mgr = _make_manager()
        s = ConcreteScreen(mgr)
        mgr.push(s)
        mgr.render()  # first render clears dirty
        result = mgr.render()
        assert result is False

    def test_render_empty_stack(self):
        mgr = _make_manager()
        assert mgr.render() is False

    def test_render_no_lcd(self):
        mgr = ScreenManager(lcd=None)
        s = ConcreteScreen(mgr)
        mgr.push(s)
        result = mgr.render()
        assert result is True
        assert s.is_dirty is False

    def test_force_render(self):
        mgr = _make_manager()
        s = ConcreteScreen(mgr)
        mgr.push(s)
        mgr.render()  # clears dirty
        assert s.is_dirty is False
        mgr.force_render()
        # force_render marks dirty and re-renders
        mgr.lcd.write_bitmap.assert_called()

    def test_render_overlay_on_top(self):
        mgr = _make_manager()
        base = ConcreteScreen(mgr)
        overlay = ConcreteScreen(mgr)
        mgr.push(base)
        mgr.show_overlay(overlay)
        mgr.render()
        assert base.render_calls >= 1
        assert overlay.render_calls >= 1


# ===================================================================
# MenuScreen (base_menu.py)
# ===================================================================


class TestMenuScreen:
    def _make_menu(self, n_items=5, manager=None):
        from g13_linux.menu.screens.base_menu import MenuScreen

        mgr = manager or _make_manager()
        items = [
            MenuItem(id=f"item_{i}", label=f"Item {i}", action=lambda: None) for i in range(n_items)
        ]
        return MenuScreen(mgr, "TEST", items), mgr

    def test_init(self):
        menu, _ = self._make_menu()
        assert menu.title == "TEST"
        assert menu.selected_index == 0
        assert menu.scroll_offset == 0

    def test_navigate_down(self):
        menu, _ = self._make_menu()
        menu.on_input(InputEvent.STICK_DOWN)
        assert menu.selected_index == 1

    def test_navigate_up(self):
        menu, _ = self._make_menu()
        menu.on_input(InputEvent.STICK_DOWN)
        menu.on_input(InputEvent.STICK_UP)
        assert menu.selected_index == 0

    def test_wrap_down(self):
        menu, _ = self._make_menu(n_items=3)
        for _ in range(3):
            menu.on_input(InputEvent.STICK_DOWN)
        assert menu.selected_index == 0  # wrapped

    def test_wrap_up(self):
        menu, _ = self._make_menu(n_items=3)
        menu.on_input(InputEvent.STICK_UP)
        assert menu.selected_index == 2  # wrapped to last

    def test_scroll_adjusts(self):
        menu, _ = self._make_menu(n_items=10)
        # Navigate past VISIBLE_ITEMS
        for _ in range(6):
            menu.on_input(InputEvent.STICK_DOWN)
        assert menu.selected_index == 6
        assert menu.scroll_offset > 0

    def test_scroll_adjusts_up(self):
        menu, _ = self._make_menu(n_items=10)
        # Go down then wrap up to last
        menu.on_input(InputEvent.STICK_UP)
        assert menu.selected_index == 9
        assert menu.scroll_offset == 9 - menu.VISIBLE_ITEMS + 1

    def test_select_action(self):
        from g13_linux.menu.screens.base_menu import MenuScreen

        mgr = _make_manager()
        called = []
        items = [MenuItem(id="x", label="X", action=lambda: called.append(True))]
        menu = MenuScreen(mgr, "T", items)
        menu.on_input(InputEvent.STICK_PRESS)
        assert called == [True]

    def test_select_submenu(self):
        from g13_linux.menu.screens.base_menu import MenuScreen

        mgr = _make_manager()
        sub_screen = ConcreteScreen(mgr)
        items = [MenuItem(id="x", label="X", submenu=lambda: sub_screen)]
        menu = MenuScreen(mgr, "T", items)
        mgr.push(menu)
        menu.on_input(InputEvent.STICK_PRESS)
        assert mgr.current is sub_screen

    def test_select_disabled_item_does_nothing(self):
        from g13_linux.menu.screens.base_menu import MenuScreen

        mgr = _make_manager()
        called = []
        items = [MenuItem(id="x", label="X", action=lambda: called.append(1), enabled=False)]
        menu = MenuScreen(mgr, "T", items)
        menu.on_input(InputEvent.STICK_PRESS)
        assert called == []

    def test_back_button_pops(self):
        menu, mgr = self._make_menu()
        mgr.push(menu)
        menu.on_input(InputEvent.BUTTON_BD)
        assert mgr.current is None

    def test_move_selection_empty(self):
        from g13_linux.menu.screens.base_menu import MenuScreen

        mgr = _make_manager()
        menu = MenuScreen(mgr, "T", [])
        menu._move_selection(1)  # should not raise

    def test_select_current_empty(self):
        from g13_linux.menu.screens.base_menu import MenuScreen

        mgr = _make_manager()
        menu = MenuScreen(mgr, "T", [])
        menu._select_current()  # should not raise

    def test_render_calls_canvas(self):
        menu, _ = self._make_menu()
        canvas = _mock_canvas()
        menu.render(canvas)
        assert canvas.draw_text.called
        assert canvas.draw_hline.called

    def test_render_scroll_indicators_few_items(self):
        menu, _ = self._make_menu(n_items=2)
        canvas = _mock_canvas()
        menu.render(canvas)
        # With <= VISIBLE_ITEMS, no scroll indicator
        assert not canvas.draw_vline.called

    def test_render_scroll_indicators_many_items(self):
        menu, _ = self._make_menu(n_items=10)
        canvas = _mock_canvas()
        menu.render(canvas)
        assert canvas.draw_vline.called

    def test_render_item_with_value_getter(self):
        from g13_linux.menu.screens.base_menu import MenuScreen

        mgr = _make_manager()
        items = [MenuItem(id="v", label="Val", value_getter=lambda: "ON", action=lambda: None)]
        menu = MenuScreen(mgr, "T", items)
        canvas = _mock_canvas()
        menu.render(canvas)
        # value should be rendered — just verify no crash

    def test_render_item_with_submenu_arrow(self):
        from g13_linux.menu.screens.base_menu import MenuScreen

        mgr = _make_manager()
        items = [MenuItem(id="s", label="Sub", submenu=lambda: ConcreteScreen(mgr))]
        menu = MenuScreen(mgr, "T", items)
        canvas = _mock_canvas()
        menu.render(canvas)

    def test_unhandled_input_returns_false(self):
        menu, _ = self._make_menu()
        assert menu.on_input(InputEvent.BUTTON_M1) is False


# ===================================================================
# ToastScreen
# ===================================================================


class TestToastScreen:
    def test_any_input_dismisses(self):
        from g13_linux.menu.screens.toast import ToastScreen

        mgr = _make_manager()
        toast = ToastScreen(mgr, "Hello")
        mgr.show_overlay(toast)
        result = toast.on_input(InputEvent.STICK_PRESS)
        assert result is True
        assert mgr._overlay is None

    def test_render(self):
        from g13_linux.menu.screens.toast import ToastScreen

        mgr = _make_manager()
        toast = ToastScreen(mgr, "Test message")
        canvas = _mock_canvas()
        toast.render(canvas)
        assert canvas.draw_rect.called
        assert canvas.draw_text.called

    def test_render_with_icon(self):
        from g13_linux.menu.screens.toast import ToastScreen

        mgr = _make_manager()
        icon = MagicMock()
        toast = ToastScreen(mgr, "With icon", icon=icon)
        canvas = _mock_canvas()
        toast.render(canvas)
        canvas.draw_icon.assert_called_once()


# ===================================================================
# ConfirmDialog
# ===================================================================


class TestConfirmDialog:
    def test_initial_selected_no(self):
        from g13_linux.menu.screens.toast import ConfirmDialog

        mgr = _make_manager()
        dlg = ConfirmDialog(mgr, "Sure?", on_confirm=lambda: None)
        assert dlg.selected == 0  # No

    def test_toggle_left_right(self):
        from g13_linux.menu.screens.toast import ConfirmDialog

        mgr = _make_manager()
        dlg = ConfirmDialog(mgr, "Sure?", on_confirm=lambda: None)
        dlg.on_input(InputEvent.STICK_RIGHT)
        assert dlg.selected == 1  # Yes
        dlg.on_input(InputEvent.STICK_LEFT)
        assert dlg.selected == 0  # No

    def test_confirm_yes(self):
        from g13_linux.menu.screens.toast import ConfirmDialog

        mgr = _make_manager()
        confirmed = []
        dlg = ConfirmDialog(mgr, "Sure?", on_confirm=lambda: confirmed.append(True))
        mgr.show_overlay(dlg)
        dlg.on_input(InputEvent.STICK_RIGHT)  # select Yes
        dlg.on_input(InputEvent.STICK_PRESS)
        assert confirmed == [True]
        assert mgr._overlay is None

    def test_confirm_no(self):
        from g13_linux.menu.screens.toast import ConfirmDialog

        mgr = _make_manager()
        cancelled = []
        dlg = ConfirmDialog(
            mgr, "Sure?", on_confirm=lambda: None, on_cancel=lambda: cancelled.append(True)
        )
        mgr.show_overlay(dlg)
        dlg.on_input(InputEvent.STICK_PRESS)  # selected=0 => No
        assert cancelled == [True]
        assert mgr._overlay is None

    def test_back_button_cancels(self):
        from g13_linux.menu.screens.toast import ConfirmDialog

        mgr = _make_manager()
        cancelled = []
        dlg = ConfirmDialog(
            mgr, "Sure?", on_confirm=lambda: None, on_cancel=lambda: cancelled.append(True)
        )
        mgr.show_overlay(dlg)
        dlg.on_input(InputEvent.BUTTON_BD)
        assert cancelled == [True]
        assert mgr._overlay is None

    def test_back_button_no_cancel_callback(self):
        from g13_linux.menu.screens.toast import ConfirmDialog

        mgr = _make_manager()
        dlg = ConfirmDialog(mgr, "Sure?", on_confirm=lambda: None)
        mgr.show_overlay(dlg)
        dlg.on_input(InputEvent.BUTTON_BD)
        assert mgr._overlay is None

    def test_press_no_without_cancel_callback(self):
        from g13_linux.menu.screens.toast import ConfirmDialog

        mgr = _make_manager()
        dlg = ConfirmDialog(mgr, "Sure?", on_confirm=lambda: None, on_cancel=None)
        mgr.show_overlay(dlg)
        dlg.on_input(InputEvent.STICK_PRESS)  # No selected, no cancel callback
        assert mgr._overlay is None

    def test_unhandled_event(self):
        from g13_linux.menu.screens.toast import ConfirmDialog

        mgr = _make_manager()
        dlg = ConfirmDialog(mgr, "Sure?", on_confirm=lambda: None)
        assert dlg.on_input(InputEvent.BUTTON_M1) is False

    def test_render(self):
        from g13_linux.menu.screens.toast import ConfirmDialog

        mgr = _make_manager()
        dlg = ConfirmDialog(mgr, "Delete?", on_confirm=lambda: None)
        canvas = _mock_canvas()
        dlg.render(canvas)
        assert canvas.draw_rect.called
        assert canvas.draw_text.called


# ===================================================================
# MainMenuScreen
# ===================================================================


class TestMainMenuScreen:
    def test_init_has_five_items(self):
        from g13_linux.menu.screens.main_menu import MainMenuScreen

        mgr = _make_manager()
        menu = MainMenuScreen(mgr)
        assert len(menu.items) == 5
        ids = [item.id for item in menu.items]
        assert "profiles" in ids
        assert "macros" in ids
        assert "led" in ids
        assert "settings" in ids
        assert "info" in ids

    def test_all_items_have_submenus(self):
        from g13_linux.menu.screens.main_menu import MainMenuScreen

        mgr = _make_manager()
        menu = MainMenuScreen(mgr)
        for item in menu.items:
            assert item.submenu is not None

    def test_create_profiles_screen(self):
        from g13_linux.menu.screens.main_menu import MainMenuScreen

        mgr = _make_manager()
        menu = MainMenuScreen(mgr)
        screen = menu._create_profiles_screen()
        from g13_linux.menu.screens.profiles import ProfilesScreen

        assert isinstance(screen, ProfilesScreen)

    def test_create_macros_screen(self):
        from g13_linux.menu.screens.main_menu import MainMenuScreen

        mgr = _make_manager()
        mgr.daemon = MagicMock()
        mgr.daemon.macro_manager = None
        menu = MainMenuScreen(mgr)
        screen = menu._create_macros_screen()
        from g13_linux.menu.screens.macros import MacrosScreen

        assert isinstance(screen, MacrosScreen)

    def test_create_settings_screen(self):
        from g13_linux.menu.screens.main_menu import MainMenuScreen

        mgr = _make_manager()
        menu = MainMenuScreen(mgr)
        screen = menu._create_settings_screen()
        from g13_linux.menu.screens.settings import SettingsScreen

        assert isinstance(screen, SettingsScreen)

    def test_create_info_screen(self):
        from g13_linux.menu.screens.main_menu import MainMenuScreen

        mgr = _make_manager()
        menu = MainMenuScreen(mgr)
        screen = menu._create_info_screen()
        from g13_linux.menu.screens.info import InfoScreen

        assert isinstance(screen, InfoScreen)

    def test_create_led_screen(self):
        from g13_linux.menu.screens.main_menu import MainMenuScreen

        mgr = _make_manager()
        menu = MainMenuScreen(mgr)
        screen = menu._create_led_screen()
        from g13_linux.menu.screens.led_settings import LEDSettingsScreen

        assert isinstance(screen, LEDSettingsScreen)


# ===================================================================
# MacrosScreen
# ===================================================================


class TestMacrosScreen:
    def test_no_daemon_shows_no_macros(self):
        from g13_linux.menu.screens.macros import MacrosScreen

        mgr = _make_manager()
        mgr.daemon = None
        screen = MacrosScreen(mgr)
        # Should have "No macros" + "Record New"
        assert len(screen.items) == 2
        assert screen.items[0].id == "no_macros"
        assert screen.items[0].enabled is False
        assert screen.items[1].id == "record"

    def test_with_macros_builds_items(self):
        from g13_linux.menu.screens.macros import MacrosScreen

        mgr = _make_manager()
        daemon = MagicMock()
        daemon.macro_manager.list_macro_summaries.return_value = [
            {"id": "m1", "name": "Attack", "step_count": 5},
            {"id": "m2", "name": "Defend", "step_count": 3},
        ]
        mgr.daemon = daemon
        screen = MacrosScreen(mgr)
        # 2 macros + 1 "Record New"
        assert len(screen.items) == 3
        assert screen.items[0].id == "macro_m1"
        assert screen.items[1].id == "macro_m2"
        assert screen.items[2].id == "record"

    def test_long_macro_name_truncated(self):
        from g13_linux.menu.screens.macros import MacrosScreen

        mgr = _make_manager()
        daemon = MagicMock()
        daemon.macro_manager.list_macro_summaries.return_value = [
            {"id": "m1", "name": "A" * 20, "step_count": 2},
        ]
        mgr.daemon = daemon
        screen = MacrosScreen(mgr)
        assert len(screen.items[0].label) <= 20  # truncated name + " (2)"

    def test_on_enter_refreshes(self):
        from g13_linux.menu.screens.macros import MacrosScreen

        mgr = _make_manager()
        daemon = MagicMock()
        daemon.macro_manager.list_macro_summaries.return_value = []
        mgr.daemon = daemon
        screen = MacrosScreen(mgr)
        assert len(screen.items) >= 1  # at least "no macros" + "record"
        # Add macros
        daemon.macro_manager.list_macro_summaries.return_value = [
            {"id": "m1", "name": "New", "step_count": 1}
        ]
        screen.on_enter()
        assert len(screen.items) == 2  # 1 macro + Record New
        assert screen.selected_index == 0
        assert screen.scroll_offset == 0

    def test_show_macro_info(self):
        from g13_linux.menu.screens.macros import MacrosScreen

        mgr = _make_manager()
        daemon = MagicMock()
        macro = MagicMock()
        macro.name = "Test"
        macro.step_count = 10
        macro.duration_ms = 5000
        daemon.macro_manager.list_macro_summaries.return_value = [
            {"id": "m1", "name": "Test", "step_count": 10}
        ]
        daemon.macro_manager.load_macro.return_value = macro
        mgr.daemon = daemon
        screen = MacrosScreen(mgr)
        screen._show_macro_info("m1")
        assert mgr._overlay is not None

    def test_show_macro_info_not_found(self):
        from g13_linux.menu.screens.macros import MacrosScreen

        mgr = _make_manager()
        daemon = MagicMock()
        daemon.macro_manager.list_macro_summaries.return_value = []
        daemon.macro_manager.load_macro.side_effect = FileNotFoundError
        mgr.daemon = daemon
        screen = MacrosScreen(mgr)
        screen._show_macro_info("missing")
        assert mgr._overlay is not None  # error toast

    def test_record_macro(self):
        from g13_linux.menu.screens.macros import MacrosScreen

        mgr = _make_manager()
        mgr.daemon = None
        screen = MacrosScreen(mgr)
        screen._record_macro()
        assert mgr._overlay is not None


# ===================================================================
# SettingsScreen
# ===================================================================


class TestSettingsScreen:
    def test_init_items(self):
        from g13_linux.menu.screens.settings import SettingsScreen

        mgr = _make_manager()
        screen = SettingsScreen(mgr)
        ids = [i.id for i in screen.items]
        assert "clock" in ids
        assert "idle_timeout" in ids
        assert "stick_sensitivity" in ids
        assert "reset" in ids

    def test_timeout_value_no_settings(self):
        from g13_linux.menu.screens.settings import SettingsScreen

        mgr = _make_manager()
        screen = SettingsScreen(mgr)
        assert screen._get_timeout_value() == "30s"

    def test_timeout_value_never(self):
        from g13_linux.menu.screens.settings import SettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        mgr.settings_manager.idle_timeout = 0
        screen = SettingsScreen(mgr)
        assert screen._get_timeout_value() == "Never"

    def test_timeout_value_seconds(self):
        from g13_linux.menu.screens.settings import SettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        mgr.settings_manager.idle_timeout = 15
        screen = SettingsScreen(mgr)
        assert screen._get_timeout_value() == "15s"

    def test_timeout_value_minutes(self):
        from g13_linux.menu.screens.settings import SettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        mgr.settings_manager.idle_timeout = 120
        screen = SettingsScreen(mgr)
        assert screen._get_timeout_value() == "2m"

    def test_sensitivity_value_no_settings(self):
        from g13_linux.menu.screens.settings import SettingsScreen

        mgr = _make_manager()
        screen = SettingsScreen(mgr)
        assert screen._get_sensitivity_value() == "Normal"

    def test_sensitivity_value_with_settings(self):
        from g13_linux.menu.screens.settings import SettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        mgr.settings_manager.stick_sensitivity = "high"
        screen = SettingsScreen(mgr)
        assert screen._get_sensitivity_value() == "High"

    def test_cycle_sensitivity(self):
        from g13_linux.menu.screens.settings import SettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        mgr.settings_manager.stick_sensitivity = "low"
        screen = SettingsScreen(mgr)
        screen._cycle_sensitivity()
        assert mgr.settings_manager.stick_sensitivity == "normal"
        assert mgr._overlay is not None

    def test_cycle_sensitivity_wraps(self):
        from g13_linux.menu.screens.settings import SettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        mgr.settings_manager.stick_sensitivity = "high"
        screen = SettingsScreen(mgr)
        screen._cycle_sensitivity()
        assert mgr.settings_manager.stick_sensitivity == "low"

    def test_cycle_sensitivity_invalid_resets(self):
        from g13_linux.menu.screens.settings import SettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        mgr.settings_manager.stick_sensitivity = "bogus"
        screen = SettingsScreen(mgr)
        screen._cycle_sensitivity()
        assert mgr.settings_manager.stick_sensitivity == "normal"

    def test_cycle_sensitivity_no_settings(self):
        from g13_linux.menu.screens.settings import SettingsScreen

        mgr = _make_manager()
        screen = SettingsScreen(mgr)
        screen._cycle_sensitivity()  # no crash
        assert mgr._overlay is not None

    def test_reset_defaults(self):
        from g13_linux.menu.screens.settings import SettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        screen = SettingsScreen(mgr)
        screen._reset_defaults()
        mgr.settings_manager.reset_to_defaults.assert_called_once()
        assert mgr._overlay is not None

    def test_reset_defaults_no_settings(self):
        from g13_linux.menu.screens.settings import SettingsScreen

        mgr = _make_manager()
        screen = SettingsScreen(mgr)
        screen._reset_defaults()  # no crash
        assert mgr._overlay is not None


# ===================================================================
# ClockSettingsScreen
# ===================================================================


class TestClockSettingsScreen:
    def test_init_items(self):
        from g13_linux.menu.screens.settings import ClockSettingsScreen

        mgr = _make_manager()
        screen = ClockSettingsScreen(mgr)
        ids = [i.id for i in screen.items]
        assert "format_24" in ids
        assert "format_12" in ids
        assert "show_seconds" in ids
        assert "show_date" in ids

    def test_check_mark_selected(self):
        from g13_linux.menu.screens.settings import ClockSettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        mgr.settings_manager.clock_format = "24h"
        screen = ClockSettingsScreen(mgr)
        assert screen._check_mark("24h") == "*"
        assert screen._check_mark("12h") == ""

    def test_check_mark_no_settings(self):
        from g13_linux.menu.screens.settings import ClockSettingsScreen

        mgr = _make_manager()
        screen = ClockSettingsScreen(mgr)
        assert screen._check_mark("24h") == ""

    def test_seconds_value(self):
        from g13_linux.menu.screens.settings import ClockSettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        mgr.settings_manager.clock_show_seconds = True
        screen = ClockSettingsScreen(mgr)
        assert screen._get_seconds_value() == "On"
        mgr.settings_manager.clock_show_seconds = False
        assert screen._get_seconds_value() == "Off"

    def test_seconds_value_no_settings(self):
        from g13_linux.menu.screens.settings import ClockSettingsScreen

        mgr = _make_manager()
        screen = ClockSettingsScreen(mgr)
        assert screen._get_seconds_value() == "On"

    def test_date_value(self):
        from g13_linux.menu.screens.settings import ClockSettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        mgr.settings_manager.clock_show_date = False
        screen = ClockSettingsScreen(mgr)
        assert screen._get_date_value() == "Off"

    def test_date_value_no_settings(self):
        from g13_linux.menu.screens.settings import ClockSettingsScreen

        mgr = _make_manager()
        screen = ClockSettingsScreen(mgr)
        assert screen._get_date_value() == "On"

    def test_set_format(self):
        from g13_linux.menu.screens.settings import ClockSettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        screen = ClockSettingsScreen(mgr)
        screen._set_format("12h")
        assert mgr.settings_manager.clock_format == "12h"
        assert mgr._overlay is not None

    def test_toggle_seconds(self):
        from g13_linux.menu.screens.settings import ClockSettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        mgr.settings_manager.clock_show_seconds = True
        screen = ClockSettingsScreen(mgr)
        screen._toggle_seconds()
        assert mgr.settings_manager.clock_show_seconds is False
        assert mgr._overlay is not None

    def test_toggle_seconds_no_settings(self):
        from g13_linux.menu.screens.settings import ClockSettingsScreen

        mgr = _make_manager()
        screen = ClockSettingsScreen(mgr)
        screen._toggle_seconds()  # no crash
        assert mgr._overlay is not None

    def test_toggle_date(self):
        from g13_linux.menu.screens.settings import ClockSettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        mgr.settings_manager.clock_show_date = False
        screen = ClockSettingsScreen(mgr)
        screen._toggle_date()
        assert mgr.settings_manager.clock_show_date is True

    def test_toggle_date_no_settings(self):
        from g13_linux.menu.screens.settings import ClockSettingsScreen

        mgr = _make_manager()
        screen = ClockSettingsScreen(mgr)
        screen._toggle_date()  # no crash


# ===================================================================
# TimeoutSettingsScreen
# ===================================================================


class TestTimeoutSettingsScreen:
    def test_init_items(self):
        from g13_linux.menu.screens.settings import TimeoutSettingsScreen

        mgr = _make_manager()
        screen = TimeoutSettingsScreen(mgr)
        assert len(screen.items) == 5

    def test_check_mark_selected(self):
        from g13_linux.menu.screens.settings import TimeoutSettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        mgr.settings_manager.idle_timeout = 30
        screen = TimeoutSettingsScreen(mgr)
        assert screen._check_mark(30) == "*"
        assert screen._check_mark(0) == ""

    def test_check_mark_no_settings(self):
        from g13_linux.menu.screens.settings import TimeoutSettingsScreen

        mgr = _make_manager()
        screen = TimeoutSettingsScreen(mgr)
        assert screen._check_mark(30) == ""

    def test_set_timeout_seconds(self):
        from g13_linux.menu.screens.settings import TimeoutSettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        screen = TimeoutSettingsScreen(mgr)
        mgr.push(screen)
        screen._set_timeout(15)
        assert mgr.settings_manager.idle_timeout == 15
        assert mgr._overlay is not None

    def test_set_timeout_never(self):
        from g13_linux.menu.screens.settings import TimeoutSettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        screen = TimeoutSettingsScreen(mgr)
        mgr.push(screen)
        screen._set_timeout(0)
        assert mgr.settings_manager.idle_timeout == 0

    def test_set_timeout_minutes(self):
        from g13_linux.menu.screens.settings import TimeoutSettingsScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        screen = TimeoutSettingsScreen(mgr)
        mgr.push(screen)
        screen._set_timeout(300)
        assert mgr.settings_manager.idle_timeout == 300

    def test_set_timeout_pops_screen(self):
        from g13_linux.menu.screens.settings import TimeoutSettingsScreen

        mgr = _make_manager()
        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = TimeoutSettingsScreen(mgr)
        mgr.push(screen)
        screen._set_timeout(30)
        # Should have popped back
        assert mgr.current is base


# ===================================================================
# InfoScreen
# ===================================================================


class TestInfoScreen:
    def test_init_grabs_deps(self):
        from g13_linux.menu.screens.info import InfoScreen

        mgr = _make_manager()
        mgr.daemon = MagicMock()
        mgr.profile_manager = MagicMock()
        screen = InfoScreen(mgr)
        assert screen.daemon is mgr.daemon
        assert screen.profile_manager is mgr.profile_manager

    def test_init_no_deps(self):
        from g13_linux.menu.screens.info import InfoScreen

        mgr = _make_manager()
        screen = InfoScreen(mgr)
        assert screen.daemon is None
        assert screen.profile_manager is None

    def test_back_button_pops(self):
        from g13_linux.menu.screens.info import InfoScreen

        mgr = _make_manager()
        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = InfoScreen(mgr)
        mgr.push(screen)
        screen.on_input(InputEvent.BUTTON_BD)
        assert mgr.current is base

    def test_stick_press_pops(self):
        from g13_linux.menu.screens.info import InfoScreen

        mgr = _make_manager()
        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = InfoScreen(mgr)
        mgr.push(screen)
        screen.on_input(InputEvent.STICK_PRESS)
        assert mgr.current is base

    def test_unhandled_input(self):
        from g13_linux.menu.screens.info import InfoScreen

        mgr = _make_manager()
        screen = InfoScreen(mgr)
        assert screen.on_input(InputEvent.STICK_UP) is False

    def test_render_no_deps(self):
        from g13_linux.menu.screens.info import InfoScreen

        mgr = _make_manager()
        screen = InfoScreen(mgr)
        canvas = _mock_canvas()
        screen.render(canvas)
        assert canvas.draw_text.called

    def test_render_with_profile_current_name(self):
        from g13_linux.menu.screens.info import InfoScreen

        mgr = _make_manager()
        mgr.profile_manager = MagicMock(spec=["current_name"])
        mgr.profile_manager.current_name = "MyProfile"
        screen = InfoScreen(mgr)
        canvas = _mock_canvas()
        screen.render(canvas)

    def test_render_with_profile_current_attr(self):
        from g13_linux.menu.screens.info import InfoScreen

        mgr = _make_manager()
        pm = MagicMock(spec=["current"])
        pm.current = MagicMock()
        pm.current.name = "AltProfile"
        mgr.profile_manager = pm
        screen = InfoScreen(mgr)
        canvas = _mock_canvas()
        screen.render(canvas)

    def test_render_with_daemon_stats(self):
        from g13_linux.menu.screens.info import InfoScreen

        mgr = _make_manager()
        mgr.daemon = MagicMock()
        mgr.daemon.uptime = "1:23:45"
        mgr.daemon.key_count = 9999
        screen = InfoScreen(mgr)
        canvas = _mock_canvas()
        screen.render(canvas)

    def test_render_with_led_controller(self):
        from g13_linux.menu.screens.info import InfoScreen

        mgr = _make_manager()
        led = MagicMock()
        led.current_color.to_hex.return_value = "#FF0000"
        led.current_effect.value = "pulse"
        mgr.led_controller = led
        screen = InfoScreen(mgr)
        canvas = _mock_canvas()
        screen.render(canvas)

    def test_render_with_led_no_effect(self):
        from g13_linux.menu.screens.info import InfoScreen

        mgr = _make_manager()
        led = MagicMock()
        led.current_color.to_hex.return_value = "#00FF00"
        led.current_effect = None
        mgr.led_controller = led
        screen = InfoScreen(mgr)
        canvas = _mock_canvas()
        screen.render(canvas)

    def test_version_constant(self):
        from g13_linux.menu.screens.info import InfoScreen

        assert InfoScreen.VERSION == "1.0.0"


# ===================================================================
# ProfilesScreen
# ===================================================================


class TestProfilesScreen:
    def test_no_profile_manager(self):
        from g13_linux.menu.screens.profiles import ProfilesScreen

        mgr = _make_manager()
        screen = ProfilesScreen(mgr)
        assert len(screen.items) == 1
        assert screen.items[0].id == "no_pm"
        assert screen.items[0].enabled is False

    def test_with_profiles(self):
        from g13_linux.menu.screens.profiles import ProfilesScreen

        mgr = _make_manager()
        pm = MagicMock()
        pm.current_name = "default"
        pm.list_profiles.return_value = ["default", "gaming"]
        mgr.profile_manager = pm
        screen = ProfilesScreen(mgr)
        # 2 profiles + "New Profile"
        assert len(screen.items) == 3
        assert "* " in screen.items[0].label  # current marked
        assert "  " in screen.items[1].label  # non-current

    def test_with_profiles_dict_attr(self):
        from g13_linux.menu.screens.profiles import ProfilesScreen

        mgr = _make_manager()
        pm = MagicMock(spec=["current_name", "profiles"])
        pm.current_name = "a"
        pm.profiles = {"a": None, "b": None}
        mgr.profile_manager = pm
        screen = ProfilesScreen(mgr)
        # 2 profiles + New Profile
        assert len(screen.items) == 3

    def test_select_profile_success(self):
        from g13_linux.menu.screens.profiles import ProfilesScreen

        mgr = _make_manager()
        pm = MagicMock()
        pm.current_name = "default"
        pm.list_profiles.return_value = ["default", "gaming"]
        profile = MagicMock()
        profile.backlight = {"color": "#FF0000"}
        pm.load_profile.return_value = profile
        mgr.profile_manager = pm
        led = MagicMock()
        mgr.led_controller = led

        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = ProfilesScreen(mgr)
        mgr.push(screen)
        screen._select_profile("gaming")
        pm.load_profile.assert_called_with("gaming")
        led.set_color.assert_called_with(255, 0, 0)
        assert mgr._overlay is not None  # toast

    def test_select_profile_not_found(self):
        from g13_linux.menu.screens.profiles import ProfilesScreen

        mgr = _make_manager()
        pm = MagicMock()
        pm.current_name = "default"
        pm.list_profiles.return_value = ["default"]
        pm.load_profile.side_effect = FileNotFoundError
        mgr.profile_manager = pm

        screen = ProfilesScreen(mgr)
        mgr.push(screen)
        screen._select_profile("missing")
        assert mgr._overlay is not None  # error toast

    def test_select_profile_generic_error(self):
        from g13_linux.menu.screens.profiles import ProfilesScreen

        mgr = _make_manager()
        pm = MagicMock()
        pm.current_name = "default"
        pm.list_profiles.return_value = ["default"]
        pm.load_profile.side_effect = RuntimeError("oops")
        mgr.profile_manager = pm

        screen = ProfilesScreen(mgr)
        mgr.push(screen)
        screen._select_profile("default")
        assert mgr._overlay is not None

    def test_select_profile_no_pm(self):
        from g13_linux.menu.screens.profiles import ProfilesScreen

        mgr = _make_manager()
        screen = ProfilesScreen(mgr)
        screen._select_profile("x")  # should not raise

    def test_apply_profile_hardware_no_led(self):
        from g13_linux.menu.screens.profiles import ProfilesScreen

        mgr = _make_manager()
        pm = MagicMock()
        pm.current_name = "a"
        pm.list_profiles.return_value = ["a"]
        mgr.profile_manager = pm
        screen = ProfilesScreen(mgr)
        profile = MagicMock()
        profile.backlight = {"color": "#00FF00"}
        screen._apply_profile_hardware(profile)  # no led, no crash

    def test_apply_profile_hardware_invalid_color(self):
        from g13_linux.menu.screens.profiles import ProfilesScreen

        mgr = _make_manager()
        pm = MagicMock()
        pm.current_name = "a"
        pm.list_profiles.return_value = ["a"]
        mgr.profile_manager = pm
        led = MagicMock()
        mgr.led_controller = led
        screen = ProfilesScreen(mgr)
        profile = MagicMock()
        profile.backlight = {"color": "red"}  # not hex format
        screen._apply_profile_hardware(profile)
        led.set_color.assert_not_called()

    def test_apply_profile_hardware_short_hex(self):
        from g13_linux.menu.screens.profiles import ProfilesScreen

        mgr = _make_manager()
        pm = MagicMock()
        pm.current_name = "a"
        pm.list_profiles.return_value = ["a"]
        mgr.profile_manager = pm
        led = MagicMock()
        mgr.led_controller = led
        screen = ProfilesScreen(mgr)
        profile = MagicMock()
        profile.backlight = {"color": "#FFF"}  # too short
        screen._apply_profile_hardware(profile)
        led.set_color.assert_not_called()

    def test_create_profile(self):
        from g13_linux.menu.screens.profiles import ProfilesScreen

        mgr = _make_manager()
        pm = MagicMock()
        pm.current_name = "a"
        pm.list_profiles.return_value = ["a"]
        mgr.profile_manager = pm
        screen = ProfilesScreen(mgr)
        screen._create_profile()
        assert mgr._overlay is not None

    def test_on_enter_refreshes(self):
        from g13_linux.menu.screens.profiles import ProfilesScreen

        mgr = _make_manager()
        pm = MagicMock()
        pm.current_name = "a"
        pm.list_profiles.return_value = ["a"]
        mgr.profile_manager = pm
        screen = ProfilesScreen(mgr)
        # Modify profiles
        pm.list_profiles.return_value = ["a", "b", "c"]
        screen.on_enter()
        # 3 profiles + New Profile = 4
        assert len(screen.items) == 4
        assert screen.selected_index == 0
        assert screen.scroll_offset == 0


# ===================================================================
# IdleScreen
# ===================================================================


class TestIdleScreen:
    def test_init(self):
        from g13_linux.menu.screens.idle import IdleScreen

        mgr = _make_manager()
        screen = IdleScreen(mgr)
        assert screen.profile_manager is None
        assert screen.settings_manager is None

    def test_on_input_returns_false(self):
        from g13_linux.menu.screens.idle import IdleScreen

        mgr = _make_manager()
        screen = IdleScreen(mgr)
        assert screen.on_input(InputEvent.STICK_PRESS) is False
        assert screen.on_input(InputEvent.BUTTON_BD) is False

    def test_update_marks_dirty_on_second_change(self):
        from g13_linux.menu.screens.idle import IdleScreen

        mgr = _make_manager()
        screen = IdleScreen(mgr)
        screen._dirty = False
        screen._last_second = -1
        screen.update(0.016)
        assert screen.is_dirty is True

    def test_update_no_seconds_mode(self):
        from g13_linux.menu.screens.idle import IdleScreen

        mgr = _make_manager()
        sm = MagicMock()
        sm.clock_show_seconds = False
        screen = IdleScreen(mgr, settings_manager=sm)
        screen._dirty = False
        screen._last_second = -1
        screen.update(0.016)
        assert screen.is_dirty is True

    def test_render_no_profile(self):
        from g13_linux.menu.screens.idle import IdleScreen

        mgr = _make_manager()
        mgr.daemon = None
        screen = IdleScreen(mgr)
        canvas = _mock_canvas()
        screen.render(canvas)
        assert canvas.draw_text.called
        canvas.draw_text_centered.assert_called()

    def test_render_with_profile(self):
        from g13_linux.menu.screens.idle import IdleScreen

        mgr = _make_manager()
        mgr.daemon = None
        pm = MagicMock()
        pm.current = MagicMock()
        pm.current.name = "Gaming"
        pm.current.m_state = 2
        screen = IdleScreen(mgr, profile_manager=pm)
        canvas = _mock_canvas()
        screen.render(canvas)

    def test_render_with_profile_current_name(self):
        from g13_linux.menu.screens.idle import IdleScreen

        mgr = _make_manager()
        mgr.daemon = None
        pm = MagicMock(spec=["current_name"])
        pm.current_name = "Alt"
        screen = IdleScreen(mgr, profile_manager=pm)
        canvas = _mock_canvas()
        screen.render(canvas)

    def test_render_with_daemon(self):
        from g13_linux.menu.screens.idle import IdleScreen

        mgr = _make_manager()
        mgr.daemon = MagicMock()
        mgr.daemon.uptime = "0:05"
        mgr.daemon.key_count = 42
        screen = IdleScreen(mgr)
        canvas = _mock_canvas()
        screen.render(canvas)

    def test_format_time_24h_seconds(self):
        from g13_linux.menu.screens.idle import IdleScreen

        mgr = _make_manager()
        screen = IdleScreen(mgr)
        result = screen._format_time()
        # Default: 24h with seconds
        assert ":" in result

    def test_format_time_12h_no_seconds(self):
        from g13_linux.menu.screens.idle import IdleScreen

        mgr = _make_manager()
        sm = MagicMock()
        sm.clock_format = "12h"
        sm.clock_show_seconds = False
        screen = IdleScreen(mgr, settings_manager=sm)
        result = screen._format_time()
        # Should contain AM or PM
        assert "M" in result

    def test_format_time_12h_with_seconds(self):
        from g13_linux.menu.screens.idle import IdleScreen

        mgr = _make_manager()
        sm = MagicMock()
        sm.clock_format = "12h"
        sm.clock_show_seconds = True
        screen = IdleScreen(mgr, settings_manager=sm)
        result = screen._format_time()
        assert "M" in result

    def test_format_time_24h_no_seconds(self):
        from g13_linux.menu.screens.idle import IdleScreen

        mgr = _make_manager()
        sm = MagicMock()
        sm.clock_format = "24h"
        sm.clock_show_seconds = False
        screen = IdleScreen(mgr, settings_manager=sm)
        result = screen._format_time()
        # HH:MM only
        assert len(result) == 5


# ===================================================================
# ClockScreen
# ===================================================================


class TestClockScreen:
    def test_init_defaults(self):
        from g13_linux.menu.screens.idle import ClockScreen

        mgr = _make_manager()
        screen = ClockScreen(mgr)
        assert screen.show_seconds is True
        assert screen.show_date is True

    def test_init_custom(self):
        from g13_linux.menu.screens.idle import ClockScreen

        mgr = _make_manager()
        screen = ClockScreen(mgr, show_seconds=False, show_date=False)
        assert screen.show_seconds is False
        assert screen.show_date is False

    def test_stick_press_pops(self):
        from g13_linux.menu.screens.idle import ClockScreen

        mgr = _make_manager()
        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = ClockScreen(mgr)
        mgr.push(screen)
        screen.on_input(InputEvent.STICK_PRESS)
        assert mgr.current is base

    def test_other_input_returns_false(self):
        from g13_linux.menu.screens.idle import ClockScreen

        mgr = _make_manager()
        screen = ClockScreen(mgr)
        assert screen.on_input(InputEvent.STICK_UP) is False

    def test_update_with_seconds(self):
        from g13_linux.menu.screens.idle import ClockScreen

        mgr = _make_manager()
        screen = ClockScreen(mgr, show_seconds=True)
        screen._dirty = False
        screen._last_second = -1
        screen.update(0.016)
        assert screen.is_dirty is True

    def test_update_without_seconds(self):
        from g13_linux.menu.screens.idle import ClockScreen

        mgr = _make_manager()
        screen = ClockScreen(mgr, show_seconds=False)
        screen._dirty = False
        screen._last_second = -1
        screen.update(0.016)
        assert screen.is_dirty is True

    def test_render_with_seconds_and_date(self):
        from g13_linux.menu.screens.idle import ClockScreen

        mgr = _make_manager()
        screen = ClockScreen(mgr, show_seconds=True, show_date=True)
        canvas = _mock_canvas()
        screen.render(canvas)
        assert canvas.draw_text_centered.call_count >= 2

    def test_render_no_seconds_no_date(self):
        from g13_linux.menu.screens.idle import ClockScreen

        mgr = _make_manager()
        screen = ClockScreen(mgr, show_seconds=False, show_date=False)
        canvas = _mock_canvas()
        screen.render(canvas)
        assert canvas.draw_text_centered.call_count == 1


# ===================================================================
# LEDSettingsScreen
# ===================================================================


class TestLEDSettingsScreen:
    def test_init_items(self):
        from g13_linux.menu.screens.led_settings import LEDSettingsScreen

        mgr = _make_manager()
        screen = LEDSettingsScreen(mgr)
        ids = [i.id for i in screen.items]
        assert "color" in ids
        assert "brightness" in ids
        assert "effect" in ids
        assert "off" in ids

    def test_color_value_no_led(self):
        from g13_linux.menu.screens.led_settings import LEDSettingsScreen

        mgr = _make_manager()
        screen = LEDSettingsScreen(mgr)
        assert screen._get_color_value() == "#FFFFFF"

    def test_color_value_with_led(self):
        from g13_linux.menu.screens.led_settings import LEDSettingsScreen

        mgr = _make_manager()
        led = MagicMock()
        led.current_color.to_hex.return_value = "#00FF00"
        mgr.led_controller = led
        screen = LEDSettingsScreen(mgr)
        assert screen._get_color_value() == "#00FF00"

    def test_brightness_value_no_led(self):
        from g13_linux.menu.screens.led_settings import LEDSettingsScreen

        mgr = _make_manager()
        screen = LEDSettingsScreen(mgr)
        assert screen._get_brightness_value() == "100%"

    def test_brightness_value_with_led(self):
        from g13_linux.menu.screens.led_settings import LEDSettingsScreen

        mgr = _make_manager()
        led = MagicMock()
        led.brightness = 50
        mgr.led_controller = led
        screen = LEDSettingsScreen(mgr)
        assert screen._get_brightness_value() == "50%"

    def test_effect_value_no_led(self):
        from g13_linux.menu.screens.led_settings import LEDSettingsScreen

        mgr = _make_manager()
        screen = LEDSettingsScreen(mgr)
        assert screen._get_effect_value() == "None"

    def test_effect_value_with_led(self):
        from g13_linux.menu.screens.led_settings import LEDSettingsScreen

        mgr = _make_manager()
        led = MagicMock()
        led.current_effect.value = "rainbow"
        mgr.led_controller = led
        screen = LEDSettingsScreen(mgr)
        assert screen._get_effect_value() == "rainbow"

    def test_effect_value_none_effect(self):
        from g13_linux.menu.screens.led_settings import LEDSettingsScreen

        mgr = _make_manager()
        led = MagicMock()
        led.current_effect = None
        mgr.led_controller = led
        screen = LEDSettingsScreen(mgr)
        assert screen._get_effect_value() == "None"

    def test_turn_off(self):
        from g13_linux.menu.screens.led_settings import LEDSettingsScreen

        mgr = _make_manager()
        led = MagicMock()
        mgr.led_controller = led
        screen = LEDSettingsScreen(mgr)
        screen._turn_off()
        led.off.assert_called_once()
        assert mgr._overlay is not None

    def test_turn_off_no_led(self):
        from g13_linux.menu.screens.led_settings import LEDSettingsScreen

        mgr = _make_manager()
        screen = LEDSettingsScreen(mgr)
        screen._turn_off()  # no crash
        assert mgr._overlay is not None


# ===================================================================
# ColorPickerScreen
# ===================================================================


class TestColorPickerScreen:
    def test_init_default_selection(self):
        from g13_linux.menu.screens.led_settings import ColorPickerScreen

        mgr = _make_manager()
        screen = ColorPickerScreen(mgr)
        assert screen.selected == 0

    def test_init_finds_current_color(self):
        from g13_linux.led.colors import RGB
        from g13_linux.menu.screens.led_settings import ColorPickerScreen

        mgr = _make_manager()
        led = MagicMock()
        led.current_color = RGB(0, 255, 0)  # Green
        mgr.led_controller = led
        screen = ColorPickerScreen(mgr)
        assert screen.selected == 3  # Green is index 3

    def test_navigate_left(self):
        from g13_linux.menu.screens.led_settings import ColorPickerScreen

        mgr = _make_manager()
        screen = ColorPickerScreen(mgr)
        screen.selected = 0
        screen.on_input(InputEvent.STICK_LEFT)
        assert screen.selected == len(screen.PRESETS) - 1  # wrap

    def test_navigate_right(self):
        from g13_linux.menu.screens.led_settings import ColorPickerScreen

        mgr = _make_manager()
        screen = ColorPickerScreen(mgr)
        screen.on_input(InputEvent.STICK_RIGHT)
        assert screen.selected == 1

    def test_navigate_right_wraps(self):
        from g13_linux.menu.screens.led_settings import ColorPickerScreen

        mgr = _make_manager()
        screen = ColorPickerScreen(mgr)
        screen.selected = len(screen.PRESETS) - 1
        screen.on_input(InputEvent.STICK_RIGHT)
        assert screen.selected == 0

    def test_preview_color(self):
        from g13_linux.menu.screens.led_settings import ColorPickerScreen

        mgr = _make_manager()
        led = MagicMock()
        mgr.led_controller = led
        screen = ColorPickerScreen(mgr)
        screen.on_input(InputEvent.STICK_RIGHT)
        led.set_rgb.assert_called()

    def test_apply_color(self):
        from g13_linux.menu.screens.led_settings import ColorPickerScreen

        mgr = _make_manager()
        led = MagicMock()
        mgr.led_controller = led
        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = ColorPickerScreen(mgr)
        mgr.push(screen)
        screen.on_input(InputEvent.STICK_PRESS)
        led.stop_effect.assert_called()
        led.set_rgb.assert_called()
        assert mgr.current is base  # popped

    def test_back_button_pops(self):
        from g13_linux.menu.screens.led_settings import ColorPickerScreen

        mgr = _make_manager()
        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = ColorPickerScreen(mgr)
        mgr.push(screen)
        screen.on_input(InputEvent.BUTTON_BD)
        assert mgr.current is base

    def test_unhandled_returns_false(self):
        from g13_linux.menu.screens.led_settings import ColorPickerScreen

        mgr = _make_manager()
        screen = ColorPickerScreen(mgr)
        assert screen.on_input(InputEvent.BUTTON_M1) is False

    def test_render(self):
        from g13_linux.menu.screens.led_settings import ColorPickerScreen

        mgr = _make_manager()
        screen = ColorPickerScreen(mgr)
        canvas = _mock_canvas()
        screen.render(canvas)
        assert canvas.draw_text.called
        assert canvas.draw_text_centered.called
        assert canvas.draw_rect.called


# ===================================================================
# BrightnessScreen
# ===================================================================


class TestBrightnessScreen:
    def test_init_default(self):
        from g13_linux.menu.screens.led_settings import BrightnessScreen

        mgr = _make_manager()
        screen = BrightnessScreen(mgr)
        assert screen.brightness == 100

    def test_init_from_led(self):
        from g13_linux.menu.screens.led_settings import BrightnessScreen

        mgr = _make_manager()
        led = MagicMock()
        led.brightness = 70
        mgr.led_controller = led
        screen = BrightnessScreen(mgr)
        assert screen.brightness == 70

    def test_decrease_brightness(self):
        from g13_linux.menu.screens.led_settings import BrightnessScreen

        mgr = _make_manager()
        screen = BrightnessScreen(mgr)
        screen.on_input(InputEvent.STICK_LEFT)
        assert screen.brightness == 90

    def test_increase_brightness(self):
        from g13_linux.menu.screens.led_settings import BrightnessScreen

        mgr = _make_manager()
        screen = BrightnessScreen(mgr)
        screen.brightness = 50
        screen.on_input(InputEvent.STICK_RIGHT)
        assert screen.brightness == 60

    def test_brightness_min_clamp(self):
        from g13_linux.menu.screens.led_settings import BrightnessScreen

        mgr = _make_manager()
        screen = BrightnessScreen(mgr)
        screen.brightness = 0
        screen.on_input(InputEvent.STICK_LEFT)
        assert screen.brightness == 0

    def test_brightness_max_clamp(self):
        from g13_linux.menu.screens.led_settings import BrightnessScreen

        mgr = _make_manager()
        screen = BrightnessScreen(mgr)
        screen.brightness = 100
        screen.on_input(InputEvent.STICK_RIGHT)
        assert screen.brightness == 100

    def test_apply_brightness(self):
        from g13_linux.menu.screens.led_settings import BrightnessScreen

        mgr = _make_manager()
        led = MagicMock()
        mgr.led_controller = led
        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = BrightnessScreen(mgr)
        mgr.push(screen)
        screen.brightness = 80
        screen.on_input(InputEvent.STICK_PRESS)
        led.set_brightness.assert_called_with(80)
        assert mgr.current is base

    def test_cancel_restores(self):
        from g13_linux.menu.screens.led_settings import BrightnessScreen

        mgr = _make_manager()
        led = MagicMock()
        led.brightness = 60
        mgr.led_controller = led
        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = BrightnessScreen(mgr)
        mgr.push(screen)
        screen.on_input(InputEvent.BUTTON_BD)
        led.set_brightness.assert_called_with(60)
        assert mgr.current is base

    def test_unhandled_returns_false(self):
        from g13_linux.menu.screens.led_settings import BrightnessScreen

        mgr = _make_manager()
        screen = BrightnessScreen(mgr)
        assert screen.on_input(InputEvent.BUTTON_M1) is False

    def test_render(self):
        from g13_linux.menu.screens.led_settings import BrightnessScreen

        mgr = _make_manager()
        screen = BrightnessScreen(mgr)
        canvas = _mock_canvas()
        screen.render(canvas)
        assert canvas.draw_text.called
        assert canvas.draw_rect.called

    def test_render_zero_brightness(self):
        from g13_linux.menu.screens.led_settings import BrightnessScreen

        mgr = _make_manager()
        screen = BrightnessScreen(mgr)
        screen.brightness = 0
        canvas = _mock_canvas()
        screen.render(canvas)


# ===================================================================
# EffectSelectScreen
# ===================================================================


class TestEffectSelectScreen:
    def test_init_items(self):
        from g13_linux.menu.screens.led_settings import EffectSelectScreen

        mgr = _make_manager()
        screen = EffectSelectScreen(mgr)
        ids = [i.id for i in screen.items]
        assert "solid" in ids
        assert "pulse" in ids
        assert "rainbow" in ids
        assert "fade" in ids
        assert "none" in ids

    def test_set_effect_solid(self):
        from g13_linux.led.effects import EffectType
        from g13_linux.menu.screens.led_settings import EffectSelectScreen

        mgr = _make_manager()
        led = MagicMock()
        mgr.led_controller = led
        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = EffectSelectScreen(mgr)
        mgr.push(screen)
        screen._set_effect(EffectType.SOLID)
        led.stop_effect.assert_called()
        assert mgr._overlay is not None

    def test_set_effect_pulse(self):
        from g13_linux.led.effects import EffectType
        from g13_linux.menu.screens.led_settings import EffectSelectScreen

        mgr = _make_manager()
        led = MagicMock()
        mgr.led_controller = led
        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = EffectSelectScreen(mgr)
        mgr.push(screen)
        screen._set_effect(EffectType.PULSE)
        led.start_effect.assert_called_once()

    def test_set_effect_rainbow(self):
        from g13_linux.led.effects import EffectType
        from g13_linux.menu.screens.led_settings import EffectSelectScreen

        mgr = _make_manager()
        led = MagicMock()
        mgr.led_controller = led
        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = EffectSelectScreen(mgr)
        mgr.push(screen)
        screen._set_effect(EffectType.RAINBOW)
        led.start_effect.assert_called_once()

    def test_set_effect_fade(self):
        from g13_linux.led.effects import EffectType
        from g13_linux.menu.screens.led_settings import EffectSelectScreen

        mgr = _make_manager()
        led = MagicMock()
        mgr.led_controller = led
        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = EffectSelectScreen(mgr)
        mgr.push(screen)
        screen._set_effect(EffectType.FADE)
        led.start_effect.assert_called_once()

    def test_set_effect_no_led(self):
        from g13_linux.led.effects import EffectType
        from g13_linux.menu.screens.led_settings import EffectSelectScreen

        mgr = _make_manager()
        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = EffectSelectScreen(mgr)
        mgr.push(screen)
        screen._set_effect(EffectType.PULSE)  # no crash, no led

    def test_stop_effect(self):
        from g13_linux.menu.screens.led_settings import EffectSelectScreen

        mgr = _make_manager()
        led = MagicMock()
        mgr.led_controller = led
        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = EffectSelectScreen(mgr)
        mgr.push(screen)
        screen._stop_effect()
        led.stop_effect.assert_called()
        assert mgr._overlay is not None

    def test_stop_effect_no_led(self):
        from g13_linux.menu.screens.led_settings import EffectSelectScreen

        mgr = _make_manager()
        base = ConcreteScreen(mgr)
        mgr.push(base)
        screen = EffectSelectScreen(mgr)
        mgr.push(screen)
        screen._stop_effect()  # no crash


# ===================================================================
# Integration-style tests
# ===================================================================


class TestMenuIntegration:
    """End-to-end navigation through multiple screens."""

    def test_main_menu_navigate_and_enter_settings(self):
        from g13_linux.menu.screens.main_menu import MainMenuScreen

        mgr = _make_manager()
        main = MainMenuScreen(mgr)
        mgr.push(main)

        # Navigate down to Settings (index 3)
        for _ in range(3):
            mgr.handle_input(InputEvent.STICK_DOWN)
        assert main.selected_index == 3

        # Enter settings
        mgr.handle_input(InputEvent.STICK_PRESS)
        from g13_linux.menu.screens.settings import SettingsScreen

        assert isinstance(mgr.current, SettingsScreen)
        assert mgr.stack_depth == 2

        # Back out
        mgr.handle_input(InputEvent.BUTTON_BD)
        assert mgr.current is main

    def test_pop_to_root_from_deep_navigation(self):
        from g13_linux.menu.screens.main_menu import MainMenuScreen

        mgr = _make_manager()
        mgr.settings_manager = MagicMock()
        mgr.settings_manager.clock_format = "24h"

        main = MainMenuScreen(mgr)
        mgr.push(main)

        # Go into Settings > Clock
        mgr.handle_input(InputEvent.STICK_DOWN)  # 1
        mgr.handle_input(InputEvent.STICK_DOWN)  # 2
        mgr.handle_input(InputEvent.STICK_DOWN)  # 3 = Settings
        mgr.handle_input(InputEvent.STICK_PRESS)
        assert mgr.stack_depth == 2

        # Enter Clock submenu
        mgr.handle_input(InputEvent.STICK_PRESS)  # Clock is first item
        assert mgr.stack_depth == 3

        mgr.pop_to_root()
        assert mgr.stack_depth == 1
        assert mgr.current is main

    def test_overlay_while_navigating(self):
        from g13_linux.menu.screens.main_menu import MainMenuScreen
        from g13_linux.menu.screens.toast import ToastScreen

        mgr = _make_manager()
        main = MainMenuScreen(mgr)
        mgr.push(main)

        toast = ToastScreen(mgr, "Hello!")
        mgr.show_overlay(toast, duration=5.0)

        # Input goes to overlay first
        mgr.handle_input(InputEvent.STICK_PRESS)
        assert mgr._overlay is None  # toast dismissed

        # Now input goes to menu
        mgr.handle_input(InputEvent.STICK_DOWN)
        assert main.selected_index == 1

        # Cleanup timer
        if mgr._overlay_timer:
            mgr._overlay_timer.cancel()

    def test_full_render_cycle(self):
        from g13_linux.menu.screens.main_menu import MainMenuScreen

        mgr = _make_manager()
        main = MainMenuScreen(mgr)
        mgr.push(main)

        # First render
        assert mgr.render() is True
        assert main.is_dirty is False

        # No change => no render
        assert mgr.render() is False

        # Navigate => dirty => render
        mgr.handle_input(InputEvent.STICK_DOWN)
        assert main.is_dirty is True
        assert mgr.render() is True
