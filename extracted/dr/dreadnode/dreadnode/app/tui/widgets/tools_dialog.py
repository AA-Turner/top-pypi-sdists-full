"""Tools browser dialog — shows all available tools grouped by capability."""

import typing as t

from rich.text import Text
from textual.widgets.option_list import Option

from dreadnode.app.client.models import ToolInfo
from dreadnode.app.tui.theme import FG, FG_FAINTEST, FG_MUTED
from dreadnode.app.tui.widgets.overlay_mixin import OverlayMixin


class ToolsDialog(OverlayMixin):
    """Popup dialog triggered by /tools — shows tools grouped by capability source."""

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)

    def show_tools(self, tools: list[ToolInfo]) -> None:
        """Populate with tools grouped by capability and show."""
        self.clear_options()

        if not tools:
            self.add_option(
                Option(
                    Text("No tools available", style=f"italic {FG_MUTED}"),
                    disabled=True,
                )
            )
            self.border_title = "Tools"
            self.add_class("-visible")
            return

        groups: dict[str, list[ToolInfo]] = {}
        for tool in tools:
            groups.setdefault(tool.capability or "unknown", []).append(tool)

        first = True
        for cap_name, cap_tools in groups.items():
            if not first:
                self.add_option(Option(Text(""), disabled=True))
            first = False

            header = Text()
            header.append(f" {cap_name}", style=f"bold {FG_MUTED}")
            header.append(f"  {len(cap_tools)}", style=FG_FAINTEST)
            self.add_option(Option(header, disabled=True))

            for tool in cap_tools:
                line = Text()
                line.append(f"   {tool.name or '?'}", style=FG)
                desc = tool.description
                if desc:
                    if len(desc) > 50:
                        desc = desc[:47] + "\u2026"
                    line.append(f"  {desc}", style=FG_FAINTEST)
                self.add_option(Option(line, disabled=True))

        self.border_title = f"Tools ({len(tools)})"
        self.add_class("-visible")
