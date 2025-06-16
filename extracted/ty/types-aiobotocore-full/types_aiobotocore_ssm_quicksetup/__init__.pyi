"""
Main interface for ssm-quicksetup service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_quicksetup/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ssm_quicksetup import (
        Client,
        ListConfigurationManagersPaginator,
        ListConfigurationsPaginator,
        SystemsManagerQuickSetupClient,
    )

    session = get_session()
    async with session.create_client("ssm-quicksetup") as client:
        client: SystemsManagerQuickSetupClient
        ...


    list_configuration_managers_paginator: ListConfigurationManagersPaginator = client.get_paginator("list_configuration_managers")
    list_configurations_paginator: ListConfigurationsPaginator = client.get_paginator("list_configurations")
    ```
"""

from .client import SystemsManagerQuickSetupClient
from .paginator import ListConfigurationManagersPaginator, ListConfigurationsPaginator

Client = SystemsManagerQuickSetupClient

__all__ = (
    "Client",
    "ListConfigurationManagersPaginator",
    "ListConfigurationsPaginator",
    "SystemsManagerQuickSetupClient",
)
