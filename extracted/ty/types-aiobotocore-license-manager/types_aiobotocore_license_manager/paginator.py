"""
Type annotations for license-manager service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_license_manager.client import LicenseManagerClient
    from types_aiobotocore_license_manager.paginator import (
        ListAssociationsForLicenseConfigurationPaginator,
        ListLicenseConfigurationsPaginator,
        ListLicenseSpecificationsForResourcePaginator,
        ListResourceInventoryPaginator,
        ListUsageForLicenseConfigurationPaginator,
    )

    session = get_session()
    with session.create_client("license-manager") as client:
        client: LicenseManagerClient

        list_associations_for_license_configuration_paginator: ListAssociationsForLicenseConfigurationPaginator = client.get_paginator("list_associations_for_license_configuration")
        list_license_configurations_paginator: ListLicenseConfigurationsPaginator = client.get_paginator("list_license_configurations")
        list_license_specifications_for_resource_paginator: ListLicenseSpecificationsForResourcePaginator = client.get_paginator("list_license_specifications_for_resource")
        list_resource_inventory_paginator: ListResourceInventoryPaginator = client.get_paginator("list_resource_inventory")
        list_usage_for_license_configuration_paginator: ListUsageForLicenseConfigurationPaginator = client.get_paginator("list_usage_for_license_configuration")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAssociationsForLicenseConfigurationRequestPaginateTypeDef,
    ListAssociationsForLicenseConfigurationResponseTypeDef,
    ListLicenseConfigurationsRequestPaginateTypeDef,
    ListLicenseConfigurationsResponseTypeDef,
    ListLicenseSpecificationsForResourceRequestPaginateTypeDef,
    ListLicenseSpecificationsForResourceResponseTypeDef,
    ListResourceInventoryRequestPaginateTypeDef,
    ListResourceInventoryResponseTypeDef,
    ListUsageForLicenseConfigurationRequestPaginateTypeDef,
    ListUsageForLicenseConfigurationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAssociationsForLicenseConfigurationPaginator",
    "ListLicenseConfigurationsPaginator",
    "ListLicenseSpecificationsForResourcePaginator",
    "ListResourceInventoryPaginator",
    "ListUsageForLicenseConfigurationPaginator",
)


if TYPE_CHECKING:
    _ListAssociationsForLicenseConfigurationPaginatorBase = AioPaginator[
        ListAssociationsForLicenseConfigurationResponseTypeDef
    ]
else:
    _ListAssociationsForLicenseConfigurationPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAssociationsForLicenseConfigurationPaginator(
    _ListAssociationsForLicenseConfigurationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListAssociationsForLicenseConfiguration.html#LicenseManager.Paginator.ListAssociationsForLicenseConfiguration)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators/#listassociationsforlicenseconfigurationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociationsForLicenseConfigurationRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssociationsForLicenseConfigurationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListAssociationsForLicenseConfiguration.html#LicenseManager.Paginator.ListAssociationsForLicenseConfiguration.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators/#listassociationsforlicenseconfigurationpaginator)
        """


if TYPE_CHECKING:
    _ListLicenseConfigurationsPaginatorBase = AioPaginator[ListLicenseConfigurationsResponseTypeDef]
else:
    _ListLicenseConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLicenseConfigurationsPaginator(_ListLicenseConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListLicenseConfigurations.html#LicenseManager.Paginator.ListLicenseConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators/#listlicenseconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLicenseConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLicenseConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListLicenseConfigurations.html#LicenseManager.Paginator.ListLicenseConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators/#listlicenseconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListLicenseSpecificationsForResourcePaginatorBase = AioPaginator[
        ListLicenseSpecificationsForResourceResponseTypeDef
    ]
else:
    _ListLicenseSpecificationsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLicenseSpecificationsForResourcePaginator(
    _ListLicenseSpecificationsForResourcePaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListLicenseSpecificationsForResource.html#LicenseManager.Paginator.ListLicenseSpecificationsForResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators/#listlicensespecificationsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLicenseSpecificationsForResourceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLicenseSpecificationsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListLicenseSpecificationsForResource.html#LicenseManager.Paginator.ListLicenseSpecificationsForResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators/#listlicensespecificationsforresourcepaginator)
        """


if TYPE_CHECKING:
    _ListResourceInventoryPaginatorBase = AioPaginator[ListResourceInventoryResponseTypeDef]
else:
    _ListResourceInventoryPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourceInventoryPaginator(_ListResourceInventoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListResourceInventory.html#LicenseManager.Paginator.ListResourceInventory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators/#listresourceinventorypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceInventoryRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceInventoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListResourceInventory.html#LicenseManager.Paginator.ListResourceInventory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators/#listresourceinventorypaginator)
        """


if TYPE_CHECKING:
    _ListUsageForLicenseConfigurationPaginatorBase = AioPaginator[
        ListUsageForLicenseConfigurationResponseTypeDef
    ]
else:
    _ListUsageForLicenseConfigurationPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListUsageForLicenseConfigurationPaginator(_ListUsageForLicenseConfigurationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListUsageForLicenseConfiguration.html#LicenseManager.Paginator.ListUsageForLicenseConfiguration)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators/#listusageforlicenseconfigurationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsageForLicenseConfigurationRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUsageForLicenseConfigurationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/paginator/ListUsageForLicenseConfiguration.html#LicenseManager.Paginator.ListUsageForLicenseConfiguration.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/paginators/#listusageforlicenseconfigurationpaginator)
        """
