"""
Main interface for comprehendmedical service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_comprehendmedical/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_comprehendmedical import (
        Client,
        ComprehendMedicalClient,
    )

    session = Session()
    client: ComprehendMedicalClient = session.client("comprehendmedical")
    ```
"""

from .client import ComprehendMedicalClient

Client = ComprehendMedicalClient


__all__ = ("Client", "ComprehendMedicalClient")
