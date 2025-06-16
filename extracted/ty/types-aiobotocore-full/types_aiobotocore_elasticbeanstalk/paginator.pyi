"""
Type annotations for elasticbeanstalk service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elasticbeanstalk.client import ElasticBeanstalkClient
    from types_aiobotocore_elasticbeanstalk.paginator import (
        DescribeApplicationVersionsPaginator,
        DescribeEnvironmentManagedActionHistoryPaginator,
        DescribeEnvironmentsPaginator,
        DescribeEventsPaginator,
        ListPlatformVersionsPaginator,
    )

    session = get_session()
    with session.create_client("elasticbeanstalk") as client:
        client: ElasticBeanstalkClient

        describe_application_versions_paginator: DescribeApplicationVersionsPaginator = client.get_paginator("describe_application_versions")
        describe_environment_managed_action_history_paginator: DescribeEnvironmentManagedActionHistoryPaginator = client.get_paginator("describe_environment_managed_action_history")
        describe_environments_paginator: DescribeEnvironmentsPaginator = client.get_paginator("describe_environments")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        list_platform_versions_paginator: ListPlatformVersionsPaginator = client.get_paginator("list_platform_versions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ApplicationVersionDescriptionsMessageTypeDef,
    DescribeApplicationVersionsMessagePaginateTypeDef,
    DescribeEnvironmentManagedActionHistoryRequestPaginateTypeDef,
    DescribeEnvironmentManagedActionHistoryResultTypeDef,
    DescribeEnvironmentsMessagePaginateTypeDef,
    DescribeEventsMessagePaginateTypeDef,
    EnvironmentDescriptionsMessageTypeDef,
    EventDescriptionsMessageTypeDef,
    ListPlatformVersionsRequestPaginateTypeDef,
    ListPlatformVersionsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeApplicationVersionsPaginator",
    "DescribeEnvironmentManagedActionHistoryPaginator",
    "DescribeEnvironmentsPaginator",
    "DescribeEventsPaginator",
    "ListPlatformVersionsPaginator",
)

if TYPE_CHECKING:
    _DescribeApplicationVersionsPaginatorBase = AioPaginator[
        ApplicationVersionDescriptionsMessageTypeDef
    ]
else:
    _DescribeApplicationVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeApplicationVersionsPaginator(_DescribeApplicationVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeApplicationVersions.html#ElasticBeanstalk.Paginator.DescribeApplicationVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/paginators/#describeapplicationversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeApplicationVersionsMessagePaginateTypeDef]
    ) -> AioPageIterator[ApplicationVersionDescriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeApplicationVersions.html#ElasticBeanstalk.Paginator.DescribeApplicationVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/paginators/#describeapplicationversionspaginator)
        """

if TYPE_CHECKING:
    _DescribeEnvironmentManagedActionHistoryPaginatorBase = AioPaginator[
        DescribeEnvironmentManagedActionHistoryResultTypeDef
    ]
else:
    _DescribeEnvironmentManagedActionHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeEnvironmentManagedActionHistoryPaginator(
    _DescribeEnvironmentManagedActionHistoryPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeEnvironmentManagedActionHistory.html#ElasticBeanstalk.Paginator.DescribeEnvironmentManagedActionHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/paginators/#describeenvironmentmanagedactionhistorypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEnvironmentManagedActionHistoryRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeEnvironmentManagedActionHistoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeEnvironmentManagedActionHistory.html#ElasticBeanstalk.Paginator.DescribeEnvironmentManagedActionHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/paginators/#describeenvironmentmanagedactionhistorypaginator)
        """

if TYPE_CHECKING:
    _DescribeEnvironmentsPaginatorBase = AioPaginator[EnvironmentDescriptionsMessageTypeDef]
else:
    _DescribeEnvironmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeEnvironmentsPaginator(_DescribeEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeEnvironments.html#ElasticBeanstalk.Paginator.DescribeEnvironments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/paginators/#describeenvironmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEnvironmentsMessagePaginateTypeDef]
    ) -> AioPageIterator[EnvironmentDescriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeEnvironments.html#ElasticBeanstalk.Paginator.DescribeEnvironments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/paginators/#describeenvironmentspaginator)
        """

if TYPE_CHECKING:
    _DescribeEventsPaginatorBase = AioPaginator[EventDescriptionsMessageTypeDef]
else:
    _DescribeEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeEventsPaginator(_DescribeEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeEvents.html#ElasticBeanstalk.Paginator.DescribeEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/paginators/#describeeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventsMessagePaginateTypeDef]
    ) -> AioPageIterator[EventDescriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeEvents.html#ElasticBeanstalk.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/paginators/#describeeventspaginator)
        """

if TYPE_CHECKING:
    _ListPlatformVersionsPaginatorBase = AioPaginator[ListPlatformVersionsResultTypeDef]
else:
    _ListPlatformVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPlatformVersionsPaginator(_ListPlatformVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/ListPlatformVersions.html#ElasticBeanstalk.Paginator.ListPlatformVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/paginators/#listplatformversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPlatformVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPlatformVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/ListPlatformVersions.html#ElasticBeanstalk.Paginator.ListPlatformVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/paginators/#listplatformversionspaginator)
        """
