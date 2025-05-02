"""
Main interface for cloudtrail-data service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail_data/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_cloudtrail_data import (
        Client,
        CloudTrailDataServiceClient,
    )

    session = Session()
    client: CloudTrailDataServiceClient = session.client("cloudtrail-data")
    ```
"""

from .client import CloudTrailDataServiceClient

Client = CloudTrailDataServiceClient


__all__ = ("Client", "CloudTrailDataServiceClient")
