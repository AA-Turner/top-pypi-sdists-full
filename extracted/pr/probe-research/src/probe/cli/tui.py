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
from typing import NamedTuple

#: Returned by a prompt when the user pressed Escape. Distinct from None, which
#: questionary already uses for Ctrl-C -- "go back one step" and "abandon the
#: whole wizard" are different intentions and must not collapse into each other.
BACK = object()
#: Decline this optional import and continue the surrounding flow.
SKIP = object()


class StyledLine(str):
    """Plain text with a shared TUI style, including after wrapping."""

    def __new__(cls, text: str, *, style: str = ""):
        line = super().__new__(cls, text)
        line.style = style
        return line

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


def indent(text: str, pad: int | None = None) -> str:
    """Shift every line right so a block sits centred."""
    prefix = " " * (left_pad() if pad is None else pad)
    return "\n".join(prefix + line if line.strip() else line for line in text.splitlines())


def wrap(text: str, width: int = CONTENT_WIDTH) -> list[str]:
    """Break a paragraph at CONTENT_WIDTH so centring has something to centre.

    A line wider than the block runs off the right edge once it carries the
    left pad, and then wraps at whatever column the terminal happens to end at
    -- which reads as a broken layout rather than a long sentence.

    Leading indent is preserved. A bullet hangs two further, to clear its own
    "- " marker; a plain paragraph stays flush, because indenting its second
    line makes it look like a list item that lost its bullet.
    """
    import textwrap

    lead = " " * (len(text) - len(text.lstrip()))
    hang = lead + ("  " if text.lstrip().startswith("- ") else "")
    return textwrap.wrap(text.strip(), width, initial_indent=lead, subsequent_indent=hang) or [""]


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


class Frame(NamedTuple):
    """How one full screen's rows are spent, top to bottom."""

    top: int
    header: int
    body: int
    bottom: int


def frame_rows(available: int, height: int | None, header: int = 0, *, margin: int = MARGIN) -> Frame:
    """Split `available` screen rows into top margin, header, body, bottom margin.

    The one place the margin arithmetic lives, so `center_vertically` and the
    tests cannot drift apart. Guarantees, in order of precedence:

    1. Every field is >= 0 and the four sum to exactly `available`. A negative
       Dimension is not a cosmetic bug -- prompt_toolkit raises on it, and the
       whole point of this module's guards is that layout never takes the
       prompt down with it.
    2. `body` never exceeds `available - header - 2*margin`. Content taller
       than that SCROLLS inside the frame rather than overflowing past the
       bottom edge, which is why the body gets a fixed height instead of its
       preferred one.
    3. `top` and `bottom` are each at least `margin` (default MARGIN) -- until
       the terminal is too short to afford it, when the margin shrinks.
       Whitespace is what gives way on a tiny screen.
    """
    available = max(1, available)
    header = max(0, min(header, available - 1))
    margin = max(0, min(margin, (available - header - 1) // 2))
    body_max = max(1, available - header - 2 * margin)
    body = body_max if height is None else max(1, min(height, body_max))
    extra = max(0, available - header - body)
    top = min(extra, max(margin, extra // 2))
    return Frame(top=top, header=header, body=body, bottom=extra - top)


def top_spacer(height: int) -> int:
    """Blank rows `page()` prints above a block of `height` rows.

    `page()` cannot reserve rows the way a prompt_toolkit layout can -- it is
    plain prints onto a screen `clear()` has already blanked, so the bottom
    margin is simply the rows it declines to fill. That makes the top spacer
    the only knob, and it carries both jobs: the MARGIN, and the centring.

    Two rules survive from before the margin existed:

    * A block taller than the SCREEN still gets no spacer at all. Centring it
      would only choose which end to amputate, and the top is the end with the
      verdict on it.
    * Between those, the margin gives way before the content does: a block that
      fits the screen but not the framed area keeps every line, with whatever
      margin is left over.
    """
    screen = max(1, rows())
    framed_height = max(1, screen - 2 * MARGIN)
    return min(MARGIN + max(0, framed_height - height) // 2, max(0, screen - height))


def _copy_to_clipboard(
    text: str, output, *, label: str = "Full report", compact: bool = False,
) -> str:
    """Prefer the local clipboard; SSH must address the reader's terminal.

    OSC 52 has no success acknowledgement, so report sending the request
    separately from a native clipboard command that completed successfully.
    """
    import base64
    import os
    import subprocess

    commands: list[tuple[list[str], str]] = []
    if not (os.environ.get("SSH_CONNECTION") or os.environ.get("SSH_TTY")):
        if sys.platform == "darwin":
            commands.append((["pbcopy"], "utf-8"))
        elif sys.platform == "win32":
            commands.append((["clip.exe"], "utf-16le"))
        else:
            if os.environ.get("WAYLAND_DISPLAY"):
                commands.append((["wl-copy"], "utf-8"))
            if os.environ.get("DISPLAY"):
                commands.extend([
                    (["xclip", "-selection", "clipboard"], "utf-8"),
                    (["xsel", "--clipboard", "--input"], "utf-8"),
                ])
    for command, encoding in commands:
        if not shutil.which(command[0]):
            continue
        try:
            subprocess.run(
                command,
                input=text.encode(encoding),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2,
                check=True,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        return f"{label} copied." if compact else f"{label} copied to clipboard."

    if interactive() and os.environ.get("TERM") != "dumb":
        payload = base64.b64encode(text.encode("utf-8")).decode("ascii")
        try:
            # https://www.invisible-island.net/xterm/ctlseqs/ctlseqs.html
            output.write_raw(f"\033]52;c;{payload}\a")
            output.flush()
        except OSError:
            pass
        else:
            return "Copy sent; paste to check." if compact else "Copy sent to terminal; paste to check clipboard support."
    return "Copy unavailable; select text." if compact else "Could not copy. Run `probe doctor` to get the report as text."


def _copy_prompt(text: str, message: str) -> str:
    """Copy on a single keypress and stay on the report until Enter/Escape."""
    from prompt_toolkit import PromptSession
    from prompt_toolkit.application import get_app_session
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.keys import Keys

    bindings = KeyBindings()
    status = ""

    @bindings.add("c")
    @bindings.add("C")
    def copy(event) -> None:
        nonlocal status
        status = _copy_to_clipboard(text, event.app.output)
        event.app.invalidate()

    @bindings.add("enter")
    @bindings.add("escape", eager=True)
    def back(event) -> None:
        event.app.exit(result="")

    @bindings.add(Keys.Any)
    @bindings.add(Keys.BracketedPaste)
    def ignore(event) -> None:
        pass

    def hint() -> str:
        lines = ([status] if status else []) + [f"c Copy full report · {message}"]
        return indent("\n".join(lines))

    # An explicit output keeps prompt_toolkit's TERM=dumb fallback from
    # replacing our single-key bindings with its default line input.
    return PromptSession(output=get_app_session().output).prompt(hint, key_bindings=bindings)


def page(
    lines: list[str], prompt: str | None = None, *, copyable: bool = False,
    progress: Sequence[str] | None = None,
) -> str:
    """Show output in the shared frame; a pause uses scrollable content.

    Piped output remains plain text. Live progress without a prompt leaves
    its latest state visible. Reports with a prompt keep Continue and keyboard
    help in the same place as other pages. Copy includes the full original
    report, including rows outside the viewport.
    """
    progress = progress if progress is not None else onboarding_header()
    raw = "\n".join(lines).splitlines()
    if not interactive():
        # Verbatim: hard-wrapping piped output only breaks a grep.
        print("\n".join([*(progress or []), *raw]))
        return ""
    if prompt is not None:
        import questionary

        title, *details = raw or ["Probe Research"]
        question = questionary.select(
            "Continue", choices=[questionary.Choice("Continue", value="")],
            style=style(), pointer=pointer(), instruction=" ",
        )
        hint = "enter continue · tab read · pgup/dn · esc back"
        if copyable:
            hint = "enter continue · c copy · tab read · pgup/dn · esc back"

            @question.application.key_bindings.add("c", eager=True)
            @question.application.key_bindings.add("C", eager=True)
            def copy_report(event):
                _copy_to_clipboard("\n".join(lines), event.app.output)

        sectioned(question, title=title, lines=details, prompt=prompt, instruction=hint)
        ask(question, progress=progress)
        return ""
    body: list[str] = []
    width = max(1, min(CONTENT_WIDTH, columns() - left_pad() - 1))
    for line in raw:
        # Wrapped HERE, not by the terminal: a line that overflows the block
        # wraps back to column 0, which breaks the centred column the whole
        # page is built on.
        body += wrap(line, width) if len(line) > width else [line]
    screen = max(1, rows())
    margin = safe_margin(screen)
    pinned = [*header_lines(progress), ""] if progress else []
    pinned = pinned[:max(0, screen - 2 * margin - 1)]
    room = max(1, screen - 2 * margin - len(pinned))
    if len(body) > room:
        # Live progress must not scroll the heading under terminal chrome.
        # Keep the title and most recent status, marking omitted history.
        hidden = len(body) - room + 1
        body = ([body[0], f"… {hidden} earlier lines hidden"[:width], *body[-(room - 2):]]
                if room > 2 else body[:room])
    clear()
    if _Window.entered:
        _Window.shown = list(raw)
    print("\n" * margin, end="")
    for line in [*pinned, *(indent(line) if line.strip() else "" for line in body)]:
        print(line)
    return ""


def style():
    """Questionary styling.

    Two deliberate choices:

    * `highlighted` is `noreverse`. The default inverts the whole entry into a
      block of background colour, which on a multi-line choice paints three
      lines of solid white and is genuinely hard to read.
    * `selected` is green, so a ticked box reads as ticked at a glance rather
      than needing you to compare two similar glyphs.
    * `separator` and `instruction` are warm tan, not grey. At #6c6c6c the
      headings and hints read as disabled; #b56f28 is the amber the
      dashboard's status dots use (globals.css), so the two surfaces share a
      palette -- its lighter tint #f7ecdd was tried first and washed out.
      `nav_back` is the one deliberate grey survivor -- see `dim_band_back`.
    """
    import questionary

    return questionary.Style(
        [
            ("qmark", "fg:#5f87ff bold"),
            ("question", "bold"),
            ("pointer", "fg:#5f87ff bold"),
            ("highlighted", "noreverse bold"),
            ("selected", "fg:#00af5f noreverse"),
            ("separator", "fg:#b56f28"),
            ("instruction", "fg:#b56f28"),
            ("nav_back", "fg:#6c6c6c"),
            ("answer", "fg:#00af5f bold"),
            ("danger", "fg:#d75f5f"),
        ]
    )


def use_checkmarks() -> None:
    """Swap questionary's ●/○ for ✔/○.

    `common` does `from questionary.constants import INDICATOR_SELECTED`, so the
    name is bound at import time and patching `questionary.constants` has no
    effect. The module that actually reads it is the one to patch.

    Still used by prompts that let questionary draw the box. The capability
    picker draws its own -- see `TICK` / `UNTICK` and `checkbox_control`.
    """
    from questionary.prompts import common

    common.INDICATOR_SELECTED = "✔"
    common.INDICATOR_UNSELECTED = "○"


#: The box we draw OURSELVES, on rows that carry one.
TICK = "✔"
UNTICK = "○"
#: The MIDDLE of a three-state row (`setup.row_box`). A third glyph rather than
#: a tick reused: a cycling row drawn with two glyphs makes two of its three
#: states look identical, and on the tracking default the pair that would
#: collide is `read-only` and `off` -- the state where the team's history is
#: still searchable and the state where it is not.
HALF = "◐"
#: The `daemon` position of the same row: recording is on, and something other
#: than the agent does it. Filled rather than ticked so it never reads as `on`.
AUTO = "◉"


def checkbox_control(question):
    """The questionary InquirerControl behind a checkbox prompt, or None.

    Reached through the layout because `checkbox()` keeps the control in a
    closure and hands back only a Question. Same posture as
    `center_vertically`: questionary is pinned `>=2.0,<3`, the codebase already
    patches its module-level indicator constants, and every reach-in here is
    guarded so a reshuffle degrades the prompt instead of breaking it.
    """
    try:
        from questionary.prompts.common import InquirerControl

        def walk(container):
            for child in getattr(container, "children", []) or []:
                yield from walk(child)
            inner = getattr(container, "content", None)
            if isinstance(inner, InquirerControl):
                yield inner
            elif inner is not None:
                yield from walk(inner)

        return next(walk(question.application.layout.container), None)
    except Exception:  # noqa: BLE001 - a prompt that renders is worth more than a box
        return None


def draw_own_boxes(question) -> bool:
    """Stop questionary drawing the box, so WE decide which rows get one.

    `use_indicator` is all-rows-or-nothing and `checkbox()` does not expose it
    (passing it reaches PromptSession and raises), so it is set on the control
    after construction. The reason we want it off at all: a row you can put the
    cursor on ALWAYS gets a box, and an action row -- "Next" -- rendered as
    `○ Next` reads as an option someone forgot to tick.

    Returns whether it worked, so the caller can fall back to questionary's own
    box rather than shipping a picker with no boxes at all.
    """
    control = checkbox_control(question)
    if control is None:
        return False
    control.use_indicator = False
    return True


#: Token classes a nav band row can arrive under. It was `class:separator`
#: alone while the band was a label; now that it takes the cursor questionary
#: styles it as a choice -- `class:text` when it is not pointed at,
#: `class:highlighted` when it is -- and a repaint keyed on the old class alone
#: silently stopped firing the day the band became selectable.
_BAND_CLASSES = ("class:separator", "class:text", "class:highlighted")


def dim_band_back(question, left: str, *, active=None) -> bool:
    """Repaint the `‹ Back` half of the nav band grey, leaving `Next ›` tan.

    The band is ONE row and questionary styles a row as one token -- so the two
    halves cannot carry different colours from the title alone. The control's
    token source is the bound method it handed to prompt_toolkit at
    construction, reachable as `.text` afterwards, so it is wrapped here: any
    band token containing `left` gets that span re-tagged `class:nav_back` and
    keeps its own class for the rest of the row.

    `active` is a zero-argument predicate saying that Back is the end the cursor
    is on right now, and it SKIPS the dim for that render. Quieting Back is a
    statement about which end is secondary; making it the dimmest thing on
    screen at the moment it is also the selected thing says the opposite, and
    the rectangle around it would be arguing with its own contents.

    Same posture as `draw_own_boxes`: a guarded reach into internals that
    degrades to a one-colour band rather than failing to render.
    """
    control = checkbox_control(question)
    if control is None:
        return False
    try:
        original = control.text

        def repaint():
            # Guarded INSIDE the render loop too, not just at attachment: a
            # token whose text is not a str (questionary extends list-titles
            # into the stream verbatim) must degrade to the unsplit band, not
            # crash a prompt that would have rendered fine unwrapped.
            try:
                if active is not None and active():
                    return original()
                tokens = []
                for token in original():
                    if len(token) == 2 and token[0] in _BAND_CLASSES and left in token[1]:
                        head, _, tail = token[1].partition(left)
                        if head:
                            tokens.append((token[0], head))
                        tokens.append(("class:nav_back", left))
                        if tail:
                            tokens.append((token[0], tail))
                    else:
                        tokens.append(token)
                return tokens
            except Exception:  # noqa: BLE001 - a one-colour band beats no prompt
                return original()

        control.text = repaint
        return True
    except Exception:  # noqa: BLE001 - a one-colour band beats no prompt
        return False


def blank_pointer_when(question, predicate) -> bool:
    """Draw no `»` on the rows `predicate` accepts, without moving their text.

    ONE row needs this: the nav band, whose `‹ Back` and `Next ›` are two cursor
    stops on a single line. questionary can only put its pointer at the START of
    a row, so on the band it would sit against `‹ Back` while the rectangle sat
    around `Next ›` -- two markers claiming the cursor is in two places. The
    rectangle is the marker there; the arrow keeps the option rows, which is
    where it says something the box does not.

    The pointer token is replaced by spaces of the same width rather than
    dropped, so the band's columns do not shift when the cursor arrives on it.
    """
    control = checkbox_control(question)
    if control is None:
        return False
    try:
        original = control.text

        def repaint():
            try:
                pointed = control.get_pointed_at()
                if pointed is None or not predicate(getattr(pointed, "value", None)):
                    return original()
                return [
                    (("class:text", " " * len(token[1])) if token[0] == "class:pointer" else token)
                    for token in original()
                ]
            except Exception:  # noqa: BLE001 - two markers beat no prompt
                return original()

        control.text = repaint
        return True
    except Exception:  # noqa: BLE001 - two markers beat no prompt
        return False


def content_height(message: str, choices=(), instruction: str = "") -> int:
    """How many rows the prompt will occupy.

    Counted, not asked. `Container.preferred_height()` needs a running event
    loop and returns a placeholder without one, which silently produced a
    22-row spacer for 44 rows of content and pushed the BOTTOM off instead --
    the same bug wearing a different hat.

    Pass the prompt's `instruction` too when the LAST rows matter: questionary
    appends it to the question line at render, and if the combined line wraps
    at the terminal edge every count below it is one row short -- the body
    window folds its final rows, which since the band moved to the bottom are
    exactly `‹ Back / Next ›`. Measured, not hypothetical: a 14-char longer
    instruction folded the band off a real 80x24 pty while blank rows sat
    unused below it.
    """
    import questionary

    rows = message.count("\n") + 1  # the message block, question included
    if instruction:
        # The question's own last line already carries its pad; questionary
        # renders `<last line> <instruction>` as one row, wrapping at the edge.
        last = message.rsplit("\n", 1)[-1]
        if len(last) + 1 + len(instruction) >= columns():
            rows += 1
    for choice in choices:
        if isinstance(choice, questionary.Separator):
            rows += 1
        else:
            rows += str(getattr(choice, "title", "")).count("\n") + 1
    # Only a list prompt draws an instruction line. A confirm renders its
    # answer inline on the last message row, so counting one for it would sit
    # the whole page half a row high.
    return rows + (1 if choices else 0)


def header_lines(header: str | Sequence[str] | None) -> list[str]:
    """Normalise a `header=` argument into the rows that get pinned.

    Public because the caller needs to know what its header will cost before it
    counts the rest: the header sits OUTSIDE `content_height()`, which counts
    only what questionary draws. Long lines are wrapped to CONTENT_WIDTH and
    every line carries the same `left_pad()` as the block below it, so a pinned
    path lines up with the question rather than floating at column 0.

    Accepts a plain string (split on newlines) or any sequence of lines.
    """
    if header is None:
        return []
    raw = header.splitlines() if isinstance(header, str) else list(header)
    out: list[str] = []
    width = max(1, min(CONTENT_WIDTH, columns() - left_pad() - 1))
    for line in raw:
        for part in wrap(line, width) if len(line) > width else [line]:
            out.append(indent(part) if part.strip() else "")
    return out


def center_vertically(
    question,
    height: int | None = None,
    header: str | Sequence[str] | None = None,
    *,
    margin: int = MARGIN,
    progress: Sequence[str] | None = None,
):
    """Render full-screen, with shared pages anchored and legacy prompts centred.

    questionary renders inline, growing downward from the cursor, so anything
    taller than the room below it scrolls -- which is what kept eating the first
    rows of the state block, and is worse in a block-based terminal like Warp
    where the block boundary is not where a classic terminal's would be.

    Full screen removes the problem outright: prompt_toolkit owns the viewport,
    so there is no "above" to scroll into. It is also the only way centring
    becomes possible at all.

    The layout is four bands -- top margin, pinned header, body, bottom margin
    -- sized by `frame_rows()`. Three consequences worth stating:

    * The top and bottom bands are EXACT, so the body is whatever is left. That
      is what makes content taller than the frame scroll inside it instead of
      running off the bottom edge: squeezed below its preferred height,
      questionary's choice window scrolls itself to keep the pointed row
      visible -- it emits a `[SetCursorPosition]` token, and that is what
      prompt_toolkit scrolls to. Step screens keep the state block above it;
      the main menu keeps status and choices together, expanding into spare
      bottom space before scrolling the whole page on a short terminal.
    * NOT a ScrollablePane, which is the obvious thing to reach for and is
      wrong here. It follows the FOCUSED window's cursor, and the focused
      window is questionary's input buffer up in the message block -- so the
      pane sits at scroll 0 and the choices below the fold become unreachable.
      Bounding the band lets each window scroll on its own cursor instead.
    * `header` rows are pinned ABOVE the body, so a folder path stays readable
      at the bottom of a long list. They are NOT part of `height`.

    Every reach into questionary/prompt_toolkit internals is guarded, same
    posture as `checkbox_control`: questionary is pinned `>=2.0,<3` and a
    library reshuffle must degrade the prompt, never fail to render it.
    """
    try:
        from prompt_toolkit.layout import HSplit, Layout, Window
        from prompt_toolkit.layout.controls import FormattedTextControl
        from prompt_toolkit.layout.dimension import Dimension

        app = question.application
        inner = app.layout.container
        focused = app.layout.current_window
        pinned = header_lines(header)
        def progress_lines():
            return header_lines(progress if progress is not None else onboarding_header())

        def progress_height():
            lines = progress_lines()
            return len(lines) + 1 if lines else 0

        def frame() -> Frame:
            from prompt_toolkit.application import get_app

            screen_rows = get_app().output.get_size().rows
            available = max(1, screen_rows - progress_height())
            if (getattr(question, "_probe_sectioned", False)
                    or getattr(question, "_probe_continuous", False)):
                frame = frame_rows(available, None, len(pinned), margin=safe_margin(screen_rows))
                fit_choices = getattr(question, "_probe_fit_choices", None)
                if fit_choices is not None:
                    # Keep the top clearance, but let a complete menu use
                    # spare whitespace below it before it has to scroll.
                    spare = max(0, frame.bottom - 2)
                    preferred = fit_choices(frame.body + spare)
                    extra = min(spare, max(0, preferred - frame.body))
                    frame = frame._replace(body=frame.body + extra, bottom=frame.bottom - extra)
                return frame
            return frame_rows(
                available, height, len(pinned), margin=max(margin, safe_margin(screen_rows)),
            )

        def band(name: str):
            return lambda: Dimension.exact(getattr(frame(), name))

        question._probe_body_height = lambda: frame().body

        # Padding surrounds the entire UI, including the progress header.
        bands = [Window(height=band("top"))]
        if progress is not None or _onboarding.get() is not None:
            bands.append(Window(
                height=lambda: Dimension.exact(progress_height()),
                content=FormattedTextControl(lambda: "\n".join(progress_lines()) + "\n"),
                wrap_lines=False, always_hide_cursor=True,
            ))
        if pinned:
            bands.append(
                Window(
                    height=band("header"),
                    content=FormattedTextControl(
                        [("class:question", "\n".join(pinned))], focusable=False
                    ),
                    # Exact height is only exact if a long line cannot silently
                    # become two rows and push the body down.
                    wrap_lines=False,
                    always_hide_cursor=True,
                )
            )
        bands += [HSplit([inner], height=band("body")), Window(height=band("bottom"))]

        app.full_screen = True
        app.layout = Layout(HSplit(bands), focused_element=focused)
    except Exception:  # noqa: BLE001 - layout is cosmetic, never break the prompt
        pass
    if _Window.armed:
        full_window(question)
    return question


def full_window(question) -> None:
    """Draw this prompt over the whole of the wizard's window.

    `app.full_screen = True` above does NOT do this, and never did: prompt_toolkit
    reads full-screen from the RENDERER, which the Application built with its
    own flag before this module saw it. So every prompt drew INLINE, from the
    cursor down, and a terminal that treats inline output as a transcript
    (Warp) scrolled it instead of handing the keys to the menu.

    The renderer is switched here, but the alternate screen stays the
    `window`'s: a prompt that entered and left it itself would drop the whole
    wizard back to the shell's screen between two prompts. Entering is
    replaced by what entering looks like -- a clean window, cursor home -- and
    leaving by nothing, so the next screen draws over this one.
    """
    try:
        _enter_window()
        _new_screen()
        app = question.application
        output = app.output
        if output not in _Window.patched:
            # Leaving wipes the window too: prompt_toolkit's last paint parks
            # the cursor below the prompt, and whatever prints next would land
            # under a prompt that is already answered.
            output.enter_alternate_screen = lambda: output.write_raw("\033[H\033[2J")
            output.quit_alternate_screen = lambda: output.write_raw("\033[H\033[2J")
            _Window.patched.append(output)
        app.renderer.full_screen = True
    except Exception:  # noqa: BLE001 - an inline prompt beats no prompt
        pass


def bind_escape(question):
    """Make Escape resolve the prompt to BACK.

    questionary gives Ctrl-C (abandon) but nothing for "I chose wrong, take me
    back one step", which is the far more common intention in a menu you are
    meant to sit in.
    """
    try:
        bindings = getattr(question, "_probe_bindings", question.application.key_bindings)

        @bindings.add("escape", eager=True)
        def _(event) -> None:  # pragma: no cover - requires a live terminal
            event.app.exit(result=BACK)

    except Exception:  # noqa: BLE001 - never let styling break the prompt
        pass
    return question


def ask(
    question,
    height: int | None = None,
    header: str | Sequence[str] | None = None,
    *,
    margin: int = MARGIN,
    progress: Sequence[str] | None = None,
):
    """Run a prompt full-screen and centred, with Escape bound.

    Returns BACK, None (Ctrl-C), or the chosen value.

    `height` is the counted row total from content_height(); without it the
    prompt still fills the frame, just top-aligned inside it.

    `margin` sets the minimum outer spacing. A smaller value gives long
    review pages more room on compact terminals while keeping them centred.

    `header` is a string or list of lines pinned ABOVE the scrolling body, so
    it stays on screen at the bottom of a long list -- what a folder picker
    needs to keep the current path readable. Do NOT add its rows to `height`:
    the frame reserves them separately (see `header_lines`).
    """
    content = getattr(question, "_probe_content", None)
    if (content is not None and not getattr(question, "_probe_sectioned", False)
            and not getattr(question, "_probe_continuous", False)):
        sectioned(question, **content)
    return bind_escape(center_vertically(
        question, height, header=header, margin=margin, progress=progress,
    )).ask()


def sectioned(
    question, *, title: str, lines: Sequence[str] | Callable[[], Sequence[str]], prompt: str,
    instruction: str | Callable[[], str] = "↑↓ choose · enter · tab read · pgup/dn · esc back",
    compact_choices: Sequence | None = None,
):
    """One installer layout: heading, scrollable content, choices, keyboard help.

    Keep the existing choice control and bindings, including checkbox navigation
    and validation. Only the presentation is shared. Content scrolls independently
    so long explanations never push the actions or keyboard help out of reach.
    """
    from prompt_toolkit.application import get_app
    from prompt_toolkit.filters import has_focus, to_filter
    from prompt_toolkit.layout import HSplit, Layout, ScrollOffsets, VSplit, Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.layout.dimension import Dimension
    from prompt_toolkit.lexers import Lexer
    from prompt_toolkit.widgets import TextArea

    control = checkbox_control(question)
    app = question.application
    bindings = app.key_bindings
    if not hasattr(bindings, "add"):
        from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings

        bindings = KeyBindings()
        app.key_bindings = merge_key_bindings([app.key_bindings, bindings])
    question._probe_bindings = bindings
    # Questionary normally focuses its hidden prompt buffer; the choice
    # control must become focusable when we give it its own action region.
    if control is not None:
        control.focusable = to_filter(True)
    # Buffer controls reserve a trailing cursor cell even with the cursor hidden.
    # Leave it room so a full text line does not wrap onto an empty extra row.
    line_styles = []

    def document_text():
        width = max(1, min(CONTENT_WIDTH, app.output.get_size().columns - left_pad() - 1))
        current = lines() if callable(lines) else lines
        rendered = [
            (part, line.style if isinstance(line, StyledLine) else "")
            for line in current for part in wrap(line, width=width)
        ]
        line_styles[:] = [style for _, style in rendered]
        return "\n".join(part for part, _ in rendered)

    class LineLexer(Lexer):
        def lex_document(self, document):
            def get_line(index):
                style = line_styles[index] if index < len(line_styles) else ""
                return [(style, document.lines[index])]
            return get_line

    initial_text = document_text()
    document = TextArea(
        text=initial_text, read_only=True, focusable=True,
        scrollbar=False, wrap_lines=True, lexer=LineLexer(),
        width=lambda: Dimension.exact(
            max(1, min(CONTENT_WIDTH + 1, get_app().output.get_size().columns - left_pad()))
        ),
        height=lambda: Dimension.exact(region_heights()[0]),
    )
    document.window.always_hide_cursor = to_filter(True)

    def pointed_tail() -> int:
        # The rows under the pointed row's FIRST line -- its description. The
        # window scrolls only as far as the cursor, which sits on that first
        # line, so without this a row at the bottom of a short terminal showed
        # its title with the words that explain it cut off below the fold.
        try:
            return plain_title(control.get_pointed_at().title).count("\n")
        except Exception:  # noqa: BLE001 - a scroll offset is not worth a crash
            return 0

    floor = 1 if compact_choices is not None else 0
    action_window = (
        Window(
            control, wrap_lines=True, always_hide_cursor=True,
            scroll_offsets=ScrollOffsets(top=floor, bottom=lambda: max(floor, pointed_tail())),
        ) if control is not None else None
    )
    action_focus = action_window if control is not None else app.layout.current_window

    def action_width():
        return max(1, min(get_app().output.get_size().columns, left_pad() + CONTENT_WIDTH + 1))

    spacious_choices = list(control.choices) if control is not None else []

    def region_budget():
        # Fit the actual content. Giving the document flexible height turns five
        # status lines into half an empty screen and hides a menu that would fit.
        # When content overflows, reserve room for choices and keep both regions
        # keyboard-scrollable. Unused terminal rows belong AFTER the help line.
        screen = get_app().output.get_size()
        body_height = getattr(question, "_probe_body_height", lambda: max(1, screen.rows - 2))()
        document_rows = len(document.text.splitlines()) if document.text.strip() else 0
        chrome = 2 + bool(document_rows) + (control is not None) + 2
        chrome += bool(control is not None and control.error_message)
        available = max(1, body_height - chrome)
        # Preserve a short status summary in full when it uses at most half
        # the room; longer documents yield more space to the choices.
        minimum_content = (document_rows if document_rows <= available // 2
                           else min(document_rows, max(1, available // 3)))
        return available, minimum_content, document_rows

    def fit_choices():
        if control is None or compact_choices is None:
            return
        available, minimum_content, _ = region_budget()
        pointed = control.get_pointed_at()
        for candidate in (spacious_choices, compact_choices):
            control.choices = list(candidate)
            control.pointed_at = control.choices.index(pointed)
            # Pick a density BEFORE layout caches the live control's tokens.
            # Fresh controls measure candidates without caching stale spacing.
            content = FormattedTextControl(control.text).create_content(
                action_width(), app.output.get_size().rows,
            )
            preferred = sum(
                content.get_height_for_line(index, action_width(), None)
                for index in range(content.line_count)
            )
            if preferred <= available - minimum_content:
                break

    def region_heights():
        available, minimum_content, document_rows = region_budget()
        if control is None:
            preferred = 3
        else:
            content = control.create_content(action_width(), app.output.get_size().rows)
            preferred = sum(
                content.get_height_for_line(index, action_width(), None)
                for index in range(content.line_count)
            )
        action_reserve = min(preferred, max(1, available - minimum_content))
        document_height = min(document_rows, max(0, available - action_reserve))
        return document_height, max(1, min(preferred, available - document_height))

    if action_window is not None:
        action_window.width = lambda: Dimension.exact(action_width())
        actions = VSplit([action_window, Window()])
    else:
        actions = app.layout.container
    actions.height = lambda: Dimension.exact(region_heights()[1])
    title_window = Window(
        FormattedTextControl(lambda: [("class:question", indent(title))]),
        height=2, wrap_lines=False,
    )
    question_window = Window(
        FormattedTextControl(lambda: [("class:question", indent(prompt))]),
        height=1 if control is not None else 0, wrap_lines=False,
    )
    def help_text():
        room = get_app().output.get_size().columns - left_pad()
        readable = bool(document.text.strip())
        hint = instruction() if callable(instruction) else instruction
        escape = next((part.strip() for part in hint.split("·")
                       if part.strip().lower().startswith("esc ")), "esc back")
        if not readable:
            hint = hint.replace(" · tab read", "").replace(" · pgup/dn", "")
        if len(hint) > room:
            toggle = " · space" if "space" in hint else ""
            read = " · tab read" if readable else ""
            hint = f"↑↓ choose{toggle} · enter{read} · {escape}"
        if len(hint) > room:
            read = " · tab" if readable else ""
            hint = f"↑↓ · enter{read} · {escape}"
        return [("class:instruction", indent(hint))]

    help_window = Window(
        FormattedTextControl(help_text),
        height=1, wrap_lines=False,
    )
    validation = Window(
        FormattedTextControl(lambda: [("class:instruction", indent(control.error_message or ""))]
                             if control is not None else []),
        height=lambda: 1 if control is not None and control.error_message else 0,
        wrap_lines=False,
    )
    app.layout = Layout(
        HSplit([
            title_window,
            # The padding windows otherwise expand when the document is empty:
            # a zero-height child does not constrain a VSplit's preferred size.
            VSplit(
                [Window(width=lambda: left_pad()), document, Window()],
                height=lambda: Dimension.exact(region_heights()[0]),
            ),
            Window(height=lambda: int(bool(document.text.strip()))),
            question_window, actions, validation,
            # Spare rows go ABOVE the key hints, which keep the window's last
            # row on every screen, like the menu's.
            Window(height=Dimension(min=0, preferred=0, weight=1)),
            Window(height=1), help_window,
        ]),
        focused_element=action_focus,
    )
    question._probe_sectioned = True
    from prompt_toolkit.document import Document

    def refresh_document(_app):
        if control is not None:
            control.pointer = pointer()
        updated = document_text()
        if updated != document.text:
            position = min(document.buffer.cursor_position, len(updated))
            document.buffer.set_document(Document(updated, position), bypass_readonly=True)
        if not updated.strip() and app.layout.has_focus(document):
            app.layout.focus(action_focus)
        fit_choices()

    app.before_render += refresh_document
    if callable(lines):
        app.refresh_interval = 1.0

    @bindings.add("tab", eager=True)
    @bindings.add("s-tab", eager=True)
    def toggle_focus(event):
        if document.text.strip():
            event.app.layout.focus(action_focus if event.app.layout.has_focus(document) else document)

    @bindings.add("up", filter=has_focus(document), eager=True)
    def document_up(event):
        document.buffer.cursor_up()

    @bindings.add("down", filter=has_focus(document), eager=True)
    def document_down(event):
        document.buffer.cursor_down()

    @bindings.add("enter", filter=has_focus(document), eager=True)
    def return_to_actions(event):
        event.app.layout.focus(action_focus)

    def scroll(event, direction: int) -> None:
        if not document.text.strip():
            return
        info = document.window.render_info
        if info is None:
            return
        buffer = document.buffer
        current = buffer.document.cursor_position_row
        # Repeated keys can arrive before the next render. Advance by a page
        # from the updated cursor instead of reusing a stale viewport edge.
        step = max(1, info.window_height - 1)
        if direction < 0:
            target = max(0, min(info.first_visible_line(), current - step))
        else:
            target = max(info.last_visible_line(), current + step)
        document.window.vertical_scroll = target
        buffer.cursor_position = buffer.document.translate_row_col_to_index(target, 0)

    @bindings.add("pageup", eager=True)
    def page_up(event):
        scroll(event, -1)

    @bindings.add("pagedown", eager=True)
    def page_down(event):
        scroll(event, 1)

    return question


#: A menu row that ends something (sign out): red, and bold while pointed at.
#: Set as `choice.probe_style`; `menu` draws it.
DANGER_STYLE = "class:danger"


def plain_title(title) -> str:
    """A choice title as text, whether a string or formatted `(style, text)` parts."""
    if isinstance(title, list):
        return "".join(part[1] for part in title)
    return str(title)


def review(
    title: str, lines: Sequence[str] | Callable[[], Sequence[str]],
    choices: Sequence[tuple[str, object]] | Callable[[], Sequence[tuple[str, object]]],
    *, instruction: str = "↑↓ choose · enter · tab read · pgup/dn · esc back",
    copy_text: str | None = None, copy_label: str = "text",
    next_value: object | None = None,
    default: object | None = None,
    fallback: object | None = None,
    compact_actions: bool = False,
):
    """A shared installer page with a scrollable document and spaced actions.

    Live choices preserve the selected value as actions change. If that value
    disappears, select ``fallback`` instead; callers should keep a safe action
    such as Back available throughout the visit.
    """
    if not interactive():
        page([title, "", *(lines() if callable(lines) else lines)])
        return None
    import questionary

    def build_options(current):
        options = []
        for label, value in current:
            if options and not compact_actions:
                options.append(questionary.Separator(" "))
            options.append(questionary.Choice(label, value=value))
        return options

    current_choices = list(choices() if callable(choices) else choices)
    question = questionary.select(
        "What would you like to do?", choices=build_options(current_choices), instruction=" ",
        style=style(), qmark=qmark(), pointer=pointer(),
        **({"default": default} if default is not None else {}),
    )
    copy_status = ""
    if copy_text is not None:
        @question.application.key_bindings.add("c", eager=True)
        @question.application.key_bindings.add("C", eager=True)
        def copy(event):
            nonlocal copy_status
            copy_status = _copy_to_clipboard(
                copy_text, event.app.output, label=copy_label.capitalize(),
                compact=True,
            )
            event.app.invalidate()

    def hint():
        if copy_status:
            return copy_status
        room = question.application.output.get_size().columns - left_pad()
        if copy_text is not None and len(instruction) > room:
            return "↑↓ · enter · c copy · esc back"
        return instruction

    sectioned(
        question, title=title, lines=lines, prompt="What would you like to do?",
        instruction=hint,
    )
    if callable(choices):
        control = checkbox_control(question)

        def refresh_choices(_app):
            nonlocal current_choices
            updated = list(choices())
            if updated == current_choices:
                return
            if not updated:
                raise ValueError("Live review choices must include an available action.")
            pointed_value = control.get_pointed_at().value
            values = [value for _, value in updated]
            selected = pointed_value if pointed_value in values else fallback
            if selected not in values:
                if fallback is not None:
                    raise ValueError("The live review fallback must be an available action.")
                selected = values[0]
            options = build_options(updated)
            control.choices = options
            control.pointed_at = next(
                index for index, option in enumerate(options)
                if not isinstance(option, questionary.Separator) and option.value == selected
            )
            current_choices = updated

        # The document refresh runs first, so callers can share one fresh state
        # between their text and action providers without mismatched frames.
        question.application.before_render += refresh_choices
        question.application.refresh_interval = 1.0
    bind_step_keys(question, on_back=lambda event: event.app.exit(result=BACK))
    if next_value is not None:
        bind_step_keys(question, on_next=lambda event: event.app.exit(result=next_value))
        control = checkbox_control(question)

        @question.application.key_bindings.add("enter", eager=True)
        def advance(event):
            # Enter chooses the highlighted action, including from document
            # focus. The right arrow remains the explicit forward shortcut.
            event.app.exit(result=control.get_pointed_at().value if control is not None else next_value)

    return ask(question)


def text(title: str, lines: Sequence[str], prompt: str):
    """A freeform correction using the same frame, style and Escape as menus."""
    if not interactive():
        page([title, *lines])
        return None
    import questionary

    question = questionary.text(prompt, style=style(), qmark=qmark())
    sectioned(
        question, title=title, lines=lines, prompt=prompt,
        instruction="type your response · enter · tab read · pgup/dn · esc back",
    )
    return ask(question)


def rows() -> int:
    try:
        return shutil.get_terminal_size().lines
    except OSError:
        return 24


# NOTE: no vertical centring. questionary emits the qmark BEFORE the message,
# so leading newlines inside the message strand a lone `?` at the top of the
# screen with the content pushed below it. Padding outside the prompt does not
# work either -- prompt_toolkit renders relative to the cursor, so the padding
# is what scrolls the top away. Vertically centred would be nice; wrong-looking
# is worse than top-aligned.


class Framed(str):
    """Plain-text fallback plus the sections used by interactive prompts."""

    def __new__(cls, value: str, *, title: str, lines: Sequence[str], prompt: str):
        result = super().__new__(cls, value)
        result.sections = {"title": title, "lines": list(lines), "prompt": prompt}
        return result


def select(message: str, **kwargs):
    """Questionary select with the installer's shared page sections."""
    import questionary

    question = questionary.select(message, **kwargs)
    if isinstance(message, Framed):
        question._probe_content = message.sections
    return question


def collapsed(choices: Sequence, pointed) -> list:
    """`choices` with every group but the one holding `pointed` cut to its heading.

    A group is a heading Separator and the rows after it, up to the next
    heading. The blank rows directly ABOVE a heading belong to that heading --
    they are its air -- and are kept only where there is something to separate:
    above the first group, and either side of the open one. Collapsed headings
    otherwise stack, one line each, which is the space this saves.

    A group with no heading is never collapsed: there would be nothing left of
    it on screen, and the cursor would still walk through its rows unseen.
    """
    from questionary import Separator

    def blank(choice) -> bool:
        return isinstance(choice, Separator) and not str(choice.title).strip()

    groups: list[tuple[list, list]] = []  # (heading air + heading, rows)
    air: list = []
    for choice in choices:
        if blank(choice):
            air.append(choice)
        elif isinstance(choice, Separator):
            groups.append(([*air, choice], []))
            air = []
        else:
            if not groups:
                groups.append(([], []))
            groups[-1][1].extend([*air, choice])
            air = []
    if groups:
        groups[-1][1].extend(air)

    open_index = next((i for i, (_, rows) in enumerate(groups) if pointed in rows), None)
    shown: list = []
    for index, (lead, rows) in enumerate(groups):
        headed = any(not blank(choice) for choice in lead)
        expanded = index == open_index or not headed
        if expanded or index == 0 or (open_index is not None and index - 1 == open_index):
            shown.extend(lead)
        else:
            shown.extend(choice for choice in lead if not blank(choice))
        if expanded:
            shown.extend(rows)
    return shown


def menu(
    message: Framed,
    *,
    live_lines: Callable[[], Sequence[str]] | None = None,
    collapse: bool = False,
    hint: Callable[[object], str | None] | None = None,
    **kwargs,
):
    """A continuous main menu; separate content/action panes belong to steps.

    The status and choices share one window. Expand into spare bottom space
    before tightening empty gaps. Only a terminal too short for the complete
    menu scrolls, and then the whole page moves together.

    `collapse` draws only the cursor's group open and every other group as its
    heading alone (`collapsed`). It changes the DRAWING, never the list the
    keys walk: questionary's own up/down still step through every row in
    order, so moving past a group's last row opens the next group on its
    first row -- the cursor goes exactly where it went before, and the menu
    folds itself around it.

    `hint` names extra keys for the pointed row: handed the row's value, it
    returns a phrase for the help line (`←→ switch`) or None. And a caller
    that repaints a row after a key press does it through
    `question._probe_retitle(choice, title)`: every frame redraws the rows from
    their stored titles, so a title assigned straight onto the choice is gone
    by the next frame.
    """
    from prompt_toolkit.filters import to_filter
    from prompt_toolkit.layout import HSplit, Layout, ScrollOffsets, VSplit, Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.layout.dimension import Dimension
    from questionary import Separator

    question = select(message, **kwargs)
    control = checkbox_control(question)
    if control is None:
        return question
    app = question.application
    content = message.sections
    if live_lines is not None:
        def refresh_lines(_app):
            # Read once per frame, so sizing and painting use one consistent
            # snapshot even when several jobs advance while this menu is open.
            content["lines"] = list(live_lines())

        app.before_render += refresh_lines
        app.refresh_interval = 1.0
    original = control.text
    full_choices = list(control.choices)
    initial_indent = body_indent()
    titles = {choice: choice.title for choice in full_choices if not isinstance(choice, Separator)}

    def retitle(choice, title: str) -> None:
        # Stored at the indent the menu was BUILT with, which is what `tokens`
        # rewrites to the current one on every frame.
        titles[choice] = title.replace("\n" + body_indent(), "\n" + initial_indent)

    question._probe_retitle = retitle
    compact_choices = [
        choice for choice in full_choices
        if not (isinstance(choice, Separator) and not str(choice.title).strip())
    ]

    def width():
        return max(1, min(app.output.get_size().columns, left_pad() + CONTENT_WIDTH + 1))

    def tokens():
        # Choices carry continuation indentation from construction. Reflow it
        # alongside the status when the terminal width changes.
        control.pointer = pointer()
        pointed = control.get_pointed_at()
        for choice, title in titles.items():
            text = title.replace("\n" + initial_indent, "\n" + body_indent())
            style = getattr(choice, "probe_style", None)
            # A styled row is drawn as formatted text (questionary shows a list
            # title as given), bold while the cursor is on it like any row.
            choice.title = [(f"{style} bold" if choice is pointed else style, text)] if style else text
        text_width = max(1, min(CONTENT_WIDTH, width() - left_pad() - 1))
        body = [
            (line.style if isinstance(line, StyledLine) else "class:text", indent(part) + "\n")
            for line in content["lines"] for part in wrap(line, text_width)
        ]
        return [
            ("class:question", indent(content["title"]) + "\n\n"),
            *body,
            *([("class:text", "\n")] if body else []),
            ("class:question", indent(content["prompt"]) + "\n"),
            *original(),
        ]

    if collapse:
        walk = tokens

        def tokens():
            # Draw from the folded list, then put the walked list straight
            # back: `pointed_at` indexes whichever list is current, and the
            # key handlers between two paints must see the full one.
            every, at = control.choices, control.pointed_at
            pointed = every[at]
            shown = collapsed(every, pointed)
            control.choices, control.pointed_at = shown, shown.index(pointed)
            try:
                return walk()
            finally:
                control.choices, control.pointed_at = every, at

    control.text = tokens
    control.focusable = to_filter(True)

    def text_height(text):
        # Each density candidate needs fresh fragments: the live control caches
        # them for a whole render pass, including earlier sizing calls.
        measured = FormattedTextControl(text).create_content(width(), app.output.get_size().rows)
        return sum(
            measured.get_height_for_line(index, width(), None)
            for index in range(measured.line_count)
        )

    def footer_height():
        # The blank above the key hints, then the hints however many rows
        # they wrap to.
        return 1 + help_rows()[0][1].count("\n") + 1

    def preferred_height():
        return footer_height() + text_height(tokens)

    def fit_choices(maximum: int) -> int:
        pointed = control.get_pointed_at()
        for choices in (full_choices, compact_choices):
            control.choices = choices
            control.pointed_at = choices.index(pointed)
            preferred = preferred_height()
            if preferred <= maximum:
                break
        return preferred

    def body_height():
        available = question._probe_body_height()
        return max(1, min(preferred_height(), available) - footer_height())

    def help_parts() -> list[str]:
        # Words, not glyphs alone: this line is how someone who has never seen
        # the wizard learns that the arrows move through it. A hint that says
        # what Enter does replaces the plain `enter choose`.
        extra = hint(getattr(control.get_pointed_at(), "value", None)) if hint else None
        enter = None if extra and "enter" in extra else "enter choose"
        return ["↑ ↓ move", *(extra.split(" · ") if extra else []),
                *([enter] if enter else []), "esc back"]

    def help_rows():
        # Broken BETWEEN phrases, never inside one: "esc / to go back" across
        # two rows reads as two instructions.
        room = max(1, min(CONTENT_WIDTH, width() - left_pad() - 1))
        lines: list[str] = []
        for part in help_parts():
            if lines and len(lines[-1]) + 3 + len(part) <= room:
                lines[-1] += " · " + part
            else:
                lines.append(part)
        return [("class:instruction", "\n".join(indent(line) for line in lines))]

    window = Window(
        control, wrap_lines=True, always_hide_cursor=True,
        width=lambda: Dimension.exact(width()),
        height=lambda: Dimension.exact(body_height()),
        scroll_offsets=ScrollOffsets(
            bottom=lambda: max(0, text_height(body_indent() + plain_title(control.get_pointed_at().title)) - 1),
        ),
    )
    # The key hints sit on the window's LAST rows, under any spare space, so
    # they are in the same place however long the menu is at the moment.
    app.layout = Layout(HSplit([
        VSplit([window, Window()]),
        Window(height=Dimension(min=0, preferred=0, weight=1)),
        Window(height=1),
        Window(
            FormattedTextControl(help_rows),
            height=lambda: Dimension.exact(help_rows()[0][1].count("\n") + 1),
            wrap_lines=False,
        ),
    ]), focused_element=window)
    question._probe_continuous = True
    question._probe_fit_choices = fit_choices
    return question


def checkbox(message: str, **kwargs):
    """The same page layout with multi-selection and existing picker bindings."""
    import questionary

    question = questionary.checkbox(message, **kwargs)
    if isinstance(message, Framed):
        question._probe_content = {
            **message.sections,
            "instruction": "↑↓ choose · space toggle · enter · tab read · pgup/dn · esc back",
        }
    return question


def framed(title: str, lines: list[str], question: str, *, progress: str | None = None) -> str:
    """State block + question as ONE prompt message.

    Printing the state separately and letting questionary render underneath is
    what cut the top off: prompt_toolkit takes the screen after the print, and
    anything already emitted scrolls away. Handing it the whole block means it
    owns the layout and nothing can drift out of view.
    """
    header = [title, "", progress, ""] if progress is not None else [title, ""]
    block = [*header, *lines, "", question]
    padded = [(" " * left_pad() + ln if ln.strip() else "") for ln in block]
    # The first line rides behind the qmark, which already carries the indent.
    padded[0] = padded[0].lstrip()
    return Framed("\n".join(padded), title=title, lines=lines, prompt=question)


def qmark() -> str:
    """The `?` marker, carrying the indent itself.

    Padding the MESSAGE instead leaves the marker stranded at column 0 with its
    text 78 columns away, which is what shipped in 0.13.0 and looks like a
    rendering fault. questionary emits `(qmark)(space)(message)`, so putting the
    pad inside the marker moves the whole line together.
    """
    return " " * left_pad() + "?"


def pointer() -> str:
    """The `»` marker, likewise carrying the indent.

    questionary draws `" {pointer} "` on the highlighted row and
    `" " * (2 + len(pointer))` on the others, so a padded pointer keeps every
    row aligned -- selected and unselected end at the same column.
    """
    return " " * max(0, left_pad() - 1) + "»"


def body_indent() -> str:
    """Where a choice's continuation lines start -- and where its box starts.

    The pointer prefix only exists on the FIRST line of a choice; wrapped
    description lines get nothing, so they carry their own pad.

    Derived from `pointer()` rather than from `left_pad()` directly, because
    what a continuation line has to line up with is the column questionary
    actually starts a title on: `" {pointer} "` / `" " * (2 + len(pointer))`.
    Those agree with `left_pad() + 2` on every terminal wide enough to have a
    left pad -- and disagree by one on a terminal too narrow for one, since the
    pointer cannot be shorter than the `»` in it. That was a cosmetic
    one-column drift while nothing was drawn in the gap; it is a rectangle with
    a rail out of true now, so the two are the same number.
    """
    return " " * (2 + len(pointer()))


#: Columns every choice row gives up on its left so the selection rectangle has
#: a rail to sit in. Spent on EVERY row, pointed or not: a gutter that only
#: appeared under the cursor would shift a row's text two columns sideways the
#: moment you arrowed onto it, and a menu whose text jumps as you read it is
#: worse than one carrying two columns of air.
BOX_GUTTER = 2


def box_width() -> int:
    """How wide the selection rectangle is, rails included.

    The rectangle starts where a choice's text starts -- the column
    `body_indent()` names -- and runs to the right edge of the same
    CONTENT_WIDTH block every other screen is centred in, so a boxed row is
    exactly as wide as the paragraph above it.

    Floored at 24 and clamped to what is left of the terminal AFTER that
    starting column: a rectangle whose edge runs past the last column wraps
    back to column 0 and stops reading as a rectangle at all, which is exactly
    what a screen too narrow to have a left pad produced.
    """
    return max(24, min(CONTENT_WIDTH - BOX_GUTTER, columns() - len(body_indent())))


def box_edge(width: int, *, lead: int = 0, top: bool = True) -> str:
    """The `┌────┐` (or `└────┘`) row of a selection rectangle.

    Returned WITHOUT the choice prefix, because the row it goes in is a
    questionary Separator and questionary already draws
    `" " * (2 + len(pointer))` in front of one -- the same prefix an unpointed
    choice title gets. That is what lets the rectangle's top and bottom live in
    the blank separator rows either side of a row instead of in the row itself:
    the box costs no extra lines, so nothing below it moves when the cursor
    arrives.

    `lead` insets the rectangle from that origin, for the nav band -- whose two
    halves sit at opposite ends of one row and are boxed one at a time.
    """
    width = max(2, width)
    left, right = ("┌", "┐") if top else ("└", "┘")
    return " " * max(0, lead) + left + "─" * (width - 2) + right


def box_rails(lines: Sequence[str], width: int) -> list[str]:
    """Put `│ … │` down both sides of the row the cursor is on.

    Every line is padded out so the right rail lands in ONE column across a
    multi-line choice. A line too long for the box keeps its text and loses
    that rail rather than being cut: the text is the half carrying meaning, and
    on the capture row the half that would disappear is the clause naming where
    the data goes.

    A row with ONE field, which is every row but the nav band -- the band's two
    ends share a line and are boxed one at a time, so it composes its own row
    in `setup.nav_layout` and only borrows `box_edge` from here.
    """
    room = max(1, width - 2 - BOX_GUTTER)
    return [
        f"│ {line}" if len(line) > room else f"│ {line.ljust(room)} │" for line in lines
    ]


def box_gutter(lines: Sequence[str]) -> list[str]:
    """The same rows with the rail column left BLANK -- an unpointed row.

    The counterpart to `box_rails`, and the reason `BOX_GUTTER` is not free:
    both have to be applied to their respective rows, or a row's text sits two
    columns left of every other row's right up until you point at it.
    """
    return [f"{' ' * BOX_GUTTER}{line}" for line in lines]


def heading(title: str) -> str:
    """`Install/update/uninstall`: the label above a group of choices.

    The title alone, in the heading colour. It used to be led by two dashes,
    and before that ruled out to 46 columns; both were chrome competing with
    the handful of lines that are the actual menu. The colour says "this names
    what follows", and the blank line above it does the separating.

    A questionary Separator is drawn with the SAME prefix a choice title gets
    (`" " * (2 + len(pointer))`, see `common.InquirerControl._get_choice_tokens`),
    so a heading built here lines up with the rows it introduces instead of
    floating at column 0 while they sit indented.
    """
    return title


def bind_step_keys(question, *, on_back=None, on_next=None):
    """Left/Right as the wizard's step nav, alongside `bind_escape`.

    A visible `‹ Back` / `Next ›` band is what makes the way through a step
    discoverable, but travelling UP to it past every choice to leave is worse
    than the invisible Escape it replaced. The arrows mean the band can be read
    as a label -- these keys do this -- rather than a place you have to go.

    Left and Right are otherwise unclaimed on both prompts we use: questionary
    binds Up/Down (and j/k, and Ctrl-N/P) for movement, and its catch-all
    `Keys.Any` handler loses to anything registered later, because
    prompt_toolkit resolves a key with `matches[-1]`.

    Guarded like every other reach into the library: a prompt that renders with
    one fewer shortcut beats a wizard that cannot ask the question at all.
    """
    try:
        bindings = question.application.key_bindings

        if on_back is not None:

            @bindings.add("left", eager=True)
            def _(event) -> None:  # pragma: no cover - requires a live terminal
                on_back(event)

        if on_next is not None:

            @bindings.add("right", eager=True)
            def _(event) -> None:  # pragma: no cover - requires a live terminal
                on_next(event)

    except Exception:  # noqa: BLE001 - never let a binding break the prompt
        pass
    return question


def point_at(control, predicate) -> None:
    """Park the cursor on the first row `predicate` accepts.

    Load-bearing again. questionary seats the cursor on whichever selectable
    row comes first, which was harmless while the nav band was a Separator it
    would skip; the band takes the cursor now, and where a step OPENS is a
    product decision -- on `Next ›`, so continuing costs one keystroke and the
    options are reached by going deliberately up -- not something to inherit
    from the library's iteration order.
    """
    try:
        for index, choice in enumerate(control.choices):
            if getattr(choice, "disabled", None):
                continue
            if predicate(getattr(choice, "value", None)):
                control.pointed_at = index
                return
    except Exception:  # noqa: BLE001 - a cursor in the wrong place is not a crash
        pass


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
    """
    if not interactive():
        yield
        return
    import itertools
    import threading

    frames = itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
    stop = threading.Event()
    header = onboarding_header()
    output = sys.stdout
    size = None
    status_row = 1

    def paint() -> None:
        nonlocal size, status_row
        height, width = max(1, rows()), max(1, columns())
        margin = safe_margin(height)
        pinned = header_lines(header)[:max(0, height - 2 * margin - 2)]
        first = margin + len(pinned) + (1 if pinned else 0)
        last = max(first, height - margin - 1)
        status_row = (first + last) // 2 + 1
        line = f"{next(frames)} {' '.join(label.split())}"
        room = max(1, min(CONTENT_WIDTH, width - 1))
        if len(line) > room:
            line = line[:room - 1] + "…"
        pad = max(0, (width - len(line)) // 2)
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
        output.write(prefix + f"\033[?25l\033[{status_row};1H\033[2K{' ' * pad}{line}\033[K")
        output.flush()
        size = (height, width)

    def spin() -> None:
        while not stop.wait(0.08):
            try:
                paint()
            except Exception:  # noqa: BLE001 - a dead stdout must not kill the thread loudly
                return

    thread = None
    try:
        try:
            paint()
            thread = threading.Thread(target=spin, daemon=True)
            thread.start()
        except Exception:  # noqa: BLE001 - no spinner beats no work
            thread = None
        yield
    finally:
        try:
            stop.set()
            if thread is not None:
                try:
                    thread.join(timeout=0.5)
                except RuntimeError:
                    pass  # interrupted before the thread started
        finally:
            try:
                output.write(f"\033[{status_row};1H\033[2K\033[?25h")
                output.flush()
            except Exception:  # noqa: BLE001
                pass


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
    ) -> None:
        # `overall` maps this agent's resolved tasks into the containing install
        # flow. Other callers keep the ordinary task counter.
        self._title = title
        self._steps = list(steps)
        self._state = [_PENDING] * len(steps)
        self._results: list[str] = []
        self._next: list[str] = []
        self._queued: list[str] = []
        self._overall = overall

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

    def bar(self) -> str:
        total = len(self._steps) or 1
        return f"{progress_bar(self._done() / total, width=_BAR_WIDTH)}  {self._done()}/{total}"

    def block(self) -> list[str]:
        if self._overall is not None:
            fraction = self._done() / len(self._steps) if self._steps else 1.0
            lines = [*self._overall(fraction), "", self._title, ""]
        else:
            lines = [self._title, self.bar(), ""]
        lines += [
            f"  {_MARKS[state]} {step}"
            for step, state in zip(self._steps, self._state, strict=False)
        ]
        if self._results:
            lines += ["", "What changed:", *(f"  - {line}" for line in self._results)]
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
        if self._overall is not None:
            page(block[3:], progress=block[:2])
        else:
            page(block)

    def close(self) -> None:
        """Leave the finished screen on display, results and all."""
        self.render()
