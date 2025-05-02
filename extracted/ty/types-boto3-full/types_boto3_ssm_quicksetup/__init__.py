"""
Main interface for ssm-quicksetup service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_quicksetup/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_ssm_quicksetup import (
        Client,
        ListConfigurationManagersPaginator,
        ListConfigurationsPaginator,
        SystemsManagerQuickSetupClient,
    )

    session = Session()
    client: SystemsManagerQuickSetupClient = session.client("ssm-quicksetup")

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
