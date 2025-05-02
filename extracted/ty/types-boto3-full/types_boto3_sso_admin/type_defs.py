"""
Type annotations for sso-admin service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sso_admin/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_boto3_sso_admin.type_defs import AccessControlAttributeValueOutputTypeDef

    data: AccessControlAttributeValueOutputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Any, Union

from .literals import (
    ApplicationStatusType,
    ApplicationVisibilityType,
    FederationProtocolType,
    GrantTypeType,
    InstanceAccessControlAttributeConfigurationStatusType,
    InstanceStatusType,
    PrincipalTypeType,
    ProvisioningStatusType,
    ProvisionTargetTypeType,
    SignInOriginType,
    StatusValuesType,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Mapping, Sequence
else:
    from typing import Dict, List, Mapping, Sequence
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
    "GetApplicationAccessScopeRequestTypeDef",
    "GetApplicationAccessScopeResponseTypeDef",
    "GetApplicationAssignmentConfigurationRequestTypeDef",
    "GetApplicationAssignmentConfigurationResponseTypeDef",
    "GetApplicationAuthenticationMethodRequestTypeDef",
    "GetApplicationAuthenticationMethodResponseTypeDef",
    "GetApplicationGrantRequestTypeDef",
    "GetApplicationGrantResponseTypeDef",
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
    Source: List[str]


class AccessControlAttributeValueTypeDef(TypedDict):
    Source: Sequence[str]


class AccountAssignmentForPrincipalTypeDef(TypedDict):
    AccountId: NotRequired[str]
    PermissionSetArn: NotRequired[str]
    PrincipalId: NotRequired[str]
    PrincipalType: NotRequired[PrincipalTypeType]


class AccountAssignmentOperationStatusMetadataTypeDef(TypedDict):
    CreatedDate: NotRequired[datetime]
    RequestId: NotRequired[str]
    Status: NotRequired[StatusValuesType]


class AccountAssignmentOperationStatusTypeDef(TypedDict):
    CreatedDate: NotRequired[datetime]
    FailureReason: NotRequired[str]
    PermissionSetArn: NotRequired[str]
    PrincipalId: NotRequired[str]
    PrincipalType: NotRequired[PrincipalTypeType]
    RequestId: NotRequired[str]
    Status: NotRequired[StatusValuesType]
    TargetId: NotRequired[str]
    TargetType: NotRequired[Literal["AWS_ACCOUNT"]]


class AccountAssignmentTypeDef(TypedDict):
    AccountId: NotRequired[str]
    PermissionSetArn: NotRequired[str]
    PrincipalId: NotRequired[str]
    PrincipalType: NotRequired[PrincipalTypeType]


class ApplicationAssignmentForPrincipalTypeDef(TypedDict):
    ApplicationArn: NotRequired[str]
    PrincipalId: NotRequired[str]
    PrincipalType: NotRequired[PrincipalTypeType]


class ApplicationAssignmentTypeDef(TypedDict):
    ApplicationArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType


class DisplayDataTypeDef(TypedDict):
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    IconUrl: NotRequired[str]


class CustomerManagedPolicyReferenceTypeDef(TypedDict):
    Name: str
    Path: NotRequired[str]


class AttachManagedPolicyToPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    ManagedPolicyArn: str
    PermissionSetArn: str


class AttachedManagedPolicyTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]


class IamAuthenticationMethodOutputTypeDef(TypedDict):
    ActorPolicy: Dict[str, Any]


class IamAuthenticationMethodTypeDef(TypedDict):
    ActorPolicy: Mapping[str, Any]


class AuthorizationCodeGrantOutputTypeDef(TypedDict):
    RedirectUris: NotRequired[List[str]]


class AuthorizationCodeGrantTypeDef(TypedDict):
    RedirectUris: NotRequired[Sequence[str]]


class AuthorizedTokenIssuerOutputTypeDef(TypedDict):
    AuthorizedAudiences: NotRequired[List[str]]
    TrustedTokenIssuerArn: NotRequired[str]


class AuthorizedTokenIssuerTypeDef(TypedDict):
    AuthorizedAudiences: NotRequired[Sequence[str]]
    TrustedTokenIssuerArn: NotRequired[str]


class CreateAccountAssignmentRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType
    TargetId: str
    TargetType: Literal["AWS_ACCOUNT"]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
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
    CreatedDate: NotRequired[datetime]
    Description: NotRequired[str]
    Name: NotRequired[str]
    PermissionSetArn: NotRequired[str]
    RelayState: NotRequired[str]
    SessionDuration: NotRequired[str]


class DeleteAccountAssignmentRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType
    TargetId: str
    TargetType: Literal["AWS_ACCOUNT"]


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
    AccountAssignmentCreationRequestId: str
    InstanceArn: str


class DescribeAccountAssignmentDeletionStatusRequestTypeDef(TypedDict):
    AccountAssignmentDeletionRequestId: str
    InstanceArn: str


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


class DescribePermissionSetProvisioningStatusRequestTypeDef(TypedDict):
    InstanceArn: str
    ProvisionPermissionSetRequestId: str


class PermissionSetProvisioningStatusTypeDef(TypedDict):
    AccountId: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    FailureReason: NotRequired[str]
    PermissionSetArn: NotRequired[str]
    RequestId: NotRequired[str]
    Status: NotRequired[StatusValuesType]


class DescribePermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str


class DescribeTrustedTokenIssuerRequestTypeDef(TypedDict):
    TrustedTokenIssuerArn: str


class DetachManagedPolicyFromPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    ManagedPolicyArn: str
    PermissionSetArn: str


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


class GetInlinePolicyForPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str


class GetPermissionsBoundaryForPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str


class InstanceMetadataTypeDef(TypedDict):
    CreatedDate: NotRequired[datetime]
    IdentityStoreId: NotRequired[str]
    InstanceArn: NotRequired[str]
    Name: NotRequired[str]
    OwnerAccountId: NotRequired[str]
    Status: NotRequired[InstanceStatusType]


class OperationStatusFilterTypeDef(TypedDict):
    Status: NotRequired[StatusValuesType]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAccountAssignmentsFilterTypeDef(TypedDict):
    AccountId: NotRequired[str]


class ListAccountAssignmentsRequestTypeDef(TypedDict):
    AccountId: str
    InstanceArn: str
    PermissionSetArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListAccountsForProvisionedPermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ProvisioningStatus: NotRequired[ProvisioningStatusType]


class ListApplicationAccessScopesRequestTypeDef(TypedDict):
    ApplicationArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ScopeDetailsTypeDef(TypedDict):
    Scope: str
    AuthorizedTargets: NotRequired[List[str]]


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
    CreatedDate: NotRequired[datetime]
    RequestId: NotRequired[str]
    Status: NotRequired[StatusValuesType]


class ListPermissionSetsProvisionedToAccountRequestTypeDef(TypedDict):
    AccountId: str
    InstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ProvisioningStatus: NotRequired[ProvisioningStatusType]


class ListPermissionSetsRequestTypeDef(TypedDict):
    InstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    InstanceArn: NotRequired[str]
    NextToken: NotRequired[str]


class ListTrustedTokenIssuersRequestTypeDef(TypedDict):
    InstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class TrustedTokenIssuerMetadataTypeDef(TypedDict):
    Name: NotRequired[str]
    TrustedTokenIssuerArn: NotRequired[str]
    TrustedTokenIssuerType: NotRequired[Literal["OIDC_JWT"]]


class OidcJwtConfigurationTypeDef(TypedDict):
    ClaimAttributePath: str
    IdentityStoreAttributePath: str
    IssuerUrl: str
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
    ApplicationArn: str
    Scope: str
    AuthorizedTargets: NotRequired[Sequence[str]]


class PutApplicationAssignmentConfigurationRequestTypeDef(TypedDict):
    ApplicationArn: str
    AssignmentRequired: bool


class PutInlinePolicyToPermissionSetRequestTypeDef(TypedDict):
    InlinePolicy: str
    InstanceArn: str
    PermissionSetArn: str


class ResourceServerScopeDetailsTypeDef(TypedDict):
    DetailedTitle: NotRequired[str]
    LongDescription: NotRequired[str]


class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]
    InstanceArn: NotRequired[str]


class UpdateInstanceRequestTypeDef(TypedDict):
    InstanceArn: str
    Name: str


class UpdatePermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    PermissionSetArn: str
    Description: NotRequired[str]
    RelayState: NotRequired[str]
    SessionDuration: NotRequired[str]


class AccessControlAttributeOutputTypeDef(TypedDict):
    Key: str
    Value: AccessControlAttributeValueOutputTypeDef


class AccessControlAttributeTypeDef(TypedDict):
    Key: str
    Value: AccessControlAttributeValueTypeDef


class AttachCustomerManagedPolicyReferenceToPermissionSetRequestTypeDef(TypedDict):
    CustomerManagedPolicyReference: CustomerManagedPolicyReferenceTypeDef
    InstanceArn: str
    PermissionSetArn: str


class DetachCustomerManagedPolicyReferenceFromPermissionSetRequestTypeDef(TypedDict):
    CustomerManagedPolicyReference: CustomerManagedPolicyReferenceTypeDef
    InstanceArn: str
    PermissionSetArn: str


class PermissionsBoundaryTypeDef(TypedDict):
    CustomerManagedPolicyReference: NotRequired[CustomerManagedPolicyReferenceTypeDef]
    ManagedPolicyArn: NotRequired[str]


class AuthenticationMethodOutputTypeDef(TypedDict):
    Iam: NotRequired[IamAuthenticationMethodOutputTypeDef]


class AuthenticationMethodTypeDef(TypedDict):
    Iam: NotRequired[IamAuthenticationMethodTypeDef]


class JwtBearerGrantOutputTypeDef(TypedDict):
    AuthorizedTokenIssuers: NotRequired[List[AuthorizedTokenIssuerOutputTypeDef]]


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
    ApplicationArn: str
    PrincipalId: str
    PrincipalType: PrincipalTypeType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeInstanceResponseTypeDef(TypedDict):
    CreatedDate: datetime
    IdentityStoreId: str
    InstanceArn: str
    Name: str
    OwnerAccountId: str
    Status: InstanceStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetApplicationAccessScopeResponseTypeDef(TypedDict):
    AuthorizedTargets: List[str]
    Scope: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetApplicationAssignmentConfigurationResponseTypeDef(TypedDict):
    AssignmentRequired: bool
    ResponseMetadata: ResponseMetadataTypeDef


class GetInlinePolicyForPermissionSetResponseTypeDef(TypedDict):
    InlinePolicy: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListAccountAssignmentCreationStatusResponseTypeDef(TypedDict):
    AccountAssignmentsCreationStatus: List[AccountAssignmentOperationStatusMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAccountAssignmentDeletionStatusResponseTypeDef(TypedDict):
    AccountAssignmentsDeletionStatus: List[AccountAssignmentOperationStatusMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAccountAssignmentsForPrincipalResponseTypeDef(TypedDict):
    AccountAssignments: List[AccountAssignmentForPrincipalTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAccountAssignmentsResponseTypeDef(TypedDict):
    AccountAssignments: List[AccountAssignmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAccountsForProvisionedPermissionSetResponseTypeDef(TypedDict):
    AccountIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListApplicationAssignmentsForPrincipalResponseTypeDef(TypedDict):
    ApplicationAssignments: List[ApplicationAssignmentForPrincipalTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListApplicationAssignmentsResponseTypeDef(TypedDict):
    ApplicationAssignments: List[ApplicationAssignmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef(TypedDict):
    CustomerManagedPolicyReferences: List[CustomerManagedPolicyReferenceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListManagedPoliciesInPermissionSetResponseTypeDef(TypedDict):
    AttachedManagedPolicies: List[AttachedManagedPolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPermissionSetsProvisionedToAccountResponseTypeDef(TypedDict):
    PermissionSets: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPermissionSetsResponseTypeDef(TypedDict):
    PermissionSets: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateInstanceRequestTypeDef(TypedDict):
    ClientToken: NotRequired[str]
    Name: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreatePermissionSetRequestTypeDef(TypedDict):
    InstanceArn: str
    Name: str
    Description: NotRequired[str]
    RelayState: NotRequired[str]
    SessionDuration: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
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


class DescribePermissionSetProvisioningStatusResponseTypeDef(TypedDict):
    PermissionSetProvisioningStatus: PermissionSetProvisioningStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ProvisionPermissionSetResponseTypeDef(TypedDict):
    PermissionSetProvisioningStatus: PermissionSetProvisioningStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListInstancesResponseTypeDef(TypedDict):
    Instances: List[InstanceMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAccountAssignmentCreationStatusRequestTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[OperationStatusFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListAccountAssignmentDeletionStatusRequestTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[OperationStatusFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListPermissionSetProvisioningStatusRequestTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[OperationStatusFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListAccountAssignmentCreationStatusRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[OperationStatusFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAccountAssignmentDeletionStatusRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[OperationStatusFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAccountAssignmentsRequestPaginateTypeDef(TypedDict):
    AccountId: str
    InstanceArn: str
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
    AccountId: str
    InstanceArn: str
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
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListApplicationAccessScopesResponseTypeDef(TypedDict):
    Scopes: List[ScopeDetailsTypeDef]
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
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListApplicationsRequestPaginateTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[ListApplicationsFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListApplicationsRequestTypeDef(TypedDict):
    InstanceArn: str
    Filter: NotRequired[ListApplicationsFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListPermissionSetProvisioningStatusResponseTypeDef(TypedDict):
    PermissionSetsProvisioningStatus: List[PermissionSetProvisioningStatusMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTrustedTokenIssuersResponseTypeDef(TypedDict):
    TrustedTokenIssuers: List[TrustedTokenIssuerMetadataTypeDef]
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
    Scopes: NotRequired[Dict[str, ResourceServerScopeDetailsTypeDef]]


class InstanceAccessControlAttributeConfigurationOutputTypeDef(TypedDict):
    AccessControlAttributes: List[AccessControlAttributeOutputTypeDef]


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
    AuthenticationMethod: NotRequired[AuthenticationMethodOutputTypeDef]
    AuthenticationMethodType: NotRequired[Literal["IAM"]]


class GetApplicationAuthenticationMethodResponseTypeDef(TypedDict):
    AuthenticationMethod: AuthenticationMethodOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


AuthenticationMethodUnionTypeDef = Union[
    AuthenticationMethodTypeDef, AuthenticationMethodOutputTypeDef
]


class GrantOutputTypeDef(TypedDict):
    AuthorizationCode: NotRequired[AuthorizationCodeGrantOutputTypeDef]
    JwtBearer: NotRequired[JwtBearerGrantOutputTypeDef]
    RefreshToken: NotRequired[Dict[str, Any]]
    TokenExchange: NotRequired[Dict[str, Any]]


class GrantTypeDef(TypedDict):
    AuthorizationCode: NotRequired[AuthorizationCodeGrantTypeDef]
    JwtBearer: NotRequired[JwtBearerGrantTypeDef]
    RefreshToken: NotRequired[Mapping[str, Any]]
    TokenExchange: NotRequired[Mapping[str, Any]]


class CreateTrustedTokenIssuerRequestTypeDef(TypedDict):
    InstanceArn: str
    Name: str
    TrustedTokenIssuerConfiguration: TrustedTokenIssuerConfigurationTypeDef
    TrustedTokenIssuerType: Literal["OIDC_JWT"]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeTrustedTokenIssuerResponseTypeDef(TypedDict):
    Name: str
    TrustedTokenIssuerArn: str
    TrustedTokenIssuerConfiguration: TrustedTokenIssuerConfigurationTypeDef
    TrustedTokenIssuerType: Literal["OIDC_JWT"]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTrustedTokenIssuerRequestTypeDef(TypedDict):
    TrustedTokenIssuerArn: str
    Name: NotRequired[str]
    TrustedTokenIssuerConfiguration: NotRequired[TrustedTokenIssuerUpdateConfigurationTypeDef]


class ApplicationTypeDef(TypedDict):
    ApplicationAccount: NotRequired[str]
    ApplicationArn: NotRequired[str]
    ApplicationProviderArn: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    Description: NotRequired[str]
    InstanceArn: NotRequired[str]
    Name: NotRequired[str]
    PortalOptions: NotRequired[PortalOptionsTypeDef]
    Status: NotRequired[ApplicationStatusType]


class CreateApplicationRequestTypeDef(TypedDict):
    ApplicationProviderArn: str
    InstanceArn: str
    Name: str
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    PortalOptions: NotRequired[PortalOptionsTypeDef]
    Status: NotRequired[ApplicationStatusType]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeApplicationResponseTypeDef(TypedDict):
    ApplicationAccount: str
    ApplicationArn: str
    ApplicationProviderArn: str
    CreatedDate: datetime
    Description: str
    InstanceArn: str
    Name: str
    PortalOptions: PortalOptionsTypeDef
    Status: ApplicationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateApplicationRequestTypeDef(TypedDict):
    ApplicationArn: str
    Description: NotRequired[str]
    Name: NotRequired[str]
    PortalOptions: NotRequired[UpdateApplicationPortalOptionsTypeDef]
    Status: NotRequired[ApplicationStatusType]


class ApplicationProviderTypeDef(TypedDict):
    ApplicationProviderArn: str
    DisplayData: NotRequired[DisplayDataTypeDef]
    FederationProtocol: NotRequired[FederationProtocolType]
    ResourceServerConfig: NotRequired[ResourceServerConfigTypeDef]


class DescribeApplicationProviderResponseTypeDef(TypedDict):
    ApplicationProviderArn: str
    DisplayData: DisplayDataTypeDef
    FederationProtocol: FederationProtocolType
    ResourceServerConfig: ResourceServerConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef(TypedDict):
    InstanceAccessControlAttributeConfiguration: (
        InstanceAccessControlAttributeConfigurationOutputTypeDef
    )
    Status: InstanceAccessControlAttributeConfigurationStatusType
    StatusReason: str
    ResponseMetadata: ResponseMetadataTypeDef


InstanceAccessControlAttributeConfigurationUnionTypeDef = Union[
    InstanceAccessControlAttributeConfigurationTypeDef,
    InstanceAccessControlAttributeConfigurationOutputTypeDef,
]


class ListApplicationAuthenticationMethodsResponseTypeDef(TypedDict):
    AuthenticationMethods: List[AuthenticationMethodItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PutApplicationAuthenticationMethodRequestTypeDef(TypedDict):
    ApplicationArn: str
    AuthenticationMethod: AuthenticationMethodUnionTypeDef
    AuthenticationMethodType: Literal["IAM"]


class GetApplicationGrantResponseTypeDef(TypedDict):
    Grant: GrantOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GrantItemTypeDef(TypedDict):
    Grant: GrantOutputTypeDef
    GrantType: GrantTypeType


GrantUnionTypeDef = Union[GrantTypeDef, GrantOutputTypeDef]


class ListApplicationsResponseTypeDef(TypedDict):
    Applications: List[ApplicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListApplicationProvidersResponseTypeDef(TypedDict):
    ApplicationProviders: List[ApplicationProviderTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateInstanceAccessControlAttributeConfigurationRequestTypeDef(TypedDict):
    InstanceAccessControlAttributeConfiguration: (
        InstanceAccessControlAttributeConfigurationUnionTypeDef
    )
    InstanceArn: str


class UpdateInstanceAccessControlAttributeConfigurationRequestTypeDef(TypedDict):
    InstanceAccessControlAttributeConfiguration: (
        InstanceAccessControlAttributeConfigurationUnionTypeDef
    )
    InstanceArn: str


class ListApplicationGrantsResponseTypeDef(TypedDict):
    Grants: List[GrantItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PutApplicationGrantRequestTypeDef(TypedDict):
    ApplicationArn: str
    Grant: GrantUnionTypeDef
    GrantType: GrantTypeType
