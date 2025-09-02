import base64
import inspect
import io
import pathlib
import tempfile
import threading
import uuid
from typing import override

import altair
import fastapi.staticfiles
import fastmcp
import mcp
import pandas as pd
import sqlalchemy as sa
import uvicorn

from bir_mcp.core import BaseMcp
from bir_mcp.utils import find_available_port


class Charts(BaseMcp):
    def __init__(
        self,
        engines: dict[str, sa.Engine],
        timezone: str = "UTC",
        max_served_static_files: int = 100,
    ):
        super().__init__(timezone=timezone)
        self.engines = engines

        # Initialize a background FastAPI + Uvicorn server to serve generated HTML chart files
        self._max_served_files = max_served_static_files
        self._serve_dir_obj = tempfile.TemporaryDirectory()
        self.serve_dir = pathlib.Path(self._serve_dir_obj.name)
        self.port = find_available_port()
        self.app = fastapi.FastAPI()
        self.app.mount(
            "/",
            fastapi.staticfiles.StaticFiles(directory=str(self.serve_dir), html=True),
            name="static",
        )

        def _run() -> None:
            uvicorn.run(
                self.app,
                host="127.0.0.1",
                port=self.port,
                log_level="warning",
                lifespan="off",  # faster startup; we don't need lifespan events
            )

        self.thread = threading.Thread(target=_run, daemon=True)
        self.thread.start()

    @override
    def get_tag(self):
        return "charts"

    @override
    def get_mcp_server_without_components(self):
        server = fastmcp.FastMCP(
            name="MCP server with charting and plotting tools",
            instructions=inspect.cleandoc("""
                Contains tools to create charts and plots.
            """),
        )
        return server

    @override
    def get_mcp_tools(self, max_output_length: int | None = None, tags: set[str] | None = None):
        tools = [
            self.build_chart,
            self.build_html_page,
        ]
        tools = [
            fastmcp.tools.FunctionTool.from_function(
                tool,
                tags=tags,
                annotations=mcp.types.ToolAnnotations(
                    readOnlyHint=True, destructiveHint=False, idempotentHint=True
                ),
            )
            for tool in tools
        ]
        return tools

    def _cleanup_old_files(self) -> None:
        paths = self.serve_dir.iterdir()
        paths = sorted(paths, key=lambda path: path.stat().st_mtime)
        for path in paths[-self._max_served_files :]:
            path.unlink(missing_ok=True)

    def _build_link(self, path: str, name: str | None = None) -> str:
        link = f"http://127.0.0.1:{self.port}/{path}"
        link = f"[{name}]({link})" if name else link
        return link

    def build_chart(self, vega_lite_json_spec: str, sql_query: str, connection_name: str):
        """
        Build a single chart from a Vega-Lite JSON specification and a SQL query.
        The connection name can be determined by calling the get_database_info tool of an SQL MCP.
        Refer to data source as "sql_query", for example:
        ```json
        {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "data": {"name": "sql_query"},
        "title": "My Bar Chart",
        "mark": "bar",
        "encoding": {
            "x": {"field": "category", "type": "nominal", "title": "Category"},
            "y": {"field": "value", "type": "quantitative", "title": "Value"},
            "color": {"field": "group", "type": "nominal", "title": "Group"}
        },
        "width": 400,
        "height": 300
        }
        ```
        Spaces in the example JSON are just for human readability, when generating the real JSON,
        omit all spaces.
        """
        # Json schema https://vega.github.io/schema/vega-lite/v5.json is huge, need RAG for it.
        # After generating PNG chart may need to filter it from chat conversation to save tokens
        if not (engine := self.engines.get(connection_name)):
            raise ValueError(
                f"Connection {connection_name} not found among available connections: {sorted(self.engines)}"
            )

        df = pd.read_sql(sql_query, engine)
        chart = altair.Chart.from_json(vega_lite_json_spec)
        chart.data = df
        io_bytes = io.BytesIO()
        chart.save(io_bytes, format="png")
        image = mcp.types.ImageContent(
            type="image",
            mimeType="image/png",
            data=base64.b64encode(io_bytes.getvalue()).decode(),
        )

        self._cleanup_old_files()
        filename = f"chart_{uuid.uuid4().hex}.html"
        file_path = self.serve_dir / filename
        chart.save(file_path, format="html")
        text = mcp.types.TextContent(
            type="text",
            text=self._build_link(name="Chart", path=filename),
        )

        return [image, text]

    def build_html_page(self, html: str):
        """Build and serve an HTML page. Returns a link to the page."""
        self._cleanup_old_files()
        filename = f"page_{uuid.uuid4().hex}.html"
        file_path = self.serve_dir / filename
        # TODO: switch to anyio.read_file for async, but it's probably a minor optimization.
        with open(file_path, "w") as f:
            f.write(html)

        text = mcp.types.TextContent(
            type="text",
            text=self._build_link(name="Page", path=filename),
        )
        return text
