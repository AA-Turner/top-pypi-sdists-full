# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["S3DataSourceConfig"]


class S3DataSourceConfig(BaseModel):
    aws_account_id: str
    """AWS account ID that owns the S3 bucket."""

    aws_region: str
    """AWS region where the S3 bucket is located."""

    s3_bucket: str
    """Name of the S3 bucket where the data is stored."""

    source: Literal["S3"]

    s3_prefix: Optional[str] = None
    """Prefix of the S3 bucket where the data is stored.

    If not specified, the entire bucket will be used.
    """
