"""
Main interface for bedrock-data-automation service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_bedrock_data_automation import (
        Client,
        DataAutomationforBedrockClient,
        ListBlueprintsPaginator,
        ListDataAutomationProjectsPaginator,
    )

    session = get_session()
    async with session.create_client("bedrock-data-automation") as client:
        client: DataAutomationforBedrockClient
        ...


    list_blueprints_paginator: ListBlueprintsPaginator = client.get_paginator("list_blueprints")
    list_data_automation_projects_paginator: ListDataAutomationProjectsPaginator = client.get_paginator("list_data_automation_projects")
    ```
"""

from .client import DataAutomationforBedrockClient
from .paginator import ListBlueprintsPaginator, ListDataAutomationProjectsPaginator

Client = DataAutomationforBedrockClient


__all__ = (
    "Client",
    "DataAutomationforBedrockClient",
    "ListBlueprintsPaginator",
    "ListDataAutomationProjectsPaginator",
)
