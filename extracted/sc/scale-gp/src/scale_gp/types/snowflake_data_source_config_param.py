# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["SnowflakeDataSourceConfigParam"]


class SnowflakeDataSourceConfigParam(TypedDict, total=False):
    account: Required[str]
    """Snowflake account identifier"""

    source: Required[Literal["Snowflake"]]

    user: Required[str]
    """Snowflake user name"""
