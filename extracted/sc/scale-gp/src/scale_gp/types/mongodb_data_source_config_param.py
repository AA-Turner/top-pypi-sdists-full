# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["MongoDBDataSourceConfigParam"]


class MongoDBDataSourceConfigParam(TypedDict, total=False):
    database: Required[str]
    """Database name to connect to"""

    source: Required[Literal["MongoDB"]]

    connect_timeout: int
    """Connection timeout in seconds"""
