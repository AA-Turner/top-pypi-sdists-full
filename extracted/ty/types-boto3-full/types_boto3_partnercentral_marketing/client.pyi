"""
Type annotations for partnercentral-marketing service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_partnercentral_marketing.client import PartnerCentralMarketingClient

    session = Session()
    client: PartnerCentralMarketingClient = session.client("partnercentral-marketing")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListCampaignAssetsPaginator,
    ListCampaignsPaginator,
    ListSocialConnectionsPaginator,
    SearchCampaignTemplatesPaginator,
)
from .type_defs import (
    BatchCreateCampaignAssetRequestTypeDef,
    BatchCreateCampaignAssetResponseTypeDef,
    CreateCampaignRequestTypeDef,
    CreateCampaignResponseTypeDef,
    CreateSocialConnectionAuthorizationUrlRequestTypeDef,
    CreateSocialConnectionAuthorizationUrlResponseTypeDef,
    DeactivateCampaignAssetRequestTypeDef,
    DeactivateCampaignAssetResponseTypeDef,
    DeleteCampaignAssetRequestTypeDef,
    DeleteCampaignRequestTypeDef,
    DeleteSocialConnectionRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCampaignAssetActivationTaskRequestTypeDef,
    GetCampaignAssetActivationTaskResponseTypeDef,
    GetCampaignAssetExportTaskRequestTypeDef,
    GetCampaignAssetExportTaskResponseTypeDef,
    GetCampaignAssetRequestTypeDef,
    GetCampaignAssetResponseTypeDef,
    GetCampaignRequestTypeDef,
    GetCampaignResponseTypeDef,
    GetCampaignTemplateRequestTypeDef,
    GetCampaignTemplateResponseTypeDef,
    ListCampaignAssetsRequestTypeDef,
    ListCampaignAssetsResponseTypeDef,
    ListCampaignsRequestTypeDef,
    ListCampaignsResponseTypeDef,
    ListSocialConnectionsRequestTypeDef,
    ListSocialConnectionsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    SearchCampaignTemplatesRequestTypeDef,
    SearchCampaignTemplatesResponseTypeDef,
    StartCampaignAssetActivationTaskRequestTypeDef,
    StartCampaignAssetActivationTaskResponseTypeDef,
    StartCampaignAssetExportTaskRequestTypeDef,
    StartCampaignAssetExportTaskResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateCampaignAssetRequestTypeDef,
    UpdateCampaignAssetResponseTypeDef,
    UpdateCampaignRequestTypeDef,
    UpdateCampaignResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("PartnerCentralMarketingClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class PartnerCentralMarketingClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing.html#PartnerCentralMarketing.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PartnerCentralMarketingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing.html#PartnerCentralMarketing.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#generate_presigned_url)
        """

    def batch_create_campaign_asset(
        self, **kwargs: Unpack[BatchCreateCampaignAssetRequestTypeDef]
    ) -> BatchCreateCampaignAssetResponseTypeDef:
        """
        Instantiates one or more of the campaign template's blueprints as assets of
        this campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/batch_create_campaign_asset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#batch_create_campaign_asset)
        """

    def create_campaign(
        self, **kwargs: Unpack[CreateCampaignRequestTypeDef]
    ) -> CreateCampaignResponseTypeDef:
        """
        Creates a new marketing campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/create_campaign.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#create_campaign)
        """

    def create_social_connection_authorization_url(
        self, **kwargs: Unpack[CreateSocialConnectionAuthorizationUrlRequestTypeDef]
    ) -> CreateSocialConnectionAuthorizationUrlResponseTypeDef:
        """
        Creates a single-use URL the partner visits to authorize publishing on a
        platform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/create_social_connection_authorization_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#create_social_connection_authorization_url)
        """

    def deactivate_campaign_asset(
        self, **kwargs: Unpack[DeactivateCampaignAssetRequestTypeDef]
    ) -> DeactivateCampaignAssetResponseTypeDef:
        """
        Stops a live campaign asset: an email's scheduled send is withdrawn, a social
        post is removed before it publishes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/deactivate_campaign_asset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#deactivate_campaign_asset)
        """

    def delete_campaign(
        self, **kwargs: Unpack[DeleteCampaignRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Permanently deletes a campaign, its assets and their stored files.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/delete_campaign.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#delete_campaign)
        """

    def delete_campaign_asset(
        self, **kwargs: Unpack[DeleteCampaignAssetRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Permanently deletes a campaign asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/delete_campaign_asset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#delete_campaign_asset)
        """

    def delete_social_connection(
        self, **kwargs: Unpack[DeleteSocialConnectionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Revokes and deletes one social connection; other connections on the same
        platform are untouched.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/delete_social_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#delete_social_connection)
        """

    def get_campaign(
        self, **kwargs: Unpack[GetCampaignRequestTypeDef]
    ) -> GetCampaignResponseTypeDef:
        """
        Retrieves a campaign by its identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/get_campaign.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#get_campaign)
        """

    def get_campaign_asset(
        self, **kwargs: Unpack[GetCampaignAssetRequestTypeDef]
    ) -> GetCampaignAssetResponseTypeDef:
        """
        Retrieves an asset by its identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/get_campaign_asset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#get_campaign_asset)
        """

    def get_campaign_asset_activation_task(
        self, **kwargs: Unpack[GetCampaignAssetActivationTaskRequestTypeDef]
    ) -> GetCampaignAssetActivationTaskResponseTypeDef:
        """
        Reads a campaign's current activation task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/get_campaign_asset_activation_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#get_campaign_asset_activation_task)
        """

    def get_campaign_asset_export_task(
        self, **kwargs: Unpack[GetCampaignAssetExportTaskRequestTypeDef]
    ) -> GetCampaignAssetExportTaskResponseTypeDef:
        """
        Retrieves a campaign asset export task by its identifier, reporting its status
        and, when the task is COMPLETED, a freshly minted short-lived presigned URL for
        downloading the ZIP archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/get_campaign_asset_export_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#get_campaign_asset_export_task)
        """

    def get_campaign_template(
        self, **kwargs: Unpack[GetCampaignTemplateRequestTypeDef]
    ) -> GetCampaignTemplateResponseTypeDef:
        """
        Retrieves full detail of one campaign template, including its ordered asset
        templates with their field schema and layout previews.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/get_campaign_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#get_campaign_template)
        """

    def list_campaign_assets(
        self, **kwargs: Unpack[ListCampaignAssetsRequestTypeDef]
    ) -> ListCampaignAssetsResponseTypeDef:
        """
        Lists assets for a campaign with pagination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/list_campaign_assets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#list_campaign_assets)
        """

    def list_campaigns(
        self, **kwargs: Unpack[ListCampaignsRequestTypeDef]
    ) -> ListCampaignsResponseTypeDef:
        """
        Lists campaigns with optional filters and pagination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/list_campaigns.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#list_campaigns)
        """

    def list_social_connections(
        self, **kwargs: Unpack[ListSocialConnectionsRequestTypeDef]
    ) -> ListSocialConnectionsResponseTypeDef:
        """
        Lists the partner's social connections, optionally filtered by platform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/list_social_connections.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#list_social_connections)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags applied to a Partner Central Marketing resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#list_tags_for_resource)
        """

    def search_campaign_templates(
        self, **kwargs: Unpack[SearchCampaignTemplatesRequestTypeDef]
    ) -> SearchCampaignTemplatesResponseTypeDef:
        """
        Searches and browses the AWS-authored campaign template catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/search_campaign_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#search_campaign_templates)
        """

    def start_campaign_asset_activation_task(
        self, **kwargs: Unpack[StartCampaignAssetActivationTaskRequestTypeDef]
    ) -> StartCampaignAssetActivationTaskResponseTypeDef:
        """
        Activates 1-25 of a campaign's assets as one ordered unit, and returns a task
        to poll.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/start_campaign_asset_activation_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#start_campaign_asset_activation_task)
        """

    def start_campaign_asset_export_task(
        self, **kwargs: Unpack[StartCampaignAssetExportTaskRequestTypeDef]
    ) -> StartCampaignAssetExportTaskResponseTypeDef:
        """
        Starts an asynchronous task that packages a campaign's assets into a single
        downloadable ZIP archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/start_campaign_asset_export_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#start_campaign_asset_export_task)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Adds or replaces tags on a Partner Central Marketing resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes tags from a Partner Central Marketing resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#untag_resource)
        """

    def update_campaign(
        self, **kwargs: Unpack[UpdateCampaignRequestTypeDef]
    ) -> UpdateCampaignResponseTypeDef:
        """
        Edits a campaign in place.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/update_campaign.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#update_campaign)
        """

    def update_campaign_asset(
        self, **kwargs: Unpack[UpdateCampaignAssetRequestTypeDef]
    ) -> UpdateCampaignAssetResponseTypeDef:
        """
        Updates an asset's field values, layout or send time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/update_campaign_asset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#update_campaign_asset)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_campaign_assets"]
    ) -> ListCampaignAssetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_campaigns"]
    ) -> ListCampaignsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_social_connections"]
    ) -> ListSocialConnectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_campaign_templates"]
    ) -> SearchCampaignTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/client/#get_paginator)
        """
