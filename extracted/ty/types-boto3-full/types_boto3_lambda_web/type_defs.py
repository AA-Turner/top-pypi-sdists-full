"""
Type annotations for lambda-web service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lambda_web/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_lambda_web.type_defs import AccountQuotasTypeDef

    data: AccountQuotasTypeDef = ...
    ```
"""

from __future__ import annotations

import sys

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AccountQuotasTypeDef",
    "AccountUsageTypeDef",
    "GetWebAccountSettingsResponseTypeDef",
    "ResponseMetadataTypeDef",
)


class AccountQuotasTypeDef(TypedDict):
    maxTotalArmVCpus: int
    maxTotalRateLimit: int
    maxRevisionsPerFunction: int
    maxEndpointsPerFunction: int


class AccountUsageTypeDef(TypedDict):
    functionCount: int


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class GetWebAccountSettingsResponseTypeDef(TypedDict):
    accountQuotas: AccountQuotasTypeDef
    accountUsage: AccountUsageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
