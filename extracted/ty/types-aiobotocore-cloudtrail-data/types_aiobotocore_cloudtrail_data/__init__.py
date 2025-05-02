"""
Main interface for cloudtrail-data service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail_data/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudtrail_data import (
        Client,
        CloudTrailDataServiceClient,
    )

    session = get_session()
    async with session.create_client("cloudtrail-data") as client:
        client: CloudTrailDataServiceClient
        ...

    ```
"""

from .client import CloudTrailDataServiceClient

Client = CloudTrailDataServiceClient


__all__ = ("Client", "CloudTrailDataServiceClient")
