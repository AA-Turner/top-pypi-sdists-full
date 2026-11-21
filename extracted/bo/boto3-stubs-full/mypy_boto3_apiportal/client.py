"""
Type annotations for apiportal service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_apiportal.client import APIPortalClient

    session = Session()
    client: APIPortalClient = session.client("apiportal")
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
    ListApiInventoryItemsPaginator,
    ListDiscoveryStatusesPaginator,
    ListManagedApiEventsPaginator,
    ListManagedApisPaginator,
    ListPortalsPaginator,
    ListProductApiPagesPaginator,
    ListProductPagesPaginator,
    ListProductsPaginator,
)
from .type_defs import (
    AssociateManagedApisRequestTypeDef,
    AssociateManagedApisResponseTypeDef,
    CreateManagedApiRequestTypeDef,
    CreateManagedApiResponseTypeDef,
    CreatePortalPreviewRequestTypeDef,
    CreatePortalRequestTypeDef,
    CreatePortalResponseTypeDef,
    CreateProductApiPageRequestTypeDef,
    CreateProductApiPageResponseTypeDef,
    CreateProductPageRequestTypeDef,
    CreateProductPageResponseTypeDef,
    CreateProductRequestTypeDef,
    CreateProductResponseTypeDef,
    DeleteManagedApiRequestTypeDef,
    DeletePortalRequestTypeDef,
    DeleteProductApiPageRequestTypeDef,
    DeleteProductPageRequestTypeDef,
    DeleteProductRequestTypeDef,
    DeleteProductSharingPolicyRequestTypeDef,
    DisassociateManagedApisRequestTypeDef,
    DisassociateManagedApisResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetApiInventoryItemRequestTypeDef,
    GetApiInventoryItemResponseTypeDef,
    GetDiscoveryConfigurationResponseTypeDef,
    GetManagedApiRequestTypeDef,
    GetManagedApiResponseTypeDef,
    GetOrganizationDiscoveryConfigurationResponseTypeDef,
    GetPortalRequestTypeDef,
    GetPortalResponseTypeDef,
    GetProductApiPageRequestTypeDef,
    GetProductApiPageResponseTypeDef,
    GetProductPageRequestTypeDef,
    GetProductPageResponseTypeDef,
    GetProductRequestTypeDef,
    GetProductResponseTypeDef,
    GetProductSharingPolicyRequestTypeDef,
    GetProductSharingPolicyResponseTypeDef,
    ListApiInventoryItemsRequestTypeDef,
    ListApiInventoryItemsResponseTypeDef,
    ListDiscoveryStatusesRequestTypeDef,
    ListDiscoveryStatusesResponseTypeDef,
    ListManagedApiEventsRequestTypeDef,
    ListManagedApiEventsResponseTypeDef,
    ListManagedApisRequestTypeDef,
    ListManagedApisResponseTypeDef,
    ListPortalsRequestTypeDef,
    ListPortalsResponseTypeDef,
    ListProductApiPagesRequestTypeDef,
    ListProductApiPagesResponseTypeDef,
    ListProductPagesRequestTypeDef,
    ListProductPagesResponseTypeDef,
    ListProductsRequestTypeDef,
    ListProductsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutDiscoveryConfigurationRequestTypeDef,
    PutDiscoveryConfigurationResponseTypeDef,
    PutOrganizationDiscoveryConfigurationRequestTypeDef,
    PutOrganizationDiscoveryConfigurationResponseTypeDef,
    PutProductSharingPolicyRequestTypeDef,
    StartDiscoveryRequestTypeDef,
    StopDiscoveryRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdatePortalPublishStatusRequestTypeDef,
    UpdatePortalRequestTypeDef,
    UpdatePortalResponseTypeDef,
    UpdateProductApiPageRequestTypeDef,
    UpdateProductApiPageResponseTypeDef,
    UpdateProductPageRequestTypeDef,
    UpdateProductPageResponseTypeDef,
    UpdateProductRequestTypeDef,
    UpdateProductResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("APIPortalClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    BadRequestException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    LimitExceededException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]


class APIPortalClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal.html#APIPortal.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        APIPortalClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal.html#APIPortal.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#generate_presigned_url)
        """

    def associate_managed_apis(
        self, **kwargs: Unpack[AssociateManagedApisRequestTypeDef]
    ) -> AssociateManagedApisResponseTypeDef:
        """
        Associate one or more Managed APIs with a product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/associate_managed_apis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#associate_managed_apis)
        """

    def create_managed_api(
        self, **kwargs: Unpack[CreateManagedApiRequestTypeDef]
    ) -> CreateManagedApiResponseTypeDef:
        """
        Promote a discovered API in the API inventory into the managed API list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/create_managed_api.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#create_managed_api)
        """

    def create_portal(
        self, **kwargs: Unpack[CreatePortalRequestTypeDef]
    ) -> CreatePortalResponseTypeDef:
        """
        Creates a portal that publishes documentation for the products it includes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/create_portal.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#create_portal)
        """

    def create_portal_preview(
        self, **kwargs: Unpack[CreatePortalPreviewRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts building a preview of the portal's current content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/create_portal_preview.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#create_portal_preview)
        """

    def create_product(
        self, **kwargs: Unpack[CreateProductRequestTypeDef]
    ) -> CreateProductResponseTypeDef:
        """
        Creates a product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/create_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#create_product)
        """

    def create_product_api_page(
        self, **kwargs: Unpack[CreateProductApiPageRequestTypeDef]
    ) -> CreateProductApiPageResponseTypeDef:
        """
        Creates an API page that documents a Managed API in a product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/create_product_api_page.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#create_product_api_page)
        """

    def create_product_page(
        self, **kwargs: Unpack[CreateProductPageRequestTypeDef]
    ) -> CreateProductPageResponseTypeDef:
        """
        Creates a product page with free-form documentation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/create_product_page.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#create_product_page)
        """

    def delete_discovery_configuration(self) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the discovery configuration and stops any running discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/delete_discovery_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#delete_discovery_configuration)
        """

    def delete_managed_api(
        self, **kwargs: Unpack[DeleteManagedApiRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a Managed API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/delete_managed_api.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#delete_managed_api)
        """

    def delete_organization_discovery_configuration(self) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the organization-wide discovery configuration and stops any running
        discovery across the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/delete_organization_discovery_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#delete_organization_discovery_configuration)
        """

    def delete_portal(
        self, **kwargs: Unpack[DeletePortalRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/delete_portal.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#delete_portal)
        """

    def delete_product(
        self, **kwargs: Unpack[DeleteProductRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/delete_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#delete_product)
        """

    def delete_product_api_page(
        self, **kwargs: Unpack[DeleteProductApiPageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an API page.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/delete_product_api_page.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#delete_product_api_page)
        """

    def delete_product_page(
        self, **kwargs: Unpack[DeleteProductPageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a product page.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/delete_product_page.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#delete_product_page)
        """

    def delete_product_sharing_policy(
        self, **kwargs: Unpack[DeleteProductSharingPolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the sharing policy of a product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/delete_product_sharing_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#delete_product_sharing_policy)
        """

    def disassociate_managed_apis(
        self, **kwargs: Unpack[DisassociateManagedApisRequestTypeDef]
    ) -> DisassociateManagedApisResponseTypeDef:
        """
        Disassociate one or more Managed APIs from a product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/disassociate_managed_apis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#disassociate_managed_apis)
        """

    def get_api_inventory_item(
        self, **kwargs: Unpack[GetApiInventoryItemRequestTypeDef]
    ) -> GetApiInventoryItemResponseTypeDef:
        """
        Gets full details of a single API inventory item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_api_inventory_item.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_api_inventory_item)
        """

    def get_discovery_configuration(self) -> GetDiscoveryConfigurationResponseTypeDef:
        """
        Retrieves the discovery configuration for the account and region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_discovery_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_discovery_configuration)
        """

    def get_managed_api(
        self, **kwargs: Unpack[GetManagedApiRequestTypeDef]
    ) -> GetManagedApiResponseTypeDef:
        """
        Returns a Managed API, including its security posture findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_managed_api.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_managed_api)
        """

    def get_organization_discovery_configuration(
        self,
    ) -> GetOrganizationDiscoveryConfigurationResponseTypeDef:
        """
        Retrieves the organization-wide discovery configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_organization_discovery_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_organization_discovery_configuration)
        """

    def get_portal(self, **kwargs: Unpack[GetPortalRequestTypeDef]) -> GetPortalResponseTypeDef:
        """
        Returns the configuration, publish status, and preview status of a portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_portal.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_portal)
        """

    def get_product(self, **kwargs: Unpack[GetProductRequestTypeDef]) -> GetProductResponseTypeDef:
        """
        Returns a product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_product)
        """

    def get_product_api_page(
        self, **kwargs: Unpack[GetProductApiPageRequestTypeDef]
    ) -> GetProductApiPageResponseTypeDef:
        """
        Returns an API page, including its body.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_product_api_page.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_product_api_page)
        """

    def get_product_page(
        self, **kwargs: Unpack[GetProductPageRequestTypeDef]
    ) -> GetProductPageResponseTypeDef:
        """
        Returns a product page, including its body.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_product_page.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_product_page)
        """

    def get_product_sharing_policy(
        self, **kwargs: Unpack[GetProductSharingPolicyRequestTypeDef]
    ) -> GetProductSharingPolicyResponseTypeDef:
        """
        Returns the sharing policy of a product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_product_sharing_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_product_sharing_policy)
        """

    def list_api_inventory_items(
        self, **kwargs: Unpack[ListApiInventoryItemsRequestTypeDef]
    ) -> ListApiInventoryItemsResponseTypeDef:
        """
        Lists discovered API inventory items with filtering and pagination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/list_api_inventory_items.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#list_api_inventory_items)
        """

    def list_discovery_statuses(
        self, **kwargs: Unpack[ListDiscoveryStatusesRequestTypeDef]
    ) -> ListDiscoveryStatusesResponseTypeDef:
        """
        Lists discovery statuses for services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/list_discovery_statuses.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#list_discovery_statuses)
        """

    def list_managed_api_events(
        self, **kwargs: Unpack[ListManagedApiEventsRequestTypeDef]
    ) -> ListManagedApiEventsResponseTypeDef:
        """
        Lists API-security events for a single managed API, most recent first.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/list_managed_api_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#list_managed_api_events)
        """

    def list_managed_apis(
        self, **kwargs: Unpack[ListManagedApisRequestTypeDef]
    ) -> ListManagedApisResponseTypeDef:
        """
        Lists the Managed APIs in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/list_managed_apis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#list_managed_apis)
        """

    def list_portals(
        self, **kwargs: Unpack[ListPortalsRequestTypeDef]
    ) -> ListPortalsResponseTypeDef:
        """
        Lists the portals in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/list_portals.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#list_portals)
        """

    def list_product_api_pages(
        self, **kwargs: Unpack[ListProductApiPagesRequestTypeDef]
    ) -> ListProductApiPagesResponseTypeDef:
        """
        Lists the API pages in a product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/list_product_api_pages.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#list_product_api_pages)
        """

    def list_product_pages(
        self, **kwargs: Unpack[ListProductPagesRequestTypeDef]
    ) -> ListProductPagesResponseTypeDef:
        """
        Lists the product pages in a product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/list_product_pages.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#list_product_pages)
        """

    def list_products(
        self, **kwargs: Unpack[ListProductsRequestTypeDef]
    ) -> ListProductsResponseTypeDef:
        """
        Lists products you own, products shared with you, or both.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/list_products.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#list_products)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for an API Portal resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#list_tags_for_resource)
        """

    def put_discovery_configuration(
        self, **kwargs: Unpack[PutDiscoveryConfigurationRequestTypeDef]
    ) -> PutDiscoveryConfigurationResponseTypeDef:
        """
        Creates or updates the discovery configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/put_discovery_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#put_discovery_configuration)
        """

    def put_organization_discovery_configuration(
        self, **kwargs: Unpack[PutOrganizationDiscoveryConfigurationRequestTypeDef]
    ) -> PutOrganizationDiscoveryConfigurationResponseTypeDef:
        """
        Creates or updates the organization-wide discovery configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/put_organization_discovery_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#put_organization_discovery_configuration)
        """

    def put_product_sharing_policy(
        self, **kwargs: Unpack[PutProductSharingPolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or replaces the sharing policy of a product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/put_product_sharing_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#put_product_sharing_policy)
        """

    def start_discovery(
        self, **kwargs: Unpack[StartDiscoveryRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts the API discovery process.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/start_discovery.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#start_discovery)
        """

    def stop_discovery(
        self, **kwargs: Unpack[StopDiscoveryRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops the running API discovery process.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/stop_discovery.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#stop_discovery)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Adds or updates tags on an API Portal resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes tags from an API Portal resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#untag_resource)
        """

    def update_portal(
        self, **kwargs: Unpack[UpdatePortalRequestTypeDef]
    ) -> UpdatePortalResponseTypeDef:
        """
        Updates a portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/update_portal.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#update_portal)
        """

    def update_portal_publish_status(
        self, **kwargs: Unpack[UpdatePortalPublishStatusRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Publishes or disables a portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/update_portal_publish_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#update_portal_publish_status)
        """

    def update_product(
        self, **kwargs: Unpack[UpdateProductRequestTypeDef]
    ) -> UpdateProductResponseTypeDef:
        """
        Updates a product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/update_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#update_product)
        """

    def update_product_api_page(
        self, **kwargs: Unpack[UpdateProductApiPageRequestTypeDef]
    ) -> UpdateProductApiPageResponseTypeDef:
        """
        Updates an API page.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/update_product_api_page.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#update_product_api_page)
        """

    def update_product_page(
        self, **kwargs: Unpack[UpdateProductPageRequestTypeDef]
    ) -> UpdateProductPageResponseTypeDef:
        """
        Updates a product page.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/update_product_page.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#update_product_page)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_api_inventory_items"]
    ) -> ListApiInventoryItemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_discovery_statuses"]
    ) -> ListDiscoveryStatusesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_managed_api_events"]
    ) -> ListManagedApiEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_managed_apis"]
    ) -> ListManagedApisPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_portals"]
    ) -> ListPortalsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_product_api_pages"]
    ) -> ListProductApiPagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_product_pages"]
    ) -> ListProductPagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_products"]
    ) -> ListProductsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/client/#get_paginator)
        """
