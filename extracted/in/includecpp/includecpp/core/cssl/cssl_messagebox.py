"""
CSSL MessageBox Module - Simple message dialogs for CSSL
Version 4.9.7

Usage in CSSL:
    messagebox = include("cssl-gui.MessageBox");

    // Simple usage - show() waits by default
    msg = new messagebox(ok_btn=true);
    msg.setTitle("My Title");
    msg.setText("Hello World!");
    msg.show();  // Blocks until user clicks OK

    // Non-blocking usage
    msg.show(wait=false);  // Returns immediately
    // ... do other things ...
    msg.wait();  // Wait for dialog to close later

    // Convenience functions
    messagebox.showInfo("Title", "Message");
    messagebox.showWarning("Title", "Warning!");
    messagebox.showError("Title", "Error!");
    result = messagebox.askYesNo("Title", "Are you sure?");
    result = messagebox.askOkCancel("Title", "Continue?");
"""

import tkinter as tk
from tkinter import ttk
import threading
import os
import platform
from typing import Any, Callable, Dict, List, Optional

# Sound support
if platform.system() == 'Windows':
    import winsound
    SOUND_AVAILABLE = True
else:
    SOUND_AVAILABLE = False


def _strip_ansi(text: str) -> str:
    """Strip ANSI escape sequences (fmt:: formatting) from text"""
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', str(text))


def _extract_ansi_color(text: str) -> Optional[str]:
    """Extract color from ANSI escape sequence and return tkinter color"""
    import re
    # ANSI color codes to tkinter colors
    ansi_to_color = {
        '30': '#000000',  # black
        '31': '#ff0000',  # red
        '32': '#00ff00',  # green
        '33': '#ffff00',  # yellow
        '34': '#0000ff',  # blue
        '35': '#ff00ff',  # magenta
        '36': '#00ffff',  # cyan
        '37': '#ffffff',  # white
        '90': '#808080',  # bright black (gray)
        '91': '#ff5555',  # bright red
        '92': '#55ff55',  # bright green
        '93': '#ffff55',  # bright yellow
        '94': '#5555ff',  # bright blue
        '95': '#ff55ff',  # bright magenta
        '96': '#55ffff',  # bright cyan
        '97': '#ffffff',  # bright white
    }
    # Match ANSI color code like \x1b[32m
    match = re.search(r'\x1B\[(\d+)m', str(text))
    if match:
        code = match.group(1)
        return ansi_to_color.get(code)
    return None


class MessageBoxButton:
    """A button in a MessageBox"""

    def __init__(self, parent: 'CsslMessageBox', text: str = "OK", is_default: bool = False):
        self._parent = parent
        self._text = text
        self._is_default = is_default
        self._callback: Optional[Callable] = None
        self._tk_button: Optional[tk.Button] = None
        self._visible = True
        self._color: Optional[str] = None

    def setText(self, text: str) -> 'MessageBoxButton':
        """Set button text (supports fmt:: colors)"""
        # Extract color before stripping ANSI codes
        color = _extract_ansi_color(text)
        clean_text = _strip_ansi(text)
        self._text = clean_text
        self._color = color
        if self._tk_button:
            self._tk_button.configure(text=clean_text)
            # Apply color if detected (need tk.Button, not ttk.Button for foreground)
        return self

    def setTextColor(self, color: str) -> 'MessageBoxButton':
        """Set button text color"""
        self._color = color
        return self

    def getText(self) -> str:
        """Get button text"""
        return self._text

    def onClick(self, callback: Callable) -> 'MessageBoxButton':
        """Set click callback"""
        self._callback = callback
        return self

    def on_click(self, callback: Callable) -> 'MessageBoxButton':
        """Alias for onClick"""
        return self.onClick(callback)

    def _handle_click(self) -> None:
        """Internal click handler"""
        # Set result to button text before calling callback
        self._parent._result = self._text

        if self._callback:
            try:
                self._callback()
            except Exception as e:
                print(f"[MessageBox] Button callback error: {e}")
        else:
            # Default: close the message box
            self._parent.close()

    def show(self) -> 'MessageBoxButton':
        """Show the button"""
        self._visible = True
        if self._tk_button:
            self._tk_button.pack(side=tk.LEFT, padx=5)
        return self

    def hide(self) -> 'MessageBoxButton':
        """Hide the button"""
        self._visible = False
        if self._tk_button:
            self._tk_button.pack_forget()
        return self

    def _create(self, parent_frame: tk.Frame) -> None:
        """Create the tkinter button"""
        # Use tk.Button (not ttk) to support foreground color
        self._tk_button = tk.Button(
            parent_frame,
            text=self._text,
            command=self._handle_click,
            padx=15,
            pady=5
        )
        # Apply color if set (from fmt:: formatting)
        if self._color:
            self._tk_button.configure(fg=self._color)
        if self._visible:
            self._tk_button.pack(side=tk.LEFT, padx=5)


class CsslMessageBox:
    """
    CSSL MessageBox - Simple message dialog

    Usage:
        msg = new CsslMessageBox(ok_btn=true, cancel_btn=true);
        msg.setTitle("Title");
        msg.setText("Message");
        msg.ok_btn.setText("Accept");
        msg.show();
    """

    def __init__(self, ok_btn: bool = True, cancel_btn: bool = False,
                 yes_btn: bool = False, no_btn: bool = False,
                 custom_btns: List[str] = None):
        self._title = "Message"
        self._text = ""
        self._width = 350
        self._height = 150
        self._running = False
        self._result: Optional[str] = None
        self._sound_path: Optional[str] = None
        self._bg_color = "#2d2d2d"
        self._fg_color = "#ffffff"
        self._window: Optional[tk.Tk] = None
        self._text_label: Optional[tk.Label] = None

        # Create buttons based on parameters
        self._buttons: Dict[str, MessageBoxButton] = {}

        if ok_btn:
            self._buttons['ok_btn'] = MessageBoxButton(self, "OK", is_default=True)
            self.ok_btn = self._buttons['ok_btn']

        if cancel_btn:
            self._buttons['cancel_btn'] = MessageBoxButton(self, "Cancel")
            self.cancel_btn = self._buttons['cancel_btn']

        if yes_btn:
            self._buttons['yes_btn'] = MessageBoxButton(self, "Yes", is_default=True)
            self.yes_btn = self._buttons['yes_btn']

        if no_btn:
            self._buttons['no_btn'] = MessageBoxButton(self, "No")
            self.no_btn = self._buttons['no_btn']

        if custom_btns:
            for i, btn_text in enumerate(custom_btns):
                btn_name = f'btn_{i}'
                self._buttons[btn_name] = MessageBoxButton(self, btn_text)
                setattr(self, btn_name, self._buttons[btn_name])

    def setTitle(self, title: str) -> 'CsslMessageBox':
        """Set the message box title"""
        self._title = title
        if self._window:
            self._window.title(title)
        return self

    def setText(self, text: str) -> 'CsslMessageBox':
        """Set the message text (supports fmt:: formatting)"""
        # Strip ANSI/fmt codes for display (tkinter doesn't support them)
        clean_text = self._strip_formatting(text)
        self._text = clean_text
        if self._text_label:
            self._text_label.configure(text=clean_text)
        return self

    def _strip_formatting(self, text: str) -> str:
        """Strip fmt:: formatting codes (ANSI escape sequences)"""
        import re
        # Remove ANSI escape sequences
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', str(text))

    def setSize(self, width: int, height: int) -> 'CsslMessageBox':
        """Set the message box size"""
        self._width = width
        self._height = height
        if self._window:
            self._window.geometry(f"{width}x{height}")
        return self

    def setBackgroundColor(self, color: str) -> 'CsslMessageBox':
        """Set background color"""
        self._bg_color = color
        return self

    def setTextColor(self, color: str) -> 'CsslMessageBox':
        """Set text color"""
        self._fg_color = color
        return self

    def playSound(self, path: str) -> 'CsslMessageBox':
        """Set sound to play when message box appears"""
        self._sound_path = path
        return self

    def _play_sound(self) -> None:
        """Play the configured sound"""
        if not self._sound_path or not SOUND_AVAILABLE:
            return

        if not os.path.exists(self._sound_path):
            return

        def _do_play():
            try:
                if self._sound_path.lower().endswith('.wav'):
                    winsound.PlaySound(self._sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except:
                pass

        threading.Thread(target=_do_play, daemon=True).start()

    def addButton(self, text: str, callback: Callable = None) -> MessageBoxButton:
        """Add a custom button"""
        btn_name = f'btn_{len(self._buttons)}'
        btn = MessageBoxButton(self, text)
        if callback:
            btn.onClick(callback)
        self._buttons[btn_name] = btn
        setattr(self, btn_name, btn)
        return btn

    def show(self, wait: bool = True) -> 'CsslMessageBox':
        """Show the message box

        Args:
            wait: If True (default), blocks until the dialog is closed.
                  If False, returns immediately (use wait() later).
        """
        self._create_window()
        self._running = True

        # Play sound if configured
        if self._sound_path:
            self._play_sound()

        # By default, wait for user to close the dialog
        if wait:
            self.wait()

        return self

    def _create_window(self) -> None:
        """Create the tkinter window"""
        # Create as a standalone Tk window (simpler, more reliable)
        self._window = tk.Tk()
        self._window.title(self._title)
        self._window.configure(bg=self._bg_color)
        self._window.resizable(False, False)
        self._window.protocol("WM_DELETE_WINDOW", self._on_close)

        # Center on screen
        screen_width = self._window.winfo_screenwidth()
        screen_height = self._window.winfo_screenheight()
        x = (screen_width // 2) - (self._width // 2)
        y = (screen_height // 2) - (self._height // 2)
        self._window.geometry(f"{self._width}x{self._height}+{x}+{y}")

        # Make it stay on top
        self._window.attributes('-topmost', True)
        self._window.focus_force()

        # Create content frame
        content_frame = tk.Frame(self._window, bg=self._bg_color)
        content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=15)

        # Text label
        self._text_label = tk.Label(
            content_frame,
            text=self._text,
            bg=self._bg_color,
            fg=self._fg_color,
            font=("Arial", 11),
            wraplength=self._width - 50,
            justify=tk.LEFT
        )
        self._text_label.pack(expand=True, fill=tk.BOTH)

        # Button frame
        button_frame = tk.Frame(self._window, bg=self._bg_color)
        button_frame.pack(side=tk.BOTTOM, pady=15)

        # Create buttons
        for btn in self._buttons.values():
            btn._create(button_frame)

    def _on_close(self) -> None:
        """Handle window close"""
        self._running = False
        if self._result is None:
            self._result = "closed"
        if self._window:
            try:
                self._window.grab_release()
                self._window.destroy()
            except tk.TclError:
                pass
            self._window = None

    def close(self) -> None:
        """Close the message box"""
        self._on_close()

    def hide(self) -> 'CsslMessageBox':
        """Hide the message box (can be shown again)"""
        if self._window:
            self._window.withdraw()
        return self

    def isRunning(self) -> bool:
        """Check if the message box is still open"""
        return self._running

    def getResult(self) -> Optional[str]:
        """Get the result (which button was clicked)"""
        return self._result

    def wait(self, timeout_ms: int = None) -> Optional[str]:
        """Wait for the message box to close and return result

        Args:
            timeout_ms: If provided, only wait this many milliseconds then return.
                        If None (default), blocks until dialog closes.
        """
        import time

        if timeout_ms is not None:
            # Non-blocking wait with timeout - just process events once
            if self._window and self._running:
                try:
                    self._window.update()
                    if self._window:  # Check again after update
                        self._window.update_idletasks()
                except tk.TclError:
                    self._running = False
        else:
            # Blocking wait - manually pump events until window closes
            while self._running and self._window:
                try:
                    self._window.update()
                    if not self._window or not self._running:
                        break
                    self._window.update_idletasks()
                    time.sleep(0.01)  # Prevent CPU spinning
                except tk.TclError:
                    self._running = False
                    break

        return self._result

    def mainloop(self) -> None:
        """Run the message box event loop (alias for wait())"""
        self.wait()

    def update(self) -> None:
        """Process pending events"""
        if self._window:
            try:
                self._window.update()
            except tk.TclError:
                self._running = False


# Convenience functions
def showInfo(title: str, message: str) -> None:
    """Show an info message box"""
    msg = CsslMessageBox(ok_btn=True)
    msg.setTitle(title)
    msg.setText(message)
    msg.show()  # wait=True by default


def showWarning(title: str, message: str) -> None:
    """Show a warning message box"""
    msg = CsslMessageBox(ok_btn=True)
    msg.setTitle(title)
    msg.setText(message)
    msg.setBackgroundColor("#4a3c00")
    msg.show()  # wait=True by default


def showError(title: str, message: str) -> None:
    """Show an error message box"""
    msg = CsslMessageBox(ok_btn=True)
    msg.setTitle(title)
    msg.setText(message)
    msg.setBackgroundColor("#4a0000")
    msg.show()  # wait=True by default


def askYesNo(title: str, message: str) -> bool:
    """Show a yes/no question and return True for Yes"""
    result = [None]

    def on_yes():
        result[0] = True
        msg.close()

    def on_no():
        result[0] = False
        msg.close()

    msg = CsslMessageBox(yes_btn=True, no_btn=True)
    msg.setTitle(title)
    msg.setText(message)
    msg.yes_btn.onClick(on_yes)
    msg.no_btn.onClick(on_no)
    msg.show()  # wait=True by default

    return result[0] if result[0] is not None else False


def askOkCancel(title: str, message: str) -> bool:
    """Show an OK/Cancel question and return True for OK"""
    result = [None]

    def on_ok():
        result[0] = True
        msg.close()

    def on_cancel():
        result[0] = False
        msg.close()

    msg = CsslMessageBox(ok_btn=True, cancel_btn=True)
    msg.setTitle(title)
    msg.setText(message)
    msg.ok_btn.onClick(on_ok)
    msg.cancel_btn.onClick(on_cancel)
    msg.show()  # wait=True by default

    return result[0] if result[0] is not None else False


class CsslMessageBoxModule:
    """Module returned by include("cssl-gui.MessageBox")"""

    # The main class
    MessageBox = CsslMessageBox

    # Convenience functions
    showInfo = staticmethod(showInfo)
    showWarning = staticmethod(showWarning)
    showError = staticmethod(showError)
    askYesNo = staticmethod(askYesNo)
    askOkCancel = staticmethod(askOkCancel)

    def __new__(cls, *args, **kwargs):
        """Allow: msg = new messagebox(ok_btn=true)"""
        return CsslMessageBox(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        pass


# Global module instance
_messagebox_module = None


def get_messagebox_module():
    """Get the MessageBox module"""
    global _messagebox_module
    if _messagebox_module is None:
        _messagebox_module = CsslMessageBoxModule
    return _messagebox_module


__all__ = [
    'CsslMessageBox',
    'MessageBoxButton',
    'CsslMessageBoxModule',
    'get_messagebox_module',
    'showInfo',
    'showWarning',
    'showError',
    'askYesNo',
    'askOkCancel',
]
