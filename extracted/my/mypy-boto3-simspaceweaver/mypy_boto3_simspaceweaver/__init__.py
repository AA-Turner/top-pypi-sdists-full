"""
Main interface for simspaceweaver service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_simspaceweaver import (
        Client,
        SimSpaceWeaverClient,
    )

    session = Session()
    client: SimSpaceWeaverClient = session.client("simspaceweaver")
    ```
"""

from .client import SimSpaceWeaverClient

Client = SimSpaceWeaverClient


__all__ = ("Client", "SimSpaceWeaverClient")
