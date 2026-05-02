"""Tests for GlobalHotkeyManager."""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def manager(qtbot):
    """Create GlobalHotkeyManager instance."""
    from g13_linux.gui.models.global_hotkeys import GlobalHotkeyManager

    mgr = GlobalHotkeyManager()
    return mgr


class TestGlobalHotkeyManagerInit:
    """Tests for GlobalHotkeyManager initialization."""

    def test_init_empty_hotkeys(self, manager):
        """Test manager starts with no hotkeys."""
        assert manager.registered_hotkeys == {}

    def test_init_not_running(self, manager):
        """Test manager starts not running."""
        assert manager.is_running is False

    def test_init_no_listener(self, manager):
        """Test manager starts with no listener."""
        assert manager._listener is None


class TestGlobalHotkeyManagerSignals:
    """Tests for signal availability."""

    def test_has_hotkey_triggered_signal(self, manager):
        """Test hotkey_triggered signal exists."""
        assert hasattr(manager, "hotkey_triggered")

    def test_has_error_occurred_signal(self, manager):
        """Test error_occurred signal exists."""
        assert hasattr(manager, "error_occurred")


class TestGlobalHotkeyManagerRegister:
    """Tests for hotkey registration."""

    def test_register_hotkey(self, manager):
        """Test registering a hotkey."""
        result = manager.register_hotkey("ctrl+shift+f1", "macro-123")

        assert result is True
        assert "ctrl+shift+f1" in manager.registered_hotkeys
        assert manager.registered_hotkeys["ctrl+shift+f1"] == "macro-123"

    def test_register_hotkey_normalizes(self, manager):
        """Test hotkey is normalized on registration."""
        manager.register_hotkey("Ctrl + Shift + F1", "macro-123")

        assert "ctrl+shift+f1" in manager.registered_hotkeys

    def test_register_invalid_hotkey(self, manager, qtbot):
        """Test registering invalid hotkey emits error."""
        with qtbot.waitSignal(manager.error_occurred, timeout=1000):
            result = manager.register_hotkey("", "macro-123")

        assert result is False

    def test_register_hotkey_while_running(self, manager):
        """Test registering hotkey while running restarts listener."""
        manager._running = True
        manager._hotkeys = {"ctrl+a": "old-macro"}

        with patch.object(manager, "_restart_listener") as mock_restart:
            manager.register_hotkey("ctrl+b", "new-macro")

            mock_restart.assert_called_once()


class TestGlobalHotkeyManagerUnregister:
    """Tests for hotkey unregistration."""

    def test_unregister_hotkey(self, manager):
        """Test unregistering a hotkey."""
        manager._hotkeys["ctrl+shift+f1"] = "macro-123"

        result = manager.unregister_hotkey("ctrl+shift+f1")

        assert result is True
        assert "ctrl+shift+f1" not in manager.registered_hotkeys

    def test_unregister_nonexistent_hotkey(self, manager):
        """Test unregistering nonexistent hotkey returns False."""
        result = manager.unregister_hotkey("ctrl+z")

        assert result is False

    def test_unregister_hotkey_while_running(self, manager):
        """Test unregistering while running restarts listener."""
        manager._running = True
        manager._hotkeys = {"ctrl+a": "macro-1", "ctrl+b": "macro-2"}

        with patch.object(manager, "_restart_listener") as mock_restart:
            manager.unregister_hotkey("ctrl+a")

            mock_restart.assert_called_once()

    def test_unregister_macro(self, manager):
        """Test unregistering all hotkeys for a macro."""
        manager._hotkeys = {
            "ctrl+a": "macro-1",
            "ctrl+b": "macro-1",
            "ctrl+c": "macro-2",
        }

        count = manager.unregister_macro("macro-1")

        assert count == 2
        assert "ctrl+a" not in manager._hotkeys
        assert "ctrl+b" not in manager._hotkeys
        assert "ctrl+c" in manager._hotkeys

    def test_unregister_macro_not_found(self, manager):
        """Test unregistering macro with no hotkeys returns 0."""
        count = manager.unregister_macro("nonexistent")

        assert count == 0

    def test_unregister_macro_while_running(self, manager):
        """Test unregistering macro while running restarts listener."""
        manager._running = True
        manager._hotkeys = {"ctrl+a": "macro-1"}

        with patch.object(manager, "_restart_listener") as mock_restart:
            manager.unregister_macro("macro-1")

            mock_restart.assert_called_once()


class TestGlobalHotkeyManagerLookup:
    """Tests for hotkey lookup methods."""

    def test_get_macro_for_hotkey(self, manager):
        """Test getting macro ID for hotkey."""
        manager._hotkeys["ctrl+f1"] = "macro-123"

        result = manager.get_macro_for_hotkey("ctrl+f1")

        assert result == "macro-123"

    def test_get_macro_for_nonexistent_hotkey(self, manager):
        """Test getting macro for nonexistent hotkey returns None."""
        result = manager.get_macro_for_hotkey("ctrl+z")

        assert result is None

    def test_get_macro_for_invalid_hotkey(self, manager):
        """Test getting macro for invalid hotkey returns None."""
        result = manager.get_macro_for_hotkey("")

        assert result is None

    def test_get_hotkey_for_macro(self, manager):
        """Test getting hotkey for macro."""
        manager._hotkeys["ctrl+f1"] = "macro-123"

        result = manager.get_hotkey_for_macro("macro-123")

        assert result == "ctrl+f1"

    def test_get_hotkey_for_nonexistent_macro(self, manager):
        """Test getting hotkey for nonexistent macro returns None."""
        result = manager.get_hotkey_for_macro("nonexistent")

        assert result is None


class TestGlobalHotkeyManagerStartStop:
    """Tests for start/stop methods."""

    def test_start_when_already_running(self, manager):
        """Test start returns True when already running."""
        manager._running = True

        result = manager.start()

        assert result is True

    def test_start_with_no_hotkeys(self, manager):
        """Test start with no hotkeys marks as running."""
        result = manager.start()

        assert result is True
        assert manager.is_running is True

    def test_start_with_hotkeys(self, manager):
        """Test start with hotkeys starts listener."""
        manager._hotkeys = {"ctrl+f1": "macro-123"}

        with patch.object(manager, "_start_listener", return_value=True) as mock_start:
            result = manager.start()

            mock_start.assert_called_once()
            assert result is True

    def test_stop(self, manager):
        """Test stop sets running to False and stops listener."""
        manager._running = True

        with patch.object(manager, "_stop_listener") as mock_stop:
            manager.stop()

            assert manager._running is False
            mock_stop.assert_called_once()


class TestGlobalHotkeyManagerListener:
    """Tests for listener internals."""

    def test_start_listener_success(self, manager):
        """Test successful listener start with pynput mocked."""
        import sys

        manager._hotkeys = {"ctrl+f1": "macro-123"}

        # Mock pynput module to avoid X11 requirement in CI
        # Remove cached module so patch takes effect
        cached_pynput = sys.modules.pop("pynput", None)
        cached_keyboard = sys.modules.pop("pynput.keyboard", None)

        try:
            mock_keyboard = MagicMock()
            mock_listener = MagicMock()
            mock_keyboard.GlobalHotKeys.return_value = mock_listener

            with patch.dict(
                "sys.modules",
                {"pynput": MagicMock(keyboard=mock_keyboard), "pynput.keyboard": mock_keyboard},
            ):
                result = manager._start_listener()

                assert result is True
                assert manager._running is True
                mock_listener.start.assert_called_once()
        finally:
            # Restore cached modules
            if cached_pynput:
                sys.modules["pynput"] = cached_pynput
            if cached_keyboard:
                sys.modules["pynput.keyboard"] = cached_keyboard

        # Cleanup
        manager._stop_listener()

    def test_start_listener_no_handlers(self, manager):
        """Test listener start with invalid hotkeys still marks running."""
        import sys

        manager._hotkeys = {"invalid+++key": "macro-123"}

        # Mock pynput to avoid X11 requirement
        cached_pynput = sys.modules.pop("pynput", None)
        cached_keyboard = sys.modules.pop("pynput.keyboard", None)

        try:
            mock_keyboard = MagicMock()
            with patch.dict(
                "sys.modules",
                {"pynput": MagicMock(keyboard=mock_keyboard), "pynput.keyboard": mock_keyboard},
            ):
                result = manager._start_listener()

                # Still returns True even if no valid handlers (handlers dict empty)
                assert result is True
                assert manager._running is True
        finally:
            if cached_pynput:
                sys.modules["pynput"] = cached_pynput
            if cached_keyboard:
                sys.modules["pynput.keyboard"] = cached_keyboard

    def test_start_listener_with_valid_hotkeys(self, manager):
        """Test listener start creates actual listener."""
        import sys

        manager._hotkeys = {"ctrl+a": "macro-123"}

        # Mock pynput for CI
        cached_pynput = sys.modules.pop("pynput", None)
        cached_keyboard = sys.modules.pop("pynput.keyboard", None)

        try:
            mock_keyboard = MagicMock()
            mock_listener = MagicMock()
            mock_keyboard.GlobalHotKeys.return_value = mock_listener

            with patch.dict(
                "sys.modules",
                {"pynput": MagicMock(keyboard=mock_keyboard), "pynput.keyboard": mock_keyboard},
            ):
                result = manager._start_listener()

                assert result is True
                assert manager._listener is not None
        finally:
            if cached_pynput:
                sys.modules["pynput"] = cached_pynput
            if cached_keyboard:
                sys.modules["pynput.keyboard"] = cached_keyboard

        # Cleanup
        manager._stop_listener()

    def test_stop_listener(self, manager):
        """Test stopping listener."""
        mock_listener = MagicMock()
        manager._listener = mock_listener

        manager._stop_listener()

        mock_listener.stop.assert_called_once()
        assert manager._listener is None

    def test_stop_listener_no_listener(self, manager):
        """Test stopping when no listener exists."""
        manager._listener = None

        # Should not raise
        manager._stop_listener()

    def test_stop_listener_exception(self, manager):
        """Test stopping listener with exception."""
        mock_listener = MagicMock()
        mock_listener.stop.side_effect = Exception("Stop error")
        manager._listener = mock_listener

        # Should not raise
        manager._stop_listener()
        assert manager._listener is None

    def test_restart_listener(self, manager):
        """Test restart listener stops and starts."""
        manager._running = True
        manager._hotkeys = {"ctrl+f1": "macro-123"}

        with patch.object(manager, "_stop_listener") as mock_stop:
            with patch.object(manager, "_start_listener") as mock_start:
                manager._restart_listener()

                mock_stop.assert_called_once()
                mock_start.assert_called_once()

    def test_restart_listener_not_running(self, manager):
        """Test restart when not running only stops."""
        manager._running = False
        manager._hotkeys = {"ctrl+f1": "macro-123"}

        with patch.object(manager, "_stop_listener") as mock_stop:
            with patch.object(manager, "_start_listener") as mock_start:
                manager._restart_listener()

                mock_stop.assert_called_once()
                mock_start.assert_not_called()

    def test_restart_listener_no_hotkeys(self, manager):
        """Test restart with no hotkeys only stops."""
        manager._running = True
        manager._hotkeys = {}

        with patch.object(manager, "_stop_listener") as mock_stop:
            with patch.object(manager, "_start_listener") as mock_start:
                manager._restart_listener()

                mock_stop.assert_called_once()
                mock_start.assert_not_called()


class TestGlobalHotkeyManagerNormalize:
    """Tests for hotkey normalization."""

    def test_normalize_lowercase(self, manager):
        """Test normalization lowercases input."""
        result = manager._normalize_hotkey("CTRL+SHIFT+F1")

        assert result == "ctrl+shift+f1"

    def test_normalize_removes_spaces(self, manager):
        """Test normalization removes spaces."""
        result = manager._normalize_hotkey("ctrl + shift + f1")

        assert result == "ctrl+shift+f1"

    def test_normalize_control_to_ctrl(self, manager):
        """Test normalization converts 'control' to 'ctrl'."""
        result = manager._normalize_hotkey("control+a")

        assert result == "ctrl+a"

    def test_normalize_super_to_cmd(self, manager):
        """Test normalization converts 'super' to 'cmd'."""
        result = manager._normalize_hotkey("super+a")

        assert result == "cmd+a"

    def test_normalize_meta_to_cmd(self, manager):
        """Test normalization converts 'meta' to 'cmd'."""
        result = manager._normalize_hotkey("meta+a")

        assert result == "cmd+a"

    def test_normalize_win_to_cmd(self, manager):
        """Test normalization converts 'win' to 'cmd'."""
        result = manager._normalize_hotkey("win+a")

        assert result == "cmd+a"

    def test_normalize_empty_string(self, manager):
        """Test normalization of empty string returns None."""
        result = manager._normalize_hotkey("")

        assert result is None

    def test_normalize_none(self, manager):
        """Test normalization of None returns None."""
        result = manager._normalize_hotkey(None)

        assert result is None

    def test_normalize_skips_empty_parts(self, manager):
        """Test normalization skips empty parts from double plus."""
        result = manager._normalize_hotkey("ctrl++a")

        assert result == "ctrl+a"

    def test_normalize_only_empty_parts(self, manager):
        """Test normalization with only empty parts returns None."""
        result = manager._normalize_hotkey("+++")

        assert result is None


class TestGlobalHotkeyManagerPynputFormat:
    """Tests for pynput format conversion."""

    def test_to_pynput_format_modifiers(self, manager):
        """Test converting modifiers to pynput format."""
        result = manager._to_pynput_format("ctrl+shift+alt")

        assert result == "<ctrl>+<shift>+<alt>"

    def test_to_pynput_format_function_keys(self, manager):
        """Test converting function keys to pynput format."""
        result = manager._to_pynput_format("f1")
        assert result == "<f1>"

        result = manager._to_pynput_format("f12")
        assert result == "<f12>"

    def test_to_pynput_format_special_keys(self, manager):
        """Test converting special keys to pynput format."""
        for key in [
            "space",
            "tab",
            "enter",
            "backspace",
            "delete",
            "home",
            "end",
            "pageup",
            "pagedown",
            "up",
            "down",
            "left",
            "right",
            "insert",
            "escape",
        ]:
            result = manager._to_pynput_format(key)
            assert result == f"<{key}>"

    def test_to_pynput_format_return_to_enter(self, manager):
        """Test 'return' is converted to 'enter'."""
        result = manager._to_pynput_format("return")

        assert result == "<enter>"

    def test_to_pynput_format_esc_to_escape(self, manager):
        """Test 'esc' is converted to 'escape'."""
        result = manager._to_pynput_format("esc")

        assert result == "<escape>"

    def test_to_pynput_format_single_char(self, manager):
        """Test single character keys are not wrapped."""
        result = manager._to_pynput_format("a")

        assert result == "a"

    def test_to_pynput_format_combo(self, manager):
        """Test full combo conversion."""
        result = manager._to_pynput_format("ctrl+shift+a")

        assert result == "<ctrl>+<shift>+a"

    def test_to_pynput_format_unknown_key(self, manager):
        """Test unknown multi-char key returns None."""
        result = manager._to_pynput_format("unknownkey")

        assert result is None

    def test_to_pynput_format_empty(self, manager):
        """Test empty string returns None."""
        result = manager._to_pynput_format("")

        assert result is None

    def test_to_pynput_format_none(self, manager):
        """Test None returns None."""
        result = manager._to_pynput_format(None)

        assert result is None

    def test_to_pynput_format_cmd(self, manager):
        """Test cmd modifier converts to pynput format."""
        result = manager._to_pynput_format("cmd+a")

        assert result == "<cmd>+a"


class TestGlobalHotkeyManagerClearAll:
    """Tests for clear_all method."""

    def test_clear_all(self, manager):
        """Test clearing all hotkeys."""
        manager._hotkeys = {"ctrl+a": "macro-1", "ctrl+b": "macro-2"}

        manager.clear_all()

        assert manager._hotkeys == {}

    def test_clear_all_stops_listener(self, manager):
        """Test clear_all stops listener when running."""
        manager._running = True
        manager._hotkeys = {"ctrl+a": "macro-1"}

        with patch.object(manager, "_stop_listener") as mock_stop:
            manager.clear_all()

            mock_stop.assert_called_once()

    def test_clear_all_not_running(self, manager):
        """Test clear_all does not call stop when not running."""
        manager._running = False
        manager._hotkeys = {"ctrl+a": "macro-1"}

        with patch.object(manager, "_stop_listener") as mock_stop:
            manager.clear_all()

            mock_stop.assert_not_called()


class TestGlobalHotkeyManagerHotkeyTriggered:
    """Tests for hotkey trigger functionality."""

    def test_hotkey_signal_can_be_emitted(self, manager, qtbot):
        """Test hotkey_triggered signal can be emitted and received."""
        received = []
        manager.hotkey_triggered.connect(received.append)

        with qtbot.waitSignal(manager.hotkey_triggered, timeout=1000) as blocker:
            manager.hotkey_triggered.emit("macro-123")

        assert blocker.args == ["macro-123"]
        assert received == ["macro-123"]

    def test_make_handler_closure(self, manager, qtbot):
        """Test the closure pattern used for hotkey handlers."""

        # Test the pattern used in _start_listener
        def make_handler(mid: str):
            def handler():
                manager.hotkey_triggered.emit(mid)

            return handler

        handler = make_handler("test-macro-id")

        with qtbot.waitSignal(manager.hotkey_triggered, timeout=1000) as blocker:
            handler()

        assert blocker.args == ["test-macro-id"]


class TestGlobalHotkeyManagerMissingCoverage:
    """Tests for edge cases to achieve 100% coverage."""

    def test_start_listener_import_error(self, manager, qtbot):
        """Test _start_listener handles ImportError when pynput unavailable (lines 163-165)."""
        import sys

        manager._hotkeys = {"ctrl+f1": "macro-123"}

        errors = []
        manager.error_occurred.connect(errors.append)

        # Remove pynput from modules to force fresh import attempt
        cached_pynput = sys.modules.pop("pynput", None)
        cached_keyboard = sys.modules.pop("pynput.keyboard", None)

        try:
            # Patch import to fail for pynput
            original_import = (
                __builtins__.__import__ if hasattr(__builtins__, "__import__") else __import__
            )

            def mock_import(name, *args, **kwargs):
                if name == "pynput" or name.startswith("pynput."):
                    raise ImportError("No module named 'pynput'")
                return original_import(name, *args, **kwargs)

            with patch("builtins.__import__", side_effect=mock_import):
                result = manager._start_listener()

            assert result is False
            assert len(errors) == 1
            assert "pynput not installed" in errors[0]
        finally:
            # Restore cached modules
            if cached_pynput:
                sys.modules["pynput"] = cached_pynput
            if cached_keyboard:
                sys.modules["pynput.keyboard"] = cached_keyboard

    def test_start_listener_generic_exception(self, manager, qtbot):
        """Test _start_listener handles generic Exception (lines 166-168)."""
        import sys

        manager._hotkeys = {"ctrl+f1": "macro-123"}

        errors = []
        manager.error_occurred.connect(errors.append)

        # Remove pynput from modules
        cached_pynput = sys.modules.pop("pynput", None)
        cached_keyboard = sys.modules.pop("pynput.keyboard", None)

        try:
            # Create mock that raises exception on GlobalHotKeys instantiation
            mock_keyboard = MagicMock()
            mock_keyboard.GlobalHotKeys.side_effect = RuntimeError("X11 display not found")

            with patch.dict(
                "sys.modules",
                {"pynput": MagicMock(keyboard=mock_keyboard), "pynput.keyboard": mock_keyboard},
            ):
                result = manager._start_listener()

            assert result is False
            assert len(errors) == 1
            assert "Failed to start hotkey listener" in errors[0]
        finally:
            if cached_pynput:
                sys.modules["pynput"] = cached_pynput
            if cached_keyboard:
                sys.modules["pynput.keyboard"] = cached_keyboard

    def test_handler_closure_emits_signal(self, manager, qtbot):
        """Test the actual handler closure created in _start_listener emits signal (line 148)."""
        import sys

        manager._hotkeys = {"ctrl+a": "test-macro-id"}

        # Remove pynput from modules
        cached_pynput = sys.modules.pop("pynput", None)
        cached_keyboard = sys.modules.pop("pynput.keyboard", None)

        captured_handlers = {}

        try:
            mock_keyboard = MagicMock()
            mock_listener = MagicMock()

            def capture_handlers(handlers):
                captured_handlers.update(handlers)
                return mock_listener

            mock_keyboard.GlobalHotKeys.side_effect = capture_handlers

            with patch.dict(
                "sys.modules",
                {"pynput": MagicMock(keyboard=mock_keyboard), "pynput.keyboard": mock_keyboard},
            ):
                manager._start_listener()

            # The handler should have been captured
            assert len(captured_handlers) == 1
            pynput_key = "<ctrl>+a"
            assert pynput_key in captured_handlers

            # Call the handler and verify signal is emitted
            with qtbot.waitSignal(manager.hotkey_triggered, timeout=1000) as blocker:
                captured_handlers[pynput_key]()

            assert blocker.args == ["test-macro-id"]
        finally:
            if cached_pynput:
                sys.modules["pynput"] = cached_pynput
            if cached_keyboard:
                sys.modules["pynput.keyboard"] = cached_keyboard

        # Cleanup
        manager._stop_listener()
