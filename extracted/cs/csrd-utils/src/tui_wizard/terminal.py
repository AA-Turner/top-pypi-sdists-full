"""Low-level terminal helpers: cbreak mode, character reading, escape sequences."""

import os
import select
import sys
from collections.abc import Iterator
from contextlib import contextmanager


def is_tty() -> bool:
    """Return ``True`` when both stdin and stdout are connected to a TTY.

    Set the environment variable ``CSRD_NO_TTY=1`` to force non-TTY
    (numbered-fallback) mode even when running in a real terminal.
    This is useful for manual testing of the non-interactive code paths.
    """

    if os.environ.get("CSRD_NO_TTY", "").strip() in {"1", "true", "yes"}:
        return False
    return sys.stdin.isatty() and sys.stdout.isatty()


@contextmanager
def cbreak_mode() -> Iterator[int | None]:
    """Context manager that sets the terminal to cbreak mode and restores on exit.

    Yields the file descriptor on success, or ``None`` when raw terminal
    controls are unavailable (e.g. on Windows without termios).
    """

    try:
        import termios
        import tty
    except Exception:
        yield None
        return

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        sys.stdout.write("\x1b[?25l")  # hide cursor
        sys.stdout.flush()
        yield fd
    finally:
        sys.stdout.write("\x1b[?25h")  # restore cursor
        sys.stdout.flush()
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def read_char(fd: int) -> str:
    """Read a single byte from *fd* using unbuffered :func:`os.read`.

    This avoids the Python buffered-IO vs ``select`` race where
    ``sys.stdin.read(1)`` consumes multiple bytes into its internal
    buffer, causing ``select.select`` to see an empty fd even though
    characters are available.
    """

    return os.read(fd, 1).decode("latin-1")


def read_escape_seq(fd: int) -> str:
    """After reading ``\\x1b``, distinguish standalone Escape from arrow keys.

    Uses ``select`` with a 50 ms timeout on the raw *fd*: if more bytes
    arrive they form an arrow-key sequence (``[A``/``[B``); otherwise the
    keypress was a bare Escape.

    Returns ``"ESC"`` for standalone Escape, ``"UP"`` / ``"DOWN"`` for
    arrows, or ``""`` for unrecognised sequences.
    """

    ready, _, _ = select.select([fd], [], [], 0.05)
    if not ready:
        return "ESC"

    ch = read_char(fd)
    if ch != "[":
        return ""  # unknown sequence

    code = read_char(fd)
    if code == "A":
        return "UP"
    if code == "B":
        return "DOWN"
    return ""
