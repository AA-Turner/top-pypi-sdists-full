"""
Main interface for fis service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_fis import (
        Client,
        FISClient,
        ListActionsPaginator,
        ListExperimentResolvedTargetsPaginator,
        ListExperimentTemplatesPaginator,
        ListExperimentsPaginator,
        ListTargetAccountConfigurationsPaginator,
        ListTargetResourceTypesPaginator,
    )

    session = get_session()
    async with session.create_client("fis") as client:
        client: FISClient
        ...


    list_actions_paginator: ListActionsPaginator = client.get_paginator("list_actions")
    list_experiment_resolved_targets_paginator: ListExperimentResolvedTargetsPaginator = client.get_paginator("list_experiment_resolved_targets")
    list_experiment_templates_paginator: ListExperimentTemplatesPaginator = client.get_paginator("list_experiment_templates")
    list_experiments_paginator: ListExperimentsPaginator = client.get_paginator("list_experiments")
    list_target_account_configurations_paginator: ListTargetAccountConfigurationsPaginator = client.get_paginator("list_target_account_configurations")
    list_target_resource_types_paginator: ListTargetResourceTypesPaginator = client.get_paginator("list_target_resource_types")
    ```
"""

from .client import FISClient
from .paginator import (
    ListActionsPaginator,
    ListExperimentResolvedTargetsPaginator,
    ListExperimentsPaginator,
    ListExperimentTemplatesPaginator,
    ListTargetAccountConfigurationsPaginator,
    ListTargetResourceTypesPaginator,
)

Client = FISClient


__all__ = (
    "Client",
    "FISClient",
    "ListActionsPaginator",
    "ListExperimentResolvedTargetsPaginator",
    "ListExperimentTemplatesPaginator",
    "ListExperimentsPaginator",
    "ListTargetAccountConfigurationsPaginator",
    "ListTargetResourceTypesPaginator",
)
