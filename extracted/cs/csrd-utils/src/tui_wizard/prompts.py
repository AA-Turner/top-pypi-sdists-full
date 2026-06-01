"""Interactive prompt helpers: text, yes/no, single-select, multi-select."""

import sys

from .exceptions import GoBack
from .terminal import cbreak_mode, is_tty, read_char, read_escape_seq

# ---------------------------------------------------------------------------
# Text input
# ---------------------------------------------------------------------------


def _tty_line_input(display_prompt: str) -> str:
    """Read a line of text in cbreak mode with Escape / Ctrl-C support.

    Handles printable characters, backspace, Enter, Escape, and Ctrl-C.
    Raises ``GoBack`` on Escape, ``KeyboardInterrupt`` on Ctrl-C.
    Returns the entered string on Enter.
    """

    buf: list[str] = []
    sys.stdout.write(display_prompt)
    sys.stdout.flush()

    with cbreak_mode() as fd:
        if fd is None:
            raise RuntimeError("cbreak unavailable")

        while True:
            ch = read_char(fd)
            if ch in {"\r", "\n"}:
                sys.stdout.write("\n")
                sys.stdout.flush()
                return "".join(buf)
            if ch == "\x03":
                sys.stdout.write("\n")
                sys.stdout.flush()
                raise KeyboardInterrupt
            if ch == "\x1b":
                seq = read_escape_seq(fd)
                if seq == "ESC":
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    raise GoBack
                # Ignore arrow keys in text input
            elif ch in {"\x7f", "\x08"}:
                if buf:
                    buf.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            elif ch >= " ":
                buf.append(ch)
                sys.stdout.write(ch)
                sys.stdout.flush()


def prompt_text(question: str, *, default: str = "") -> str:
    """Prompt the user for a text value.

    Returns *default* when the user submits an empty answer.
    Raises ``GoBack`` on Escape, ``KeyboardInterrupt`` on Ctrl-C,
    and returns *default* on EOF.
    """

    hint = f" [{default}]" if default else ""
    display = f"{question}{hint}: "

    if is_tty():
        try:
            answer = _tty_line_input(display).strip()
        except EOFError:
            return default
        return answer or default

    try:
        answer = input(display).strip()
    except EOFError:
        return default
    if answer.lower() in {"back", "b"}:
        raise GoBack
    return answer or default


def prompt_yes_no(question: str, *, default: bool = True) -> bool:
    """Prompt the user with a yes/no question.

    Returns *default* when the user submits an empty answer.
    Raises ``GoBack`` on Escape, ``KeyboardInterrupt`` on Ctrl-C.
    On ``EOFError`` returns ``False``.
    """

    hint = "Y/n" if default else "y/N"
    display = f"{question} ({hint}): "

    if is_tty():
        try:
            answer = _tty_line_input(display).strip().lower()
        except EOFError:
            return False
        if not answer:
            return default
        return answer in {"y", "yes", "true", "1"}

    try:
        answer = input(display).strip().lower()
    except EOFError:
        return False
    if not answer:
        return default
    return answer in {"y", "yes", "true", "1"}


# ---------------------------------------------------------------------------
# Single-select
# ---------------------------------------------------------------------------


def prompt_single_select(
    prompt: str,
    options: list[str],
    *,
    auto_select: bool = True,
    disabled: set[int] | None = None,
    inline: bool = False,
) -> str | None:
    """Interactive single-select: arrow keys to move, Enter to confirm.

    Falls back to numbered input in non-TTY contexts.
    Returns the selected option or ``None`` on cancel/empty.
    Raises ``GoBack`` when the user presses Escape.

    When *auto_select* is ``True`` (default) and only one **enabled** option
    exists, it is selected automatically without showing a list.  Set to
    ``False`` when the user should always see the options.

    *disabled* is a set of indices into *options* that are shown grayed out
    and cannot be selected.  The cursor skips them.

    When *inline* is ``True``, the TTY menu renders below the current
    cursor position without clearing the screen.  Use this for
    sub-prompts that fire mid-step so surrounding context stays visible.
    """

    if not options:
        return None

    disabled = disabled or set()
    enabled_indices = [i for i in range(len(options)) if i not in disabled]

    if not enabled_indices:
        return None

    if auto_select and len(enabled_indices) == 1:
        idx = enabled_indices[0]
        print(f"{prompt} {options[idx]}")
        return options[idx]

    if not is_tty():
        return _single_select_non_tty(prompt, options, disabled=disabled)

    with cbreak_mode() as fd:
        if fd is None:
            return _single_select_non_tty(prompt, options, disabled=disabled)

        cursor = enabled_indices[0]
        render = _render_single_select_inline if inline else _render_single_select
        total_lines = render(prompt, options, cursor, disabled=disabled, _first=True)
        while True:
            ch = read_char(fd)
            if ch in {"\r", "\n"} and cursor not in disabled:
                break
            if ch == "\x03":
                sys.stdout.write("\r\n")
                sys.stdout.flush()
                raise KeyboardInterrupt
            if ch == "\x1b":
                seq = read_escape_seq(fd)
                if seq == "ESC":
                    if inline:
                        # Erase the inline menu
                        sys.stdout.write(f"\x1b[{total_lines}A\x1b[J")
                        sys.stdout.flush()
                    else:
                        sys.stdout.write("\x1b[2J\x1b[H")
                        sys.stdout.flush()
                    raise GoBack
                if seq == "UP":
                    pos = enabled_indices.index(cursor) if cursor in enabled_indices else 0
                    pos = (pos - 1) % len(enabled_indices)
                    cursor = enabled_indices[pos]
                    render(prompt, options, cursor, disabled=disabled, _total=total_lines)
                elif seq == "DOWN":
                    pos = enabled_indices.index(cursor) if cursor in enabled_indices else 0
                    pos = (pos + 1) % len(enabled_indices)
                    cursor = enabled_indices[pos]
                    render(prompt, options, cursor, disabled=disabled, _total=total_lines)

    if inline:
        # Erase the inline menu, print selection as a one-liner
        sys.stdout.write(f"\x1b[{total_lines}A\x1b[J")
        sys.stdout.write(f"{prompt} {options[cursor]}\r\n")
        sys.stdout.flush()
    else:
        sys.stdout.write("\x1b[2J\x1b[H")
        sys.stdout.flush()
    return options[cursor]


def _render_single_select(
    prompt: str,
    options: list[str],
    cursor: int,
    *,
    disabled: set[int] | None = None,
    _first: bool = False,
    _total: int = 0,
) -> int:
    """Draw the single-select list in full-screen cbreak mode."""

    disabled = disabled or set()
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.write(f"{prompt}\r\n")
    sys.stdout.write("(↑/↓ move, Enter confirm, Esc back)\r\n\r\n")
    lines = 3
    for idx, option in enumerate(options):
        pointer = ">" if idx == cursor else " "
        if idx in disabled:
            sys.stdout.write(f" {pointer} \x1b[2m{option}\x1b[0m\r\n")
        else:
            sys.stdout.write(f" {pointer} {option}\r\n")
        lines += 1
    sys.stdout.flush()
    return lines


def _render_single_select_inline(
    prompt: str,
    options: list[str],
    cursor: int,
    *,
    disabled: set[int] | None = None,
    _first: bool = False,
    _total: int = 0,
) -> int:
    """Draw the single-select list inline (no screen clear).

    On first render, prints below the current cursor.  On re-render,
    moves the cursor up to overwrite the previous menu area.
    """

    disabled = disabled or set()
    total_lines = len(options) + 3  # prompt + hint + blank + options
    if not _first:
        # Move up to start of menu and clear
        sys.stdout.write(f"\x1b[{_total}A\x1b[J")
    sys.stdout.write(f"{prompt}\r\n")
    sys.stdout.write("(↑/↓ move, Enter confirm, Esc back)\r\n\r\n")
    for idx, option in enumerate(options):
        pointer = ">" if idx == cursor else " "
        if idx in disabled:
            sys.stdout.write(f" {pointer} \x1b[2m{option}\x1b[0m\r\n")
        else:
            sys.stdout.write(f" {pointer} {option}\r\n")
    sys.stdout.flush()
    return total_lines


def _single_select_non_tty(
    prompt: str,
    options: list[str],
    *,
    disabled: set[int] | None = None,
) -> str | None:
    """Numbered fallback for non-TTY single-select."""

    disabled = disabled or set()
    print(prompt)
    for idx, option in enumerate(options, start=1):
        if (idx - 1) in disabled:
            print(f"  {idx}) {option}  [disabled]")
        else:
            print(f"  {idx}) {option}")
    print("  0) back")

    try:
        raw = input("Select [1]: ").strip()
    except EOFError:
        return None

    if raw.lower() in {"0", "back", "b"}:
        raise GoBack

    enabled_indices = [i for i in range(len(options)) if i not in disabled]
    if not raw:
        return options[enabled_indices[0]] if enabled_indices else None
    if raw.isdigit():
        idx = int(raw) - 1
        if 0 <= idx < len(options) and idx not in disabled:
            return options[idx]
    lower = raw.lower()
    for opt in options:
        if opt.lower() == lower:
            return opt
    return None


# ---------------------------------------------------------------------------
# Multi-select
# ---------------------------------------------------------------------------


def prompt_multi_select(
    prompt: str,
    options: list[str],
    *,
    disabled: set[int] | None = None,
    inline: bool = False,
    auto_select_on_enter: bool = False,
) -> list[str]:
    """Interactive multi-select: spacebar toggles, Enter confirms.

    Falls back to comma-separated numeric input in non-TTY contexts.
    Returns the selected option values (empty list if none selected).
    Raises ``KeyboardInterrupt`` on Ctrl-C and ``GoBack`` on Escape.

    *disabled* is a set of indices into *options* that are shown grayed
    out and cannot be toggled.  The cursor skips them.

    When *inline* is ``True``, the TTY menu renders below the current
    cursor position without clearing the screen.  Use this for
    sub-prompts that fire mid-step so surrounding context stays visible.

    When *auto_select_on_enter* is ``True``, pressing Enter with nothing
    toggled auto-selects the highlighted item.  Use this for prompts
    where "pick exactly this one" is the common intent (e.g. capabilities).
    When ``False`` (default), Enter with nothing toggled returns an empty
    list — appropriate for optional prompts where "none" is valid.
    """

    if not options:
        return []

    disabled = disabled or set()
    enabled_indices = [i for i in range(len(options)) if i not in disabled]

    if not enabled_indices:
        return []

    if not is_tty():
        return _multi_select_non_tty(prompt, options, disabled=disabled)

    with cbreak_mode() as fd:
        if fd is None:
            return _multi_select_non_tty(prompt, options, disabled=disabled)

        selected: set[int] = set()
        cursor = enabled_indices[0]

        render = _render_multi_select_inline if inline else _render_multi_select
        total_lines = render(prompt, options, selected, cursor, disabled=disabled, _first=True)
        while True:
            ch = read_char(fd)
            if ch in {"\r", "\n"}:
                # When auto_select_on_enter is set and nothing was toggled,
                # treat Enter as "select highlighted item and confirm".
                # Otherwise Enter with nothing toggled = empty selection.
                if not selected and auto_select_on_enter and cursor not in disabled:
                    selected.add(cursor)
                break
            if ch == "\x03":
                sys.stdout.write("\r\n")
                sys.stdout.flush()
                raise KeyboardInterrupt
            if ch == " " and cursor not in disabled:
                selected.symmetric_difference_update({cursor})
                render(prompt, options, selected, cursor, disabled=disabled, _total=total_lines)
            elif ch == "\x1b":
                seq = read_escape_seq(fd)
                if seq == "ESC":
                    if inline:
                        sys.stdout.write(f"\x1b[{total_lines}A\x1b[J")
                        sys.stdout.flush()
                    else:
                        sys.stdout.write("\x1b[2J\x1b[H")
                        sys.stdout.flush()
                    raise GoBack
                if seq == "UP":
                    pos = enabled_indices.index(cursor) if cursor in enabled_indices else 0
                    pos = (pos - 1) % len(enabled_indices)
                    cursor = enabled_indices[pos]
                    render(prompt, options, selected, cursor, disabled=disabled, _total=total_lines)
                elif seq == "DOWN":
                    pos = enabled_indices.index(cursor) if cursor in enabled_indices else 0
                    pos = (pos + 1) % len(enabled_indices)
                    cursor = enabled_indices[pos]
                    render(prompt, options, selected, cursor, disabled=disabled, _total=total_lines)

    if inline:
        # Erase inline menu, print compact summary
        sys.stdout.write(f"\x1b[{total_lines}A\x1b[J")
        chosen = [options[i] for i in sorted(selected)]
        if chosen:
            short = ", ".join(c.split(" — ")[0] for c in chosen)
            sys.stdout.write(f"{prompt} {short}\r\n")
        else:
            sys.stdout.write(f"{prompt} (none)\r\n")
        sys.stdout.flush()
    else:
        sys.stdout.write("\x1b[2J\x1b[H")
        sys.stdout.flush()
    return [options[i] for i in sorted(selected)]


def _render_multi_select(
    prompt: str,
    options: list[str],
    selected: set[int],
    cursor: int,
    *,
    disabled: set[int] | None = None,
    _first: bool = False,
    _total: int = 0,
) -> int:
    """Draw the multi-select list in full-screen cbreak mode."""

    disabled = disabled or set()
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.write(f"{prompt}\r\n")
    sys.stdout.write("(↑/↓ move, Space toggle, Enter confirm, Esc back)\r\n\r\n")
    lines = 3
    for idx, option in enumerate(options):
        pointer = ">" if idx == cursor else " "
        check = "●" if idx in selected else "○"
        if idx in disabled:
            sys.stdout.write(f" {pointer} \x1b[2m{check} {option}\x1b[0m\r\n")
        else:
            sys.stdout.write(f" {pointer} {check} {option}\r\n")
        lines += 1
    sys.stdout.flush()
    return lines


def _render_multi_select_inline(
    prompt: str,
    options: list[str],
    selected: set[int],
    cursor: int,
    *,
    disabled: set[int] | None = None,
    _first: bool = False,
    _total: int = 0,
) -> int:
    """Draw the multi-select list inline (no screen clear)."""

    disabled = disabled or set()
    total_lines = len(options) + 3
    if not _first:
        sys.stdout.write(f"\x1b[{_total}A\x1b[J")
    sys.stdout.write(f"{prompt}\r\n")
    sys.stdout.write("(↑/↓ move, Space toggle, Enter confirm, Esc back)\r\n\r\n")
    for idx, option in enumerate(options):
        pointer = ">" if idx == cursor else " "
        check = "●" if idx in selected else "○"
        if idx in disabled:
            sys.stdout.write(f" {pointer} \x1b[2m{check} {option}\x1b[0m\r\n")
        else:
            sys.stdout.write(f" {pointer} {check} {option}\r\n")
    sys.stdout.flush()
    return total_lines


def _multi_select_non_tty(
    prompt: str,
    options: list[str],
    *,
    disabled: set[int] | None = None,
) -> list[str]:
    """Comma-separated numeric fallback for non-TTY multi-select."""

    disabled = disabled or set()
    print(prompt)
    for idx, option in enumerate(options, start=1):
        suffix = " [disabled]" if (idx - 1) in disabled else ""
        print(f"  {idx}) {option}{suffix}")
    print("  0) back")
    print()

    try:
        raw = input("Select (comma-separated numbers, 'all', or 'back'): ").strip().lower()
    except EOFError:
        return []

    if raw in {"0", "back", "b"}:
        raise GoBack

    if raw in {"all", "*"}:
        return [options[i] for i in range(len(options)) if i not in disabled]
    if not raw:
        return []

    result: list[str] = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            idx = int(part) - 1
            if 0 <= idx < len(options) and idx not in disabled and options[idx] not in result:
                result.append(options[idx])
    return result
