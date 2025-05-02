"""
Main interface for neptunedata service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_neptunedata import (
        Client,
        NeptuneDataClient,
    )

    session = get_session()
    async with session.create_client("neptunedata") as client:
        client: NeptuneDataClient
        ...

    ```
"""

from .client import NeptuneDataClient

Client = NeptuneDataClient


__all__ = ("Client", "NeptuneDataClient")
