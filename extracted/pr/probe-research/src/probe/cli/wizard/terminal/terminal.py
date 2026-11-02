"""Terminal presentation for the wizard.

A wizard is a place you are IN, not a transcript you scroll. Every earlier
version redrew the state block and the menu below the previous one, so a few
actions left a screen of stale copies and you had to work out which block was
current. This module clears between steps so there is exactly one truth on
screen.

Kept separate from setup.py so the wizard's logic never has to think about
escape codes, and so all of it stays out of `probe log`'s import path.
"""

from __future__ import annotations
import shutil
import sys
from collections.abc import Callable, Sequence
from contextlib import contextmanager
from contextvars import ContextVar

#: Returned by a prompt when the user pressed Escape. Distinct from None, which
#: questionary already uses for Ctrl-C -- "go back one step" and "abandon the
#: whole wizard" are different intentions and must not collapse into each other.
BACK = object()
#: Decline this optional import and continue the surrounding flow.
SKIP = object()

#: Wide enough for the longest description, narrow enough to stay readable on a
#: full-screen terminal. Centering a block wider than this gains nothing.
CONTENT_WIDTH = 76

#: Minimum centring margin for legacy unsectioned prompts.
MARGIN = 3


def safe_margin(available: int) -> int:
    """Keep the whole UI clear of terminal chrome, yielding on short screens."""
    if available < 24:
        return min(1, max(0, (available - 1) // 2))
    # Warp's command bar can cover the first five rows. Tall terminals need
    # breathing room beyond that overlay; keep compact terminals unchanged.
    if available >= 64:
        return 8
    if available >= 48:
        return 7
    return min(5, max(0, available // 8))


_onboarding: ContextVar[Callable[[], Sequence[str]] | None] = ContextVar("onboarding", default=None)


@contextmanager
def onboarding(header: Callable[[], Sequence[str]]):
    """Carry the current install stage through nested import and result screens."""
    token = _onboarding.set(header)
    try:
        yield
    finally:
        _onboarding.reset(token)


def onboarding_header() -> list[str]:
    header = _onboarding.get()
    return list(header()) if header is not None else []


def interactive() -> bool:
    """Both ends must be a TTY: piped stdin with a TTY stdout is a script."""
    return sys.stdin.isatty() and sys.stdout.isatty()


class _Window:
    """The wizard's own screen. See `window`."""

    armed = False
    entered = False
    #: What the current screen said in plain text since it was drawn -- the
    #: lines `say()` printed and the body of a status `page()` -- so they can
    #: be printed again on the normal screen when the window closes over them.
    shown: list[str] = []
    #: Outputs `full_window` took the alternate-screen switch away from.
    #: prompt_toolkit hands every prompt in a process the SAME Output, so the
    #: patch outlives the prompt; it is taken off again when the window closes.
    patched: list = []


def _enter_window() -> None:
    """Switch to the alternate screen the first time a screen is drawn."""
    if _Window.armed and not _Window.entered:
        _Window.entered = True
        sys.stdout.write("\033[?1049h\033[H\033[2J")
        sys.stdout.flush()


def _new_screen() -> None:
    _Window.shown = []


@contextmanager
def window(enabled: bool = True):
    """Run the wizard in a window of its own, the way Claude Code or vim does.

    The terminal's ALTERNATE screen, entered once and left once. Inside it the
    wizard owns the whole window -- every screen is drawn full-size and anything
    taller than the window scrolls inside it, under the wizard's own keys -- and
    the shell's own screen and scrollback are left exactly as they were.
    Drawn inline instead, a block-based terminal such as Warp treated the
    wizard as ordinary command output: its arrow keys scrolled Warp's own
    blocks rather than reaching the menu.

    Entered LAZILY, by the first screen drawn (`clear`, a board, a prompt), so
    a run that never draws one -- a usage error, the headless refusal, the
    bootstrap note -- prints on the normal screen as any command would.

    Leaving puts back the normal screen, and then prints again what the last
    screen said in plain text (`say` lines, a status page's body): an error or
    a result shown right before the wizard exits would otherwise vanish with
    the window. A traceback needs no help -- the exception passes through here
    first, so it prints after the window has closed.

    Only for a real terminal on stdout: a test that fakes `interactive()` over
    a captured stream must not receive screen-switching escapes.
    """
    if not enabled or _Window.armed or not (sys.stdout.isatty() and sys.stdin.isatty()):
        yield
        return
    _Window.armed, _Window.entered = True, False
    _new_screen()
    try:
        yield
    finally:
        entered, shown = _Window.entered, list(_Window.shown)
        _Window.armed = _Window.entered = False
        _new_screen()
        for output in _Window.patched:
            vars(output).pop("enter_alternate_screen", None)
            vars(output).pop("quit_alternate_screen", None)
        _Window.patched = []
        if entered:
            sys.stdout.write("\033[?25h\033[?1049l")
            sys.stdout.flush()
            for line in shown:
                print(line)


def leave_window() -> None:
    """Put the shell's own screen back NOW, cursor shown: this process is about
    to be replaced (`os.execve`, the Update's hand-off to the newest release),
    and nothing after this line runs to close the window. Should the exec
    fail, the next screen drawn opens the window again."""
    try:
        if _Window.entered:
            sys.stdout.write("\033[?25h\033[?1049l")
            sys.stdout.flush()
            _Window.entered = False
    except Exception:  # noqa: BLE001 - a screen is never worth failing the hand-off over
        pass


def columns() -> int:
    try:
        return shutil.get_terminal_size().columns
    except OSError:
        return 80


def left_pad() -> int:
    """Spaces needed to centre a CONTENT_WIDTH block in this terminal.

    Zero on a narrow terminal: padding something that already does not fit only
    makes it wrap, which is worse than being left-aligned.
    """
    slack = columns() - CONTENT_WIDTH
    return max(0, slack // 2)


def clear() -> None:
    """Wipe the screen and park the cursor at the top.

    Only when interactive -- doing this to a pipe or a CI log would emit escape
    codes into captured output, and there is no screen to clear anyway.
    """
    if not interactive():
        return
    if _Window.armed:
        # Inside the wizard's window there is no scrollback to protect the
        # reader from, and the shell's own belongs to the shell: wipe the
        # window only.
        _enter_window()
        _new_screen()
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        return
    # \033[3J also drops the scrollback, so the previous step cannot be
    # recovered by scrolling. That is deliberate: the wizard is showing live
    # state, and a stale copy of it further up is a lie waiting to be read.
    sys.stdout.write("\033[3J\033[2J\033[H")
    sys.stdout.flush()


def final(text: str, *, file=None) -> None:
    """Output a run ends on: centred on the wizard's screen when there is one
    (and so printed again when the window closes), plain otherwise -- a
    one-shot `--action diagnose` report stays copyable, unindented."""
    if _Window.entered:
        say(text)
    else:
        print(text, file=file)


def say(text: str = "") -> None:
    """Print centred -- but only when there is a screen to centre in.

    Piped output stays flush-left: an indent there is noise every log grep has
    to strip, and the one consumer that never sees the layout is CI.
    """
    if _Window.entered:
        _Window.shown.extend(text.splitlines() or [""])
    if not text:
        print()
    elif interactive():
        print(indent(text))
    else:
        print(text)


def rows() -> int:
    try:
        return shutil.get_terminal_size().lines
    except OSError:
        return 24
from probe.cli.wizard.terminal.forms import text  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.layout import indent  # noqa: E402 -- pieces need each other; the front door loads this one first
