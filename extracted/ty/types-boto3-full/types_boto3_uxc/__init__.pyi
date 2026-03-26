"""
Main interface for uxc service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_uxc/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_uxc import (
        Client,
        ListServicesPaginator,
        UserExperienceCustomizationClient,
    )

    session = Session()
    client: UserExperienceCustomizationClient = session.client("uxc")

    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```
"""

from .client import UserExperienceCustomizationClient
from .paginator import ListServicesPaginator

Client = UserExperienceCustomizationClient

__all__ = ("Client", "ListServicesPaginator", "UserExperienceCustomizationClient")
