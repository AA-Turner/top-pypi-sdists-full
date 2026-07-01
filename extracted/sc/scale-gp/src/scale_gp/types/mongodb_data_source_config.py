# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["MongoDBDataSourceConfig"]


class MongoDBDataSourceConfig(BaseModel):
    database: str
    """Database name to connect to"""

    source: Literal["MongoDB"]

    connect_timeout: Optional[int] = None
    """Connection timeout in seconds"""
