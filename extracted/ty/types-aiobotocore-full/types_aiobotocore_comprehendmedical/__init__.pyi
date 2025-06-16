"""
Main interface for comprehendmedical service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_comprehendmedical import (
        Client,
        ComprehendMedicalClient,
    )

    session = get_session()
    async with session.create_client("comprehendmedical") as client:
        client: ComprehendMedicalClient
        ...

    ```
"""

from .client import ComprehendMedicalClient

Client = ComprehendMedicalClient

__all__ = ("Client", "ComprehendMedicalClient")
