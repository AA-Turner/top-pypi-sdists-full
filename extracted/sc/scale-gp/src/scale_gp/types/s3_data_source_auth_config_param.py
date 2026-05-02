# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["S3DataSourceAuthConfigParam"]


class S3DataSourceAuthConfigParam(TypedDict, total=False):
    source: Required[Literal["S3"]]

    encrypted: bool

    external_id: str
    """External ID defined by the customer for the IAM role"""

    s3_role: str
    """Name of the role that a client will be initialized via AssumeRole of AWS sts"""
