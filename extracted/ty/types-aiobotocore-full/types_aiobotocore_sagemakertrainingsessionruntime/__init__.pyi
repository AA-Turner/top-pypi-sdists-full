"""
Main interface for sagemakertrainingsessionruntime service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemakertrainingsessionruntime/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemakertrainingsessionruntime import (
        Client,
        SageMakerTrainingSessionRuntimeClient,
    )

    session = get_session()
    async with session.create_client("sagemakertrainingsessionruntime") as client:
        client: SageMakerTrainingSessionRuntimeClient
        ...

    ```
"""

from .client import SageMakerTrainingSessionRuntimeClient

Client = SageMakerTrainingSessionRuntimeClient

__all__ = ("Client", "SageMakerTrainingSessionRuntimeClient")
