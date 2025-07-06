"""
Main interface for inspector-scan service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector_scan/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_inspector_scan import (
        Client,
        InspectorscanClient,
    )

    session = get_session()
    async with session.create_client("inspector-scan") as client:
        client: InspectorscanClient
        ...

    ```
"""

from .client import InspectorscanClient

Client = InspectorscanClient


__all__ = ("Client", "InspectorscanClient")
