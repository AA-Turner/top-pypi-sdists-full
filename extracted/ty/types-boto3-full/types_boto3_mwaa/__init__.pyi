"""
Main interface for mwaa service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_mwaa import (
        Client,
        ListEnvironmentsPaginator,
        MWAAClient,
    )

    session = Session()
    client: MWAAClient = session.client("mwaa")

    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```
"""

from .client import MWAAClient
from .paginator import ListEnvironmentsPaginator

Client = MWAAClient

__all__ = ("Client", "ListEnvironmentsPaginator", "MWAAClient")
