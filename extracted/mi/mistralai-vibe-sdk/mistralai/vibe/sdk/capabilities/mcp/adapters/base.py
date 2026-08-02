"""Shared implementation details for MCP capability adapters."""

from collections.abc import Iterable
from typing import Any

import structlog
from pydantic import ValidationError

from mistralai.vibe.sdk.capabilities.mcp.config import McpConfigBase
from mistralai.vibe.sdk.capabilities.mcp.types import McpToolDescriptor

logger = structlog.get_logger()


class McpAdapterBase[ConfigT: McpConfigBase]:
    """Shared base for concrete MCP adapters."""

    def __init__(self, config: ConfigT) -> None:
        self._config = config

    @property
    def server_key(self) -> str:
        """Return the stable identifier for this MCP server, derived from its config."""
        return self._config.server_key

    @property
    def _log_context(self) -> dict[str, Any]:
        """Extra structured-log fields identifying this adapter's server."""
        return {}

    def _normalize_tools(self, raw_tools: Iterable[Any]) -> list[McpToolDescriptor]:
        """Convert raw MCP tool payloads into internal tool descriptors."""
        tools: list[McpToolDescriptor] = []

        for raw in raw_tools:
            try:
                tools.append(McpToolDescriptor.model_validate(raw, from_attributes=True))
            except ValidationError as exc:
                logger.warning(
                    "mcp.tool.validation_failed",
                    mcp_server_key=self.server_key,
                    **self._log_context,
                    exc_info=exc,
                )

        return tools
