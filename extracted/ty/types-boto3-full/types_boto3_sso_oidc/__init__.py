"""
Main interface for sso-oidc service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_oidc/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sso_oidc import (
        Client,
        SSOOIDCClient,
    )

    session = Session()
    client: SSOOIDCClient = session.client("sso-oidc")
    ```
"""

from .client import SSOOIDCClient

Client = SSOOIDCClient


__all__ = ("Client", "SSOOIDCClient")
