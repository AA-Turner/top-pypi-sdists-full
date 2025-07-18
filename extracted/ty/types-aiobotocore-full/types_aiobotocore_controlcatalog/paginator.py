"""
Type annotations for controlcatalog service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_controlcatalog.client import ControlCatalogClient
    from types_aiobotocore_controlcatalog.paginator import (
        ListCommonControlsPaginator,
        ListControlMappingsPaginator,
        ListControlsPaginator,
        ListDomainsPaginator,
        ListObjectivesPaginator,
    )

    session = get_session()
    with session.create_client("controlcatalog") as client:
        client: ControlCatalogClient

        list_common_controls_paginator: ListCommonControlsPaginator = client.get_paginator("list_common_controls")
        list_control_mappings_paginator: ListControlMappingsPaginator = client.get_paginator("list_control_mappings")
        list_controls_paginator: ListControlsPaginator = client.get_paginator("list_controls")
        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_objectives_paginator: ListObjectivesPaginator = client.get_paginator("list_objectives")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListCommonControlsRequestPaginateTypeDef,
    ListCommonControlsResponseTypeDef,
    ListControlMappingsRequestPaginateTypeDef,
    ListControlMappingsResponseTypeDef,
    ListControlsRequestPaginateTypeDef,
    ListControlsResponseTypeDef,
    ListDomainsRequestPaginateTypeDef,
    ListDomainsResponseTypeDef,
    ListObjectivesRequestPaginateTypeDef,
    ListObjectivesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListCommonControlsPaginator",
    "ListControlMappingsPaginator",
    "ListControlsPaginator",
    "ListDomainsPaginator",
    "ListObjectivesPaginator",
)


if TYPE_CHECKING:
    _ListCommonControlsPaginatorBase = AioPaginator[ListCommonControlsResponseTypeDef]
else:
    _ListCommonControlsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCommonControlsPaginator(_ListCommonControlsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListCommonControls.html#ControlCatalog.Paginator.ListCommonControls)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listcommoncontrolspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCommonControlsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCommonControlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListCommonControls.html#ControlCatalog.Paginator.ListCommonControls.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listcommoncontrolspaginator)
        """


if TYPE_CHECKING:
    _ListControlMappingsPaginatorBase = AioPaginator[ListControlMappingsResponseTypeDef]
else:
    _ListControlMappingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListControlMappingsPaginator(_ListControlMappingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListControlMappings.html#ControlCatalog.Paginator.ListControlMappings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listcontrolmappingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListControlMappingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListControlMappingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListControlMappings.html#ControlCatalog.Paginator.ListControlMappings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listcontrolmappingspaginator)
        """


if TYPE_CHECKING:
    _ListControlsPaginatorBase = AioPaginator[ListControlsResponseTypeDef]
else:
    _ListControlsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListControlsPaginator(_ListControlsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListControls.html#ControlCatalog.Paginator.ListControls)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listcontrolspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListControlsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListControlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListControls.html#ControlCatalog.Paginator.ListControls.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listcontrolspaginator)
        """


if TYPE_CHECKING:
    _ListDomainsPaginatorBase = AioPaginator[ListDomainsResponseTypeDef]
else:
    _ListDomainsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDomainsPaginator(_ListDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListDomains.html#ControlCatalog.Paginator.ListDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listdomainspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListDomains.html#ControlCatalog.Paginator.ListDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listdomainspaginator)
        """


if TYPE_CHECKING:
    _ListObjectivesPaginatorBase = AioPaginator[ListObjectivesResponseTypeDef]
else:
    _ListObjectivesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListObjectivesPaginator(_ListObjectivesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListObjectives.html#ControlCatalog.Paginator.ListObjectives)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listobjectivespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListObjectivesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListObjectivesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/paginator/ListObjectives.html#ControlCatalog.Paginator.ListObjectives.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listobjectivespaginator)
        """
