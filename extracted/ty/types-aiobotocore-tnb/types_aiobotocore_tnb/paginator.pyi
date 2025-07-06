"""
Type annotations for tnb service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_tnb.client import TelcoNetworkBuilderClient
    from types_aiobotocore_tnb.paginator import (
        ListSolFunctionInstancesPaginator,
        ListSolFunctionPackagesPaginator,
        ListSolNetworkInstancesPaginator,
        ListSolNetworkOperationsPaginator,
        ListSolNetworkPackagesPaginator,
    )

    session = get_session()
    with session.create_client("tnb") as client:
        client: TelcoNetworkBuilderClient

        list_sol_function_instances_paginator: ListSolFunctionInstancesPaginator = client.get_paginator("list_sol_function_instances")
        list_sol_function_packages_paginator: ListSolFunctionPackagesPaginator = client.get_paginator("list_sol_function_packages")
        list_sol_network_instances_paginator: ListSolNetworkInstancesPaginator = client.get_paginator("list_sol_network_instances")
        list_sol_network_operations_paginator: ListSolNetworkOperationsPaginator = client.get_paginator("list_sol_network_operations")
        list_sol_network_packages_paginator: ListSolNetworkPackagesPaginator = client.get_paginator("list_sol_network_packages")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListSolFunctionInstancesInputPaginateTypeDef,
    ListSolFunctionInstancesOutputTypeDef,
    ListSolFunctionPackagesInputPaginateTypeDef,
    ListSolFunctionPackagesOutputTypeDef,
    ListSolNetworkInstancesInputPaginateTypeDef,
    ListSolNetworkInstancesOutputTypeDef,
    ListSolNetworkOperationsInputPaginateTypeDef,
    ListSolNetworkOperationsOutputTypeDef,
    ListSolNetworkPackagesInputPaginateTypeDef,
    ListSolNetworkPackagesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListSolFunctionInstancesPaginator",
    "ListSolFunctionPackagesPaginator",
    "ListSolNetworkInstancesPaginator",
    "ListSolNetworkOperationsPaginator",
    "ListSolNetworkPackagesPaginator",
)

if TYPE_CHECKING:
    _ListSolFunctionInstancesPaginatorBase = AioPaginator[ListSolFunctionInstancesOutputTypeDef]
else:
    _ListSolFunctionInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSolFunctionInstancesPaginator(_ListSolFunctionInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolFunctionInstances.html#TelcoNetworkBuilder.Paginator.ListSolFunctionInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolfunctioninstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSolFunctionInstancesInputPaginateTypeDef]
    ) -> AioPageIterator[ListSolFunctionInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolFunctionInstances.html#TelcoNetworkBuilder.Paginator.ListSolFunctionInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolfunctioninstancespaginator)
        """

if TYPE_CHECKING:
    _ListSolFunctionPackagesPaginatorBase = AioPaginator[ListSolFunctionPackagesOutputTypeDef]
else:
    _ListSolFunctionPackagesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSolFunctionPackagesPaginator(_ListSolFunctionPackagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolFunctionPackages.html#TelcoNetworkBuilder.Paginator.ListSolFunctionPackages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolfunctionpackagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSolFunctionPackagesInputPaginateTypeDef]
    ) -> AioPageIterator[ListSolFunctionPackagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolFunctionPackages.html#TelcoNetworkBuilder.Paginator.ListSolFunctionPackages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolfunctionpackagespaginator)
        """

if TYPE_CHECKING:
    _ListSolNetworkInstancesPaginatorBase = AioPaginator[ListSolNetworkInstancesOutputTypeDef]
else:
    _ListSolNetworkInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSolNetworkInstancesPaginator(_ListSolNetworkInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkInstances.html#TelcoNetworkBuilder.Paginator.ListSolNetworkInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolnetworkinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSolNetworkInstancesInputPaginateTypeDef]
    ) -> AioPageIterator[ListSolNetworkInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkInstances.html#TelcoNetworkBuilder.Paginator.ListSolNetworkInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolnetworkinstancespaginator)
        """

if TYPE_CHECKING:
    _ListSolNetworkOperationsPaginatorBase = AioPaginator[ListSolNetworkOperationsOutputTypeDef]
else:
    _ListSolNetworkOperationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSolNetworkOperationsPaginator(_ListSolNetworkOperationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkOperations.html#TelcoNetworkBuilder.Paginator.ListSolNetworkOperations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolnetworkoperationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSolNetworkOperationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSolNetworkOperationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkOperations.html#TelcoNetworkBuilder.Paginator.ListSolNetworkOperations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolnetworkoperationspaginator)
        """

if TYPE_CHECKING:
    _ListSolNetworkPackagesPaginatorBase = AioPaginator[ListSolNetworkPackagesOutputTypeDef]
else:
    _ListSolNetworkPackagesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSolNetworkPackagesPaginator(_ListSolNetworkPackagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkPackages.html#TelcoNetworkBuilder.Paginator.ListSolNetworkPackages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolnetworkpackagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSolNetworkPackagesInputPaginateTypeDef]
    ) -> AioPageIterator[ListSolNetworkPackagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkPackages.html#TelcoNetworkBuilder.Paginator.ListSolNetworkPackages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolnetworkpackagespaginator)
        """
