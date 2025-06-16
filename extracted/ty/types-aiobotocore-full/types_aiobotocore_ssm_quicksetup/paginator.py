"""
Type annotations for ssm-quicksetup service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_quicksetup/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ssm_quicksetup.client import SystemsManagerQuickSetupClient
    from types_aiobotocore_ssm_quicksetup.paginator import (
        ListConfigurationManagersPaginator,
        ListConfigurationsPaginator,
    )

    session = get_session()
    with session.create_client("ssm-quicksetup") as client:
        client: SystemsManagerQuickSetupClient

        list_configuration_managers_paginator: ListConfigurationManagersPaginator = client.get_paginator("list_configuration_managers")
        list_configurations_paginator: ListConfigurationsPaginator = client.get_paginator("list_configurations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListConfigurationManagersInputPaginateTypeDef,
    ListConfigurationManagersOutputTypeDef,
    ListConfigurationsInputPaginateTypeDef,
    ListConfigurationsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListConfigurationManagersPaginator", "ListConfigurationsPaginator")


if TYPE_CHECKING:
    _ListConfigurationManagersPaginatorBase = AioPaginator[ListConfigurationManagersOutputTypeDef]
else:
    _ListConfigurationManagersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConfigurationManagersPaginator(_ListConfigurationManagersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup/paginator/ListConfigurationManagers.html#SystemsManagerQuickSetup.Paginator.ListConfigurationManagers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_quicksetup/paginators/#listconfigurationmanagerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfigurationManagersInputPaginateTypeDef]
    ) -> AioPageIterator[ListConfigurationManagersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup/paginator/ListConfigurationManagers.html#SystemsManagerQuickSetup.Paginator.ListConfigurationManagers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_quicksetup/paginators/#listconfigurationmanagerspaginator)
        """


if TYPE_CHECKING:
    _ListConfigurationsPaginatorBase = AioPaginator[ListConfigurationsOutputTypeDef]
else:
    _ListConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConfigurationsPaginator(_ListConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup/paginator/ListConfigurations.html#SystemsManagerQuickSetup.Paginator.ListConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_quicksetup/paginators/#listconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfigurationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup/paginator/ListConfigurations.html#SystemsManagerQuickSetup.Paginator.ListConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_quicksetup/paginators/#listconfigurationspaginator)
        """
