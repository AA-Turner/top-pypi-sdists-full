"""
Main interface for ivschat service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ivschat/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_ivschat import (
        Client,
        IvschatClient,
    )

    session = Session()
    client: IvschatClient = session.client("ivschat")
    ```
"""

from .client import IvschatClient

Client = IvschatClient


__all__ = ("Client", "IvschatClient")
