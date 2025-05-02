"""
Main interface for codestar-connections service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_connections/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codestar_connections import (
        Client,
        CodeStarconnectionsClient,
    )

    session = get_session()
    async with session.create_client("codestar-connections") as client:
        client: CodeStarconnectionsClient
        ...

    ```
"""

from .client import CodeStarconnectionsClient

Client = CodeStarconnectionsClient

__all__ = ("Client", "CodeStarconnectionsClient")
