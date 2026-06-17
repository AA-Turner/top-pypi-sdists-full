"""
Type annotations for outposts service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_outposts/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_outposts.type_defs import AddressTypeDef

    data: AddressTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AddressTypeType,
    AssetStateType,
    AssetTypeType,
    AWSServiceNameType,
    BlockingResourceTypeType,
    CapacityTaskFailureTypeType,
    CapacityTaskStatusType,
    CatalogItemClassType,
    CatalogItemStatusType,
    ComputeAssetStateType,
    DecommissionRequestStatusType,
    FiberOpticCableTypeType,
    FormFactorType,
    LineItemStatusType,
    MaximumSupportedWeightLbsType,
    OpticalStandardType,
    OrderingRequirementStatusType,
    OrderingRequirementTypeType,
    OrderStatusType,
    OrderTypeType,
    OutpostGenerationType,
    PaymentOptionType,
    PaymentTermType,
    PowerConnectorType,
    PowerDrawKvaType,
    PowerFeedDropType,
    PowerPhaseType,
    PricingResultType,
    QuoteCapacityTypeType,
    QuoteConstraintTypeType,
    QuoteRackUseTypeType,
    QuoteSpecificationTypeType,
    QuoteStatusType,
    RackUnitHeightType,
    ShipmentCarrierType,
    SubscriptionStatusType,
    SubscriptionTypeType,
    SupportedHardwareTypeType,
    SupportedStorageEnumType,
    TaskActionOnBlockingInstancesType,
    UplinkCountType,
    UplinkGbpsType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AddressTypeDef",
    "AssetInfoTypeDef",
    "AssetInstanceTypeCapacityTypeDef",
    "AssetInstanceTypeDef",
    "AssetLocationTypeDef",
    "BlockingInstanceTypeDef",
    "CancelCapacityTaskInputTypeDef",
    "CancelOrderInputTypeDef",
    "CapacitySummaryTypeDef",
    "CapacityTaskFailureTypeDef",
    "CapacityTaskSummaryTypeDef",
    "CatalogItemTypeDef",
    "ComputeAttributesTypeDef",
    "ConnectionDetailsTypeDef",
    "CreateOrderInputTypeDef",
    "CreateOrderOutputTypeDef",
    "CreateOutpostInputTypeDef",
    "CreateOutpostOutputTypeDef",
    "CreateQuoteInputTypeDef",
    "CreateQuoteOutputTypeDef",
    "CreateRenewalInputTypeDef",
    "CreateRenewalOutputTypeDef",
    "CreateSiteInputTypeDef",
    "CreateSiteOutputTypeDef",
    "DeleteOutpostInputTypeDef",
    "DeleteQuoteInputTypeDef",
    "DeleteSiteInputTypeDef",
    "DetailedInstanceTypeItemTypeDef",
    "EC2CapacityTypeDef",
    "FormFactorConfigTypeDef",
    "GetCapacityTaskInputTypeDef",
    "GetCapacityTaskOutputTypeDef",
    "GetCatalogItemInputTypeDef",
    "GetCatalogItemOutputTypeDef",
    "GetConnectionRequestTypeDef",
    "GetConnectionResponseTypeDef",
    "GetOrderInputTypeDef",
    "GetOrderOutputTypeDef",
    "GetOutpostBillingInformationInputPaginateTypeDef",
    "GetOutpostBillingInformationInputTypeDef",
    "GetOutpostBillingInformationOutputTypeDef",
    "GetOutpostInputTypeDef",
    "GetOutpostInstanceTypesInputPaginateTypeDef",
    "GetOutpostInstanceTypesInputTypeDef",
    "GetOutpostInstanceTypesOutputTypeDef",
    "GetOutpostOutputTypeDef",
    "GetOutpostSupportedInstanceTypesInputPaginateTypeDef",
    "GetOutpostSupportedInstanceTypesInputTypeDef",
    "GetOutpostSupportedInstanceTypesOutputTypeDef",
    "GetQuoteInputTypeDef",
    "GetQuoteOutputTypeDef",
    "GetRenewalPricingInputTypeDef",
    "GetRenewalPricingOutputTypeDef",
    "GetSiteAddressInputTypeDef",
    "GetSiteAddressOutputTypeDef",
    "GetSiteInputTypeDef",
    "GetSiteOutputTypeDef",
    "InstanceTypeCapacityTypeDef",
    "InstanceTypeItemTypeDef",
    "InstancesToExcludeOutputTypeDef",
    "InstancesToExcludeTypeDef",
    "InstancesToExcludeUnionTypeDef",
    "LineItemAssetInformationTypeDef",
    "LineItemRequestTypeDef",
    "LineItemTypeDef",
    "ListAssetInstancesInputPaginateTypeDef",
    "ListAssetInstancesInputTypeDef",
    "ListAssetInstancesOutputTypeDef",
    "ListAssetsInputPaginateTypeDef",
    "ListAssetsInputTypeDef",
    "ListAssetsOutputTypeDef",
    "ListBlockingInstancesForCapacityTaskInputPaginateTypeDef",
    "ListBlockingInstancesForCapacityTaskInputTypeDef",
    "ListBlockingInstancesForCapacityTaskOutputTypeDef",
    "ListCapacityTasksInputPaginateTypeDef",
    "ListCapacityTasksInputTypeDef",
    "ListCapacityTasksOutputTypeDef",
    "ListCatalogItemsInputPaginateTypeDef",
    "ListCatalogItemsInputTypeDef",
    "ListCatalogItemsOutputTypeDef",
    "ListOrderableInstanceTypesInputPaginateTypeDef",
    "ListOrderableInstanceTypesInputTypeDef",
    "ListOrderableInstanceTypesOutputTypeDef",
    "ListOrdersInputPaginateTypeDef",
    "ListOrdersInputTypeDef",
    "ListOrdersOutputTypeDef",
    "ListOutpostsInputPaginateTypeDef",
    "ListOutpostsInputTypeDef",
    "ListOutpostsOutputTypeDef",
    "ListQuotesInputPaginateTypeDef",
    "ListQuotesInputTypeDef",
    "ListQuotesOutputTypeDef",
    "ListSitesInputPaginateTypeDef",
    "ListSitesInputTypeDef",
    "ListSitesOutputTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "OrderSummaryTypeDef",
    "OrderTypeDef",
    "OrderingRequirementTypeDef",
    "OutpostTypeDef",
    "PaginatorConfigTypeDef",
    "PricingOptionTypeDef",
    "QuoteCapacityTypeDef",
    "QuoteConstraintTypeDef",
    "QuoteOptionTypeDef",
    "QuoteSpecificationTypeDef",
    "QuoteSummaryTypeDef",
    "QuoteTypeDef",
    "RackPhysicalPropertiesTypeDef",
    "RackSpecificationDetailsTypeDef",
    "ResponseMetadataTypeDef",
    "ServerSpecificationDetailsTypeDef",
    "ShipmentInformationTypeDef",
    "SiteTypeDef",
    "StartCapacityTaskInputTypeDef",
    "StartCapacityTaskOutputTypeDef",
    "StartConnectionRequestTypeDef",
    "StartConnectionResponseTypeDef",
    "StartOutpostDecommissionInputTypeDef",
    "StartOutpostDecommissionOutputTypeDef",
    "SubscriptionPricingDetailsTypeDef",
    "SubscriptionTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateOutpostInputTypeDef",
    "UpdateOutpostOutputTypeDef",
    "UpdateQuoteInputTypeDef",
    "UpdateQuoteOutputTypeDef",
    "UpdateSiteAddressInputTypeDef",
    "UpdateSiteAddressOutputTypeDef",
    "UpdateSiteInputTypeDef",
    "UpdateSiteOutputTypeDef",
    "UpdateSiteRackPhysicalPropertiesInputTypeDef",
    "UpdateSiteRackPhysicalPropertiesOutputTypeDef",
)

class AddressTypeDef(TypedDict):
    ContactName: str
    ContactPhoneNumber: str
    AddressLine1: str
    City: str
    StateOrRegion: str
    PostalCode: str
    CountryCode: str
    AddressLine2: NotRequired[str]
    AddressLine3: NotRequired[str]
    DistrictOrCounty: NotRequired[str]
    Municipality: NotRequired[str]

class AssetLocationTypeDef(TypedDict):
    RackElevation: NotRequired[float]

class AssetInstanceTypeCapacityTypeDef(TypedDict):
    InstanceType: str
    Count: int

class AssetInstanceTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    InstanceType: NotRequired[str]
    AssetId: NotRequired[str]
    AccountId: NotRequired[str]
    AwsServiceName: NotRequired[AWSServiceNameType]

class BlockingInstanceTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    AccountId: NotRequired[str]
    AwsServiceName: NotRequired[AWSServiceNameType]

class CancelCapacityTaskInputTypeDef(TypedDict):
    CapacityTaskId: str
    OutpostIdentifier: str

class CancelOrderInputTypeDef(TypedDict):
    OrderId: str

class QuoteCapacityTypeDef(TypedDict):
    QuoteCapacityType: NotRequired[QuoteCapacityTypeType]
    Unit: NotRequired[str]
    Quantity: NotRequired[float]

CapacityTaskFailureTypeDef = TypedDict(
    "CapacityTaskFailureTypeDef",
    {
        "Reason": str,
        "Type": NotRequired[CapacityTaskFailureTypeType],
    },
)

class CapacityTaskSummaryTypeDef(TypedDict):
    CapacityTaskId: NotRequired[str]
    OutpostId: NotRequired[str]
    OrderId: NotRequired[str]
    AssetId: NotRequired[str]
    CapacityTaskStatus: NotRequired[CapacityTaskStatusType]
    CreationDate: NotRequired[datetime]
    CompletionDate: NotRequired[datetime]
    LastModifiedDate: NotRequired[datetime]

class EC2CapacityTypeDef(TypedDict):
    Family: NotRequired[str]
    MaxSize: NotRequired[str]
    Quantity: NotRequired[str]

class ConnectionDetailsTypeDef(TypedDict):
    ClientPublicKey: NotRequired[str]
    ServerPublicKey: NotRequired[str]
    ServerEndpoint: NotRequired[str]
    ClientTunnelAddress: NotRequired[str]
    ServerTunnelAddress: NotRequired[str]
    AllowedIps: NotRequired[list[str]]

class LineItemRequestTypeDef(TypedDict):
    CatalogItemId: NotRequired[str]
    Quantity: NotRequired[int]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateOutpostInputTypeDef(TypedDict):
    Name: str
    SiteId: str
    Description: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    SupportedHardwareType: NotRequired[SupportedHardwareTypeType]

class OutpostTypeDef(TypedDict):
    OutpostId: NotRequired[str]
    OwnerId: NotRequired[str]
    OutpostArn: NotRequired[str]
    SiteId: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    LifeCycleStatus: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    Tags: NotRequired[dict[str, str]]
    SiteArn: NotRequired[str]
    SupportedHardwareType: NotRequired[SupportedHardwareTypeType]

class QuoteConstraintTypeDef(TypedDict):
    QuoteConstraintType: NotRequired[QuoteConstraintTypeType]
    Value: NotRequired[str]

class CreateRenewalInputTypeDef(TypedDict):
    PaymentOption: PaymentOptionType
    PaymentTerm: PaymentTermType
    OutpostIdentifier: str
    ClientToken: NotRequired[str]

class RackPhysicalPropertiesTypeDef(TypedDict):
    PowerDrawKva: NotRequired[PowerDrawKvaType]
    PowerPhase: NotRequired[PowerPhaseType]
    PowerConnector: NotRequired[PowerConnectorType]
    PowerFeedDrop: NotRequired[PowerFeedDropType]
    UplinkGbps: NotRequired[UplinkGbpsType]
    UplinkCount: NotRequired[UplinkCountType]
    FiberOpticCableType: NotRequired[FiberOpticCableTypeType]
    OpticalStandard: NotRequired[OpticalStandardType]
    MaximumSupportedWeightLbs: NotRequired[MaximumSupportedWeightLbsType]

class DeleteOutpostInputTypeDef(TypedDict):
    OutpostId: str

class DeleteQuoteInputTypeDef(TypedDict):
    QuoteIdentifier: str

class DeleteSiteInputTypeDef(TypedDict):
    SiteId: str

class FormFactorConfigTypeDef(TypedDict):
    FormFactor: NotRequired[FormFactorType]
    OutpostGeneration: NotRequired[OutpostGenerationType]

class GetCapacityTaskInputTypeDef(TypedDict):
    CapacityTaskId: str
    OutpostIdentifier: str

class InstanceTypeCapacityTypeDef(TypedDict):
    InstanceType: str
    Count: int

class InstancesToExcludeOutputTypeDef(TypedDict):
    Instances: NotRequired[list[str]]
    AccountIds: NotRequired[list[str]]
    Services: NotRequired[list[AWSServiceNameType]]

class GetCatalogItemInputTypeDef(TypedDict):
    CatalogItemId: str

class GetConnectionRequestTypeDef(TypedDict):
    ConnectionId: str

class GetOrderInputTypeDef(TypedDict):
    OrderId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class GetOutpostBillingInformationInputTypeDef(TypedDict):
    OutpostIdentifier: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class SubscriptionTypeDef(TypedDict):
    SubscriptionId: NotRequired[str]
    SubscriptionType: NotRequired[SubscriptionTypeType]
    SubscriptionStatus: NotRequired[SubscriptionStatusType]
    OrderIds: NotRequired[list[str]]
    BeginDate: NotRequired[datetime]
    EndDate: NotRequired[datetime]
    Currency: NotRequired[Literal["USD"]]
    MonthlyRecurringPrice: NotRequired[float]
    UpfrontPrice: NotRequired[float]

class GetOutpostInputTypeDef(TypedDict):
    OutpostId: str

class GetOutpostInstanceTypesInputTypeDef(TypedDict):
    OutpostId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class InstanceTypeItemTypeDef(TypedDict):
    InstanceType: NotRequired[str]
    VCPUs: NotRequired[int]

class GetOutpostSupportedInstanceTypesInputTypeDef(TypedDict):
    OutpostIdentifier: str
    OrderId: NotRequired[str]
    AssetId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class GetQuoteInputTypeDef(TypedDict):
    QuoteIdentifier: str

class GetRenewalPricingInputTypeDef(TypedDict):
    OutpostIdentifier: str

class GetSiteAddressInputTypeDef(TypedDict):
    SiteId: str
    AddressType: AddressTypeType

class GetSiteInputTypeDef(TypedDict):
    SiteId: str

class InstancesToExcludeTypeDef(TypedDict):
    Instances: NotRequired[Sequence[str]]
    AccountIds: NotRequired[Sequence[str]]
    Services: NotRequired[Sequence[AWSServiceNameType]]

class LineItemAssetInformationTypeDef(TypedDict):
    AssetId: NotRequired[str]
    MacAddressList: NotRequired[list[str]]

class ShipmentInformationTypeDef(TypedDict):
    ShipmentTrackingNumber: NotRequired[str]
    ShipmentCarrier: NotRequired[ShipmentCarrierType]

class ListAssetInstancesInputTypeDef(TypedDict):
    OutpostIdentifier: str
    AssetIdFilter: NotRequired[Sequence[str]]
    InstanceTypeFilter: NotRequired[Sequence[str]]
    AccountIdFilter: NotRequired[Sequence[str]]
    AwsServiceFilter: NotRequired[Sequence[AWSServiceNameType]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAssetsInputTypeDef(TypedDict):
    OutpostIdentifier: str
    HostIdFilter: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    StatusFilter: NotRequired[Sequence[AssetStateType]]
    AssetTypeFilter: NotRequired[Sequence[AssetTypeType]]

class ListBlockingInstancesForCapacityTaskInputTypeDef(TypedDict):
    OutpostIdentifier: str
    CapacityTaskId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCapacityTasksInputTypeDef(TypedDict):
    OutpostIdentifierFilter: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    CapacityTaskStatusFilter: NotRequired[Sequence[CapacityTaskStatusType]]

class ListCatalogItemsInputTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ItemClassFilter: NotRequired[Sequence[CatalogItemClassType]]
    SupportedStorageFilter: NotRequired[Sequence[SupportedStorageEnumType]]
    EC2FamilyFilter: NotRequired[Sequence[str]]

class ListOrderableInstanceTypesInputTypeDef(TypedDict):
    OutpostGenerationFilter: NotRequired[OutpostGenerationType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListOrdersInputTypeDef(TypedDict):
    OutpostIdentifierFilter: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class OrderSummaryTypeDef(TypedDict):
    OutpostId: NotRequired[str]
    OrderId: NotRequired[str]
    OrderType: NotRequired[OrderTypeType]
    Status: NotRequired[OrderStatusType]
    LineItemCountsByStatus: NotRequired[dict[LineItemStatusType, int]]
    OrderSubmissionDate: NotRequired[datetime]
    OrderFulfilledDate: NotRequired[datetime]

class ListOutpostsInputTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    LifeCycleStatusFilter: NotRequired[Sequence[str]]
    AvailabilityZoneFilter: NotRequired[Sequence[str]]
    AvailabilityZoneIdFilter: NotRequired[Sequence[str]]

class ListQuotesInputTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListSitesInputTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    OperatingAddressCountryCodeFilter: NotRequired[Sequence[str]]
    OperatingAddressStateOrRegionFilter: NotRequired[Sequence[str]]
    OperatingAddressCityFilter: NotRequired[Sequence[str]]

class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str

class OrderingRequirementTypeDef(TypedDict):
    StatusMessage: NotRequired[str]
    OrderingRequirementType: NotRequired[OrderingRequirementTypeType]
    Status: NotRequired[OrderingRequirementStatusType]

class SubscriptionPricingDetailsTypeDef(TypedDict):
    PaymentOption: NotRequired[PaymentOptionType]
    PaymentTerm: NotRequired[PaymentTermType]
    UpfrontPrice: NotRequired[float]
    MonthlyRecurringPrice: NotRequired[float]
    Currency: NotRequired[Literal["USD"]]

class StartConnectionRequestTypeDef(TypedDict):
    AssetId: str
    ClientPublicKey: str
    NetworkInterfaceDeviceIndex: int
    DeviceSerialNumber: NotRequired[str]

class StartOutpostDecommissionInputTypeDef(TypedDict):
    OutpostIdentifier: str
    ValidateOnly: NotRequired[bool]

class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateOutpostInputTypeDef(TypedDict):
    OutpostId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    SupportedHardwareType: NotRequired[SupportedHardwareTypeType]

class UpdateSiteInputTypeDef(TypedDict):
    SiteId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    Notes: NotRequired[str]

class UpdateSiteRackPhysicalPropertiesInputTypeDef(TypedDict):
    SiteId: str
    PowerDrawKva: NotRequired[PowerDrawKvaType]
    PowerPhase: NotRequired[PowerPhaseType]
    PowerConnector: NotRequired[PowerConnectorType]
    PowerFeedDrop: NotRequired[PowerFeedDropType]
    UplinkGbps: NotRequired[UplinkGbpsType]
    UplinkCount: NotRequired[UplinkCountType]
    FiberOpticCableType: NotRequired[FiberOpticCableTypeType]
    OpticalStandard: NotRequired[OpticalStandardType]
    MaximumSupportedWeightLbs: NotRequired[MaximumSupportedWeightLbsType]

class UpdateSiteAddressInputTypeDef(TypedDict):
    SiteId: str
    AddressType: AddressTypeType
    Address: AddressTypeDef

class ComputeAttributesTypeDef(TypedDict):
    HostId: NotRequired[str]
    State: NotRequired[ComputeAssetStateType]
    InstanceFamilies: NotRequired[list[str]]
    InstanceTypeCapacities: NotRequired[list[AssetInstanceTypeCapacityTypeDef]]
    MaxVcpus: NotRequired[int]

class CapacitySummaryTypeDef(TypedDict):
    ExistingCapacities: NotRequired[list[QuoteCapacityTypeDef]]
    FinalCapacities: NotRequired[list[QuoteCapacityTypeDef]]
    CapacityChange: NotRequired[list[QuoteCapacityTypeDef]]

class CatalogItemTypeDef(TypedDict):
    CatalogItemId: NotRequired[str]
    ItemStatus: NotRequired[CatalogItemStatusType]
    EC2Capacities: NotRequired[list[EC2CapacityTypeDef]]
    PowerKva: NotRequired[float]
    WeightLbs: NotRequired[int]
    SupportedUplinkGbps: NotRequired[list[int]]
    SupportedStorage: NotRequired[list[SupportedStorageEnumType]]

class RackSpecificationDetailsTypeDef(TypedDict):
    RackId: NotRequired[str]
    RackUse: NotRequired[QuoteRackUseTypeType]
    RackPowerDrawKva: NotRequired[float]
    RackWeightLbs: NotRequired[float]
    RackHeightInches: NotRequired[float]
    RackWidthInches: NotRequired[float]
    RackDepthInches: NotRequired[float]
    RackUnitHeight: NotRequired[RackUnitHeightType]
    EC2Capacities: NotRequired[list[EC2CapacityTypeDef]]

class ServerSpecificationDetailsTypeDef(TypedDict):
    ServerPowerDrawKva: NotRequired[float]
    ServerWeightLbs: NotRequired[float]
    ServerHeightInches: NotRequired[float]
    ServerWidthInches: NotRequired[float]
    ServerDepthInches: NotRequired[float]
    RackUnitHeight: NotRequired[RackUnitHeightType]
    EC2Capacities: NotRequired[list[EC2CapacityTypeDef]]

class CreateOrderInputTypeDef(TypedDict):
    OutpostIdentifier: str
    PaymentOption: PaymentOptionType
    QuoteIdentifier: NotRequired[str]
    QuoteOptionIdentifier: NotRequired[str]
    LineItems: NotRequired[Sequence[LineItemRequestTypeDef]]
    PaymentTerm: NotRequired[PaymentTermType]

class CreateRenewalOutputTypeDef(TypedDict):
    PaymentOption: PaymentOptionType
    PaymentTerm: PaymentTermType
    OutpostId: str
    UpfrontPrice: float
    MonthlyRecurringPrice: float
    Currency: Literal["USD"]
    ResponseMetadata: ResponseMetadataTypeDef

class GetConnectionResponseTypeDef(TypedDict):
    ConnectionId: str
    ConnectionDetails: ConnectionDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSiteAddressOutputTypeDef(TypedDict):
    SiteId: str
    AddressType: AddressTypeType
    Address: AddressTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAssetInstancesOutputTypeDef(TypedDict):
    AssetInstances: list[AssetInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListBlockingInstancesForCapacityTaskOutputTypeDef(TypedDict):
    BlockingInstances: list[BlockingInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCapacityTasksOutputTypeDef(TypedDict):
    CapacityTasks: list[CapacityTaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartConnectionResponseTypeDef(TypedDict):
    ConnectionId: str
    UnderlayIpAddress: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartOutpostDecommissionOutputTypeDef(TypedDict):
    Status: DecommissionRequestStatusType
    BlockingResourceTypes: list[BlockingResourceTypeType]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSiteAddressOutputTypeDef(TypedDict):
    AddressType: AddressTypeType
    Address: AddressTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateOutpostOutputTypeDef(TypedDict):
    Outpost: OutpostTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetOutpostOutputTypeDef(TypedDict):
    Outpost: OutpostTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListOutpostsOutputTypeDef(TypedDict):
    Outposts: list[OutpostTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateOutpostOutputTypeDef(TypedDict):
    Outpost: OutpostTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateQuoteInputTypeDef(TypedDict):
    CountryCode: str
    RequestedCapacities: Sequence[QuoteCapacityTypeDef]
    OutpostIdentifier: NotRequired[str]
    RequestedConstraints: NotRequired[Sequence[QuoteConstraintTypeDef]]
    RequestedPaymentOptions: NotRequired[Sequence[PaymentOptionType]]
    RequestedPaymentTerms: NotRequired[Sequence[PaymentTermType]]
    Description: NotRequired[str]

class UpdateQuoteInputTypeDef(TypedDict):
    QuoteIdentifier: str
    OutpostIdentifier: NotRequired[str]
    CountryCode: NotRequired[str]
    RequestedCapacities: NotRequired[Sequence[QuoteCapacityTypeDef]]
    RequestedConstraints: NotRequired[Sequence[QuoteConstraintTypeDef]]
    RequestedPaymentOptions: NotRequired[Sequence[PaymentOptionType]]
    RequestedPaymentTerms: NotRequired[Sequence[PaymentTermType]]
    Description: NotRequired[str]

class CreateSiteInputTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    Notes: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    OperatingAddress: NotRequired[AddressTypeDef]
    ShippingAddress: NotRequired[AddressTypeDef]
    RackPhysicalProperties: NotRequired[RackPhysicalPropertiesTypeDef]

class SiteTypeDef(TypedDict):
    SiteId: NotRequired[str]
    AccountId: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[dict[str, str]]
    SiteArn: NotRequired[str]
    Notes: NotRequired[str]
    OperatingAddressCountryCode: NotRequired[str]
    OperatingAddressStateOrRegion: NotRequired[str]
    OperatingAddressCity: NotRequired[str]
    RackPhysicalProperties: NotRequired[RackPhysicalPropertiesTypeDef]

class DetailedInstanceTypeItemTypeDef(TypedDict):
    InstanceType: NotRequired[str]
    VCPUs: NotRequired[int]
    MemoryInMib: NotRequired[int]
    NetworkPerformance: NotRequired[str]
    FormFactorConfigs: NotRequired[list[FormFactorConfigTypeDef]]

class GetCapacityTaskOutputTypeDef(TypedDict):
    CapacityTaskId: str
    OutpostId: str
    OrderId: str
    AssetId: str
    RequestedInstancePools: list[InstanceTypeCapacityTypeDef]
    InstancesToExclude: InstancesToExcludeOutputTypeDef
    DryRun: bool
    CapacityTaskStatus: CapacityTaskStatusType
    Failed: CapacityTaskFailureTypeDef
    CreationDate: datetime
    CompletionDate: datetime
    LastModifiedDate: datetime
    TaskActionOnBlockingInstances: TaskActionOnBlockingInstancesType
    ResponseMetadata: ResponseMetadataTypeDef

class StartCapacityTaskOutputTypeDef(TypedDict):
    CapacityTaskId: str
    OutpostId: str
    OrderId: str
    AssetId: str
    RequestedInstancePools: list[InstanceTypeCapacityTypeDef]
    InstancesToExclude: InstancesToExcludeOutputTypeDef
    DryRun: bool
    CapacityTaskStatus: CapacityTaskStatusType
    Failed: CapacityTaskFailureTypeDef
    CreationDate: datetime
    CompletionDate: datetime
    LastModifiedDate: datetime
    TaskActionOnBlockingInstances: TaskActionOnBlockingInstancesType
    ResponseMetadata: ResponseMetadataTypeDef

class GetOutpostBillingInformationInputPaginateTypeDef(TypedDict):
    OutpostIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetOutpostInstanceTypesInputPaginateTypeDef(TypedDict):
    OutpostId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetOutpostSupportedInstanceTypesInputPaginateTypeDef(TypedDict):
    OutpostIdentifier: str
    OrderId: NotRequired[str]
    AssetId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAssetInstancesInputPaginateTypeDef(TypedDict):
    OutpostIdentifier: str
    AssetIdFilter: NotRequired[Sequence[str]]
    InstanceTypeFilter: NotRequired[Sequence[str]]
    AccountIdFilter: NotRequired[Sequence[str]]
    AwsServiceFilter: NotRequired[Sequence[AWSServiceNameType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAssetsInputPaginateTypeDef(TypedDict):
    OutpostIdentifier: str
    HostIdFilter: NotRequired[Sequence[str]]
    StatusFilter: NotRequired[Sequence[AssetStateType]]
    AssetTypeFilter: NotRequired[Sequence[AssetTypeType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListBlockingInstancesForCapacityTaskInputPaginateTypeDef(TypedDict):
    OutpostIdentifier: str
    CapacityTaskId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCapacityTasksInputPaginateTypeDef(TypedDict):
    OutpostIdentifierFilter: NotRequired[str]
    CapacityTaskStatusFilter: NotRequired[Sequence[CapacityTaskStatusType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCatalogItemsInputPaginateTypeDef(TypedDict):
    ItemClassFilter: NotRequired[Sequence[CatalogItemClassType]]
    SupportedStorageFilter: NotRequired[Sequence[SupportedStorageEnumType]]
    EC2FamilyFilter: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOrderableInstanceTypesInputPaginateTypeDef(TypedDict):
    OutpostGenerationFilter: NotRequired[OutpostGenerationType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOrdersInputPaginateTypeDef(TypedDict):
    OutpostIdentifierFilter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOutpostsInputPaginateTypeDef(TypedDict):
    LifeCycleStatusFilter: NotRequired[Sequence[str]]
    AvailabilityZoneFilter: NotRequired[Sequence[str]]
    AvailabilityZoneIdFilter: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQuotesInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSitesInputPaginateTypeDef(TypedDict):
    OperatingAddressCountryCodeFilter: NotRequired[Sequence[str]]
    OperatingAddressStateOrRegionFilter: NotRequired[Sequence[str]]
    OperatingAddressCityFilter: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetOutpostBillingInformationOutputTypeDef(TypedDict):
    Subscriptions: list[SubscriptionTypeDef]
    ContractEndDate: str
    PaymentTerm: PaymentTermType
    PaymentOption: PaymentOptionType
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetOutpostInstanceTypesOutputTypeDef(TypedDict):
    InstanceTypes: list[InstanceTypeItemTypeDef]
    OutpostId: str
    OutpostArn: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetOutpostSupportedInstanceTypesOutputTypeDef(TypedDict):
    InstanceTypes: list[InstanceTypeItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

InstancesToExcludeUnionTypeDef = Union[InstancesToExcludeTypeDef, InstancesToExcludeOutputTypeDef]

class LineItemTypeDef(TypedDict):
    CatalogItemId: NotRequired[str]
    LineItemId: NotRequired[str]
    Quantity: NotRequired[int]
    Status: NotRequired[LineItemStatusType]
    ShipmentInformation: NotRequired[ShipmentInformationTypeDef]
    AssetInformationList: NotRequired[list[LineItemAssetInformationTypeDef]]
    PreviousLineItemId: NotRequired[str]
    PreviousOrderId: NotRequired[str]

class ListOrdersOutputTypeDef(TypedDict):
    Orders: list[OrderSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PricingOptionTypeDef(TypedDict):
    PricingType: NotRequired[Literal["SUBSCRIPTION"]]
    SubscriptionPricingDetails: NotRequired[SubscriptionPricingDetailsTypeDef]

class AssetInfoTypeDef(TypedDict):
    AssetId: NotRequired[str]
    RackId: NotRequired[str]
    AssetType: NotRequired[AssetTypeType]
    ComputeAttributes: NotRequired[ComputeAttributesTypeDef]
    AssetLocation: NotRequired[AssetLocationTypeDef]

class GetCatalogItemOutputTypeDef(TypedDict):
    CatalogItem: CatalogItemTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListCatalogItemsOutputTypeDef(TypedDict):
    CatalogItems: list[CatalogItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class QuoteSpecificationTypeDef(TypedDict):
    QuoteSpecificationType: NotRequired[QuoteSpecificationTypeType]
    ExistingRackSpecificationDetails: NotRequired[RackSpecificationDetailsTypeDef]
    FinalRackSpecificationDetails: NotRequired[RackSpecificationDetailsTypeDef]
    ServerSpecificationDetails: NotRequired[ServerSpecificationDetailsTypeDef]

class CreateSiteOutputTypeDef(TypedDict):
    Site: SiteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSiteOutputTypeDef(TypedDict):
    Site: SiteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListSitesOutputTypeDef(TypedDict):
    Sites: list[SiteTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateSiteOutputTypeDef(TypedDict):
    Site: SiteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSiteRackPhysicalPropertiesOutputTypeDef(TypedDict):
    Site: SiteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListOrderableInstanceTypesOutputTypeDef(TypedDict):
    InstanceTypes: list[DetailedInstanceTypeItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class StartCapacityTaskInputTypeDef(TypedDict):
    OutpostIdentifier: str
    InstancePools: Sequence[InstanceTypeCapacityTypeDef]
    OrderId: NotRequired[str]
    AssetId: NotRequired[str]
    InstancesToExclude: NotRequired[InstancesToExcludeUnionTypeDef]
    DryRun: NotRequired[bool]
    TaskActionOnBlockingInstances: NotRequired[TaskActionOnBlockingInstancesType]

class OrderTypeDef(TypedDict):
    OutpostId: NotRequired[str]
    QuoteIdentifier: NotRequired[str]
    QuoteOptionIdentifier: NotRequired[str]
    OrderId: NotRequired[str]
    Status: NotRequired[OrderStatusType]
    LineItems: NotRequired[list[LineItemTypeDef]]
    PaymentOption: NotRequired[PaymentOptionType]
    OrderSubmissionDate: NotRequired[datetime]
    OrderFulfilledDate: NotRequired[datetime]
    PaymentTerm: NotRequired[PaymentTermType]
    OrderType: NotRequired[OrderTypeType]

class GetRenewalPricingOutputTypeDef(TypedDict):
    PricingResult: PricingResultType
    PricingOptions: list[PricingOptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListAssetsOutputTypeDef(TypedDict):
    Assets: list[AssetInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class QuoteOptionTypeDef(TypedDict):
    QuoteOptionIdentifier: NotRequired[str]
    Capacities: NotRequired[list[QuoteCapacityTypeDef]]
    CapacitySummary: NotRequired[CapacitySummaryTypeDef]
    Specifications: NotRequired[list[QuoteSpecificationTypeDef]]
    PricingOptions: NotRequired[list[PricingOptionTypeDef]]

class CreateOrderOutputTypeDef(TypedDict):
    Order: OrderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetOrderOutputTypeDef(TypedDict):
    Order: OrderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class QuoteSummaryTypeDef(TypedDict):
    QuoteId: NotRequired[str]
    AccountId: NotRequired[str]
    QuoteStatus: NotRequired[QuoteStatusType]
    StatusMessage: NotRequired[str]
    OutpostArn: NotRequired[str]
    CountryCode: NotRequired[str]
    RequestedCapacities: NotRequired[list[QuoteCapacityTypeDef]]
    RequestedConstraints: NotRequired[list[QuoteConstraintTypeDef]]
    RequestedPaymentOptions: NotRequired[list[PaymentOptionType]]
    RequestedPaymentTerms: NotRequired[list[PaymentTermType]]
    QuoteOptions: NotRequired[list[QuoteOptionTypeDef]]
    SubmittedOrderId: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    ExpirationDate: NotRequired[datetime]
    Description: NotRequired[str]

class QuoteTypeDef(TypedDict):
    QuoteId: NotRequired[str]
    AccountId: NotRequired[str]
    QuoteStatus: NotRequired[QuoteStatusType]
    StatusMessage: NotRequired[str]
    OutpostArn: NotRequired[str]
    CountryCode: NotRequired[str]
    RequestedCapacities: NotRequired[list[QuoteCapacityTypeDef]]
    RequestedConstraints: NotRequired[list[QuoteConstraintTypeDef]]
    RequestedPaymentOptions: NotRequired[list[PaymentOptionType]]
    RequestedPaymentTerms: NotRequired[list[PaymentTermType]]
    QuoteOptions: NotRequired[list[QuoteOptionTypeDef]]
    OrderingRequirements: NotRequired[list[OrderingRequirementTypeDef]]
    SubmittedOrderId: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    ExpirationDate: NotRequired[datetime]
    Description: NotRequired[str]

class ListQuotesOutputTypeDef(TypedDict):
    Quotes: list[QuoteSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateQuoteOutputTypeDef(TypedDict):
    Quote: QuoteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetQuoteOutputTypeDef(TypedDict):
    Quote: QuoteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateQuoteOutputTypeDef(TypedDict):
    Quote: QuoteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
