"""
Main interface for signin service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signin/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_signin import (
        Client,
        SignInServiceClient,
    )

    session = get_session()
    async with session.create_client("signin") as client:
        client: SignInServiceClient
        ...

    ```
"""

from .client import SignInServiceClient

Client = SignInServiceClient

__all__ = ("Client", "SignInServiceClient")
