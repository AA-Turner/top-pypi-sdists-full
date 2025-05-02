"""
Main interface for eks-auth service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_eks_auth/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_eks_auth import (
        Client,
        EKSAuthClient,
    )

    session = Session()
    client: EKSAuthClient = session.client("eks-auth")
    ```
"""

from .client import EKSAuthClient

Client = EKSAuthClient


__all__ = ("Client", "EKSAuthClient")
