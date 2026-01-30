"""
CSSL Keyboard Framework - Keyboard input handling for CSSL
Version 4.9.7

Provides keyboard listening, key state checking, and hotkey registration.
Cross-platform support using pynput library.

Usage in CSSL:
    keyboard = include("cssl-keyboard");

    // Listen for a key
    keyboard('listen', 'ESCAPE', myCallback);

    // Check if key is pressed
    if (keyboard::isPressed('SPACE')) {
        printl("Space pressed!");
    }

    // Register hotkey
    keyboard::hotkey('CTRL+S', saveFunction);
"""

import threading
import time
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from enum import Enum, IntEnum
from dataclasses import dataclass
import queue

# Try to import pynput for keyboard handling
try:
    from pynput import keyboard as pynput_keyboard
    from pynput.keyboard import Key, KeyCode
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False

# Fallback to tkinter for basic keyboard support
import tkinter as tk


class KeyState(IntEnum):
    """Key state constants"""
    Released = 0
    Pressed = 1
    Held = 2


class CsslKey(Enum):
    """CSSL Key constants - maps to common key names"""
    # Letters
    A = 'a'
    B = 'b'
    C = 'c'
    D = 'd'
    E = 'e'
    F = 'f'
    G = 'g'
    H = 'h'
    I = 'i'
    J = 'j'
    K = 'k'
    L = 'l'
    M = 'm'
    N = 'n'
    O = 'o'
    P = 'p'
    Q = 'q'
    R = 'r'
    S = 's'
    T = 't'
    U = 'u'
    V = 'v'
    W = 'w'
    X = 'x'
    Y = 'y'
    Z = 'z'

    # Numbers
    NUM_0 = '0'
    NUM_1 = '1'
    NUM_2 = '2'
    NUM_3 = '3'
    NUM_4 = '4'
    NUM_5 = '5'
    NUM_6 = '6'
    NUM_7 = '7'
    NUM_8 = '8'
    NUM_9 = '9'

    # Function keys
    F1 = 'f1'
    F2 = 'f2'
    F3 = 'f3'
    F4 = 'f4'
    F5 = 'f5'
    F6 = 'f6'
    F7 = 'f7'
    F8 = 'f8'
    F9 = 'f9'
    F10 = 'f10'
    F11 = 'f11'
    F12 = 'f12'

    # Special keys
    ESCAPE = 'escape'
    ENTER = 'enter'
    RETURN = 'return'
    TAB = 'tab'
    SPACE = 'space'
    BACKSPACE = 'backspace'
    DELETE = 'delete'
    INSERT = 'insert'
    HOME = 'home'
    END = 'end'
    PAGE_UP = 'page_up'
    PAGE_DOWN = 'page_down'

    # Arrow keys
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    # Modifier keys
    SHIFT = 'shift'
    CTRL = 'ctrl'
    CONTROL = 'ctrl'
    ALT = 'alt'
    CMD = 'cmd'
    WIN = 'win'
    SUPER = 'super'
    CAPS_LOCK = 'caps_lock'

    # Numpad
    NUMPAD_0 = 'numpad_0'
    NUMPAD_1 = 'numpad_1'
    NUMPAD_2 = 'numpad_2'
    NUMPAD_3 = 'numpad_3'
    NUMPAD_4 = 'numpad_4'
    NUMPAD_5 = 'numpad_5'
    NUMPAD_6 = 'numpad_6'
    NUMPAD_7 = 'numpad_7'
    NUMPAD_8 = 'numpad_8'
    NUMPAD_9 = 'numpad_9'
    NUMPAD_PLUS = 'numpad_plus'
    NUMPAD_MINUS = 'numpad_minus'
    NUMPAD_MULTIPLY = 'numpad_multiply'
    NUMPAD_DIVIDE = 'numpad_divide'
    NUMPAD_ENTER = 'numpad_enter'
    NUMPAD_DOT = 'numpad_dot'


@dataclass
class KeyListener:
    """A registered key listener"""
    key: str
    callback: Callable
    once: bool = False
    active: bool = True


@dataclass
class HotkeyListener:
    """A registered hotkey listener"""
    keys: Set[str]
    callback: Callable
    active: bool = True


class CsslKeyboardController:
    """The main keyboard controller - handles all keyboard operations"""

    _instance: Optional['CsslKeyboardController'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self._pressed_keys: Set[str] = set()
        self._key_states: Dict[str, KeyState] = {}
        self._listeners: Dict[str, List[KeyListener]] = {}
        self._hotkey_listeners: List[HotkeyListener] = []
        self._global_listeners: List[Callable] = []
        self._listener_thread: Optional[threading.Thread] = None
        self._running = False
        self._event_queue: queue.Queue = queue.Queue()
        self._pynput_listener = None
        self._cssl_runtime = None

        # Key name mapping
        self._key_map = self._build_key_map()

        # Start the keyboard listener
        self._start_listener()

    def _build_key_map(self) -> Dict[str, str]:
        """Build a mapping of key names to standardized names"""
        key_map = {}

        # Map pynput Key enum to our names
        if PYNPUT_AVAILABLE:
            key_map.update({
                'Key.esc': 'escape',
                'Key.escape': 'escape',
                'Key.enter': 'enter',
                'Key.return': 'enter',
                'Key.tab': 'tab',
                'Key.space': 'space',
                'Key.backspace': 'backspace',
                'Key.delete': 'delete',
                'Key.insert': 'insert',
                'Key.home': 'home',
                'Key.end': 'end',
                'Key.page_up': 'page_up',
                'Key.page_down': 'page_down',
                'Key.up': 'up',
                'Key.down': 'down',
                'Key.left': 'left',
                'Key.right': 'right',
                'Key.shift': 'shift',
                'Key.shift_l': 'shift',
                'Key.shift_r': 'shift',
                'Key.ctrl': 'ctrl',
                'Key.ctrl_l': 'ctrl',
                'Key.ctrl_r': 'ctrl',
                'Key.alt': 'alt',
                'Key.alt_l': 'alt',
                'Key.alt_r': 'alt',
                'Key.cmd': 'cmd',
                'Key.cmd_l': 'cmd',
                'Key.cmd_r': 'cmd',
                'Key.caps_lock': 'caps_lock',
                'Key.f1': 'f1',
                'Key.f2': 'f2',
                'Key.f3': 'f3',
                'Key.f4': 'f4',
                'Key.f5': 'f5',
                'Key.f6': 'f6',
                'Key.f7': 'f7',
                'Key.f8': 'f8',
                'Key.f9': 'f9',
                'Key.f10': 'f10',
                'Key.f11': 'f11',
                'Key.f12': 'f12',
            })

        # Add common aliases
        aliases = {
            'ESC': 'escape',
            'ESCAPE': 'escape',
            'RETURN': 'enter',
            'ENTER': 'enter',
            'SPACE': 'space',
            'TAB': 'tab',
            'BACKSPACE': 'backspace',
            'DELETE': 'delete',
            'DEL': 'delete',
            'INSERT': 'insert',
            'INS': 'insert',
            'HOME': 'home',
            'END': 'end',
            'PAGEUP': 'page_up',
            'PAGE_UP': 'page_up',
            'PAGEDOWN': 'page_down',
            'PAGE_DOWN': 'page_down',
            'UP': 'up',
            'DOWN': 'down',
            'LEFT': 'left',
            'RIGHT': 'right',
            'ARROW_UP': 'up',
            'ARROW_DOWN': 'down',
            'ARROW_LEFT': 'left',
            'ARROW_RIGHT': 'right',
            'SHIFT': 'shift',
            'CTRL': 'ctrl',
            'CONTROL': 'ctrl',
            'ALT': 'alt',
            'CMD': 'cmd',
            'WIN': 'cmd',
            'SUPER': 'cmd',
            'META': 'cmd',
            'CAPSLOCK': 'caps_lock',
            'CAPS_LOCK': 'caps_lock',
            'CAPS': 'caps_lock',
        }

        # Add function key aliases
        for i in range(1, 13):
            aliases[f'F{i}'] = f'f{i}'

        key_map.update(aliases)

        # Add lowercase versions
        for k, v in list(key_map.items()):
            key_map[k.lower()] = v

        return key_map

    def _normalize_key(self, key: Any) -> str:
        """Normalize a key to a standard string representation"""
        if key is None:
            return ''

        key_str = str(key)

        # Check direct mapping
        if key_str in self._key_map:
            return self._key_map[key_str]

        # Handle pynput KeyCode
        if PYNPUT_AVAILABLE:
            if hasattr(key, 'char') and key.char:
                return key.char.lower()
            if hasattr(key, 'name'):
                name = f"Key.{key.name}"
                if name in self._key_map:
                    return self._key_map[name]
                return key.name.lower()

        # Return as-is if no mapping found
        return key_str.lower().replace("'", "")

    def _start_listener(self) -> None:
        """Start the keyboard listener"""
        if self._running:
            return

        self._running = True

        if PYNPUT_AVAILABLE:
            def on_press(key):
                normalized = self._normalize_key(key)
                self._pressed_keys.add(normalized)
                self._key_states[normalized] = KeyState.Pressed
                self._trigger_listeners(normalized, 'press')
                self._check_hotkeys()

            def on_release(key):
                normalized = self._normalize_key(key)
                self._pressed_keys.discard(normalized)
                self._key_states[normalized] = KeyState.Released
                self._trigger_listeners(normalized, 'release')

            self._pynput_listener = pynput_keyboard.Listener(
                on_press=on_press,
                on_release=on_release
            )
            self._pynput_listener.daemon = True
            self._pynput_listener.start()
        else:
            print("[CsslKeyboard] Warning: pynput not available, keyboard listening limited")

    def _stop_listener(self) -> None:
        """Stop the keyboard listener"""
        self._running = False
        if self._pynput_listener:
            self._pynput_listener.stop()
            self._pynput_listener = None

    def _trigger_listeners(self, key: str, event_type: str) -> None:
        """Trigger registered listeners for a key"""
        if key in self._listeners:
            for listener in self._listeners[key][:]:  # Copy list to allow removal
                if listener.active:
                    try:
                        listener.callback()
                    except Exception as e:
                        print(f"[CsslKeyboard] Listener error: {e}")

                    if listener.once:
                        self._listeners[key].remove(listener)

        # Trigger global listeners
        for callback in self._global_listeners:
            try:
                callback(key, event_type)
            except Exception as e:
                print(f"[CsslKeyboard] Global listener error: {e}")

    def _check_hotkeys(self) -> None:
        """Check if any hotkeys are triggered"""
        for hotkey in self._hotkey_listeners:
            if hotkey.active and hotkey.keys.issubset(self._pressed_keys):
                try:
                    hotkey.callback()
                except Exception as e:
                    print(f"[CsslKeyboard] Hotkey error: {e}")

    def listen(self, key: str, callback: Callable, once: bool = False) -> None:
        """Register a listener for a key"""
        normalized = self._normalize_key(key)

        if normalized not in self._listeners:
            self._listeners[normalized] = []

        self._listeners[normalized].append(KeyListener(
            key=normalized,
            callback=callback,
            once=once
        ))

    def unlisten(self, key: str, callback: Callable = None) -> bool:
        """Remove a listener for a key"""
        normalized = self._normalize_key(key)

        if normalized not in self._listeners:
            return False

        if callback is None:
            # Remove all listeners for this key
            self._listeners[normalized] = []
            return True
        else:
            # Remove specific callback
            original_len = len(self._listeners[normalized])
            self._listeners[normalized] = [
                l for l in self._listeners[normalized]
                if l.callback != callback
            ]
            return len(self._listeners[normalized]) < original_len

    def hotkey(self, keys: str, callback: Callable) -> None:
        """Register a hotkey combination (e.g., 'CTRL+S')"""
        key_parts = keys.upper().replace(' ', '').split('+')
        normalized_keys = set()

        for part in key_parts:
            normalized = self._normalize_key(part)
            normalized_keys.add(normalized)

        self._hotkey_listeners.append(HotkeyListener(
            keys=normalized_keys,
            callback=callback
        ))

    def unhotkey(self, keys: str = None, callback: Callable = None) -> bool:
        """Remove a hotkey listener"""
        if keys is None and callback is None:
            self._hotkey_listeners = []
            return True

        if keys:
            key_parts = keys.upper().replace(' ', '').split('+')
            normalized_keys = set(self._normalize_key(part) for part in key_parts)

            original_len = len(self._hotkey_listeners)
            self._hotkey_listeners = [
                h for h in self._hotkey_listeners
                if h.keys != normalized_keys
            ]
            return len(self._hotkey_listeners) < original_len

        if callback:
            original_len = len(self._hotkey_listeners)
            self._hotkey_listeners = [
                h for h in self._hotkey_listeners
                if h.callback != callback
            ]
            return len(self._hotkey_listeners) < original_len

        return False

    def isPressed(self, key: str) -> bool:
        """Check if a key is currently pressed"""
        normalized = self._normalize_key(key)
        return normalized in self._pressed_keys

    def isHeld(self, key: str) -> bool:
        """Check if a key is being held down"""
        normalized = self._normalize_key(key)
        return self._key_states.get(normalized) in (KeyState.Pressed, KeyState.Held)

    def getState(self, key: str) -> KeyState:
        """Get the current state of a key"""
        normalized = self._normalize_key(key)
        return self._key_states.get(normalized, KeyState.Released)

    def getPressedKeys(self) -> Set[str]:
        """Get all currently pressed keys"""
        return self._pressed_keys.copy()

    def waitFor(self, key: str, timeout: float = None) -> bool:
        """Wait for a key to be pressed"""
        normalized = self._normalize_key(key)
        event = threading.Event()
        result = [False]

        def on_key():
            result[0] = True
            event.set()

        self.listen(normalized, on_key, once=True)
        event.wait(timeout=timeout)

        if not result[0]:
            self.unlisten(normalized, on_key)

        return result[0]

    def onGlobal(self, callback: Callable) -> None:
        """Register a global listener for all key events"""
        self._global_listeners.append(callback)

    def offGlobal(self, callback: Callable = None) -> bool:
        """Remove a global listener"""
        if callback is None:
            self._global_listeners = []
            return True
        else:
            try:
                self._global_listeners.remove(callback)
                return True
            except ValueError:
                return False

    def type(self, text: str, interval: float = 0.05) -> None:
        """Type text using the keyboard"""
        if PYNPUT_AVAILABLE:
            controller = pynput_keyboard.Controller()
            for char in text:
                controller.type(char)
                time.sleep(interval)
        else:
            print("[CsslKeyboard] Warning: pynput not available for typing")

    def press(self, key: str) -> None:
        """Simulate pressing a key"""
        if PYNPUT_AVAILABLE:
            controller = pynput_keyboard.Controller()
            normalized = self._normalize_key(key)

            # Map to pynput key
            if hasattr(Key, normalized):
                controller.press(getattr(Key, normalized))
            else:
                controller.press(normalized)
        else:
            print("[CsslKeyboard] Warning: pynput not available for key simulation")

    def release(self, key: str) -> None:
        """Simulate releasing a key"""
        if PYNPUT_AVAILABLE:
            controller = pynput_keyboard.Controller()
            normalized = self._normalize_key(key)

            # Map to pynput key
            if hasattr(Key, normalized):
                controller.release(getattr(Key, normalized))
            else:
                controller.release(normalized)
        else:
            print("[CsslKeyboard] Warning: pynput not available for key simulation")

    def tap(self, key: str) -> None:
        """Simulate tapping a key (press + release)"""
        self.press(key)
        self.release(key)

    def __call__(self, action: str, key: str = None, callback: Callable = None) -> Any:
        """Allow calling as keyboard('listen', 'KEY', callback)"""
        action = action.lower()

        if action == 'listen':
            if key and callback:
                self.listen(key, callback)
                return True
        elif action == 'unlisten':
            if key:
                return self.unlisten(key, callback)
        elif action == 'ispressed':
            if key:
                return self.isPressed(key)
        elif action == 'hotkey':
            if key and callback:
                self.hotkey(key, callback)
                return True
        elif action == 'type':
            if key:
                self.type(key)
                return True
        elif action == 'press':
            if key:
                self.press(key)
                return True
        elif action == 'release':
            if key:
                self.release(key)
                return True
        elif action == 'tap':
            if key:
                self.tap(key)
                return True
        elif action == 'wait':
            if key:
                return self.waitFor(key)

        return None

    def setRuntime(self, runtime: Any) -> None:
        """Set the CSSL runtime"""
        self._cssl_runtime = runtime

    def stop(self) -> None:
        """Stop the keyboard controller"""
        self._stop_listener()

    def start(self) -> None:
        """Start the keyboard controller"""
        self._start_listener()

    def isListening(self) -> bool:
        """Check if the keyboard controller is running"""
        return self._running

    def clearHotkeys(self) -> None:
        """Clear all hotkey listeners"""
        self._hotkey_listeners = []

    def clearListeners(self) -> None:
        """Clear all key listeners"""
        self._listeners = {}
        self._global_listeners = []


class CsslKeyboardModule:
    """The CSSL Keyboard module - returned by include("cssl-keyboard")"""

    def __init__(self):
        self._controller = CsslKeyboardController()

    def __call__(self, action: str, key: str = None, callback: Callable = None) -> Any:
        """Allow calling as keyboard('listen', 'KEY', callback)"""
        return self._controller(action, key, callback)

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to controller"""
        if name.startswith('_'):
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

        # Check if it's a method on the controller
        if hasattr(self._controller, name):
            return getattr(self._controller, name)

        # Check for key constants
        try:
            return CsslKey[name.upper()].value
        except KeyError:
            pass

        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

    # Expose key constants
    Key = CsslKey

    # Expose commonly used methods directly
    def listen(self, key: str, callback: Callable, once: bool = False) -> None:
        return self._controller.listen(key, callback, once)

    def unlisten(self, key: str, callback: Callable = None) -> bool:
        return self._controller.unlisten(key, callback)

    def hotkey(self, keys: str, callback: Callable) -> None:
        return self._controller.hotkey(keys, callback)

    def isPressed(self, key: str) -> bool:
        return self._controller.isPressed(key)

    def isHeld(self, key: str) -> bool:
        return self._controller.isHeld(key)

    def getState(self, key: str) -> KeyState:
        return self._controller.getState(key)

    def getPressedKeys(self) -> Set[str]:
        return self._controller.getPressedKeys()

    def waitFor(self, key: str, timeout: float = None) -> bool:
        return self._controller.waitFor(key, timeout)

    def type(self, text: str, interval: float = 0.05) -> None:
        return self._controller.type(text, interval)

    def press(self, key: str) -> None:
        return self._controller.press(key)

    def release(self, key: str) -> None:
        return self._controller.release(key)

    def tap(self, key: str) -> None:
        return self._controller.tap(key)

    def stop(self) -> None:
        return self._controller.stop()

    def start(self) -> None:
        return self._controller.start()

    def isListening(self) -> bool:
        return self._controller.isListening()

    def clearHotkeys(self) -> None:
        return self._controller.clearHotkeys()

    def clearListeners(self) -> None:
        return self._controller.clearListeners()


# Global module instance
_keyboard_module: Optional[CsslKeyboardModule] = None


def get_keyboard_module() -> CsslKeyboardModule:
    """Get the keyboard module instance"""
    global _keyboard_module
    if _keyboard_module is None:
        _keyboard_module = CsslKeyboardModule()
    return _keyboard_module


# Export classes for direct import
__all__ = [
    'CsslKey',
    'KeyState',
    'CsslKeyboardController',
    'CsslKeyboardModule',
    'get_keyboard_module',
]
