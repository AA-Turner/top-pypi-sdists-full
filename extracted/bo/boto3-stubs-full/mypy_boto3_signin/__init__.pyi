"""
Main interface for signin service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signin/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_signin import (
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
