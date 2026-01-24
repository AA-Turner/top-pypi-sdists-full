"""
Main interface for launch-wizard service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_launch_wizard import (
        Client,
        LaunchWizardClient,
        ListDeploymentEventsPaginator,
        ListDeploymentPatternVersionsPaginator,
        ListDeploymentsPaginator,
        ListWorkloadDeploymentPatternsPaginator,
        ListWorkloadsPaginator,
    )

    session = get_session()
    async with session.create_client("launch-wizard") as client:
        client: LaunchWizardClient
        ...


    list_deployment_events_paginator: ListDeploymentEventsPaginator = client.get_paginator("list_deployment_events")
    list_deployment_pattern_versions_paginator: ListDeploymentPatternVersionsPaginator = client.get_paginator("list_deployment_pattern_versions")
    list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
    list_workload_deployment_patterns_paginator: ListWorkloadDeploymentPatternsPaginator = client.get_paginator("list_workload_deployment_patterns")
    list_workloads_paginator: ListWorkloadsPaginator = client.get_paginator("list_workloads")
    ```
"""

from .client import LaunchWizardClient
from .paginator import (
    ListDeploymentEventsPaginator,
    ListDeploymentPatternVersionsPaginator,
    ListDeploymentsPaginator,
    ListWorkloadDeploymentPatternsPaginator,
    ListWorkloadsPaginator,
)

Client = LaunchWizardClient


__all__ = (
    "Client",
    "LaunchWizardClient",
    "ListDeploymentEventsPaginator",
    "ListDeploymentPatternVersionsPaginator",
    "ListDeploymentsPaginator",
    "ListWorkloadDeploymentPatternsPaginator",
    "ListWorkloadsPaginator",
)
