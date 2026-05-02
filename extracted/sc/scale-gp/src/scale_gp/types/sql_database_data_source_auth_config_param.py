# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["SqlDatabaseDataSourceAuthConfigParam"]


class SqlDatabaseDataSourceAuthConfigParam(TypedDict, total=False):
    password: Required[str]
    """Password for database authentication"""

    source: Required[Literal["SQLDatabase"]]

    encrypted: bool
