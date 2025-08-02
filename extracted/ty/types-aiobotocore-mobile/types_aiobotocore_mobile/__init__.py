"""
Main interface for mobile service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mobile import (
        Client,
        ListBundlesPaginator,
        ListProjectsPaginator,
        MobileClient,
    )

    session = get_session()
    async with session.create_client("mobile") as client:
        client: MobileClient
        ...


    list_bundles_paginator: ListBundlesPaginator = client.get_paginator("list_bundles")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    ```
"""

from .client import MobileClient
from .paginator import ListBundlesPaginator, ListProjectsPaginator

Client = MobileClient

__all__ = ("Client", "ListBundlesPaginator", "ListProjectsPaginator", "MobileClient")
