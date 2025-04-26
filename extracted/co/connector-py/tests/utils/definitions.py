import typing as t

from connector.utils.pagination import (
    NextPageTokenInterface,
    PaginationBase,
    create_next_page_token,
)


class Pagination(PaginationBase):
    page: int


if t.TYPE_CHECKING:

    class NextPageToken(NextPageTokenInterface[Pagination]):
        def paginations(self) -> list[Pagination]:
            pass

        @classmethod
        def from_paginations(cls, paginations: list[Pagination]) -> "NextPageToken":
            pass
else:
    NextPageToken = create_next_page_token(Pagination, "NextPageToken")
