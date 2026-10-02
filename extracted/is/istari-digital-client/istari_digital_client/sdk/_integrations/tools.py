"""Tools manager (IstariIntegrations surface)."""

from __future__ import annotations

from typing import Any

from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._integrations.integration_types import Tool as ToolType, ToolVersion
from istari_digital_client.sdk._generated.v2.models.new_tool import NewTool
from istari_digital_client.sdk._generated.v2.models.new_tool_version import NewToolVersion
from istari_digital_client.sdk._generated.v2.models.tool_include import ToolInclude


class Tools(_Manager):
    """Manager for tools: create / get / list."""

    def create(
        self, *, name: str, tool_versions: list[NewToolVersion] | None = None
    ) -> ToolType:
        """Create a new tool.

        Mutates: true
        """
        dto = self._call(
            self._engine.v2_api.create_tool,
            NewTool(name=name, tool_versions=tool_versions or []),
        )
        return ToolType._bind(dto, mgr=self)

    def get(self, tool_id: str) -> ToolType:
        """Fetch a tool by UUID."""
        dto = self._call(self._engine.v2_api.get_tool, tool_id)
        return ToolType._bind(dto, mgr=self)

    def list(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        include: list[ToolInclude] | None = None,
        include_deprecated: bool | None = None,
        sort: str | None = None,
    ) -> Page[ToolType]:
        """List tools."""

        def fetch(page_num: int) -> Any:
            return self._call(
                self._engine.v2_api.list_tools,
                page=page_num,
                size=size,
                include=include,
                include_deprecated=include_deprecated,
                sort=sort,
            )

        return self._paginate_offset(
            fetch, lambda d: ToolType._bind(d, mgr=self), start_page=page or 1
        )

    def create_version(self, tool_id: str, *, tool_version: str) -> ToolVersion:
        """Create a new tool version.

        Mutates: true
        """
        dto = self._call(
            self._engine.v2_api.create_tool_versions,
            tool_id,
            NewToolVersion(tool_version=tool_version),
        )
        return ToolVersion._bind(dto, mgr=self)

    def get_version(self, version_id: str) -> ToolVersion:
        """Fetch a tool version by its ID.

        Note: Tool version IDs are globally unique, so no tool_id is needed.
        """
        dto = self._call(self._engine.v2_api.get_tool_version, version_id)
        return ToolVersion._bind(dto, mgr=self)

    def list_versions(
        self, *, page: int | None = None, size: int | None = None
    ) -> Page[ToolVersion]:
        """List all tool versions.

        Note: The API lists all tool versions globally, not filtered by tool.
        """

        def fetch(page_num: int) -> Any:
            return self._call(
                self._engine.v2_api.list_tool_versions,
                page=page_num,
                size=size,
            )

        return self._paginate_offset(
            fetch, lambda d: ToolVersion._bind(d, mgr=self), start_page=page or 1
        )
