"""
Main interface for personalize-events service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize_events/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_personalize_events import (
        Client,
        PersonalizeEventsClient,
    )

    session = get_session()
    async with session.create_client("personalize-events") as client:
        client: PersonalizeEventsClient
        ...

    ```
"""

from .client import PersonalizeEventsClient

Client = PersonalizeEventsClient


__all__ = ("Client", "PersonalizeEventsClient")
