"""
Main interface for cloudsearchdomain service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearchdomain/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudsearchdomain import (
        Client,
        CloudSearchDomainClient,
    )

    session = get_session()
    async with session.create_client("cloudsearchdomain") as client:
        client: CloudSearchDomainClient
        ...

    ```
"""

from .client import CloudSearchDomainClient

Client = CloudSearchDomainClient


__all__ = ("Client", "CloudSearchDomainClient")
