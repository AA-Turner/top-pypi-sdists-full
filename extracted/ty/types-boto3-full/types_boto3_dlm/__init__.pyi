"""
Main interface for dlm service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dlm/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_dlm import (
        Client,
        DLMClient,
    )

    session = Session()
    client: DLMClient = session.client("dlm")
    ```
"""

from .client import DLMClient

Client = DLMClient

__all__ = ("Client", "DLMClient")
