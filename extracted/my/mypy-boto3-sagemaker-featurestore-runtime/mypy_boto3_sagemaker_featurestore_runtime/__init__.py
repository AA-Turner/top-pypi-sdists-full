"""
Main interface for sagemaker-featurestore-runtime service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_featurestore_runtime/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sagemaker_featurestore_runtime import (
        Client,
        ListRecordsPaginator,
        SageMakerFeatureStoreRuntimeClient,
    )

    session = Session()
    client: SageMakerFeatureStoreRuntimeClient = session.client("sagemaker-featurestore-runtime")

    list_records_paginator: ListRecordsPaginator = client.get_paginator("list_records")
    ```
"""

from .client import SageMakerFeatureStoreRuntimeClient
from .paginator import ListRecordsPaginator

Client = SageMakerFeatureStoreRuntimeClient


__all__ = ("Client", "ListRecordsPaginator", "SageMakerFeatureStoreRuntimeClient")
