"""Skills browser dialog — searchable, scrollable, selectable."""

from __future__ import annotations

import typing as t

from rich.text import Text
from textual.message import Message
from textual.widgets.option_list import Option

from dreadnode.app.tui.theme import ACCENT, FG, FG_FAINTEST, FG_MUTED
from dreadnode.app.tui.widgets.overlay_mixin import OverlayMixin


class SkillsDialog(OverlayMixin):
    """Popup dialog for browsing and selecting skills."""

    class SkillSelected(Message):
        """Posted when a skill is selected from the dialog."""

        def __init__(self, skill_name: str) -> None:
            self.skill_name = skill_name
            super().__init__()

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)
        self._skills: list[tuple[str, str]] = []

    def show_skills(self, skills: list[tuple[str, str]]) -> None:
        """Populate with skills and show. Each tuple is (name, description)."""
        self._skills = skills
        self._populate(skills)

    def filter(self, query: str) -> None:
        """Re-render with only skills matching the query."""
        q = query.lower()
        filtered = [(n, d) for n, d in self._skills if q in n.lower() or q in d.lower()]
        self._populate(filtered)

    def _populate(self, skills: list[tuple[str, str]]) -> None:
        self.clear_options()

        if not skills:
            self.add_option(
                Option(Text("No skills found", style=f"italic {FG_MUTED}"), disabled=True)
            )
            self.highlighted = 0
            self.border_title = "Skills (0)"
            self.add_class("-visible")
            return

        for name, desc in skills:
            label = Text()
            label.append(" /", style=ACCENT)
            label.append(name, style=FG)
            if desc:
                truncated = desc[:60] + "\u2026" if len(desc) > 60 else desc
                label.append(f"  {truncated}", style=FG_FAINTEST)
            self.add_option(Option(label, id=name))

        self.highlighted = 0
        self.border_title = f"Skills ({len(skills)})"
        self.add_class("-visible")

    def select_highlighted(self) -> bool:
        if not self.is_visible or self.option_count == 0:
            return False
        idx = self.highlighted
        if idx is not None and 0 <= idx < self.option_count:
            option = self.get_option_at_index(idx)
            if option.id:
                self.post_message(self.SkillSelected(option.id))
                self.hide()
                return True
        return False

    def on_option_list_option_selected(self, event: OverlayMixin.OptionSelected) -> None:
        option_id = event.option.id
        if option_id:
            self.post_message(self.SkillSelected(option_id))
            self.hide()
