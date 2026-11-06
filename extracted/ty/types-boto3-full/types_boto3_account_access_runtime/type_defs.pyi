"""
Type annotations for account-access-runtime service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_account_access_runtime/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_account_access_runtime.type_defs import AccessDetailsTypeDef

    data: AccessDetailsTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccessDetailsTypeDef",
    "CredentialsDetailsTypeDef",
    "GetRoleCredentialsRequestTypeDef",
    "GetRoleCredentialsResponseTypeDef",
    "ListRolesRequestPaginateTypeDef",
    "ListRolesRequestTypeDef",
    "ListRolesResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ProgrammaticAccessDetailsTypeDef",
    "ResponseMetadataTypeDef",
)

class AccessDetailsTypeDef(TypedDict):
    accountId: str
    roleArn: str
    accountName: NotRequired[str]

class ProgrammaticAccessDetailsTypeDef(TypedDict):
    accessKeyId: str
    secretAccessKey: str
    sessionToken: str
    expiresAt: datetime

class GetRoleCredentialsRequestTypeDef(TypedDict):
    tenantId: str
    roleArn: str
    accessType: Literal["PROGRAMMATIC_ACCESS"]
    sessionName: NotRequired[str]
    sessionDuration: NotRequired[int]

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

class ListRolesRequestTypeDef(TypedDict):
    tenantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class CredentialsDetailsTypeDef(TypedDict):
    programmaticAccess: NotRequired[ProgrammaticAccessDetailsTypeDef]

class ListRolesResponseTypeDef(TypedDict):
    roles: list[AccessDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListRolesRequestPaginateTypeDef(TypedDict):
    tenantId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetRoleCredentialsResponseTypeDef(TypedDict):
    credentialsDetails: CredentialsDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
