"""Build execution and evidence client."""

from __future__ import annotations

from collections.abc import Mapping

from labqoat._generated.build import Build
from labqoat._generated.build_log_page import BuildLogPage
from labqoat.base_client import BaseClient
from labqoat.json_document import JsonValue


class BuildsClient(BaseClient):
    """Source builds and retained execution logs."""

    def create_build(self, payload: Mapping[str, JsonValue]) -> Build:
        """Register a build."""
        response = self.send_json("POST", "/api/v1/builds", payload)
        return self.decode(response, "/api/v1/builds", Build.from_dict)

    def start_build(self, ref: str) -> Build:
        """Start an accepted build."""
        path = f"/api/v1/builds/item/start?ref={BaseClient.encode_ref(ref)}"
        response = self.send_json("POST", path, {})
        return self.decode(response, path, Build.from_dict)

    def get_build(self, ref: str) -> Build:
        """Read one build."""
        path = f"/api/v1/builds/item?ref={BaseClient.encode_ref(ref)}"
        return self.decode(self.send("GET", path), path, Build.from_dict)

    def get_build_logs(self, ref: str, limit: int = 20) -> BuildLogPage:
        """Read bounded build execution logs."""
        path = f"/api/v1/builds/item/logs?ref={BaseClient.encode_ref(ref)}&limit={limit}"
        return self.decode(self.send("GET", path), path, BuildLogPage.from_dict)
