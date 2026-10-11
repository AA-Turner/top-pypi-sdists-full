"""Shared finalize logic for Rows and Cells write responses."""

from typing import TYPE_CHECKING, Optional, Union

import pandas as pd

from intapp_rest_client.models import ErrorHandling

from ..utils.process_response_errors import process_errors
from .converters import convert_to_output_format
from .models import BatchResult, RowsWriteResult

if TYPE_CHECKING:
    import polars as pl


def finalize_write_result(
    ok_rows: list,
    row_error_rows: list,
    all_errors: list,
    total_requested: int,
    *,
    failed_inputs: Optional[list] = None,
    raise_on_row_errors: bool,
    output: str,
    error_handling: ErrorHandling,
    transport_failure_count: Optional[int] = None,
    total_succeeded: Optional[int] = None,
) -> Union[list, pd.DataFrame, "pl.DataFrame", BatchResult, RowsWriteResult]:
    """Process permanent row errors and build return value or BatchResult."""
    process_errors(row_error_rows, raise_on_row_errors=raise_on_row_errors)
    failed_inputs = failed_inputs or []

    if output == "write_result":
        if error_handling != ErrorHandling.FAIL_FAST:
            raise ValueError(
                "output='write_result' is only supported with error_handling=FAIL_FAST"
            )
        return RowsWriteResult(
            rows=ok_rows + row_error_rows,
            ok_rows=ok_rows,
            row_errors=row_error_rows,
            failed_inputs=failed_inputs,
        )

    if error_handling != ErrorHandling.FAIL_FAST:
        transport_failed = (
            transport_failure_count
            if transport_failure_count is not None
            else len(all_errors)
        )
        succeeded = total_succeeded if total_succeeded is not None else len(ok_rows)
        return BatchResult(
            results=(
                convert_to_output_format(ok_rows, output)
                if output != "list"
                else ok_rows
            ),
            errors=all_errors,
            row_errors=row_error_rows,
            total_requested=total_requested,
            total_succeeded=succeeded,
            total_failed=transport_failed + len(row_error_rows),
        )

    return convert_to_output_format(ok_rows, output)
