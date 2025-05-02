"""
Type annotations for sso-admin service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sso_admin.client import SSOAdminClient

    session = Session()
    client: SSOAdminClient = session.client("sso-admin")
    ```
"""

from __future__ import annotations

import sys
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
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
from .type_defs import (
    AttachCustomerManagedPolicyReferenceToPermissionSetRequestTypeDef,
    AttachManagedPolicyToPermissionSetRequestTypeDef,
    CreateAccountAssignmentRequestTypeDef,
    CreateAccountAssignmentResponseTypeDef,
    CreateApplicationAssignmentRequestTypeDef,
    CreateApplicationRequestTypeDef,
    CreateApplicationResponseTypeDef,
    CreateInstanceAccessControlAttributeConfigurationRequestTypeDef,
    CreateInstanceRequestTypeDef,
    CreateInstanceResponseTypeDef,
    CreatePermissionSetRequestTypeDef,
    CreatePermissionSetResponseTypeDef,
    CreateTrustedTokenIssuerRequestTypeDef,
    CreateTrustedTokenIssuerResponseTypeDef,
    DeleteAccountAssignmentRequestTypeDef,
    DeleteAccountAssignmentResponseTypeDef,
    DeleteApplicationAccessScopeRequestTypeDef,
    DeleteApplicationAssignmentRequestTypeDef,
    DeleteApplicationAuthenticationMethodRequestTypeDef,
    DeleteApplicationGrantRequestTypeDef,
    DeleteApplicationRequestTypeDef,
    DeleteInlinePolicyFromPermissionSetRequestTypeDef,
    DeleteInstanceAccessControlAttributeConfigurationRequestTypeDef,
    DeleteInstanceRequestTypeDef,
    DeletePermissionsBoundaryFromPermissionSetRequestTypeDef,
    DeletePermissionSetRequestTypeDef,
    DeleteTrustedTokenIssuerRequestTypeDef,
    DescribeAccountAssignmentCreationStatusRequestTypeDef,
    DescribeAccountAssignmentCreationStatusResponseTypeDef,
    DescribeAccountAssignmentDeletionStatusRequestTypeDef,
    DescribeAccountAssignmentDeletionStatusResponseTypeDef,
    DescribeApplicationAssignmentRequestTypeDef,
    DescribeApplicationAssignmentResponseTypeDef,
    DescribeApplicationProviderRequestTypeDef,
    DescribeApplicationProviderResponseTypeDef,
    DescribeApplicationRequestTypeDef,
    DescribeApplicationResponseTypeDef,
    DescribeInstanceAccessControlAttributeConfigurationRequestTypeDef,
    DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef,
    DescribeInstanceRequestTypeDef,
    DescribeInstanceResponseTypeDef,
    DescribePermissionSetProvisioningStatusRequestTypeDef,
    DescribePermissionSetProvisioningStatusResponseTypeDef,
    DescribePermissionSetRequestTypeDef,
    DescribePermissionSetResponseTypeDef,
    DescribeTrustedTokenIssuerRequestTypeDef,
    DescribeTrustedTokenIssuerResponseTypeDef,
    DetachCustomerManagedPolicyReferenceFromPermissionSetRequestTypeDef,
    DetachManagedPolicyFromPermissionSetRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetApplicationAccessScopeRequestTypeDef,
    GetApplicationAccessScopeResponseTypeDef,
    GetApplicationAssignmentConfigurationRequestTypeDef,
    GetApplicationAssignmentConfigurationResponseTypeDef,
    GetApplicationAuthenticationMethodRequestTypeDef,
    GetApplicationAuthenticationMethodResponseTypeDef,
    GetApplicationGrantRequestTypeDef,
    GetApplicationGrantResponseTypeDef,
    GetInlinePolicyForPermissionSetRequestTypeDef,
    GetInlinePolicyForPermissionSetResponseTypeDef,
    GetPermissionsBoundaryForPermissionSetRequestTypeDef,
    GetPermissionsBoundaryForPermissionSetResponseTypeDef,
    ListAccountAssignmentCreationStatusRequestTypeDef,
    ListAccountAssignmentCreationStatusResponseTypeDef,
    ListAccountAssignmentDeletionStatusRequestTypeDef,
    ListAccountAssignmentDeletionStatusResponseTypeDef,
    ListAccountAssignmentsForPrincipalRequestTypeDef,
    ListAccountAssignmentsForPrincipalResponseTypeDef,
    ListAccountAssignmentsRequestTypeDef,
    ListAccountAssignmentsResponseTypeDef,
    ListAccountsForProvisionedPermissionSetRequestTypeDef,
    ListAccountsForProvisionedPermissionSetResponseTypeDef,
    ListApplicationAccessScopesRequestTypeDef,
    ListApplicationAccessScopesResponseTypeDef,
    ListApplicationAssignmentsForPrincipalRequestTypeDef,
    ListApplicationAssignmentsForPrincipalResponseTypeDef,
    ListApplicationAssignmentsRequestTypeDef,
    ListApplicationAssignmentsResponseTypeDef,
    ListApplicationAuthenticationMethodsRequestTypeDef,
    ListApplicationAuthenticationMethodsResponseTypeDef,
    ListApplicationGrantsRequestTypeDef,
    ListApplicationGrantsResponseTypeDef,
    ListApplicationProvidersRequestTypeDef,
    ListApplicationProvidersResponseTypeDef,
    ListApplicationsRequestTypeDef,
    ListApplicationsResponseTypeDef,
    ListCustomerManagedPolicyReferencesInPermissionSetRequestTypeDef,
    ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef,
    ListInstancesRequestTypeDef,
    ListInstancesResponseTypeDef,
    ListManagedPoliciesInPermissionSetRequestTypeDef,
    ListManagedPoliciesInPermissionSetResponseTypeDef,
    ListPermissionSetProvisioningStatusRequestTypeDef,
    ListPermissionSetProvisioningStatusResponseTypeDef,
    ListPermissionSetsProvisionedToAccountRequestTypeDef,
    ListPermissionSetsProvisionedToAccountResponseTypeDef,
    ListPermissionSetsRequestTypeDef,
    ListPermissionSetsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrustedTokenIssuersRequestTypeDef,
    ListTrustedTokenIssuersResponseTypeDef,
    ProvisionPermissionSetRequestTypeDef,
    ProvisionPermissionSetResponseTypeDef,
    PutApplicationAccessScopeRequestTypeDef,
    PutApplicationAssignmentConfigurationRequestTypeDef,
    PutApplicationAuthenticationMethodRequestTypeDef,
    PutApplicationGrantRequestTypeDef,
    PutInlinePolicyToPermissionSetRequestTypeDef,
    PutPermissionsBoundaryToPermissionSetRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateApplicationRequestTypeDef,
    UpdateInstanceAccessControlAttributeConfigurationRequestTypeDef,
    UpdateInstanceRequestTypeDef,
    UpdatePermissionSetRequestTypeDef,
    UpdateTrustedTokenIssuerRequestTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("SSOAdminClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class SSOAdminClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SSOAdminClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#generate_presigned_url)
        """

    def attach_customer_managed_policy_reference_to_permission_set(
        self, **kwargs: Unpack[AttachCustomerManagedPolicyReferenceToPermissionSetRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Attaches the specified customer managed policy to the specified
        <a>PermissionSet</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/attach_customer_managed_policy_reference_to_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#attach_customer_managed_policy_reference_to_permission_set)
        """

    def attach_managed_policy_to_permission_set(
        self, **kwargs: Unpack[AttachManagedPolicyToPermissionSetRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Attaches an Amazon Web Services managed policy ARN to a permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/attach_managed_policy_to_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#attach_managed_policy_to_permission_set)
        """

    def create_account_assignment(
        self, **kwargs: Unpack[CreateAccountAssignmentRequestTypeDef]
    ) -> CreateAccountAssignmentResponseTypeDef:
        """
        Assigns access to a principal for a specified Amazon Web Services account using
        a specified permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/create_account_assignment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#create_account_assignment)
        """

    def create_application(
        self, **kwargs: Unpack[CreateApplicationRequestTypeDef]
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates an application in IAM Identity Center for the given application
        provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/create_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#create_application)
        """

    def create_application_assignment(
        self, **kwargs: Unpack[CreateApplicationAssignmentRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Grant application access to a user or group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/create_application_assignment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#create_application_assignment)
        """

    def create_instance(
        self, **kwargs: Unpack[CreateInstanceRequestTypeDef]
    ) -> CreateInstanceResponseTypeDef:
        """
        Creates an instance of IAM Identity Center for a standalone Amazon Web Services
        account that is not managed by Organizations or a member Amazon Web Services
        account in an organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/create_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#create_instance)
        """

    def create_instance_access_control_attribute_configuration(
        self, **kwargs: Unpack[CreateInstanceAccessControlAttributeConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enables the attributes-based access control (ABAC) feature for the specified
        IAM Identity Center instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/create_instance_access_control_attribute_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#create_instance_access_control_attribute_configuration)
        """

    def create_permission_set(
        self, **kwargs: Unpack[CreatePermissionSetRequestTypeDef]
    ) -> CreatePermissionSetResponseTypeDef:
        """
        Creates a permission set within a specified IAM Identity Center instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/create_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#create_permission_set)
        """

    def create_trusted_token_issuer(
        self, **kwargs: Unpack[CreateTrustedTokenIssuerRequestTypeDef]
    ) -> CreateTrustedTokenIssuerResponseTypeDef:
        """
        Creates a connection to a trusted token issuer in an instance of IAM Identity
        Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/create_trusted_token_issuer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#create_trusted_token_issuer)
        """

    def delete_account_assignment(
        self, **kwargs: Unpack[DeleteAccountAssignmentRequestTypeDef]
    ) -> DeleteAccountAssignmentResponseTypeDef:
        """
        Deletes a principal's access from a specified Amazon Web Services account using
        a specified permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/delete_account_assignment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#delete_account_assignment)
        """

    def delete_application(
        self, **kwargs: Unpack[DeleteApplicationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the association with the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/delete_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#delete_application)
        """

    def delete_application_access_scope(
        self, **kwargs: Unpack[DeleteApplicationAccessScopeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an IAM Identity Center access scope from an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/delete_application_access_scope.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#delete_application_access_scope)
        """

    def delete_application_assignment(
        self, **kwargs: Unpack[DeleteApplicationAssignmentRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Revoke application access to an application by deleting application assignments
        for a user or group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/delete_application_assignment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#delete_application_assignment)
        """

    def delete_application_authentication_method(
        self, **kwargs: Unpack[DeleteApplicationAuthenticationMethodRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an authentication method from an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/delete_application_authentication_method.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#delete_application_authentication_method)
        """

    def delete_application_grant(
        self, **kwargs: Unpack[DeleteApplicationGrantRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a grant from an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/delete_application_grant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#delete_application_grant)
        """

    def delete_inline_policy_from_permission_set(
        self, **kwargs: Unpack[DeleteInlinePolicyFromPermissionSetRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the inline policy from a specified permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/delete_inline_policy_from_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#delete_inline_policy_from_permission_set)
        """

    def delete_instance(self, **kwargs: Unpack[DeleteInstanceRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the instance of IAM Identity Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/delete_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#delete_instance)
        """

    def delete_instance_access_control_attribute_configuration(
        self, **kwargs: Unpack[DeleteInstanceAccessControlAttributeConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disables the attributes-based access control (ABAC) feature for the specified
        IAM Identity Center instance and deletes all of the attribute mappings that
        have been configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/delete_instance_access_control_attribute_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#delete_instance_access_control_attribute_configuration)
        """

    def delete_permission_set(
        self, **kwargs: Unpack[DeletePermissionSetRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/delete_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#delete_permission_set)
        """

    def delete_permissions_boundary_from_permission_set(
        self, **kwargs: Unpack[DeletePermissionsBoundaryFromPermissionSetRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the permissions boundary from a specified <a>PermissionSet</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/delete_permissions_boundary_from_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#delete_permissions_boundary_from_permission_set)
        """

    def delete_trusted_token_issuer(
        self, **kwargs: Unpack[DeleteTrustedTokenIssuerRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a trusted token issuer configuration from an instance of IAM Identity
        Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/delete_trusted_token_issuer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#delete_trusted_token_issuer)
        """

    def describe_account_assignment_creation_status(
        self, **kwargs: Unpack[DescribeAccountAssignmentCreationStatusRequestTypeDef]
    ) -> DescribeAccountAssignmentCreationStatusResponseTypeDef:
        """
        Describes the status of the assignment creation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/describe_account_assignment_creation_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#describe_account_assignment_creation_status)
        """

    def describe_account_assignment_deletion_status(
        self, **kwargs: Unpack[DescribeAccountAssignmentDeletionStatusRequestTypeDef]
    ) -> DescribeAccountAssignmentDeletionStatusResponseTypeDef:
        """
        Describes the status of the assignment deletion request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/describe_account_assignment_deletion_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#describe_account_assignment_deletion_status)
        """

    def describe_application(
        self, **kwargs: Unpack[DescribeApplicationRequestTypeDef]
    ) -> DescribeApplicationResponseTypeDef:
        """
        Retrieves the details of an application associated with an instance of IAM
        Identity Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/describe_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#describe_application)
        """

    def describe_application_assignment(
        self, **kwargs: Unpack[DescribeApplicationAssignmentRequestTypeDef]
    ) -> DescribeApplicationAssignmentResponseTypeDef:
        """
        Retrieves a direct assignment of a user or group to an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/describe_application_assignment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#describe_application_assignment)
        """

    def describe_application_provider(
        self, **kwargs: Unpack[DescribeApplicationProviderRequestTypeDef]
    ) -> DescribeApplicationProviderResponseTypeDef:
        """
        Retrieves details about a provider that can be used to connect an Amazon Web
        Services managed application or customer managed application to IAM Identity
        Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/describe_application_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#describe_application_provider)
        """

    def describe_instance(
        self, **kwargs: Unpack[DescribeInstanceRequestTypeDef]
    ) -> DescribeInstanceResponseTypeDef:
        """
        Returns the details of an instance of IAM Identity Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/describe_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#describe_instance)
        """

    def describe_instance_access_control_attribute_configuration(
        self, **kwargs: Unpack[DescribeInstanceAccessControlAttributeConfigurationRequestTypeDef]
    ) -> DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef:
        """
        Returns the list of IAM Identity Center identity store attributes that have
        been configured to work with attributes-based access control (ABAC) for the
        specified IAM Identity Center instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/describe_instance_access_control_attribute_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#describe_instance_access_control_attribute_configuration)
        """

    def describe_permission_set(
        self, **kwargs: Unpack[DescribePermissionSetRequestTypeDef]
    ) -> DescribePermissionSetResponseTypeDef:
        """
        Gets the details of the permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/describe_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#describe_permission_set)
        """

    def describe_permission_set_provisioning_status(
        self, **kwargs: Unpack[DescribePermissionSetProvisioningStatusRequestTypeDef]
    ) -> DescribePermissionSetProvisioningStatusResponseTypeDef:
        """
        Describes the status for the given permission set provisioning request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/describe_permission_set_provisioning_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#describe_permission_set_provisioning_status)
        """

    def describe_trusted_token_issuer(
        self, **kwargs: Unpack[DescribeTrustedTokenIssuerRequestTypeDef]
    ) -> DescribeTrustedTokenIssuerResponseTypeDef:
        """
        Retrieves details about a trusted token issuer configuration stored in an
        instance of IAM Identity Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/describe_trusted_token_issuer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#describe_trusted_token_issuer)
        """

    def detach_customer_managed_policy_reference_from_permission_set(
        self, **kwargs: Unpack[DetachCustomerManagedPolicyReferenceFromPermissionSetRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Detaches the specified customer managed policy from the specified
        <a>PermissionSet</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/detach_customer_managed_policy_reference_from_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#detach_customer_managed_policy_reference_from_permission_set)
        """

    def detach_managed_policy_from_permission_set(
        self, **kwargs: Unpack[DetachManagedPolicyFromPermissionSetRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Detaches the attached Amazon Web Services managed policy ARN from the specified
        permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/detach_managed_policy_from_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#detach_managed_policy_from_permission_set)
        """

    def get_application_access_scope(
        self, **kwargs: Unpack[GetApplicationAccessScopeRequestTypeDef]
    ) -> GetApplicationAccessScopeResponseTypeDef:
        """
        Retrieves the authorized targets for an IAM Identity Center access scope for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_application_access_scope.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_application_access_scope)
        """

    def get_application_assignment_configuration(
        self, **kwargs: Unpack[GetApplicationAssignmentConfigurationRequestTypeDef]
    ) -> GetApplicationAssignmentConfigurationResponseTypeDef:
        """
        Retrieves the configuration of <a>PutApplicationAssignmentConfiguration</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_application_assignment_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_application_assignment_configuration)
        """

    def get_application_authentication_method(
        self, **kwargs: Unpack[GetApplicationAuthenticationMethodRequestTypeDef]
    ) -> GetApplicationAuthenticationMethodResponseTypeDef:
        """
        Retrieves details about an authentication method used by an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_application_authentication_method.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_application_authentication_method)
        """

    def get_application_grant(
        self, **kwargs: Unpack[GetApplicationGrantRequestTypeDef]
    ) -> GetApplicationGrantResponseTypeDef:
        """
        Retrieves details about an application grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_application_grant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_application_grant)
        """

    def get_inline_policy_for_permission_set(
        self, **kwargs: Unpack[GetInlinePolicyForPermissionSetRequestTypeDef]
    ) -> GetInlinePolicyForPermissionSetResponseTypeDef:
        """
        Obtains the inline policy assigned to the permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_inline_policy_for_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_inline_policy_for_permission_set)
        """

    def get_permissions_boundary_for_permission_set(
        self, **kwargs: Unpack[GetPermissionsBoundaryForPermissionSetRequestTypeDef]
    ) -> GetPermissionsBoundaryForPermissionSetResponseTypeDef:
        """
        Obtains the permissions boundary for a specified <a>PermissionSet</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_permissions_boundary_for_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_permissions_boundary_for_permission_set)
        """

    def list_account_assignment_creation_status(
        self, **kwargs: Unpack[ListAccountAssignmentCreationStatusRequestTypeDef]
    ) -> ListAccountAssignmentCreationStatusResponseTypeDef:
        """
        Lists the status of the Amazon Web Services account assignment creation
        requests for a specified IAM Identity Center instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_account_assignment_creation_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_account_assignment_creation_status)
        """

    def list_account_assignment_deletion_status(
        self, **kwargs: Unpack[ListAccountAssignmentDeletionStatusRequestTypeDef]
    ) -> ListAccountAssignmentDeletionStatusResponseTypeDef:
        """
        Lists the status of the Amazon Web Services account assignment deletion
        requests for a specified IAM Identity Center instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_account_assignment_deletion_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_account_assignment_deletion_status)
        """

    def list_account_assignments(
        self, **kwargs: Unpack[ListAccountAssignmentsRequestTypeDef]
    ) -> ListAccountAssignmentsResponseTypeDef:
        """
        Lists the assignee of the specified Amazon Web Services account with the
        specified permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_account_assignments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_account_assignments)
        """

    def list_account_assignments_for_principal(
        self, **kwargs: Unpack[ListAccountAssignmentsForPrincipalRequestTypeDef]
    ) -> ListAccountAssignmentsForPrincipalResponseTypeDef:
        """
        Retrieves a list of the IAM Identity Center associated Amazon Web Services
        accounts that the principal has access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_account_assignments_for_principal.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_account_assignments_for_principal)
        """

    def list_accounts_for_provisioned_permission_set(
        self, **kwargs: Unpack[ListAccountsForProvisionedPermissionSetRequestTypeDef]
    ) -> ListAccountsForProvisionedPermissionSetResponseTypeDef:
        """
        Lists all the Amazon Web Services accounts where the specified permission set
        is provisioned.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_accounts_for_provisioned_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_accounts_for_provisioned_permission_set)
        """

    def list_application_access_scopes(
        self, **kwargs: Unpack[ListApplicationAccessScopesRequestTypeDef]
    ) -> ListApplicationAccessScopesResponseTypeDef:
        """
        Lists the access scopes and authorized targets associated with an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_application_access_scopes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_application_access_scopes)
        """

    def list_application_assignments(
        self, **kwargs: Unpack[ListApplicationAssignmentsRequestTypeDef]
    ) -> ListApplicationAssignmentsResponseTypeDef:
        """
        Lists Amazon Web Services account users that are assigned to an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_application_assignments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_application_assignments)
        """

    def list_application_assignments_for_principal(
        self, **kwargs: Unpack[ListApplicationAssignmentsForPrincipalRequestTypeDef]
    ) -> ListApplicationAssignmentsForPrincipalResponseTypeDef:
        """
        Lists the applications to which a specified principal is assigned.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_application_assignments_for_principal.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_application_assignments_for_principal)
        """

    def list_application_authentication_methods(
        self, **kwargs: Unpack[ListApplicationAuthenticationMethodsRequestTypeDef]
    ) -> ListApplicationAuthenticationMethodsResponseTypeDef:
        """
        Lists all of the authentication methods supported by the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_application_authentication_methods.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_application_authentication_methods)
        """

    def list_application_grants(
        self, **kwargs: Unpack[ListApplicationGrantsRequestTypeDef]
    ) -> ListApplicationGrantsResponseTypeDef:
        """
        List the grants associated with an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_application_grants.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_application_grants)
        """

    def list_application_providers(
        self, **kwargs: Unpack[ListApplicationProvidersRequestTypeDef]
    ) -> ListApplicationProvidersResponseTypeDef:
        """
        Lists the application providers configured in the IAM Identity Center identity
        store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_application_providers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_application_providers)
        """

    def list_applications(
        self, **kwargs: Unpack[ListApplicationsRequestTypeDef]
    ) -> ListApplicationsResponseTypeDef:
        """
        Lists all applications associated with the instance of IAM Identity Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_applications.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_applications)
        """

    def list_customer_managed_policy_references_in_permission_set(
        self, **kwargs: Unpack[ListCustomerManagedPolicyReferencesInPermissionSetRequestTypeDef]
    ) -> ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef:
        """
        Lists all customer managed policies attached to a specified
        <a>PermissionSet</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_customer_managed_policy_references_in_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_customer_managed_policy_references_in_permission_set)
        """

    def list_instances(
        self, **kwargs: Unpack[ListInstancesRequestTypeDef]
    ) -> ListInstancesResponseTypeDef:
        """
        Lists the details of the organization and account instances of IAM Identity
        Center that were created in or visible to the account calling this API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_instances)
        """

    def list_managed_policies_in_permission_set(
        self, **kwargs: Unpack[ListManagedPoliciesInPermissionSetRequestTypeDef]
    ) -> ListManagedPoliciesInPermissionSetResponseTypeDef:
        """
        Lists the Amazon Web Services managed policy that is attached to a specified
        permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_managed_policies_in_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_managed_policies_in_permission_set)
        """

    def list_permission_set_provisioning_status(
        self, **kwargs: Unpack[ListPermissionSetProvisioningStatusRequestTypeDef]
    ) -> ListPermissionSetProvisioningStatusResponseTypeDef:
        """
        Lists the status of the permission set provisioning requests for a specified
        IAM Identity Center instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_permission_set_provisioning_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_permission_set_provisioning_status)
        """

    def list_permission_sets(
        self, **kwargs: Unpack[ListPermissionSetsRequestTypeDef]
    ) -> ListPermissionSetsResponseTypeDef:
        """
        Lists the <a>PermissionSet</a>s in an IAM Identity Center instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_permission_sets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_permission_sets)
        """

    def list_permission_sets_provisioned_to_account(
        self, **kwargs: Unpack[ListPermissionSetsProvisionedToAccountRequestTypeDef]
    ) -> ListPermissionSetsProvisionedToAccountResponseTypeDef:
        """
        Lists all the permission sets that are provisioned to a specified Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_permission_sets_provisioned_to_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_permission_sets_provisioned_to_account)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags that are attached to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_tags_for_resource)
        """

    def list_trusted_token_issuers(
        self, **kwargs: Unpack[ListTrustedTokenIssuersRequestTypeDef]
    ) -> ListTrustedTokenIssuersResponseTypeDef:
        """
        Lists all the trusted token issuers configured in an instance of IAM Identity
        Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/list_trusted_token_issuers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#list_trusted_token_issuers)
        """

    def provision_permission_set(
        self, **kwargs: Unpack[ProvisionPermissionSetRequestTypeDef]
    ) -> ProvisionPermissionSetResponseTypeDef:
        """
        The process by which a specified permission set is provisioned to the specified
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/provision_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#provision_permission_set)
        """

    def put_application_access_scope(
        self, **kwargs: Unpack[PutApplicationAccessScopeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates the list of authorized targets for an IAM Identity Center
        access scope for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/put_application_access_scope.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#put_application_access_scope)
        """

    def put_application_assignment_configuration(
        self, **kwargs: Unpack[PutApplicationAssignmentConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Configure how users gain access to an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/put_application_assignment_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#put_application_assignment_configuration)
        """

    def put_application_authentication_method(
        self, **kwargs: Unpack[PutApplicationAuthenticationMethodRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates an authentication method for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/put_application_authentication_method.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#put_application_authentication_method)
        """

    def put_application_grant(
        self, **kwargs: Unpack[PutApplicationGrantRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds a grant to an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/put_application_grant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#put_application_grant)
        """

    def put_inline_policy_to_permission_set(
        self, **kwargs: Unpack[PutInlinePolicyToPermissionSetRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Attaches an inline policy to a permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/put_inline_policy_to_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#put_inline_policy_to_permission_set)
        """

    def put_permissions_boundary_to_permission_set(
        self, **kwargs: Unpack[PutPermissionsBoundaryToPermissionSetRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Attaches an Amazon Web Services managed or customer managed policy to the
        specified <a>PermissionSet</a> as a permissions boundary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/put_permissions_boundary_to_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#put_permissions_boundary_to_permission_set)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates a set of tags with a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Disassociates a set of tags from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#untag_resource)
        """

    def update_application(
        self, **kwargs: Unpack[UpdateApplicationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates application properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/update_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#update_application)
        """

    def update_instance(self, **kwargs: Unpack[UpdateInstanceRequestTypeDef]) -> Dict[str, Any]:
        """
        Update the details for the instance of IAM Identity Center that is owned by the
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/update_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#update_instance)
        """

    def update_instance_access_control_attribute_configuration(
        self, **kwargs: Unpack[UpdateInstanceAccessControlAttributeConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the IAM Identity Center identity store attributes that you can use with
        the IAM Identity Center instance for attributes-based access control (ABAC).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/update_instance_access_control_attribute_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#update_instance_access_control_attribute_configuration)
        """

    def update_permission_set(
        self, **kwargs: Unpack[UpdatePermissionSetRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an existing permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/update_permission_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#update_permission_set)
        """

    def update_trusted_token_issuer(
        self, **kwargs: Unpack[UpdateTrustedTokenIssuerRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the name of the trusted token issuer, or the path of a source attribute
        or destination attribute for a trusted token issuer configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/update_trusted_token_issuer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#update_trusted_token_issuer)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_account_assignment_creation_status"]
    ) -> ListAccountAssignmentCreationStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_account_assignment_deletion_status"]
    ) -> ListAccountAssignmentDeletionStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_account_assignments_for_principal"]
    ) -> ListAccountAssignmentsForPrincipalPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_account_assignments"]
    ) -> ListAccountAssignmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_accounts_for_provisioned_permission_set"]
    ) -> ListAccountsForProvisionedPermissionSetPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_application_access_scopes"]
    ) -> ListApplicationAccessScopesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_application_assignments_for_principal"]
    ) -> ListApplicationAssignmentsForPrincipalPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_application_assignments"]
    ) -> ListApplicationAssignmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_application_authentication_methods"]
    ) -> ListApplicationAuthenticationMethodsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_application_grants"]
    ) -> ListApplicationGrantsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_application_providers"]
    ) -> ListApplicationProvidersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_customer_managed_policy_references_in_permission_set"]
    ) -> ListCustomerManagedPolicyReferencesInPermissionSetPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_instances"]
    ) -> ListInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_managed_policies_in_permission_set"]
    ) -> ListManagedPoliciesInPermissionSetPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_permission_set_provisioning_status"]
    ) -> ListPermissionSetProvisioningStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_permission_sets"]
    ) -> ListPermissionSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_permission_sets_provisioned_to_account"]
    ) -> ListPermissionSetsProvisionedToAccountPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_trusted_token_issuers"]
    ) -> ListTrustedTokenIssuersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/client/#get_paginator)
        """
