"""
Type annotations for network-security-manager service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_network_security_manager.client import NetworkSecurityManagerCustomerAPIClient
    from types_aiobotocore_network_security_manager.paginator import (
        ListAdminAccountsPaginator,
        ListAggregateResourceSynchronizationStatusesPaginator,
        ListDeploymentSnapshotsPaginator,
        ListDeploymentsPaginator,
        ListPoliciesPaginator,
        ListPolicySnapshotsPaginator,
        ListResourceAssociationsPaginator,
        ListResourceSynchronizationStatusesPaginator,
        ListRuleSnapshotsPaginator,
        ListRulesPaginator,
        ListScopeSnapshotsPaginator,
        ListScopesPaginator,
        ListTemplateSnapshotsPaginator,
        ListTemplatesPaginator,
    )

    session = get_session()
    with session.create_client("network-security-manager") as client:
        client: NetworkSecurityManagerCustomerAPIClient

        list_admin_accounts_paginator: ListAdminAccountsPaginator = client.get_paginator("list_admin_accounts")
        list_aggregate_resource_synchronization_statuses_paginator: ListAggregateResourceSynchronizationStatusesPaginator = client.get_paginator("list_aggregate_resource_synchronization_statuses")
        list_deployment_snapshots_paginator: ListDeploymentSnapshotsPaginator = client.get_paginator("list_deployment_snapshots")
        list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
        list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
        list_policy_snapshots_paginator: ListPolicySnapshotsPaginator = client.get_paginator("list_policy_snapshots")
        list_resource_associations_paginator: ListResourceAssociationsPaginator = client.get_paginator("list_resource_associations")
        list_resource_synchronization_statuses_paginator: ListResourceSynchronizationStatusesPaginator = client.get_paginator("list_resource_synchronization_statuses")
        list_rule_snapshots_paginator: ListRuleSnapshotsPaginator = client.get_paginator("list_rule_snapshots")
        list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
        list_scope_snapshots_paginator: ListScopeSnapshotsPaginator = client.get_paginator("list_scope_snapshots")
        list_scopes_paginator: ListScopesPaginator = client.get_paginator("list_scopes")
        list_template_snapshots_paginator: ListTemplateSnapshotsPaginator = client.get_paginator("list_template_snapshots")
        list_templates_paginator: ListTemplatesPaginator = client.get_paginator("list_templates")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAdminAccountsRequestPaginateTypeDef,
    ListAdminAccountsResponseTypeDef,
    ListAggregateResourceSynchronizationStatusesInputPaginateTypeDef,
    ListAggregateResourceSynchronizationStatusesOutputTypeDef,
    ListDeploymentsInputPaginateTypeDef,
    ListDeploymentSnapshotsInputPaginateTypeDef,
    ListDeploymentSnapshotsOutputTypeDef,
    ListDeploymentsOutputTypeDef,
    ListPoliciesInputPaginateTypeDef,
    ListPoliciesOutputTypeDef,
    ListPolicySnapshotsInputPaginateTypeDef,
    ListPolicySnapshotsOutputTypeDef,
    ListResourceAssociationsInputPaginateTypeDef,
    ListResourceAssociationsOutputTypeDef,
    ListResourceSynchronizationStatusesInputPaginateTypeDef,
    ListResourceSynchronizationStatusesOutputTypeDef,
    ListRulesInputPaginateTypeDef,
    ListRuleSnapshotsInputPaginateTypeDef,
    ListRuleSnapshotsOutputTypeDef,
    ListRulesOutputTypeDef,
    ListScopesInputPaginateTypeDef,
    ListScopeSnapshotsInputPaginateTypeDef,
    ListScopeSnapshotsOutputTypeDef,
    ListScopesOutputTypeDef,
    ListTemplatesInputPaginateTypeDef,
    ListTemplateSnapshotsInputPaginateTypeDef,
    ListTemplateSnapshotsOutputTypeDef,
    ListTemplatesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAdminAccountsPaginator",
    "ListAggregateResourceSynchronizationStatusesPaginator",
    "ListDeploymentSnapshotsPaginator",
    "ListDeploymentsPaginator",
    "ListPoliciesPaginator",
    "ListPolicySnapshotsPaginator",
    "ListResourceAssociationsPaginator",
    "ListResourceSynchronizationStatusesPaginator",
    "ListRuleSnapshotsPaginator",
    "ListRulesPaginator",
    "ListScopeSnapshotsPaginator",
    "ListScopesPaginator",
    "ListTemplateSnapshotsPaginator",
    "ListTemplatesPaginator",
)


if TYPE_CHECKING:
    _ListAdminAccountsPaginatorBase = AioPaginator[ListAdminAccountsResponseTypeDef]
else:
    _ListAdminAccountsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAdminAccountsPaginator(_ListAdminAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListAdminAccounts.html#NetworkSecurityManagerCustomerAPI.Paginator.ListAdminAccounts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listadminaccountspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAdminAccountsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAdminAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListAdminAccounts.html#NetworkSecurityManagerCustomerAPI.Paginator.ListAdminAccounts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listadminaccountspaginator)
        """


if TYPE_CHECKING:
    _ListAggregateResourceSynchronizationStatusesPaginatorBase = AioPaginator[
        ListAggregateResourceSynchronizationStatusesOutputTypeDef
    ]
else:
    _ListAggregateResourceSynchronizationStatusesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAggregateResourceSynchronizationStatusesPaginator(
    _ListAggregateResourceSynchronizationStatusesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListAggregateResourceSynchronizationStatuses.html#NetworkSecurityManagerCustomerAPI.Paginator.ListAggregateResourceSynchronizationStatuses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listaggregateresourcesynchronizationstatusespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAggregateResourceSynchronizationStatusesInputPaginateTypeDef]
    ) -> AioPageIterator[ListAggregateResourceSynchronizationStatusesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListAggregateResourceSynchronizationStatuses.html#NetworkSecurityManagerCustomerAPI.Paginator.ListAggregateResourceSynchronizationStatuses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listaggregateresourcesynchronizationstatusespaginator)
        """


if TYPE_CHECKING:
    _ListDeploymentSnapshotsPaginatorBase = AioPaginator[ListDeploymentSnapshotsOutputTypeDef]
else:
    _ListDeploymentSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeploymentSnapshotsPaginator(_ListDeploymentSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListDeploymentSnapshots.html#NetworkSecurityManagerCustomerAPI.Paginator.ListDeploymentSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listdeploymentsnapshotspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentSnapshotsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDeploymentSnapshotsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListDeploymentSnapshots.html#NetworkSecurityManagerCustomerAPI.Paginator.ListDeploymentSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listdeploymentsnapshotspaginator)
        """


if TYPE_CHECKING:
    _ListDeploymentsPaginatorBase = AioPaginator[ListDeploymentsOutputTypeDef]
else:
    _ListDeploymentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeploymentsPaginator(_ListDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListDeployments.html#NetworkSecurityManagerCustomerAPI.Paginator.ListDeployments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listdeploymentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDeploymentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListDeployments.html#NetworkSecurityManagerCustomerAPI.Paginator.ListDeployments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listdeploymentspaginator)
        """


if TYPE_CHECKING:
    _ListPoliciesPaginatorBase = AioPaginator[ListPoliciesOutputTypeDef]
else:
    _ListPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPoliciesPaginator(_ListPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListPolicies.html#NetworkSecurityManagerCustomerAPI.Paginator.ListPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listpoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPoliciesInputPaginateTypeDef]
    ) -> AioPageIterator[ListPoliciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListPolicies.html#NetworkSecurityManagerCustomerAPI.Paginator.ListPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listpoliciespaginator)
        """


if TYPE_CHECKING:
    _ListPolicySnapshotsPaginatorBase = AioPaginator[ListPolicySnapshotsOutputTypeDef]
else:
    _ListPolicySnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPolicySnapshotsPaginator(_ListPolicySnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListPolicySnapshots.html#NetworkSecurityManagerCustomerAPI.Paginator.ListPolicySnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listpolicysnapshotspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPolicySnapshotsInputPaginateTypeDef]
    ) -> AioPageIterator[ListPolicySnapshotsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListPolicySnapshots.html#NetworkSecurityManagerCustomerAPI.Paginator.ListPolicySnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listpolicysnapshotspaginator)
        """


if TYPE_CHECKING:
    _ListResourceAssociationsPaginatorBase = AioPaginator[ListResourceAssociationsOutputTypeDef]
else:
    _ListResourceAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourceAssociationsPaginator(_ListResourceAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListResourceAssociations.html#NetworkSecurityManagerCustomerAPI.Paginator.ListResourceAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listresourceassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceAssociationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListResourceAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListResourceAssociations.html#NetworkSecurityManagerCustomerAPI.Paginator.ListResourceAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listresourceassociationspaginator)
        """


if TYPE_CHECKING:
    _ListResourceSynchronizationStatusesPaginatorBase = AioPaginator[
        ListResourceSynchronizationStatusesOutputTypeDef
    ]
else:
    _ListResourceSynchronizationStatusesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourceSynchronizationStatusesPaginator(
    _ListResourceSynchronizationStatusesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListResourceSynchronizationStatuses.html#NetworkSecurityManagerCustomerAPI.Paginator.ListResourceSynchronizationStatuses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listresourcesynchronizationstatusespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceSynchronizationStatusesInputPaginateTypeDef]
    ) -> AioPageIterator[ListResourceSynchronizationStatusesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListResourceSynchronizationStatuses.html#NetworkSecurityManagerCustomerAPI.Paginator.ListResourceSynchronizationStatuses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listresourcesynchronizationstatusespaginator)
        """


if TYPE_CHECKING:
    _ListRuleSnapshotsPaginatorBase = AioPaginator[ListRuleSnapshotsOutputTypeDef]
else:
    _ListRuleSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRuleSnapshotsPaginator(_ListRuleSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListRuleSnapshots.html#NetworkSecurityManagerCustomerAPI.Paginator.ListRuleSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listrulesnapshotspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRuleSnapshotsInputPaginateTypeDef]
    ) -> AioPageIterator[ListRuleSnapshotsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListRuleSnapshots.html#NetworkSecurityManagerCustomerAPI.Paginator.ListRuleSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listrulesnapshotspaginator)
        """


if TYPE_CHECKING:
    _ListRulesPaginatorBase = AioPaginator[ListRulesOutputTypeDef]
else:
    _ListRulesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRulesPaginator(_ListRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListRules.html#NetworkSecurityManagerCustomerAPI.Paginator.ListRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listrulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRulesInputPaginateTypeDef]
    ) -> AioPageIterator[ListRulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListRules.html#NetworkSecurityManagerCustomerAPI.Paginator.ListRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listrulespaginator)
        """


if TYPE_CHECKING:
    _ListScopeSnapshotsPaginatorBase = AioPaginator[ListScopeSnapshotsOutputTypeDef]
else:
    _ListScopeSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListScopeSnapshotsPaginator(_ListScopeSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListScopeSnapshots.html#NetworkSecurityManagerCustomerAPI.Paginator.ListScopeSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listscopesnapshotspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScopeSnapshotsInputPaginateTypeDef]
    ) -> AioPageIterator[ListScopeSnapshotsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListScopeSnapshots.html#NetworkSecurityManagerCustomerAPI.Paginator.ListScopeSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listscopesnapshotspaginator)
        """


if TYPE_CHECKING:
    _ListScopesPaginatorBase = AioPaginator[ListScopesOutputTypeDef]
else:
    _ListScopesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListScopesPaginator(_ListScopesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListScopes.html#NetworkSecurityManagerCustomerAPI.Paginator.ListScopes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listscopespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScopesInputPaginateTypeDef]
    ) -> AioPageIterator[ListScopesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListScopes.html#NetworkSecurityManagerCustomerAPI.Paginator.ListScopes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listscopespaginator)
        """


if TYPE_CHECKING:
    _ListTemplateSnapshotsPaginatorBase = AioPaginator[ListTemplateSnapshotsOutputTypeDef]
else:
    _ListTemplateSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTemplateSnapshotsPaginator(_ListTemplateSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListTemplateSnapshots.html#NetworkSecurityManagerCustomerAPI.Paginator.ListTemplateSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listtemplatesnapshotspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTemplateSnapshotsInputPaginateTypeDef]
    ) -> AioPageIterator[ListTemplateSnapshotsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListTemplateSnapshots.html#NetworkSecurityManagerCustomerAPI.Paginator.ListTemplateSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listtemplatesnapshotspaginator)
        """


if TYPE_CHECKING:
    _ListTemplatesPaginatorBase = AioPaginator[ListTemplatesOutputTypeDef]
else:
    _ListTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTemplatesPaginator(_ListTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListTemplates.html#NetworkSecurityManagerCustomerAPI.Paginator.ListTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listtemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTemplatesInputPaginateTypeDef]
    ) -> AioPageIterator[ListTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/paginator/ListTemplates.html#NetworkSecurityManagerCustomerAPI.Paginator.ListTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/paginators/#listtemplatespaginator)
        """
