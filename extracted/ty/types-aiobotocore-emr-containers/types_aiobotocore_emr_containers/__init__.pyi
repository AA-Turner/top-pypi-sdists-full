"""
Main interface for emr-containers service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_emr_containers import (
        Client,
        EMRContainersClient,
        ListJobRunsPaginator,
        ListJobTemplatesPaginator,
        ListManagedEndpointsPaginator,
        ListSecurityConfigurationsPaginator,
        ListVirtualClustersPaginator,
    )

    session = get_session()
    async with session.create_client("emr-containers") as client:
        client: EMRContainersClient
        ...


    list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
    list_job_templates_paginator: ListJobTemplatesPaginator = client.get_paginator("list_job_templates")
    list_managed_endpoints_paginator: ListManagedEndpointsPaginator = client.get_paginator("list_managed_endpoints")
    list_security_configurations_paginator: ListSecurityConfigurationsPaginator = client.get_paginator("list_security_configurations")
    list_virtual_clusters_paginator: ListVirtualClustersPaginator = client.get_paginator("list_virtual_clusters")
    ```
"""

from .client import EMRContainersClient
from .paginator import (
    ListJobRunsPaginator,
    ListJobTemplatesPaginator,
    ListManagedEndpointsPaginator,
    ListSecurityConfigurationsPaginator,
    ListVirtualClustersPaginator,
)

Client = EMRContainersClient

__all__ = (
    "Client",
    "EMRContainersClient",
    "ListJobRunsPaginator",
    "ListJobTemplatesPaginator",
    "ListManagedEndpointsPaginator",
    "ListSecurityConfigurationsPaginator",
    "ListVirtualClustersPaginator",
)
