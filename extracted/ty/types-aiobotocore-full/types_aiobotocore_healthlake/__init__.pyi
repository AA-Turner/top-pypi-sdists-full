"""
Main interface for healthlake service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_healthlake import (
        Client,
        HealthLakeClient,
    )

    session = get_session()
    async with session.create_client("healthlake") as client:
        client: HealthLakeClient
        ...

    ```
"""

from .client import HealthLakeClient

Client = HealthLakeClient

__all__ = ("Client", "HealthLakeClient")
