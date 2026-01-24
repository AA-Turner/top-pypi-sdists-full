"""
Type annotations for sso-admin service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_admin/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_sso_admin.type_defs import AccessControlAttributeValueOutputTypeDef

    data: AccessControlAttributeValueOutputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import (
    ApplicationStatusType,
    ApplicationVisibilityType,
    FederationProtocolType,
    GrantTypeType,
    InstanceAccessControlAttributeConfigurationStatusType,
    InstanceStatusType,
    KmsKeyStatusType,
    KmsKeyTypeType,
    PrincipalTypeType,
    ProvisioningStatusType,
    ProvisionTargetTypeType,
    SignInOriginType,
    StatusValuesType,
    UserBackgroundSessionApplicationStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccessControlAttributeOutputTypeDef",
    "AccessControlAttributeTypeDef",
    "AccessControlAttributeValueOutputTypeDef",
    "AccessControlAttributeValueTypeDef",
    "AccountAssignmentForPrincipalTypeDef",
    "AccountAssignmentOperationStatusMetadataTypeDef",
    "AccountAssignmentOperationStatusTypeDef",
    "AccountAssignmentTypeDef",
    "ApplicationAssignmentForPrincipalTypeDef",
    "ApplicationAssignmentTypeDef",
    "ApplicationProviderTypeDef",
    "ApplicationTypeDef",
    "AttachCustomerManagedPolicyReferenceToPermissionSetRequestTypeDef",
    "AttachManagedPolicyToPermissionSetRequestTypeDef",
    "AttachedManagedPolicyTypeDef",
    "AuthenticationMethodItemTypeDef",
    "AuthenticationMethodOutputTypeDef",
    "AuthenticationMethodTypeDef",
    "AuthenticationMethodUnionTypeDef",
    "AuthorizationCodeGrantOutputTypeDef",
    "AuthorizationCodeGrantTypeDef",
    "AuthorizedTokenIssuerOutputTypeDef",
    "AuthorizedTokenIssuerTypeDef",
    "CreateAccountAssignmentRequestTypeDef",
    "CreateAccountAssignmentResponseTypeDef",
    "CreateApplicationAssignmentRequestTypeDef",
    "CreateApplicationRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateInstanceAccessControlAttributeConfigurationRequestTypeDef",
    "CreateInstanceRequestTypeDef",
    "CreateInstanceResponseTypeDef",
    "CreatePermissionSetRequestTypeDef",
    "CreatePermissionSetResponseTypeDef",
    "CreateTrustedTokenIssuerRequestTypeDef",
    "CreateTrustedTokenIssuerResponseTypeDef",
    "CustomerManagedPolicyReferenceTypeDef",
    "DeleteAccountAssignmentRequestTypeDef",
    "DeleteAccountAssignmentResponseTypeDef",
    "DeleteApplicationAccessScopeRequestTypeDef",
    "DeleteApplicationAssignmentRequestTypeDef",
    "DeleteApplicationAuthenticationMethodRequestTypeDef",
    "DeleteApplicationGrantRequestTypeDef",
    "DeleteApplicationRequestTypeDef",
    "DeleteInlinePolicyFromPermissionSetRequestTypeDef",
    "DeleteInstanceAccessControlAttributeConfigurationRequestTypeDef",
    "DeleteInstanceRequestTypeDef",
    "DeletePermissionSetRequestTypeDef",
    "DeletePermissionsBoundaryFromPermissionSetRequestTypeDef",
    "DeleteTrustedTokenIssuerRequestTypeDef",
    "DescribeAccountAssignmentCreationStatusRequestTypeDef",
    "DescribeAccountAssignmentCreationStatusResponseTypeDef",
    "DescribeAccountAssignmentDeletionStatusRequestTypeDef",
    "DescribeAccountAssignmentDeletionStatusResponseTypeDef",
    "DescribeApplicationAssignmentRequestTypeDef",
    "DescribeApplicationAssignmentResponseTypeDef",
    "DescribeApplicationProviderRequestTypeDef",
    "DescribeApplicationProviderResponseTypeDef",
    "DescribeApplicationRequestTypeDef",
    "DescribeApplicationResponseTypeDef",
    "DescribeInstanceAccessControlAttributeConfigurationRequestTypeDef",
    "DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef",
    "DescribeInstanceRequestTypeDef",
    "DescribeInstanceResponseTypeDef",
    "DescribePermissionSetProvisioningStatusRequestTypeDef",
    "DescribePermissionSetProvisioningStatusResponseTypeDef",
    "DescribePermissionSetRequestTypeDef",
    "DescribePermissionSetResponseTypeDef",
    "DescribeTrustedTokenIssuerRequestTypeDef",
    "DescribeTrustedTokenIssuerResponseTypeDef",
    "DetachCustomerManagedPolicyReferenceFromPermissionSetRequestTypeDef",
    "DetachManagedPolicyFromPermissionSetRequestTypeDef",
    "DisplayDataTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionConfigurationDetailsTypeDef",
    "EncryptionConfigurationTypeDef",
    "GetApplicationAccessScopeRequestTypeDef",
    "GetApplicationAccessScopeResponseTypeDef",
    "GetApplicationAssignmentConfigurationRequestTypeDef",
    "GetApplicationAssignmentConfigurationResponseTypeDef",
    "GetApplicationAuthenticationMethodRequestTypeDef",
    "GetApplicationAuthenticationMethodResponseTypeDef",
    "GetApplicationGrantRequestTypeDef",
    "GetApplicationGrantResponseTypeDef",
    "GetApplicationSessionConfigurationRequestTypeDef",
    "GetApplicationSessionConfigurationResponseTypeDef",
    "GetInlinePolicyForPermissionSetRequestTypeDef",
    "GetInlinePolicyForPermissionSetResponseTypeDef",
    "GetPermissionsBoundaryForPermissionSetRequestTypeDef",
    "GetPermissionsBoundaryForPermissionSetResponseTypeDef",
    "GrantItemTypeDef",
    "GrantOutputTypeDef",
    "GrantTypeDef",
    "GrantUnionTypeDef",
    "IamAuthenticationMethodOutputTypeDef",
    "IamAuthenticationMethodTypeDef",
    "InstanceAccessControlAttributeConfigurationOutputTypeDef",
    "InstanceAccessControlAttributeConfigurationTypeDef",
    "InstanceAccessControlAttributeConfigurationUnionTypeDef",
    "InstanceMetadataTypeDef",
    "JwtBearerGrantOutputTypeDef",
    "JwtBearerGrantTypeDef",
    "ListAccountAssignmentCreationStatusRequestPaginateTypeDef",
    "ListAccountAssignmentCreationStatusRequestTypeDef",
    "ListAccountAssignmentCreationStatusResponseTypeDef",
    "ListAccountAssignmentDeletionStatusRequestPaginateTypeDef",
    "ListAccountAssignmentDeletionStatusRequestTypeDef",
    "ListAccountAssignmentDeletionStatusResponseTypeDef",
    "ListAccountAssignmentsFilterTypeDef",
    "ListAccountAssignmentsForPrincipalRequestPaginateTypeDef",
    "ListAccountAssignmentsForPrincipalRequestTypeDef",
    "ListAccountAssignmentsForPrincipalResponseTypeDef",
    "ListAccountAssignmentsRequestPaginateTypeDef",
    "ListAccountAssignmentsRequestTypeDef",
    "ListAccountAssignmentsResponseTypeDef",
    "ListAccountsForProvisionedPermissionSetRequestPaginateTypeDef",
    "ListAccountsForProvisionedPermissionSetRequestTypeDef",
    "ListAccountsForProvisionedPermissionSetResponseTypeDef",
    "ListApplicationAccessScopesRequestPaginateTypeDef",
    "ListApplicationAccessScopesRequestTypeDef",
    "ListApplicationAccessScopesResponseTypeDef",
    "ListApplicationAssignmentsFilterTypeDef",
    "ListApplicationAssignmentsForPrincipalRequestPaginateTypeDef",
    "ListApplicationAssignmentsForPrincipalRequestTypeDef",
    "ListApplicationAssignmentsForPrincipalResponseTypeDef",
    "ListApplicationAssignmentsRequestPaginateTypeDef",
    "ListApplicationAssignmentsRequestTypeDef",
    "ListApplicationAssignmentsResponseTypeDef",
    "ListApplicationAuthenticationMethodsRequestPaginateTypeDef",
    "ListApplicationAuthenticationMethodsRequestTypeDef",
    "ListApplicationAuthenticationMethodsResponseTypeDef",
    "ListApplicationGrantsRequestPaginateTypeDef",
    "ListApplicationGrantsRequestTypeDef",
    "ListApplicationGrantsResponseTypeDef",
    "ListApplicationProvidersRequestPaginateTypeDef",
    "ListApplicationProvidersRequestTypeDef",
    "ListApplicationProvidersResponseTypeDef",
    "ListApplicationsFilterTypeDef",
    "ListApplicationsRequestPaginateTypeDef",
    "ListApplicationsRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListCustomerManagedPolicyReferencesInPermissionSetRequestPaginateTypeDef",
    "ListCustomerManagedPolicyReferencesInPermissionSetRequestTypeDef",
    "ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef",
    "ListInstancesRequestPaginateTypeDef",
    "ListInstancesRequestTypeDef",
    "ListInstancesResponseTypeDef",
    "ListManagedPoliciesInPermissionSetRequestPaginateTypeDef",
    "ListManagedPoliciesInPermissionSetRequestTypeDef",
    "ListManagedPoliciesInPermissionSetResponseTypeDef",
    "ListPermissionSetProvisioningStatusRequestPaginateTypeDef",
    "ListPermissionSetProvisioningStatusRequestTypeDef",
    "ListPermissionSetProvisioningStatusResponseTypeDef",
    "ListPermissionSetsProvisionedToAccountRequestPaginateTypeDef",
    "ListPermissionSetsProvisionedToAccountRequestTypeDef",
    "ListPermissionSetsProvisionedToAccountResponseTypeDef",
    "ListPermissionSetsRequestPaginateTypeDef",
    "ListPermissionSetsRequestTypeDef",
    "ListPermissionSetsResponseTypeDef",
    "ListTagsForResourceRequestPaginateTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTrustedTokenIssuersRequestPaginateTypeDef",
    "ListTrustedTokenIssuersRequestTypeDef",
    "ListTrustedTokenIssuersResponseTypeDef",
    "OidcJwtConfigurationTypeDef",
    "OidcJwtUpdateConfigurationTypeDef",
    "OperationStatusFilterTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionSetProvisioningStatusMetadataTypeDef",
    "PermissionSetProvisioningStatusTypeDef",
    "PermissionSetTypeDef",
    "PermissionsBoundaryTypeDef",
    "PortalOptionsTypeDef",
    "ProvisionPermissionSetRequestTypeDef",
    "ProvisionPermissionSetResponseTypeDef",
    "PutApplicationAccessScopeRequestTypeDef",
    "PutApplicationAssignmentConfigurationRequestTypeDef",
    "PutApplicationAuthenticationMethodRequestTypeDef",
    "PutApplicationGrantRequestTypeDef",
    "PutApplicationSessionConfigurationRequestTypeDef",
    "PutInlinePolicyToPermissionSetRequestTypeDef",
    "PutPermissionsBoundaryToPermissionSetRequestTypeDef",
    "ResourceServerConfigTypeDef",
    "ResourceServerScopeDetailsTypeDef",
    "ResponseMetadataTypeDef",
    "ScopeDetailsTypeDef",
    "SignInOptionsTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "TrustedTokenIssuerConfigurationTypeDef",
    "TrustedTokenIssuerMetadataTypeDef",
    "TrustedTokenIssuerUpdateConfigurationTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateApplicationPortalOptionsTypeDef",
    "UpdateApplicationRequestTypeDef",
    "UpdateInstanceAccessControlAttributeConfigurationRequestTypeDef",
    "UpdateInstanceRequestTypeDef",
    "UpdatePermissionSetRequestTypeDef",
    "UpdateTrustedTokenIssuerRequestTypeDef",
)

class AccessControlAttributeValueOutputTypeDef(TypedDict):
    Source: list[str]

class AccessControlAttributeValueTypeDef(TypedDict):
    Source: Sequence[str]

class AccountAssignmentForPrincipalTypeDef(TypedDict):
    AccountId: NotRequired[str]
    PermissionSetArn: NotRequired[str]
    PrincipalId: NotRequired[str]
    PrincipalType: NotRequired[PrincipalTypeType]

class AccountAssignmentOperationStatusMetadataTypeDef(TypedDict):
    Status: NotRequired[StatusValuesType]
    RequestId: NotRequired[str]
    CreatedDate: NotRequired[datetime]

class AccountAssignmentOperationStatusTypeDef(TypedDict):
    Status: NotRequired[StatusValuesType]
    RequestId: NotRequired[str]
    FailureReason: NotRequired[str]
    TargetId: NotRequired[str]
    TargetType: NotRequired[Literal["AWS_ACCOUNT"]]
    PermissionSetArn: NotRequired[str]
    PrincipalType: NotRequired[PrincipalTypeType]
    PrincipalId: NotRequired[str]
    CreatedDate: NotRequired[datetime]

class AccountAssignmentTypeDef(TypedDict):
    AccountId: NotRequired[str]
    PermissionSetArn: NotRequired[str]
    PrincipalType: NotRequired[PrincipalTypeType]
    PrincipalId: NotRequired[str]

class ApplicationAssignmentForPrincipalTypeDef(TypedDict):
    ApplicationArn: NotRequired[str]
    PrincipalId: NotRequired[str]
    PrincipalType: NotRequired[PrincipalTypeType]

class ApplicationAssignmentTypeDef(TypedDict):
    ApplicationArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType

class DisplayDataTypeDef(TypedDict):
    DisplayName: NotRequired[str]
    IconUrl: NotRequired[str]
    Description: NotRequired[str]

class CustomerManagedPolicyReferenceTypeDef(TypedDict):
    Name: str
    Path: NotRequired[str]

class AttachManagedPolicyToPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    ManagedPolicyArn: str

class AttachedManagedPolicyTypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]

class IamAuthenticationMethodOutputTypeDef(TypedDict):
    ActorPolicy: dict[str, Any]

class IamAuthenticationMethodTypeDef(TypedDict):
    ActorPolicy: Mapping[str, Any]

class AuthorizationCodeGrantOutputTypeDef(TypedDict):
    RedirectUris: NotRequired[list[str]]

class AuthorizationCodeGrantTypeDef(TypedDict):
    RedirectUris: NotRequired[Sequence[str]]

class AuthorizedTokenIssuerOutputTypeDef(TypedDict):
    TrustedTokenIssuerArn: NotRequired[str]
    AuthorizedAudiences: NotRequired[list[str]]

class AuthorizedTokenIssuerTypeDef(TypedDict):
    TrustedTokenIssuerArn: NotRequired[str]
    AuthorizedAudiences: NotRequired[Sequence[str]]

class CreateAccountAssignmentRequestTypeDef(TypedDict):
    InstanceArn: str
    TargetId: str
    TargetType: Literal["AWS_ACCOUNT"]
    PermissionSetArn: str
    PrincipalType: PrincipalTypeType
    PrincipalId: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateApplicationAssignmentRequestTypeDef(TypedDict):
    ApplicationArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class PermissionSetTypeDef(TypedDict):
    Name: NotRequired[str]
    PermissionSetArn: NotRequired[str]
    Description: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    SessionDuration: NotRequired[str]
    RelayState: NotRequired[str]

class DeleteAccountAssignmentRequestTypeDef(TypedDict):
    InstanceArn: str
    TargetId: str
    TargetType: Literal["AWS_ACCOUNT"]
    PermissionSetArn: str
    PrincipalType: PrincipalTypeType
    PrincipalId: str

class DeleteApplicationAccessScopeRequestTypeDef(TypedDict):
    ApplicationArn: str
    Scope: str

class DeleteApplicationAssignmentRequestTypeDef(TypedDict):
    ApplicationArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType

class DeleteApplicationAuthenticationMethodRequestTypeDef(TypedDict):
    ApplicationArn: str
    AuthenticationMethodType: Literal["IAM"]

class DeleteApplicationGrantRequestTypeDef(TypedDict):
    ApplicationArn: str
    GrantType: GrantTypeType

class DeleteApplicationRequestTypeDef(TypedDict):
    ApplicationArn: str

class DeleteInlinePolicyFromPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str

class DeleteInstanceAccessControlAttributeConfigurationRequestTypeDef(TypedDict):
    InstanceArn: str

class DeleteInstanceRequestTypeDef(TypedDict):
    InstanceArn: str

class DeletePermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str

class DeletePermissionsBoundaryFromPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str

class DeleteTrustedTokenIssuerRequestTypeDef(TypedDict):
    TrustedTokenIssuerArn: str

class DescribeAccountAssignmentCreationStatusRequestTypeDef(TypedDict):
    InstanceArn: str
    AccountAssignmentCreationRequestId: str

class DescribeAccountAssignmentDeletionStatusRequestTypeDef(TypedDict):
    InstanceArn: str
    AccountAssignmentDeletionRequestId: str

class DescribeApplicationAssignmentRequestTypeDef(TypedDict):
    ApplicationArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType

class DescribeApplicationProviderRequestTypeDef(TypedDict):
    ApplicationProviderArn: str

class DescribeApplicationRequestTypeDef(TypedDict):
    ApplicationArn: str

class DescribeInstanceAccessControlAttributeConfigurationRequestTypeDef(TypedDict):
    InstanceArn: str

class DescribeInstanceRequestTypeDef(TypedDict):
    InstanceArn: str

class EncryptionConfigurationDetailsTypeDef(TypedDict):
    KeyType: NotRequired[KmsKeyTypeType]
    KmsKeyArn: NotRequired[str]
    EncryptionStatus: NotRequired[KmsKeyStatusType]
    EncryptionStatusReason: NotRequired[str]

class DescribePermissionSetProvisioningStatusRequestTypeDef(TypedDict):
    InstanceArn: str
    ProvisionPermissionSetRequestId: str

class PermissionSetProvisioningStatusTypeDef(TypedDict):
    Status: NotRequired[StatusValuesType]
    RequestId: NotRequired[str]
    AccountId: NotRequired[str]
    PermissionSetArn: NotRequired[str]
    FailureReason: NotRequired[str]
    CreatedDate: NotRequired[datetime]

class DescribePermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str

class DescribeTrustedTokenIssuerRequestTypeDef(TypedDict):
    TrustedTokenIssuerArn: str

class DetachManagedPolicyFromPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    ManagedPolicyArn: str

class EncryptionConfigurationTypeDef(TypedDict):
    KeyType: KmsKeyTypeType
    KmsKeyArn: NotRequired[str]

class GetApplicationAccessScopeRequestTypeDef(TypedDict):
    ApplicationArn: str
    Scope: str

class GetApplicationAssignmentConfigurationRequestTypeDef(TypedDict):
    ApplicationArn: str

class GetApplicationAuthenticationMethodRequestTypeDef(TypedDict):
    ApplicationArn: str
    AuthenticationMethodType: Literal["IAM"]

class GetApplicationGrantRequestTypeDef(TypedDict):
    ApplicationArn: str
    GrantType: GrantTypeType

class GetApplicationSessionConfigurationRequestTypeDef(TypedDict):
    ApplicationArn: str

class GetInlinePolicyForPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str

class GetPermissionsBoundaryForPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str

class InstanceMetadataTypeDef(TypedDict):
    InstanceArn: NotRequired[str]
    IdentityStoreId: NotRequired[str]
    OwnerAccountId: NotRequired[str]
    Name: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    Status: NotRequired[InstanceStatusType]
    StatusReason: NotRequired[str]

class OperationStatusFilterTypeDef(TypedDict):
    Status: NotRequired[StatusValuesType]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAccountAssignmentsFilterTypeDef(TypedDict):
    AccountId: NotRequired[str]

class ListAccountAssignmentsRequestTypeDef(TypedDict):
    InstanceArn: str
    AccountId: str
    PermissionSetArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAccountsForProvisionedPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    ProvisioningStatus: NotRequired[ProvisioningStatusType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListApplicationAccessScopesRequestTypeDef(TypedDict):
    ApplicationArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ScopeDetailsTypeDef(TypedDict):
    Scope: str
    AuthorizedTargets: NotRequired[list[str]]

class ListApplicationAssignmentsFilterTypeDef(TypedDict):
    ApplicationArn: NotRequired[str]

class ListApplicationAssignmentsRequestTypeDef(TypedDict):
    ApplicationArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListApplicationAuthenticationMethodsRequestTypeDef(TypedDict):
    ApplicationArn: str
    NextToken: NotRequired[str]

class ListApplicationGrantsRequestTypeDef(TypedDict):
    ApplicationArn: str
    NextToken: NotRequired[str]

class ListApplicationProvidersRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListApplicationsFilterTypeDef(TypedDict):
    ApplicationAccount: NotRequired[str]
    ApplicationProvider: NotRequired[str]

class ListCustomerManagedPolicyReferencesInPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListInstancesRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListManagedPoliciesInPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class PermissionSetProvisioningStatusMetadataTypeDef(TypedDict):
    Status: NotRequired[StatusValuesType]
    RequestId: NotRequired[str]
    CreatedDate: NotRequired[datetime]

class ListPermissionSetsProvisionedToAccountRequestTypeDef(TypedDict):
    InstanceArn: str
    AccountId: str
    ProvisioningStatus: NotRequired[ProvisioningStatusType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListPermissionSetsRequestTypeDef(TypedDict):
    InstanceArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    InstanceArn: NotRequired[str]
    NextToken: NotRequired[str]

class ListTrustedTokenIssuersRequestTypeDef(TypedDict):
    InstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class TrustedTokenIssuerMetadataTypeDef(TypedDict):
    TrustedTokenIssuerArn: NotRequired[str]
    Name: NotRequired[str]
    TrustedTokenIssuerType: NotRequired[Literal["OIDC_JWT"]]

class OidcJwtConfigurationTypeDef(TypedDict):
    IssuerUrl: str
    ClaimAttributePath: str
    IdentityStoreAttributePath: str
    JwksRetrievalOption: Literal["OPEN_ID_DISCOVERY"]

class OidcJwtUpdateConfigurationTypeDef(TypedDict):
    ClaimAttributePath: NotRequired[str]
    IdentityStoreAttributePath: NotRequired[str]
    JwksRetrievalOption: NotRequired[Literal["OPEN_ID_DISCOVERY"]]

class SignInOptionsTypeDef(TypedDict):
    Origin: SignInOriginType
    ApplicationUrl: NotRequired[str]

class ProvisionPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    TargetType: ProvisionTargetTypeType
    TargetId: NotRequired[str]

class PutApplicationAccessScopeRequestTypeDef(TypedDict):
    Scope: str
    ApplicationArn: str
    AuthorizedTargets: NotRequired[Sequence[str]]

class PutApplicationAssignmentConfigurationRequestTypeDef(TypedDict):
    ApplicationArn: str
    AssignmentRequired: bool

class PutApplicationSessionConfigurationRequestTypeDef(TypedDict):
    ApplicationArn: str
    UserBackgroundSessionApplicationStatus: NotRequired[UserBackgroundSessionApplicationStatusType]

class PutInlinePolicyToPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    InlinePolicy: str

class ResourceServerScopeDetailsTypeDef(TypedDict):
    LongDescription: NotRequired[str]
    DetailedTitle: NotRequired[str]

class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]
    InstanceArn: NotRequired[str]

class UpdatePermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    Description: NotRequired[str]
    SessionDuration: NotRequired[str]
    RelayState: NotRequired[str]

class AccessControlAttributeOutputTypeDef(TypedDict):
    Key: str
    Value: AccessControlAttributeValueOutputTypeDef

class AccessControlAttributeTypeDef(TypedDict):
    Key: str
    Value: AccessControlAttributeValueTypeDef

class AttachCustomerManagedPolicyReferenceToPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    CustomerManagedPolicyReference: CustomerManagedPolicyReferenceTypeDef

class DetachCustomerManagedPolicyReferenceFromPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    CustomerManagedPolicyReference: CustomerManagedPolicyReferenceTypeDef

class PermissionsBoundaryTypeDef(TypedDict):
    CustomerManagedPolicyReference: NotRequired[CustomerManagedPolicyReferenceTypeDef]
    ManagedPolicyArn: NotRequired[str]

class AuthenticationMethodOutputTypeDef(TypedDict):
    Iam: NotRequired[IamAuthenticationMethodOutputTypeDef]

class AuthenticationMethodTypeDef(TypedDict):
    Iam: NotRequired[IamAuthenticationMethodTypeDef]

class JwtBearerGrantOutputTypeDef(TypedDict):
    AuthorizedTokenIssuers: NotRequired[list[AuthorizedTokenIssuerOutputTypeDef]]

class JwtBearerGrantTypeDef(TypedDict):
    AuthorizedTokenIssuers: NotRequired[Sequence[AuthorizedTokenIssuerTypeDef]]

class CreateAccountAssignmentResponseTypeDef(TypedDict):
    AccountAssignmentCreationStatus: AccountAssignmentOperationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateApplicationResponseTypeDef(TypedDict):
    ApplicationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateInstanceResponseTypeDef(TypedDict):
    InstanceArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTrustedTokenIssuerResponseTypeDef(TypedDict):
    TrustedTokenIssuerArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAccountAssignmentResponseTypeDef(TypedDict):
    AccountAssignmentDeletionStatus: AccountAssignmentOperationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAccountAssignmentCreationStatusResponseTypeDef(TypedDict):
    AccountAssignmentCreationStatus: AccountAssignmentOperationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAccountAssignmentDeletionStatusResponseTypeDef(TypedDict):
    AccountAssignmentDeletionStatus: AccountAssignmentOperationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeApplicationAssignmentResponseTypeDef(TypedDict):
    PrincipalType: PrincipalTypeType
    PrincipalId: str
    ApplicationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetApplicationAccessScopeResponseTypeDef(TypedDict):
    Scope: str
    AuthorizedTargets: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetApplicationAssignmentConfigurationResponseTypeDef(TypedDict):
    AssignmentRequired: bool
    ResponseMetadata: ResponseMetadataTypeDef

class GetApplicationSessionConfigurationResponseTypeDef(TypedDict):
    UserBackgroundSessionApplicationStatus: UserBackgroundSessionApplicationStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class GetInlinePolicyForPermissionSetResponseTypeDef(TypedDict):
    InlinePolicy: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAccountAssignmentCreationStatusResponseTypeDef(TypedDict):
    AccountAssignmentsCreationStatus: list[AccountAssignmentOperationStatusMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAccountAssignmentDeletionStatusResponseTypeDef(TypedDict):
    AccountAssignmentsDeletionStatus: list[AccountAssignmentOperationStatusMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAccountAssignmentsForPrincipalResponseTypeDef(TypedDict):
    AccountAssignments: list[AccountAssignmentForPrincipalTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAccountAssignmentsResponseTypeDef(TypedDict):
    AccountAssignments: list[AccountAssignmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAccountsForProvisionedPermissionSetResponseTypeDef(TypedDict):
    AccountIds: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListApplicationAssignmentsForPrincipalResponseTypeDef(TypedDict):
    ApplicationAssignments: list[ApplicationAssignmentForPrincipalTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListApplicationAssignmentsResponseTypeDef(TypedDict):
    ApplicationAssignments: list[ApplicationAssignmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef(TypedDict):
    CustomerManagedPolicyReferences: list[CustomerManagedPolicyReferenceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListManagedPoliciesInPermissionSetResponseTypeDef(TypedDict):
    AttachedManagedPolicies: list[AttachedManagedPolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListPermissionSetsProvisionedToAccountResponseTypeDef(TypedDict):
    PermissionSets: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListPermissionSetsResponseTypeDef(TypedDict):
    PermissionSets: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateInstanceRequestTypeDef(TypedDict):
    Name: NotRequired[str]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreatePermissionSetRequestTypeDef(TypedDict):
    Name: str
    InstanceArn: str
    Description: NotRequired[str]
    SessionDuration: NotRequired[str]
    RelayState: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]
    InstanceArn: NotRequired[str]

class CreatePermissionSetResponseTypeDef(TypedDict):
    PermissionSet: PermissionSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribePermissionSetResponseTypeDef(TypedDict):
    PermissionSet: PermissionSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeInstanceResponseTypeDef(TypedDict):
    InstanceArn: str
    IdentityStoreId: str
    OwnerAccountId: str
    Name: str
    CreatedDate: datetime
    Status: InstanceStatusType
    StatusReason: str
    EncryptionConfigurationDetails: EncryptionConfigurationDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribePermissionSetProvisioningStatusResponseTypeDef(TypedDict):
    PermissionSetProvisioningStatus: PermissionSetProvisioningStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ProvisionPermissionSetResponseTypeDef(TypedDict):
    PermissionSetProvisioningStatus: PermissionSetProvisioningStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateInstanceRequestTypeDef(TypedDict):
    InstanceArn: str
    Name: NotRequired[str]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]

class ListInstancesResponseTypeDef(TypedDict):
    Instances: list[InstanceMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAccountAssignmentCreationStatusRequestTypeDef(TypedDict):
    InstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filter: NotRequired[OperationStatusFilterTypeDef]

class ListAccountAssignmentDeletionStatusRequestTypeDef(TypedDict):
    InstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filter: NotRequired[OperationStatusFilterTypeDef]

class ListPermissionSetProvisioningStatusRequestTypeDef(TypedDict):
    InstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filter: NotRequired[OperationStatusFilterTypeDef]

class ListAccountAssignmentCreationStatusRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[OperationStatusFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAccountAssignmentDeletionStatusRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[OperationStatusFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAccountAssignmentsRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    AccountId: str
    PermissionSetArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAccountsForProvisionedPermissionSetRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    ProvisioningStatus: NotRequired[ProvisioningStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationAccessScopesRequestPaginateTypeDef(TypedDict):
    ApplicationArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationAssignmentsRequestPaginateTypeDef(TypedDict):
    ApplicationArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationAuthenticationMethodsRequestPaginateTypeDef(TypedDict):
    ApplicationArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationGrantsRequestPaginateTypeDef(TypedDict):
    ApplicationArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationProvidersRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCustomerManagedPolicyReferencesInPermissionSetRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListInstancesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListManagedPoliciesInPermissionSetRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPermissionSetProvisioningStatusRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[OperationStatusFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPermissionSetsProvisionedToAccountRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    AccountId: str
    ProvisioningStatus: NotRequired[ProvisioningStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPermissionSetsRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTagsForResourceRequestPaginateTypeDef(TypedDict):
    ResourceArn: str
    InstanceArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTrustedTokenIssuersRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAccountAssignmentsForPrincipalRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType
    Filter: NotRequired[ListAccountAssignmentsFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAccountAssignmentsForPrincipalRequestTypeDef(TypedDict):
    InstanceArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType
    Filter: NotRequired[ListAccountAssignmentsFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListApplicationAccessScopesResponseTypeDef(TypedDict):
    Scopes: list[ScopeDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListApplicationAssignmentsForPrincipalRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType
    Filter: NotRequired[ListApplicationAssignmentsFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationAssignmentsForPrincipalRequestTypeDef(TypedDict):
    InstanceArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType
    Filter: NotRequired[ListApplicationAssignmentsFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListApplicationsRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[ListApplicationsFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationsRequestTypeDef(TypedDict):
    InstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filter: NotRequired[ListApplicationsFilterTypeDef]

class ListPermissionSetProvisioningStatusResponseTypeDef(TypedDict):
    PermissionSetsProvisioningStatus: list[PermissionSetProvisioningStatusMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTrustedTokenIssuersResponseTypeDef(TypedDict):
    TrustedTokenIssuers: list[TrustedTokenIssuerMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class TrustedTokenIssuerConfigurationTypeDef(TypedDict):
    OidcJwtConfiguration: NotRequired[OidcJwtConfigurationTypeDef]

class TrustedTokenIssuerUpdateConfigurationTypeDef(TypedDict):
    OidcJwtConfiguration: NotRequired[OidcJwtUpdateConfigurationTypeDef]

class PortalOptionsTypeDef(TypedDict):
    SignInOptions: NotRequired[SignInOptionsTypeDef]
    Visibility: NotRequired[ApplicationVisibilityType]

class UpdateApplicationPortalOptionsTypeDef(TypedDict):
    SignInOptions: NotRequired[SignInOptionsTypeDef]

class ResourceServerConfigTypeDef(TypedDict):
    Scopes: NotRequired[dict[str, ResourceServerScopeDetailsTypeDef]]

class InstanceAccessControlAttributeConfigurationOutputTypeDef(TypedDict):
    AccessControlAttributes: list[AccessControlAttributeOutputTypeDef]

class InstanceAccessControlAttributeConfigurationTypeDef(TypedDict):
    AccessControlAttributes: Sequence[AccessControlAttributeTypeDef]

class GetPermissionsBoundaryForPermissionSetResponseTypeDef(TypedDict):
    PermissionsBoundary: PermissionsBoundaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutPermissionsBoundaryToPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    PermissionsBoundary: PermissionsBoundaryTypeDef

class AuthenticationMethodItemTypeDef(TypedDict):
    AuthenticationMethodType: NotRequired[Literal["IAM"]]
    AuthenticationMethod: NotRequired[AuthenticationMethodOutputTypeDef]

class GetApplicationAuthenticationMethodResponseTypeDef(TypedDict):
    AuthenticationMethod: AuthenticationMethodOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

AuthenticationMethodUnionTypeDef = Union[
    AuthenticationMethodTypeDef, AuthenticationMethodOutputTypeDef
]

class GrantOutputTypeDef(TypedDict):
    AuthorizationCode: NotRequired[AuthorizationCodeGrantOutputTypeDef]
    JwtBearer: NotRequired[JwtBearerGrantOutputTypeDef]
    RefreshToken: NotRequired[dict[str, Any]]
    TokenExchange: NotRequired[dict[str, Any]]

class GrantTypeDef(TypedDict):
    AuthorizationCode: NotRequired[AuthorizationCodeGrantTypeDef]
    JwtBearer: NotRequired[JwtBearerGrantTypeDef]
    RefreshToken: NotRequired[Mapping[str, Any]]
    TokenExchange: NotRequired[Mapping[str, Any]]

class CreateTrustedTokenIssuerRequestTypeDef(TypedDict):
    InstanceArn: str
    Name: str
    TrustedTokenIssuerType: Literal["OIDC_JWT"]
    TrustedTokenIssuerConfiguration: TrustedTokenIssuerConfigurationTypeDef
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class DescribeTrustedTokenIssuerResponseTypeDef(TypedDict):
    TrustedTokenIssuerArn: str
    Name: str
    TrustedTokenIssuerType: Literal["OIDC_JWT"]
    TrustedTokenIssuerConfiguration: TrustedTokenIssuerConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTrustedTokenIssuerRequestTypeDef(TypedDict):
    TrustedTokenIssuerArn: str
    Name: NotRequired[str]
    TrustedTokenIssuerConfiguration: NotRequired[TrustedTokenIssuerUpdateConfigurationTypeDef]

class ApplicationTypeDef(TypedDict):
    ApplicationArn: NotRequired[str]
    ApplicationProviderArn: NotRequired[str]
    Name: NotRequired[str]
    ApplicationAccount: NotRequired[str]
    InstanceArn: NotRequired[str]
    Status: NotRequired[ApplicationStatusType]
    PortalOptions: NotRequired[PortalOptionsTypeDef]
    Description: NotRequired[str]
    CreatedDate: NotRequired[datetime]

class CreateApplicationRequestTypeDef(TypedDict):
    InstanceArn: str
    ApplicationProviderArn: str
    Name: str
    Description: NotRequired[str]
    PortalOptions: NotRequired[PortalOptionsTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    Status: NotRequired[ApplicationStatusType]
    ClientToken: NotRequired[str]

class DescribeApplicationResponseTypeDef(TypedDict):
    ApplicationArn: str
    ApplicationProviderArn: str
    Name: str
    ApplicationAccount: str
    InstanceArn: str
    Status: ApplicationStatusType
    PortalOptions: PortalOptionsTypeDef
    Description: str
    CreatedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApplicationRequestTypeDef(TypedDict):
    ApplicationArn: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    Status: NotRequired[ApplicationStatusType]
    PortalOptions: NotRequired[UpdateApplicationPortalOptionsTypeDef]

class ApplicationProviderTypeDef(TypedDict):
    ApplicationProviderArn: str
    FederationProtocol: NotRequired[FederationProtocolType]
    DisplayData: NotRequired[DisplayDataTypeDef]
    ResourceServerConfig: NotRequired[ResourceServerConfigTypeDef]

class DescribeApplicationProviderResponseTypeDef(TypedDict):
    ApplicationProviderArn: str
    FederationProtocol: FederationProtocolType
    DisplayData: DisplayDataTypeDef
    ResourceServerConfig: ResourceServerConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef(TypedDict):
    Status: InstanceAccessControlAttributeConfigurationStatusType
    StatusReason: str
    InstanceAccessControlAttributeConfiguration: (
        InstanceAccessControlAttributeConfigurationOutputTypeDef
    )
    ResponseMetadata: ResponseMetadataTypeDef

InstanceAccessControlAttributeConfigurationUnionTypeDef = Union[
    InstanceAccessControlAttributeConfigurationTypeDef,
    InstanceAccessControlAttributeConfigurationOutputTypeDef,
]

class ListApplicationAuthenticationMethodsResponseTypeDef(TypedDict):
    AuthenticationMethods: list[AuthenticationMethodItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PutApplicationAuthenticationMethodRequestTypeDef(TypedDict):
    ApplicationArn: str
    AuthenticationMethodType: Literal["IAM"]
    AuthenticationMethod: AuthenticationMethodUnionTypeDef

class GetApplicationGrantResponseTypeDef(TypedDict):
    Grant: GrantOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GrantItemTypeDef(TypedDict):
    GrantType: GrantTypeType
    Grant: GrantOutputTypeDef

GrantUnionTypeDef = Union[GrantTypeDef, GrantOutputTypeDef]

class ListApplicationsResponseTypeDef(TypedDict):
    Applications: list[ApplicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListApplicationProvidersResponseTypeDef(TypedDict):
    ApplicationProviders: list[ApplicationProviderTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateInstanceAccessControlAttributeConfigurationRequestTypeDef(TypedDict):
    InstanceArn: str
    InstanceAccessControlAttributeConfiguration: (
        InstanceAccessControlAttributeConfigurationUnionTypeDef
    )

class UpdateInstanceAccessControlAttributeConfigurationRequestTypeDef(TypedDict):
    InstanceArn: str
    InstanceAccessControlAttributeConfiguration: (
        InstanceAccessControlAttributeConfigurationUnionTypeDef
    )

class ListApplicationGrantsResponseTypeDef(TypedDict):
    Grants: list[GrantItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PutApplicationGrantRequestTypeDef(TypedDict):
    ApplicationArn: str
    GrantType: GrantTypeType
    Grant: GrantUnionTypeDef
