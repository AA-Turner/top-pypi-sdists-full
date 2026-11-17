"""
Type annotations for connectscheduling service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectscheduling/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_connectscheduling.type_defs import ActorInfoTypeDef

    data: ActorInfoTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Union

from .literals import (
    ApprovalTypeType,
    DurationUnitType,
    RuleFailureActionType,
    TimeOffStatusType,
    TimeOffValidationCodeType,
    TimeOffValidationSeverityType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ActorInfoTypeDef",
    "ApproveTimeOffRequestTypeDef",
    "CancelTimeOffRequestTypeDef",
    "CreateTimeOffRequestTypeDef",
    "CreateTimeOffResponseTypeDef",
    "DurationTypeDef",
    "GetTimeOffRequestTypeDef",
    "GetTimeOffResponseTypeDef",
    "PutTimeOffBalanceRequestTypeDef",
    "RejectTimeOffRequestTypeDef",
    "ResponseMetadataTypeDef",
    "TimeOffValidationResultTypeDef",
    "TimestampTypeDef",
)

class ActorInfoTypeDef(TypedDict):
    ConnectUserArn: NotRequired[str]
    AWSIdentityArn: NotRequired[str]

class ApproveTimeOffRequestTypeDef(TypedDict):
    InstanceId: str
    UserId: str
    TimeOffId: str
    Description: NotRequired[str]
    RuleFailureAction: NotRequired[RuleFailureActionType]

class CancelTimeOffRequestTypeDef(TypedDict):
    InstanceId: str
    UserId: str
    TimeOffId: str
    Description: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DurationTypeDef(TypedDict):
    Value: int
    Unit: DurationUnitType

class GetTimeOffRequestTypeDef(TypedDict):
    InstanceId: str
    UserId: str
    TimeOffId: str

class TimeOffValidationResultTypeDef(TypedDict):
    Severity: TimeOffValidationSeverityType
    Code: TimeOffValidationCodeType

class RejectTimeOffRequestTypeDef(TypedDict):
    InstanceId: str
    UserId: str
    TimeOffId: str
    Description: NotRequired[str]

class CreateTimeOffRequestTypeDef(TypedDict):
    InstanceId: str
    UserId: str
    ShiftActivityId: str
    StartAt: TimestampTypeDef
    EndAt: TimestampTypeDef
    ApprovalType: ApprovalTypeType
    Description: NotRequired[str]
    RuleFailureAction: NotRequired[RuleFailureActionType]
    ClientToken: NotRequired[str]

class CreateTimeOffResponseTypeDef(TypedDict):
    TimeOffId: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutTimeOffBalanceRequestTypeDef(TypedDict):
    InstanceId: str
    UserId: str
    ShiftActivityId: str
    Balance: DurationTypeDef

class GetTimeOffResponseTypeDef(TypedDict):
    TimeOffId: str
    UserId: str
    ShiftActivityId: str
    StartAt: datetime
    EndAt: datetime
    Status: TimeOffStatusType
    Description: str
    ValidationResults: list[TimeOffValidationResultTypeDef]
    CreatedBy: ActorInfoTypeDef
    CreatedAt: datetime
    UpdatedBy: ActorInfoTypeDef
    UpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef
