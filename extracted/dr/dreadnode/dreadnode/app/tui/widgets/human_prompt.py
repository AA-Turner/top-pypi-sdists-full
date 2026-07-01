"""Inline widget for ``ask_user`` prompts (single question or bundle).

Renders a ``HumanPrompt`` with one or more ``HumanQuestion`` entries.
Each question is either ``kind="choice"`` (option list with optional
inline-typeable last row when ``custom=True``) or ``kind="input"`` (a
bordered editor mirroring the composer's ``> ___`` style). For bundles
a tab strip at the top shows progress and lets the user move between
questions.

Per-``request_id`` drafts (selections, typed text, current tab index)
live in a module-scope dict so switching sessions or replaying a
snapshot does not lose work in progress. The cache is cleared on
terminal action (submit / cancel / turn-abort).

Keys: ``↑↓`` navigate · ``Enter`` selects/submits · ``Space`` toggles
in multi-select · ``Tab``/``Shift+Tab`` moves between bundle questions
· ``Esc`` cancels. On the inline type row (choice + ``custom=True``),
printable characters append to the typed answer and ``Backspace``
deletes — ``Up``/``Down`` still navigate.
"""

import typing as t
from dataclasses import dataclass, field

from rich.markup import escape as rich_escape
from textual import events
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import Input, Static

from dreadnode.app.api.models import HumanPrompt, HumanQuestion, QuestionAnswer
from dreadnode.app.tui.theme import ACCENT, BG, BORDER, FG, FG_MUTED, FG_SUBTLE

_PLACEHOLDER = "Type your answer…"


@dataclass(slots=True)
class _QuestionDraft:
    """Per-question state preserved across session-switch / snapshot replay."""

    cursor: int = 0
    selected_labels: list[str] = field(default_factory=list)
    typed_text: str = ""


@dataclass(slots=True)
class _PromptDraft:
    """Per-``request_id`` state."""

    tab_index: int = 0
    questions: dict[int, _QuestionDraft] = field(default_factory=dict)

    def for_question(self, idx: int) -> _QuestionDraft:
        if idx not in self.questions:
            self.questions[idx] = _QuestionDraft()
        return self.questions[idx]


_DRAFT_CACHE: dict[str, _PromptDraft] = {}


def clear_draft(request_id: str) -> None:
    """Drop the cached draft for ``request_id`` (called on terminal action)."""
    _DRAFT_CACHE.pop(request_id, None)


def _has_type_row(question: HumanQuestion) -> bool:
    return question.kind == "choice" and question.custom


def _has_submit_row(question: HumanQuestion) -> bool:
    """Multi-select needs an explicit submit affordance — Enter on a real option toggles."""
    return question.kind == "choice" and question.multiple


def _type_row_index(question: HumanQuestion) -> int | None:
    if not _has_type_row(question):
        return None
    return len(question.options)


def _submit_row_index(question: HumanQuestion) -> int | None:
    if not _has_submit_row(question):
        return None
    return len(question.options) + (1 if _has_type_row(question) else 0)


def _option_count(question: HumanQuestion) -> int:
    """Total navigable rows: real options + optional inline type row + optional submit row."""
    extras = (1 if _has_type_row(question) else 0) + (1 if _has_submit_row(question) else 0)
    return len(question.options) + extras


def _is_type_row(question: HumanQuestion, idx: int) -> bool:
    return _type_row_index(question) == idx


def _is_submit_row(question: HumanQuestion, idx: int) -> bool:
    return _submit_row_index(question) == idx


def _question_is_answered(question: HumanQuestion, draft: _QuestionDraft) -> bool:
    if question.kind == "input":
        return bool(draft.typed_text.strip())
    return bool(draft.typed_text.strip()) or bool(draft.selected_labels)


def _build_answer(question: HumanQuestion, draft: _QuestionDraft) -> QuestionAnswer:
    if question.kind == "input":
        return QuestionAnswer(text=draft.typed_text.strip(), was_custom=True)
    typed = draft.typed_text.strip()
    if typed:
        return QuestionAnswer(custom_text=typed, was_custom=True)
    return QuestionAnswer(selected_labels=list(draft.selected_labels))


class HumanPromptWidget(Static):
    """Multi-question agent prompt widget.

    Owns the answer surface end-to-end: composer is expected to be
    disabled by the host while a prompt is active, and Submit / Cancel
    come exclusively from this widget's keyboard shortcuts.
    """

    DEFAULT_CSS = f"""
    HumanPromptWidget {{
        display: none;
        height: auto;
        padding: 0 2;
        background: transparent;
        border-top: hkey {BORDER};
        border-bottom: hkey {BORDER};
    }}
    HumanPromptWidget.-active {{
        display: block;
    }}
    HumanPromptWidget #hp-tabs {{
        height: auto;
        margin-bottom: 1;
    }}
    HumanPromptWidget #hp-tabs.-hidden {{
        display: none;
    }}
    HumanPromptWidget #hp-prompt {{
        height: auto;
        margin-bottom: 1;
        text-style: bold;
        color: {FG};
    }}
    HumanPromptWidget #hp-options {{
        height: auto;
    }}
    HumanPromptWidget #hp-options.-hidden {{
        display: none;
    }}
    HumanPromptWidget #hp-input-bar {{
        height: 3;
        margin-top: 0;
        padding: 0 1;
        background: {BG};
        border: solid {BORDER};
    }}
    HumanPromptWidget #hp-input-bar.-hidden {{
        display: none;
    }}
    HumanPromptWidget #hp-input-bar:focus-within {{
        border: solid {ACCENT};
    }}
    HumanPromptWidget #hp-input-char {{
        width: 2;
        height: 1;
        color: {ACCENT};
        background: transparent;
        padding: 0;
        content-align: left middle;
    }}
    HumanPromptWidget #hp-input-field {{
        border: none;
        background: transparent;
        color: {FG};
        height: 1;
        padding: 0;
        width: 1fr;
    }}
    HumanPromptWidget #hp-input-field:focus {{
        border: none;
        background: transparent;
    }}
    HumanPromptWidget #hp-hint {{
        height: auto;
        color: {FG_MUTED};
        margin-top: 1;
    }}
    """

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("escape", "cancel", "Cancel", show=False),
    ]

    class Submit(Message):
        """Posted when the user submits a complete bundle."""

        def __init__(self, request_id: str, answers: list[QuestionAnswer]) -> None:
            self.request_id = request_id
            self.answers = answers
            super().__init__()

    class Cancel(Message):
        """Posted when the user cancels the prompt."""

        def __init__(self, request_id: str) -> None:
            self.request_id = request_id
            super().__init__()

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)
        self.can_focus = True
        self._prompt: HumanPrompt | None = None
        self._draft: _PromptDraft | None = None

    def compose(self) -> ComposeResult:
        yield Static("", id="hp-tabs")
        yield Static("", id="hp-prompt")
        yield Static("", id="hp-options")
        yield Horizontal(
            Static("> ", id="hp-input-char"),
            Input(id="hp-input-field"),
            id="hp-input-bar",
            classes="-hidden",
        )
        yield Static("", id="hp-hint")

    @property
    def is_active(self) -> bool:
        return self.has_class("-active")

    def show_prompt(self, prompt: HumanPrompt) -> None:
        """Display the prompt; restore any draft cached for this request_id."""
        self._prompt = prompt
        self._draft = _DRAFT_CACHE.setdefault(prompt.request_id, _PromptDraft())
        self.add_class("-active")
        self._refresh_view()
        self._sync_focus()

    def hide_prompt(self) -> None:
        self.remove_class("-active")
        self._prompt = None
        self._draft = None

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _active_question(self) -> tuple[int, HumanQuestion]:
        assert self._prompt is not None
        assert self._draft is not None
        idx = self._draft.tab_index
        idx = max(0, min(idx, len(self._prompt.questions) - 1))
        self._draft.tab_index = idx
        return idx, self._prompt.questions[idx]

    def _refresh_view(self) -> None:
        if self._prompt is None or self._draft is None:
            return

        self._render_tabs()
        idx, question = self._active_question()
        self.query_one("#hp-prompt", Static).update(question.prompt)
        self._render_options(question, self._draft.for_question(idx))
        self._render_input(question, self._draft.for_question(idx))
        self._render_hint(question)

    def _sync_focus(self) -> None:
        """For input-only questions, focus the editor; otherwise focus the widget."""
        if self._prompt is None or self._draft is None:
            return
        _, question = self._active_question()
        if question.kind == "input":
            self.query_one("#hp-input-field", Input).focus()
        else:
            self.focus()

    def _render_tabs(self) -> None:
        assert self._prompt is not None
        assert self._draft is not None
        tabs = self.query_one("#hp-tabs", Static)
        if len(self._prompt.questions) <= 1:
            tabs.add_class("-hidden")
            tabs.update("")
            return
        tabs.remove_class("-hidden")

        parts: list[str] = []
        for i, q in enumerate(self._prompt.questions):
            answered = _question_is_answered(q, self._draft.for_question(i))
            marker = "✓" if answered else "○"
            label = q.header or f"Q{i + 1}"
            chip = f"{marker} {label}"
            if i == self._draft.tab_index:
                parts.append(f"[bold {ACCENT}]{chip}[/]")
            elif answered:
                parts.append(f"[{FG_SUBTLE}]{chip}[/]")
            else:
                parts.append(f"[{FG_MUTED}]{chip}[/]")

        all_answered = all(
            _question_is_answered(q, self._draft.for_question(i))
            for i, q in enumerate(self._prompt.questions)
        )
        submit = f"[bold {ACCENT}]→ Submit[/]" if all_answered else f"[{FG_MUTED}]→ Submit[/]"
        parts.append(submit)

        tabs.update("   ".join(parts))

    def _render_options(self, question: HumanQuestion, draft: _QuestionDraft) -> None:
        options = self.query_one("#hp-options", Static)
        if question.kind != "choice":
            options.add_class("-hidden")
            options.update("")
            return
        options.remove_class("-hidden")

        n_total = _option_count(question)
        # Right-align option numbers when there are 10+ options.
        width = max(2, len(str(n_total)) + 1)
        lines: list[str] = []

        for i, opt in enumerate(question.options):
            is_active = i == draft.cursor
            picked = opt.label in draft.selected_labels

            cursor_glyph = (
                f"[bold {ACCENT}]›[/]" if is_active else " "  # noqa: RUF001
            )
            number_text = f"{i + 1}.".rjust(width)
            number = f"[{ACCENT}]{number_text}[/]" if is_active else f"[{FG_MUTED}]{number_text}[/]"

            if question.multiple:
                # Escape the open bracket so Rich doesn't parse \[x] as markup.
                checkbox = r"\[✓]" if picked else r"\[ ]"
                checkbox_color = ACCENT if picked else FG_MUTED
                checkbox_render = f"[{checkbox_color}]{checkbox}[/]"
                label_render = (
                    f"[bold {FG}]{rich_escape(opt.label)}[/]"
                    if is_active
                    else f"[{FG}]{rich_escape(opt.label)}[/]"
                )
                head = f"{cursor_glyph} {number} {checkbox_render} {label_render}"
                desc_indent = " " * (1 + 1 + width + 1 + 3 + 1)
            else:
                label_render = (
                    f"[bold {FG}]{rich_escape(opt.label)}[/]"
                    if is_active
                    else f"[{FG}]{rich_escape(opt.label)}[/]"
                )
                head = f"{cursor_glyph} {number} {label_render}"
                desc_indent = " " * (1 + 1 + width + 1)

            line = head
            if opt.description:
                line += f"\n{desc_indent}[{FG_MUTED}]{rich_escape(opt.description)}[/]"
            lines.append(line)

        type_idx = _type_row_index(question)
        if type_idx is not None:
            is_active = draft.cursor == type_idx
            cursor_glyph = (
                f"[bold {ACCENT}]›[/]" if is_active else " "  # noqa: RUF001
            )
            number_text = f"{type_idx + 1}.".rjust(width)
            number = f"[{ACCENT}]{number_text}[/]" if is_active else f"[{FG_MUTED}]{number_text}[/]"

            cursor_block = "[reverse] [/reverse]"
            typed = draft.typed_text
            if typed:
                typed_render = rich_escape(typed)
                if is_active:
                    body = f"[{FG}]{typed_render}[/]{cursor_block}"
                else:
                    body = f"[{FG}]{typed_render}[/]"
            elif is_active:
                body = f"{cursor_block}[{FG_MUTED}] {_PLACEHOLDER}[/]"
            else:
                body = f"[{FG_MUTED}]{_PLACEHOLDER}[/]"

            lines.append(f"{cursor_glyph} {number} {body}")

        submit_idx = _submit_row_index(question)
        if submit_idx is not None:
            is_active = draft.cursor == submit_idx
            answered = _question_is_answered(question, draft)
            cursor_glyph = (
                f"[bold {ACCENT}]›[/]" if is_active else " "  # noqa: RUF001
            )
            if is_active and answered:
                body = f"[bold {ACCENT}]→ Submit[/]"
            elif is_active:
                body = f"[{FG_MUTED}]→ Submit (no selection)[/]"
            elif answered:
                body = f"[{FG_SUBTLE}]→ Submit[/]"
            else:
                body = f"[{FG_MUTED}]→ Submit[/]"
            # Indent to align with options (skip the number column).
            indent = " " * (1 + width + 1)
            lines.append(f"{cursor_glyph} {indent}{body}")

        options.update("\n".join(lines))

    def _render_input(self, question: HumanQuestion, draft: _QuestionDraft) -> None:
        input_bar = self.query_one("#hp-input-bar", Horizontal)
        input_field = self.query_one("#hp-input-field", Input)
        if question.kind == "input":
            input_bar.remove_class("-hidden")
            if input_field.value != draft.typed_text:
                input_field.value = draft.typed_text
        else:
            input_bar.add_class("-hidden")

    def _render_hint(self, question: HumanQuestion) -> None:
        assert self._prompt is not None
        bundle = len(self._prompt.questions) > 1
        nav_parts: list[str] = []
        if question.kind == "input":
            nav_parts.append("Type")
            nav_parts.append("Enter to continue" if bundle else "Enter to submit")
        else:
            nav_parts.append("↑↓ navigate")
            if question.multiple:
                nav_parts.append("Space toggle")
                nav_parts.append("Enter to continue" if bundle else "Enter to submit")
            else:
                nav_parts.append("Enter select")
        if bundle:
            nav_parts.append("Tab switch question")
        nav_parts.append("Esc cancel")
        self.query_one("#hp-hint", Static).update("  ·  ".join(nav_parts))

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------

    def on_input_changed(self, event: Input.Changed) -> None:
        if self._draft is None or self._prompt is None or event.input.id != "hp-input-field":
            return
        idx, _ = self._active_question()
        self._draft.for_question(idx).typed_text = event.value
        self._render_tabs()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Enter inside the bordered editor — Input consumes the key before on_key sees it."""
        if not self.is_active or self._prompt is None or self._draft is None:
            return
        if event.input.id != "hp-input-field":
            return
        event.stop()
        idx, question = self._active_question()
        draft = self._draft.for_question(idx)
        if not _question_is_answered(question, draft):
            return
        self._maybe_advance_or_submit()

    def on_key(self, event: events.Key) -> None:
        if not self.is_active or self._prompt is None or self._draft is None:
            return
        idx, question = self._active_question()
        draft = self._draft.for_question(idx)

        if event.key == "escape":
            event.stop()
            self.action_cancel()
            return

        if event.key in {"tab", "shift+tab"}:
            if len(self._prompt.questions) <= 1:
                return
            event.stop()
            direction = -1 if event.key == "shift+tab" else 1
            self._draft.tab_index = (self._draft.tab_index + direction) % len(
                self._prompt.questions
            )
            self._refresh_view()
            self._sync_focus()
            return

        if question.kind == "input":
            # The bordered Input owns its key handling; Enter is on_input_submitted.
            return

        # Choice mode — cursor-driven options + optional inline type/submit rows.
        on_type_row = _is_type_row(question, draft.cursor)
        on_submit_row = _is_submit_row(question, draft.cursor)
        n_options = _option_count(question)

        if event.key in {"up", "down"} or (event.key in {"j", "k"} and not on_type_row):
            event.stop()
            direction = -1 if event.key in {"up", "k"} else 1
            draft.cursor = (draft.cursor + direction) % n_options
            self._render_options(question, draft)
            return

        if on_submit_row:
            if event.key == "enter":
                event.stop()
                if _question_is_answered(question, draft):
                    self._maybe_advance_or_submit()
            return

        if on_type_row:
            if event.key == "backspace":
                event.stop()
                if draft.typed_text:
                    draft.typed_text = draft.typed_text[:-1]
                    self._render_options(question, draft)
                    self._render_tabs()
                return
            if event.key == "enter":
                event.stop()
                if draft.typed_text.strip():
                    self._maybe_advance_or_submit()
                return
            if (
                event.character is not None
                and len(event.character) == 1
                and event.character.isprintable()
            ):
                event.stop()
                draft.typed_text += event.character
                self._render_options(question, draft)
                self._render_tabs()
            return

        # Cursor on a real option row.
        if event.key == "space" and question.multiple:
            event.stop()
            self._toggle_current(question, draft)
            return
        if event.key == "enter":
            event.stop()
            self._activate_current(question, draft)
            return

    def _toggle_current(self, question: HumanQuestion, draft: _QuestionDraft) -> None:
        label = question.options[draft.cursor].label
        if label in draft.selected_labels:
            draft.selected_labels.remove(label)
        else:
            draft.selected_labels.append(label)
        # Selecting a labeled option clears any typed custom answer (mutually exclusive).
        if draft.typed_text:
            draft.typed_text = ""
        self._render_options(question, draft)
        self._render_tabs()

    def _activate_current(self, question: HumanQuestion, draft: _QuestionDraft) -> None:
        label = question.options[draft.cursor].label
        if question.multiple:
            self._toggle_current(question, draft)
            return
        # Single-select: pick this label, clear any typed custom answer, advance / submit.
        draft.selected_labels = [label]
        draft.typed_text = ""
        self._render_options(question, draft)
        self._render_tabs()
        self._maybe_advance_or_submit()

    def _maybe_advance_or_submit(self) -> None:
        assert self._prompt is not None
        assert self._draft is not None
        # Multi-question: move to next unanswered question; if all answered, submit.
        if len(self._prompt.questions) > 1:
            n = len(self._prompt.questions)
            for offset in range(1, n + 1):
                next_idx = (self._draft.tab_index + offset) % n
                next_q = self._prompt.questions[next_idx]
                next_d = self._draft.for_question(next_idx)
                if not _question_is_answered(next_q, next_d):
                    self._draft.tab_index = next_idx
                    self._refresh_view()
                    self._sync_focus()
                    return
        self._handle_submit()

    def _handle_submit(self) -> None:
        if self._prompt is None or self._draft is None:
            return
        all_answered = all(
            _question_is_answered(q, self._draft.for_question(i))
            for i, q in enumerate(self._prompt.questions)
        )
        if not all_answered:
            return
        answers = [
            _build_answer(q, self._draft.for_question(i))
            for i, q in enumerate(self._prompt.questions)
        ]
        request_id = self._prompt.request_id
        clear_draft(request_id)
        self.hide_prompt()
        self.post_message(self.Submit(request_id, answers))

    def action_cancel(self) -> None:
        if self._prompt is None:
            return
        request_id = self._prompt.request_id
        clear_draft(request_id)
        self.hide_prompt()
        self.post_message(self.Cancel(request_id))
