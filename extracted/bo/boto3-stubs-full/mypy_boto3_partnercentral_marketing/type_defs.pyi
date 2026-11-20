"""
Type annotations for partnercentral-marketing service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_marketing/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_partnercentral_marketing.type_defs import ActivationIssueTypeDef

    data: ActivationIssueTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AssetLanguageType,
    AttemptStatusType,
    CampaignAssetActivationStatusType,
    CampaignAssetActivationTaskStatusType,
    CampaignAssetCategoryType,
    CampaignAssetExportFailureCodeType,
    CampaignAssetExportTaskStatusType,
    CampaignAssetStateReasonType,
    CampaignAssetStateType,
    CampaignAssetTemplateTypeType,
    CampaignSettingType,
    CampaignSortNameType,
    CampaignStateType,
    CampaignTemplateCollectionType,
    CatalogType,
    CompanySizeType,
    CustomerSegmentType,
    DeliveryStatusType,
    FileFormatType,
    ImageFormatType,
    IndustryType,
    LayoutFormatType,
    LayoutPageTypeType,
    PartnerProfileFieldType,
    PlatformType,
    ScanStatusType,
    SendModeType,
    SocialConnectionStatusType,
    SortOrderType,
    TemplateFieldSectionType,
    ThemeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ActivationIssueTypeDef",
    "AssetLinkFieldTypeTypeDef",
    "BatchCreateCampaignAssetEntryTypeDef",
    "BatchCreateCampaignAssetErrorTypeDef",
    "BatchCreateCampaignAssetRequestTypeDef",
    "BatchCreateCampaignAssetResponseTypeDef",
    "BatchCreateCampaignAssetResultTypeDef",
    "CampaignAssetActivationOutcomeTypeDef",
    "CampaignAssetExportFailureReasonTypeDef",
    "CampaignAssetFieldValueTypeDef",
    "CampaignAssetImageSourceTypeDef",
    "CampaignAssetLayoutOptionTypeDef",
    "CampaignAssetLayoutTypeDef",
    "CampaignAssetSummaryTypeDef",
    "CampaignAssetTemplateFieldTypeDef",
    "CampaignAssetTemplateTypeDef",
    "CampaignAssetTypeDef",
    "CampaignSortTypeDef",
    "CampaignSummaryTypeDef",
    "CampaignTemplateSummaryTypeDef",
    "CampaignTemplateTypeDef",
    "CampaignTypeDef",
    "CreateCampaignRequestTypeDef",
    "CreateCampaignResponseTypeDef",
    "CreateSocialConnectionAuthorizationUrlRequestTypeDef",
    "CreateSocialConnectionAuthorizationUrlResponseTypeDef",
    "DeactivateCampaignAssetRequestTypeDef",
    "DeactivateCampaignAssetResponseTypeDef",
    "DeleteCampaignAssetRequestTypeDef",
    "DeleteCampaignRequestTypeDef",
    "DeleteSocialConnectionRequestTypeDef",
    "EmailTargetDetailTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FieldTypeTypeDef",
    "FieldValueInputTypeDef",
    "FileRefTypeDef",
    "GetCampaignAssetActivationTaskRequestTypeDef",
    "GetCampaignAssetActivationTaskResponseTypeDef",
    "GetCampaignAssetExportTaskRequestTypeDef",
    "GetCampaignAssetExportTaskResponseTypeDef",
    "GetCampaignAssetRequestTypeDef",
    "GetCampaignAssetResponseTypeDef",
    "GetCampaignRequestTypeDef",
    "GetCampaignResponseTypeDef",
    "GetCampaignTemplateRequestTypeDef",
    "GetCampaignTemplateResponseTypeDef",
    "ImageFieldTypeTypeDef",
    "LayoutPreviewTypeDef",
    "ListCampaignAssetsRequestPaginateTypeDef",
    "ListCampaignAssetsRequestTypeDef",
    "ListCampaignAssetsResponseTypeDef",
    "ListCampaignsRequestPaginateTypeDef",
    "ListCampaignsRequestTypeDef",
    "ListCampaignsResponseTypeDef",
    "ListSocialConnectionsRequestPaginateTypeDef",
    "ListSocialConnectionsRequestTypeDef",
    "ListSocialConnectionsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MonetaryValueTypeDef",
    "PaginatorConfigTypeDef",
    "PartnerBadgeDetailTypeDef",
    "PartnerProfileBrandingTypeDef",
    "ReferenceMaterialTypeDef",
    "ResponseMetadataTypeDef",
    "RichTextFieldTypeTypeDef",
    "SearchCampaignTemplatesRequestPaginateTypeDef",
    "SearchCampaignTemplatesRequestTypeDef",
    "SearchCampaignTemplatesResponseTypeDef",
    "SocialConnectionSummaryTypeDef",
    "StartCampaignAssetActivationTaskRequestTypeDef",
    "StartCampaignAssetActivationTaskResponseTypeDef",
    "StartCampaignAssetExportTaskRequestTypeDef",
    "StartCampaignAssetExportTaskResponseTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "TargetAudienceOutputTypeDef",
    "TargetAudienceTypeDef",
    "TargetAudienceUnionTypeDef",
    "TemplateFieldValueTypeDef",
    "TextFieldTypeTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateCampaignAssetRequestTypeDef",
    "UpdateCampaignAssetResponseTypeDef",
    "UpdateCampaignRequestTypeDef",
    "UpdateCampaignResponseTypeDef",
)

class ActivationIssueTypeDef(TypedDict):
    Code: CampaignAssetStateReasonType
    Message: str
    FieldId: NotRequired[str]
    CampaignSetting: NotRequired[CampaignSettingType]
    PartnerProfileField: NotRequired[PartnerProfileFieldType]
    AffectedAssetIds: NotRequired[list[str]]

class AssetLinkFieldTypeTypeDef(TypedDict):
    Category: CampaignAssetCategoryType
    LabelFieldId: NotRequired[str]

class BatchCreateCampaignAssetEntryTypeDef(TypedDict):
    SourceAssetTemplateIdentifier: str

class BatchCreateCampaignAssetErrorTypeDef(TypedDict):
    SourceAssetTemplateId: str
    Code: str
    Message: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CampaignAssetActivationOutcomeTypeDef(TypedDict):
    CampaignAssetId: str
    Status: CampaignAssetActivationStatusType
    Reason: NotRequired[CampaignAssetStateReasonType]
    Message: NotRequired[str]

class CampaignAssetExportFailureReasonTypeDef(TypedDict):
    Code: CampaignAssetExportFailureCodeType
    Message: str

class CampaignAssetImageSourceTypeDef(TypedDict):
    CampaignIdentifier: str
    CampaignAssetIdentifier: str
    FieldId: str

class LayoutPreviewTypeDef(TypedDict):
    Format: LayoutFormatType
    Url: str
    PageType: NotRequired[LayoutPageTypeType]

class CampaignAssetSummaryTypeDef(TypedDict):
    Id: str
    Category: CampaignAssetCategoryType
    Name: str
    LinkLabel: NotRequired[str]
    State: NotRequired[CampaignAssetStateType]
    LastActivationStatus: NotRequired[AttemptStatusType]
    DeliveryStatus: NotRequired[DeliveryStatusType]
    DeliveryStatusReason: NotRequired[CampaignAssetStateReasonType]
    SourceAssetTemplateId: NotRequired[str]
    SocialPlatform: NotRequired[PlatformType]
    StartedAt: NotRequired[datetime]
    FileFormat: NotRequired[FileFormatType]
    SendMode: NotRequired[SendModeType]
    ScheduledSendAt: NotRequired[datetime]

class CampaignSortTypeDef(TypedDict):
    SortBy: CampaignSortNameType
    SortOrder: SortOrderType

class CampaignSummaryTypeDef(TypedDict):
    CampaignId: str
    Arn: str
    Name: str
    State: CampaignStateType
    Language: NotRequired[AssetLanguageType]
    StartOn: NotRequired[str]
    EndOn: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]

CampaignTemplateSummaryTypeDef = TypedDict(
    "CampaignTemplateSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Collection": CampaignTemplateCollectionType,
        "Industry": NotRequired[IndustryType],
        "UseCase": NotRequired[str],
        "Description": NotRequired[str],
        "LanguageCode": NotRequired[AssetLanguageType],
        "AwsServices": NotRequired[list[str]],
        "CustomerSegments": NotRequired[list[CustomerSegmentType]],
        "Themes": NotRequired[list[ThemeType]],
        "ThumbnailUrl": NotRequired[str],
    },
)

class ReferenceMaterialTypeDef(TypedDict):
    Name: str
    Url: NotRequired[str]

class EmailTargetDetailTypeDef(TypedDict):
    ScanStatus: NotRequired[ScanStatusType]
    AttachedAt: NotRequired[datetime]
    ValidCount: NotRequired[int]
    RejectedCount: NotRequired[int]
    DuplicateCount: NotRequired[int]
    FileName: NotRequired[str]

class MonetaryValueTypeDef(TypedDict):
    Amount: str
    CurrencyCode: str

class PartnerBadgeDetailTypeDef(TypedDict):
    Url: str
    AttachedAt: datetime

class PartnerProfileBrandingTypeDef(TypedDict):
    RefreshedAt: datetime
    DisplayName: NotRequired[str]
    WebsiteUrl: NotRequired[str]
    LogoUrl: NotRequired[str]

class TargetAudienceOutputTypeDef(TypedDict):
    Industries: NotRequired[list[IndustryType]]
    CompanySizes: NotRequired[list[CompanySizeType]]
    Countries: NotRequired[list[str]]

class FileRefTypeDef(TypedDict):
    S3Uri: str
    VersionId: str

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class CreateSocialConnectionAuthorizationUrlRequestTypeDef(TypedDict):
    Catalog: CatalogType
    Platform: PlatformType

class DeactivateCampaignAssetRequestTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifier: str
    CampaignAssetIdentifier: str

class DeleteCampaignAssetRequestTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifier: str
    CampaignAssetIdentifier: str

class DeleteCampaignRequestTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifier: str

class DeleteSocialConnectionRequestTypeDef(TypedDict):
    Catalog: CatalogType
    Identifier: str
    ClientToken: NotRequired[str]

class RichTextFieldTypeTypeDef(TypedDict):
    AllowedTags: list[str]
    MaxLength: NotRequired[int]
    Placeholder: NotRequired[str]

class TextFieldTypeTypeDef(TypedDict):
    MinLength: NotRequired[int]
    MaxLength: NotRequired[int]
    Pattern: NotRequired[str]
    Placeholder: NotRequired[str]

class GetCampaignAssetActivationTaskRequestTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifier: str

class GetCampaignAssetExportTaskRequestTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifier: str
    CampaignAssetExportTaskIdentifier: str

class GetCampaignAssetRequestTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifier: str
    CampaignAssetIdentifier: str

class GetCampaignRequestTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifier: str

class GetCampaignTemplateRequestTypeDef(TypedDict):
    Catalog: CatalogType
    Identifier: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListCampaignAssetsRequestTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifier: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListSocialConnectionsRequestTypeDef(TypedDict):
    Catalog: CatalogType
    Platform: NotRequired[PlatformType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class SocialConnectionSummaryTypeDef(TypedDict):
    Id: str
    Platform: PlatformType
    Status: SocialConnectionStatusType
    PageName: NotRequired[str]
    AccountName: NotRequired[str]
    ConnectedAt: NotRequired[datetime]
    ExpiresAt: NotRequired[datetime]

class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str

SearchCampaignTemplatesRequestTypeDef = TypedDict(
    "SearchCampaignTemplatesRequestTypeDef",
    {
        "Catalog": CatalogType,
        "SearchText": NotRequired[str],
        "Industry": NotRequired[Sequence[IndustryType]],
        "UseCase": NotRequired[Sequence[str]],
        "Language": NotRequired[Sequence[AssetLanguageType]],
        "AwsServices": NotRequired[Sequence[str]],
        "CustomerSegments": NotRequired[Sequence[CustomerSegmentType]],
        "Themes": NotRequired[Sequence[ThemeType]],
        "Collection": NotRequired[Sequence[CampaignTemplateCollectionType]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

class StartCampaignAssetActivationTaskRequestTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifier: str
    CampaignAssetIdentifiers: Sequence[str]
    ClientToken: NotRequired[str]

class StartCampaignAssetExportTaskRequestTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifier: str
    ClientToken: NotRequired[str]

class TargetAudienceTypeDef(TypedDict):
    Industries: NotRequired[Sequence[IndustryType]]
    CompanySizes: NotRequired[Sequence[CompanySizeType]]
    Countries: NotRequired[Sequence[str]]

TimestampTypeDef = Union[datetime, str]

class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class BatchCreateCampaignAssetRequestTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifier: str
    Entries: Sequence[BatchCreateCampaignAssetEntryTypeDef]

class CreateCampaignResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSocialConnectionAuthorizationUrlResponseTypeDef(TypedDict):
    Platform: PlatformType
    AuthorizationUrl: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeactivateCampaignAssetResponseTypeDef(TypedDict):
    Id: str
    State: CampaignAssetStateType
    LastActivationStatus: AttemptStatusType
    StateReason: CampaignAssetStateReasonType
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class StartCampaignAssetExportTaskResponseTypeDef(TypedDict):
    Id: str
    Status: CampaignAssetExportTaskStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateCampaignAssetResponseTypeDef(TypedDict):
    Id: str
    State: CampaignAssetStateType
    ActivationIssues: list[ActivationIssueTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateCampaignResponseTypeDef(TypedDict):
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetCampaignAssetActivationTaskResponseTypeDef(TypedDict):
    CampaignId: str
    TaskId: str
    TaskStatus: CampaignAssetActivationTaskStatusType
    StartedAt: datetime
    EndedAt: datetime
    Assets: list[CampaignAssetActivationOutcomeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartCampaignAssetActivationTaskResponseTypeDef(TypedDict):
    CampaignId: str
    TaskId: str
    TaskStatus: CampaignAssetActivationTaskStatusType
    StartedAt: datetime
    EndedAt: datetime
    Assets: list[CampaignAssetActivationOutcomeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetCampaignAssetExportTaskResponseTypeDef(TypedDict):
    Id: str
    Status: CampaignAssetExportTaskStatusType
    CreatedAt: datetime
    DownloadUrl: str
    ExpiresAt: datetime
    FailureReason: CampaignAssetExportFailureReasonTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

TemplateFieldValueTypeDef = TypedDict(
    "TemplateFieldValueTypeDef",
    {
        "Text": NotRequired[str],
        "ImageReference": NotRequired[str],
        "LinkedAssetId": NotRequired[str],
        "CampaignAssetImage": NotRequired[CampaignAssetImageSourceTypeDef],
    },
)

class CampaignAssetLayoutOptionTypeDef(TypedDict):
    Value: str
    FieldIds: list[str]
    Label: NotRequired[str]
    LayoutPreviews: NotRequired[list[LayoutPreviewTypeDef]]

class ImageFieldTypeTypeDef(TypedDict):
    MaxSizeBytes: NotRequired[int]
    AllowedFormats: NotRequired[list[ImageFormatType]]
    DefaultValue: NotRequired[LayoutPreviewTypeDef]
    RecommendedWidthPixels: NotRequired[int]
    RecommendedHeightPixels: NotRequired[int]

class ListCampaignAssetsResponseTypeDef(TypedDict):
    Items: list[CampaignAssetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCampaignsRequestTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifiers: NotRequired[Sequence[str]]
    Name: NotRequired[str]
    States: NotRequired[Sequence[CampaignStateType]]
    Sort: NotRequired[CampaignSortTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCampaignsResponseTypeDef(TypedDict):
    Items: list[CampaignSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class SearchCampaignTemplatesResponseTypeDef(TypedDict):
    TotalResults: int
    CampaignTemplates: list[CampaignTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CampaignTypeDef(TypedDict):
    CampaignId: str
    Arn: str
    Name: str
    State: CampaignStateType
    ActivationIssues: list[ActivationIssueTypeDef]
    CampaignTemplateId: NotRequired[str]
    Language: NotRequired[AssetLanguageType]
    PartnerProfile: NotRequired[PartnerProfileBrandingTypeDef]
    SenderEmail: NotRequired[str]
    PrivacyPolicyUrl: NotRequired[str]
    PartnerAddress: NotRequired[str]
    PartnerBadge: NotRequired[PartnerBadgeDetailTypeDef]
    EmailTarget: NotRequired[EmailTargetDetailTypeDef]
    EmailTargetEngagementGroupIds: NotRequired[list[str]]
    SocialConnections: NotRequired[dict[PlatformType, list[str]]]
    EstimatedBudget: NotRequired[MonetaryValueTypeDef]
    TotalBudget: NotRequired[MonetaryValueTypeDef]
    TargetAudience: NotRequired[TargetAudienceOutputTypeDef]
    StartOn: NotRequired[str]
    EndOn: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]

class ListTagsForResourceResponseTypeDef(TypedDict):
    ResourceArn: str
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class ListCampaignAssetsRequestPaginateTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCampaignsRequestPaginateTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifiers: NotRequired[Sequence[str]]
    Name: NotRequired[str]
    States: NotRequired[Sequence[CampaignStateType]]
    Sort: NotRequired[CampaignSortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSocialConnectionsRequestPaginateTypeDef(TypedDict):
    Catalog: CatalogType
    Platform: NotRequired[PlatformType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

SearchCampaignTemplatesRequestPaginateTypeDef = TypedDict(
    "SearchCampaignTemplatesRequestPaginateTypeDef",
    {
        "Catalog": CatalogType,
        "SearchText": NotRequired[str],
        "Industry": NotRequired[Sequence[IndustryType]],
        "UseCase": NotRequired[Sequence[str]],
        "Language": NotRequired[Sequence[AssetLanguageType]],
        "AwsServices": NotRequired[Sequence[str]],
        "CustomerSegments": NotRequired[Sequence[CustomerSegmentType]],
        "Themes": NotRequired[Sequence[ThemeType]],
        "Collection": NotRequired[Sequence[CampaignTemplateCollectionType]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListSocialConnectionsResponseTypeDef(TypedDict):
    Items: list[SocialConnectionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

TargetAudienceUnionTypeDef = Union[TargetAudienceTypeDef, TargetAudienceOutputTypeDef]

class FieldValueInputTypeDef(TypedDict):
    FieldId: str
    Value: NotRequired[TemplateFieldValueTypeDef]

class CampaignAssetLayoutTypeDef(TypedDict):
    Options: list[CampaignAssetLayoutOptionTypeDef]
    Selected: NotRequired[str]

FieldTypeTypeDef = TypedDict(
    "FieldTypeTypeDef",
    {
        "Text": NotRequired[TextFieldTypeTypeDef],
        "RichText": NotRequired[RichTextFieldTypeTypeDef],
        "Image": NotRequired[ImageFieldTypeTypeDef],
        "AssetLink": NotRequired[AssetLinkFieldTypeTypeDef],
    },
)

class GetCampaignResponseTypeDef(TypedDict):
    Campaign: CampaignTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCampaignRequestTypeDef(TypedDict):
    Catalog: CatalogType
    Name: str
    CampaignTemplateId: str
    SenderEmail: NotRequired[str]
    PrivacyPolicyUrl: NotRequired[str]
    PartnerAddress: NotRequired[str]
    PartnerBadge: NotRequired[FileRefTypeDef]
    EmailTarget: NotRequired[FileRefTypeDef]
    EmailTargetEngagementGroupIds: NotRequired[Sequence[str]]
    TargetAudience: NotRequired[TargetAudienceUnionTypeDef]
    EstimatedBudget: NotRequired[MonetaryValueTypeDef]
    TotalBudget: NotRequired[MonetaryValueTypeDef]
    StartOn: NotRequired[str]
    EndOn: NotRequired[str]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class UpdateCampaignRequestTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifier: str
    Name: NotRequired[str]
    SenderEmail: NotRequired[str]
    PrivacyPolicyUrl: NotRequired[str]
    PartnerAddress: NotRequired[str]
    PartnerBadge: NotRequired[FileRefTypeDef]
    EmailTarget: NotRequired[FileRefTypeDef]
    EmailTargetEngagementGroupIds: NotRequired[Sequence[str]]
    SocialConnections: NotRequired[Mapping[PlatformType, Sequence[str]]]
    EstimatedBudget: NotRequired[MonetaryValueTypeDef]
    TotalBudget: NotRequired[MonetaryValueTypeDef]
    TargetAudience: NotRequired[TargetAudienceUnionTypeDef]
    ClientToken: NotRequired[str]
    StartOn: NotRequired[str]
    EndOn: NotRequired[str]

class UpdateCampaignAssetRequestTypeDef(TypedDict):
    Catalog: CatalogType
    CampaignIdentifier: str
    CampaignAssetIdentifier: str
    FieldValues: NotRequired[Sequence[FieldValueInputTypeDef]]
    Layout: NotRequired[str]
    SendMode: NotRequired[SendModeType]
    ScheduledSendAt: NotRequired[TimestampTypeDef]
    ClientToken: NotRequired[str]

class BatchCreateCampaignAssetResultTypeDef(TypedDict):
    SourceAssetTemplateId: str
    Id: str
    Layout: NotRequired[CampaignAssetLayoutTypeDef]

CampaignAssetTemplateFieldTypeDef = TypedDict(
    "CampaignAssetTemplateFieldTypeDef",
    {
        "FieldId": str,
        "Type": FieldTypeTypeDef,
        "Label": NotRequired[str],
        "Description": NotRequired[str],
        "Section": NotRequired[TemplateFieldSectionType],
        "Page": NotRequired[int],
        "Required": NotRequired[bool],
        "CampaignSetting": NotRequired[CampaignSettingType],
        "PartnerProfileField": NotRequired[PartnerProfileFieldType],
    },
)

class BatchCreateCampaignAssetResponseTypeDef(TypedDict):
    Errors: list[BatchCreateCampaignAssetErrorTypeDef]
    Successful: list[BatchCreateCampaignAssetResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CampaignAssetFieldValueTypeDef(TypedDict):
    Field: CampaignAssetTemplateFieldTypeDef
    Value: NotRequired[TemplateFieldValueTypeDef]

CampaignAssetTemplateTypeDef = TypedDict(
    "CampaignAssetTemplateTypeDef",
    {
        "Id": str,
        "Type": CampaignAssetTemplateTypeType,
        "Label": str,
        "DisplayOrder": NotRequired[int],
        "Fields": NotRequired[list[CampaignAssetTemplateFieldTypeDef]],
        "LayoutPreviews": NotRequired[list[LayoutPreviewTypeDef]],
        "PrerequisiteAssetTemplateIds": NotRequired[list[str]],
        "SocialPlatform": NotRequired[PlatformType],
    },
)

class CampaignAssetTypeDef(TypedDict):
    Id: str
    CampaignId: str
    Category: CampaignAssetCategoryType
    Name: str
    State: CampaignAssetStateType
    ActivationIssues: list[ActivationIssueTypeDef]
    LinkLabel: NotRequired[str]
    LastActivationStatus: NotRequired[AttemptStatusType]
    DeliveryStatus: NotRequired[DeliveryStatusType]
    DeliveryStatusReason: NotRequired[CampaignAssetStateReasonType]
    SourceAssetTemplateId: NotRequired[str]
    SocialPlatform: NotRequired[PlatformType]
    FileFormat: NotRequired[FileFormatType]
    SendMode: NotRequired[SendModeType]
    ScheduledSendAt: NotRequired[datetime]
    FieldValues: NotRequired[list[CampaignAssetFieldValueTypeDef]]
    LayoutPreviews: NotRequired[list[LayoutPreviewTypeDef]]
    Layout: NotRequired[CampaignAssetLayoutTypeDef]
    PublicUrl: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]

CampaignTemplateTypeDef = TypedDict(
    "CampaignTemplateTypeDef",
    {
        "Id": str,
        "Name": str,
        "Collection": CampaignTemplateCollectionType,
        "Industry": NotRequired[IndustryType],
        "UseCase": NotRequired[str],
        "Description": NotRequired[str],
        "LanguageCode": NotRequired[AssetLanguageType],
        "AwsServices": NotRequired[list[str]],
        "CustomerSegments": NotRequired[list[CustomerSegmentType]],
        "Themes": NotRequired[list[ThemeType]],
        "SetupDuration": NotRequired[str],
        "ThumbnailUrl": NotRequired[str],
        "EffectiveDateBegin": NotRequired[datetime],
        "AssetTemplates": NotRequired[list[CampaignAssetTemplateTypeDef]],
        "ReferenceMaterials": NotRequired[list[ReferenceMaterialTypeDef]],
        "CreatedAt": NotRequired[datetime],
        "UpdatedAt": NotRequired[datetime],
    },
)

class GetCampaignAssetResponseTypeDef(TypedDict):
    Asset: CampaignAssetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetCampaignTemplateResponseTypeDef(TypedDict):
    CampaignTemplate: CampaignTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
