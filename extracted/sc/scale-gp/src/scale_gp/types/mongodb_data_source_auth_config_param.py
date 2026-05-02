# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["MongoDBDataSourceAuthConfigParam"]


class MongoDBDataSourceAuthConfigParam(TypedDict, total=False):
    connection_uri: Required[str]
    """MongoDB connection URI"""

    source: Required[Literal["MongoDB"]]

    encrypted: bool
