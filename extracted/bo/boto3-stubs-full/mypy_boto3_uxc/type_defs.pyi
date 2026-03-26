"""
Type annotations for uxc service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_uxc/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_uxc.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence

from .literals import AccountColorType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "GetAccountCustomizationsOutputTypeDef",
    "ListServicesInputPaginateTypeDef",
    "ListServicesInputTypeDef",
    "ListServicesOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "UpdateAccountCustomizationsInputTypeDef",
    "UpdateAccountCustomizationsOutputTypeDef",
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListServicesInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class UpdateAccountCustomizationsInputTypeDef(TypedDict):
    accountColor: NotRequired[AccountColorType]
    visibleServices: NotRequired[Sequence[str]]
    visibleRegions: NotRequired[Sequence[str]]

class GetAccountCustomizationsOutputTypeDef(TypedDict):
    accountColor: AccountColorType
    visibleServices: list[str]
    visibleRegions: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListServicesOutputTypeDef(TypedDict):
    services: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateAccountCustomizationsOutputTypeDef(TypedDict):
    accountColor: AccountColorType
    visibleServices: list[str]
    visibleRegions: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListServicesInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]
