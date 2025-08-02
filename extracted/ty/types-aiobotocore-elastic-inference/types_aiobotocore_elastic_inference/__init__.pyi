"""
Main interface for elastic-inference service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_elastic_inference import (
        Client,
        DescribeAcceleratorsPaginator,
        ElasticInferenceClient,
    )

    session = get_session()
    async with session.create_client("elastic-inference") as client:
        client: ElasticInferenceClient
        ...


    describe_accelerators_paginator: DescribeAcceleratorsPaginator = client.get_paginator("describe_accelerators")
    ```
"""

from .client import ElasticInferenceClient
from .paginator import DescribeAcceleratorsPaginator

Client = ElasticInferenceClient

__all__ = ("Client", "DescribeAcceleratorsPaginator", "ElasticInferenceClient")
