"""
Type annotations for signin service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_signin.type_defs import AccessTokenTypeDef

    data: AccessTokenTypeDef = ...
    ```
"""

from __future__ import annotations

import sys

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AccessTokenTypeDef",
    "CreateOAuth2TokenRequestBodyTypeDef",
    "CreateOAuth2TokenRequestTypeDef",
    "CreateOAuth2TokenResponseBodyTypeDef",
    "CreateOAuth2TokenResponseTypeDef",
    "ResponseMetadataTypeDef",
)


class AccessTokenTypeDef(TypedDict):
    accessKeyId: str
    secretAccessKey: str
    sessionToken: str


class CreateOAuth2TokenRequestBodyTypeDef(TypedDict):
    clientId: str
    grantType: str
    code: NotRequired[str]
    redirectUri: NotRequired[str]
    codeVerifier: NotRequired[str]
    refreshToken: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateOAuth2TokenResponseBodyTypeDef(TypedDict):
    accessToken: AccessTokenTypeDef
    tokenType: str
    expiresIn: int
    refreshToken: str
    idToken: NotRequired[str]


class CreateOAuth2TokenRequestTypeDef(TypedDict):
    tokenInput: CreateOAuth2TokenRequestBodyTypeDef


class CreateOAuth2TokenResponseTypeDef(TypedDict):
    tokenOutput: CreateOAuth2TokenResponseBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
