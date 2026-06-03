"""
Main interface for sagemakerjobruntime service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemakerjobruntime/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sagemakerjobruntime import (
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
