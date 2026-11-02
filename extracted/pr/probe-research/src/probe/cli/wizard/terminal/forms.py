"""the installer's full-screen prompts: the sectioned layout, the review page, text and secret inputs, Escape and step keys."""

from __future__ import annotations
from collections.abc import Callable, Sequence
from probe.cli.wizard.terminal.terminal import BACK, CONTENT_WIDTH, MARGIN, interactive, left_pad


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
            [fragment for fragment in row if fragment[0] != ZERO_WIDTH_ESCAPE]
            for line in current for row in line_rows(line, width)
        ]
        line_styles[:] = rendered
        return "\n".join("".join(text for _, text in row) for row in rendered)

    class LineLexer(Lexer):
        def lex_document(self, document):
            def get_line(index):
                return line_styles[index] if index < len(line_styles) else [("", document.lines[index])]
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


def secret(title: str, lines: Sequence[str], prompt: str):
    """`text`, with what is typed hidden: an API key never shows on screen or
    in the terminal's scrollback."""
    if not interactive():
        page([title, *lines])
        return None
    import questionary

    question = questionary.password(prompt, style=style(), qmark=qmark())
    sectioned(
        question, title=title, lines=lines, prompt=prompt,
        instruction="paste or type · enter · esc back",
    )
    return ask(question)


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
from probe.cli.wizard.terminal.boxes import checkbox_control  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.choices import pointer, qmark  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.clipboard import _copy_to_clipboard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.layout import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    ZERO_WIDTH_ESCAPE,
    center_vertically,
    indent,
    line_rows,
    page,
    plain_title,
    style,
)
