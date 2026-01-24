"""
Main interface for osis service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_osis import (
        Client,
        ListPipelineEndpointConnectionsPaginator,
        ListPipelineEndpointsPaginator,
        OpenSearchIngestionClient,
    )

    session = get_session()
    async with session.create_client("osis") as client:
        client: OpenSearchIngestionClient
        ...


    list_pipeline_endpoint_connections_paginator: ListPipelineEndpointConnectionsPaginator = client.get_paginator("list_pipeline_endpoint_connections")
    list_pipeline_endpoints_paginator: ListPipelineEndpointsPaginator = client.get_paginator("list_pipeline_endpoints")
    ```
"""

from .client import OpenSearchIngestionClient
from .paginator import ListPipelineEndpointConnectionsPaginator, ListPipelineEndpointsPaginator

Client = OpenSearchIngestionClient

__all__ = (
    "Client",
    "ListPipelineEndpointConnectionsPaginator",
    "ListPipelineEndpointsPaginator",
    "OpenSearchIngestionClient",
)
