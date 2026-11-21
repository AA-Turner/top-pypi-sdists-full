"""
Main interface for sagemaker-gateway-runtime service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_gateway_runtime/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sagemaker_gateway_runtime import (
        Client,
        SageMakerGatewayRuntimeClient,
    )

    session = Session()
    client: SageMakerGatewayRuntimeClient = session.client("sagemaker-gateway-runtime")
    ```
"""

from .client import SageMakerGatewayRuntimeClient

Client = SageMakerGatewayRuntimeClient

__all__ = ("Client", "SageMakerGatewayRuntimeClient")
