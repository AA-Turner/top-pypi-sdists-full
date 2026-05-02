# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["SnowflakeDataSourceConfig"]


class SnowflakeDataSourceConfig(BaseModel):
    account: str
    """Snowflake account identifier"""

    source: Literal["Snowflake"]

    user: str
    """Snowflake user name"""
