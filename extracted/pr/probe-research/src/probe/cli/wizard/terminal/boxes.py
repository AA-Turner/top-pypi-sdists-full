"""draw selection boxes and repaint questionary's checkbox control: own boxes, rails and edges, a dimmed Back, hidden pointers, headings."""

from __future__ import annotations
from collections.abc import Sequence


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
from probe.cli.wizard.terminal.choices import body_indent  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.terminal import CONTENT_WIDTH, columns  # noqa: E402 -- pieces need each other; the front door loads this one first
