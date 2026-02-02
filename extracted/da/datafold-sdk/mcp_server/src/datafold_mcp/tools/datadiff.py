"""DataDiff comparison tools."""

import asyncio
import logging
from typing import Annotated, Any, Literal

from fastmcp import FastMCP

from datafold_mcp.client import DatafoldAPIError, DatafoldClient

logger = logging.getLogger(__name__)

# Terminal statuses from JobStatus enum (see datafold/models/mixins.py)
# done = success, failed = error, cancelled = user cancelled
TERMINAL_STATUSES = {"done", "failed", "cancelled"}

# Algorithm options
AlgorithmType = Literal["fetch_and_join", "join"]


async def _wait_for_datadiff(
    client: DatafoldClient,
    diff_id: int,
    timeout: int,
) -> dict[str, Any]:
    """Poll for datadiff completion and return results."""
    elapsed = 10
    poll_interval = 2
    await asyncio.sleep(elapsed)  # no need to poll for the first 5-10 seconds

    while elapsed < timeout:
        status_response = await client.get_datadiff(diff_id)
        status = status_response.get("status", "").lower()

        logger.debug(f"DataDiff {diff_id} status: {status} (elapsed: {elapsed}s)")

        if status in TERMINAL_STATUSES:
            # Fetch summary for both success and failure cases
            summary = await client.get_datadiff_summary(diff_id)
            return summary

        await asyncio.sleep(poll_interval)
        elapsed += poll_interval

    # Timeout reached
    return {
        "diff_id": diff_id,
        "status": "timeout",
        "error": f"DataDiff did not complete within {timeout} seconds",
    }


async def _guess_pk_for_table(
    client: DatafoldClient,
    data_source_id: int,
    table: list[str],
) -> list[str] | None:
    """Guess primary keys for a table, returns None on failure."""
    try:
        result = await client.guess_primary_keys(
            data_source_id=data_source_id,
            table=table,
            sample_size=5000,
            candidates=1,
        )
        if result.get("error"):
            logger.warning(f"PK guesser failed for {table}: {result['error']}")
            return None
        if result.get("candidates"):
            pk = result["candidates"][0]["pk"]
            logger.info(f"Guessed PKs for {table}: {pk}")
            return pk
        return None
    except (DatafoldAPIError, KeyError, IndexError) as e:
        logger.warning(f"PK guesser error for {table}: {e}")
        return None


# pylint: disable=too-many-statements
def register_datadiff_tools(mcp: FastMCP, client: DatafoldClient) -> None:
    """Register DataDiff related tools with the MCP server."""

    @mcp.tool(
        name="run_datadiff",
        description=(
            "Execute a comprehensive data comparison (DataDiff) between two tables or queries. "
            "Identifies differences in data values, missing rows, and extra rows. "
            "For each side, provide EITHER a table OR a query, not both. "
            "If pk_columns not provided and using tables, will auto-guess primary keys. "
            "By default, waits for completion and returns results."
        ),
        tags={"datadiff", "comparison", "data-quality"},
    )
    # pylint: disable=too-many-return-statements,too-many-branches,too-many-statements
    async def run_datadiff(
        data_source1_id: Annotated[int, "Source data source ID"],
        data_source2_id: Annotated[int, "Destination data source ID"],
        table1: Annotated[list[str] | None, "Source table path, e.g. ['schema', 'table']"] = None,
        table2: Annotated[list[str] | None, "Destination table path, e.g. ['schema', 'table']"] = None,
        query1: Annotated[str | None, "Source SQL query (alternative to table1)"] = None,
        query2: Annotated[str | None, "Destination SQL query (alternative to table2)"] = None,
        pk_columns: Annotated[
            list[str] | None,
            "Primary key columns for row matching. If not provided and using tables, will auto-guess.",
        ] = None,
        include_columns: Annotated[
            list[str] | None, "Columns to include in comparison (default: None [all])"
        ] = None,
        exclude_columns: Annotated[
            list[str] | None, "Columns to exclude from comparison"
        ] = None,
        filter1: Annotated[str | None, "SQL WHERE clause filter for source"] = None,
        filter2: Annotated[str | None, "SQL WHERE clause filter for destination"] = None,
        algorithm: Annotated[
            AlgorithmType,
            "Comparison algorithm: 'fetch_and_join' (downloads data, most accurate) or 'join' (uses DB joins, faster)",
        ] = "fetch_and_join",
        # Comparison options
        compare_duplicates: Annotated[
            bool | None, "Whether to include duplicate rows in comparison"
        ] = None,
        columns_to_compare: Annotated[
            list[str] | None, "Specific columns to compare (for hash-based algorithms)"
        ] = None,
        column_mapping: Annotated[
            list[tuple[str, str]] | None, "Map columns between datasets, e.g. [('col_a', 'col_b')]"
        ] = None,
        # Sampling configuration
        sampling_ratio: Annotated[
            float | None, "Sampling ratio 0.0-1.0 for large table comparisons"
        ] = None,
        sampling_tolerance: Annotated[
            float | None, "Statistical tolerance for sampling (0.0-1.0)"
        ] = None,
        sampling_confidence: Annotated[
            float | None, "Confidence level for sampling (0-100)"
        ] = None,
        sampling_threshold: Annotated[
            int | None, "Minimum row count to trigger sampling"
        ] = None,
        sampling_max_rows: Annotated[
            int | None, "Maximum rows to sample"
        ] = None,
        # Tolerance settings
        diff_tolerance: Annotated[
            float | None, "Numeric tolerance for value comparisons"
        ] = None,
        tolerance_mode: Annotated[
            Literal["absolute", "relative"] | None, "How to apply diff_tolerance"
        ] = None,
        datetime_tolerance: Annotated[
            int | None, "Tolerance for datetime comparisons in seconds"
        ] = None,
        # Materialization
        materialize_dataset1: Annotated[
            bool | None, "Materialize source dataset before comparison"
        ] = None,
        materialize_dataset2: Annotated[
            bool | None, "Materialize destination dataset before comparison"
        ] = None,
        materialization_destination_id: Annotated[
            int | None, "Data source ID for materialization"
        ] = None,
        materialize_without_sampling: Annotated[
            bool | None, "Skip sampling when materializing datasets"
        ] = None,
        # Tool-specific parameters
        wait_for_result: Annotated[
            bool, "If True, wait for diff to complete and return results"
        ] = True,
        timeout: Annotated[int, "Maximum seconds to wait for completion"] = 120,
    ) -> dict[str, Any]:
        """Create and run a DataDiff comparison."""
        # Validate inputs
        src_has_table = table1 is not None
        src_has_query = query1 is not None
        dst_has_table = table2 is not None
        dst_has_query = query2 is not None

        if not src_has_table and not src_has_query:
            return {"error": "Source dataset not specified. Provide either table1 or query1"}
        if src_has_table and src_has_query:
            return {"error": "Source dataset specified twice. Use either table1 or query1, not both"}
        if not dst_has_table and not dst_has_query:
            return {"error": "Destination dataset not specified. Provide either table2 or query2"}
        if dst_has_table and dst_has_query:
            return {"error": "Destination dataset specified twice. Use either table2 or query2, not both"}

        # Auto-guess PKs if not provided and using tables
        if pk_columns is None:
            if table1:
                logger.info(f"Auto-guessing PKs for source table {table1}")
                pk_columns = await _guess_pk_for_table(client, data_source1_id, table1)
            elif table2:
                logger.info(f"Auto-guessing PKs for destination table {table2}")
                pk_columns = await _guess_pk_for_table(client, data_source2_id, table2)

            if pk_columns is None:
                return {
                    "error": "pk_columns not provided and auto-guess failed. "
                    "Please provide pk_columns explicitly."
                }

        logger.info(
            f"Creating datadiff: ds1={data_source1_id}, ds2={data_source2_id}, "
            f"pk={pk_columns}, wait={wait_for_result}, timeout={timeout}s"
        )

        # Build kwargs for optional parameters - pass all non-None values to API
        kwargs: dict[str, Any] = {}

        # Basic options
        if include_columns:
            kwargs["include_columns"] = include_columns
        if exclude_columns:
            kwargs["exclude_columns"] = exclude_columns
        if filter1:
            kwargs["filter1"] = filter1
        if filter2:
            kwargs["filter2"] = filter2
        if algorithm != "fetch_and_join":
            kwargs["algorithm"] = algorithm

        # Comparison options
        if compare_duplicates is not None:
            kwargs["compare_duplicates"] = compare_duplicates
        if columns_to_compare is not None:
            kwargs["columns_to_compare"] = columns_to_compare
        if column_mapping is not None:
            kwargs["column_mapping"] = column_mapping

        # Sampling configuration
        if sampling_ratio is not None:
            kwargs["sampling_ratio"] = sampling_ratio
        if sampling_tolerance is not None:
            kwargs["sampling_tolerance"] = sampling_tolerance
        if sampling_confidence is not None:
            kwargs["sampling_confidence"] = sampling_confidence
        if sampling_threshold is not None:
            kwargs["sampling_threshold"] = sampling_threshold
        if sampling_max_rows is not None:
            kwargs["sampling_max_rows"] = sampling_max_rows

        # Tolerance settings
        if diff_tolerance is not None:
            kwargs["diff_tolerance"] = diff_tolerance
        if tolerance_mode is not None:
            kwargs["tolerance_mode"] = tolerance_mode
        if datetime_tolerance is not None:
            kwargs["datetime_tolerance"] = datetime_tolerance

        # Materialization
        if materialize_dataset1 is not None:
            kwargs["materialize_dataset1"] = materialize_dataset1
        if materialize_dataset2 is not None:
            kwargs["materialize_dataset2"] = materialize_dataset2
        if materialization_destination_id is not None:
            kwargs["materialization_destination_id"] = materialization_destination_id
        if materialize_without_sampling is not None:
            kwargs["materialize_without_sampling"] = materialize_without_sampling

        response = await client.create_datadiff(
            data_source1_id=data_source1_id,
            data_source2_id=data_source2_id,
            pk_columns=pk_columns,
            table1=table1,
            table2=table2,
            query1=query1,
            query2=query2,
            **kwargs,
        )

        diff_id = response.get("id")
        if not diff_id:
            return {"error": "Failed to create datadiff", "response": response}

        logger.info(f"Created datadiff {diff_id}")

        if not wait_for_result:
            return {"diff_id": diff_id, "status": "created", "pk_columns": pk_columns}

        result = await _wait_for_datadiff(client, diff_id, timeout)
        result["pk_columns"] = pk_columns
        return result

    @mcp.tool(
        name="datadiff_status",
        description="Check the execution status of a DataDiff comparison.",
        tags={"datadiff", "status", "monitoring"},
    )
    async def datadiff_status(
        diff_id: Annotated[int, "DataDiff ID to check"],
    ) -> dict[str, Any]:
        """Get DataDiff status and details."""
        return await client.get_datadiff(diff_id)

    @mcp.tool(
        name="datadiff_summary",
        description=(
            "Get a human-readable summary of a DataDiff comparison. "
            "Includes status, configuration, results statistics, and detailed feedback. "
            "Recommended over datadiff_results for understanding diff outcomes."
        ),
        tags={"datadiff", "results", "summary"},
    )
    async def datadiff_summary(
        diff_id: Annotated[int, "DataDiff ID"],
    ) -> dict[str, Any]:
        """Get human-readable DataDiff summary with feedback."""
        return await client.get_datadiff_summary(diff_id)
