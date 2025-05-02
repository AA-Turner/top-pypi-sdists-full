"""
Main interface for autoscaling-plans service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_autoscaling_plans import (
        AutoScalingPlansClient,
        Client,
        DescribeScalingPlanResourcesPaginator,
        DescribeScalingPlansPaginator,
    )

    session = get_session()
    async with session.create_client("autoscaling-plans") as client:
        client: AutoScalingPlansClient
        ...


    describe_scaling_plan_resources_paginator: DescribeScalingPlanResourcesPaginator = client.get_paginator("describe_scaling_plan_resources")
    describe_scaling_plans_paginator: DescribeScalingPlansPaginator = client.get_paginator("describe_scaling_plans")
    ```
"""

from .client import AutoScalingPlansClient
from .paginator import DescribeScalingPlanResourcesPaginator, DescribeScalingPlansPaginator

Client = AutoScalingPlansClient

__all__ = (
    "AutoScalingPlansClient",
    "Client",
    "DescribeScalingPlanResourcesPaginator",
    "DescribeScalingPlansPaginator",
)
