"""
Type annotations for workspaces-thin-client service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_thin_client/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_workspaces_thin_client.client import WorkSpacesThinClientClient
    from types_aiobotocore_workspaces_thin_client.paginator import (
        ListDevicesPaginator,
        ListEnvironmentsPaginator,
        ListSoftwareSetsPaginator,
    )

    session = get_session()
    with session.create_client("workspaces-thin-client") as client:
        client: WorkSpacesThinClientClient

        list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
        list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
        list_software_sets_paginator: ListSoftwareSetsPaginator = client.get_paginator("list_software_sets")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDevicesRequestPaginateTypeDef,
    ListDevicesResponseTypeDef,
    ListEnvironmentsRequestPaginateTypeDef,
    ListEnvironmentsResponseTypeDef,
    ListSoftwareSetsRequestPaginateTypeDef,
    ListSoftwareSetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListDevicesPaginator", "ListEnvironmentsPaginator", "ListSoftwareSetsPaginator")

if TYPE_CHECKING:
    _ListDevicesPaginatorBase = AioPaginator[ListDevicesResponseTypeDef]
else:
    _ListDevicesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDevicesPaginator(_ListDevicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/paginator/ListDevices.html#WorkSpacesThinClient.Paginator.ListDevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_thin_client/paginators/#listdevicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDevicesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/paginator/ListDevices.html#WorkSpacesThinClient.Paginator.ListDevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_thin_client/paginators/#listdevicespaginator)
        """

if TYPE_CHECKING:
    _ListEnvironmentsPaginatorBase = AioPaginator[ListEnvironmentsResponseTypeDef]
else:
    _ListEnvironmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEnvironmentsPaginator(_ListEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/paginator/ListEnvironments.html#WorkSpacesThinClient.Paginator.ListEnvironments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_thin_client/paginators/#listenvironmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/paginator/ListEnvironments.html#WorkSpacesThinClient.Paginator.ListEnvironments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_thin_client/paginators/#listenvironmentspaginator)
        """

if TYPE_CHECKING:
    _ListSoftwareSetsPaginatorBase = AioPaginator[ListSoftwareSetsResponseTypeDef]
else:
    _ListSoftwareSetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSoftwareSetsPaginator(_ListSoftwareSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/paginator/ListSoftwareSets.html#WorkSpacesThinClient.Paginator.ListSoftwareSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_thin_client/paginators/#listsoftwaresetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSoftwareSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSoftwareSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/paginator/ListSoftwareSets.html#WorkSpacesThinClient.Paginator.ListSoftwareSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_thin_client/paginators/#listsoftwaresetspaginator)
        """
