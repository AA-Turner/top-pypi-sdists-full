"""
Main interface for payment-cryptography-data service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_payment_cryptography_data import (
        Client,
        PaymentCryptographyDataPlaneClient,
    )

    session = get_session()
    async with session.create_client("payment-cryptography-data") as client:
        client: PaymentCryptographyDataPlaneClient
        ...

    ```
"""

from .client import PaymentCryptographyDataPlaneClient

Client = PaymentCryptographyDataPlaneClient


__all__ = ("Client", "PaymentCryptographyDataPlaneClient")
