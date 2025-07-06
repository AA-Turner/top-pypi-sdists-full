"""
Main interface for cloud9 service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloud9/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloud9 import (
        Client,
        Cloud9Client,
        DescribeEnvironmentMembershipsPaginator,
        ListEnvironmentsPaginator,
    )

    session = get_session()
    async with session.create_client("cloud9") as client:
        client: Cloud9Client
        ...


    describe_environment_memberships_paginator: DescribeEnvironmentMembershipsPaginator = client.get_paginator("describe_environment_memberships")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```
"""

from .client import Cloud9Client
from .paginator import DescribeEnvironmentMembershipsPaginator, ListEnvironmentsPaginator

Client = Cloud9Client

__all__ = (
    "Client",
    "Cloud9Client",
    "DescribeEnvironmentMembershipsPaginator",
    "ListEnvironmentsPaginator",
)
