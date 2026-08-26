"""
Main interface for iam-toolbox service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iam_toolbox/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iam_toolbox import (
        Client,
        GetRequestAuthorizationDetailsPaginator,
        IAMToolboxPreviewClient,
    )

    session = Session()
    client: IAMToolboxPreviewClient = session.client("iam-toolbox")

    get_request_authorization_details_paginator: GetRequestAuthorizationDetailsPaginator = client.get_paginator("get_request_authorization_details")
    ```
"""

from .client import IAMToolboxPreviewClient
from .paginator import GetRequestAuthorizationDetailsPaginator

Client = IAMToolboxPreviewClient

__all__ = ("Client", "GetRequestAuthorizationDetailsPaginator", "IAMToolboxPreviewClient")
