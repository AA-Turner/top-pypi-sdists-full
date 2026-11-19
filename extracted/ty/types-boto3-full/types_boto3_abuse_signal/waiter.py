"""
Type annotations for abuse-signal service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_abuse_signal/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_abuse_signal.client import AbuseSignalClient
    from types_boto3_abuse_signal.waiter import (
        ReportProcessingWaiter,
    )

    session = Session()
    client: AbuseSignalClient = session.client("abuse-signal")

    report_processing_waiter: ReportProcessingWaiter = client.get_waiter("report_processing")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetAbuseReportStatusRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ReportProcessingWaiter",)


class ReportProcessingWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/abuse-signal/waiter/ReportProcessing.html#AbuseSignal.Waiter.ReportProcessing)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_abuse_signal/waiters/#reportprocessingwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetAbuseReportStatusRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/abuse-signal/waiter/ReportProcessing.html#AbuseSignal.Waiter.ReportProcessing.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_abuse_signal/waiters/#reportprocessingwaiter)
        """
