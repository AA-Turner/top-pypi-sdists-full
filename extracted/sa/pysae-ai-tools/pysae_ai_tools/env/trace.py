"""Resolver progress trace, spinner and interactivity — state carried by context.

The resolver chain narrates its attempts on **stdout** (same stream as the
resolved value): a cyan ``$VAR`` heading, then indented ``⏳ / ✓ / ✗ / ↷`` lines.
Two switches shape that narration, both scoped to a ``with`` block rather than a
module global so they are re-entrant and thread-safe under a ``ThreadPool``:

- :func:`silence_trace` — suppress every line (``env resolve --set`` / ``--json``
  need a pristine stdout carrying only assignments or JSON).
- :func:`assume_noninteractive` — force resolvers that need a human (browser
  OAuth, credential paste, ``glab auth login``) to self-skip even on a TTY,
  while still printing the trace (unlike silencing).

State lives in :class:`contextvars.ContextVar`, so nesting restores the previous
value on exit and concurrent resolutions never clobber each other.
"""

import contextlib
import sys
import threading
from collections.abc import Iterator
from contextvars import ContextVar

import typer

_silent: ContextVar[bool] = ContextVar("env_trace_silent", default=False)
_noninteractive: ContextVar[bool] = ContextVar("env_trace_noninteractive", default=False)


@contextlib.contextmanager
def silence_trace() -> Iterator[None]:
    """Suppress resolver progress lines for the duration of the ``with`` block."""
    token = _silent.set(True)
    try:
        yield
    finally:
        _silent.reset(token)


@contextlib.contextmanager
def assume_noninteractive() -> Iterator[None]:
    """Force resolvers to treat the run as non-interactive for the ``with`` block."""
    token = _noninteractive.set(True)
    try:
        yield
    finally:
        _noninteractive.reset(token)


def set_noninteractive(enabled: bool) -> None:
    """Force resolvers to treat the run as non-interactive for the rest of it.

    The un-scoped form of :func:`assume_noninteractive`, for a CLI flag that
    applies to a whole invocation rather than a block. Wired to the install
    framework's ``--non-interactive`` (see
    ``install.common.checklist.force_non_interactive``) so that one flag silences
    both layers: the prompts *and* the resolvers that would open a browser.
    """
    _noninteractive.set(enabled)


def is_silent() -> bool:
    """True when the trace is suppressed (``--set`` / ``--json`` mode)."""
    return _silent.get()


def is_tty() -> bool:
    """True when stdout is an interactive terminal (where the trace lives)."""
    try:
        return sys.stdout.isatty()
    except (AttributeError, ValueError):
        return False


def is_non_interactive() -> bool:
    """True when no TTY is attached or trace is silenced (CI / --set mode).

    Resolvers that need human interaction (browser auth, credential
    paste, yes/no prompts) consult this to decide whether to attempt
    the recovery path or skip cleanly.
    """
    return _noninteractive.get() or not is_tty() or is_silent()


def emit(line: str, *, color: str | None = None) -> None:
    """Print a resolver progress line on stdout (unless suppressed).

    Trace lives on stdout — same stream as the resolved value. The
    ``--set`` mode silences it entirely (:func:`silence_trace`) so that
    ``eval "$(pysae-ai-tools env resolve --set VAR)"`` only sees the
    shell-syntax assignment lines.
    """
    if is_silent():
        return
    if color is None:
        typer.echo(line)
    else:
        typer.secho(line, fg=color)
    sys.stdout.flush()


def header(var: str) -> None:
    """Print the var name as a heading before its resolver attempts.

    A blank line precedes the heading so each variable's block is visually
    separated from the previous one in the upfront install section.
    """
    emit("")
    emit(f"  ${var}", color=typer.colors.CYAN)


def expand_label(label: str) -> str:
    """Substitute the ``<user>`` placeholder in a label with the real AWS username.

    Only resolves the username when a label is actually displayed (skipped in
    silent ``--set`` / ``--json`` mode, so no STS round-trip there). The lookup
    is cached, so this is cheap after the first call.
    """
    if is_silent() or "<user>" not in label:
        return label
    from .aws import current_aws_username

    user = current_aws_username()
    return label.replace("<user>", user) if user else label


_SPINNER_FRAMES = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")
_SPINNER_INTERVAL_S = 0.08


class _Spinner:
    """Background thread that redraws a braille-spinner frame next to a label.

    Single-line redraw via ``\\r`` + ``\\033[2K`` (erase to end of line); the
    main thread is expected to call :meth:`stop` before printing the final
    outcome on the same line.
    """

    def __init__(self, label: str) -> None:
        self.label = label
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        i = 0
        while not self._stop.is_set():
            frame = _SPINNER_FRAMES[i % len(_SPINNER_FRAMES)]
            sys.stdout.write("\r\033[2K")
            typer.secho(f"    {frame} {self.label}", fg=typer.colors.YELLOW, nl=False)
            sys.stdout.flush()
            i += 1
            self._stop.wait(_SPINNER_INTERVAL_S)

    def stop(self) -> None:
        if self._thread is not None:
            self._stop.set()
            self._thread.join()
            self._thread = None


_active_spinner: ContextVar[_Spinner | None] = ContextVar("env_trace_spinner", default=None)


def pending(label: str) -> None:
    """Start a spinner next to ``label`` (or print a static placeholder when
    we don't have a TTY). The spinner is stopped — and its line cleared — by
    the next :func:`success` / :func:`failure` / :func:`skipped` call.
    """
    if is_silent():
        return
    if is_tty():
        spinner = _Spinner(label)
        _active_spinner.set(spinner)
        spinner.start()
    else:
        typer.secho(f"    ⏳ {label}", fg=typer.colors.YELLOW)


def _clear_pending_line() -> None:
    """Stop the active spinner and erase its line so the final outcome can be printed."""
    if is_silent():
        return
    spinner = _active_spinner.get()
    if spinner is not None:
        spinner.stop()
        _active_spinner.set(None)
    if is_tty():
        sys.stdout.write("\r\033[2K")
        sys.stdout.flush()


def success(label: str) -> None:
    """Print an indented success line under a previously printed header."""
    _clear_pending_line()
    emit(f"    ✓ {label}", color=typer.colors.GREEN)


def failure(label: str, reason: str) -> None:
    """Print a short indented failure line under the var header."""
    _clear_pending_line()
    emit(f"    ✗ {label} failed — {reason}", color=typer.colors.BRIGHT_BLACK)


def skipped(label: str, reason: str) -> None:
    """Print an indented skip line — distinct from a hard failure.

    Used by resolvers that genuinely need a TTY to recover (interactive
    auth flows, credential prompts) when the run is non-interactive
    (CI, ``--set`` mode, headless invocations). The chain falls through
    to the next resolver as if this one had failed, but the trace makes
    clear it was deliberately not attempted rather than tried-and-failed.
    """
    _clear_pending_line()
    emit(f"    ↷ {label} skipped — {reason}", color=typer.colors.BRIGHT_BLACK)


def skipped_fallback(label: str) -> None:
    """Print a dim-grey line for an unused fallback resolver.

    Surfaces what the resolver chain *would* have tried next if the earlier
    resolver had failed — gives the user a complete picture of the chain
    without having to read ``env/config.py``.
    """
    if is_silent():
        return
    typer.secho(f"    ↷ {label} (fallback non utilisé)", fg=typer.colors.BRIGHT_BLACK)
    sys.stdout.flush()
