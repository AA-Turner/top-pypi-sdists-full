"""
Type annotations for connectscheduling service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectscheduling/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_connectscheduling.client import ConnectSchedulingClient

    session = Session()
    client: ConnectSchedulingClient = session.client("connectscheduling")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    ApproveTimeOffRequestTypeDef,
    CancelTimeOffRequestTypeDef,
    CreateTimeOffRequestTypeDef,
    CreateTimeOffResponseTypeDef,
    GetTimeOffRequestTypeDef,
    GetTimeOffResponseTypeDef,
    PutTimeOffBalanceRequestTypeDef,
    RejectTimeOffRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ConnectSchedulingClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class ConnectSchedulingClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectscheduling.html#ConnectScheduling.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectscheduling/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConnectSchedulingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectscheduling.html#ConnectScheduling.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectscheduling/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectscheduling/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectscheduling/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectscheduling/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectscheduling/client/#generate_presigned_url)
        """

    def approve_time_off(self, **kwargs: Unpack[ApproveTimeOffRequestTypeDef]) -> dict[str, Any]:
        """
        Approves a time off request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectscheduling/client/approve_time_off.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectscheduling/client/#approve_time_off)
        """

    def cancel_time_off(self, **kwargs: Unpack[CancelTimeOffRequestTypeDef]) -> dict[str, Any]:
        """
        Cancels a time off request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectscheduling/client/cancel_time_off.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectscheduling/client/#cancel_time_off)
        """

    def create_time_off(
        self, **kwargs: Unpack[CreateTimeOffRequestTypeDef]
    ) -> CreateTimeOffResponseTypeDef:
        """
        Creates a time off request for a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectscheduling/client/create_time_off.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectscheduling/client/#create_time_off)
        """

    def get_time_off(self, **kwargs: Unpack[GetTimeOffRequestTypeDef]) -> GetTimeOffResponseTypeDef:
        """
        Returns a time off request, including its current status and validation results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectscheduling/client/get_time_off.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectscheduling/client/#get_time_off)
        """

    def put_time_off_balance(
        self, **kwargs: Unpack[PutTimeOffBalanceRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Sets the time off balance for one user and shift activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectscheduling/client/put_time_off_balance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectscheduling/client/#put_time_off_balance)
        """

    def reject_time_off(self, **kwargs: Unpack[RejectTimeOffRequestTypeDef]) -> dict[str, Any]:
        """
        Rejects a time off request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectscheduling/client/reject_time_off.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectscheduling/client/#reject_time_off)
        """
