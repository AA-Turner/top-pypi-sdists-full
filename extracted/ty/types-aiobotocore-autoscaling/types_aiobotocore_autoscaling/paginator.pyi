"""
Type annotations for autoscaling service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_autoscaling.client import AutoScalingClient
    from types_aiobotocore_autoscaling.paginator import (
        DescribeAutoScalingGroupsPaginator,
        DescribeAutoScalingInstancesPaginator,
        DescribeLaunchConfigurationsPaginator,
        DescribeLoadBalancerTargetGroupsPaginator,
        DescribeLoadBalancersPaginator,
        DescribeNotificationConfigurationsPaginator,
        DescribePoliciesPaginator,
        DescribeScalingActivitiesPaginator,
        DescribeScheduledActionsPaginator,
        DescribeTagsPaginator,
        DescribeWarmPoolPaginator,
    )

    session = get_session()
    with session.create_client("autoscaling") as client:
        client: AutoScalingClient

        describe_auto_scaling_groups_paginator: DescribeAutoScalingGroupsPaginator = client.get_paginator("describe_auto_scaling_groups")
        describe_auto_scaling_instances_paginator: DescribeAutoScalingInstancesPaginator = client.get_paginator("describe_auto_scaling_instances")
        describe_launch_configurations_paginator: DescribeLaunchConfigurationsPaginator = client.get_paginator("describe_launch_configurations")
        describe_load_balancer_target_groups_paginator: DescribeLoadBalancerTargetGroupsPaginator = client.get_paginator("describe_load_balancer_target_groups")
        describe_load_balancers_paginator: DescribeLoadBalancersPaginator = client.get_paginator("describe_load_balancers")
        describe_notification_configurations_paginator: DescribeNotificationConfigurationsPaginator = client.get_paginator("describe_notification_configurations")
        describe_policies_paginator: DescribePoliciesPaginator = client.get_paginator("describe_policies")
        describe_scaling_activities_paginator: DescribeScalingActivitiesPaginator = client.get_paginator("describe_scaling_activities")
        describe_scheduled_actions_paginator: DescribeScheduledActionsPaginator = client.get_paginator("describe_scheduled_actions")
        describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
        describe_warm_pool_paginator: DescribeWarmPoolPaginator = client.get_paginator("describe_warm_pool")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ActivitiesTypeTypeDef,
    AutoScalingGroupNamesTypePaginateTypeDef,
    AutoScalingGroupsTypeTypeDef,
    AutoScalingInstancesTypeTypeDef,
    DescribeAutoScalingInstancesTypePaginateTypeDef,
    DescribeLoadBalancersRequestPaginateTypeDef,
    DescribeLoadBalancersResponseTypeDef,
    DescribeLoadBalancerTargetGroupsRequestPaginateTypeDef,
    DescribeLoadBalancerTargetGroupsResponseTypeDef,
    DescribeNotificationConfigurationsAnswerTypeDef,
    DescribeNotificationConfigurationsTypePaginateTypeDef,
    DescribePoliciesTypePaginateTypeDef,
    DescribeScalingActivitiesTypePaginateTypeDef,
    DescribeScheduledActionsTypePaginateTypeDef,
    DescribeTagsTypePaginateTypeDef,
    DescribeWarmPoolAnswerTypeDef,
    DescribeWarmPoolTypePaginateTypeDef,
    LaunchConfigurationNamesTypePaginateTypeDef,
    LaunchConfigurationsTypeTypeDef,
    PoliciesTypeTypeDef,
    ScheduledActionsTypeTypeDef,
    TagsTypeTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAutoScalingGroupsPaginator",
    "DescribeAutoScalingInstancesPaginator",
    "DescribeLaunchConfigurationsPaginator",
    "DescribeLoadBalancerTargetGroupsPaginator",
    "DescribeLoadBalancersPaginator",
    "DescribeNotificationConfigurationsPaginator",
    "DescribePoliciesPaginator",
    "DescribeScalingActivitiesPaginator",
    "DescribeScheduledActionsPaginator",
    "DescribeTagsPaginator",
    "DescribeWarmPoolPaginator",
)

if TYPE_CHECKING:
    _DescribeAutoScalingGroupsPaginatorBase = AioPaginator[AutoScalingGroupsTypeTypeDef]
else:
    _DescribeAutoScalingGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeAutoScalingGroupsPaginator(_DescribeAutoScalingGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeAutoScalingGroups.html#AutoScaling.Paginator.DescribeAutoScalingGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeautoscalinggroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[AutoScalingGroupNamesTypePaginateTypeDef]
    ) -> AioPageIterator[AutoScalingGroupsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeAutoScalingGroups.html#AutoScaling.Paginator.DescribeAutoScalingGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeautoscalinggroupspaginator)
        """

if TYPE_CHECKING:
    _DescribeAutoScalingInstancesPaginatorBase = AioPaginator[AutoScalingInstancesTypeTypeDef]
else:
    _DescribeAutoScalingInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeAutoScalingInstancesPaginator(_DescribeAutoScalingInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeAutoScalingInstances.html#AutoScaling.Paginator.DescribeAutoScalingInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeautoscalinginstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAutoScalingInstancesTypePaginateTypeDef]
    ) -> AioPageIterator[AutoScalingInstancesTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeAutoScalingInstances.html#AutoScaling.Paginator.DescribeAutoScalingInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeautoscalinginstancespaginator)
        """

if TYPE_CHECKING:
    _DescribeLaunchConfigurationsPaginatorBase = AioPaginator[LaunchConfigurationsTypeTypeDef]
else:
    _DescribeLaunchConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeLaunchConfigurationsPaginator(_DescribeLaunchConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLaunchConfigurations.html#AutoScaling.Paginator.DescribeLaunchConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describelaunchconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[LaunchConfigurationNamesTypePaginateTypeDef]
    ) -> AioPageIterator[LaunchConfigurationsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLaunchConfigurations.html#AutoScaling.Paginator.DescribeLaunchConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describelaunchconfigurationspaginator)
        """

if TYPE_CHECKING:
    _DescribeLoadBalancerTargetGroupsPaginatorBase = AioPaginator[
        DescribeLoadBalancerTargetGroupsResponseTypeDef
    ]
else:
    _DescribeLoadBalancerTargetGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeLoadBalancerTargetGroupsPaginator(_DescribeLoadBalancerTargetGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLoadBalancerTargetGroups.html#AutoScaling.Paginator.DescribeLoadBalancerTargetGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeloadbalancertargetgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeLoadBalancerTargetGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeLoadBalancerTargetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLoadBalancerTargetGroups.html#AutoScaling.Paginator.DescribeLoadBalancerTargetGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeloadbalancertargetgroupspaginator)
        """

if TYPE_CHECKING:
    _DescribeLoadBalancersPaginatorBase = AioPaginator[DescribeLoadBalancersResponseTypeDef]
else:
    _DescribeLoadBalancersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeLoadBalancersPaginator(_DescribeLoadBalancersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLoadBalancers.html#AutoScaling.Paginator.DescribeLoadBalancers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeloadbalancerspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeLoadBalancersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeLoadBalancersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLoadBalancers.html#AutoScaling.Paginator.DescribeLoadBalancers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeloadbalancerspaginator)
        """

if TYPE_CHECKING:
    _DescribeNotificationConfigurationsPaginatorBase = AioPaginator[
        DescribeNotificationConfigurationsAnswerTypeDef
    ]
else:
    _DescribeNotificationConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeNotificationConfigurationsPaginator(_DescribeNotificationConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeNotificationConfigurations.html#AutoScaling.Paginator.DescribeNotificationConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describenotificationconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeNotificationConfigurationsTypePaginateTypeDef]
    ) -> AioPageIterator[DescribeNotificationConfigurationsAnswerTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeNotificationConfigurations.html#AutoScaling.Paginator.DescribeNotificationConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describenotificationconfigurationspaginator)
        """

if TYPE_CHECKING:
    _DescribePoliciesPaginatorBase = AioPaginator[PoliciesTypeTypeDef]
else:
    _DescribePoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribePoliciesPaginator(_DescribePoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribePolicies.html#AutoScaling.Paginator.DescribePolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describepoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribePoliciesTypePaginateTypeDef]
    ) -> AioPageIterator[PoliciesTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribePolicies.html#AutoScaling.Paginator.DescribePolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describepoliciespaginator)
        """

if TYPE_CHECKING:
    _DescribeScalingActivitiesPaginatorBase = AioPaginator[ActivitiesTypeTypeDef]
else:
    _DescribeScalingActivitiesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeScalingActivitiesPaginator(_DescribeScalingActivitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeScalingActivities.html#AutoScaling.Paginator.DescribeScalingActivities)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describescalingactivitiespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeScalingActivitiesTypePaginateTypeDef]
    ) -> AioPageIterator[ActivitiesTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeScalingActivities.html#AutoScaling.Paginator.DescribeScalingActivities.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describescalingactivitiespaginator)
        """

if TYPE_CHECKING:
    _DescribeScheduledActionsPaginatorBase = AioPaginator[ScheduledActionsTypeTypeDef]
else:
    _DescribeScheduledActionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeScheduledActionsPaginator(_DescribeScheduledActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeScheduledActions.html#AutoScaling.Paginator.DescribeScheduledActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describescheduledactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeScheduledActionsTypePaginateTypeDef]
    ) -> AioPageIterator[ScheduledActionsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeScheduledActions.html#AutoScaling.Paginator.DescribeScheduledActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describescheduledactionspaginator)
        """

if TYPE_CHECKING:
    _DescribeTagsPaginatorBase = AioPaginator[TagsTypeTypeDef]
else:
    _DescribeTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeTagsPaginator(_DescribeTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeTags.html#AutoScaling.Paginator.DescribeTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describetagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTagsTypePaginateTypeDef]
    ) -> AioPageIterator[TagsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeTags.html#AutoScaling.Paginator.DescribeTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describetagspaginator)
        """

if TYPE_CHECKING:
    _DescribeWarmPoolPaginatorBase = AioPaginator[DescribeWarmPoolAnswerTypeDef]
else:
    _DescribeWarmPoolPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeWarmPoolPaginator(_DescribeWarmPoolPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeWarmPool.html#AutoScaling.Paginator.DescribeWarmPool)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describewarmpoolpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeWarmPoolTypePaginateTypeDef]
    ) -> AioPageIterator[DescribeWarmPoolAnswerTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeWarmPool.html#AutoScaling.Paginator.DescribeWarmPool.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describewarmpoolpaginator)
        """
