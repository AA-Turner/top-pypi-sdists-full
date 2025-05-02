"""
Main interface for sagemaker-runtime service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_runtime/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemaker_runtime import (
        Client,
        SageMakerRuntimeClient,
    )

    session = get_session()
    async with session.create_client("sagemaker-runtime") as client:
        client: SageMakerRuntimeClient
        ...

    ```
"""

from .client import SageMakerRuntimeClient

Client = SageMakerRuntimeClient

__all__ = ("Client", "SageMakerRuntimeClient")
