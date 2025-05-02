"""
Main interface for waf-regional service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_waf_regional/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_waf_regional import (
        Client,
        WAFRegionalClient,
    )

    session = Session()
    client: WAFRegionalClient = session.client("waf-regional")
    ```
"""

from .client import WAFRegionalClient

Client = WAFRegionalClient


__all__ = ("Client", "WAFRegionalClient")
