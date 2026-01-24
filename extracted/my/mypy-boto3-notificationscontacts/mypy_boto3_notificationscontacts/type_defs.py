"""
Type annotations for notificationscontacts service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_notificationscontacts.type_defs import ActivateEmailContactRequestTypeDef

    data: ActivateEmailContactRequestTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime

from .literals import EmailContactStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ActivateEmailContactRequestTypeDef",
    "CreateEmailContactRequestTypeDef",
    "CreateEmailContactResponseTypeDef",
    "DeleteEmailContactRequestTypeDef",
    "EmailContactTypeDef",
    "GetEmailContactRequestTypeDef",
    "GetEmailContactResponseTypeDef",
    "ListEmailContactsRequestPaginateTypeDef",
    "ListEmailContactsRequestTypeDef",
    "ListEmailContactsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SendActivationCodeRequestTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
)


class ActivateEmailContactRequestTypeDef(TypedDict):
    arn: str
    code: str


class CreateEmailContactRequestTypeDef(TypedDict):
    name: str
    emailAddress: str
    tags: NotRequired[Mapping[str, str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteEmailContactRequestTypeDef(TypedDict):
    arn: str


class EmailContactTypeDef(TypedDict):
    arn: str
    name: str
    address: str
    status: EmailContactStatusType
    creationTime: datetime
    updateTime: datetime


class GetEmailContactRequestTypeDef(TypedDict):
    arn: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListEmailContactsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    arn: str


class SendActivationCodeRequestTypeDef(TypedDict):
    arn: str


class TagResourceRequestTypeDef(TypedDict):
    arn: str
    tags: Mapping[str, str]


class UntagResourceRequestTypeDef(TypedDict):
    arn: str
    tagKeys: Sequence[str]


class CreateEmailContactResponseTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetEmailContactResponseTypeDef(TypedDict):
    emailContact: EmailContactTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListEmailContactsResponseTypeDef(TypedDict):
    emailContacts: list[EmailContactTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListEmailContactsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]
