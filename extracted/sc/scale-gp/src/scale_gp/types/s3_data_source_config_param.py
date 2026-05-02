# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["S3DataSourceConfigParam"]


class S3DataSourceConfigParam(TypedDict, total=False):
    aws_account_id: Required[str]
    """AWS account ID that owns the S3 bucket."""

    aws_region: Required[str]
    """AWS region where the S3 bucket is located."""

    s3_bucket: Required[str]
    """Name of the S3 bucket where the data is stored."""

    source: Required[Literal["S3"]]

    s3_prefix: str
    """Prefix of the S3 bucket where the data is stored.

    If not specified, the entire bucket will be used.
    """
