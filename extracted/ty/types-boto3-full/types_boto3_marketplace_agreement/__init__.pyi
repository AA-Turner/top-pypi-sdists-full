"""
Main interface for marketplace-agreement service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_marketplace_agreement import (
        AgreementServiceClient,
        Client,
    )

    session = Session()
    client: AgreementServiceClient = session.client("marketplace-agreement")
    ```
"""

from .client import AgreementServiceClient

Client = AgreementServiceClient

__all__ = ("AgreementServiceClient", "Client")
