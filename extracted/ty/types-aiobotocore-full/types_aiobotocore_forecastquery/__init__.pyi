"""
Main interface for forecastquery service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_forecastquery/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_forecastquery import (
        Client,
        ForecastQueryServiceClient,
    )

    session = get_session()
    async with session.create_client("forecastquery") as client:
        client: ForecastQueryServiceClient
        ...

    ```
"""

from .client import ForecastQueryServiceClient

Client = ForecastQueryServiceClient

__all__ = ("Client", "ForecastQueryServiceClient")
