"""
Main interface for mwaa service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mwaa import (
        Client,
        ListEnvironmentsPaginator,
        MWAAClient,
    )

    session = get_session()
    async with session.create_client("mwaa") as client:
        client: MWAAClient
        ...


    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```
"""

from .client import MWAAClient
from .paginator import ListEnvironmentsPaginator

Client = MWAAClient

__all__ = ("Client", "ListEnvironmentsPaginator", "MWAAClient")
