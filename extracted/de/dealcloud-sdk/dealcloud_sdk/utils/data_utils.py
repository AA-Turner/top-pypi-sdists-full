"""Data utilities with improved pagination per DealCloud API best practices.

Pagination Strategy:
- Do NOT rely on totalRecords for pagination
- Continue querying until empty rows array is returned
- Per API docs: "If you request beyond the available pages, the API will return 
  a 200 OK response with an empty rows array."
- Use parallel requests for efficiency
"""

import logging
from math import floor
from typing import TYPE_CHECKING, Generator, Optional, Union
import numpy as np
import pandas as pd

if TYPE_CHECKING:
    import polars as pl

from ..constants.data import CELL_PAGINATION_LIMIT, DEFAULT_PAGE_SIZE, MAX_SPECULATIVE_PAGES


def flatten_nested_list(nested_list: list) -> list:
    """Flatten a nested list."""
    return [r for sublist in nested_list for r in sublist]


def format_data(data: Union[list[dict], pd.DataFrame, "pl.DataFrame"]) -> tuple[list[dict], set]:
    """
    Format input data to list of dicts and extract columns.
    
    Accepts:
        - list[dict]: Returned as-is
        - pandas.DataFrame: Converted via to_dict(orient="records")
        - polars.DataFrame: Converted via to_dicts()
    
    Args:
        data: Input data in any supported format
    
    Returns:
        Tuple of (list of dicts, set of column names)
    """
    # Check for polars DataFrame (has to_dicts method and _df attribute)
    if hasattr(data, 'to_dicts') and hasattr(data, '_df'):
        # Polars DataFrame
        data = data.to_dicts()
    elif isinstance(data, pd.DataFrame):
        # Pandas DataFrame — scalar replace(np.nan, None) misses NA in str/StringDtype cols (pandas 3+)
        data = data.replace([np.nan, pd.NA], None)
        data = data.to_dict(orient="records")
    # else: assume list[dict]
    
    columns = set(flatten_nested_list([list(row.keys()) for row in data]))
    return data, columns


def divide_pages(paginate_list: list, page_size: int) -> Generator[list, None, None]:
    """Divide list into pages."""
    for i in range(0, len(paginate_list), page_size):
        yield paginate_list[i:i + page_size]


def calculate_pagination(
    rows: list[dict], 
    columns: set, 
    cell_pagination_limit: int = CELL_PAGINATION_LIMIT
) -> list:
    """Calculate pagination for data uploads."""
    row_count = len(rows)
    column_count = len(columns)
    total_cells = row_count * column_count
    
    if total_cells > cell_pagination_limit:
        logging.info("data upload pagination required")
        entries_per_page = floor(cell_pagination_limit / column_count)
        return list(divide_pages(rows, entries_per_page))
    else:
        return [rows]


def query_by_entry_id(entry_id: int) -> str:
    """Build a DealCloud query string that filters to a single entry by ID."""
    return f"{{entryid: {entry_id}}}"


def rows_query_payload_builder(
    query: str,
    fields: Optional[list[str]] = None,
    limit: Optional[int] = None,
    skip: Optional[int] = None,
) -> dict:
    """Build request body for query rows POST request."""
    payload = {"query": query, "wrapIntoArrays": True}
    if fields:
        payload["fields"] = fields
    if limit:
        payload["limit"] = limit
    if skip:
        payload["skip"] = skip
    return payload


def generate_page_offsets(page_size: int = DEFAULT_PAGE_SIZE, max_parallel_pages: int = MAX_SPECULATIVE_PAGES) -> list[int]:
    """
    Generate initial page offsets for parallel fetching.
    
    We speculatively fetch multiple pages in parallel, then continue
    until we get an empty response.
    """
    return [i * page_size for i in range(max_parallel_pages)]


