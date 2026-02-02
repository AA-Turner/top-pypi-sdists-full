"""Data source tools."""

import logging
from typing import Annotated, Any

from fastmcp import FastMCP

from datafold_mcp.client import DatafoldClient

logger = logging.getLogger(__name__)


def register_data_source_tools(mcp: FastMCP, client: DatafoldClient) -> None:
    """Register data source related tools with the MCP server."""

    @mcp.tool(
        name="list_data_sources",
        description="List all available data sources with their key information.",
        tags={"data-sources", "list", "metadata"},
    )
    async def list_data_sources() -> list[dict[str, Any]]:
        """List available data sources."""
        return await client.list_data_sources()

    @mcp.tool(
        name="get_table_schema",
        description=(
            "Get schema information for a specific table including column names, types, and metadata. "
            "Useful for understanding table structure before running queries or datadiffs."
        ),
        tags={"database", "schema", "metadata"},
    )
    async def get_table_schema(
        data_source_id: Annotated[int, "Data source ID"],
        table_path: Annotated[list[str], "Table path (e.g., ['schema', 'table'])"],
        timeout: Annotated[int, "Maximum seconds to wait for schema fetch"] = 60,
    ) -> dict[str, Any]:
        """Get table schema information."""
        logger.info(f"Fetching schema for {table_path} from data_source_id={data_source_id}")
        return await client.get_table_schema(data_source_id, table_path, timeout)

    @mcp.tool(
        name="guess_primary_keys",
        description=(
            "Automatically guess primary key columns for a table using brute force analysis. "
            "Analyzes column uniqueness to identify the best PK candidates. "
            "Useful when you need to run a datadiff but don't know the primary keys."
        ),
        tags={"database", "schema", "primary-key", "datadiff"},
    )
    async def guess_primary_keys(
        data_source_id: Annotated[int, "Data source ID"],
        table: Annotated[list[str], "Table path (e.g., ['schema', 'table'])"],
        sample_size: Annotated[
            int | None, "Sample size for analysis (None for full table, recommended: 5000)"
        ] = 5000,
        avoid_types: Annotated[
            list[str] | None, "Column types to avoid (e.g., ['text', 'blob'])"
        ] = None,
        avoid_names: Annotated[
            list[str] | None, "Column names to avoid (e.g., ['created_at', 'updated_at'])"
        ] = None,
        candidates: Annotated[int, "Number of PK candidates to return"] = 1,
    ) -> dict[str, Any]:
        """Guess primary key columns for a table."""
        table_str = ".".join(table)
        logger.info(f"Guessing PKs for table={table_str} on data_source_id={data_source_id}")

        result = await client.guess_primary_keys(
            data_source_id=data_source_id,
            table=table,
            sample_size=sample_size,
            avoid_types=avoid_types,
            avoid_names=avoid_names,
            candidates=candidates,
        )

        return result
