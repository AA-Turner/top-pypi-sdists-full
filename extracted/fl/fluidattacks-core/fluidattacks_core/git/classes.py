from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
)


class CommitInfo(NamedTuple):
    hash: str
    author: str
    modified_date: datetime


class RebaseResult(NamedTuple):
    path: str
    line: int
    rev: str


class InvalidParameter(Exception):
    """Exception to control empty required parameters."""

    def __init__(self, field: str = "") -> None:
        if field:
            msg = f"Exception - Field {field} is invalid"
        else:
            msg = "Exception - Error value is not valid"
        super().__init__(msg)
