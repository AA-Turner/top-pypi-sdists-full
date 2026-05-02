"""Global hotkey registration for standalone macro triggers."""

from collections.abc import Callable

from PyQt6.QtCore import QObject, pyqtSignal


class GlobalHotkeyManager(QObject):
    """
    Manages global hotkey registration for standalone macro triggers.

    Uses pynput for system-wide hotkey capture.

    Signals:
        hotkey_triggered(str): Emitted when a registered hotkey is pressed (macro_id)
        error_occurred(str): Emitted on errors
    """

    hotkey_triggered = pyqtSignal(str)  # macro_id
    error_occurred = pyqtSignal(str)

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._hotkeys: dict[str, str] = {}  # hotkey_string -> macro_id
        self._listener = None
        self._running = False

    @property
    def is_running(self) -> bool:
        """True if listening for hotkeys."""
        return self._running

    @property
    def registered_hotkeys(self) -> dict[str, str]:
        """Return copy of registered hotkeys."""
        return self._hotkeys.copy()

    def register_hotkey(self, hotkey: str, macro_id: str) -> bool:
        """
        Register a global hotkey to trigger a macro.

        Args:
            hotkey: Hotkey string (e.g., "ctrl+shift+f1")
            macro_id: Macro ID to trigger

        Returns:
            True if registration successful
        """
        # Normalize hotkey format
        normalized = self._normalize_hotkey(hotkey)
        if not normalized:
            self.error_occurred.emit(f"Invalid hotkey format: {hotkey}")
            return False

        self._hotkeys[normalized] = macro_id

        # Restart listener to pick up new hotkey
        if self._running:
            self._restart_listener()

        return True

    def unregister_hotkey(self, hotkey: str) -> bool:
        """
        Unregister a hotkey.

        Args:
            hotkey: Hotkey string to unregister

        Returns:
            True if hotkey was registered and removed
        """
        normalized = self._normalize_hotkey(hotkey)
        if normalized and normalized in self._hotkeys:
            del self._hotkeys[normalized]
            if self._running:
                self._restart_listener()
            return True
        return False

    def unregister_macro(self, macro_id: str) -> int:
        """
        Remove all hotkeys for a macro.

        Args:
            macro_id: Macro ID to unregister

        Returns:
            Number of hotkeys removed
        """
        to_remove = [k for k, v in self._hotkeys.items() if v == macro_id]
        for hotkey in to_remove:
            del self._hotkeys[hotkey]

        if to_remove and self._running:
            self._restart_listener()

        return len(to_remove)

    def get_macro_for_hotkey(self, hotkey: str) -> str | None:
        """Get macro ID for a hotkey."""
        normalized = self._normalize_hotkey(hotkey)
        return self._hotkeys.get(normalized) if normalized else None

    def get_hotkey_for_macro(self, macro_id: str) -> str | None:
        """Get hotkey string for a macro (first match)."""
        for hotkey, mid in self._hotkeys.items():
            if mid == macro_id:
                return hotkey
        return None

    def start(self) -> bool:
        """
        Start listening for hotkeys.

        Returns:
            True if started successfully
        """
        if self._running:
            return True

        if not self._hotkeys:
            # Nothing to listen for
            self._running = True
            return True

        return self._start_listener()

    def stop(self) -> None:
        """Stop listening for hotkeys."""
        self._running = False
        self._stop_listener()

    def _start_listener(self) -> bool:
        """Start the pynput hotkey listener."""
        try:
            from pynput import keyboard

            # Build hotkey handlers
            hotkey_handlers = {}
            for hotkey_str, macro_id in self._hotkeys.items():
                # Convert to pynput format and create handler
                pynput_combo = self._to_pynput_format(hotkey_str)
                if pynput_combo:
                    # Create a closure to capture macro_id
                    def make_handler(mid: str) -> Callable:
                        def handler():
                            self.hotkey_triggered.emit(mid)

                        return handler

                    hotkey_handlers[pynput_combo] = make_handler(macro_id)

            if hotkey_handlers:
                self._listener = keyboard.GlobalHotKeys(hotkey_handlers)
                self._listener.start()
                self._running = True
                return True
            else:
                self._running = True
                return True

        except ImportError:
            self.error_occurred.emit("pynput not installed - global hotkeys disabled")
            return False
        except Exception as e:
            self.error_occurred.emit(f"Failed to start hotkey listener: {e}")
            return False

    def _stop_listener(self) -> None:
        """Stop the pynput listener."""
        if self._listener:
            try:
                self._listener.stop()
            except Exception:
                pass
            self._listener = None

    def _restart_listener(self) -> None:
        """Restart listener with updated hotkeys."""
        self._stop_listener()
        if self._running and self._hotkeys:
            self._start_listener()

    def _normalize_hotkey(self, hotkey: str) -> str | None:
        """
        Normalize hotkey string to consistent format.

        Input formats accepted:
        - "Ctrl+Shift+F1"
        - "ctrl+shift+f1"
        - "CTRL + SHIFT + F1"

        Output format: "ctrl+shift+f1" (lowercase, no spaces)
        """
        if not hotkey:
            return None

        # Lowercase and remove spaces
        normalized = hotkey.lower().replace(" ", "")

        # Split into parts and filter empty strings
        parts = normalized.split("+")
        valid_parts = []

        for part in parts:
            if not part:
                continue

            # Normalize modifier names
            if part in ("control",):
                part = "ctrl"
            elif part in ("super", "meta", "win"):
                part = "cmd"

            valid_parts.append(part)

        if not valid_parts:
            return None

        return "+".join(valid_parts)

    def _to_pynput_format(self, hotkey: str) -> str | None:
        """
        Convert normalized hotkey to pynput GlobalHotKeys format.

        Input: "ctrl+shift+f1"
        Output: "<ctrl>+<shift>+<f1>"
        """
        if not hotkey:
            return None

        parts = hotkey.split("+")
        pynput_parts = []

        for part in parts:
            # Modifiers and special keys get angle brackets
            if part in ("ctrl", "alt", "shift", "cmd"):
                pynput_parts.append(f"<{part}>")
            elif part.startswith("f") and part[1:].isdigit():
                # Function keys: f1-f12
                pynput_parts.append(f"<{part}>")
            elif part in (
                "space",
                "tab",
                "enter",
                "return",
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
                "esc",
            ):
                # Special keys
                if part == "return":
                    part = "enter"
                elif part == "esc":
                    part = "escape"
                pynput_parts.append(f"<{part}>")
            elif len(part) == 1:
                # Single character keys
                pynput_parts.append(part)
            else:
                # Unknown key
                return None

        return "+".join(pynput_parts)

    def clear_all(self) -> None:
        """Remove all registered hotkeys."""
        self._hotkeys.clear()
        if self._running:
            self._stop_listener()
