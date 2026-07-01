"""Profile picker dialog — shows saved profiles for switching."""

from __future__ import annotations

import typing as t

from rich.text import Text
from textual.message import Message
from textual.widgets.option_list import Option

from dreadnode.app.tui.theme import BRAND, FG, FG_FAINTEST, FG_MUTED, FG_SUBTLE, WARNING
from dreadnode.app.tui.widgets.overlay_mixin import OverlayMixin

if t.TYPE_CHECKING:
    from textual.events import Key

    from dreadnode.app.config import Profile


class ProfileDialog(OverlayMixin):
    """Popup dialog triggered by /profile — lists saved profiles for switching."""

    class ProfileSelected(Message):
        """Posted when a profile is selected."""

        def __init__(self, profile_name: str) -> None:
            self.profile_name = profile_name
            super().__init__()

    class ProfileDeleted(Message):
        """Posted when a profile deletion is requested via 'x' key."""

        def __init__(self, profile_name: str) -> None:
            self.profile_name = profile_name
            super().__init__()

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)
        self._profile_names: list[str] = []
        self._active_name: str | None = None

    def show_profiles(
        self,
        profiles: dict[str, Profile],
        active_name: str | None = None,
    ) -> None:
        """Populate the dialog with profiles and show it."""
        self._profile_names = list(profiles.keys())
        self._active_name = active_name
        self.clear_options()

        if not profiles:
            self.add_option(
                Option(
                    Text("No profiles saved", style=f"italic {FG_MUTED}"),
                    disabled=True,
                )
            )
            self.border_title = "Profiles"
            self.add_class("-visible")
            return

        for name, profile in profiles.items():
            is_active = name == active_name
            disconnected = not profile.api_key

            label = Text()
            # Selection dot + name
            if is_active:
                label.append(" ● ", style=BRAND)
                label.append(name, style=f"bold {FG}")
            else:
                label.append(" ○ ", style=FG_FAINTEST)
                label.append(name, style=FG_SUBTLE)

            # Disconnected indicator
            if disconnected:
                label.append("  ·  ", style=FG_FAINTEST)
                label.append("disconnected", style=WARNING)

            # Detail line: email · server URL
            parts: list[str] = []
            if profile.email:
                parts.append(profile.email)
            if profile.url:
                parts.append(profile.url)
            if parts:
                label.append(f"\n     {' · '.join(parts)}", style=FG_MUTED)

            self.add_option(Option(label, id=name))

        self.highlighted = 0
        self.border_title = f"Profiles ({len(profiles)})  ^X delete"
        self.add_class("-visible")

    def select_highlighted(self) -> bool:
        if not self.is_visible or self.option_count == 0:
            return False
        idx = self.highlighted
        if idx is not None and 0 <= idx < self.option_count:
            option = self.get_option_at_index(idx)
            if option.id:
                self.post_message(self.ProfileSelected(option.id))
                self.hide()
                return True
        return False

    def on_option_list_option_selected(self, event: OverlayMixin.OptionSelected) -> None:
        option_id = event.option.id
        if option_id:
            self.post_message(self.ProfileSelected(option_id))
            self.hide()

    def on_key(self, event: Key) -> bool:
        if not self.is_visible:
            return False
        if event.key == "ctrl+x":
            event.prevent_default()
            event.stop()
            idx = self.highlighted
            if idx is not None and 0 <= idx < self.option_count:
                option = self.get_option_at_index(idx)
                if option.id and option.id != self._active_name:
                    self.post_message(self.ProfileDeleted(option.id))
                    self.hide()
                    return True
            return True
        return False
