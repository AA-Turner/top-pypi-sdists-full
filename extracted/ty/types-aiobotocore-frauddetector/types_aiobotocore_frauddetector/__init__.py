"""
Main interface for frauddetector service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_frauddetector import (
        Client,
        FraudDetectorClient,
    )

    session = get_session()
    async with session.create_client("frauddetector") as client:
        client: FraudDetectorClient
        ...

    ```
"""

from .client import FraudDetectorClient

Client = FraudDetectorClient


__all__ = ("Client", "FraudDetectorClient")
