"""
Main interface for sagemaker-edge service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_edge/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemaker_edge import (
        Client,
        SagemakerEdgeManagerClient,
    )

    session = get_session()
    async with session.create_client("sagemaker-edge") as client:
        client: SagemakerEdgeManagerClient
        ...

    ```
"""

from .client import SagemakerEdgeManagerClient

Client = SagemakerEdgeManagerClient


__all__ = ("Client", "SagemakerEdgeManagerClient")
