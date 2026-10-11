"""Data write operations (insert, update, delete, upsert)."""

from typing import TYPE_CHECKING, Callable, Optional, Union
import pandas as pd

from ..constants.data import DATA_READ_WORKER_COUNT
from ..utils.data_utils import calculate_pagination, divide_pages, format_data
from ..utils.process_response_errors import resolve_raise_on_row_errors

from .converters import OutputFormat, convert_to_output_format
from intapp_rest_client.models import ErrorHandling

from .finalize import finalize_write_result
from .models import BatchResult, RowsWriteResult
from .write_recovery import assign_insert_entry_ids, recover_payloads, recover_payload_write

if TYPE_CHECKING:
    import polars as pl
    from .dealcloud_data import DealCloudData


def _delete_transport_failure_count(errors: list, delete_batches: list[list]) -> int:
    """Count entry IDs that failed due to transport errors on DELETE batches."""
    total = 0
    for err in errors:
        if isinstance(err, dict) and "payload_index" in err:
            idx = err["payload_index"]
            if 0 <= idx < len(delete_batches):
                total += len(delete_batches[idx])
        elif delete_batches:
            total += len(delete_batches[0])
        else:
            total += 1
    return total


def _merge_upsert_results(
    left: Union[list, pd.DataFrame, "pl.DataFrame", BatchResult, RowsWriteResult],
    right: Union[list, pd.DataFrame, "pl.DataFrame", BatchResult, RowsWriteResult],
    *,
    output: str,
    total_requested: int,
) -> Union[list, pd.DataFrame, "pl.DataFrame", BatchResult, RowsWriteResult]:
    """Combine insert and update upsert partial results."""
    if isinstance(left, BatchResult):
        if not isinstance(right, BatchResult):
            raise TypeError("upsert insert/update results must both be BatchResult")
        return BatchResult(
            results=left.results + right.results,
            errors=left.errors + right.errors,
            row_errors=left.row_errors + right.row_errors,
            total_requested=total_requested,
            total_succeeded=left.total_succeeded + right.total_succeeded,
            total_failed=left.total_failed + right.total_failed,
        )
    if isinstance(left, RowsWriteResult):
        if not isinstance(right, RowsWriteResult):
            raise TypeError("upsert insert/update results must both be RowsWriteResult")
        return RowsWriteResult(
            rows=left.rows + right.rows,
            ok_rows=left.ok_rows + right.ok_rows,
            row_errors=left.row_errors + right.row_errors,
            failed_inputs=left.failed_inputs + right.failed_inputs,
        )
    if output == "list":
        return list(left) + list(right)
    if isinstance(left, pd.DataFrame):
        return pd.concat([left, right], ignore_index=True)
    import polars as pl

    if isinstance(left, pl.DataFrame):
        return pl.concat([left, right])
    raise TypeError(f"Cannot merge upsert results with output={output!r}")


def validate_field_mapping(
    self: "DealCloudData",
    object_api_name: str,
    columns: Union[set[str], list[str]],
) -> bool:
    """
    Validate that column names exist in a DealCloud object.
    
    Use this for pre-flight validation before attempting insert/update
    operations. Get clear error messages upfront rather than mid-batch failures.
    
    Args:
        self: DealCloudData instance
        object_api_name: Object API name (e.g., "Company")
        columns: Column names to validate (set or list)
    
    Returns:
        True if all columns are valid
    
    Raises:
        KeyError: If any columns don't exist, lists the invalid columns
    
    Example:
        >>> # Validate before import
        >>> df = pd.read_csv("import_data.csv")
        >>> try:
        ...     dc.validate_field_mapping("Company", set(df.columns))
        ...     print("All columns valid!")
        ...     dc.insert_data("Company", df)
        ... except KeyError as e:
        ...     print(f"Invalid columns: {e}")
        
        >>> # Check programmatically
        >>> columns = {"Name", "Status", "InvalidField"}
        >>> try:
        ...     dc.validate_field_mapping("Company", columns)
        ... except KeyError as e:
        ...     invalid = str(e)  # Contains list of invalid fields
        ...     print(f"Please fix these columns: {invalid}")
    
    Note:
        "EntryId" is always considered valid even though it's not a field.
    """
    if isinstance(columns, list):
        columns = set(columns)
    
    fields = self.get_fields(object_api_name)
    column_names = ["EntryId"] + [f.apiName for f in fields if f.apiName]
    invalid = [c for c in columns if c not in column_names]
    if invalid:
        raise KeyError(f"Mapping error, could not map: {invalid}")
    
    return True


def insert_data(
    self: "DealCloudData",
    object_api_name: str,
    data: Union[list[dict], pd.DataFrame, "pl.DataFrame"],
    use_dealcloud_ids: bool = True,
    lookup_column: Optional[str] = None,
    output: str = "list",
    progress_callback: Optional[Callable[[int, int], None]] = None,
    error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    raise_on_row_errors: Optional[bool] = None,
) -> Union[list[dict], pd.DataFrame, "pl.DataFrame", BatchResult, RowsWriteResult]:
    """
    Insert data into DealCloud.
    
    Args:
        self: DealCloudData instance
        object_api_name: API name of the object
        data: Data to insert. Accepts:
              - list[dict]
              - pandas.DataFrame
              - polars.DataFrame (requires: pip install dealcloud-sdk[polars])
        use_dealcloud_ids: Use DealCloud IDs for references
        lookup_column: Column to use for lookup
        output: Output format:
               - "list": List of dictionaries (default)
               - "write_result": :class:`RowsWriteResult` with ``rows``, ``ok_rows``, ``row_errors``
               - "pandas": pandas DataFrame
               - "polars": Polars DataFrame (requires: pip install dealcloud-sdk[polars])
        progress_callback: Optional callback (current, total)
        error_handling: Parallel **transport** error behavior (FAIL_FAST, COLLECT, LOG_ONLY).
            Does not control row-level ``Errors`` in HTTP 200 responses.
        raise_on_row_errors: When True, raise after recovery if any row could not be committed.
            When None, uses ``DealCloudConfig.raiseOnRowErrors``.

    Returns:
        Insert results in requested format. Committed rows only for ``output="list"``.
        Permanent row failures are logged and included in ``output="write_result"`` /
        ``BatchResult.row_errors``. Rows writes automatically split indexed row errors
        and retry clean rows once per HTTP payload (all-or-none batch semantics).
    
    Example:
        >>> import polars as pl
        >>> df = pl.DataFrame({"Name": ["Acme", "Beta"], "Revenue": [1000, 2000]})
        >>> result = dc.insert_data("Company", df, output="polars")
    """
    data, columns = format_data(data)
    validate_field_mapping(self, object_api_name, columns)

    payloads = calculate_pagination(data, columns, self.cell_pagination_limit)
    total_payloads = len(payloads)
    url = f"{self._rows_url}/{object_api_name}"
    worker_count = min(DATA_READ_WORKER_COUNT, self.create_concurrency)

    def send_once(payload: list[dict]) -> object:
        return self._client.post(url, json=payload)

    recovery = recover_payloads(
        [list(p) for p in payloads],
        send_once,
        is_insert=True,
        assign_entry_ids=assign_insert_entry_ids,
        max_workers=worker_count,
        error_handling=error_handling,
    )

    if progress_callback:
        try:
            progress_callback(total_payloads, total_payloads)
        except Exception as e:
            self._logger.warning(f"Progress callback failed: {e}")

    resolved_raise = resolve_raise_on_row_errors(
        self._raise_on_row_errors_default, raise_on_row_errors
    )
    return finalize_write_result(
        recovery.ok_rows,
        recovery.row_errors,
        recovery.transport_errors,
        len(data),
        failed_inputs=recovery.failed_inputs,
        raise_on_row_errors=resolved_raise,
        output=output,
        error_handling=error_handling,
    )


def update_data(
    self: "DealCloudData",
    object_api_name: str,
    data: Union[list[dict], pd.DataFrame, "pl.DataFrame"],
    use_dealcloud_ids: bool = True,
    lookup_column: Optional[str] = None,
    output: str = "list",
    progress_callback: Optional[Callable[[int, int], None]] = None,
    error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    raise_on_row_errors: Optional[bool] = None,
) -> Union[list[dict], pd.DataFrame, "pl.DataFrame", BatchResult, RowsWriteResult]:
    """
    Update data in DealCloud.
    
    Args:
        self: DealCloudData instance
        object_api_name: API name of the object
        data: Data to update. Accepts:
              - list[dict]
              - pandas.DataFrame
              - polars.DataFrame (requires: pip install dealcloud-sdk[polars])
        use_dealcloud_ids: Use DealCloud IDs for references
        lookup_column: Column to use for lookup
        output: Output format:
               - "list": List of dictionaries (default)
               - "write_result": :class:`RowsWriteResult`
               - "pandas": pandas DataFrame
               - "polars": Polars DataFrame (requires: pip install dealcloud-sdk[polars])
        progress_callback: Optional callback (current, total)
        error_handling: Parallel **transport** error behavior. Does not control row
            ``Errors`` in HTTP 200 responses.
        raise_on_row_errors: When True, raise after recovery if any row could not be committed.
            When None, uses ``DealCloudConfig.raiseOnRowErrors``.

    Returns:
        Update results in requested format. Committed rows only for ``output="list"``.
        Rows writes automatically split indexed row errors and retry clean rows once
        per HTTP payload (all-or-none batch semantics).
    
    Example:
        >>> import polars as pl
        >>> df = pl.DataFrame({"EntryId": [123, 456], "Revenue": [1500, 2500]})
        >>> result = dc.update_data("Company", df, output="polars")
    """
    data, columns = format_data(data)
    validate_field_mapping(self, object_api_name, columns)
    payloads = calculate_pagination(data, columns, self.cell_pagination_limit)
    total_payloads = len(payloads)
    url = f"{self._rows_url}/{object_api_name}"
    worker_count = min(DATA_READ_WORKER_COUNT, self.create_concurrency)

    def send_once(payload: list[dict]) -> object:
        return self._client.put(url, json=payload)

    recovery = recover_payloads(
        [list(p) for p in payloads],
        send_once,
        is_insert=False,
        max_workers=worker_count,
        error_handling=error_handling,
    )

    if progress_callback:
        try:
            progress_callback(total_payloads, total_payloads)
        except Exception as e:
            self._logger.warning(f"Progress callback failed: {e}")

    total_requested = len(data) if isinstance(data, list) else len(data)
    resolved_raise = resolve_raise_on_row_errors(
        self._raise_on_row_errors_default, raise_on_row_errors
    )
    return finalize_write_result(
        recovery.ok_rows,
        recovery.row_errors,
        recovery.transport_errors,
        total_requested,
        failed_inputs=recovery.failed_inputs,
        raise_on_row_errors=resolved_raise,
        output=output,
        error_handling=error_handling,
    )


def upsert_data(
    self: "DealCloudData",
    object_api_name: str,
    data: Union[list[dict], pd.DataFrame, "pl.DataFrame"],
    use_dealcloud_ids: bool = True,
    lookup_column: Optional[str] = None,
    output: str = "list",
    progress_callback: Optional[Callable[[int, int], None]] = None,
    error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    raise_on_row_errors: Optional[bool] = None,
) -> Union[list[dict], pd.DataFrame, "pl.DataFrame", BatchResult, RowsWriteResult]:
    """
    Insert or update data based on EntryId presence.
    
    Args:
        self: DealCloudData instance
        object_api_name: API name of the object
        data: Data to upsert. Accepts:
              - list[dict]
              - pandas.DataFrame
              - polars.DataFrame (requires: pip install dealcloud-sdk[polars])
        use_dealcloud_ids: Use DealCloud IDs for references
        lookup_column: Column to use for lookup
        output: Output format:
               - "list": List of dictionaries (default)
               - "write_result": :class:`RowsWriteResult`
               - "pandas": pandas DataFrame
               - "polars": Polars DataFrame (requires: pip install dealcloud-sdk[polars])
        progress_callback: Optional callback (current, total)
        error_handling: Parallel **transport** error behavior for insert/update paths.
        raise_on_row_errors: When True, raise on row-level ``Errors`` in HTTP 200 body.
            When None, uses ``DealCloudConfig.raiseOnRowErrors``.
    
    Returns:
        Upsert results in requested format. If error_handling=COLLECT, returns BatchResult.
    
    Example:
        >>> import polars as pl
        >>> df = pl.DataFrame({
        ...     "EntryId": [123, None],  # 123 will update, None will insert
        ...     "Name": ["Updated Corp", "New Corp"],
        ... })
        >>> result = dc.upsert_data("Company", df, output="polars")
    """
    data, columns = format_data(data)
    validate_field_mapping(self, object_api_name, columns)

    inserts = [dict(r) for r in data if not r.get("EntryId")]
    updates = [dict(r) for r in data if r.get("EntryId")]

    common_kwargs = dict(
        use_dealcloud_ids=use_dealcloud_ids,
        lookup_column=lookup_column,
        output=output,
        progress_callback=progress_callback,
        error_handling=error_handling,
        raise_on_row_errors=raise_on_row_errors,
    )

    if not inserts and not updates:
        if error_handling != ErrorHandling.FAIL_FAST:
            return BatchResult(total_requested=0, total_succeeded=0)
        if output == "write_result":
            return RowsWriteResult()
        return convert_to_output_format([], output)

    result = None
    if inserts:
        result = insert_data(self, object_api_name, inserts, **common_kwargs)
    if updates:
        update_result = update_data(self, object_api_name, updates, **common_kwargs)
        if result is None:
            result = update_result
        else:
            result = _merge_upsert_results(
                result,
                update_result,
                output=output,
                total_requested=len(data),
            )
    return result


def delete_data(
    self: "DealCloudData",
    object_api_name: str,
    records: list[int],
    page_size: Optional[int] = None,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    raise_on_row_errors: Optional[bool] = None,
) -> Union[list[dict], BatchResult]:
    """
    Delete data from DealCloud.

    When there are multiple batches (records exceed page_size), deletes are executed
    in parallel up to ``delete_concurrency``. With multiple batches, progress_callback
    may be invoked once at the end.

    Args:
        self: DealCloudData instance
        object_api_name: API name of the object
        records: List of entry IDs to delete
        page_size: Batch size for deletes
        progress_callback: Optional callback (current, total)
        error_handling: Parallel **transport** error behavior. Does not control row
            ``Errors`` in HTTP 200 responses.
        raise_on_row_errors: When True, raise on row-level ``Errors`` in HTTP 200 body.
            When None, uses ``DealCloudConfig.raiseOnRowErrors``.

    Returns:
        Delete results. If error_handling=COLLECT or LOG_ONLY, returns BatchResult.
    """
    resolved_raise = resolve_raise_on_row_errors(
        self._raise_on_row_errors_default, raise_on_row_errors
    )

    if not records:
        if error_handling != ErrorHandling.FAIL_FAST:
            return BatchResult(total_requested=0, total_succeeded=0)
        return []

    # Use configured delete page size
    if page_size is None:
        page_size = self.delete_page_size

    # Validate and cap page size (API performance limits)
    if page_size > 10000:
        import warnings
        warnings.warn(
            f"page_size {page_size} exceeds maximum of 10000. Capping to 10000.",
            UserWarning
        )
        page_size = 10000
    if page_size < 1:
        raise ValueError("page_size must be at least 1")

    url = f"{self._entrydata_url}/{object_api_name}"
    delete_batches = list(divide_pages(records, page_size))
    total_batches = len(delete_batches)
    virtual_payloads = [[{"EntryId": eid} for eid in batch] for batch in delete_batches]

    def send_once(virtual_rows: list[dict]) -> object:
        entry_ids = [row["EntryId"] for row in virtual_rows]
        return self._client.delete(url, json=entry_ids)

    recovery = recover_payloads(
        virtual_payloads,
        send_once,
        is_insert=False,
        max_workers=self.delete_concurrency if total_batches > 1 else 1,
        error_handling=error_handling,
    )

    if progress_callback:
        try:
            progress_callback(total_batches, total_batches)
        except Exception as e:
            self._logger.warning(f"Progress callback failed: {e}")

    transport_failed = (
        _delete_transport_failure_count(recovery.transport_errors, delete_batches)
        if recovery.transport_errors
        else None
    )
    return finalize_write_result(
        recovery.ok_rows,
        recovery.row_errors,
        recovery.transport_errors,
        len(records),
        failed_inputs=recovery.failed_inputs,
        raise_on_row_errors=resolved_raise,
        output="list",
        error_handling=error_handling,
        transport_failure_count=transport_failed,
    )
