"""
Type annotations for backup-gateway service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_backup_gateway.client import BackupGatewayClient
    from types_aiobotocore_backup_gateway.paginator import (
        ListGatewaysPaginator,
        ListHypervisorsPaginator,
        ListVirtualMachinesPaginator,
    )

    session = get_session()
    with session.create_client("backup-gateway") as client:
        client: BackupGatewayClient

        list_gateways_paginator: ListGatewaysPaginator = client.get_paginator("list_gateways")
        list_hypervisors_paginator: ListHypervisorsPaginator = client.get_paginator("list_hypervisors")
        list_virtual_machines_paginator: ListVirtualMachinesPaginator = client.get_paginator("list_virtual_machines")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListGatewaysInputPaginateTypeDef,
    ListGatewaysOutputTypeDef,
    ListHypervisorsInputPaginateTypeDef,
    ListHypervisorsOutputTypeDef,
    ListVirtualMachinesInputPaginateTypeDef,
    ListVirtualMachinesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListGatewaysPaginator", "ListHypervisorsPaginator", "ListVirtualMachinesPaginator")


if TYPE_CHECKING:
    _ListGatewaysPaginatorBase = AioPaginator[ListGatewaysOutputTypeDef]
else:
    _ListGatewaysPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGatewaysPaginator(_ListGatewaysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListGateways.html#BackupGateway.Paginator.ListGateways)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/paginators/#listgatewayspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGatewaysInputPaginateTypeDef]
    ) -> AioPageIterator[ListGatewaysOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListGateways.html#BackupGateway.Paginator.ListGateways.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/paginators/#listgatewayspaginator)
        """


if TYPE_CHECKING:
    _ListHypervisorsPaginatorBase = AioPaginator[ListHypervisorsOutputTypeDef]
else:
    _ListHypervisorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListHypervisorsPaginator(_ListHypervisorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListHypervisors.html#BackupGateway.Paginator.ListHypervisors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/paginators/#listhypervisorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHypervisorsInputPaginateTypeDef]
    ) -> AioPageIterator[ListHypervisorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListHypervisors.html#BackupGateway.Paginator.ListHypervisors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/paginators/#listhypervisorspaginator)
        """


if TYPE_CHECKING:
    _ListVirtualMachinesPaginatorBase = AioPaginator[ListVirtualMachinesOutputTypeDef]
else:
    _ListVirtualMachinesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListVirtualMachinesPaginator(_ListVirtualMachinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListVirtualMachines.html#BackupGateway.Paginator.ListVirtualMachines)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/paginators/#listvirtualmachinespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVirtualMachinesInputPaginateTypeDef]
    ) -> AioPageIterator[ListVirtualMachinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListVirtualMachines.html#BackupGateway.Paginator.ListVirtualMachines.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/paginators/#listvirtualmachinespaginator)
        """
