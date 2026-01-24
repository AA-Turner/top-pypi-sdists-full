"""
Main interface for signin service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_signin import (
        Client,
        SignInServiceClient,
    )

    session = Session()
    client: SignInServiceClient = session.client("signin")
    ```
"""

from .client import SignInServiceClient

Client = SignInServiceClient

__all__ = ("Client", "SignInServiceClient")
