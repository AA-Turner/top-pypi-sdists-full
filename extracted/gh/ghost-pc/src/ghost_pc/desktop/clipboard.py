"""Clipboard integration using Win32 API via ctypes.

Provides read/write access to the system clipboard for text content.
No external dependencies required.
"""

from __future__ import annotations

import logging
import sys

logger = logging.getLogger(__name__)

# Win32 constants
_CF_UNICODETEXT = 13
_GMEM_MOVEABLE = 0x0002


def get_clipboard_text() -> str | None:
    """Read text from the system clipboard.

    Returns None if clipboard is empty or contains non-text data.
    """
    if sys.platform != "win32":
        logger.debug("Clipboard requires Windows")
        return None

    import ctypes

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    if not user32.OpenClipboard(None):
        logger.warning("Could not open clipboard")
        return None

    try:
        handle = user32.GetClipboardData(_CF_UNICODETEXT)
        if not handle:
            return None

        ptr = kernel32.GlobalLock(handle)
        if not ptr:
            return None

        try:
            text = ctypes.wstring_at(ptr)
            return text
        finally:
            kernel32.GlobalUnlock(handle)
    finally:
        user32.CloseClipboard()


def set_clipboard_text(text: str) -> bool:
    """Write text to the system clipboard.

    Returns True if successful.
    """
    if sys.platform != "win32":
        logger.debug("Clipboard requires Windows")
        return False

    import ctypes

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    if not user32.OpenClipboard(None):
        logger.warning("Could not open clipboard")
        return False

    try:
        user32.EmptyClipboard()

        # Allocate global memory for the text
        encoded = text.encode("utf-16-le") + b"\x00\x00"
        h_mem = kernel32.GlobalAlloc(_GMEM_MOVEABLE, len(encoded))
        if not h_mem:
            return False

        ptr = kernel32.GlobalLock(h_mem)
        if not ptr:
            kernel32.GlobalFree(h_mem)
            return False

        ctypes.memmove(ptr, encoded, len(encoded))
        kernel32.GlobalUnlock(h_mem)

        user32.SetClipboardData(_CF_UNICODETEXT, h_mem)
        return True
    finally:
        user32.CloseClipboard()
