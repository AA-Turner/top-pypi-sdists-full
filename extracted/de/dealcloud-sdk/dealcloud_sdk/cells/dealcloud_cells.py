"""
Cells API operations for DealCloud.

The Cells API provides cell-level data operations, as opposed to the Rows API
which operates on entire rows. This is useful for:
- Reading/writing specific fields without fetching entire records
- More granular control over data operations
- Better performance when only specific fields are needed

See: https://api.docs.dealcloud.com/docs - Data/Cells API
"""

from typing import Literal, Optional, Union, List, Dict, Any, Callable
from functools import partial

import pandas as pd

from intapp_rest_client.models import ErrorHandling

from ..data.dealcloud_data import DealCloudData
from ..data.finalize import finalize_write_result
from ..data.models import BatchResult, RowsWriteResult
from ..data.write_recovery import assign_insert_entry_ids, recover_payloads
from ..utils.data_utils import divide_pages, format_data
from ..utils.process_response_errors import process_errors, resolve_raise_on_row_errors, split_cell_store_results, split_row_results

# API docs: max 10,000 fields per POST entrydata/get request
GET_CELLS_FIELD_LIMIT = 10_000


def _build_store_requests(
    rows: list[dict],
    field_map: dict[str, int],
    data_columns: list[str],
) -> list[dict[str, Any]]:
    store: list[dict[str, Any]] = []
    for row in rows:
        entry_id = row.get("EntryId")
        if entry_id is None:
            continue
        for col in data_columns:
            if col not in field_map:
                continue
            value = row.get(col)
            if value is None:
                continue
            store.append(
                {
                    "entryId": int(entry_id),
                    "fieldId": field_map[col],
                    "value": value,
                }
            )
    return store


def _batch_rows_by_cell_limit(
    data: list[dict],
    field_map: dict[str, int],
    data_columns: list[str],
    cell_limit: int,
) -> list[list[dict]]:
    batches: list[list[dict]] = []
    current_batch: list[dict] = []
    current_cells = 0
    for row in data:
        row_cell_count = sum(
            1
            for col in data_columns
            if col in field_map and row.get(col) is not None
        )
        if row_cell_count == 0:
            continue
        if current_cells + row_cell_count > cell_limit and current_batch:
            batches.append(current_batch)
            current_batch = []
            current_cells = 0
        current_batch.append(row)
        current_cells += row_cell_count
    if current_batch:
        batches.append(current_batch)
    return batches


def _normalize_cells_response(response: object) -> list[dict]:
    if isinstance(response, list):
        return [item for item in response if isinstance(item, dict)]
    if isinstance(response, dict):
        return [response]
    return []

# Type hints for optional polars
try:
    import polars as pl
except ImportError:  # pragma: no cover
    pl = None  # type: ignore


class DealCloudCells(DealCloudData):
    """
    One link in the linear inheritance chain; parent order is for composition
    (single DealCloud client gets all features), not dependency. Avoids mixins.
    Cells API operations.
    
    Provides cell-level data operations for fine-grained control.
    """
    
    @property
    def cells_url(self) -> str:
        """
        Get the Cells API base URL.
        
        Use this for custom cell-level API calls not covered by SDK methods.
        
        Returns:
            str: Cells API URL (e.g., "https://site.dealcloud.com/api/rest/v4/data/entrydata")
        
        Example:
            >>> # Custom cells endpoint call
            >>> url = f"{dc.cells_url}/{object_id}/custom"
            >>> response = dc.client.get(url)
        """
        return self._cells_url
    
    # =========================================================================
    # Cell Read Operations
    # =========================================================================
    
    def get_cells(
        self,
        object_id: Union[int, str],
        entry_ids: Optional[List[int]] = None,
        fields: Optional[Union[List[int], List[str]]] = None,
        *,
        resolve_reference_url: bool = False,
        fill_extended_data: bool = False,
        wrap_into_arrays: bool = False,
        date_time_behavior: Optional[int] = None,
        currency_code: Optional[str] = None,
    ) -> List[dict]:
        """
        Get cell-level data for specific entries and/or fields.

        Uses POST .../entrydata/get (no path param; body is array of DataReadRequest
        with entryId, fieldId, optional currencyCode). Max 10,000 fields per request.
        object_id is not sent to the API; it is used only to resolve entry_ids (via
        list_entries) and fields (via get_fields) when not provided.

        Args:
            object_id: Entry type ID or API name; used only to resolve entry_ids/fields when needed.
            entry_ids: Optional list of entry IDs; if None, list_entries(object_id) is used.
            fields: Optional list of field IDs (int) or field API names (str). If None, all fields are used.
            resolve_reference_url: Query param (default false). Resolve reference URLs.
            fill_extended_data: Query param (default false). Fill extended data.
            wrap_into_arrays: Query param (default false). Wrap values into arrays.
            date_time_behavior: Query param. Enum (0 or 1) for date/time handling.
            currency_code: Optional. Set on each DataReadRequest for currency-dependent fields.
        """
        # Resolve entry IDs: use provided or list all for the object
        if entry_ids is None:
            entry_ids = self.list_entries(object_id)
        if not entry_ids:
            return []

        # Resolve fields to field IDs (fields: list of int = IDs, list of str = API names)
        if fields is None:
            field_list = self.get_fields(object_id)
            field_ids = [f.id for f in field_list if f.id is not None]
        elif not fields:
            field_ids = []
        elif isinstance(fields[0], int):
            field_ids = list(fields)
        else:
            field_list = self.get_fields(object_id)
            name_to_id = {f.apiName: f.id for f in field_list if f.apiName and f.id is not None}
            field_ids = [name_to_id[name] for name in fields if name in name_to_id]
        if not field_ids:
            return []

        # Build DataReadRequest array: one item per (entry_id, field_id); optional currencyCode
        requests: List[Dict[str, Any]] = []
        for eid in entry_ids:
            for fid in field_ids:
                req: Dict[str, Any] = {"entryId": eid, "fieldId": fid}
                if currency_code is not None:
                    req["currencyCode"] = currency_code
                requests.append(req)

        # Query params per swagger (only send when non-default or set)
        params: Dict[str, Any] = {}
        if resolve_reference_url:
            params["resolveReferenceUrl"] = True
        if fill_extended_data:
            params["fillExtendedData"] = True
        if wrap_into_arrays:
            params["wrapIntoArrays"] = True
        if date_time_behavior is not None:
            params["dateTimeBehavior"] = date_time_behavior

        # Chunk to stay under API limit of 10,000 fields per request
        out: List[dict] = []
        for chunk in divide_pages(requests, GET_CELLS_FIELD_LIMIT):
            url = f"{self._cells_url}/get"
            response = self._client.post(
                url,
                json=chunk,
                params=params if params else None,
            )
            if isinstance(response, list):
                out.extend(response)
            else:
                out.append(response)
        return out
    
    def list_entries(
        self,
        object_id: Union[int, str],
        limit: Optional[int] = None,
        skip: Optional[int] = None,
    ) -> List[int]:
        """
        List entry IDs for an object.

        Uses GET .../entrydata/{entryTypeId}/entries (returns NamedEntryVm[]).
        Swagger defines no query parameters; the API returns all entries (no pagination).
        Optional limit/skip are applied client-side after fetching.

        For entries modified since a date, use get_history() (history module).
        For criteria-based listing, use list_entries_with_filter().

        Args:
            object_id: Object ID or API name.
            limit: Optional max number of entry IDs to return (client-side).
            skip: Optional number of entry IDs to skip (client-side).
        """
        url = f"{self._cells_url}/{object_id}/entries"
        response = self._client.get(url)
        if not isinstance(response, list):
            response = response.get("entryIds", []) if isinstance(response, dict) else []
        # Each item is NamedEntryVm: { id, name, entryListId }; fallback to int if raw id list
        ids = []
        for item in response:
            if isinstance(item, dict) and "id" in item:
                ids.append(item["id"])
            elif isinstance(item, int):
                ids.append(item)
        if skip is not None:
            ids = ids[skip:]
        if limit is not None:
            ids = ids[:limit]
        return ids
    
    def list_entries_with_filter(
        self,
        object_id: Union[int, str],
        filters: List[dict],
    ) -> List[int]:
        """
        List entry IDs using filter criteria.

        Uses POST .../entrydata/{entryTypeId}/filter. Each filter dict should
        have fieldId, value, and filterOperation (or operator, mapped to filterOperation).
        """
        url = f"{self._cells_url}/{object_id}/filter"
        # Normalize filter shape: API expects filterOperation; accept operator for backward compat
        body = []
        for f in filters:
            d = dict(f)
            if "operator" in d and "filterOperation" not in d:
                d["filterOperation"] = d.pop("operator")
            body.append(d)
        response = self._client.post(url, json=body)
        return response if isinstance(response, list) else []
    
    # =========================================================================
    # Cell Write Operations
    # =========================================================================
    
    def write_cells(
        self,
        object_id: Union[int, str],
        data: Union[List[dict], pd.DataFrame, "pl.DataFrame"],
        mode: Literal["create", "update", "upsert"] = "upsert",
        *,
        output: str = "list",
        error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
        raise_on_row_errors: Optional[bool] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Union[List[dict], BatchResult, RowsWriteResult]:
        """
        Write cell data with specified mode.
        
        Args:
            object_id: Object ID or API name
            data: Cell data to write. Accepts:
                  - list[dict]: Direct cell data
                  - pandas.DataFrame: Converted automatically
                  - polars.DataFrame: Converted automatically (requires: pip install dealcloud-sdk[polars])
                  
                  Format:
                  [
                      {
                          "EntryId": 123,  # Positive for update, negative for create
                          "FieldApiName": value,
                          ...
                      }
                  ]
            mode: Operation mode:
                - "create": Insert new records (EntryId must be negative)
                - "update": Update existing records (EntryId must be positive)
                - "upsert": Insert or update based on EntryId
            output: ``"list"`` (default) or ``"write_result"`` for :class:`RowsWriteResult`.
            error_handling: Parallel **transport** error behavior for batched cell writes.
                Does not control row ``Errors`` in HTTP 200 responses.
            raise_on_row_errors: When True, raise on row-level ``Errors`` in HTTP 200 body.
                When None, uses ``DealCloudConfig.raiseOnRowErrors``.
            progress_callback: Optional callback (completed_batches, total_batches).
        
        Returns:
            List of results, :class:`RowsWriteResult`, or :class:`BatchResult` when
            ``error_handling=COLLECT``.
        
        Example:
            # Create new records from list
            results = dc.write_cells("Company", [
                {"EntryId": -1, "Name": "New Company", "Status": [1]},
                {"EntryId": -2, "Name": "Another Company", "Status": [2]},
            ], mode="create")
            
            # Update from polars DataFrame
            import polars as pl
            df = pl.DataFrame({"EntryId": [123, 456], "Status": [[2], [3]]})
            results = dc.write_cells("Company", df, mode="update")
        """
        if output not in ("list", "write_result"):
            raise ValueError("write_cells output must be 'list' or 'write_result'")

        url = f"{self._cells_url}/{object_id}"

        # Convert to list[dict] and get column set
        data, columns = format_data(data)

        # Validate mode
        if mode == "create":
            for row in data:
                if row.get("EntryId", 0) > 0:
                    raise ValueError("For 'create' mode, all EntryIds must be negative")
        elif mode == "update":
            for row in data:
                if row.get("EntryId", 0) <= 0:
                    raise ValueError("For 'update' mode, all EntryIds must be positive")

        # Resolve column names (excluding EntryId) to field IDs
        data_columns = [c for c in columns if c != "EntryId"]
        field_map: Dict[str, int] = {}
        for col in data_columns:
            field = self.get_field_by_api_name(object_id, col)
            if field and field.id is not None:
                field_map[col] = field.id

        # Batch rows (do not split an entry across HTTP payloads)
        cell_limit = self.cell_pagination_limit
        row_batches = _batch_rows_by_cell_limit(data, field_map, data_columns, cell_limit)

        if not row_batches:
            if error_handling != ErrorHandling.FAIL_FAST:
                return BatchResult(total_requested=0, total_succeeded=0)
            if output == "write_result":
                return RowsWriteResult()
            return []

        worker_count = min(len(row_batches), self.create_concurrency)

        def send_once(rows: list[dict]) -> list[dict]:
            body = {"storeRequests": _build_store_requests(rows, field_map, data_columns)}
            if mode == "create":
                return _normalize_cells_response(self._client.post(url, json=body))
            return _normalize_cells_response(self._client.put(url, json=body))

        split_fn = partial(split_cell_store_results, is_create=(mode == "create"))
        recovery = recover_payloads(
            row_batches,
            send_once,
            is_insert=(mode == "create"),
            assign_entry_ids=assign_insert_entry_ids if mode == "create" else None,
            max_workers=worker_count,
            error_handling=error_handling,
            split_results=split_fn,
        )

        if progress_callback:
            try:
                progress_callback(len(row_batches), len(row_batches))
            except Exception as e:
                self._logger.warning(f"Progress callback failed: {e}")

        resolved_raise = resolve_raise_on_row_errors(
            self._raise_on_row_errors_default, raise_on_row_errors
        )
        row_error_rows = recovery.row_errors
        rows_succeeded = max(0, len(data) - len(row_error_rows))
        return finalize_write_result(
            recovery.ok_rows,
            row_error_rows,
            recovery.transport_errors,
            len(data),
            failed_inputs=recovery.failed_inputs,
            raise_on_row_errors=resolved_raise,
            output=output,
            error_handling=error_handling,
            total_succeeded=rows_succeeded,
        )
    
    def delete_cells(
        self,
        object_id: Union[int, str],
        entry_ids: List[int],
        field_ids: Optional[List[int]] = None,
        *,
        error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
        raise_on_row_errors: Optional[bool] = None,
    ) -> Union[List[dict], BatchResult]:
        """
        Delete entries by ID (Cells DELETE endpoint).

        Per Swagger, DELETE body is an array of entry IDs (int32) only; field_ids
        is not supported by the API and is ignored. To remove only certain field
        values, use update_cells or the Rows API.

        Args:
            object_id: Object ID or API name
            entry_ids: Entry IDs to delete
            field_ids: Ignored by the API (kept for compatibility)
            error_handling: **Transport** error behavior (mirrors ``delete_data`` single batch).
            raise_on_row_errors: When True, raise on row ``Errors`` in HTTP 200 body.
                When None, uses ``DealCloudConfig.raiseOnRowErrors``.
        """
        resolved_raise = resolve_raise_on_row_errors(
            self._raise_on_row_errors_default, raise_on_row_errors
        )

        if not entry_ids:
            if error_handling != ErrorHandling.FAIL_FAST:
                return BatchResult(total_requested=0, total_succeeded=0)
            return []

        url = f"{self._cells_url}/{object_id}"
        all_results: List[dict] = []
        all_errors: list = []
        try:
            result = self._client.delete(url, json=entry_ids)
            if isinstance(result, list):
                all_results.extend(result)
            else:
                all_results.append(result)
        except Exception as e:
            if error_handling == ErrorHandling.FAIL_FAST:
                raise
            all_errors.append(e)

        transport_failed = len(entry_ids) if all_errors else None
        ok_rows, row_error_rows = split_row_results(all_results)
        return finalize_write_result(
            ok_rows,
            row_error_rows,
            all_errors,
            len(entry_ids),
            raise_on_row_errors=resolved_raise,
            output="list",
            error_handling=error_handling,
            transport_failure_count=transport_failed,
        )
    
    # =========================================================================
    # DMS Backlink Operations
    # =========================================================================
    
    def _resolve_field_id(
        self,
        object_id: Union[int, str],
        field_identifier: Union[int, str],
    ) -> int:
        """
        Resolve a field identifier (ID, API name, or display name) to a field ID.
        
        Args:
            object_id: Object ID or API name
            field_identifier: Field ID (int), API name (str), or display name (str)
        
        Returns:
            Field ID as integer
        
        Raises:
            ValueError: If field cannot be found
        """
        # If already an integer, return as-is
        if isinstance(field_identifier, int):
            return field_identifier
        
        # Try API name first
        field = self.get_field_by_api_name(object_id, field_identifier)
        if field and field.id:
            return field.id
        
        # Try display name
        field = self.get_field_by_name(object_id, field_identifier)
        if field and field.id:
            return field.id
        
        raise ValueError(
            f"Field '{field_identifier}' not found in object '{object_id}'. "
            "Provide a field ID, API name, or display name."
        )
    
    def backlink_dms_document(
        self,
        object_id: Union[int, str],
        title_field: Union[int, str],
        title_value: str,
        binary_field: Union[int, str],
        format_type: str,
        document_storage_id: str,
        additional_fields: Optional[Dict[Union[int, str], Any]] = None,
        raise_on_row_errors: Optional[bool] = None,
    ) -> dict:
        """
        Backlink a DMS document to DealCloud.
        
        This method creates a new entry in the Documents object (or specified object)
        and links it to an existing document in an external DMS system (Box, SharePoint,
        iManage, etc.).
        
        See: https://api.docs.dealcloud.com/guides/how_to_backlink_docs
        
        Args:
            object_id: Entry type ID or API name (typically "Documents" or "Attachments")
            title_field: Field ID, API name, or display name for the document title
            title_value: Title/name of the document
            binary_field: Field ID, API name, or display name for the binary/document field
            format_type: File format (e.g., "pdf", "docx", "xlsx", "pptx")
            document_storage_id: DMS document ID
                - SharePoint format: "SiteID | DriveID | ItemID"
                - Box/Dropbox format: Document ID
            additional_fields: Optional dict of additional field values to set
                Format: {field_id_or_name: value}
            raise_on_row_errors: When True, raise on row ``Errors`` in HTTP 200 body.
                When None, uses ``DealCloudConfig.raiseOnRowErrors``. For ``COLLECT`` or
                ``output='write_result'``, use ``write_cells`` or Rows APIs instead.
        
        Returns:
            Created entry result with EntryId
        
        Example:
            >>> # Backlink a SharePoint document
            >>> result = dc.backlink_dms_document(
            ...     object_id="Documents",
            ...     title_field="Name",  # or field ID: 374033
            ...     title_value="My Document",
            ...     binary_field="Document",  # or field ID: 374040
            ...     format_type="pdf",
            ...     document_storage_id="site.com,guid1,guid2 | drive!id | itemid"
            ... )
            >>> print(f"Created entry: {result['EntryId']}")
            
            >>> # With additional fields
            >>> result = dc.backlink_dms_document(
            ...     object_id="Documents",
            ...     title_field="Name",
            ...     title_value="Contract.pdf",
            ...     binary_field="Document",
            ...     format_type="pdf",
            ...     document_storage_id="box_document_id_12345",
            ...     additional_fields={
            ...         "Category": [1],  # Choice field
            ...         "Status": "Active"
            ...     }
            ... )
        """
        # Resolve field identifiers to field IDs
        title_field_id = self._resolve_field_id(object_id, title_field)
        binary_field_id = self._resolve_field_id(object_id, binary_field)
        
        # Build storeRequests array
        store_requests = [
            {
                "entryId": -1,  # -1 indicates new entry
                "fieldId": title_field_id,
                "value": title_value
            }
        ]
        
        # Add additional fields to storeRequests
        if additional_fields:
            for field_identifier, value in additional_fields.items():
                field_id = self._resolve_field_id(object_id, field_identifier)
                store_requests.append({
                    "entryId": -1,
                    "fieldId": field_id,
                    "value": value
                })
        
        # Build binaryStoreRequests array
        binary_store_requests = [
            {
                "entryId": -1,
                "fieldId": binary_field_id,
                "formatType": format_type,
                "documentStorageId": document_storage_id
            }
        ]
        
        # Build payload
        payload = {
            "storeRequests": store_requests,
            "binaryStoreRequests": binary_store_requests
        }
        
        # Make POST request
        url = f"{self._cells_url}/{object_id}"
        result = self._client.post(url, json=payload)
        
        # Process errors if result is a list
        resolved_raise = resolve_raise_on_row_errors(
            self._raise_on_row_errors_default, raise_on_row_errors
        )
        if isinstance(result, list):
            process_errors(result, raise_on_row_errors=resolved_raise)
            # Return first result (should only be one for single document)
            return result[0] if result else {}
        
        return result
    
    def create_entry_with_store_requests(
        self,
        object_id: Union[int, str],
        store_requests: Optional[List[Dict[str, Any]]] = None,
        binary_store_requests: Optional[List[Dict[str, Any]]] = None,
        raise_on_row_errors: Optional[bool] = None,
    ) -> dict:
        """
        Create an entry using the storeRequests/binaryStoreRequests structure.
        
        This method provides full control over the payload structure for advanced
        use cases like backlinking multiple documents or complex field operations.
        
        Args:
            object_id: Entry type ID or API name
            store_requests: List of store request objects. Each should have:
                - entryId: -1 for new entries, positive for updates
                - fieldId: Field ID (integer)
                - value: Field value
            binary_store_requests: List of binary store request objects. Each should have:
                - entryId: -1 for new entries, positive for updates
                - fieldId: Binary field ID (integer)
                - formatType: File format (e.g., "pdf", "docx")
                - documentStorageId: DMS document ID (for backlinks) OR
                - binaryData: Base64-encoded file content (for uploads)
            raise_on_row_errors: When True, raise on row ``Errors`` in HTTP 200 body.
                When None, uses ``DealCloudConfig.raiseOnRowErrors``. For ``COLLECT`` or
                ``output='write_result'``, use ``write_cells`` or Rows APIs instead.
        
        Returns:
            Created/updated entry result
        
        Example:
            >>> # Backlink multiple documents
            >>> result = dc.create_entry_with_store_requests(
            ...     object_id="Documents",
            ...     store_requests=[
            ...         {"entryId": -1, "fieldId": 374033, "value": "Document 1"},
            ...         {"entryId": -1, "fieldId": 374034, "value": "Category A"}
            ...     ],
            ...     binary_store_requests=[
            ...         {
            ...             "entryId": -1,
            ...             "fieldId": 374040,
            ...             "formatType": "pdf",
            ...             "documentStorageId": "sharepoint_id_123"
            ...         }
            ...     ]
            ... )
        """
        payload = {}
        
        if store_requests:
            payload["storeRequests"] = store_requests
        
        if binary_store_requests:
            payload["binaryStoreRequests"] = binary_store_requests
        
        if not payload:
            raise ValueError(
                "At least one of store_requests or binary_store_requests must be provided"
            )
        
        # Make POST request
        url = f"{self._cells_url}/{object_id}"
        result = self._client.post(url, json=payload)
        
        # Process errors if result is a list
        resolved_raise = resolve_raise_on_row_errors(
            self._raise_on_row_errors_default, raise_on_row_errors
        )
        if isinstance(result, list):
            process_errors(result, raise_on_row_errors=resolved_raise)
            # Return first result (should only be one for single entry)
            return result[0] if result else {}
        
        return result


