"""
Main interface for payment-cryptography-data service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_payment_cryptography_data/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_payment_cryptography_data import (
        Client,
        PaymentCryptographyDataPlaneClient,
    )

    session = Session()
    client: PaymentCryptographyDataPlaneClient = session.client("payment-cryptography-data")
    ```
"""

from .client import PaymentCryptographyDataPlaneClient

Client = PaymentCryptographyDataPlaneClient

__all__ = ("Client", "PaymentCryptographyDataPlaneClient")
