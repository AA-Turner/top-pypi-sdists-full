"""
Main interface for signer-data service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signer_data/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_signer_data import (
        Client,
        SignerDataPlaneClient,
    )

    session = Session()
    client: SignerDataPlaneClient = session.client("signer-data")
    ```
"""

from .client import SignerDataPlaneClient

Client = SignerDataPlaneClient

__all__ = ("Client", "SignerDataPlaneClient")
