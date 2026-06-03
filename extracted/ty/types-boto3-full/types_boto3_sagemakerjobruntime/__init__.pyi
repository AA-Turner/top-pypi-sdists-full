"""
Main interface for sagemakerjobruntime service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemakerjobruntime/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sagemakerjobruntime import (
        Client,
        SagemakerJobRuntimeServiceClient,
    )

    session = Session()
    client: SagemakerJobRuntimeServiceClient = session.client("sagemakerjobruntime")
    ```
"""

from .client import SagemakerJobRuntimeServiceClient

Client = SagemakerJobRuntimeServiceClient

__all__ = ("Client", "SagemakerJobRuntimeServiceClient")
