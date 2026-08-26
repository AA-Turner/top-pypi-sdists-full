"""
Type annotations for iam-toolbox service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam_toolbox/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_iam_toolbox.type_defs import AttachedToTypeDef

    data: AttachedToTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from typing import Any

from .literals import EvaluatedEffectType, PolicyTypeType, StatementEffectType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AttachedToTypeDef",
    "EvaluationTypeDef",
    "GetRequestAuthorizationDetailsInputPaginateTypeDef",
    "GetRequestAuthorizationDetailsInputTypeDef",
    "GetRequestAuthorizationDetailsOutputTypeDef",
    "MatchedPolicyTypeDef",
    "MatchedStatementTypeDef",
    "PaginatorConfigTypeDef",
    "PolicyInfoTypeDef",
    "ResponseMetadataTypeDef",
)


class AttachedToTypeDef(TypedDict):
    arn: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetRequestAuthorizationDetailsInputTypeDef(TypedDict):
    authorizationId: str
    nextToken: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class MatchedStatementTypeDef(TypedDict):
    sid: NotRequired[str]
    evaluatedEffect: NotRequired[StatementEffectType]


PolicyInfoTypeDef = TypedDict(
    "PolicyInfoTypeDef",
    {
        "type": NotRequired[PolicyTypeType],
        "inline": NotRequired[bool],
        "uri": NotRequired[str],
        "attachedTo": NotRequired[list[AttachedToTypeDef]],
    },
)


class GetRequestAuthorizationDetailsInputPaginateTypeDef(TypedDict):
    authorizationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class MatchedPolicyTypeDef(TypedDict):
    uri: str
    matchedStatements: NotRequired[list[MatchedStatementTypeDef]]


class EvaluationTypeDef(TypedDict):
    action: str
    resource: str
    context: NotRequired[dict[str, dict[str, Any]]]
    evaluatedEffect: NotRequired[EvaluatedEffectType]
    matchedPolicies: NotRequired[list[MatchedPolicyTypeDef]]


class GetRequestAuthorizationDetailsOutputTypeDef(TypedDict):
    requestContext: dict[str, dict[str, Any]]
    evaluations: list[EvaluationTypeDef]
    policies: list[PolicyInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
