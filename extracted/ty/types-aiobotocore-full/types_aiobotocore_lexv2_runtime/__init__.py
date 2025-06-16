"""
Main interface for lexv2-runtime service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_runtime/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lexv2_runtime import (
        Client,
        LexRuntimeV2Client,
    )

    session = get_session()
    async with session.create_client("lexv2-runtime") as client:
        client: LexRuntimeV2Client
        ...

    ```
"""

from .client import LexRuntimeV2Client

Client = LexRuntimeV2Client


__all__ = ("Client", "LexRuntimeV2Client")
