"""
Type annotations for iam service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iam.client import IAMClient
    from types_aiobotocore_iam.paginator import (
        GetAccountAuthorizationDetailsPaginator,
        GetGroupPaginator,
        ListAccessKeysPaginator,
        ListAccountAliasesPaginator,
        ListAttachedGroupPoliciesPaginator,
        ListAttachedRolePoliciesPaginator,
        ListAttachedUserPoliciesPaginator,
        ListEntitiesForPolicyPaginator,
        ListGroupPoliciesPaginator,
        ListGroupsForUserPaginator,
        ListGroupsPaginator,
        ListInstanceProfileTagsPaginator,
        ListInstanceProfilesForRolePaginator,
        ListInstanceProfilesPaginator,
        ListMFADeviceTagsPaginator,
        ListMFADevicesPaginator,
        ListOpenIDConnectProviderTagsPaginator,
        ListPoliciesPaginator,
        ListPolicyTagsPaginator,
        ListPolicyVersionsPaginator,
        ListRolePoliciesPaginator,
        ListRoleTagsPaginator,
        ListRolesPaginator,
        ListSAMLProviderTagsPaginator,
        ListSSHPublicKeysPaginator,
        ListServerCertificateTagsPaginator,
        ListServerCertificatesPaginator,
        ListSigningCertificatesPaginator,
        ListUserPoliciesPaginator,
        ListUserTagsPaginator,
        ListUsersPaginator,
        ListVirtualMFADevicesPaginator,
        SimulateCustomPolicyPaginator,
        SimulatePrincipalPolicyPaginator,
    )

    session = get_session()
    with session.create_client("iam") as client:
        client: IAMClient

        get_account_authorization_details_paginator: GetAccountAuthorizationDetailsPaginator = client.get_paginator("get_account_authorization_details")
        get_group_paginator: GetGroupPaginator = client.get_paginator("get_group")
        list_access_keys_paginator: ListAccessKeysPaginator = client.get_paginator("list_access_keys")
        list_account_aliases_paginator: ListAccountAliasesPaginator = client.get_paginator("list_account_aliases")
        list_attached_group_policies_paginator: ListAttachedGroupPoliciesPaginator = client.get_paginator("list_attached_group_policies")
        list_attached_role_policies_paginator: ListAttachedRolePoliciesPaginator = client.get_paginator("list_attached_role_policies")
        list_attached_user_policies_paginator: ListAttachedUserPoliciesPaginator = client.get_paginator("list_attached_user_policies")
        list_entities_for_policy_paginator: ListEntitiesForPolicyPaginator = client.get_paginator("list_entities_for_policy")
        list_group_policies_paginator: ListGroupPoliciesPaginator = client.get_paginator("list_group_policies")
        list_groups_for_user_paginator: ListGroupsForUserPaginator = client.get_paginator("list_groups_for_user")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_instance_profile_tags_paginator: ListInstanceProfileTagsPaginator = client.get_paginator("list_instance_profile_tags")
        list_instance_profiles_for_role_paginator: ListInstanceProfilesForRolePaginator = client.get_paginator("list_instance_profiles_for_role")
        list_instance_profiles_paginator: ListInstanceProfilesPaginator = client.get_paginator("list_instance_profiles")
        list_mfa_device_tags_paginator: ListMFADeviceTagsPaginator = client.get_paginator("list_mfa_device_tags")
        list_mfa_devices_paginator: ListMFADevicesPaginator = client.get_paginator("list_mfa_devices")
        list_open_id_connect_provider_tags_paginator: ListOpenIDConnectProviderTagsPaginator = client.get_paginator("list_open_id_connect_provider_tags")
        list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
        list_policy_tags_paginator: ListPolicyTagsPaginator = client.get_paginator("list_policy_tags")
        list_policy_versions_paginator: ListPolicyVersionsPaginator = client.get_paginator("list_policy_versions")
        list_role_policies_paginator: ListRolePoliciesPaginator = client.get_paginator("list_role_policies")
        list_role_tags_paginator: ListRoleTagsPaginator = client.get_paginator("list_role_tags")
        list_roles_paginator: ListRolesPaginator = client.get_paginator("list_roles")
        list_saml_provider_tags_paginator: ListSAMLProviderTagsPaginator = client.get_paginator("list_saml_provider_tags")
        list_ssh_public_keys_paginator: ListSSHPublicKeysPaginator = client.get_paginator("list_ssh_public_keys")
        list_server_certificate_tags_paginator: ListServerCertificateTagsPaginator = client.get_paginator("list_server_certificate_tags")
        list_server_certificates_paginator: ListServerCertificatesPaginator = client.get_paginator("list_server_certificates")
        list_signing_certificates_paginator: ListSigningCertificatesPaginator = client.get_paginator("list_signing_certificates")
        list_user_policies_paginator: ListUserPoliciesPaginator = client.get_paginator("list_user_policies")
        list_user_tags_paginator: ListUserTagsPaginator = client.get_paginator("list_user_tags")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
        list_virtual_mfa_devices_paginator: ListVirtualMFADevicesPaginator = client.get_paginator("list_virtual_mfa_devices")
        simulate_custom_policy_paginator: SimulateCustomPolicyPaginator = client.get_paginator("simulate_custom_policy")
        simulate_principal_policy_paginator: SimulatePrincipalPolicyPaginator = client.get_paginator("simulate_principal_policy")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetAccountAuthorizationDetailsRequestPaginateTypeDef,
    GetAccountAuthorizationDetailsResponseTypeDef,
    GetGroupRequestPaginateTypeDef,
    GetGroupResponseTypeDef,
    ListAccessKeysRequestPaginateTypeDef,
    ListAccessKeysResponseTypeDef,
    ListAccountAliasesRequestPaginateTypeDef,
    ListAccountAliasesResponseTypeDef,
    ListAttachedGroupPoliciesRequestPaginateTypeDef,
    ListAttachedGroupPoliciesResponseTypeDef,
    ListAttachedRolePoliciesRequestPaginateTypeDef,
    ListAttachedRolePoliciesResponseTypeDef,
    ListAttachedUserPoliciesRequestPaginateTypeDef,
    ListAttachedUserPoliciesResponseTypeDef,
    ListEntitiesForPolicyRequestPaginateTypeDef,
    ListEntitiesForPolicyResponseTypeDef,
    ListGroupPoliciesRequestPaginateTypeDef,
    ListGroupPoliciesResponseTypeDef,
    ListGroupsForUserRequestPaginateTypeDef,
    ListGroupsForUserResponseTypeDef,
    ListGroupsRequestPaginateTypeDef,
    ListGroupsResponseTypeDef,
    ListInstanceProfilesForRoleRequestPaginateTypeDef,
    ListInstanceProfilesForRoleResponseTypeDef,
    ListInstanceProfilesRequestPaginateTypeDef,
    ListInstanceProfilesResponseTypeDef,
    ListInstanceProfileTagsRequestPaginateTypeDef,
    ListInstanceProfileTagsResponseTypeDef,
    ListMFADevicesRequestPaginateTypeDef,
    ListMFADevicesResponseTypeDef,
    ListMFADeviceTagsRequestPaginateTypeDef,
    ListMFADeviceTagsResponseTypeDef,
    ListOpenIDConnectProviderTagsRequestPaginateTypeDef,
    ListOpenIDConnectProviderTagsResponseTypeDef,
    ListPoliciesRequestPaginateTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyTagsRequestPaginateTypeDef,
    ListPolicyTagsResponseTypeDef,
    ListPolicyVersionsRequestPaginateTypeDef,
    ListPolicyVersionsResponseTypeDef,
    ListRolePoliciesRequestPaginateTypeDef,
    ListRolePoliciesResponseTypeDef,
    ListRolesRequestPaginateTypeDef,
    ListRolesResponseTypeDef,
    ListRoleTagsRequestPaginateTypeDef,
    ListRoleTagsResponseTypeDef,
    ListSAMLProviderTagsRequestPaginateTypeDef,
    ListSAMLProviderTagsResponseTypeDef,
    ListServerCertificatesRequestPaginateTypeDef,
    ListServerCertificatesResponseTypeDef,
    ListServerCertificateTagsRequestPaginateTypeDef,
    ListServerCertificateTagsResponseTypeDef,
    ListSigningCertificatesRequestPaginateTypeDef,
    ListSigningCertificatesResponseTypeDef,
    ListSSHPublicKeysRequestPaginateTypeDef,
    ListSSHPublicKeysResponseTypeDef,
    ListUserPoliciesRequestPaginateTypeDef,
    ListUserPoliciesResponseTypeDef,
    ListUsersRequestPaginateTypeDef,
    ListUsersResponseTypeDef,
    ListUserTagsRequestPaginateTypeDef,
    ListUserTagsResponseTypeDef,
    ListVirtualMFADevicesRequestPaginateTypeDef,
    ListVirtualMFADevicesResponseTypeDef,
    SimulateCustomPolicyRequestPaginateTypeDef,
    SimulatePolicyResponseTypeDef,
    SimulatePrincipalPolicyRequestPaginateTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetAccountAuthorizationDetailsPaginator",
    "GetGroupPaginator",
    "ListAccessKeysPaginator",
    "ListAccountAliasesPaginator",
    "ListAttachedGroupPoliciesPaginator",
    "ListAttachedRolePoliciesPaginator",
    "ListAttachedUserPoliciesPaginator",
    "ListEntitiesForPolicyPaginator",
    "ListGroupPoliciesPaginator",
    "ListGroupsForUserPaginator",
    "ListGroupsPaginator",
    "ListInstanceProfileTagsPaginator",
    "ListInstanceProfilesForRolePaginator",
    "ListInstanceProfilesPaginator",
    "ListMFADeviceTagsPaginator",
    "ListMFADevicesPaginator",
    "ListOpenIDConnectProviderTagsPaginator",
    "ListPoliciesPaginator",
    "ListPolicyTagsPaginator",
    "ListPolicyVersionsPaginator",
    "ListRolePoliciesPaginator",
    "ListRoleTagsPaginator",
    "ListRolesPaginator",
    "ListSAMLProviderTagsPaginator",
    "ListSSHPublicKeysPaginator",
    "ListServerCertificateTagsPaginator",
    "ListServerCertificatesPaginator",
    "ListSigningCertificatesPaginator",
    "ListUserPoliciesPaginator",
    "ListUserTagsPaginator",
    "ListUsersPaginator",
    "ListVirtualMFADevicesPaginator",
    "SimulateCustomPolicyPaginator",
    "SimulatePrincipalPolicyPaginator",
)

if TYPE_CHECKING:
    _GetAccountAuthorizationDetailsPaginatorBase = AioPaginator[
        GetAccountAuthorizationDetailsResponseTypeDef
    ]
else:
    _GetAccountAuthorizationDetailsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetAccountAuthorizationDetailsPaginator(_GetAccountAuthorizationDetailsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/GetAccountAuthorizationDetails.html#IAM.Paginator.GetAccountAuthorizationDetails)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#getaccountauthorizationdetailspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAccountAuthorizationDetailsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetAccountAuthorizationDetailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/GetAccountAuthorizationDetails.html#IAM.Paginator.GetAccountAuthorizationDetails.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#getaccountauthorizationdetailspaginator)
        """

if TYPE_CHECKING:
    _GetGroupPaginatorBase = AioPaginator[GetGroupResponseTypeDef]
else:
    _GetGroupPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetGroupPaginator(_GetGroupPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/GetGroup.html#IAM.Paginator.GetGroup)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#getgrouppaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetGroupRequestPaginateTypeDef]
    ) -> AioPageIterator[GetGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/GetGroup.html#IAM.Paginator.GetGroup.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#getgrouppaginator)
        """

if TYPE_CHECKING:
    _ListAccessKeysPaginatorBase = AioPaginator[ListAccessKeysResponseTypeDef]
else:
    _ListAccessKeysPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAccessKeysPaginator(_ListAccessKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAccessKeys.html#IAM.Paginator.ListAccessKeys)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listaccesskeyspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccessKeysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAccessKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAccessKeys.html#IAM.Paginator.ListAccessKeys.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listaccesskeyspaginator)
        """

if TYPE_CHECKING:
    _ListAccountAliasesPaginatorBase = AioPaginator[ListAccountAliasesResponseTypeDef]
else:
    _ListAccountAliasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAccountAliasesPaginator(_ListAccountAliasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAccountAliases.html#IAM.Paginator.ListAccountAliases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listaccountaliasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccountAliasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAccountAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAccountAliases.html#IAM.Paginator.ListAccountAliases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listaccountaliasespaginator)
        """

if TYPE_CHECKING:
    _ListAttachedGroupPoliciesPaginatorBase = AioPaginator[ListAttachedGroupPoliciesResponseTypeDef]
else:
    _ListAttachedGroupPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAttachedGroupPoliciesPaginator(_ListAttachedGroupPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedGroupPolicies.html#IAM.Paginator.ListAttachedGroupPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattachedgrouppoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAttachedGroupPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAttachedGroupPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedGroupPolicies.html#IAM.Paginator.ListAttachedGroupPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattachedgrouppoliciespaginator)
        """

if TYPE_CHECKING:
    _ListAttachedRolePoliciesPaginatorBase = AioPaginator[ListAttachedRolePoliciesResponseTypeDef]
else:
    _ListAttachedRolePoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAttachedRolePoliciesPaginator(_ListAttachedRolePoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedRolePolicies.html#IAM.Paginator.ListAttachedRolePolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattachedrolepoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAttachedRolePoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAttachedRolePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedRolePolicies.html#IAM.Paginator.ListAttachedRolePolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattachedrolepoliciespaginator)
        """

if TYPE_CHECKING:
    _ListAttachedUserPoliciesPaginatorBase = AioPaginator[ListAttachedUserPoliciesResponseTypeDef]
else:
    _ListAttachedUserPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAttachedUserPoliciesPaginator(_ListAttachedUserPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedUserPolicies.html#IAM.Paginator.ListAttachedUserPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattacheduserpoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAttachedUserPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAttachedUserPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedUserPolicies.html#IAM.Paginator.ListAttachedUserPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattacheduserpoliciespaginator)
        """

if TYPE_CHECKING:
    _ListEntitiesForPolicyPaginatorBase = AioPaginator[ListEntitiesForPolicyResponseTypeDef]
else:
    _ListEntitiesForPolicyPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEntitiesForPolicyPaginator(_ListEntitiesForPolicyPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListEntitiesForPolicy.html#IAM.Paginator.ListEntitiesForPolicy)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listentitiesforpolicypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEntitiesForPolicyRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEntitiesForPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListEntitiesForPolicy.html#IAM.Paginator.ListEntitiesForPolicy.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listentitiesforpolicypaginator)
        """

if TYPE_CHECKING:
    _ListGroupPoliciesPaginatorBase = AioPaginator[ListGroupPoliciesResponseTypeDef]
else:
    _ListGroupPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGroupPoliciesPaginator(_ListGroupPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroupPolicies.html#IAM.Paginator.ListGroupPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgrouppoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroupPolicies.html#IAM.Paginator.ListGroupPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgrouppoliciespaginator)
        """

if TYPE_CHECKING:
    _ListGroupsForUserPaginatorBase = AioPaginator[ListGroupsForUserResponseTypeDef]
else:
    _ListGroupsForUserPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGroupsForUserPaginator(_ListGroupsForUserPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroupsForUser.html#IAM.Paginator.ListGroupsForUser)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgroupsforuserpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupsForUserRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupsForUserResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroupsForUser.html#IAM.Paginator.ListGroupsForUser.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgroupsforuserpaginator)
        """

if TYPE_CHECKING:
    _ListGroupsPaginatorBase = AioPaginator[ListGroupsResponseTypeDef]
else:
    _ListGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGroupsPaginator(_ListGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroups.html#IAM.Paginator.ListGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroups.html#IAM.Paginator.ListGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgroupspaginator)
        """

if TYPE_CHECKING:
    _ListInstanceProfileTagsPaginatorBase = AioPaginator[ListInstanceProfileTagsResponseTypeDef]
else:
    _ListInstanceProfileTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInstanceProfileTagsPaginator(_ListInstanceProfileTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfileTags.html#IAM.Paginator.ListInstanceProfileTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofiletagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstanceProfileTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInstanceProfileTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfileTags.html#IAM.Paginator.ListInstanceProfileTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofiletagspaginator)
        """

if TYPE_CHECKING:
    _ListInstanceProfilesForRolePaginatorBase = AioPaginator[
        ListInstanceProfilesForRoleResponseTypeDef
    ]
else:
    _ListInstanceProfilesForRolePaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInstanceProfilesForRolePaginator(_ListInstanceProfilesForRolePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfilesForRole.html#IAM.Paginator.ListInstanceProfilesForRole)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofilesforrolepaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstanceProfilesForRoleRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInstanceProfilesForRoleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfilesForRole.html#IAM.Paginator.ListInstanceProfilesForRole.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofilesforrolepaginator)
        """

if TYPE_CHECKING:
    _ListInstanceProfilesPaginatorBase = AioPaginator[ListInstanceProfilesResponseTypeDef]
else:
    _ListInstanceProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInstanceProfilesPaginator(_ListInstanceProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfiles.html#IAM.Paginator.ListInstanceProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstanceProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInstanceProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfiles.html#IAM.Paginator.ListInstanceProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofilespaginator)
        """

if TYPE_CHECKING:
    _ListMFADeviceTagsPaginatorBase = AioPaginator[ListMFADeviceTagsResponseTypeDef]
else:
    _ListMFADeviceTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMFADeviceTagsPaginator(_ListMFADeviceTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListMFADeviceTags.html#IAM.Paginator.ListMFADeviceTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listmfadevicetagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMFADeviceTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMFADeviceTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListMFADeviceTags.html#IAM.Paginator.ListMFADeviceTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listmfadevicetagspaginator)
        """

if TYPE_CHECKING:
    _ListMFADevicesPaginatorBase = AioPaginator[ListMFADevicesResponseTypeDef]
else:
    _ListMFADevicesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMFADevicesPaginator(_ListMFADevicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListMFADevices.html#IAM.Paginator.ListMFADevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listmfadevicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMFADevicesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMFADevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListMFADevices.html#IAM.Paginator.ListMFADevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listmfadevicespaginator)
        """

if TYPE_CHECKING:
    _ListOpenIDConnectProviderTagsPaginatorBase = AioPaginator[
        ListOpenIDConnectProviderTagsResponseTypeDef
    ]
else:
    _ListOpenIDConnectProviderTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListOpenIDConnectProviderTagsPaginator(_ListOpenIDConnectProviderTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListOpenIDConnectProviderTags.html#IAM.Paginator.ListOpenIDConnectProviderTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listopenidconnectprovidertagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOpenIDConnectProviderTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOpenIDConnectProviderTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListOpenIDConnectProviderTags.html#IAM.Paginator.ListOpenIDConnectProviderTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listopenidconnectprovidertagspaginator)
        """

if TYPE_CHECKING:
    _ListPoliciesPaginatorBase = AioPaginator[ListPoliciesResponseTypeDef]
else:
    _ListPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPoliciesPaginator(_ListPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicies.html#IAM.Paginator.ListPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicies.html#IAM.Paginator.ListPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpoliciespaginator)
        """

if TYPE_CHECKING:
    _ListPolicyTagsPaginatorBase = AioPaginator[ListPolicyTagsResponseTypeDef]
else:
    _ListPolicyTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPolicyTagsPaginator(_ListPolicyTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicyTags.html#IAM.Paginator.ListPolicyTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpolicytagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPolicyTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPolicyTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicyTags.html#IAM.Paginator.ListPolicyTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpolicytagspaginator)
        """

if TYPE_CHECKING:
    _ListPolicyVersionsPaginatorBase = AioPaginator[ListPolicyVersionsResponseTypeDef]
else:
    _ListPolicyVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPolicyVersionsPaginator(_ListPolicyVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicyVersions.html#IAM.Paginator.ListPolicyVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpolicyversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPolicyVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPolicyVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicyVersions.html#IAM.Paginator.ListPolicyVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpolicyversionspaginator)
        """

if TYPE_CHECKING:
    _ListRolePoliciesPaginatorBase = AioPaginator[ListRolePoliciesResponseTypeDef]
else:
    _ListRolePoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRolePoliciesPaginator(_ListRolePoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRolePolicies.html#IAM.Paginator.ListRolePolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listrolepoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRolePoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRolePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRolePolicies.html#IAM.Paginator.ListRolePolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listrolepoliciespaginator)
        """

if TYPE_CHECKING:
    _ListRoleTagsPaginatorBase = AioPaginator[ListRoleTagsResponseTypeDef]
else:
    _ListRoleTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRoleTagsPaginator(_ListRoleTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRoleTags.html#IAM.Paginator.ListRoleTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listroletagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRoleTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRoleTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRoleTags.html#IAM.Paginator.ListRoleTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listroletagspaginator)
        """

if TYPE_CHECKING:
    _ListRolesPaginatorBase = AioPaginator[ListRolesResponseTypeDef]
else:
    _ListRolesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRolesPaginator(_ListRolesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRoles.html#IAM.Paginator.ListRoles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listrolespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRolesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRolesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRoles.html#IAM.Paginator.ListRoles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listrolespaginator)
        """

if TYPE_CHECKING:
    _ListSAMLProviderTagsPaginatorBase = AioPaginator[ListSAMLProviderTagsResponseTypeDef]
else:
    _ListSAMLProviderTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSAMLProviderTagsPaginator(_ListSAMLProviderTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSAMLProviderTags.html#IAM.Paginator.ListSAMLProviderTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsamlprovidertagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSAMLProviderTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSAMLProviderTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSAMLProviderTags.html#IAM.Paginator.ListSAMLProviderTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsamlprovidertagspaginator)
        """

if TYPE_CHECKING:
    _ListSSHPublicKeysPaginatorBase = AioPaginator[ListSSHPublicKeysResponseTypeDef]
else:
    _ListSSHPublicKeysPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSSHPublicKeysPaginator(_ListSSHPublicKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSSHPublicKeys.html#IAM.Paginator.ListSSHPublicKeys)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsshpublickeyspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSSHPublicKeysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSSHPublicKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSSHPublicKeys.html#IAM.Paginator.ListSSHPublicKeys.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsshpublickeyspaginator)
        """

if TYPE_CHECKING:
    _ListServerCertificateTagsPaginatorBase = AioPaginator[ListServerCertificateTagsResponseTypeDef]
else:
    _ListServerCertificateTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServerCertificateTagsPaginator(_ListServerCertificateTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListServerCertificateTags.html#IAM.Paginator.ListServerCertificateTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listservercertificatetagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServerCertificateTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServerCertificateTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListServerCertificateTags.html#IAM.Paginator.ListServerCertificateTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listservercertificatetagspaginator)
        """

if TYPE_CHECKING:
    _ListServerCertificatesPaginatorBase = AioPaginator[ListServerCertificatesResponseTypeDef]
else:
    _ListServerCertificatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServerCertificatesPaginator(_ListServerCertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListServerCertificates.html#IAM.Paginator.ListServerCertificates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listservercertificatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServerCertificatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServerCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListServerCertificates.html#IAM.Paginator.ListServerCertificates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listservercertificatespaginator)
        """

if TYPE_CHECKING:
    _ListSigningCertificatesPaginatorBase = AioPaginator[ListSigningCertificatesResponseTypeDef]
else:
    _ListSigningCertificatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSigningCertificatesPaginator(_ListSigningCertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSigningCertificates.html#IAM.Paginator.ListSigningCertificates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsigningcertificatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSigningCertificatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSigningCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSigningCertificates.html#IAM.Paginator.ListSigningCertificates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsigningcertificatespaginator)
        """

if TYPE_CHECKING:
    _ListUserPoliciesPaginatorBase = AioPaginator[ListUserPoliciesResponseTypeDef]
else:
    _ListUserPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUserPoliciesPaginator(_ListUserPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUserPolicies.html#IAM.Paginator.ListUserPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listuserpoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUserPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUserPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUserPolicies.html#IAM.Paginator.ListUserPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listuserpoliciespaginator)
        """

if TYPE_CHECKING:
    _ListUserTagsPaginatorBase = AioPaginator[ListUserTagsResponseTypeDef]
else:
    _ListUserTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUserTagsPaginator(_ListUserTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUserTags.html#IAM.Paginator.ListUserTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listusertagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUserTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUserTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUserTags.html#IAM.Paginator.ListUserTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listusertagspaginator)
        """

if TYPE_CHECKING:
    _ListUsersPaginatorBase = AioPaginator[ListUsersResponseTypeDef]
else:
    _ListUsersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUsersPaginator(_ListUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUsers.html#IAM.Paginator.ListUsers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUsers.html#IAM.Paginator.ListUsers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listuserspaginator)
        """

if TYPE_CHECKING:
    _ListVirtualMFADevicesPaginatorBase = AioPaginator[ListVirtualMFADevicesResponseTypeDef]
else:
    _ListVirtualMFADevicesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListVirtualMFADevicesPaginator(_ListVirtualMFADevicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListVirtualMFADevices.html#IAM.Paginator.ListVirtualMFADevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listvirtualmfadevicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVirtualMFADevicesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListVirtualMFADevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListVirtualMFADevices.html#IAM.Paginator.ListVirtualMFADevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listvirtualmfadevicespaginator)
        """

if TYPE_CHECKING:
    _SimulateCustomPolicyPaginatorBase = AioPaginator[SimulatePolicyResponseTypeDef]
else:
    _SimulateCustomPolicyPaginatorBase = AioPaginator  # type: ignore[assignment]

class SimulateCustomPolicyPaginator(_SimulateCustomPolicyPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/SimulateCustomPolicy.html#IAM.Paginator.SimulateCustomPolicy)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#simulatecustompolicypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SimulateCustomPolicyRequestPaginateTypeDef]
    ) -> AioPageIterator[SimulatePolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/SimulateCustomPolicy.html#IAM.Paginator.SimulateCustomPolicy.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#simulatecustompolicypaginator)
        """

if TYPE_CHECKING:
    _SimulatePrincipalPolicyPaginatorBase = AioPaginator[SimulatePolicyResponseTypeDef]
else:
    _SimulatePrincipalPolicyPaginatorBase = AioPaginator  # type: ignore[assignment]

class SimulatePrincipalPolicyPaginator(_SimulatePrincipalPolicyPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/SimulatePrincipalPolicy.html#IAM.Paginator.SimulatePrincipalPolicy)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#simulateprincipalpolicypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SimulatePrincipalPolicyRequestPaginateTypeDef]
    ) -> AioPageIterator[SimulatePolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/SimulatePrincipalPolicy.html#IAM.Paginator.SimulatePrincipalPolicy.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#simulateprincipalpolicypaginator)
        """
