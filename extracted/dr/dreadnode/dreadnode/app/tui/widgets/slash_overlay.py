"""Slash command overlay with fuzzy filtering and descriptions."""

from __future__ import annotations

from rich.text import Text
from textual.message import Message
from textual.widgets.option_list import Option

from dreadnode.app.tui.commands import SLASH_COMMANDS, SlashCommand
from dreadnode.app.tui.theme import ACCENT, FG, FG_MUTED, FG_SUBTLE
from dreadnode.app.tui.widgets.overlay_mixin import OverlayMixin


class SlashOverlay(OverlayMixin):
    """Popup overlay that filters slash commands as the user types."""

    class SlashSelected(Message):
        """Posted when a slash command is selected."""

        def __init__(self, command: str) -> None:
            self.command = command
            super().__init__()

    def filter_commands(
        self,
        prefix: str,
        *,
        extra_commands: list[SlashCommand] | None = None,
    ) -> None:
        """Update the option list with commands matching the prefix."""
        builtin_names = {c.name for c in SLASH_COMMANDS}
        all_commands = list(SLASH_COMMANDS)
        if extra_commands:
            all_commands.extend(c for c in extra_commands if c.name not in builtin_names)

        # Sort all commands alphabetically so skills interleave with builtins
        all_commands.sort(key=lambda c: c.name.lstrip("/").lower())

        query = prefix.lstrip("/").lower()
        matches: list[SlashCommand] = []
        for cmd in all_commands:
            name_lower = cmd.name.lstrip("/").lower()
            if not query or query in name_lower:
                matches.append(cmd)

        self.clear_options()
        if not matches:
            self.add_class("-visible")
            self.add_option(Option("No matching commands", disabled=True))
            return

        # Truncate labels to overlay width; fall back to container width when
        # the overlay hasn't been laid out yet (display: none → width 0).
        width = self.size.width or (self.container_size.width or 0) or 120
        max_width = width - 4  # borders + scrollbar

        for cmd in matches:
            is_skill = cmd.name not in builtin_names
            label = Text()
            if is_skill:
                label.append(" /", style=ACCENT)
                label.append(cmd.name.lstrip("/"), style=FG)
            else:
                label.append(f" {cmd.name}", style=f"bold {ACCENT}")
            if cmd.hint:
                label.append(f" {cmd.hint}", style=FG_SUBTLE)
            label.append(f"  {cmd.description}", style=FG_MUTED)
            label.truncate(max_width, overflow="ellipsis")
            self.add_option(Option(label, id=cmd.name))

        self.highlighted = 0
        self.add_class("-visible")

    def select_highlighted(self) -> bool:
        """Select the currently highlighted option. Returns True if handled."""
        if not self.is_visible or self.option_count == 0:
            return False
        idx = self.highlighted
        if idx is not None and 0 <= idx < self.option_count:
            option = self.get_option_at_index(idx)
            if option.id:
                self.post_message(self.SlashSelected(option.id))
                self.hide()
                return True
        return False

    def on_option_list_option_selected(self, event: OverlayMixin.OptionSelected) -> None:
        """Post a SlashSelected message when a command is chosen."""
        option_id = event.option.id
        if option_id:
            self.post_message(self.SlashSelected(option_id))
            self.hide()
