"""
Main interface for backupstorage service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_backupstorage import (
        BackupStorageClient,
        Client,
    )

    session = get_session()
    async with session.create_client("backupstorage") as client:
        client: BackupStorageClient
        ...

    ```
"""

from .client import BackupStorageClient

Client = BackupStorageClient

__all__ = ("BackupStorageClient", "Client")
