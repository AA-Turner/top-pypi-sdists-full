"""Query execution tools."""

import csv
import logging
import time
from pathlib import Path
from typing import Annotated, Any

from fastmcp import FastMCP

from datafold_mcp.client import DatafoldClient

logger = logging.getLogger(__name__)


def _save_rows_to_csv(rows: list[dict[str, Any]], file_path: str) -> None:
    """Save query result rows to a CSV file."""
    if not rows:
        Path(file_path).write_text("", encoding="utf-8")
        return

    fieldnames = list(rows[0].keys())
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


async def _execute_query(
    client: DatafoldClient,
    data_source_id: int,
    query: str,
    save_result_to_file_path: str | None,
    return_rowcount_only: bool,
    return_runtime_seconds_only: bool,
) -> dict[str, Any]:
    """Execute query and process results based on options."""
    logger.info(f"Executing query for data_source_id={data_source_id}")
    logger.debug(f"Query: {query}")

    start_time = time.perf_counter()
    result = await client.run_query(data_source_id, query)
    runtime_seconds = time.perf_counter() - start_time

    logger.info(
        f"Query completed for data_source_id={data_source_id} " f"in {runtime_seconds:.3f} seconds"
    )

    if return_runtime_seconds_only:
        return {"runtime_seconds": runtime_seconds}

    rows = result.rows
    row_count = len(rows)

    if save_result_to_file_path:
        _save_rows_to_csv(rows, save_result_to_file_path)
        logger.info(f"Saved {row_count} rows to {save_result_to_file_path}")
        return {"saved_to_file": save_result_to_file_path, "row_count": row_count}

    if return_rowcount_only:
        return {"row_count": row_count}

    return result.model_dump()


def register_query_tools(mcp: FastMCP, client: DatafoldClient) -> None:
    """Register query-related tools with the MCP server."""

    @mcp.tool(
        name="run_query",
        description=(
            "Execute a SQL query against a specified data source and return results. "
            "Can optionally save results to a CSV file, return only row count, or return only runtime."
        ),
        tags={"database", "query", "sql"},
    )
    async def run_query(
        data_source_id: Annotated[int, "Unique identifier of the data source to query against"],
        query: Annotated[str, "SQL query to execute"],
        save_result_to_file_path: Annotated[
            str | None, "Optional file path to save query results as CSV"
        ] = None,
        return_rowcount_only: Annotated[
            bool, "If True, return only the number of rows instead of the full result set"
        ] = False,
        return_runtime_seconds_only: Annotated[
            bool, "If True, return only the query execution time in seconds"
        ] = False,
    ) -> dict[str, Any]:
        """Execute a SQL query against a specified data source."""
        return await _execute_query(
            client=client,
            data_source_id=data_source_id,
            query=query,
            save_result_to_file_path=save_result_to_file_path,
            return_rowcount_only=return_rowcount_only,
            return_runtime_seconds_only=return_runtime_seconds_only,
        )

    @mcp.tool(
        name="run_query_from_file",
        description=(
            "Execute a SQL query from a file against a specified data source. "
            "Reads the query from the specified file path and executes it. "
            "Can optionally save results to a CSV file, return only row count, or return only runtime."
        ),
        tags={"database", "query", "sql", "file"},
    )
    async def run_query_from_file(
        data_source_id: Annotated[int, "Unique identifier of the data source to query against"],
        query_file_path: Annotated[str, "Path to file containing the SQL query to execute"],
        save_result_to_file_path: Annotated[
            str | None, "Optional file path to save query results as CSV"
        ] = None,
        return_rowcount_only: Annotated[
            bool, "If True, return only the number of rows instead of the full result set"
        ] = False,
        return_runtime_seconds_only: Annotated[
            bool, "If True, return only the query execution time in seconds"
        ] = False,
    ) -> dict[str, Any]:
        """Execute a SQL query from a file against a specified data source."""
        query_path = Path(query_file_path)
        if not query_path.exists():
            raise FileNotFoundError(f"Query file not found: {query_file_path}")

        query = query_path.read_text(encoding="utf-8").strip()
        if not query:
            raise ValueError(f"Query file is empty: {query_file_path}")

        logger.debug(f"Loaded query from {query_file_path}")

        return await _execute_query(
            client=client,
            data_source_id=data_source_id,
            query=query,
            save_result_to_file_path=save_result_to_file_path,
            return_rowcount_only=return_rowcount_only,
            return_runtime_seconds_only=return_runtime_seconds_only,
        )
