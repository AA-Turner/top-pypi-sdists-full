"""
Type annotations for autoscaling-plans service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling_plans/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_autoscaling_plans.client import AutoScalingPlansClient
    from types_boto3_autoscaling_plans.paginator import (
        DescribeScalingPlanResourcesPaginator,
        DescribeScalingPlansPaginator,
    )

    session = Session()
    client: AutoScalingPlansClient = session.client("autoscaling-plans")

    describe_scaling_plan_resources_paginator: DescribeScalingPlanResourcesPaginator = client.get_paginator("describe_scaling_plan_resources")
    describe_scaling_plans_paginator: DescribeScalingPlansPaginator = client.get_paginator("describe_scaling_plans")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _DescribeScalingPlanResourcesPaginatorBase = Paginator[
        DescribeScalingPlanResourcesResponseTypeDef
    ]
else:
    _DescribeScalingPlanResourcesPaginatorBase = Paginator  # type: ignore[assignment]

class DescribeScalingPlanResourcesPaginator(_DescribeScalingPlanResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlanResources.html#AutoScalingPlans.Paginator.DescribeScalingPlanResources)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling_plans/paginators/#describescalingplanresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeScalingPlanResourcesRequestPaginateTypeDef]
    ) -> PageIterator[DescribeScalingPlanResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlanResources.html#AutoScalingPlans.Paginator.DescribeScalingPlanResources.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling_plans/paginators/#describescalingplanresourcespaginator)
        """

if TYPE_CHECKING:
    _DescribeScalingPlansPaginatorBase = Paginator[DescribeScalingPlansResponseTypeDef]
else:
    _DescribeScalingPlansPaginatorBase = Paginator  # type: ignore[assignment]

class DescribeScalingPlansPaginator(_DescribeScalingPlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlans.html#AutoScalingPlans.Paginator.DescribeScalingPlans)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling_plans/paginators/#describescalingplanspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeScalingPlansRequestPaginateTypeDef]
    ) -> PageIterator[DescribeScalingPlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlans.html#AutoScalingPlans.Paginator.DescribeScalingPlans.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling_plans/paginators/#describescalingplanspaginator)
        """
