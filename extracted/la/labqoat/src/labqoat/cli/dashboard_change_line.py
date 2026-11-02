"""One readable line for a recorded dashboard leader or frontier change."""

from __future__ import annotations

from collections.abc import Mapping

from labqoat._generated.dashboard_change import DashboardChange
from labqoat.json_document import JsonDocument, JsonValue


class DashboardChangeLine:
    """Say which panel changed, which runs are involved and the values that decided it."""

    @staticmethod
    def text(change: DashboardChange) -> str:
        """Render the time, the panel and what happened on it."""
        describe = DashboardChangeLine.leader if change.kind == "leader" else DashboardChangeLine.frontier
        return f"{change.inserted_at}  {change.panel_title}: {describe(change.data)}"

    @staticmethod
    def leader(data: Mapping[str, JsonValue]) -> str:
        """Name the new leader with its ranked value, and the run it replaced when there was one."""
        leader = JsonDocument.expect_dict(data["leader"])
        text = f"new leader {leader['name']} ({data['metric']} {leader['value']})"
        previous = data.get("previous")
        if not isinstance(previous, dict):
            return text
        return f"{text}, was {previous['name']} ({previous['value']})"

    @staticmethod
    def frontier(data: Mapping[str, JsonValue]) -> str:
        """Name the runs that joined and left, and how many the frontier holds now."""
        moves = [
            f"{label} {', '.join(names)}"
            for label, names in (
                ("joined", DashboardChangeLine.names(data["added"])),
                ("left", DashboardChangeLine.names(data["removed"])),
            )
            if names
        ]
        return f"frontier moved, {'; '.join(moves)}; {data['size']} on the frontier"

    @staticmethod
    def names(points: JsonValue) -> list[str]:
        """Read the run names of frontier points with their coordinates."""
        return [
            f"{point['name']} ({point['x']}, {point['y']})"
            for point in map(JsonDocument.expect_dict, JsonDocument.expect_list(points))
        ]
