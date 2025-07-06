"""
Main interface for waf-regional service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_waf_regional import (
        Client,
        WAFRegionalClient,
    )

    session = get_session()
    async with session.create_client("waf-regional") as client:
        client: WAFRegionalClient
        ...

    ```
"""

from .client import WAFRegionalClient

Client = WAFRegionalClient

__all__ = ("Client", "WAFRegionalClient")
