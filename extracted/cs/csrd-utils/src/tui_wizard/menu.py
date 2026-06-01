"""Top-level menu runner and rendering helpers."""

import sys
from contextlib import suppress

from .models import MenuItem, filter_visible, resolve_disabled
from .terminal import cbreak_mode, is_tty, read_char, read_escape_seq


def _is_enabled(item: MenuItem) -> bool:
    """Return True if the item is selectable."""
    return not resolve_disabled(item)


def _next_enabled(items: list[MenuItem], cursor: int, direction: int) -> int:
    """Find the next enabled item index in the given direction, wrapping around."""
    n = len(items)
    for _ in range(n):
        cursor = (cursor + direction) % n
        if _is_enabled(items[cursor]):
            return cursor
    return cursor  # all disabled — stay put


def run_menu(title: str, prompt: str, items: list[MenuItem]) -> int:
    """Present *items* interactively and execute the selected handler.

    Handles TTY detection, cbreak mode, arrow-key navigation, and
    non-TTY numbered fallback.  Returns the exit code from the chosen
    handler (or ``0`` on cancel / ``1`` on interrupt).
    """

    if not items:
        return 0

    # --- non-TTY path ---
    if not is_tty():
        print_basic_menu(title, prompt, items)
        try:
            while True:
                selected = resolve_non_tty_selection(input("Select [1]: "), items)
                if selected is not None:
                    if not _is_enabled(selected):
                        hint = resolve_disabled(selected)
                        print(f"ERROR: '{selected.label}' is unavailable ({hint}).")
                        continue
                    return selected.handler()
                print(f"ERROR: Invalid selection. Enter 1-{len(items)} or a valid alias.")
        except EOFError:
            return 0
        except KeyboardInterrupt:
            with suppress(KeyboardInterrupt):
                print("\nCancelled.")
            return 1

    # --- TTY path ---
    try:
        import termios  # noqa: F401 — availability check only
    except Exception:
        print_basic_menu(title, prompt, items)
        return 0

    with cbreak_mode() as fd:
        if fd is None:
            print_basic_menu(title, prompt, items)
            return 0

        # Start cursor on first enabled item
        cursor = 0
        if not _is_enabled(items[cursor]):
            cursor = _next_enabled(items, cursor, 1)
        try:
            render_tty_menu(title, prompt, items, cursor)
            while True:
                ch = read_char(fd)
                if ch in {"\r", "\n"}:
                    break
                if ch == "\x03":
                    raise KeyboardInterrupt
                if ch == "\x1b":
                    seq = read_escape_seq(fd)
                    if seq == "ESC":
                        sys.stdout.write("\x1b[2J\x1b[H")
                        sys.stdout.flush()
                        print("Cancelled.")
                        return 0
                    if seq == "UP":
                        cursor = _next_enabled(items, cursor, -1)
                        render_tty_menu(title, prompt, items, cursor)
                    elif seq == "DOWN":
                        cursor = _next_enabled(items, cursor, 1)
                        render_tty_menu(title, prompt, items, cursor)
        except KeyboardInterrupt:
            with suppress(KeyboardInterrupt):
                print("\nCancelled.")
            return 1

    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()
    return items[cursor].handler()


def print_basic_menu(title: str, prompt: str, items: list[MenuItem]) -> None:
    """Render a numbered menu for non-TTY contexts."""

    print(title)
    print()
    print(prompt)
    for idx, item in enumerate(items, start=1):
        hint = resolve_disabled(item)
        if hint:
            print(f"  {idx}) {item.label}  ({hint})")
        else:
            print(f"  {idx}) {item.label}")


def render_tty_menu(title: str, prompt: str, items: list[MenuItem], selected: int) -> None:
    """Render menu in TTY mode with the currently selected index highlighted."""

    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.write(f"{title}\r\n\r\n")
    sys.stdout.write(f"{prompt}\r\n")
    sys.stdout.write("(↑/↓ move, Enter confirm, Esc cancel)\r\n\r\n")
    for idx, item in enumerate(items):
        hint = resolve_disabled(item)
        marker = ">" if idx == selected else " "
        if hint:
            # dim/grey: \x1b[2m ... \x1b[0m
            sys.stdout.write(f" {marker} \x1b[2m{item.label}  ({hint})\x1b[0m\r\n")
        else:
            sys.stdout.write(f" {marker} {item.label}\r\n")
    sys.stdout.flush()


def resolve_non_tty_selection(raw: str, items: list[MenuItem]) -> MenuItem | None:
    """Resolve user input from non-TTY mode into a menu item selection."""

    value = raw.strip().lower()
    if value == "":
        return items[0]

    if value.isdigit():
        index = int(value) - 1
        if 0 <= index < len(items):
            return items[index]

    for item in items:
        if value in item.aliases:
            return item
    return None


__all__ = [
    "filter_visible",
    "print_basic_menu",
    "render_tty_menu",
    "resolve_non_tty_selection",
    "run_menu",
]
