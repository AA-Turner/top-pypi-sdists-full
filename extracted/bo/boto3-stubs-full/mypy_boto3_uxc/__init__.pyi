"""
Main interface for uxc service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_uxc/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_uxc import (
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
