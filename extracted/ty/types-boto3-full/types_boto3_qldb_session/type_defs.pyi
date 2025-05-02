"""
Type annotations for qldb-session service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qldb_session/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_boto3_qldb_session.type_defs import TimingInformationTypeDef

    data: TimingInformationTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from typing import IO, Any, Union

from botocore.response import StreamingBody

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Mapping, Sequence
else:
    from typing import Dict, List, Mapping, Sequence
if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AbortTransactionResultTypeDef",
    "BlobTypeDef",
    "CommitTransactionRequestTypeDef",
    "CommitTransactionResultTypeDef",
    "EndSessionResultTypeDef",
    "ExecuteStatementRequestTypeDef",
    "ExecuteStatementResultTypeDef",
    "FetchPageRequestTypeDef",
    "FetchPageResultTypeDef",
    "IOUsageTypeDef",
    "PageTypeDef",
    "ResponseMetadataTypeDef",
    "SendCommandRequestTypeDef",
    "SendCommandResultTypeDef",
    "StartSessionRequestTypeDef",
    "StartSessionResultTypeDef",
    "StartTransactionResultTypeDef",
    "TimingInformationTypeDef",
    "ValueHolderOutputTypeDef",
    "ValueHolderTypeDef",
    "ValueHolderUnionTypeDef",
)

class TimingInformationTypeDef(TypedDict):
    ProcessingTimeMilliseconds: NotRequired[int]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class IOUsageTypeDef(TypedDict):
    ReadIOs: NotRequired[int]
    WriteIOs: NotRequired[int]

class FetchPageRequestTypeDef(TypedDict):
    TransactionId: str
    NextPageToken: str

class ValueHolderOutputTypeDef(TypedDict):
    IonBinary: NotRequired[bytes]
    IonText: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class StartSessionRequestTypeDef(TypedDict):
    LedgerName: str

class AbortTransactionResultTypeDef(TypedDict):
    TimingInformation: NotRequired[TimingInformationTypeDef]

class EndSessionResultTypeDef(TypedDict):
    TimingInformation: NotRequired[TimingInformationTypeDef]

class StartSessionResultTypeDef(TypedDict):
    SessionToken: NotRequired[str]
    TimingInformation: NotRequired[TimingInformationTypeDef]

class StartTransactionResultTypeDef(TypedDict):
    TransactionId: NotRequired[str]
    TimingInformation: NotRequired[TimingInformationTypeDef]

class CommitTransactionRequestTypeDef(TypedDict):
    TransactionId: str
    CommitDigest: BlobTypeDef

class ValueHolderTypeDef(TypedDict):
    IonBinary: NotRequired[BlobTypeDef]
    IonText: NotRequired[str]

class CommitTransactionResultTypeDef(TypedDict):
    TransactionId: NotRequired[str]
    CommitDigest: NotRequired[bytes]
    TimingInformation: NotRequired[TimingInformationTypeDef]
    ConsumedIOs: NotRequired[IOUsageTypeDef]

class PageTypeDef(TypedDict):
    Values: NotRequired[List[ValueHolderOutputTypeDef]]
    NextPageToken: NotRequired[str]

ValueHolderUnionTypeDef = Union[ValueHolderTypeDef, ValueHolderOutputTypeDef]

class ExecuteStatementResultTypeDef(TypedDict):
    FirstPage: NotRequired[PageTypeDef]
    TimingInformation: NotRequired[TimingInformationTypeDef]
    ConsumedIOs: NotRequired[IOUsageTypeDef]

class FetchPageResultTypeDef(TypedDict):
    Page: NotRequired[PageTypeDef]
    TimingInformation: NotRequired[TimingInformationTypeDef]
    ConsumedIOs: NotRequired[IOUsageTypeDef]

class ExecuteStatementRequestTypeDef(TypedDict):
    TransactionId: str
    Statement: str
    Parameters: NotRequired[Sequence[ValueHolderUnionTypeDef]]

class SendCommandResultTypeDef(TypedDict):
    StartSession: StartSessionResultTypeDef
    StartTransaction: StartTransactionResultTypeDef
    EndSession: EndSessionResultTypeDef
    CommitTransaction: CommitTransactionResultTypeDef
    AbortTransaction: AbortTransactionResultTypeDef
    ExecuteStatement: ExecuteStatementResultTypeDef
    FetchPage: FetchPageResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SendCommandRequestTypeDef(TypedDict):
    SessionToken: NotRequired[str]
    StartSession: NotRequired[StartSessionRequestTypeDef]
    StartTransaction: NotRequired[Mapping[str, Any]]
    EndSession: NotRequired[Mapping[str, Any]]
    CommitTransaction: NotRequired[CommitTransactionRequestTypeDef]
    AbortTransaction: NotRequired[Mapping[str, Any]]
    ExecuteStatement: NotRequired[ExecuteStatementRequestTypeDef]
    FetchPage: NotRequired[FetchPageRequestTypeDef]
