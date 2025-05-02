"""
Type annotations for sso-admin service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_sso_admin.client import SSOAdminClient
    from types_boto3_sso_admin.paginator import (
        ListAccountAssignmentCreationStatusPaginator,
        ListAccountAssignmentDeletionStatusPaginator,
        ListAccountAssignmentsForPrincipalPaginator,
        ListAccountAssignmentsPaginator,
        ListAccountsForProvisionedPermissionSetPaginator,
        ListApplicationAccessScopesPaginator,
        ListApplicationAssignmentsForPrincipalPaginator,
        ListApplicationAssignmentsPaginator,
        ListApplicationAuthenticationMethodsPaginator,
        ListApplicationGrantsPaginator,
        ListApplicationProvidersPaginator,
        ListApplicationsPaginator,
        ListCustomerManagedPolicyReferencesInPermissionSetPaginator,
        ListInstancesPaginator,
        ListManagedPoliciesInPermissionSetPaginator,
        ListPermissionSetProvisioningStatusPaginator,
        ListPermissionSetsPaginator,
        ListPermissionSetsProvisionedToAccountPaginator,
        ListTagsForResourcePaginator,
        ListTrustedTokenIssuersPaginator,
    )

    session = Session()
    client: SSOAdminClient = session.client("sso-admin")

    list_account_assignment_creation_status_paginator: ListAccountAssignmentCreationStatusPaginator = client.get_paginator("list_account_assignment_creation_status")
    list_account_assignment_deletion_status_paginator: ListAccountAssignmentDeletionStatusPaginator = client.get_paginator("list_account_assignment_deletion_status")
    list_account_assignments_for_principal_paginator: ListAccountAssignmentsForPrincipalPaginator = client.get_paginator("list_account_assignments_for_principal")
    list_account_assignments_paginator: ListAccountAssignmentsPaginator = client.get_paginator("list_account_assignments")
    list_accounts_for_provisioned_permission_set_paginator: ListAccountsForProvisionedPermissionSetPaginator = client.get_paginator("list_accounts_for_provisioned_permission_set")
    list_application_access_scopes_paginator: ListApplicationAccessScopesPaginator = client.get_paginator("list_application_access_scopes")
    list_application_assignments_for_principal_paginator: ListApplicationAssignmentsForPrincipalPaginator = client.get_paginator("list_application_assignments_for_principal")
    list_application_assignments_paginator: ListApplicationAssignmentsPaginator = client.get_paginator("list_application_assignments")
    list_application_authentication_methods_paginator: ListApplicationAuthenticationMethodsPaginator = client.get_paginator("list_application_authentication_methods")
    list_application_grants_paginator: ListApplicationGrantsPaginator = client.get_paginator("list_application_grants")
    list_application_providers_paginator: ListApplicationProvidersPaginator = client.get_paginator("list_application_providers")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_customer_managed_policy_references_in_permission_set_paginator: ListCustomerManagedPolicyReferencesInPermissionSetPaginator = client.get_paginator("list_customer_managed_policy_references_in_permission_set")
    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    list_managed_policies_in_permission_set_paginator: ListManagedPoliciesInPermissionSetPaginator = client.get_paginator("list_managed_policies_in_permission_set")
    list_permission_set_provisioning_status_paginator: ListPermissionSetProvisioningStatusPaginator = client.get_paginator("list_permission_set_provisioning_status")
    list_permission_sets_paginator: ListPermissionSetsPaginator = client.get_paginator("list_permission_sets")
    list_permission_sets_provisioned_to_account_paginator: ListPermissionSetsProvisionedToAccountPaginator = client.get_paginator("list_permission_sets_provisioned_to_account")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_trusted_token_issuers_paginator: ListTrustedTokenIssuersPaginator = client.get_paginator("list_trusted_token_issuers")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAccountAssignmentCreationStatusRequestPaginateTypeDef,
    ListAccountAssignmentCreationStatusResponseTypeDef,
    ListAccountAssignmentDeletionStatusRequestPaginateTypeDef,
    ListAccountAssignmentDeletionStatusResponseTypeDef,
    ListAccountAssignmentsForPrincipalRequestPaginateTypeDef,
    ListAccountAssignmentsForPrincipalResponseTypeDef,
    ListAccountAssignmentsRequestPaginateTypeDef,
    ListAccountAssignmentsResponseTypeDef,
    ListAccountsForProvisionedPermissionSetRequestPaginateTypeDef,
    ListAccountsForProvisionedPermissionSetResponseTypeDef,
    ListApplicationAccessScopesRequestPaginateTypeDef,
    ListApplicationAccessScopesResponseTypeDef,
    ListApplicationAssignmentsForPrincipalRequestPaginateTypeDef,
    ListApplicationAssignmentsForPrincipalResponseTypeDef,
    ListApplicationAssignmentsRequestPaginateTypeDef,
    ListApplicationAssignmentsResponseTypeDef,
    ListApplicationAuthenticationMethodsRequestPaginateTypeDef,
    ListApplicationAuthenticationMethodsResponseTypeDef,
    ListApplicationGrantsRequestPaginateTypeDef,
    ListApplicationGrantsResponseTypeDef,
    ListApplicationProvidersRequestPaginateTypeDef,
    ListApplicationProvidersResponseTypeDef,
    ListApplicationsRequestPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListCustomerManagedPolicyReferencesInPermissionSetRequestPaginateTypeDef,
    ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef,
    ListInstancesRequestPaginateTypeDef,
    ListInstancesResponseTypeDef,
    ListManagedPoliciesInPermissionSetRequestPaginateTypeDef,
    ListManagedPoliciesInPermissionSetResponseTypeDef,
    ListPermissionSetProvisioningStatusRequestPaginateTypeDef,
    ListPermissionSetProvisioningStatusResponseTypeDef,
    ListPermissionSetsProvisionedToAccountRequestPaginateTypeDef,
    ListPermissionSetsProvisionedToAccountResponseTypeDef,
    ListPermissionSetsRequestPaginateTypeDef,
    ListPermissionSetsResponseTypeDef,
    ListTagsForResourceRequestPaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrustedTokenIssuersRequestPaginateTypeDef,
    ListTrustedTokenIssuersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAccountAssignmentCreationStatusPaginator",
    "ListAccountAssignmentDeletionStatusPaginator",
    "ListAccountAssignmentsForPrincipalPaginator",
    "ListAccountAssignmentsPaginator",
    "ListAccountsForProvisionedPermissionSetPaginator",
    "ListApplicationAccessScopesPaginator",
    "ListApplicationAssignmentsForPrincipalPaginator",
    "ListApplicationAssignmentsPaginator",
    "ListApplicationAuthenticationMethodsPaginator",
    "ListApplicationGrantsPaginator",
    "ListApplicationProvidersPaginator",
    "ListApplicationsPaginator",
    "ListCustomerManagedPolicyReferencesInPermissionSetPaginator",
    "ListInstancesPaginator",
    "ListManagedPoliciesInPermissionSetPaginator",
    "ListPermissionSetProvisioningStatusPaginator",
    "ListPermissionSetsPaginator",
    "ListPermissionSetsProvisionedToAccountPaginator",
    "ListTagsForResourcePaginator",
    "ListTrustedTokenIssuersPaginator",
)


if TYPE_CHECKING:
    _ListAccountAssignmentCreationStatusPaginatorBase = Paginator[
        ListAccountAssignmentCreationStatusResponseTypeDef
    ]
else:
    _ListAccountAssignmentCreationStatusPaginatorBase = Paginator  # type: ignore[assignment]


class ListAccountAssignmentCreationStatusPaginator(
    _ListAccountAssignmentCreationStatusPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignmentCreationStatus.html#SSOAdmin.Paginator.ListAccountAssignmentCreationStatus)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listaccountassignmentcreationstatuspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccountAssignmentCreationStatusRequestPaginateTypeDef]
    ) -> PageIterator[ListAccountAssignmentCreationStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignmentCreationStatus.html#SSOAdmin.Paginator.ListAccountAssignmentCreationStatus.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listaccountassignmentcreationstatuspaginator)
        """


if TYPE_CHECKING:
    _ListAccountAssignmentDeletionStatusPaginatorBase = Paginator[
        ListAccountAssignmentDeletionStatusResponseTypeDef
    ]
else:
    _ListAccountAssignmentDeletionStatusPaginatorBase = Paginator  # type: ignore[assignment]


class ListAccountAssignmentDeletionStatusPaginator(
    _ListAccountAssignmentDeletionStatusPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignmentDeletionStatus.html#SSOAdmin.Paginator.ListAccountAssignmentDeletionStatus)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listaccountassignmentdeletionstatuspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccountAssignmentDeletionStatusRequestPaginateTypeDef]
    ) -> PageIterator[ListAccountAssignmentDeletionStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignmentDeletionStatus.html#SSOAdmin.Paginator.ListAccountAssignmentDeletionStatus.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listaccountassignmentdeletionstatuspaginator)
        """


if TYPE_CHECKING:
    _ListAccountAssignmentsForPrincipalPaginatorBase = Paginator[
        ListAccountAssignmentsForPrincipalResponseTypeDef
    ]
else:
    _ListAccountAssignmentsForPrincipalPaginatorBase = Paginator  # type: ignore[assignment]


class ListAccountAssignmentsForPrincipalPaginator(_ListAccountAssignmentsForPrincipalPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignmentsForPrincipal.html#SSOAdmin.Paginator.ListAccountAssignmentsForPrincipal)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listaccountassignmentsforprincipalpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccountAssignmentsForPrincipalRequestPaginateTypeDef]
    ) -> PageIterator[ListAccountAssignmentsForPrincipalResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignmentsForPrincipal.html#SSOAdmin.Paginator.ListAccountAssignmentsForPrincipal.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listaccountassignmentsforprincipalpaginator)
        """


if TYPE_CHECKING:
    _ListAccountAssignmentsPaginatorBase = Paginator[ListAccountAssignmentsResponseTypeDef]
else:
    _ListAccountAssignmentsPaginatorBase = Paginator  # type: ignore[assignment]


class ListAccountAssignmentsPaginator(_ListAccountAssignmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignments.html#SSOAdmin.Paginator.ListAccountAssignments)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listaccountassignmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccountAssignmentsRequestPaginateTypeDef]
    ) -> PageIterator[ListAccountAssignmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountAssignments.html#SSOAdmin.Paginator.ListAccountAssignments.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listaccountassignmentspaginator)
        """


if TYPE_CHECKING:
    _ListAccountsForProvisionedPermissionSetPaginatorBase = Paginator[
        ListAccountsForProvisionedPermissionSetResponseTypeDef
    ]
else:
    _ListAccountsForProvisionedPermissionSetPaginatorBase = Paginator  # type: ignore[assignment]


class ListAccountsForProvisionedPermissionSetPaginator(
    _ListAccountsForProvisionedPermissionSetPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountsForProvisionedPermissionSet.html#SSOAdmin.Paginator.ListAccountsForProvisionedPermissionSet)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listaccountsforprovisionedpermissionsetpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccountsForProvisionedPermissionSetRequestPaginateTypeDef]
    ) -> PageIterator[ListAccountsForProvisionedPermissionSetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListAccountsForProvisionedPermissionSet.html#SSOAdmin.Paginator.ListAccountsForProvisionedPermissionSet.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listaccountsforprovisionedpermissionsetpaginator)
        """


if TYPE_CHECKING:
    _ListApplicationAccessScopesPaginatorBase = Paginator[
        ListApplicationAccessScopesResponseTypeDef
    ]
else:
    _ListApplicationAccessScopesPaginatorBase = Paginator  # type: ignore[assignment]


class ListApplicationAccessScopesPaginator(_ListApplicationAccessScopesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAccessScopes.html#SSOAdmin.Paginator.ListApplicationAccessScopes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listapplicationaccessscopespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationAccessScopesRequestPaginateTypeDef]
    ) -> PageIterator[ListApplicationAccessScopesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAccessScopes.html#SSOAdmin.Paginator.ListApplicationAccessScopes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listapplicationaccessscopespaginator)
        """


if TYPE_CHECKING:
    _ListApplicationAssignmentsForPrincipalPaginatorBase = Paginator[
        ListApplicationAssignmentsForPrincipalResponseTypeDef
    ]
else:
    _ListApplicationAssignmentsForPrincipalPaginatorBase = Paginator  # type: ignore[assignment]


class ListApplicationAssignmentsForPrincipalPaginator(
    _ListApplicationAssignmentsForPrincipalPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAssignmentsForPrincipal.html#SSOAdmin.Paginator.ListApplicationAssignmentsForPrincipal)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listapplicationassignmentsforprincipalpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationAssignmentsForPrincipalRequestPaginateTypeDef]
    ) -> PageIterator[ListApplicationAssignmentsForPrincipalResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAssignmentsForPrincipal.html#SSOAdmin.Paginator.ListApplicationAssignmentsForPrincipal.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listapplicationassignmentsforprincipalpaginator)
        """


if TYPE_CHECKING:
    _ListApplicationAssignmentsPaginatorBase = Paginator[ListApplicationAssignmentsResponseTypeDef]
else:
    _ListApplicationAssignmentsPaginatorBase = Paginator  # type: ignore[assignment]


class ListApplicationAssignmentsPaginator(_ListApplicationAssignmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAssignments.html#SSOAdmin.Paginator.ListApplicationAssignments)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listapplicationassignmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationAssignmentsRequestPaginateTypeDef]
    ) -> PageIterator[ListApplicationAssignmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAssignments.html#SSOAdmin.Paginator.ListApplicationAssignments.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listapplicationassignmentspaginator)
        """


if TYPE_CHECKING:
    _ListApplicationAuthenticationMethodsPaginatorBase = Paginator[
        ListApplicationAuthenticationMethodsResponseTypeDef
    ]
else:
    _ListApplicationAuthenticationMethodsPaginatorBase = Paginator  # type: ignore[assignment]


class ListApplicationAuthenticationMethodsPaginator(
    _ListApplicationAuthenticationMethodsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAuthenticationMethods.html#SSOAdmin.Paginator.ListApplicationAuthenticationMethods)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listapplicationauthenticationmethodspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationAuthenticationMethodsRequestPaginateTypeDef]
    ) -> PageIterator[ListApplicationAuthenticationMethodsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationAuthenticationMethods.html#SSOAdmin.Paginator.ListApplicationAuthenticationMethods.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listapplicationauthenticationmethodspaginator)
        """


if TYPE_CHECKING:
    _ListApplicationGrantsPaginatorBase = Paginator[ListApplicationGrantsResponseTypeDef]
else:
    _ListApplicationGrantsPaginatorBase = Paginator  # type: ignore[assignment]


class ListApplicationGrantsPaginator(_ListApplicationGrantsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationGrants.html#SSOAdmin.Paginator.ListApplicationGrants)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listapplicationgrantspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationGrantsRequestPaginateTypeDef]
    ) -> PageIterator[ListApplicationGrantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationGrants.html#SSOAdmin.Paginator.ListApplicationGrants.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listapplicationgrantspaginator)
        """


if TYPE_CHECKING:
    _ListApplicationProvidersPaginatorBase = Paginator[ListApplicationProvidersResponseTypeDef]
else:
    _ListApplicationProvidersPaginatorBase = Paginator  # type: ignore[assignment]


class ListApplicationProvidersPaginator(_ListApplicationProvidersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationProviders.html#SSOAdmin.Paginator.ListApplicationProviders)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listapplicationproviderspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationProvidersRequestPaginateTypeDef]
    ) -> PageIterator[ListApplicationProvidersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplicationProviders.html#SSOAdmin.Paginator.ListApplicationProviders.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listapplicationproviderspaginator)
        """


if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = Paginator[ListApplicationsResponseTypeDef]
else:
    _ListApplicationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplications.html#SSOAdmin.Paginator.ListApplications)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listapplicationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsRequestPaginateTypeDef]
    ) -> PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListApplications.html#SSOAdmin.Paginator.ListApplications.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listapplicationspaginator)
        """


if TYPE_CHECKING:
    _ListCustomerManagedPolicyReferencesInPermissionSetPaginatorBase = Paginator[
        ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef
    ]
else:
    _ListCustomerManagedPolicyReferencesInPermissionSetPaginatorBase = Paginator  # type: ignore[assignment]


class ListCustomerManagedPolicyReferencesInPermissionSetPaginator(
    _ListCustomerManagedPolicyReferencesInPermissionSetPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListCustomerManagedPolicyReferencesInPermissionSet.html#SSOAdmin.Paginator.ListCustomerManagedPolicyReferencesInPermissionSet)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listcustomermanagedpolicyreferencesinpermissionsetpaginator)
    """

    def paginate(  # type: ignore[override]
        self,
        **kwargs: Unpack[ListCustomerManagedPolicyReferencesInPermissionSetRequestPaginateTypeDef],
    ) -> PageIterator[ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListCustomerManagedPolicyReferencesInPermissionSet.html#SSOAdmin.Paginator.ListCustomerManagedPolicyReferencesInPermissionSet.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listcustomermanagedpolicyreferencesinpermissionsetpaginator)
        """


if TYPE_CHECKING:
    _ListInstancesPaginatorBase = Paginator[ListInstancesResponseTypeDef]
else:
    _ListInstancesPaginatorBase = Paginator  # type: ignore[assignment]


class ListInstancesPaginator(_ListInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListInstances.html#SSOAdmin.Paginator.ListInstances)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstancesRequestPaginateTypeDef]
    ) -> PageIterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListInstances.html#SSOAdmin.Paginator.ListInstances.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listinstancespaginator)
        """


if TYPE_CHECKING:
    _ListManagedPoliciesInPermissionSetPaginatorBase = Paginator[
        ListManagedPoliciesInPermissionSetResponseTypeDef
    ]
else:
    _ListManagedPoliciesInPermissionSetPaginatorBase = Paginator  # type: ignore[assignment]


class ListManagedPoliciesInPermissionSetPaginator(_ListManagedPoliciesInPermissionSetPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListManagedPoliciesInPermissionSet.html#SSOAdmin.Paginator.ListManagedPoliciesInPermissionSet)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listmanagedpoliciesinpermissionsetpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedPoliciesInPermissionSetRequestPaginateTypeDef]
    ) -> PageIterator[ListManagedPoliciesInPermissionSetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListManagedPoliciesInPermissionSet.html#SSOAdmin.Paginator.ListManagedPoliciesInPermissionSet.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listmanagedpoliciesinpermissionsetpaginator)
        """


if TYPE_CHECKING:
    _ListPermissionSetProvisioningStatusPaginatorBase = Paginator[
        ListPermissionSetProvisioningStatusResponseTypeDef
    ]
else:
    _ListPermissionSetProvisioningStatusPaginatorBase = Paginator  # type: ignore[assignment]


class ListPermissionSetProvisioningStatusPaginator(
    _ListPermissionSetProvisioningStatusPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListPermissionSetProvisioningStatus.html#SSOAdmin.Paginator.ListPermissionSetProvisioningStatus)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listpermissionsetprovisioningstatuspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPermissionSetProvisioningStatusRequestPaginateTypeDef]
    ) -> PageIterator[ListPermissionSetProvisioningStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListPermissionSetProvisioningStatus.html#SSOAdmin.Paginator.ListPermissionSetProvisioningStatus.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listpermissionsetprovisioningstatuspaginator)
        """


if TYPE_CHECKING:
    _ListPermissionSetsPaginatorBase = Paginator[ListPermissionSetsResponseTypeDef]
else:
    _ListPermissionSetsPaginatorBase = Paginator  # type: ignore[assignment]


class ListPermissionSetsPaginator(_ListPermissionSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListPermissionSets.html#SSOAdmin.Paginator.ListPermissionSets)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listpermissionsetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPermissionSetsRequestPaginateTypeDef]
    ) -> PageIterator[ListPermissionSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListPermissionSets.html#SSOAdmin.Paginator.ListPermissionSets.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listpermissionsetspaginator)
        """


if TYPE_CHECKING:
    _ListPermissionSetsProvisionedToAccountPaginatorBase = Paginator[
        ListPermissionSetsProvisionedToAccountResponseTypeDef
    ]
else:
    _ListPermissionSetsProvisionedToAccountPaginatorBase = Paginator  # type: ignore[assignment]


class ListPermissionSetsProvisionedToAccountPaginator(
    _ListPermissionSetsProvisionedToAccountPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListPermissionSetsProvisionedToAccount.html#SSOAdmin.Paginator.ListPermissionSetsProvisionedToAccount)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listpermissionsetsprovisionedtoaccountpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPermissionSetsProvisionedToAccountRequestPaginateTypeDef]
    ) -> PageIterator[ListPermissionSetsProvisionedToAccountResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListPermissionSetsProvisionedToAccount.html#SSOAdmin.Paginator.ListPermissionSetsProvisionedToAccount.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listpermissionsetsprovisionedtoaccountpaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = Paginator[ListTagsForResourceResponseTypeDef]
else:
    _ListTagsForResourcePaginatorBase = Paginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListTagsForResource.html#SSOAdmin.Paginator.ListTagsForResource)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceRequestPaginateTypeDef]
    ) -> PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListTagsForResource.html#SSOAdmin.Paginator.ListTagsForResource.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listtagsforresourcepaginator)
        """


if TYPE_CHECKING:
    _ListTrustedTokenIssuersPaginatorBase = Paginator[ListTrustedTokenIssuersResponseTypeDef]
else:
    _ListTrustedTokenIssuersPaginatorBase = Paginator  # type: ignore[assignment]


class ListTrustedTokenIssuersPaginator(_ListTrustedTokenIssuersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListTrustedTokenIssuers.html#SSOAdmin.Paginator.ListTrustedTokenIssuers)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listtrustedtokenissuerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrustedTokenIssuersRequestPaginateTypeDef]
    ) -> PageIterator[ListTrustedTokenIssuersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/paginator/ListTrustedTokenIssuers.html#SSOAdmin.Paginator.ListTrustedTokenIssuers.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/paginators/#listtrustedtokenissuerspaginator)
        """
