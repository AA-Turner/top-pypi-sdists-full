"""
Type annotations for cleanrooms service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cleanrooms.client import CleanRoomsServiceClient
    from types_aiobotocore_cleanrooms.paginator import (
        ListAnalysisTemplatesPaginator,
        ListCollaborationAnalysisTemplatesPaginator,
        ListCollaborationConfiguredAudienceModelAssociationsPaginator,
        ListCollaborationIdNamespaceAssociationsPaginator,
        ListCollaborationPrivacyBudgetTemplatesPaginator,
        ListCollaborationPrivacyBudgetsPaginator,
        ListCollaborationsPaginator,
        ListConfiguredAudienceModelAssociationsPaginator,
        ListConfiguredTableAssociationsPaginator,
        ListConfiguredTablesPaginator,
        ListIdMappingTablesPaginator,
        ListIdNamespaceAssociationsPaginator,
        ListMembersPaginator,
        ListMembershipsPaginator,
        ListPrivacyBudgetTemplatesPaginator,
        ListPrivacyBudgetsPaginator,
        ListProtectedJobsPaginator,
        ListProtectedQueriesPaginator,
        ListSchemasPaginator,
    )

    session = get_session()
    with session.create_client("cleanrooms") as client:
        client: CleanRoomsServiceClient

        list_analysis_templates_paginator: ListAnalysisTemplatesPaginator = client.get_paginator("list_analysis_templates")
        list_collaboration_analysis_templates_paginator: ListCollaborationAnalysisTemplatesPaginator = client.get_paginator("list_collaboration_analysis_templates")
        list_collaboration_configured_audience_model_associations_paginator: ListCollaborationConfiguredAudienceModelAssociationsPaginator = client.get_paginator("list_collaboration_configured_audience_model_associations")
        list_collaboration_id_namespace_associations_paginator: ListCollaborationIdNamespaceAssociationsPaginator = client.get_paginator("list_collaboration_id_namespace_associations")
        list_collaboration_privacy_budget_templates_paginator: ListCollaborationPrivacyBudgetTemplatesPaginator = client.get_paginator("list_collaboration_privacy_budget_templates")
        list_collaboration_privacy_budgets_paginator: ListCollaborationPrivacyBudgetsPaginator = client.get_paginator("list_collaboration_privacy_budgets")
        list_collaborations_paginator: ListCollaborationsPaginator = client.get_paginator("list_collaborations")
        list_configured_audience_model_associations_paginator: ListConfiguredAudienceModelAssociationsPaginator = client.get_paginator("list_configured_audience_model_associations")
        list_configured_table_associations_paginator: ListConfiguredTableAssociationsPaginator = client.get_paginator("list_configured_table_associations")
        list_configured_tables_paginator: ListConfiguredTablesPaginator = client.get_paginator("list_configured_tables")
        list_id_mapping_tables_paginator: ListIdMappingTablesPaginator = client.get_paginator("list_id_mapping_tables")
        list_id_namespace_associations_paginator: ListIdNamespaceAssociationsPaginator = client.get_paginator("list_id_namespace_associations")
        list_members_paginator: ListMembersPaginator = client.get_paginator("list_members")
        list_memberships_paginator: ListMembershipsPaginator = client.get_paginator("list_memberships")
        list_privacy_budget_templates_paginator: ListPrivacyBudgetTemplatesPaginator = client.get_paginator("list_privacy_budget_templates")
        list_privacy_budgets_paginator: ListPrivacyBudgetsPaginator = client.get_paginator("list_privacy_budgets")
        list_protected_jobs_paginator: ListProtectedJobsPaginator = client.get_paginator("list_protected_jobs")
        list_protected_queries_paginator: ListProtectedQueriesPaginator = client.get_paginator("list_protected_queries")
        list_schemas_paginator: ListSchemasPaginator = client.get_paginator("list_schemas")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAnalysisTemplatesInputPaginateTypeDef,
    ListAnalysisTemplatesOutputTypeDef,
    ListCollaborationAnalysisTemplatesInputPaginateTypeDef,
    ListCollaborationAnalysisTemplatesOutputTypeDef,
    ListCollaborationConfiguredAudienceModelAssociationsInputPaginateTypeDef,
    ListCollaborationConfiguredAudienceModelAssociationsOutputTypeDef,
    ListCollaborationIdNamespaceAssociationsInputPaginateTypeDef,
    ListCollaborationIdNamespaceAssociationsOutputTypeDef,
    ListCollaborationPrivacyBudgetsInputPaginateTypeDef,
    ListCollaborationPrivacyBudgetsOutputTypeDef,
    ListCollaborationPrivacyBudgetTemplatesInputPaginateTypeDef,
    ListCollaborationPrivacyBudgetTemplatesOutputTypeDef,
    ListCollaborationsInputPaginateTypeDef,
    ListCollaborationsOutputTypeDef,
    ListConfiguredAudienceModelAssociationsInputPaginateTypeDef,
    ListConfiguredAudienceModelAssociationsOutputTypeDef,
    ListConfiguredTableAssociationsInputPaginateTypeDef,
    ListConfiguredTableAssociationsOutputTypeDef,
    ListConfiguredTablesInputPaginateTypeDef,
    ListConfiguredTablesOutputTypeDef,
    ListIdMappingTablesInputPaginateTypeDef,
    ListIdMappingTablesOutputTypeDef,
    ListIdNamespaceAssociationsInputPaginateTypeDef,
    ListIdNamespaceAssociationsOutputTypeDef,
    ListMembershipsInputPaginateTypeDef,
    ListMembershipsOutputTypeDef,
    ListMembersInputPaginateTypeDef,
    ListMembersOutputTypeDef,
    ListPrivacyBudgetsInputPaginateTypeDef,
    ListPrivacyBudgetsOutputTypeDef,
    ListPrivacyBudgetTemplatesInputPaginateTypeDef,
    ListPrivacyBudgetTemplatesOutputTypeDef,
    ListProtectedJobsInputPaginateTypeDef,
    ListProtectedJobsOutputTypeDef,
    ListProtectedQueriesInputPaginateTypeDef,
    ListProtectedQueriesOutputTypeDef,
    ListSchemasInputPaginateTypeDef,
    ListSchemasOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAnalysisTemplatesPaginator",
    "ListCollaborationAnalysisTemplatesPaginator",
    "ListCollaborationConfiguredAudienceModelAssociationsPaginator",
    "ListCollaborationIdNamespaceAssociationsPaginator",
    "ListCollaborationPrivacyBudgetTemplatesPaginator",
    "ListCollaborationPrivacyBudgetsPaginator",
    "ListCollaborationsPaginator",
    "ListConfiguredAudienceModelAssociationsPaginator",
    "ListConfiguredTableAssociationsPaginator",
    "ListConfiguredTablesPaginator",
    "ListIdMappingTablesPaginator",
    "ListIdNamespaceAssociationsPaginator",
    "ListMembersPaginator",
    "ListMembershipsPaginator",
    "ListPrivacyBudgetTemplatesPaginator",
    "ListPrivacyBudgetsPaginator",
    "ListProtectedJobsPaginator",
    "ListProtectedQueriesPaginator",
    "ListSchemasPaginator",
)

if TYPE_CHECKING:
    _ListAnalysisTemplatesPaginatorBase = AioPaginator[ListAnalysisTemplatesOutputTypeDef]
else:
    _ListAnalysisTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAnalysisTemplatesPaginator(_ListAnalysisTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListAnalysisTemplates.html#CleanRoomsService.Paginator.ListAnalysisTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listanalysistemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAnalysisTemplatesInputPaginateTypeDef]
    ) -> AioPageIterator[ListAnalysisTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListAnalysisTemplates.html#CleanRoomsService.Paginator.ListAnalysisTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listanalysistemplatespaginator)
        """

if TYPE_CHECKING:
    _ListCollaborationAnalysisTemplatesPaginatorBase = AioPaginator[
        ListCollaborationAnalysisTemplatesOutputTypeDef
    ]
else:
    _ListCollaborationAnalysisTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCollaborationAnalysisTemplatesPaginator(_ListCollaborationAnalysisTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationAnalysisTemplates.html#CleanRoomsService.Paginator.ListCollaborationAnalysisTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listcollaborationanalysistemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCollaborationAnalysisTemplatesInputPaginateTypeDef]
    ) -> AioPageIterator[ListCollaborationAnalysisTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationAnalysisTemplates.html#CleanRoomsService.Paginator.ListCollaborationAnalysisTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listcollaborationanalysistemplatespaginator)
        """

if TYPE_CHECKING:
    _ListCollaborationConfiguredAudienceModelAssociationsPaginatorBase = AioPaginator[
        ListCollaborationConfiguredAudienceModelAssociationsOutputTypeDef
    ]
else:
    _ListCollaborationConfiguredAudienceModelAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCollaborationConfiguredAudienceModelAssociationsPaginator(
    _ListCollaborationConfiguredAudienceModelAssociationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationConfiguredAudienceModelAssociations.html#CleanRoomsService.Paginator.ListCollaborationConfiguredAudienceModelAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listcollaborationconfiguredaudiencemodelassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self,
        **kwargs: Unpack[ListCollaborationConfiguredAudienceModelAssociationsInputPaginateTypeDef],
    ) -> AioPageIterator[ListCollaborationConfiguredAudienceModelAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationConfiguredAudienceModelAssociations.html#CleanRoomsService.Paginator.ListCollaborationConfiguredAudienceModelAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listcollaborationconfiguredaudiencemodelassociationspaginator)
        """

if TYPE_CHECKING:
    _ListCollaborationIdNamespaceAssociationsPaginatorBase = AioPaginator[
        ListCollaborationIdNamespaceAssociationsOutputTypeDef
    ]
else:
    _ListCollaborationIdNamespaceAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCollaborationIdNamespaceAssociationsPaginator(
    _ListCollaborationIdNamespaceAssociationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationIdNamespaceAssociations.html#CleanRoomsService.Paginator.ListCollaborationIdNamespaceAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listcollaborationidnamespaceassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCollaborationIdNamespaceAssociationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListCollaborationIdNamespaceAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationIdNamespaceAssociations.html#CleanRoomsService.Paginator.ListCollaborationIdNamespaceAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listcollaborationidnamespaceassociationspaginator)
        """

if TYPE_CHECKING:
    _ListCollaborationPrivacyBudgetTemplatesPaginatorBase = AioPaginator[
        ListCollaborationPrivacyBudgetTemplatesOutputTypeDef
    ]
else:
    _ListCollaborationPrivacyBudgetTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCollaborationPrivacyBudgetTemplatesPaginator(
    _ListCollaborationPrivacyBudgetTemplatesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationPrivacyBudgetTemplates.html#CleanRoomsService.Paginator.ListCollaborationPrivacyBudgetTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listcollaborationprivacybudgettemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCollaborationPrivacyBudgetTemplatesInputPaginateTypeDef]
    ) -> AioPageIterator[ListCollaborationPrivacyBudgetTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationPrivacyBudgetTemplates.html#CleanRoomsService.Paginator.ListCollaborationPrivacyBudgetTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listcollaborationprivacybudgettemplatespaginator)
        """

if TYPE_CHECKING:
    _ListCollaborationPrivacyBudgetsPaginatorBase = AioPaginator[
        ListCollaborationPrivacyBudgetsOutputTypeDef
    ]
else:
    _ListCollaborationPrivacyBudgetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCollaborationPrivacyBudgetsPaginator(_ListCollaborationPrivacyBudgetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationPrivacyBudgets.html#CleanRoomsService.Paginator.ListCollaborationPrivacyBudgets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listcollaborationprivacybudgetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCollaborationPrivacyBudgetsInputPaginateTypeDef]
    ) -> AioPageIterator[ListCollaborationPrivacyBudgetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationPrivacyBudgets.html#CleanRoomsService.Paginator.ListCollaborationPrivacyBudgets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listcollaborationprivacybudgetspaginator)
        """

if TYPE_CHECKING:
    _ListCollaborationsPaginatorBase = AioPaginator[ListCollaborationsOutputTypeDef]
else:
    _ListCollaborationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCollaborationsPaginator(_ListCollaborationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborations.html#CleanRoomsService.Paginator.ListCollaborations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listcollaborationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCollaborationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListCollaborationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborations.html#CleanRoomsService.Paginator.ListCollaborations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listcollaborationspaginator)
        """

if TYPE_CHECKING:
    _ListConfiguredAudienceModelAssociationsPaginatorBase = AioPaginator[
        ListConfiguredAudienceModelAssociationsOutputTypeDef
    ]
else:
    _ListConfiguredAudienceModelAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListConfiguredAudienceModelAssociationsPaginator(
    _ListConfiguredAudienceModelAssociationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListConfiguredAudienceModelAssociations.html#CleanRoomsService.Paginator.ListConfiguredAudienceModelAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listconfiguredaudiencemodelassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfiguredAudienceModelAssociationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListConfiguredAudienceModelAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListConfiguredAudienceModelAssociations.html#CleanRoomsService.Paginator.ListConfiguredAudienceModelAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listconfiguredaudiencemodelassociationspaginator)
        """

if TYPE_CHECKING:
    _ListConfiguredTableAssociationsPaginatorBase = AioPaginator[
        ListConfiguredTableAssociationsOutputTypeDef
    ]
else:
    _ListConfiguredTableAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListConfiguredTableAssociationsPaginator(_ListConfiguredTableAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListConfiguredTableAssociations.html#CleanRoomsService.Paginator.ListConfiguredTableAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listconfiguredtableassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfiguredTableAssociationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListConfiguredTableAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListConfiguredTableAssociations.html#CleanRoomsService.Paginator.ListConfiguredTableAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listconfiguredtableassociationspaginator)
        """

if TYPE_CHECKING:
    _ListConfiguredTablesPaginatorBase = AioPaginator[ListConfiguredTablesOutputTypeDef]
else:
    _ListConfiguredTablesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListConfiguredTablesPaginator(_ListConfiguredTablesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListConfiguredTables.html#CleanRoomsService.Paginator.ListConfiguredTables)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listconfiguredtablespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfiguredTablesInputPaginateTypeDef]
    ) -> AioPageIterator[ListConfiguredTablesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListConfiguredTables.html#CleanRoomsService.Paginator.ListConfiguredTables.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listconfiguredtablespaginator)
        """

if TYPE_CHECKING:
    _ListIdMappingTablesPaginatorBase = AioPaginator[ListIdMappingTablesOutputTypeDef]
else:
    _ListIdMappingTablesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIdMappingTablesPaginator(_ListIdMappingTablesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListIdMappingTables.html#CleanRoomsService.Paginator.ListIdMappingTables)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listidmappingtablespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIdMappingTablesInputPaginateTypeDef]
    ) -> AioPageIterator[ListIdMappingTablesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListIdMappingTables.html#CleanRoomsService.Paginator.ListIdMappingTables.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listidmappingtablespaginator)
        """

if TYPE_CHECKING:
    _ListIdNamespaceAssociationsPaginatorBase = AioPaginator[
        ListIdNamespaceAssociationsOutputTypeDef
    ]
else:
    _ListIdNamespaceAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIdNamespaceAssociationsPaginator(_ListIdNamespaceAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListIdNamespaceAssociations.html#CleanRoomsService.Paginator.ListIdNamespaceAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listidnamespaceassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIdNamespaceAssociationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListIdNamespaceAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListIdNamespaceAssociations.html#CleanRoomsService.Paginator.ListIdNamespaceAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listidnamespaceassociationspaginator)
        """

if TYPE_CHECKING:
    _ListMembersPaginatorBase = AioPaginator[ListMembersOutputTypeDef]
else:
    _ListMembersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMembersPaginator(_ListMembersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListMembers.html#CleanRoomsService.Paginator.ListMembers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listmemberspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMembersInputPaginateTypeDef]
    ) -> AioPageIterator[ListMembersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListMembers.html#CleanRoomsService.Paginator.ListMembers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listmemberspaginator)
        """

if TYPE_CHECKING:
    _ListMembershipsPaginatorBase = AioPaginator[ListMembershipsOutputTypeDef]
else:
    _ListMembershipsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMembershipsPaginator(_ListMembershipsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListMemberships.html#CleanRoomsService.Paginator.ListMemberships)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listmembershipspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMembershipsInputPaginateTypeDef]
    ) -> AioPageIterator[ListMembershipsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListMemberships.html#CleanRoomsService.Paginator.ListMemberships.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listmembershipspaginator)
        """

if TYPE_CHECKING:
    _ListPrivacyBudgetTemplatesPaginatorBase = AioPaginator[ListPrivacyBudgetTemplatesOutputTypeDef]
else:
    _ListPrivacyBudgetTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPrivacyBudgetTemplatesPaginator(_ListPrivacyBudgetTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListPrivacyBudgetTemplates.html#CleanRoomsService.Paginator.ListPrivacyBudgetTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listprivacybudgettemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPrivacyBudgetTemplatesInputPaginateTypeDef]
    ) -> AioPageIterator[ListPrivacyBudgetTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListPrivacyBudgetTemplates.html#CleanRoomsService.Paginator.ListPrivacyBudgetTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listprivacybudgettemplatespaginator)
        """

if TYPE_CHECKING:
    _ListPrivacyBudgetsPaginatorBase = AioPaginator[ListPrivacyBudgetsOutputTypeDef]
else:
    _ListPrivacyBudgetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPrivacyBudgetsPaginator(_ListPrivacyBudgetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListPrivacyBudgets.html#CleanRoomsService.Paginator.ListPrivacyBudgets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listprivacybudgetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPrivacyBudgetsInputPaginateTypeDef]
    ) -> AioPageIterator[ListPrivacyBudgetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListPrivacyBudgets.html#CleanRoomsService.Paginator.ListPrivacyBudgets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listprivacybudgetspaginator)
        """

if TYPE_CHECKING:
    _ListProtectedJobsPaginatorBase = AioPaginator[ListProtectedJobsOutputTypeDef]
else:
    _ListProtectedJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProtectedJobsPaginator(_ListProtectedJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListProtectedJobs.html#CleanRoomsService.Paginator.ListProtectedJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listprotectedjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProtectedJobsInputPaginateTypeDef]
    ) -> AioPageIterator[ListProtectedJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListProtectedJobs.html#CleanRoomsService.Paginator.ListProtectedJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listprotectedjobspaginator)
        """

if TYPE_CHECKING:
    _ListProtectedQueriesPaginatorBase = AioPaginator[ListProtectedQueriesOutputTypeDef]
else:
    _ListProtectedQueriesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProtectedQueriesPaginator(_ListProtectedQueriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListProtectedQueries.html#CleanRoomsService.Paginator.ListProtectedQueries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listprotectedqueriespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProtectedQueriesInputPaginateTypeDef]
    ) -> AioPageIterator[ListProtectedQueriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListProtectedQueries.html#CleanRoomsService.Paginator.ListProtectedQueries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listprotectedqueriespaginator)
        """

if TYPE_CHECKING:
    _ListSchemasPaginatorBase = AioPaginator[ListSchemasOutputTypeDef]
else:
    _ListSchemasPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSchemasPaginator(_ListSchemasPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListSchemas.html#CleanRoomsService.Paginator.ListSchemas)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listschemaspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSchemasInputPaginateTypeDef]
    ) -> AioPageIterator[ListSchemasOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListSchemas.html#CleanRoomsService.Paginator.ListSchemas.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listschemaspaginator)
        """
