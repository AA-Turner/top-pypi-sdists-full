"""
Main interface for eks-auth service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks_auth/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_eks_auth import (
        Client,
        EKSAuthClient,
    )

    session = get_session()
    async with session.create_client("eks-auth") as client:
        client: EKSAuthClient
        ...

    ```
"""

from .client import EKSAuthClient

Client = EKSAuthClient


__all__ = ("Client", "EKSAuthClient")
