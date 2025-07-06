"""
Main interface for s3outposts service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_s3outposts import (
        Client,
        ListEndpointsPaginator,
        ListOutpostsWithS3Paginator,
        ListSharedEndpointsPaginator,
        S3OutpostsClient,
    )

    session = get_session()
    async with session.create_client("s3outposts") as client:
        client: S3OutpostsClient
        ...


    list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
    list_outposts_with_s3_paginator: ListOutpostsWithS3Paginator = client.get_paginator("list_outposts_with_s3")
    list_shared_endpoints_paginator: ListSharedEndpointsPaginator = client.get_paginator("list_shared_endpoints")
    ```
"""

from .client import S3OutpostsClient
from .paginator import (
    ListEndpointsPaginator,
    ListOutpostsWithS3Paginator,
    ListSharedEndpointsPaginator,
)

Client = S3OutpostsClient


__all__ = (
    "Client",
    "ListEndpointsPaginator",
    "ListOutpostsWithS3Paginator",
    "ListSharedEndpointsPaginator",
    "S3OutpostsClient",
)
