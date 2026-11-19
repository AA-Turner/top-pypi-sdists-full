"""
Type annotations for abuse-signal service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_abuse_signal/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_abuse_signal.client import AbuseSignalClient

    session = Session()
    client: AbuseSignalClient = session.client("abuse-signal")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListAbuseReportStatusesPaginator
from .type_defs import (
    CreateAbuseReportRequestTypeDef,
    CreateAbuseReportResponseTypeDef,
    GetAbuseReportStatusRequestTypeDef,
    GetAbuseReportStatusResponseTypeDef,
    ListAbuseReportStatusesRequestTypeDef,
    ListAbuseReportStatusesResponseTypeDef,
)
from .waiter import ReportProcessingWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("AbuseSignalClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    SubmissionRequirementException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class AbuseSignalClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/abuse-signal.html#AbuseSignal.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_abuse_signal/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AbuseSignalClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/abuse-signal.html#AbuseSignal.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_abuse_signal/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/abuse-signal/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_abuse_signal/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/abuse-signal/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_abuse_signal/client/#generate_presigned_url)
        """

    def create_abuse_report(
        self, **kwargs: Unpack[CreateAbuseReportRequestTypeDef]
    ) -> CreateAbuseReportResponseTypeDef:
        """
        Submits a structured report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/abuse-signal/client/create_abuse_report.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_abuse_signal/client/#create_abuse_report)
        """

    def get_abuse_report_status(
        self, **kwargs: Unpack[GetAbuseReportStatusRequestTypeDef]
    ) -> GetAbuseReportStatusResponseTypeDef:
        """
        Retrieves the current processing status of a previously submitted abuse report,
        including the status, submission timestamp, and last-update time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/abuse-signal/client/get_abuse_report_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_abuse_signal/client/#get_abuse_report_status)
        """

    def list_abuse_report_statuses(
        self, **kwargs: Unpack[ListAbuseReportStatusesRequestTypeDef]
    ) -> ListAbuseReportStatusesResponseTypeDef:
        """
        Lists abuse report statuses for the calling account, ordered by submission
        time, with optional filtering and pagination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/abuse-signal/client/list_abuse_report_statuses.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_abuse_signal/client/#list_abuse_report_statuses)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_abuse_report_statuses"]
    ) -> ListAbuseReportStatusesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/abuse-signal/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_abuse_signal/client/#get_paginator)
        """

    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["report_processing"]
    ) -> ReportProcessingWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/abuse-signal/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_abuse_signal/client/#get_waiter)
        """
