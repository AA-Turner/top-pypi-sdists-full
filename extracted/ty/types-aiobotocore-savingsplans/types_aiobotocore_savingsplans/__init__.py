"""
Main interface for savingsplans service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_savingsplans import (
        Client,
        SavingsPlansClient,
    )

    session = get_session()
    async with session.create_client("savingsplans") as client:
        client: SavingsPlansClient
        ...

    ```
"""

from .client import SavingsPlansClient

Client = SavingsPlansClient


__all__ = ("Client", "SavingsPlansClient")
