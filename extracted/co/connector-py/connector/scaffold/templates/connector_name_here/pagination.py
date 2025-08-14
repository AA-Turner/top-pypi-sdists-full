"""Pagination for {title} API."""

import typing as t

from connector.client import NextPageTokenInterface, PaginationBase, create_next_page_token, get_page
from connector.integration import Request

DEFAULT_PAGE_SIZE = 100


class Pagination(PaginationBase):
    """Pagination parameters for API methods."""

    offset: int

    @classmethod
    def default(cls, endpoint: str) -> "Pagination":
        return cls(
            endpoint=endpoint,
            offset=0,
        )


if t.TYPE_CHECKING:

    class NextPageToken(NextPageTokenInterface[Pagination]):  # pragma: no cover
        @classmethod
        def from_paginations(cls, paginations: list[Pagination]) -> "NextPageToken":
            return cls(token=None)

        def paginations(self) -> list[Pagination]:
            return []
else:
    NextPageToken = create_next_page_token(Pagination, "NextPageToken")


def paginations_from_args(
    args: Request, default_endpoints: list[str]
) -> tuple[list[Pagination], Pagination, int]:
    paginations = NextPageToken(get_page(args).token).paginations()
    if not paginations:
        paginations = [Pagination.default(endpoint) for endpoint in default_endpoints]

    current_pagination = paginations.pop()
    return paginations, current_pagination, get_page(args).size or DEFAULT_PAGE_SIZE
