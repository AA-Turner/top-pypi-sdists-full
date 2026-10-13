"""
Main interface for sagemakertrainingsessionruntime service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemakertrainingsessionruntime/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sagemakertrainingsessionruntime import (
        Client,
        SageMakerTrainingSessionRuntimeClient,
    )

    session = Session()
    client: SageMakerTrainingSessionRuntimeClient = session.client("sagemakertrainingsessionruntime")
    ```
"""

from .client import SageMakerTrainingSessionRuntimeClient

Client = SageMakerTrainingSessionRuntimeClient

__all__ = ("Client", "SageMakerTrainingSessionRuntimeClient")
