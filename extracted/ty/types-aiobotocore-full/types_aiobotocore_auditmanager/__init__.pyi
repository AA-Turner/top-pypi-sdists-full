"""
Main interface for auditmanager service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_auditmanager import (
        AuditManagerClient,
        Client,
    )

    session = get_session()
    async with session.create_client("auditmanager") as client:
        client: AuditManagerClient
        ...

    ```
"""

from .client import AuditManagerClient

Client = AuditManagerClient

__all__ = ("AuditManagerClient", "Client")
