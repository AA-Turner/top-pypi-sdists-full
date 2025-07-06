"""
Main interface for marketplace-agreement service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplace_agreement import (
        AgreementServiceClient,
        Client,
    )

    session = get_session()
    async with session.create_client("marketplace-agreement") as client:
        client: AgreementServiceClient
        ...

    ```
"""

from .client import AgreementServiceClient

Client = AgreementServiceClient


__all__ = ("AgreementServiceClient", "Client")
