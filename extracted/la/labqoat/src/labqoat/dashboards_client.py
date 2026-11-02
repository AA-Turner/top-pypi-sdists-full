"""Published dashboard version client."""

from __future__ import annotations

from collections.abc import Generator, Iterator, Mapping, Sequence
from urllib.parse import urlencode

from labqoat._generated.dashboard import Dashboard
from labqoat._generated.dashboard_change import DashboardChange
from labqoat._generated.dashboard_change_page import DashboardChangePage
from labqoat._generated.dashboard_page import DashboardPage
from labqoat._generated.dashboard_version_page import DashboardVersionPage
from labqoat.base_client import BaseClient
from labqoat.dashboard_change_stream import DashboardChangeStream
from labqoat.json_document import JsonValue


class DashboardsClient(BaseClient):
    """Publish and inspect immutable dashboard versions."""

    def publish(self, payload: Mapping[str, JsonValue]) -> Dashboard:
        """Publish a dashboard version, creating or revising its identity."""
        response = self.send_json("POST", "/api/v1/dashboards", payload)
        return self.decode(response, "/api/v1/dashboards", Dashboard.from_dict)

    def get(self, ref: str, version: str | None = None) -> Dashboard:
        """Read one published dashboard version."""
        query = {"ref": ref}
        if version is not None:
            query["version"] = version
        path = f"/api/v1/dashboards/item?{urlencode(query)}"
        return self.decode(self.send("GET", path), path, Dashboard.from_dict)

    def list_page(self, limit: int | None = None, cursor: str | None = None, name: str | None = None) -> DashboardPage:
        """Read one bounded page of published dashboards."""
        query: dict[str, str] = {}
        if limit is not None:
            query["limit"] = str(limit)
        if cursor is not None:
            query["cursor"] = cursor
        if name is not None:
            query["name"] = name
        path = "/api/v1/dashboards"
        if query:
            path = f"{path}?{urlencode(query)}"
        return self.decode(self.send("GET", path), path, DashboardPage.from_dict)

    def iter_all(self, page_size: int = 20, name: str | None = None) -> Iterator[Dashboard]:
        """Yield dashboards lazily by following returned cursors."""
        cursor: str | None = None
        while True:
            page = self.list_page(limit=page_size, cursor=cursor, name=name)
            yield from page.items
            cursor = page.next_cursor
            if cursor is None:
                return

    def versions(self, ref: str, limit: int | None = None, cursor: str | None = None) -> DashboardVersionPage:
        """Read one dashboard's immutable version history."""
        query: dict[str, str] = {"ref": ref}
        if limit is not None:
            query["limit"] = str(limit)
        if cursor is not None:
            query["cursor"] = cursor
        path = f"/api/v1/dashboards/item/versions?{urlencode(query)}"
        return self.decode(self.send("GET", path), path, DashboardVersionPage.from_dict)

    def changes(
        self,
        ref: str,
        panel: str | Sequence[str] | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> DashboardChangePage:
        """Read recorded leader and frontier changes, newest first, of every watched panel or the named ones."""
        query: dict[str, str] = {"ref": ref}
        chosen = DashboardsClient.chosen(panel)
        if chosen is not None:
            query["panel"] = chosen
        if limit is not None:
            query["limit"] = str(limit)
        if cursor is not None:
            query["cursor"] = cursor
        path = f"/api/v1/dashboards/item/changes?{urlencode(query)}"
        return self.decode(self.send("GET", path), path, DashboardChangePage.from_dict)

    def watch(
        self, ref: str, panel: str | Sequence[str] | None = None, cursor: str | None = None
    ) -> Generator[DashboardChange]:
        """Yield changes as they are recorded; a change's cursor replays the ones recorded after it first."""
        return DashboardChangeStream(self, ref, DashboardsClient.chosen(panel), cursor).changes()

    @staticmethod
    def chosen(panel: str | Sequence[str] | None) -> str | None:
        """One panel id, or several as the comma-separated value the service filters by."""
        if panel is None or isinstance(panel, str):
            return panel
        return ",".join(panel)
