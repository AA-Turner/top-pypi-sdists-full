"""
Main interface for lambda-web service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lambda_web/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_lambda_web import (
        Client,
        LambdaWebClient,
    )

    session = Session()
    client: LambdaWebClient = session.client("lambda-web")
    ```
"""

from .client import LambdaWebClient

Client = LambdaWebClient


__all__ = ("Client", "LambdaWebClient")
