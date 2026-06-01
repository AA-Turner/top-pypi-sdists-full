from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any, ClassVar

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Static

from drydock.cli.history_manager import HistoryManager
from drydock.cli.textual_ui.widgets.chat_input.text_area import ChatTextArea, InputMode
from drydock.cli.textual_ui.widgets.no_markup_static import NoMarkupStatic
from drydock.cli.textual_ui.widgets.spinner import SpinnerMixin, SpinnerType


class _PromptSpinner(SpinnerMixin, Static):
    SPINNER_TYPE: ClassVar[SpinnerType] = SpinnerType.BRAILLE

    def __init__(self) -> None:
        self._indicator_widget: Static | None = None
        self.init_spinner()
        super().__init__(self._spinner.current_frame(), id="prompt-spinner")

    def on_mount(self) -> None:
        self._indicator_widget = self
        self.start_spinner_timer()


class ChatInputBody(Widget):
    class Submitted(Message):
        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()

    # 2026-05-31: ghost-suggestion cycle. Operator wants a Claude-Code-
    # style "recommended command" shown in lighter text when the input
    # is empty; Tab populates it. Rotates after each submit so the user
    # sees different tips over time. Order is intentional — most
    # generally-useful commands first.
    DEFAULT_GHOST_SUGGESTIONS: ClassVar[tuple[str, ...]] = (
        "/help",
        "/clear",
        "/undo",
        "/back",
        "/goal",
        "/skills",
        "/agents",
        "/permissions",
        "/doctor",
        "/setup-model detect",
    )

    def __init__(
        self,
        history_file: Path | None = None,
        nuage_enabled: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.input_widget: ChatTextArea | None = None
        self.prompt_widget: NoMarkupStatic | None = None
        self.ghost_widget: Static | None = None
        self._nuage_enabled = nuage_enabled
        self._switching_mode = False
        self._ghost_index: int = 0

        if history_file:
            self.history = HistoryManager(history_file)
        else:
            self.history = None

        self._completion_reset: Callable[[], None] | None = None

    def compose(self) -> ComposeResult:
        with Horizontal():
            self.prompt_widget = NoMarkupStatic(">", id="prompt")
            yield self.prompt_widget

            self.input_widget = ChatTextArea(
                id="input", nuage_enabled=self._nuage_enabled
            )
            yield self.input_widget

            # Ghost suggestion overlays the empty input area. CSS
            # positions it absolutely on top of #input (see app.tcss
            # selector #ghost-suggestion); when input has text, we
            # hide it.
            self.ghost_widget = Static(
                f"[dim]{self.DEFAULT_GHOST_SUGGESTIONS[0]} [/][dim italic](tab)[/]",
                id="ghost-suggestion",
                markup=True,
            )
            yield self.ghost_widget

    def on_mount(self) -> None:
        if self.input_widget:
            self.input_widget.focus()
            self._refresh_ghost()

    def _parse_mode_and_text(self, text: str) -> tuple[InputMode, str]:
        if text.startswith("!"):
            return "!", text[1:]
        elif text.startswith("/"):
            return "/", text[1:]
        elif text.startswith("&") and self._nuage_enabled:
            return "&", text[1:]
        else:
            return ">", text

    def _update_prompt(self) -> None:
        if not self.input_widget or not self.prompt_widget:
            return

        self.prompt_widget.update(self.input_widget.input_mode)

    def on_chat_text_area_mode_changed(self, event: ChatTextArea.ModeChanged) -> None:
        if self.prompt_widget:
            self.prompt_widget.update(event.mode)
        self._refresh_ghost()

    def _refresh_ghost(self) -> None:
        """Show the ghost suggestion when input is genuinely empty; hide
        otherwise. Called on text changes, mode changes, mount, submit."""
        if not self.input_widget or not self.ghost_widget:
            return
        # "Empty" here means default mode AND no typed characters. As
        # soon as the user types a mode prefix or any char, the ghost
        # disappears so it doesn't overlap real input.
        is_empty = (
            self.input_widget.text == ""
            and self.input_widget.input_mode == self.input_widget.DEFAULT_MODE
        )
        if is_empty:
            suggestion = self.DEFAULT_GHOST_SUGGESTIONS[
                self._ghost_index % len(self.DEFAULT_GHOST_SUGGESTIONS)
            ]
            self.input_widget.set_ghost_suggestion(suggestion)
            self.ghost_widget.update(
                f"[dim]{suggestion} [/][dim italic](tab)[/]"
            )
            self.ghost_widget.display = True
        else:
            self.input_widget.set_ghost_suggestion(None)
            self.ghost_widget.display = False

    def on_chat_text_area_changed(self, event: Any) -> None:
        # Textual fires TextArea.Changed bubbling up; we refresh the
        # ghost so it disappears as soon as the user starts typing.
        self._refresh_ghost()

    def on_chat_text_area_ghost_accepted(
        self, event: ChatTextArea.GhostAccepted
    ) -> None:
        # User accepted via Tab — hide the ghost; advance the rotation
        # so the next empty-state shows a different suggestion.
        self._ghost_index = (self._ghost_index + 1) % len(
            self.DEFAULT_GHOST_SUGGESTIONS
        )
        self._refresh_ghost()

    def _load_history_entry(self, text: str, cursor_col: int | None = None) -> None:
        if not self.input_widget:
            return

        mode, display_text = self._parse_mode_and_text(text)

        self.input_widget._navigating_history = True
        self.input_widget.set_mode(mode)
        self.input_widget.load_text(display_text)

        first_line = display_text.split("\n")[0]
        col = cursor_col if cursor_col is not None else len(first_line)
        cursor_pos = (0, col)

        self.input_widget.move_cursor(cursor_pos)
        self.input_widget._last_cursor_col = col
        self.input_widget._cursor_pos_after_load = cursor_pos
        self.input_widget._cursor_moved_since_load = False

        self._update_prompt()
        self._notify_completion_reset()

    def on_chat_text_area_history_previous(
        self, event: ChatTextArea.HistoryPrevious
    ) -> None:
        if not self.history or not self.input_widget:
            return

        if self.history._current_index == -1:
            self.input_widget._original_text = self.input_widget.text

        if (
            self.history._current_index != -1
            and self.input_widget._last_used_prefix is not None
            and self.input_widget._last_used_prefix != event.prefix
        ):
            self.history.reset_navigation()

        self.input_widget._last_used_prefix = event.prefix
        previous = self.history.get_previous(
            self.input_widget._original_text, prefix=event.prefix
        )

        if previous is not None:
            self._load_history_entry(previous)

    def on_chat_text_area_history_next(self, event: ChatTextArea.HistoryNext) -> None:
        if not self.history or not self.input_widget:
            return

        if self.history._current_index == -1:
            return

        if (
            self.input_widget._last_used_prefix is not None
            and self.input_widget._last_used_prefix != event.prefix
        ):
            self.history.reset_navigation()

        self.input_widget._last_used_prefix = event.prefix

        has_next = any(
            self.history._entries[i].startswith(event.prefix)
            for i in range(self.history._current_index + 1, len(self.history._entries))
        )

        original_matches = self.input_widget._original_text.startswith(event.prefix)

        if has_next or original_matches:
            next_entry = self.history.get_next(prefix=event.prefix)
            if next_entry is not None:
                cursor_col = (
                    len(event.prefix) if self.history._current_index == -1 else None
                )
                self._load_history_entry(next_entry, cursor_col=cursor_col)

    def on_chat_text_area_history_reset(self, event: ChatTextArea.HistoryReset) -> None:
        if self.history:
            self.history.reset_navigation()
        if self.input_widget:
            self.input_widget._original_text = ""
            self.input_widget._cursor_pos_after_load = None
            self.input_widget._cursor_moved_since_load = False

    def on_chat_text_area_submitted(self, event: ChatTextArea.Submitted) -> None:
        event.stop()

        if self._switching_mode:
            return

        if not self.input_widget:
            return

        value = event.value.strip()
        if value:
            if self.history:
                self.history.add(value)
                self.history.reset_navigation()

            self.input_widget.clear_text()
            self._update_prompt()

            self._notify_completion_reset()

            # Rotate ghost suggestion after each submit so the user
            # sees a different tip on each empty-input state.
            self._ghost_index = (self._ghost_index + 1) % len(
                self.DEFAULT_GHOST_SUGGESTIONS
            )
            self._refresh_ghost()

            self.post_message(self.Submitted(value))

    @property
    def switching_mode(self) -> bool:
        return self._switching_mode

    @switching_mode.setter
    def switching_mode(self, value: bool) -> None:
        self._switching_mode = value
        if value:
            if self.prompt_widget:
                self.prompt_widget.display = False
            if not self.query(_PromptSpinner):
                self.query_one(Horizontal).mount(_PromptSpinner(), before=0)
        else:
            for spinner in self.query(_PromptSpinner):
                spinner.remove()
            if self.prompt_widget:
                self.prompt_widget.display = True
                self._update_prompt()

    @property
    def value(self) -> str:
        if not self.input_widget:
            return ""
        return self.input_widget.get_full_text()

    @value.setter
    def value(self, text: str) -> None:
        if self.input_widget:
            mode, display_text = self._parse_mode_and_text(text)
            self.input_widget.set_mode(mode)
            self.input_widget.load_text(display_text)
            self._update_prompt()

    def focus_input(self) -> None:
        if self.input_widget:
            self.input_widget.focus()

    def set_completion_reset_callback(
        self, callback: Callable[[], None] | None
    ) -> None:
        self._completion_reset = callback

    def _notify_completion_reset(self) -> None:
        if self._completion_reset:
            self._completion_reset()

    def replace_input(self, text: str, cursor_offset: int | None = None) -> None:
        if not self.input_widget:
            return

        self.input_widget.load_text(text)
        self.input_widget.reset_history_state()
        self._update_prompt()

        if cursor_offset is not None:
            self.input_widget.set_cursor_offset(max(0, min(cursor_offset, len(text))))
