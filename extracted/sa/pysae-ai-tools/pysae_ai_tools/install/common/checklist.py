"""Cross-platform interactive checklist prompt.

Lets the user toggle items in a list with arrow keys + space + enter.
Items flagged ``locked=True`` are always selected and cannot be toggled
(used for REQUIRED tools).

Falls back to ``None`` (no prompt) when stdin is not a TTY — callers should
treat that as "use defaults" and avoid invoking the prompt in CI.
"""

import sys
from dataclasses import dataclass

import typer


@dataclass
class Item:
    name: str
    label: str = ""  # extra text shown in dim color (e.g. "REQUIRED")
    selected: bool = True
    locked: bool = False  # locked items are always selected and can't be toggled
    header_above: str = ""  # if set, a category header rendered just above this item
    is_new: bool = False  # if True, render a red bold "(NEW)" marker right after the name


_forced_non_interactive = False


def force_non_interactive(enabled: bool = True) -> None:
    """Silence every question for the rest of the run, even on a TTY.

    Set by the ``--non-interactive`` CLI flag. Two layers decide independently
    whether they may involve a human, and this is the single place that settles
    both — otherwise an unattended run would still be free to open a browser:

    - the checklist and the value prompts, via :func:`is_interactive` below;
    - the env resolvers that launch a human flow (browser OAuth,
      ``glab auth login``), via ``env.trace``.
    """
    global _forced_non_interactive
    _forced_non_interactive = enabled

    from ...env import trace

    trace.set_noninteractive(enabled)


def is_interactive() -> bool:
    """True only when both stdin and stdout are attached to a TTY — unless the
    run was forced non-interactive via :func:`force_non_interactive`."""
    if _forced_non_interactive:
        return False
    try:
        return sys.stdin.isatty() and sys.stdout.isatty()
    except (AttributeError, ValueError):
        return False


def _getch_unix() -> str:
    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":  # ANSI escape sequence (arrow keys)
            ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch


def _getch_windows() -> str:
    import msvcrt  # type: ignore[import-not-found,unused-ignore]

    ch: bytes = msvcrt.getch()  # type: ignore[attr-defined,unused-ignore]
    if ch in (b"\x00", b"\xe0"):  # arrow key prefix on Windows
        next_ch: bytes = msvcrt.getch()  # type: ignore[attr-defined,unused-ignore]
        return "\x1b[" + {b"H": "A", b"P": "B", b"M": "C", b"K": "D"}.get(next_ch, "")
    return ch.decode("utf-8", errors="ignore")


def _getch() -> str:
    if sys.platform == "win32":
        return _getch_windows()
    return _getch_unix()


def _line_count(items: list[Item]) -> int:
    """Count rendered lines: header (1) + hint (1) + blank (1) + per-item lines.

    An item with ``header_above`` adds two extra lines (blank + header).
    """
    extras = sum(2 for it in items if it.header_above)
    return 3 + len(items) + extras


def _render(items: list[Item], cursor: int, header: str) -> None:
    typer.echo(header)
    typer.secho(
        "  ↑/↓ : naviguer    espace : cocher/décocher    a : tout cocher    n : tout décocher    entrée : valider",
        fg=typer.colors.BRIGHT_BLACK,
    )
    typer.echo("")
    for i, item in enumerate(items):
        if item.header_above:
            typer.echo("")
            typer.secho(f"  {item.header_above}", fg=typer.colors.CYAN)
        pointer = "❯" if i == cursor else " "
        if item.locked:
            box = "[✓]"
            box_color = typer.colors.BRIGHT_BLACK
        elif item.selected:
            box = "[✓]"
            box_color = typer.colors.GREEN
        else:
            box = "[ ]"
            box_color = typer.colors.BRIGHT_BLACK
        typer.secho(f"  {pointer} ", nl=False, fg=typer.colors.CYAN)
        typer.secho(f"{box} ", nl=False, fg=box_color)
        typer.echo(item.name, nl=False)
        if item.label:
            typer.secho(f"  {item.label}", nl=False, fg=typer.colors.BRIGHT_BLACK)
        if item.is_new:
            typer.secho(" [NEW]", fg=typer.colors.RED, bold=True)
        else:
            typer.echo("")


def _clear_lines(n: int) -> None:
    """Move cursor up n lines and clear each one."""
    for _ in range(n):
        sys.stdout.write("\033[A\033[2K")
    sys.stdout.flush()


def prompt(items: list[Item], header: str) -> list[Item] | None:
    """Show an interactive checklist. Returns the items as toggled, or ``None``
    if the prompt cannot run (non-interactive terminal).
    """
    if not is_interactive() or not items:
        return None

    cursor = 0
    line_count = _line_count(items)
    first = True

    while True:
        if not first:
            _clear_lines(line_count)
        first = False
        _render(items, cursor, header)

        try:
            ch = _getch()
        except (OSError, KeyboardInterrupt):
            return None

        if ch in ("\r", "\n"):
            return items
        if ch == "\x03":  # Ctrl-C
            raise KeyboardInterrupt
        if ch in ("\x1b[A", "k"):  # up
            cursor = (cursor - 1) % len(items)
        elif ch in ("\x1b[B", "j"):  # down
            cursor = (cursor + 1) % len(items)
        elif ch == " ":
            if not items[cursor].locked:
                items[cursor].selected = not items[cursor].selected
        elif ch in ("a", "A"):
            for it in items:
                it.selected = True
        elif ch in ("n", "N"):
            for it in items:
                if not it.locked:
                    it.selected = False
