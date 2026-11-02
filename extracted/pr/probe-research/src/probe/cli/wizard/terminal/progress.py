"""the install phase as one live screen: steps with marks, a progress bar, merged pairing lines."""

from __future__ import annotations
import re
from collections.abc import Callable, Sequence


#: How a step reads in the plan list, by state.
_PENDING, _ACTIVE, _OK, _FAILED = "pending", "active", "ok", "failed"
_MARKS = {_PENDING: "·", _ACTIVE: "»", _OK: "✔", _FAILED: "✗"}

#: Width of the progress bar itself. Comfortably under
#: CONTENT_WIDTH so the bar plus its counter never needs wrapping.
_BAR_WIDTH = 28


def progress_bar(fraction: float, *, width: int | None = None, centered: bool = False) -> str:
    """A compact track with a solid fill that reads without terminal colours."""
    room = max(1, min(CONTENT_WIDTH, columns() - left_pad() - 1))
    width = max(1, min(_BAR_WIDTH if width is None else width, room))
    fraction = max(0.0, min(1.0, fraction))
    # Keep a cell unfilled until completion, even after rounding.
    filled = width if fraction == 1 else min(width - 1, int(width * fraction))
    bar = "━" * filled + "─" * (width - filled)
    return " " * ((room - width) // 2) + bar if centered else bar


def percent(fraction: float) -> str:
    """`fraction` as a whole percentage, rounded DOWN: 100% only when done."""
    fraction = max(0.0, min(1.0, fraction))
    return "100%" if fraction == 1 else f"{min(99, int(fraction * 100))}%"


def progress_line(fraction: float, *, width: int | None = None) -> str:
    """`progress_bar` with its percentage beside it, the pair kept to the
    room `progress_bar` would have had alone."""
    room = max(1, min(CONTENT_WIDTH, columns() - left_pad() - 1))
    label = percent(fraction)
    bar_width = max(1, min(_BAR_WIDTH if width is None else width, room - len(" 100%") - 1))
    return f"{progress_bar(fraction, width=bar_width)}  {label}"


#: `setup.authorize`'s line for each coding agent its sign-in paired.
_PAIRED = re.compile(r"^(?P<agent>.+?) Session capture paired \(device [^)]*\)\.$")


def _merged_pairings(lines: Sequence[str]) -> list[str]:
    """`lines` with every agent's "<agent> Session capture paired (device
    <id>)." made one line where the first stood: a sign-in for four agents
    said it four times, device ids included."""
    agents = [m.group("agent") for line in lines if (m := _PAIRED.match(line))]
    if len(agents) < 2:
        return list(lines)
    merged = ", ".join(agents[:-1]) + f" and {agents[-1]}"
    out: list[str] = []
    for line in lines:
        if not _PAIRED.match(line):
            out.append(line)
        elif merged:
            out.append(f"Session capture paired: {merged}.")
            merged = ""
    return out


class Progress:
    """The install phase as ONE live screen, not a stream of lines.

    The phase used to collect every message into a list and print the lot after
    all of it had finished. Since a step here shells out to `claude` -- up to
    six times, each with its own multi-second timeout -- that meant the screen
    sat on "This run will:" and nothing else for minutes, which reads as a hang.
    It also printed through `say()`, which left-pads but does NOT wrap, so a
    200-character error from `claude` ran off the block and wrapped at the
    terminal's right edge back to column 0.

    Both problems are `page()`'s job, so this drives `page()`: it wraps, it
    centres horizontally AND vertically, and it is already tested. Each state
    change redraws the whole screen.

    TWO RENDERINGS, because a screen and a log want opposite things:

      interactive   clear + redraw the whole block, bar and all
      piped/CI      append ONE line per step as it resolves

    A redraw into a pipe would print the growing block once per step (page()
    skips the clear when it is not interactive), which is log spam rather than
    progress. Appending keeps `probe wizard --yes` greppable and -- the reason
    it matters -- leaves evidence of WHICH step a wedged CI job died on.

    Results accumulate rather than scrolling past: `clear()` emits \\033[3J,
    which drops the scrollback, so anything not re-drawn is gone for good.
    """

    def __init__(
        self,
        title: str,
        steps: list[str],
        *,
        overall: Callable[[float], Sequence[str]] | None = None,
        run: Callable[[float, int], tuple[str, float]] | None = None,
    ) -> None:
        # `overall` maps this agent's resolved tasks into the containing install
        # flow (the guided install's step header). `run` maps them into the
        # whole run, every coding agent's work in it (`setup.InstallRun`): its
        # heading and its bar. Without it the heading is `title` and the bar
        # this phase's own steps.
        self._title = title
        self._steps = list(steps)
        self._state = [_PENDING] * len(steps)
        self._results: list[str] = []
        self._next: list[str] = []
        self._queued: list[str] = []
        self._overall = overall
        self._run = run
        self._shown = 0.0
        #: ((rows, columns), blank rows above the block): `_top`.
        self._anchor: tuple[tuple[int, int], int] | None = None

    # -- state ---------------------------------------------------------------

    def start(self, index: int) -> None:
        if 0 <= index < len(self._state):
            self._state[index] = _ACTIVE
        self.render()

    def finish(self, index: int, *, ok: bool = True) -> None:
        if 0 <= index < len(self._state):
            self._state[index] = _OK if ok else _FAILED
            self._queued.append(
                f"[{self._done()}/{len(self._steps)}] {self._steps[index]}"
                f" ... {'ok' if ok else 'FAILED'}"
            )
        self.render()

    def note(self, *lines: str) -> None:
        """Attach output to the screen. Kept until the phase ends."""
        for line in lines:
            if line:
                self._results.append(line)
                self._queued.append(line)
        self.render()

    def next_steps(self) -> list[str]:
        """What the user still has to do (`note_next`)."""
        return list(self._next)

    def failed_steps(self) -> list[str]:
        return [step for step, state in zip(self._steps, self._state, strict=False) if state == _FAILED]

    def problems(self) -> list[str]:
        """Each failed step, then the noted lines that are an error or what to
        do about one (`setup.needs_attention`: "could not ...", "browser
        approval failed: ...", "revoke the key ..."), never the routine report."""
        from probe.cli import wizard as wizard

        return [
            *(f"{step}: failed" for step in self.failed_steps()),
            *(
                line.removeprefix("! ").strip()
                for line in self._results
                if line.strip() and wizard.needs_attention(line)
            ),
        ]

    def note_next(self, *lines: str) -> None:
        """Attach an action the user still has to take, after this run ends.

        A separate bucket because the two halves of this screen answer different
        questions -- what happened, and what you do now -- and a reader looking
        for the second one should not have to find it inside a paragraph about
        the first. `Restart Codex` and `approve the hook` used to sit at the end
        of a wall of prose, which is where the hook approval got missed.
        """
        for line in lines:
            if line:
                self._next.append(line)
                self._queued.append(line)
        self.render()

    # -- rendering -----------------------------------------------------------

    def _done(self) -> int:
        return sum(1 for s in self._state if s in (_OK, _FAILED))

    def _get_fraction(self) -> float:
        return self._done() / len(self._steps) if self._steps else 1.0

    def _heading(self) -> tuple[str, float]:
        """The heading over the bar, and the fraction the bar shows: never
        less than it showed before (a total that grows must not undo it)."""
        heading, fraction = (
            self._run(self._get_fraction(), len(self._steps)) if self._run is not None
            else (self._title, self._get_fraction())
        )
        self._shown = max(self._shown, fraction)
        return heading, self._shown

    def bar(self) -> str:
        # The column's full width, as the install's step bar: the block's
        # widest row, so the screen reads centred.
        return progress_line(self._heading()[1], width=CONTENT_WIDTH)

    def block(self) -> list[str]:
        heading, fraction = self._heading()
        lines = [*self._overall(self._get_fraction()), ""] if self._overall is not None else []
        lines += [heading, progress_line(fraction, width=CONTENT_WIDTH), ""]
        lines += [
            f"  {_MARKS[state]} {step}"
            for step, state in zip(self._steps, self._state, strict=False)
        ]
        if self._results:
            lines += ["", "What changed:", *(f"  - {line}" for line in _merged_pairings(self._results))]
        if self._next:
            lines += ["", "What's next:", *(f"  - {line}" for line in self._next)]
        return lines

    def render(self) -> None:
        if not interactive():
            # Append-only: emit what is NEW, never the whole block again.
            #
            # FLUSHED, and that is the load-bearing word. Piped stdout is block
            # buffered, so without this the lines sit in a 4-8KB buffer that a
            # short run never fills -- and the run that matters most never
            # fills it at all: `authorize` prints the browser approval URL and
            # code through `note()` and then BLOCKS on a human, so the one
            # instruction the caller has to act on is the one guaranteed to be
            # trapped. Measured: 6s after note() returned, a piped reader had
            # received zero bytes.
            #
            # It also makes this branch's own promise true. The docstring above
            # says appending "leaves evidence of WHICH step a wedged CI job died
            # on" -- a wedged job is precisely one that never flushes on exit,
            # so that evidence was unreachable in exactly the case it was
            # written for.
            for line in self._queued:
                print(line, flush=True)
            self._queued.clear()
            return
        self._queued.clear()
        block = self.block()
        header, body = (block[:2], block[3:]) if self._overall is not None else (None, block)
        page([*[""] * self._top(body, header), *body], progress=header)

    def _top(self, body: list[str], header: Sequence[str] | None) -> int:
        """Blank rows above `body`, centring it in the room under its header
        as prompts and `working()` are: set by the first screen, then moved
        up only as far as the lines added after it need (results arrive one
        step at a time, and a block recentred on each would jump)."""
        screen, width = max(1, rows()), max(1, columns())
        pinned = header_lines(header if header is not None else onboarding_header())
        room = screen - 2 * safe_margin(screen) - (len(pinned) + 1 if pinned else 0)
        column = max(1, min(CONTENT_WIDTH, width - left_pad() - 1))
        # Counted as `page()` will draw it: a line holding newlines is several.
        rows_drawn = "\n".join(body).splitlines()
        height = sum(len(wrap(line, column)) if len(line) > column else 1 for line in rows_drawn)
        if self._anchor is None or self._anchor[0] != (screen, width):
            self._anchor = ((screen, width), max(0, (room - height) // 2))
        top = max(0, min(self._anchor[1], room - height))
        self._anchor = (self._anchor[0], top)
        return top

    def close(self) -> None:
        """Leave the finished screen on display, results and all."""
        self.render()
from probe.cli.wizard.terminal.boxes import heading  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.layout import header_lines, page, wrap  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.terminal import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    CONTENT_WIDTH,
    columns,
    interactive,
    left_pad,
    onboarding_header,
    rows,
    safe_margin,
)
