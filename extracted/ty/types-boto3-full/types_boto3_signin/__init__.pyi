"""
Main interface for signin service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_signin import (
        Client,
        ListResourcePermissionStatementsPaginator,
        SignInServiceClient,
    )

    session = Session()
    client: SignInServiceClient = session.client("signin")

    list_resource_permission_statements_paginator: ListResourcePermissionStatementsPaginator = client.get_paginator("list_resource_permission_statements")
    ```
"""

from .client import SignInServiceClient
from .paginator import ListResourcePermissionStatementsPaginator

Client = SignInServiceClient

__all__ = ("Client", "ListResourcePermissionStatementsPaginator", "SignInServiceClient")
