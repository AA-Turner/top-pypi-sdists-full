"""
Main interface for personalize-runtime service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_personalize_runtime/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_personalize_runtime import (
        Client,
        PersonalizeRuntimeClient,
    )

    session = Session()
    client: PersonalizeRuntimeClient = session.client("personalize-runtime")
    ```
"""

from .client import PersonalizeRuntimeClient

Client = PersonalizeRuntimeClient


__all__ = ("Client", "PersonalizeRuntimeClient")
