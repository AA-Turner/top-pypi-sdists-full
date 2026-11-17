"""
Main interface for connectscheduling service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectscheduling/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_connectscheduling import (
        Client,
        ConnectSchedulingClient,
    )

    session = Session()
    client: ConnectSchedulingClient = session.client("connectscheduling")
    ```
"""

from .client import ConnectSchedulingClient

Client = ConnectSchedulingClient


__all__ = ("Client", "ConnectSchedulingClient")
