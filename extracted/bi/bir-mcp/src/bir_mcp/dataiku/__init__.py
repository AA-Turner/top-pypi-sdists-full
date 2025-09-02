import datetime
import enum
import inspect
from typing import Annotated, override

import fastmcp.prompts
import fastmcp.resources
import fastmcp.tools
import httpx
import pydantic

from bir_mcp.core import BaseMcp, build_readonly_tools
from bir_mcp.grafana.prompts import get_prompts
from bir_mcp.grafana.resources import get_mcp_resource_uri_functions
from bir_mcp.grafana.utils import to_grafana_time_format
from bir_mcp.utils import araise_for_status, filter_dict_by_keys, to_maybe_ssl_context


class Dataiku(BaseMcp):
    def __init__(
        self,
        auth: tuple[str, str],
        url: str = "https://dssdesign-data.kapitalbank.az",
        http_timeout_seconds: int = 30,
        timezone: str = "UTC",
        ssl_verify: bool | str = True,
    ):
        super().__init__(timezone=timezone)
        self.client = httpx.AsyncClient(
            auth=auth,
            base_url=url,
            event_hooks={"response": [araise_for_status]},
            timeout=http_timeout_seconds,
            verify=to_maybe_ssl_context(ssl_verify),
        )

    @override
    def get_tag(self):
        return "dataiku"

    @override
    def get_mcp_server_without_components(self):
        server = fastmcp.FastMCP(
            name="Bir Dataiku MCP server",
            instructions=inspect.cleandoc("""
                Use this server for tasks related to Dataiku.
            """),
        )
        return server

    @override
    def get_mcp_tools(self, max_output_length: int | None = None, tags: set[str] | None = None):
        functions = []
        tools = build_readonly_tools(functions, max_output_length=max_output_length)
        return tools

    async def get_project_list(self) -> dict: ...
