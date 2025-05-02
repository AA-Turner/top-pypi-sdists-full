"""
Type annotations for snow-device-management service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_snow_device_management.client import SnowDeviceManagementClient
    from types_aiobotocore_snow_device_management.paginator import (
        ListDeviceResourcesPaginator,
        ListDevicesPaginator,
        ListExecutionsPaginator,
        ListTasksPaginator,
    )

    session = get_session()
    with session.create_client("snow-device-management") as client:
        client: SnowDeviceManagementClient

        list_device_resources_paginator: ListDeviceResourcesPaginator = client.get_paginator("list_device_resources")
        list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
        list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
        list_tasks_paginator: ListTasksPaginator = client.get_paginator("list_tasks")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDeviceResourcesInputPaginateTypeDef,
    ListDeviceResourcesOutputTypeDef,
    ListDevicesInputPaginateTypeDef,
    ListDevicesOutputTypeDef,
    ListExecutionsInputPaginateTypeDef,
    ListExecutionsOutputTypeDef,
    ListTasksInputPaginateTypeDef,
    ListTasksOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDeviceResourcesPaginator",
    "ListDevicesPaginator",
    "ListExecutionsPaginator",
    "ListTasksPaginator",
)

if TYPE_CHECKING:
    _ListDeviceResourcesPaginatorBase = AioPaginator[ListDeviceResourcesOutputTypeDef]
else:
    _ListDeviceResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDeviceResourcesPaginator(_ListDeviceResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListDeviceResources.html#SnowDeviceManagement.Paginator.ListDeviceResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/paginators/#listdeviceresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeviceResourcesInputPaginateTypeDef]
    ) -> AioPageIterator[ListDeviceResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListDeviceResources.html#SnowDeviceManagement.Paginator.ListDeviceResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/paginators/#listdeviceresourcespaginator)
        """

if TYPE_CHECKING:
    _ListDevicesPaginatorBase = AioPaginator[ListDevicesOutputTypeDef]
else:
    _ListDevicesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDevicesPaginator(_ListDevicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListDevices.html#SnowDeviceManagement.Paginator.ListDevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/paginators/#listdevicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDevicesInputPaginateTypeDef]
    ) -> AioPageIterator[ListDevicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListDevices.html#SnowDeviceManagement.Paginator.ListDevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/paginators/#listdevicespaginator)
        """

if TYPE_CHECKING:
    _ListExecutionsPaginatorBase = AioPaginator[ListExecutionsOutputTypeDef]
else:
    _ListExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListExecutionsPaginator(_ListExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListExecutions.html#SnowDeviceManagement.Paginator.ListExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/paginators/#listexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExecutionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListExecutions.html#SnowDeviceManagement.Paginator.ListExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/paginators/#listexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListTasksPaginatorBase = AioPaginator[ListTasksOutputTypeDef]
else:
    _ListTasksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTasksPaginator(_ListTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListTasks.html#SnowDeviceManagement.Paginator.ListTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/paginators/#listtaskspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTasksInputPaginateTypeDef]
    ) -> AioPageIterator[ListTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/paginator/ListTasks.html#SnowDeviceManagement.Paginator.ListTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/paginators/#listtaskspaginator)
        """
