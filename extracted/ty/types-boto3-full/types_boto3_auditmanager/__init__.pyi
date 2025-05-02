"""
Main interface for auditmanager service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_auditmanager import (
        AuditManagerClient,
        Client,
    )

    session = Session()
    client: AuditManagerClient = session.client("auditmanager")
    ```
"""

from .client import AuditManagerClient

Client = AuditManagerClient

__all__ = ("AuditManagerClient", "Client")
