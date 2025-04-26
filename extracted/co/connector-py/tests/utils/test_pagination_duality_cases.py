"""Test cases for test_pagination_utils.

Those cases cover scenarios for checking that ``decode_pagination`` is
inverse of ``encode_pagination``.
"""

import typing as t

from tests.utils.definitions import Pagination

Case: t.TypeAlias = list[Pagination]


def case_empty() -> Case:
    """No paginations is allowed."""
    return []


def case_single_url_page() -> Case:
    """Pagination for one call with pagination."""
    paginations = [
        Pagination(endpoint="/users", page=1),
    ]
    return paginations


def case_two_url_page() -> Case:
    """Pagination for more calls with pagination.

    This is rare case when we know the next page will call for last page
    of one endpoint and thus we can append call for the first page of
    the next endpoint.
    """
    paginations = [
        Pagination(endpoint="/users", page=100),
        Pagination(endpoint="/license", page=1),
    ]
    return paginations
