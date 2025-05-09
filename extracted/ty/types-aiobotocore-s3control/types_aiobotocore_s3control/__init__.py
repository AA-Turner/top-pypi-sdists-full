"""
Main interface for s3control service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_s3control import (
        Client,
        ListAccessPointsForObjectLambdaPaginator,
        ListCallerAccessGrantsPaginator,
        S3ControlClient,
    )

    session = get_session()
    async with session.create_client("s3control") as client:
        client: S3ControlClient
        ...


    list_access_points_for_object_lambda_paginator: ListAccessPointsForObjectLambdaPaginator = client.get_paginator("list_access_points_for_object_lambda")
    list_caller_access_grants_paginator: ListCallerAccessGrantsPaginator = client.get_paginator("list_caller_access_grants")
    ```
"""

from .client import S3ControlClient
from .paginator import ListAccessPointsForObjectLambdaPaginator, ListCallerAccessGrantsPaginator

Client = S3ControlClient


__all__ = (
    "Client",
    "ListAccessPointsForObjectLambdaPaginator",
    "ListCallerAccessGrantsPaginator",
    "S3ControlClient",
)
