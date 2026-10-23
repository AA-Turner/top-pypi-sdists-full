"""
Main interface for opensearchserverless service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_opensearchserverless import (
        Client,
        ListIngestionJobsPaginator,
        ListIngestionStreamsPaginator,
        OpenSearchServiceServerlessClient,
    )

    session = Session()
    client: OpenSearchServiceServerlessClient = session.client("opensearchserverless")

    list_ingestion_jobs_paginator: ListIngestionJobsPaginator = client.get_paginator("list_ingestion_jobs")
    list_ingestion_streams_paginator: ListIngestionStreamsPaginator = client.get_paginator("list_ingestion_streams")
    ```
"""

from .client import OpenSearchServiceServerlessClient
from .paginator import ListIngestionJobsPaginator, ListIngestionStreamsPaginator

Client = OpenSearchServiceServerlessClient


__all__ = (
    "Client",
    "ListIngestionJobsPaginator",
    "ListIngestionStreamsPaginator",
    "OpenSearchServiceServerlessClient",
)
