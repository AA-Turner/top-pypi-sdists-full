"""
Main interface for lambda-web service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_lambda_web import (
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
