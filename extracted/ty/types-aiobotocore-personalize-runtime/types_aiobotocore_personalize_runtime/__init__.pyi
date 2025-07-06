"""
Main interface for personalize-runtime service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize_runtime/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_personalize_runtime import (
        Client,
        PersonalizeRuntimeClient,
    )

    session = get_session()
    async with session.create_client("personalize-runtime") as client:
        client: PersonalizeRuntimeClient
        ...

    ```
"""

from .client import PersonalizeRuntimeClient

Client = PersonalizeRuntimeClient

__all__ = ("Client", "PersonalizeRuntimeClient")
