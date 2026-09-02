import logging
from math import floor
from typing import Generator, Optional, Union

import numpy as np
import pandas as pd

from dealcloud_sdk.constants.data import CELL_PAGINATION_LIMIT


def flatten_nested_list(nested_list: list):
    return list([r for sublist in nested_list for r in sublist])


def format_data(data: Union[list[dict], pd.DataFrame]) -> tuple[list[dict], set]:
    # format pandas to dict
    if isinstance(data, pd.DataFrame):
        data = data.replace(np.nan, None)
        data = data.to_dict(orient="records")

    columns = set(flatten_nested_list(list([row.keys() for row in data])))

    return data, columns


def divide_pages(paginate_list: list, page_size: int) -> Generator[list, None, None]:
    for i in range(0, len(paginate_list), page_size):
        yield paginate_list[i : i + page_size]


def calculate_pagination(
    rows: list[dict], columns: set, cell_pagination_limit: int = CELL_PAGINATION_LIMIT
) -> list:
    # get number of rows
    row_count = len(rows)
    # get number of columns
    column_count = len(columns)

    # determine the total number of cells and paginate appropriately
    total_cells = row_count * column_count

    if total_cells > cell_pagination_limit:
        logging.info("data upload pagination required")

        # determine the number of entries that can fit in one page
        entries_per_page = floor(cell_pagination_limit / column_count)

        data = list(divide_pages(rows, entries_per_page))
    else:
        data = [rows]

    return data


def rows_query_payload_builder(
    query: str,
    fields: Optional[list[str]] = None,
    limit: Optional[int] = None,
    skip: Optional[int] = None,
) -> dict:
    """
    Used to construct the request body for a query rows POST request,
    limit and skip can optionally be passed for pagination
    Args:
        query (str): the API query string
        fields (list[str]): the list of fields to return
        limit (int): the maximum number of rows to return
        skip (int): the offset of rows to return

    Returns:
        The API request payload
    """
    payload = {"query": query, "wrapIntoArrays": True}
    if fields:
        payload["fields"] = fields
    if limit:
        payload["limit"] = limit
    if skip:
        payload["skip"] = skip

    return payload
