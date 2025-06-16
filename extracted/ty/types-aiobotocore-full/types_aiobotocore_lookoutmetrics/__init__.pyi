"""
Main interface for lookoutmetrics service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lookoutmetrics import (
        Client,
        LookoutMetricsClient,
    )

    session = get_session()
    async with session.create_client("lookoutmetrics") as client:
        client: LookoutMetricsClient
        ...

    ```
"""

from .client import LookoutMetricsClient

Client = LookoutMetricsClient

__all__ = ("Client", "LookoutMetricsClient")
