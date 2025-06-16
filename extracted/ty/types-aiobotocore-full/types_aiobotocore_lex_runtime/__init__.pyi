"""
Main interface for lex-runtime service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_runtime/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lex_runtime import (
        Client,
        LexRuntimeServiceClient,
    )

    session = get_session()
    async with session.create_client("lex-runtime") as client:
        client: LexRuntimeServiceClient
        ...

    ```
"""

from .client import LexRuntimeServiceClient

Client = LexRuntimeServiceClient

__all__ = ("Client", "LexRuntimeServiceClient")
