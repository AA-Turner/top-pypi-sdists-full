"""
Main interface for sagemaker-featurestore-runtime service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_featurestore_runtime/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemaker_featurestore_runtime import (
        Client,
        SageMakerFeatureStoreRuntimeClient,
    )

    session = get_session()
    async with session.create_client("sagemaker-featurestore-runtime") as client:
        client: SageMakerFeatureStoreRuntimeClient
        ...

    ```
"""

from .client import SageMakerFeatureStoreRuntimeClient

Client = SageMakerFeatureStoreRuntimeClient


__all__ = ("Client", "SageMakerFeatureStoreRuntimeClient")
