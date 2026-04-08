"""
Main interface for uxc service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_uxc/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_uxc import (
        Client,
        ListServicesPaginator,
        UserExperienceCustomizationClient,
    )

    session = get_session()
    async with session.create_client("uxc") as client:
        client: UserExperienceCustomizationClient
        ...


    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```
"""

from .client import UserExperienceCustomizationClient
from .paginator import ListServicesPaginator

Client = UserExperienceCustomizationClient


__all__ = ("Client", "ListServicesPaginator", "UserExperienceCustomizationClient")
