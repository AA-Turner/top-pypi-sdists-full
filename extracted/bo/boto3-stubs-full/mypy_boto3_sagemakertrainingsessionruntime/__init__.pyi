"""
Main interface for sagemakertrainingsessionruntime service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemakertrainingsessionruntime/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sagemakertrainingsessionruntime import (
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
