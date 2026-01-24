"""
Main interface for ssm-sap service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ssm_sap import (
        Client,
        ListApplicationsPaginator,
        ListComponentsPaginator,
        ListConfigurationCheckDefinitionsPaginator,
        ListConfigurationCheckOperationsPaginator,
        ListDatabasesPaginator,
        ListOperationEventsPaginator,
        ListOperationsPaginator,
        ListSubCheckResultsPaginator,
        ListSubCheckRuleResultsPaginator,
        SsmSapClient,
    )

    session = get_session()
    async with session.create_client("ssm-sap") as client:
        client: SsmSapClient
        ...


    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
    list_configuration_check_definitions_paginator: ListConfigurationCheckDefinitionsPaginator = client.get_paginator("list_configuration_check_definitions")
    list_configuration_check_operations_paginator: ListConfigurationCheckOperationsPaginator = client.get_paginator("list_configuration_check_operations")
    list_databases_paginator: ListDatabasesPaginator = client.get_paginator("list_databases")
    list_operation_events_paginator: ListOperationEventsPaginator = client.get_paginator("list_operation_events")
    list_operations_paginator: ListOperationsPaginator = client.get_paginator("list_operations")
    list_sub_check_results_paginator: ListSubCheckResultsPaginator = client.get_paginator("list_sub_check_results")
    list_sub_check_rule_results_paginator: ListSubCheckRuleResultsPaginator = client.get_paginator("list_sub_check_rule_results")
    ```
"""

from .client import SsmSapClient
from .paginator import (
    ListApplicationsPaginator,
    ListComponentsPaginator,
    ListConfigurationCheckDefinitionsPaginator,
    ListConfigurationCheckOperationsPaginator,
    ListDatabasesPaginator,
    ListOperationEventsPaginator,
    ListOperationsPaginator,
    ListSubCheckResultsPaginator,
    ListSubCheckRuleResultsPaginator,
)

Client = SsmSapClient


__all__ = (
    "Client",
    "ListApplicationsPaginator",
    "ListComponentsPaginator",
    "ListConfigurationCheckDefinitionsPaginator",
    "ListConfigurationCheckOperationsPaginator",
    "ListDatabasesPaginator",
    "ListOperationEventsPaginator",
    "ListOperationsPaginator",
    "ListSubCheckResultsPaginator",
    "ListSubCheckRuleResultsPaginator",
    "SsmSapClient",
)
