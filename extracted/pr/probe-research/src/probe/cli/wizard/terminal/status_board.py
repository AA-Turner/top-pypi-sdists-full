"""live status while work blocks the next screen: one spinner line (working) or N concurrent rows (Board)."""

from __future__ import annotations
import sys
from collections.abc import Sequence
from contextlib import contextmanager


class Board:
    """N live rows on ONE centred screen, for agents running concurrently.

    Three import units each repainting `\\r` on "the" status line is not a
    display, it is three programs fighting over one row: whichever ticked last
    wins, the other two are invisible, and the count on screen belongs to
    whichever unit happened to interrupt. What it looked like was a backfill
    that kept restarting its progress.

    Each row is addressed ABSOLUTELY (`\\033[<row>;1H`), so a row only ever
    moves when its own agent has something to say and the others are untouched.
    That needs the screen to hold still underneath, which is why `open()` clears
    it and nothing else may print until `close()`.

    Non-interactive output gets no board at all -- see `rows_for`, which hands
    back None so the caller keeps its plain one-line-per-event logging. Absolute
    cursor addressing into a pipe is escape codes in a CI log.
    """

    def __init__(self, title: str, labels: Sequence[str], out=None) -> None:
        import threading

        self._labels = list(labels)
        self._out = out if out is not None else sys.stdout
        self._lock = threading.Lock()
        self._pad = left_pad()
        self._line_width = max(1, min(CONTENT_WIDTH, columns() - self._pad - 1))
        self._heading = [
            row for line in title.splitlines() for row in wrap(line, self._line_width)
        ] or [""]
        # Keep the heading aligned with the content on the surrounding pages.
        self._progress = [part for line in onboarding_header() for part in wrap(line, self._line_width)]
        self._margin = safe_margin(rows())
        self._last = max(1, rows() - self._margin)
        self._progress = self._progress[:max(0, rows() - 2 * self._margin - 4)]
        self._first = self._margin + 1 + (len(self._progress) + 1 if self._progress else 0)
        self._heading = self._heading[:max(1, self._last - self._first - 2)]
        self._first_row = self._first + len(self._heading) + 1
        self._visible_count = max(0, min(len(self._labels), self._last - self._first_row))
        self._hidden_count = len(self._labels) - self._visible_count
        self._width = max((len(x) for x in self._labels), default=0)

    def open(self) -> None:
        # Callers only open boards for live output. Clear that SAME stream:
        # clear() writes to global stdout, which may belong to another screen.
        pad = " " * self._pad
        heading = "".join(
            f"\033[{self._first + index};1H{pad}{line}"
            for index, line in enumerate(self._heading)
        )
        progress = "".join(
            f"\033[{self._margin + index + 1};1H{pad}{line}"
            for index, line in enumerate(self._progress)
        )
        overflow = (f"\033[{self._last};1H{pad}… {self._hidden_count} more imports"
                    if self._hidden_count else "")
        _enter_window()
        _new_screen()
        wipe = "\033[2J\033[H" if _Window.armed else "\033[3J\033[2J\033[H"
        self._out.write("\033[?25l" + wipe + progress + heading + overflow)
        self._out.flush()

    def update(self, index: int, text: str) -> None:
        """Repaint one row. Safe from any thread.

        The lock is NOT what makes that true today, and the docstring says so
        rather than implying a guarantee nothing verifies: each call is a single
        `write()` of one fully-formed string, which the GIL already serialises.
        Removing the lock passes every test here -- checked, not assumed.

        It stays because the atomicity is a property of this method being ONE
        write, which is not a property anyone editing it would think to
        preserve. The moment a row is painted in two writes -- a colour, a
        second line -- the interleaving is real and the lock is what stops it.
        """
        if not 0 <= index < self._visible_count:
            return
        row = self._first_row + index
        line = f"{self._labels[index]:<{self._width}}{text}"
        if len(line) > self._line_width:
            line = line[: self._line_width - 1] + "…"
        with self._lock:
            self._out.write(f"\033[{row};1H\033[2K" + " " * self._pad + line)
            self._out.flush()

    def row(self, index: int):
        """A one-argument painter for row `index`, for `launch_agent(paint_to=)`."""
        return lambda text: self.update(index, text)

    def close(self, *, erase: bool = False) -> None:
        """Park below the board, optionally erasing its temporary status rows."""
        with self._lock:
            cleanup = "".join(
                f"\033[{self._first_row + index};1H\033[2K"
                for index in range(self._visible_count + bool(self._hidden_count))
            ) if erase else ""
            cursor_row = min(self._last, self._first_row + self._visible_count)
            self._out.write(cleanup + f"\033[{cursor_row};1H\033[?25h")
            self._out.flush()


class Status:
    """What a `working()` line shows, changeable while it spins: its label,
    and once a caller knows how far along the work is, a bar with its
    percentage on the row under it. Read by the spinner's thread; each field
    is replaced whole, never mutated in place."""

    def __init__(self, label: str) -> None:
        self.label = label
        self.fraction: float | None = None

    def set(self, *, label: str | None = None, fraction: float | None = None) -> None:
        if label is not None:
            self.label = label
        if fraction is not None:
            # Never backwards: a total that grows mid-run must not undo
            # progress already shown.
            self.fraction = max(self.fraction or 0.0, max(0.0, min(1.0, fraction)))


#: The `working()` line on screen now, if any: a `working()` inside it keeps
#: it (one spinner per screen; two threads painting fight over the rows).
_active_status: Status | None = None


@contextmanager
def working(label: str):
    """One centered, animated status line for work that blocks the next screen.

    `Progress` is for a PHASE with named steps; this is for the anonymous
    waits between screens -- collecting device state, upgrading the CLI --
    where the alternative is a terminal that sits frozen after a keypress and
    reads as a hang. Measured before this existed: picking a menu action cost
    ~0.85s of dead air per detected coding agent, in silence.

    Non-interactive gets NOTHING -- not even a static line. `\\r` repaints into
    a pipe are log garbage, and the piped caller already gets its evidence
    from the step output itself. Same split `Progress` documents.

    Every failure path degrades to doing nothing: a spinner that cannot start
    (thread limits, closed stdout) must never take the actual work down with
    it, so the body runs whether or not anything animates.

    Yields its `Status`: `status.set(fraction=...)` adds the bar and its
    percentage under the line. Inside another `working()`, yields that one's
    and changes nothing on screen.
    """
    global _active_status
    if _active_status is not None:
        yield _active_status
        return
    status = Status(label)
    if not interactive():
        yield status
        return
    import itertools
    import threading

    frames = itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
    stop = threading.Event()
    header = onboarding_header()
    output = sys.stdout
    size = None
    status_row = 1

    def centred(text: str, width: int) -> str:
        room = max(1, min(CONTENT_WIDTH, width - 1))
        if len(text) > room:
            text = text[:room - 1] + "…"
        return " " * max(0, (width - len(text)) // 2) + text

    def paint() -> None:
        nonlocal size, status_row
        height, width = max(1, rows()), max(1, columns())
        margin = safe_margin(height)
        pinned = header_lines(header)[:max(0, height - 2 * margin - 2)]
        first = margin + len(pinned) + (1 if pinned else 0)
        last = max(first, height - margin - 1)
        status_row = (first + last) // 2 + 1
        line = centred(f"{next(frames)} {' '.join(status.label.split())}", width)
        fraction = status.fraction
        # The bar's row, blank until the work says how far along it is.
        under = "" if fraction is None else centred(progress_line(fraction), width)
        prefix = ""
        if size != (height, width):
            # A resize must erase the old centered row, not leave a second
            # copy behind. The onboarding header keeps its shared top margin.
            # Inside the wizard's window the spinner is a screen like any
            # other: it opens the window, and wipes only the window.
            _enter_window()
            wipe = "\033[2J\033[H" if _Window.armed else "\033[3J\033[2J\033[H"
            prefix = wipe + "".join(
                f"\033[{margin + index + 1};1H{text}"
                for index, text in enumerate(pinned)
            )
        output.write(
            prefix
            + f"\033[?25l\033[{status_row};1H\033[2K{line}\033[K"
            + f"\033[{status_row + 1};1H\033[2K{under}\033[K"
        )
        output.flush()
        size = (height, width)

    def spin() -> None:
        while not stop.wait(0.08):
            try:
                paint()
            except Exception:  # noqa: BLE001 - a dead stdout must not kill the thread loudly
                return

    thread = None
    _active_status = status
    try:
        try:
            paint()
            thread = threading.Thread(target=spin, daemon=True)
            thread.start()
        except Exception:  # noqa: BLE001 - no spinner beats no work
            thread = None
        yield status
    finally:
        _active_status = None
        try:
            stop.set()
            if thread is not None:
                try:
                    thread.join(timeout=0.5)
                except RuntimeError:
                    pass  # interrupted before the thread started
        finally:
            try:
                output.write(f"\033[{status_row};1H\033[2K\033[{status_row + 1};1H\033[2K\033[?25h")
                output.flush()
            except Exception:  # noqa: BLE001
                pass
from probe.cli.wizard.terminal.boxes import heading  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.forms import text  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.layout import header_lines, wrap  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.progress import progress_line  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.terminal import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    CONTENT_WIDTH,
    _Window,
    _enter_window,
    _new_screen,
    columns,
    interactive,
    left_pad,
    onboarding_header,
    rows,
    safe_margin,
)
