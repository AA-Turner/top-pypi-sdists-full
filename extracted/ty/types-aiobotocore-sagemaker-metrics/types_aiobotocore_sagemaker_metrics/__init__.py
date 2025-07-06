"""
Main interface for sagemaker-metrics service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_metrics/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemaker_metrics import (
        Client,
        SageMakerMetricsClient,
    )

    session = get_session()
    async with session.create_client("sagemaker-metrics") as client:
        client: SageMakerMetricsClient
        ...

    ```
"""

from .client import SageMakerMetricsClient

Client = SageMakerMetricsClient


__all__ = ("Client", "SageMakerMetricsClient")
