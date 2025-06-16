"""
Main interface for rds-data service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds_data/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_rds_data import (
        Client,
        RDSDataServiceClient,
    )

    session = get_session()
    async with session.create_client("rds-data") as client:
        client: RDSDataServiceClient
        ...

    ```
"""

from .client import RDSDataServiceClient

Client = RDSDataServiceClient


__all__ = ("Client", "RDSDataServiceClient")
