"""
Main interface for emr-serverless service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_emr_serverless import (
        Client,
        EMRServerlessClient,
        ListApplicationsPaginator,
        ListJobRunAttemptsPaginator,
        ListJobRunsPaginator,
    )

    session = get_session()
    async with session.create_client("emr-serverless") as client:
        client: EMRServerlessClient
        ...


    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_job_run_attempts_paginator: ListJobRunAttemptsPaginator = client.get_paginator("list_job_run_attempts")
    list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
    ```
"""

from .client import EMRServerlessClient
from .paginator import ListApplicationsPaginator, ListJobRunAttemptsPaginator, ListJobRunsPaginator

Client = EMRServerlessClient


__all__ = (
    "Client",
    "EMRServerlessClient",
    "ListApplicationsPaginator",
    "ListJobRunAttemptsPaginator",
    "ListJobRunsPaginator",
)
