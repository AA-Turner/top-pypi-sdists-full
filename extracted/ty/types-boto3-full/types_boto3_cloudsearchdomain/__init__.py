"""
Main interface for cloudsearchdomain service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudsearchdomain/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_cloudsearchdomain import (
        Client,
        CloudSearchDomainClient,
    )

    session = Session()
    client: CloudSearchDomainClient = session.client("cloudsearchdomain")
    ```
"""

from .client import CloudSearchDomainClient

Client = CloudSearchDomainClient


__all__ = ("Client", "CloudSearchDomainClient")
