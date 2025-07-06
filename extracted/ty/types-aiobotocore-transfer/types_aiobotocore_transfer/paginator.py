"""
Type annotations for transfer service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_transfer.client import TransferClient
    from types_aiobotocore_transfer.paginator import (
        ListAccessesPaginator,
        ListAgreementsPaginator,
        ListCertificatesPaginator,
        ListConnectorsPaginator,
        ListExecutionsPaginator,
        ListFileTransferResultsPaginator,
        ListProfilesPaginator,
        ListSecurityPoliciesPaginator,
        ListServersPaginator,
        ListTagsForResourcePaginator,
        ListUsersPaginator,
        ListWebAppsPaginator,
        ListWorkflowsPaginator,
    )

    session = get_session()
    with session.create_client("transfer") as client:
        client: TransferClient

        list_accesses_paginator: ListAccessesPaginator = client.get_paginator("list_accesses")
        list_agreements_paginator: ListAgreementsPaginator = client.get_paginator("list_agreements")
        list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
        list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
        list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
        list_file_transfer_results_paginator: ListFileTransferResultsPaginator = client.get_paginator("list_file_transfer_results")
        list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
        list_security_policies_paginator: ListSecurityPoliciesPaginator = client.get_paginator("list_security_policies")
        list_servers_paginator: ListServersPaginator = client.get_paginator("list_servers")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
        list_web_apps_paginator: ListWebAppsPaginator = client.get_paginator("list_web_apps")
        list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAccessesRequestPaginateTypeDef,
    ListAccessesResponseTypeDef,
    ListAgreementsRequestPaginateTypeDef,
    ListAgreementsResponseTypeDef,
    ListCertificatesRequestPaginateTypeDef,
    ListCertificatesResponseTypeDef,
    ListConnectorsRequestPaginateTypeDef,
    ListConnectorsResponseTypeDef,
    ListExecutionsRequestPaginateTypeDef,
    ListExecutionsResponseTypeDef,
    ListFileTransferResultsRequestPaginateTypeDef,
    ListFileTransferResultsResponseTypeDef,
    ListProfilesRequestPaginateTypeDef,
    ListProfilesResponseTypeDef,
    ListSecurityPoliciesRequestPaginateTypeDef,
    ListSecurityPoliciesResponseTypeDef,
    ListServersRequestPaginateTypeDef,
    ListServersResponseTypeDef,
    ListTagsForResourceRequestPaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUsersRequestPaginateTypeDef,
    ListUsersResponseTypeDef,
    ListWebAppsRequestPaginateTypeDef,
    ListWebAppsResponseTypeDef,
    ListWorkflowsRequestPaginateTypeDef,
    ListWorkflowsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAccessesPaginator",
    "ListAgreementsPaginator",
    "ListCertificatesPaginator",
    "ListConnectorsPaginator",
    "ListExecutionsPaginator",
    "ListFileTransferResultsPaginator",
    "ListProfilesPaginator",
    "ListSecurityPoliciesPaginator",
    "ListServersPaginator",
    "ListTagsForResourcePaginator",
    "ListUsersPaginator",
    "ListWebAppsPaginator",
    "ListWorkflowsPaginator",
)


if TYPE_CHECKING:
    _ListAccessesPaginatorBase = AioPaginator[ListAccessesResponseTypeDef]
else:
    _ListAccessesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAccessesPaginator(_ListAccessesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListAccesses.html#Transfer.Paginator.ListAccesses)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listaccessespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccessesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAccessesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListAccesses.html#Transfer.Paginator.ListAccesses.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listaccessespaginator)
        """


if TYPE_CHECKING:
    _ListAgreementsPaginatorBase = AioPaginator[ListAgreementsResponseTypeDef]
else:
    _ListAgreementsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAgreementsPaginator(_ListAgreementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListAgreements.html#Transfer.Paginator.ListAgreements)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listagreementspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgreementsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAgreementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListAgreements.html#Transfer.Paginator.ListAgreements.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listagreementspaginator)
        """


if TYPE_CHECKING:
    _ListCertificatesPaginatorBase = AioPaginator[ListCertificatesResponseTypeDef]
else:
    _ListCertificatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCertificatesPaginator(_ListCertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListCertificates.html#Transfer.Paginator.ListCertificates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listcertificatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCertificatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListCertificates.html#Transfer.Paginator.ListCertificates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listcertificatespaginator)
        """


if TYPE_CHECKING:
    _ListConnectorsPaginatorBase = AioPaginator[ListConnectorsResponseTypeDef]
else:
    _ListConnectorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConnectorsPaginator(_ListConnectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListConnectors.html#Transfer.Paginator.ListConnectors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listconnectorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListConnectors.html#Transfer.Paginator.ListConnectors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listconnectorspaginator)
        """


if TYPE_CHECKING:
    _ListExecutionsPaginatorBase = AioPaginator[ListExecutionsResponseTypeDef]
else:
    _ListExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListExecutionsPaginator(_ListExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListExecutions.html#Transfer.Paginator.ListExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListExecutions.html#Transfer.Paginator.ListExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListFileTransferResultsPaginatorBase = AioPaginator[ListFileTransferResultsResponseTypeDef]
else:
    _ListFileTransferResultsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFileTransferResultsPaginator(_ListFileTransferResultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListFileTransferResults.html#Transfer.Paginator.ListFileTransferResults)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listfiletransferresultspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFileTransferResultsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFileTransferResultsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListFileTransferResults.html#Transfer.Paginator.ListFileTransferResults.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listfiletransferresultspaginator)
        """


if TYPE_CHECKING:
    _ListProfilesPaginatorBase = AioPaginator[ListProfilesResponseTypeDef]
else:
    _ListProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListProfilesPaginator(_ListProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListProfiles.html#Transfer.Paginator.ListProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listprofilespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListProfiles.html#Transfer.Paginator.ListProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listprofilespaginator)
        """


if TYPE_CHECKING:
    _ListSecurityPoliciesPaginatorBase = AioPaginator[ListSecurityPoliciesResponseTypeDef]
else:
    _ListSecurityPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSecurityPoliciesPaginator(_ListSecurityPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListSecurityPolicies.html#Transfer.Paginator.ListSecurityPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listsecuritypoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSecurityPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListSecurityPolicies.html#Transfer.Paginator.ListSecurityPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listsecuritypoliciespaginator)
        """


if TYPE_CHECKING:
    _ListServersPaginatorBase = AioPaginator[ListServersResponseTypeDef]
else:
    _ListServersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServersPaginator(_ListServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListServers.html#Transfer.Paginator.ListServers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listserverspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListServers.html#Transfer.Paginator.ListServers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listserverspaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceResponseTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListTagsForResource.html#Transfer.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListTagsForResource.html#Transfer.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listtagsforresourcepaginator)
        """


if TYPE_CHECKING:
    _ListUsersPaginatorBase = AioPaginator[ListUsersResponseTypeDef]
else:
    _ListUsersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListUsersPaginator(_ListUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListUsers.html#Transfer.Paginator.ListUsers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listuserspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListUsers.html#Transfer.Paginator.ListUsers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listuserspaginator)
        """


if TYPE_CHECKING:
    _ListWebAppsPaginatorBase = AioPaginator[ListWebAppsResponseTypeDef]
else:
    _ListWebAppsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWebAppsPaginator(_ListWebAppsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListWebApps.html#Transfer.Paginator.ListWebApps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listwebappspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWebAppsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWebAppsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListWebApps.html#Transfer.Paginator.ListWebApps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listwebappspaginator)
        """


if TYPE_CHECKING:
    _ListWorkflowsPaginatorBase = AioPaginator[ListWorkflowsResponseTypeDef]
else:
    _ListWorkflowsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkflowsPaginator(_ListWorkflowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListWorkflows.html#Transfer.Paginator.ListWorkflows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listworkflowspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/paginator/ListWorkflows.html#Transfer.Paginator.ListWorkflows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/paginators/#listworkflowspaginator)
        """
