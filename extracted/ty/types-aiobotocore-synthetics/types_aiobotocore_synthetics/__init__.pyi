"""
Main interface for synthetics service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_synthetics import (
        Client,
        SyntheticsClient,
    )

    session = get_session()
    async with session.create_client("synthetics") as client:
        client: SyntheticsClient
        ...

    ```
"""

from .client import SyntheticsClient

Client = SyntheticsClient

__all__ = ("Client", "SyntheticsClient")
