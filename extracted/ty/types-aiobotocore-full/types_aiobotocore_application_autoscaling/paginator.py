"""
Type annotations for application-autoscaling service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_application_autoscaling.client import ApplicationAutoScalingClient
    from types_aiobotocore_application_autoscaling.paginator import (
        DescribeScalableTargetsPaginator,
        DescribeScalingActivitiesPaginator,
        DescribeScalingPoliciesPaginator,
        DescribeScheduledActionsPaginator,
    )

    session = get_session()
    with session.create_client("application-autoscaling") as client:
        client: ApplicationAutoScalingClient

        describe_scalable_targets_paginator: DescribeScalableTargetsPaginator = client.get_paginator("describe_scalable_targets")
        describe_scaling_activities_paginator: DescribeScalingActivitiesPaginator = client.get_paginator("describe_scaling_activities")
        describe_scaling_policies_paginator: DescribeScalingPoliciesPaginator = client.get_paginator("describe_scaling_policies")
        describe_scheduled_actions_paginator: DescribeScheduledActionsPaginator = client.get_paginator("describe_scheduled_actions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeScalableTargetsRequestPaginateTypeDef,
    DescribeScalableTargetsResponseTypeDef,
    DescribeScalingActivitiesRequestPaginateTypeDef,
    DescribeScalingActivitiesResponseTypeDef,
    DescribeScalingPoliciesRequestPaginateTypeDef,
    DescribeScalingPoliciesResponseTypeDef,
    DescribeScheduledActionsRequestPaginateTypeDef,
    DescribeScheduledActionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeScalableTargetsPaginator",
    "DescribeScalingActivitiesPaginator",
    "DescribeScalingPoliciesPaginator",
    "DescribeScheduledActionsPaginator",
)


if TYPE_CHECKING:
    _DescribeScalableTargetsPaginatorBase = AioPaginator[DescribeScalableTargetsResponseTypeDef]
else:
    _DescribeScalableTargetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeScalableTargetsPaginator(_DescribeScalableTargetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScalableTargets.html#ApplicationAutoScaling.Paginator.DescribeScalableTargets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/paginators/#describescalabletargetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeScalableTargetsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeScalableTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScalableTargets.html#ApplicationAutoScaling.Paginator.DescribeScalableTargets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/paginators/#describescalabletargetspaginator)
        """


if TYPE_CHECKING:
    _DescribeScalingActivitiesPaginatorBase = AioPaginator[DescribeScalingActivitiesResponseTypeDef]
else:
    _DescribeScalingActivitiesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeScalingActivitiesPaginator(_DescribeScalingActivitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScalingActivities.html#ApplicationAutoScaling.Paginator.DescribeScalingActivities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/paginators/#describescalingactivitiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeScalingActivitiesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeScalingActivitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScalingActivities.html#ApplicationAutoScaling.Paginator.DescribeScalingActivities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/paginators/#describescalingactivitiespaginator)
        """


if TYPE_CHECKING:
    _DescribeScalingPoliciesPaginatorBase = AioPaginator[DescribeScalingPoliciesResponseTypeDef]
else:
    _DescribeScalingPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeScalingPoliciesPaginator(_DescribeScalingPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScalingPolicies.html#ApplicationAutoScaling.Paginator.DescribeScalingPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/paginators/#describescalingpoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeScalingPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeScalingPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScalingPolicies.html#ApplicationAutoScaling.Paginator.DescribeScalingPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/paginators/#describescalingpoliciespaginator)
        """


if TYPE_CHECKING:
    _DescribeScheduledActionsPaginatorBase = AioPaginator[DescribeScheduledActionsResponseTypeDef]
else:
    _DescribeScheduledActionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeScheduledActionsPaginator(_DescribeScheduledActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScheduledActions.html#ApplicationAutoScaling.Paginator.DescribeScheduledActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/paginators/#describescheduledactionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeScheduledActionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeScheduledActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/paginator/DescribeScheduledActions.html#ApplicationAutoScaling.Paginator.DescribeScheduledActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/paginators/#describescheduledactionspaginator)
        """
