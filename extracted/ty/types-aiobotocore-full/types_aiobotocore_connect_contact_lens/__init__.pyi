"""
Main interface for connect-contact-lens service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect_contact_lens/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connect_contact_lens import (
        Client,
        ConnectContactLensClient,
    )

    session = get_session()
    async with session.create_client("connect-contact-lens") as client:
        client: ConnectContactLensClient
        ...

    ```
"""

from .client import ConnectContactLensClient

Client = ConnectContactLensClient

__all__ = ("Client", "ConnectContactLensClient")
