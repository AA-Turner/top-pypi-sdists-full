"""
Main interface for simspaceweaver service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_simspaceweaver/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_simspaceweaver import (
        Client,
        SimSpaceWeaverClient,
    )

    session = get_session()
    async with session.create_client("simspaceweaver") as client:
        client: SimSpaceWeaverClient
        ...

    ```
"""

from .client import SimSpaceWeaverClient

Client = SimSpaceWeaverClient

__all__ = ("Client", "SimSpaceWeaverClient")
