"""
Main interface for sagemakerjobruntime service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemakerjobruntime/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemakerjobruntime import (
        Client,
        SagemakerJobRuntimeServiceClient,
    )

    session = get_session()
    async with session.create_client("sagemakerjobruntime") as client:
        client: SagemakerJobRuntimeServiceClient
        ...

    ```
"""

from .client import SagemakerJobRuntimeServiceClient

Client = SagemakerJobRuntimeServiceClient

__all__ = ("Client", "SagemakerJobRuntimeServiceClient")
