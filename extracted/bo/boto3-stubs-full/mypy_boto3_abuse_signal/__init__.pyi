"""
Main interface for abuse-signal service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_abuse_signal/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_abuse_signal import (
        AbuseSignalClient,
        Client,
        ListAbuseReportStatusesPaginator,
        ReportProcessingWaiter,
    )

    session = Session()
    client: AbuseSignalClient = session.client("abuse-signal")

    report_processing_waiter: ReportProcessingWaiter = client.get_waiter("report_processing")

    list_abuse_report_statuses_paginator: ListAbuseReportStatusesPaginator = client.get_paginator("list_abuse_report_statuses")
    ```
"""

from .client import AbuseSignalClient
from .paginator import ListAbuseReportStatusesPaginator
from .waiter import ReportProcessingWaiter

Client = AbuseSignalClient

__all__ = (
    "AbuseSignalClient",
    "Client",
    "ListAbuseReportStatusesPaginator",
    "ReportProcessingWaiter",
)
