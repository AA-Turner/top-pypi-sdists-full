"""
Type annotations for appintegrations service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_appintegrations.client import AppIntegrationsServiceClient
    from types_aiobotocore_appintegrations.paginator import (
        ListApplicationAssociationsPaginator,
        ListApplicationsPaginator,
        ListDataIntegrationAssociationsPaginator,
        ListDataIntegrationsPaginator,
        ListEventIntegrationAssociationsPaginator,
        ListEventIntegrationsPaginator,
    )

    session = get_session()
    with session.create_client("appintegrations") as client:
        client: AppIntegrationsServiceClient

        list_application_associations_paginator: ListApplicationAssociationsPaginator = client.get_paginator("list_application_associations")
        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_data_integration_associations_paginator: ListDataIntegrationAssociationsPaginator = client.get_paginator("list_data_integration_associations")
        list_data_integrations_paginator: ListDataIntegrationsPaginator = client.get_paginator("list_data_integrations")
        list_event_integration_associations_paginator: ListEventIntegrationAssociationsPaginator = client.get_paginator("list_event_integration_associations")
        list_event_integrations_paginator: ListEventIntegrationsPaginator = client.get_paginator("list_event_integrations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListApplicationAssociationsRequestPaginateTypeDef,
    ListApplicationAssociationsResponseTypeDef,
    ListApplicationsRequestPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListDataIntegrationAssociationsRequestPaginateTypeDef,
    ListDataIntegrationAssociationsResponseTypeDef,
    ListDataIntegrationsRequestPaginateTypeDef,
    ListDataIntegrationsResponseTypeDef,
    ListEventIntegrationAssociationsRequestPaginateTypeDef,
    ListEventIntegrationAssociationsResponseTypeDef,
    ListEventIntegrationsRequestPaginateTypeDef,
    ListEventIntegrationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListApplicationAssociationsPaginator",
    "ListApplicationsPaginator",
    "ListDataIntegrationAssociationsPaginator",
    "ListDataIntegrationsPaginator",
    "ListEventIntegrationAssociationsPaginator",
    "ListEventIntegrationsPaginator",
)

if TYPE_CHECKING:
    _ListApplicationAssociationsPaginatorBase = AioPaginator[
        ListApplicationAssociationsResponseTypeDef
    ]
else:
    _ListApplicationAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListApplicationAssociationsPaginator(_ListApplicationAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListApplicationAssociations.html#AppIntegrationsService.Paginator.ListApplicationAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/paginators/#listapplicationassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListApplicationAssociations.html#AppIntegrationsService.Paginator.ListApplicationAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/paginators/#listapplicationassociationspaginator)
        """

if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = AioPaginator[ListApplicationsResponseTypeDef]
else:
    _ListApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListApplications.html#AppIntegrationsService.Paginator.ListApplications)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/paginators/#listapplicationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListApplications.html#AppIntegrationsService.Paginator.ListApplications.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/paginators/#listapplicationspaginator)
        """

if TYPE_CHECKING:
    _ListDataIntegrationAssociationsPaginatorBase = AioPaginator[
        ListDataIntegrationAssociationsResponseTypeDef
    ]
else:
    _ListDataIntegrationAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataIntegrationAssociationsPaginator(_ListDataIntegrationAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListDataIntegrationAssociations.html#AppIntegrationsService.Paginator.ListDataIntegrationAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/paginators/#listdataintegrationassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataIntegrationAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataIntegrationAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListDataIntegrationAssociations.html#AppIntegrationsService.Paginator.ListDataIntegrationAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/paginators/#listdataintegrationassociationspaginator)
        """

if TYPE_CHECKING:
    _ListDataIntegrationsPaginatorBase = AioPaginator[ListDataIntegrationsResponseTypeDef]
else:
    _ListDataIntegrationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataIntegrationsPaginator(_ListDataIntegrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListDataIntegrations.html#AppIntegrationsService.Paginator.ListDataIntegrations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/paginators/#listdataintegrationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataIntegrationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataIntegrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListDataIntegrations.html#AppIntegrationsService.Paginator.ListDataIntegrations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/paginators/#listdataintegrationspaginator)
        """

if TYPE_CHECKING:
    _ListEventIntegrationAssociationsPaginatorBase = AioPaginator[
        ListEventIntegrationAssociationsResponseTypeDef
    ]
else:
    _ListEventIntegrationAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEventIntegrationAssociationsPaginator(_ListEventIntegrationAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListEventIntegrationAssociations.html#AppIntegrationsService.Paginator.ListEventIntegrationAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/paginators/#listeventintegrationassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventIntegrationAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventIntegrationAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListEventIntegrationAssociations.html#AppIntegrationsService.Paginator.ListEventIntegrationAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/paginators/#listeventintegrationassociationspaginator)
        """

if TYPE_CHECKING:
    _ListEventIntegrationsPaginatorBase = AioPaginator[ListEventIntegrationsResponseTypeDef]
else:
    _ListEventIntegrationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEventIntegrationsPaginator(_ListEventIntegrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListEventIntegrations.html#AppIntegrationsService.Paginator.ListEventIntegrations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/paginators/#listeventintegrationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventIntegrationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventIntegrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/paginator/ListEventIntegrations.html#AppIntegrationsService.Paginator.ListEventIntegrations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/paginators/#listeventintegrationspaginator)
        """
