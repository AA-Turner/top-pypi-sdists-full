"""
Type annotations for autoscaling-plans service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_autoscaling_plans.client import AutoScalingPlansClient
    from types_aiobotocore_autoscaling_plans.paginator import (
        DescribeScalingPlanResourcesPaginator,
        DescribeScalingPlansPaginator,
    )

    session = get_session()
    with session.create_client("autoscaling-plans") as client:
        client: AutoScalingPlansClient

        describe_scaling_plan_resources_paginator: DescribeScalingPlanResourcesPaginator = client.get_paginator("describe_scaling_plan_resources")
        describe_scaling_plans_paginator: DescribeScalingPlansPaginator = client.get_paginator("describe_scaling_plans")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeScalingPlanResourcesRequestPaginateTypeDef,
    DescribeScalingPlanResourcesResponseTypeDef,
    DescribeScalingPlansRequestPaginateTypeDef,
    DescribeScalingPlansResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DescribeScalingPlanResourcesPaginator", "DescribeScalingPlansPaginator")


if TYPE_CHECKING:
    _DescribeScalingPlanResourcesPaginatorBase = AioPaginator[
        DescribeScalingPlanResourcesResponseTypeDef
    ]
else:
    _DescribeScalingPlanResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeScalingPlanResourcesPaginator(_DescribeScalingPlanResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlanResources.html#AutoScalingPlans.Paginator.DescribeScalingPlanResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/paginators/#describescalingplanresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeScalingPlanResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeScalingPlanResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlanResources.html#AutoScalingPlans.Paginator.DescribeScalingPlanResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/paginators/#describescalingplanresourcespaginator)
        """


if TYPE_CHECKING:
    _DescribeScalingPlansPaginatorBase = AioPaginator[DescribeScalingPlansResponseTypeDef]
else:
    _DescribeScalingPlansPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeScalingPlansPaginator(_DescribeScalingPlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlans.html#AutoScalingPlans.Paginator.DescribeScalingPlans)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/paginators/#describescalingplanspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeScalingPlansRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeScalingPlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlans.html#AutoScalingPlans.Paginator.DescribeScalingPlans.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/paginators/#describescalingplanspaginator)
        """
