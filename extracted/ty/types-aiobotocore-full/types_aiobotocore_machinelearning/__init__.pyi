"""
Main interface for machinelearning service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_machinelearning/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_machinelearning import (
        BatchPredictionAvailableWaiter,
        Client,
        DataSourceAvailableWaiter,
        DescribeBatchPredictionsPaginator,
        DescribeDataSourcesPaginator,
        DescribeEvaluationsPaginator,
        DescribeMLModelsPaginator,
        EvaluationAvailableWaiter,
        MLModelAvailableWaiter,
        MachineLearningClient,
    )

    session = get_session()
    async with session.create_client("machinelearning") as client:
        client: MachineLearningClient
        ...


    batch_prediction_available_waiter: BatchPredictionAvailableWaiter = client.get_waiter("batch_prediction_available")
    data_source_available_waiter: DataSourceAvailableWaiter = client.get_waiter("data_source_available")
    evaluation_available_waiter: EvaluationAvailableWaiter = client.get_waiter("evaluation_available")
    ml_model_available_waiter: MLModelAvailableWaiter = client.get_waiter("ml_model_available")

    describe_batch_predictions_paginator: DescribeBatchPredictionsPaginator = client.get_paginator("describe_batch_predictions")
    describe_data_sources_paginator: DescribeDataSourcesPaginator = client.get_paginator("describe_data_sources")
    describe_evaluations_paginator: DescribeEvaluationsPaginator = client.get_paginator("describe_evaluations")
    describe_ml_models_paginator: DescribeMLModelsPaginator = client.get_paginator("describe_ml_models")
    ```
"""

from .client import MachineLearningClient
from .paginator import (
    DescribeBatchPredictionsPaginator,
    DescribeDataSourcesPaginator,
    DescribeEvaluationsPaginator,
    DescribeMLModelsPaginator,
)
from .waiter import (
    BatchPredictionAvailableWaiter,
    DataSourceAvailableWaiter,
    EvaluationAvailableWaiter,
    MLModelAvailableWaiter,
)

Client = MachineLearningClient

__all__ = (
    "BatchPredictionAvailableWaiter",
    "Client",
    "DataSourceAvailableWaiter",
    "DescribeBatchPredictionsPaginator",
    "DescribeDataSourcesPaginator",
    "DescribeEvaluationsPaginator",
    "DescribeMLModelsPaginator",
    "EvaluationAvailableWaiter",
    "MLModelAvailableWaiter",
    "MachineLearningClient",
)
