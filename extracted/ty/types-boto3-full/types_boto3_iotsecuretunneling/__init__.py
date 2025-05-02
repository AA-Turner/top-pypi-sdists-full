"""
Main interface for iotsecuretunneling service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotsecuretunneling/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iotsecuretunneling import (
        Client,
        IoTSecureTunnelingClient,
    )

    session = Session()
    client: IoTSecureTunnelingClient = session.client("iotsecuretunneling")
    ```
"""

from .client import IoTSecureTunnelingClient

Client = IoTSecureTunnelingClient


__all__ = ("Client", "IoTSecureTunnelingClient")
