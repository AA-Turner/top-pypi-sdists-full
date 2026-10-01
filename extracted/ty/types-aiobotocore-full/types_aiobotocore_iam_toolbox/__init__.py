"""
Main interface for iam-toolbox service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam_toolbox/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iam_toolbox import (
        Client,
        GetRequestAuthorizationDetailsPaginator,
        IAMToolboxPreviewClient,
    )

    session = get_session()
    async with session.create_client("iam-toolbox") as client:
        client: IAMToolboxPreviewClient
        ...


    get_request_authorization_details_paginator: GetRequestAuthorizationDetailsPaginator = client.get_paginator("get_request_authorization_details")
    ```
"""

from .client import IAMToolboxPreviewClient
from .paginator import GetRequestAuthorizationDetailsPaginator

Client = IAMToolboxPreviewClient


__all__ = ("Client", "GetRequestAuthorizationDetailsPaginator", "IAMToolboxPreviewClient")
