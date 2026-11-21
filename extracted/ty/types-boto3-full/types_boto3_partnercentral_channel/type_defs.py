"""
Type annotations for partnercentral-channel service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_channel/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_partnercentral_channel.type_defs import AcceptChannelHandshakeDetailTypeDef

    data: AcceptChannelHandshakeDetailTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AccountScopeType,
    AssociationTypeType,
    ChannelContractStatusType,
    CoverageType,
    HandshakeStatusType,
    HandshakeTypeType,
    ManagedServicesSupportedServiceType,
    ParticipantTypeType,
    ProgramManagementAccountStatusType,
    ProgramManagementAccountTypeType,
    ProgramType,
    ProviderType,
    ResaleAccountModelType,
    SectorType,
    ServicePeriodTypeType,
    SortOrderType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AcceptChannelHandshakeDetailTypeDef",
    "AcceptChannelHandshakeRequestTypeDef",
    "AcceptChannelHandshakeResponseTypeDef",
    "AddressTypeDef",
    "CancelChannelContractDetailTypeDef",
    "CancelChannelContractRequestTypeDef",
    "CancelChannelContractResponseTypeDef",
    "CancelChannelHandshakeDetailTypeDef",
    "CancelChannelHandshakeRequestTypeDef",
    "CancelChannelHandshakeResponseTypeDef",
    "ChannelContractDetailTypeDef",
    "ChannelContractDetailsTypeDef",
    "ChannelContractPayloadTypeDef",
    "ChannelContractSummaryDetailsTypeDef",
    "ChannelContractSummaryTypeDef",
    "ChannelHandshakePayloadTypeDef",
    "ChannelHandshakeSummaryTypeDef",
    "CreateChannelContractDetailTypeDef",
    "CreateChannelContractRequestTypeDef",
    "CreateChannelContractResponseTypeDef",
    "CreateChannelHandshakeDetailTypeDef",
    "CreateChannelHandshakeRequestTypeDef",
    "CreateChannelHandshakeResponseTypeDef",
    "CreateProgramManagementAccountDetailTypeDef",
    "CreateProgramManagementAccountRequestTypeDef",
    "CreateProgramManagementAccountResponseTypeDef",
    "CreateRelationshipDetailTypeDef",
    "CreateRelationshipRequestTypeDef",
    "CreateRelationshipResponseTypeDef",
    "DeleteProgramManagementAccountRequestTypeDef",
    "DeleteRelationshipRequestTypeDef",
    "GetChannelContractRequestTypeDef",
    "GetChannelContractResponseTypeDef",
    "GetRelationshipRequestTypeDef",
    "GetRelationshipResponseTypeDef",
    "HandshakeDetailTypeDef",
    "ListChannelContractsRequestPaginateTypeDef",
    "ListChannelContractsRequestTypeDef",
    "ListChannelContractsResponseTypeDef",
    "ListChannelContractsTypeFiltersTypeDef",
    "ListChannelContractsTypeSortTypeDef",
    "ListChannelHandshakesRequestPaginateTypeDef",
    "ListChannelHandshakesRequestTypeDef",
    "ListChannelHandshakesResponseTypeDef",
    "ListChannelHandshakesTypeFiltersTypeDef",
    "ListChannelHandshakesTypeSortTypeDef",
    "ListProgramManagementAccountsRequestPaginateTypeDef",
    "ListProgramManagementAccountsRequestTypeDef",
    "ListProgramManagementAccountsResponseTypeDef",
    "ListProgramManagementAccountsSortBaseTypeDef",
    "ListRelationshipsRequestPaginateTypeDef",
    "ListRelationshipsRequestTypeDef",
    "ListRelationshipsResponseTypeDef",
    "ListRelationshipsSortBaseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ManagedServicesAttestationDetailsTypeDef",
    "ManagedServicesAttestationPayloadTypeDef",
    "ManagedServicesAttestationSummaryDetailsTypeDef",
    "ManagedServicesAttestationTypeFiltersTypeDef",
    "ManagedServicesAttestationTypeSortTypeDef",
    "PaginatorConfigTypeDef",
    "PartnerLedSupportTypeDef",
    "ProgramManagementAccountHandshakeDetailTypeDef",
    "ProgramManagementAccountSummaryTypeDef",
    "ProgramManagementAccountTypeFiltersTypeDef",
    "ProgramManagementAccountTypeSortTypeDef",
    "RejectChannelHandshakeDetailTypeDef",
    "RejectChannelHandshakeRequestTypeDef",
    "RejectChannelHandshakeResponseTypeDef",
    "RelationshipDetailTypeDef",
    "RelationshipSummaryTypeDef",
    "ResoldEnterpriseTypeDef",
    "ResoldUnifiedOperationsTypeDef",
    "ResponseMetadataTypeDef",
    "RevokeServicePeriodHandshakeDetailTypeDef",
    "RevokeServicePeriodPayloadTypeDef",
    "RevokeServicePeriodTypeFiltersTypeDef",
    "RevokeServicePeriodTypeSortTypeDef",
    "StartServicePeriodHandshakeDetailTypeDef",
    "StartServicePeriodPayloadTypeDef",
    "StartServicePeriodTypeFiltersTypeDef",
    "StartServicePeriodTypeSortTypeDef",
    "SupportPlanTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateProgramManagementAccountDetailTypeDef",
    "UpdateProgramManagementAccountRequestTypeDef",
    "UpdateProgramManagementAccountResponseTypeDef",
    "UpdateRelationshipDetailTypeDef",
    "UpdateRelationshipRequestTypeDef",
    "UpdateRelationshipResponseTypeDef",
)

AcceptChannelHandshakeDetailTypeDef = TypedDict(
    "AcceptChannelHandshakeDetailTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "status": NotRequired[HandshakeStatusType],
    },
)


class AcceptChannelHandshakeRequestTypeDef(TypedDict):
    catalog: str
    identifier: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AddressTypeDef(TypedDict):
    city: str
    stateOrRegion: str
    postalCode: str
    countryCode: str
    addressLine: str
    addressLine2: NotRequired[str]


CancelChannelContractDetailTypeDef = TypedDict(
    "CancelChannelContractDetailTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "status": NotRequired[ChannelContractStatusType],
        "cancellationReason": NotRequired[str],
    },
)


class CancelChannelContractRequestTypeDef(TypedDict):
    catalog: str
    identifier: str
    reason: NotRequired[str]
    clientToken: NotRequired[str]


CancelChannelHandshakeDetailTypeDef = TypedDict(
    "CancelChannelHandshakeDetailTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "status": NotRequired[HandshakeStatusType],
    },
)


class CancelChannelHandshakeRequestTypeDef(TypedDict):
    catalog: str
    identifier: str


class ManagedServicesAttestationSummaryDetailsTypeDef(TypedDict):
    legalEntityName: str
    relationshipIdentifier: str
    programManagementAccountIdentifier: str
    endDate: datetime
    supportedServices: list[ManagedServicesSupportedServiceType]
    memberAccountIds: NotRequired[list[str]]


class RevokeServicePeriodPayloadTypeDef(TypedDict):
    programManagementAccountIdentifier: str
    note: NotRequired[str]


CreateChannelContractDetailTypeDef = TypedDict(
    "CreateChannelContractDetailTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
    },
)


class TagTypeDef(TypedDict):
    key: str
    value: str


CreateChannelHandshakeDetailTypeDef = TypedDict(
    "CreateChannelHandshakeDetailTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
    },
)
CreateProgramManagementAccountDetailTypeDef = TypedDict(
    "CreateProgramManagementAccountDetailTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
    },
)
CreateRelationshipDetailTypeDef = TypedDict(
    "CreateRelationshipDetailTypeDef",
    {
        "arn": NotRequired[str],
        "id": NotRequired[str],
    },
)
TimestampTypeDef = Union[datetime, str]


class DeleteProgramManagementAccountRequestTypeDef(TypedDict):
    catalog: str
    identifier: str
    clientToken: NotRequired[str]


class DeleteRelationshipRequestTypeDef(TypedDict):
    catalog: str
    identifier: str
    programManagementAccountIdentifier: str
    clientToken: NotRequired[str]


class GetChannelContractRequestTypeDef(TypedDict):
    catalog: str
    identifier: str


class GetRelationshipRequestTypeDef(TypedDict):
    catalog: str
    programManagementAccountIdentifier: str
    identifier: str


RelationshipDetailTypeDef = TypedDict(
    "RelationshipDetailTypeDef",
    {
        "arn": NotRequired[str],
        "id": NotRequired[str],
        "revision": NotRequired[str],
        "catalog": NotRequired[str],
        "associationType": NotRequired[AssociationTypeType],
        "programManagementAccountId": NotRequired[str],
        "associatedAccountId": NotRequired[str],
        "displayName": NotRequired[str],
        "resaleAccountModel": NotRequired[ResaleAccountModelType],
        "sector": NotRequired[SectorType],
        "accountScope": NotRequired[AccountScopeType],
        "channelContractId": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "startDate": NotRequired[datetime],
        "endDate": NotRequired[datetime],
    },
)


class ProgramManagementAccountHandshakeDetailTypeDef(TypedDict):
    program: NotRequired[ProgramType]


class RevokeServicePeriodHandshakeDetailTypeDef(TypedDict):
    note: NotRequired[str]
    servicePeriodType: NotRequired[ServicePeriodTypeType]
    minimumNoticeDays: NotRequired[str]
    startDate: NotRequired[datetime]
    endDate: NotRequired[datetime]


class StartServicePeriodHandshakeDetailTypeDef(TypedDict):
    note: NotRequired[str]
    servicePeriodType: NotRequired[ServicePeriodTypeType]
    minimumNoticeDays: NotRequired[str]
    startDate: NotRequired[datetime]
    endDate: NotRequired[datetime]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ManagedServicesAttestationTypeFiltersTypeDef(TypedDict):
    relationshipIdentifiers: NotRequired[Sequence[str]]
    legalEntityNames: NotRequired[Sequence[str]]


class ManagedServicesAttestationTypeSortTypeDef(TypedDict):
    sortOrder: SortOrderType
    sortBy: Literal["UpdatedAt"]


class ProgramManagementAccountTypeFiltersTypeDef(TypedDict):
    programs: NotRequired[Sequence[ProgramType]]


class RevokeServicePeriodTypeFiltersTypeDef(TypedDict):
    servicePeriodTypes: NotRequired[Sequence[ServicePeriodTypeType]]


class StartServicePeriodTypeFiltersTypeDef(TypedDict):
    servicePeriodTypes: NotRequired[Sequence[ServicePeriodTypeType]]


class ProgramManagementAccountTypeSortTypeDef(TypedDict):
    sortOrder: SortOrderType
    sortBy: Literal["UpdatedAt"]


class RevokeServicePeriodTypeSortTypeDef(TypedDict):
    sortOrder: SortOrderType
    sortBy: Literal["UpdatedAt"]


class StartServicePeriodTypeSortTypeDef(TypedDict):
    sortOrder: SortOrderType
    sortBy: Literal["UpdatedAt"]


class ListProgramManagementAccountsSortBaseTypeDef(TypedDict):
    sortOrder: SortOrderType
    sortBy: Literal["UpdatedAt"]


ProgramManagementAccountSummaryTypeDef = TypedDict(
    "ProgramManagementAccountSummaryTypeDef",
    {
        "id": NotRequired[str],
        "revision": NotRequired[str],
        "catalog": NotRequired[str],
        "program": NotRequired[ProgramType],
        "displayName": NotRequired[str],
        "accountId": NotRequired[str],
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "startDate": NotRequired[datetime],
        "status": NotRequired[ProgramManagementAccountStatusType],
        "type": NotRequired[ProgramManagementAccountTypeType],
    },
)


class ListRelationshipsSortBaseTypeDef(TypedDict):
    sortOrder: SortOrderType
    sortBy: Literal["UpdatedAt"]


RelationshipSummaryTypeDef = TypedDict(
    "RelationshipSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "id": NotRequired[str],
        "revision": NotRequired[str],
        "catalog": NotRequired[str],
        "associationType": NotRequired[AssociationTypeType],
        "programManagementAccountId": NotRequired[str],
        "associatedAccountId": NotRequired[str],
        "displayName": NotRequired[str],
        "sector": NotRequired[SectorType],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "startDate": NotRequired[datetime],
    },
)


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class PartnerLedSupportTypeDef(TypedDict):
    coverage: CoverageType
    tamLocation: str
    provider: NotRequired[ProviderType]


RejectChannelHandshakeDetailTypeDef = TypedDict(
    "RejectChannelHandshakeDetailTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "status": NotRequired[HandshakeStatusType],
    },
)


class RejectChannelHandshakeRequestTypeDef(TypedDict):
    catalog: str
    identifier: str


class ResoldEnterpriseTypeDef(TypedDict):
    coverage: CoverageType
    tamLocation: str
    chargeAccountId: NotRequired[str]


class ResoldUnifiedOperationsTypeDef(TypedDict):
    coverage: CoverageType
    tamLocation: str
    chargeAccountId: NotRequired[str]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


UpdateProgramManagementAccountDetailTypeDef = TypedDict(
    "UpdateProgramManagementAccountDetailTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "revision": NotRequired[str],
        "displayName": NotRequired[str],
    },
)


class UpdateProgramManagementAccountRequestTypeDef(TypedDict):
    catalog: str
    identifier: str
    revision: NotRequired[str]
    displayName: NotRequired[str]


UpdateRelationshipDetailTypeDef = TypedDict(
    "UpdateRelationshipDetailTypeDef",
    {
        "arn": NotRequired[str],
        "id": NotRequired[str],
        "revision": NotRequired[str],
        "displayName": NotRequired[str],
    },
)


class AcceptChannelHandshakeResponseTypeDef(TypedDict):
    channelHandshakeDetail: AcceptChannelHandshakeDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ManagedServicesAttestationDetailsTypeDef(TypedDict):
    legalEntityName: str
    relationshipIdentifier: str
    programManagementAccountIdentifier: str
    endDate: datetime
    supportedServices: list[ManagedServicesSupportedServiceType]
    signatoryName: str
    signatoryEmail: str
    memberAccountIds: NotRequired[list[str]]
    legalEntityAddress: NotRequired[AddressTypeDef]


class CancelChannelContractResponseTypeDef(TypedDict):
    channelContractDetail: CancelChannelContractDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CancelChannelHandshakeResponseTypeDef(TypedDict):
    channelHandshakeDetail: CancelChannelHandshakeDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ChannelContractSummaryDetailsTypeDef(TypedDict):
    managedServicesAttestationDetails: NotRequired[ManagedServicesAttestationSummaryDetailsTypeDef]


class CreateChannelContractResponseTypeDef(TypedDict):
    channelContractDetail: CreateChannelContractDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


CreateProgramManagementAccountRequestTypeDef = TypedDict(
    "CreateProgramManagementAccountRequestTypeDef",
    {
        "catalog": str,
        "program": ProgramType,
        "displayName": str,
        "accountId": str,
        "clientToken": NotRequired[str],
        "tags": NotRequired[Sequence[TagTypeDef]],
        "type": NotRequired[ProgramManagementAccountTypeType],
    },
)


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]


class CreateChannelHandshakeResponseTypeDef(TypedDict):
    channelHandshakeDetail: CreateChannelHandshakeDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProgramManagementAccountResponseTypeDef(TypedDict):
    programManagementAccountDetail: CreateProgramManagementAccountDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRelationshipResponseTypeDef(TypedDict):
    relationshipDetail: CreateRelationshipDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ManagedServicesAttestationPayloadTypeDef(TypedDict):
    legalEntityName: str
    relationshipIdentifier: str
    programManagementAccountIdentifier: str
    endDate: TimestampTypeDef
    supportedServices: Sequence[ManagedServicesSupportedServiceType]
    legalEntityAddress: AddressTypeDef
    signatoryName: str
    signatoryEmail: str
    memberAccountIds: NotRequired[Sequence[str]]


class StartServicePeriodPayloadTypeDef(TypedDict):
    programManagementAccountIdentifier: str
    servicePeriodType: ServicePeriodTypeType
    note: NotRequired[str]
    minimumNoticeDays: NotRequired[str]
    endDate: NotRequired[TimestampTypeDef]


class GetRelationshipResponseTypeDef(TypedDict):
    relationshipDetail: RelationshipDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class HandshakeDetailTypeDef(TypedDict):
    startServicePeriodHandshakeDetail: NotRequired[StartServicePeriodHandshakeDetailTypeDef]
    revokeServicePeriodHandshakeDetail: NotRequired[RevokeServicePeriodHandshakeDetailTypeDef]
    programManagementAccountHandshakeDetail: NotRequired[
        ProgramManagementAccountHandshakeDetailTypeDef
    ]


class ListChannelContractsTypeFiltersTypeDef(TypedDict):
    managedServicesAttestationTypeFilters: NotRequired[ManagedServicesAttestationTypeFiltersTypeDef]


class ListChannelContractsTypeSortTypeDef(TypedDict):
    managedServicesAttestationTypeSort: NotRequired[ManagedServicesAttestationTypeSortTypeDef]


class ListChannelHandshakesTypeFiltersTypeDef(TypedDict):
    startServicePeriodTypeFilters: NotRequired[StartServicePeriodTypeFiltersTypeDef]
    revokeServicePeriodTypeFilters: NotRequired[RevokeServicePeriodTypeFiltersTypeDef]
    programManagementAccountTypeFilters: NotRequired[ProgramManagementAccountTypeFiltersTypeDef]


class ListChannelHandshakesTypeSortTypeDef(TypedDict):
    startServicePeriodTypeSort: NotRequired[StartServicePeriodTypeSortTypeDef]
    revokeServicePeriodTypeSort: NotRequired[RevokeServicePeriodTypeSortTypeDef]
    programManagementAccountTypeSort: NotRequired[ProgramManagementAccountTypeSortTypeDef]


ListProgramManagementAccountsRequestPaginateTypeDef = TypedDict(
    "ListProgramManagementAccountsRequestPaginateTypeDef",
    {
        "catalog": str,
        "displayNames": NotRequired[Sequence[str]],
        "programs": NotRequired[Sequence[ProgramType]],
        "accountIds": NotRequired[Sequence[str]],
        "statuses": NotRequired[Sequence[ProgramManagementAccountStatusType]],
        "sort": NotRequired[ListProgramManagementAccountsSortBaseTypeDef],
        "type": NotRequired[ProgramManagementAccountTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListProgramManagementAccountsRequestTypeDef = TypedDict(
    "ListProgramManagementAccountsRequestTypeDef",
    {
        "catalog": str,
        "maxResults": NotRequired[int],
        "displayNames": NotRequired[Sequence[str]],
        "programs": NotRequired[Sequence[ProgramType]],
        "accountIds": NotRequired[Sequence[str]],
        "statuses": NotRequired[Sequence[ProgramManagementAccountStatusType]],
        "sort": NotRequired[ListProgramManagementAccountsSortBaseTypeDef],
        "nextToken": NotRequired[str],
        "type": NotRequired[ProgramManagementAccountTypeType],
    },
)


class ListProgramManagementAccountsResponseTypeDef(TypedDict):
    items: list[ProgramManagementAccountSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListRelationshipsRequestPaginateTypeDef(TypedDict):
    catalog: str
    associatedAccountIds: NotRequired[Sequence[str]]
    associationTypes: NotRequired[Sequence[AssociationTypeType]]
    displayNames: NotRequired[Sequence[str]]
    programManagementAccountIdentifiers: NotRequired[Sequence[str]]
    sort: NotRequired[ListRelationshipsSortBaseTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRelationshipsRequestTypeDef(TypedDict):
    catalog: str
    maxResults: NotRequired[int]
    associatedAccountIds: NotRequired[Sequence[str]]
    associationTypes: NotRequired[Sequence[AssociationTypeType]]
    displayNames: NotRequired[Sequence[str]]
    programManagementAccountIdentifiers: NotRequired[Sequence[str]]
    sort: NotRequired[ListRelationshipsSortBaseTypeDef]
    nextToken: NotRequired[str]


class ListRelationshipsResponseTypeDef(TypedDict):
    items: list[RelationshipSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RejectChannelHandshakeResponseTypeDef(TypedDict):
    channelHandshakeDetail: RejectChannelHandshakeDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SupportPlanTypeDef(TypedDict):
    resoldEnterprise: NotRequired[ResoldEnterpriseTypeDef]
    partnerLedSupport: NotRequired[PartnerLedSupportTypeDef]
    resoldUnifiedOperations: NotRequired[ResoldUnifiedOperationsTypeDef]


class UpdateProgramManagementAccountResponseTypeDef(TypedDict):
    programManagementAccountDetail: UpdateProgramManagementAccountDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRelationshipResponseTypeDef(TypedDict):
    relationshipDetail: UpdateRelationshipDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ChannelContractDetailsTypeDef(TypedDict):
    managedServicesAttestationDetails: NotRequired[ManagedServicesAttestationDetailsTypeDef]


ChannelContractSummaryTypeDef = TypedDict(
    "ChannelContractSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "catalog": str,
        "contractType": Literal["MANAGED_SERVICES_ATTESTATION"],
        "status": ChannelContractStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "details": ChannelContractSummaryDetailsTypeDef,
        "respondedAt": NotRequired[datetime],
    },
)


class ChannelContractPayloadTypeDef(TypedDict):
    managedServicesAttestationPayload: NotRequired[ManagedServicesAttestationPayloadTypeDef]


class ChannelHandshakePayloadTypeDef(TypedDict):
    startServicePeriodPayload: NotRequired[StartServicePeriodPayloadTypeDef]
    revokeServicePeriodPayload: NotRequired[RevokeServicePeriodPayloadTypeDef]


ChannelHandshakeSummaryTypeDef = TypedDict(
    "ChannelHandshakeSummaryTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "catalog": NotRequired[str],
        "handshakeType": NotRequired[HandshakeTypeType],
        "ownerAccountId": NotRequired[str],
        "senderAccountId": NotRequired[str],
        "senderDisplayName": NotRequired[str],
        "receiverAccountId": NotRequired[str],
        "associatedResourceId": NotRequired[str],
        "detail": NotRequired[HandshakeDetailTypeDef],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "status": NotRequired[HandshakeStatusType],
    },
)


class ListChannelContractsRequestPaginateTypeDef(TypedDict):
    catalog: str
    contractType: Literal["MANAGED_SERVICES_ATTESTATION"]
    statuses: NotRequired[Sequence[ChannelContractStatusType]]
    contractTypeFilters: NotRequired[ListChannelContractsTypeFiltersTypeDef]
    contractTypeSort: NotRequired[ListChannelContractsTypeSortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListChannelContractsRequestTypeDef(TypedDict):
    catalog: str
    contractType: Literal["MANAGED_SERVICES_ATTESTATION"]
    statuses: NotRequired[Sequence[ChannelContractStatusType]]
    contractTypeFilters: NotRequired[ListChannelContractsTypeFiltersTypeDef]
    contractTypeSort: NotRequired[ListChannelContractsTypeSortTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListChannelHandshakesRequestPaginateTypeDef(TypedDict):
    handshakeType: HandshakeTypeType
    catalog: str
    participantType: ParticipantTypeType
    statuses: NotRequired[Sequence[HandshakeStatusType]]
    associatedResourceIdentifiers: NotRequired[Sequence[str]]
    handshakeTypeFilters: NotRequired[ListChannelHandshakesTypeFiltersTypeDef]
    handshakeTypeSort: NotRequired[ListChannelHandshakesTypeSortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListChannelHandshakesRequestTypeDef(TypedDict):
    handshakeType: HandshakeTypeType
    catalog: str
    participantType: ParticipantTypeType
    maxResults: NotRequired[int]
    statuses: NotRequired[Sequence[HandshakeStatusType]]
    associatedResourceIdentifiers: NotRequired[Sequence[str]]
    handshakeTypeFilters: NotRequired[ListChannelHandshakesTypeFiltersTypeDef]
    handshakeTypeSort: NotRequired[ListChannelHandshakesTypeSortTypeDef]
    nextToken: NotRequired[str]


class CreateRelationshipRequestTypeDef(TypedDict):
    catalog: str
    associationType: AssociationTypeType
    programManagementAccountIdentifier: str
    displayName: str
    sector: SectorType
    associatedAccountId: NotRequired[str]
    resaleAccountModel: NotRequired[ResaleAccountModelType]
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    requestedSupportPlan: NotRequired[SupportPlanTypeDef]
    accountScope: NotRequired[AccountScopeType]
    startDate: NotRequired[TimestampTypeDef]


class UpdateRelationshipRequestTypeDef(TypedDict):
    catalog: str
    identifier: str
    programManagementAccountIdentifier: str
    revision: NotRequired[str]
    displayName: NotRequired[str]
    requestedSupportPlan: NotRequired[SupportPlanTypeDef]


ChannelContractDetailTypeDef = TypedDict(
    "ChannelContractDetailTypeDef",
    {
        "id": str,
        "arn": str,
        "catalog": str,
        "contractType": Literal["MANAGED_SERVICES_ATTESTATION"],
        "status": ChannelContractStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "details": ChannelContractDetailsTypeDef,
        "respondedAt": NotRequired[datetime],
        "cancellationReason": NotRequired[str],
    },
)


class ListChannelContractsResponseTypeDef(TypedDict):
    items: list[ChannelContractSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateChannelContractRequestTypeDef(TypedDict):
    contractType: Literal["MANAGED_SERVICES_ATTESTATION"]
    catalog: str
    payload: ChannelContractPayloadTypeDef
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateChannelHandshakeRequestTypeDef(TypedDict):
    handshakeType: HandshakeTypeType
    catalog: str
    associatedResourceIdentifier: str
    payload: NotRequired[ChannelHandshakePayloadTypeDef]
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class ListChannelHandshakesResponseTypeDef(TypedDict):
    items: list[ChannelHandshakeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetChannelContractResponseTypeDef(TypedDict):
    channelContractDetail: ChannelContractDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
