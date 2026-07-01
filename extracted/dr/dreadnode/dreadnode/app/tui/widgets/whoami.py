"""WhoAmI widget — styled user identity card for the conversation stream."""

from __future__ import annotations

from typing import Any

from rich.text import Text
from textual.widgets import Static

from dreadnode.app.tui.theme import ACCENT, FG_FAINTEST, FG_SUBTLE


def render_whoami(
    profile_name: str,
    url: str,
    *,
    username: str | None = None,
    email: str | None = None,
    organization: str | None = None,
    workspace: str | None = None,
    project: str | None = None,
) -> Text:
    """Render a styled identity card as Rich Text."""
    text = Text()

    # Header — profile name prominent
    text.append("│ ", style=FG_FAINTEST)
    text.append(profile_name, style=f"bold {ACCENT}")
    text.append("  profile", style=FG_FAINTEST)

    # Detail rows — label-aligned with dim hints
    fields: list[tuple[str, str | None]] = [
        ("user", username),
        ("email", email),
        ("org", organization),
        ("workspace", workspace),
        ("project", project),
        ("server", url),
    ]
    for label, value in fields:
        if value:
            text.append("\n│   ", style=FG_FAINTEST)
            text.append(f"{label:<10}", style=FG_FAINTEST)
            text.append(value, style=FG_SUBTLE if label != "server" else FG_FAINTEST)

    return text


class WhoAmI(Static):
    """Inline identity card displayed by the /whoami command."""

    def __init__(
        self,
        profile_name: str,
        url: str,
        *,
        username: str | None = None,
        email: str | None = None,
        organization: str | None = None,
        workspace: str | None = None,
        project: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._rendered = render_whoami(
            profile_name,
            url,
            username=username,
            email=email,
            organization=organization,
            workspace=workspace,
            project=project,
        )

    def render(self) -> Text:
        return self._rendered
