"""
Main interface for pi service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pi import (
        Client,
        PIClient,
    )

    session = get_session()
    async with session.create_client("pi") as client:
        client: PIClient
        ...

    ```
"""

from .client import PIClient

Client = PIClient

__all__ = ("Client", "PIClient")
