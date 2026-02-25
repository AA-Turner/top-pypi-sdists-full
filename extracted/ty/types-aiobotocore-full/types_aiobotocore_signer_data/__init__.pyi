"""
Main interface for signer-data service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer_data/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_signer_data import (
        Client,
        SignerDataPlaneClient,
    )

    session = get_session()
    async with session.create_client("signer-data") as client:
        client: SignerDataPlaneClient
        ...

    ```
"""

from .client import SignerDataPlaneClient

Client = SignerDataPlaneClient

__all__ = ("Client", "SignerDataPlaneClient")
