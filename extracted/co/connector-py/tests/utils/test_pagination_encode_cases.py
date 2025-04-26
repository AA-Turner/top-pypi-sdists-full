"""Test cases for test_pagination_utils.

Those cases cover scenarios for ``encode_pagination`` function.
"""

import typing as t

from tests.utils.test_pagination import Pagination

Case: t.TypeAlias = list[Pagination]


def case_single_url_page() -> Case:
    """Pagination for one call with pagination."""
    paginations = [
        Pagination(endpoint="/users", page=1),
    ]
    return paginations


def case_two_url_page() -> Case:
    """Pagination for one call with pagination."""
    paginations = [
        Pagination(endpoint="/users", page=1),
        Pagination(endpoint="/roles", page=20),
    ]
    return paginations
