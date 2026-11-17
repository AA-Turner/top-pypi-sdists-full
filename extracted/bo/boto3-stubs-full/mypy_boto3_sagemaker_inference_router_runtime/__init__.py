"""
Main interface for sagemaker-inference-router-runtime service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_inference_router_runtime/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sagemaker_inference_router_runtime import (
        Client,
        SageMakerInferenceRouterRuntimeClient,
    )

    session = Session()
    client: SageMakerInferenceRouterRuntimeClient = session.client("sagemaker-inference-router-runtime")
    ```
"""

from .client import SageMakerInferenceRouterRuntimeClient

Client = SageMakerInferenceRouterRuntimeClient


__all__ = ("Client", "SageMakerInferenceRouterRuntimeClient")
