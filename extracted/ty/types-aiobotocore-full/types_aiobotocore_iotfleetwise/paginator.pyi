"""
Type annotations for iotfleetwise service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iotfleetwise.client import IoTFleetWiseClient
    from types_aiobotocore_iotfleetwise.paginator import (
        GetVehicleStatusPaginator,
        ListCampaignsPaginator,
        ListDecoderManifestNetworkInterfacesPaginator,
        ListDecoderManifestSignalsPaginator,
        ListDecoderManifestsPaginator,
        ListFleetsForVehiclePaginator,
        ListFleetsPaginator,
        ListModelManifestNodesPaginator,
        ListModelManifestsPaginator,
        ListSignalCatalogNodesPaginator,
        ListSignalCatalogsPaginator,
        ListStateTemplatesPaginator,
        ListVehiclesInFleetPaginator,
        ListVehiclesPaginator,
    )

    session = get_session()
    with session.create_client("iotfleetwise") as client:
        client: IoTFleetWiseClient

        get_vehicle_status_paginator: GetVehicleStatusPaginator = client.get_paginator("get_vehicle_status")
        list_campaigns_paginator: ListCampaignsPaginator = client.get_paginator("list_campaigns")
        list_decoder_manifest_network_interfaces_paginator: ListDecoderManifestNetworkInterfacesPaginator = client.get_paginator("list_decoder_manifest_network_interfaces")
        list_decoder_manifest_signals_paginator: ListDecoderManifestSignalsPaginator = client.get_paginator("list_decoder_manifest_signals")
        list_decoder_manifests_paginator: ListDecoderManifestsPaginator = client.get_paginator("list_decoder_manifests")
        list_fleets_for_vehicle_paginator: ListFleetsForVehiclePaginator = client.get_paginator("list_fleets_for_vehicle")
        list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
        list_model_manifest_nodes_paginator: ListModelManifestNodesPaginator = client.get_paginator("list_model_manifest_nodes")
        list_model_manifests_paginator: ListModelManifestsPaginator = client.get_paginator("list_model_manifests")
        list_signal_catalog_nodes_paginator: ListSignalCatalogNodesPaginator = client.get_paginator("list_signal_catalog_nodes")
        list_signal_catalogs_paginator: ListSignalCatalogsPaginator = client.get_paginator("list_signal_catalogs")
        list_state_templates_paginator: ListStateTemplatesPaginator = client.get_paginator("list_state_templates")
        list_vehicles_in_fleet_paginator: ListVehiclesInFleetPaginator = client.get_paginator("list_vehicles_in_fleet")
        list_vehicles_paginator: ListVehiclesPaginator = client.get_paginator("list_vehicles")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetVehicleStatusRequestPaginateTypeDef,
    GetVehicleStatusResponseTypeDef,
    ListCampaignsRequestPaginateTypeDef,
    ListCampaignsResponseTypeDef,
    ListDecoderManifestNetworkInterfacesRequestPaginateTypeDef,
    ListDecoderManifestNetworkInterfacesResponseTypeDef,
    ListDecoderManifestSignalsRequestPaginateTypeDef,
    ListDecoderManifestSignalsResponsePaginatorTypeDef,
    ListDecoderManifestsRequestPaginateTypeDef,
    ListDecoderManifestsResponseTypeDef,
    ListFleetsForVehicleRequestPaginateTypeDef,
    ListFleetsForVehicleResponseTypeDef,
    ListFleetsRequestPaginateTypeDef,
    ListFleetsResponseTypeDef,
    ListModelManifestNodesRequestPaginateTypeDef,
    ListModelManifestNodesResponseTypeDef,
    ListModelManifestsRequestPaginateTypeDef,
    ListModelManifestsResponseTypeDef,
    ListSignalCatalogNodesRequestPaginateTypeDef,
    ListSignalCatalogNodesResponseTypeDef,
    ListSignalCatalogsRequestPaginateTypeDef,
    ListSignalCatalogsResponseTypeDef,
    ListStateTemplatesRequestPaginateTypeDef,
    ListStateTemplatesResponseTypeDef,
    ListVehiclesInFleetRequestPaginateTypeDef,
    ListVehiclesInFleetResponseTypeDef,
    ListVehiclesRequestPaginateTypeDef,
    ListVehiclesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetVehicleStatusPaginator",
    "ListCampaignsPaginator",
    "ListDecoderManifestNetworkInterfacesPaginator",
    "ListDecoderManifestSignalsPaginator",
    "ListDecoderManifestsPaginator",
    "ListFleetsForVehiclePaginator",
    "ListFleetsPaginator",
    "ListModelManifestNodesPaginator",
    "ListModelManifestsPaginator",
    "ListSignalCatalogNodesPaginator",
    "ListSignalCatalogsPaginator",
    "ListStateTemplatesPaginator",
    "ListVehiclesInFleetPaginator",
    "ListVehiclesPaginator",
)

if TYPE_CHECKING:
    _GetVehicleStatusPaginatorBase = AioPaginator[GetVehicleStatusResponseTypeDef]
else:
    _GetVehicleStatusPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetVehicleStatusPaginator(_GetVehicleStatusPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/GetVehicleStatus.html#IoTFleetWise.Paginator.GetVehicleStatus)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#getvehiclestatuspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetVehicleStatusRequestPaginateTypeDef]
    ) -> AioPageIterator[GetVehicleStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/GetVehicleStatus.html#IoTFleetWise.Paginator.GetVehicleStatus.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#getvehiclestatuspaginator)
        """

if TYPE_CHECKING:
    _ListCampaignsPaginatorBase = AioPaginator[ListCampaignsResponseTypeDef]
else:
    _ListCampaignsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCampaignsPaginator(_ListCampaignsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListCampaigns.html#IoTFleetWise.Paginator.ListCampaigns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listcampaignspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCampaignsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCampaignsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListCampaigns.html#IoTFleetWise.Paginator.ListCampaigns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listcampaignspaginator)
        """

if TYPE_CHECKING:
    _ListDecoderManifestNetworkInterfacesPaginatorBase = AioPaginator[
        ListDecoderManifestNetworkInterfacesResponseTypeDef
    ]
else:
    _ListDecoderManifestNetworkInterfacesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDecoderManifestNetworkInterfacesPaginator(
    _ListDecoderManifestNetworkInterfacesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifestNetworkInterfaces.html#IoTFleetWise.Paginator.ListDecoderManifestNetworkInterfaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestnetworkinterfacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDecoderManifestNetworkInterfacesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDecoderManifestNetworkInterfacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifestNetworkInterfaces.html#IoTFleetWise.Paginator.ListDecoderManifestNetworkInterfaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestnetworkinterfacespaginator)
        """

if TYPE_CHECKING:
    _ListDecoderManifestSignalsPaginatorBase = AioPaginator[
        ListDecoderManifestSignalsResponsePaginatorTypeDef
    ]
else:
    _ListDecoderManifestSignalsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDecoderManifestSignalsPaginator(_ListDecoderManifestSignalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifestSignals.html#IoTFleetWise.Paginator.ListDecoderManifestSignals)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestsignalspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDecoderManifestSignalsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDecoderManifestSignalsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifestSignals.html#IoTFleetWise.Paginator.ListDecoderManifestSignals.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestsignalspaginator)
        """

if TYPE_CHECKING:
    _ListDecoderManifestsPaginatorBase = AioPaginator[ListDecoderManifestsResponseTypeDef]
else:
    _ListDecoderManifestsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDecoderManifestsPaginator(_ListDecoderManifestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifests.html#IoTFleetWise.Paginator.ListDecoderManifests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDecoderManifestsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDecoderManifestsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifests.html#IoTFleetWise.Paginator.ListDecoderManifests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestspaginator)
        """

if TYPE_CHECKING:
    _ListFleetsForVehiclePaginatorBase = AioPaginator[ListFleetsForVehicleResponseTypeDef]
else:
    _ListFleetsForVehiclePaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFleetsForVehiclePaginator(_ListFleetsForVehiclePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListFleetsForVehicle.html#IoTFleetWise.Paginator.ListFleetsForVehicle)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listfleetsforvehiclepaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFleetsForVehicleRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFleetsForVehicleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListFleetsForVehicle.html#IoTFleetWise.Paginator.ListFleetsForVehicle.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listfleetsforvehiclepaginator)
        """

if TYPE_CHECKING:
    _ListFleetsPaginatorBase = AioPaginator[ListFleetsResponseTypeDef]
else:
    _ListFleetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFleetsPaginator(_ListFleetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListFleets.html#IoTFleetWise.Paginator.ListFleets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listfleetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFleetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListFleets.html#IoTFleetWise.Paginator.ListFleets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listfleetspaginator)
        """

if TYPE_CHECKING:
    _ListModelManifestNodesPaginatorBase = AioPaginator[ListModelManifestNodesResponseTypeDef]
else:
    _ListModelManifestNodesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListModelManifestNodesPaginator(_ListModelManifestNodesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListModelManifestNodes.html#IoTFleetWise.Paginator.ListModelManifestNodes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listmodelmanifestnodespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelManifestNodesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListModelManifestNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListModelManifestNodes.html#IoTFleetWise.Paginator.ListModelManifestNodes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listmodelmanifestnodespaginator)
        """

if TYPE_CHECKING:
    _ListModelManifestsPaginatorBase = AioPaginator[ListModelManifestsResponseTypeDef]
else:
    _ListModelManifestsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListModelManifestsPaginator(_ListModelManifestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListModelManifests.html#IoTFleetWise.Paginator.ListModelManifests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listmodelmanifestspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelManifestsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListModelManifestsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListModelManifests.html#IoTFleetWise.Paginator.ListModelManifests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listmodelmanifestspaginator)
        """

if TYPE_CHECKING:
    _ListSignalCatalogNodesPaginatorBase = AioPaginator[ListSignalCatalogNodesResponseTypeDef]
else:
    _ListSignalCatalogNodesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSignalCatalogNodesPaginator(_ListSignalCatalogNodesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListSignalCatalogNodes.html#IoTFleetWise.Paginator.ListSignalCatalogNodes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listsignalcatalognodespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSignalCatalogNodesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSignalCatalogNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListSignalCatalogNodes.html#IoTFleetWise.Paginator.ListSignalCatalogNodes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listsignalcatalognodespaginator)
        """

if TYPE_CHECKING:
    _ListSignalCatalogsPaginatorBase = AioPaginator[ListSignalCatalogsResponseTypeDef]
else:
    _ListSignalCatalogsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSignalCatalogsPaginator(_ListSignalCatalogsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListSignalCatalogs.html#IoTFleetWise.Paginator.ListSignalCatalogs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listsignalcatalogspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSignalCatalogsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSignalCatalogsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListSignalCatalogs.html#IoTFleetWise.Paginator.ListSignalCatalogs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listsignalcatalogspaginator)
        """

if TYPE_CHECKING:
    _ListStateTemplatesPaginatorBase = AioPaginator[ListStateTemplatesResponseTypeDef]
else:
    _ListStateTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStateTemplatesPaginator(_ListStateTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListStateTemplates.html#IoTFleetWise.Paginator.ListStateTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#liststatetemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStateTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListStateTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListStateTemplates.html#IoTFleetWise.Paginator.ListStateTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#liststatetemplatespaginator)
        """

if TYPE_CHECKING:
    _ListVehiclesInFleetPaginatorBase = AioPaginator[ListVehiclesInFleetResponseTypeDef]
else:
    _ListVehiclesInFleetPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListVehiclesInFleetPaginator(_ListVehiclesInFleetPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListVehiclesInFleet.html#IoTFleetWise.Paginator.ListVehiclesInFleet)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listvehiclesinfleetpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVehiclesInFleetRequestPaginateTypeDef]
    ) -> AioPageIterator[ListVehiclesInFleetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListVehiclesInFleet.html#IoTFleetWise.Paginator.ListVehiclesInFleet.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listvehiclesinfleetpaginator)
        """

if TYPE_CHECKING:
    _ListVehiclesPaginatorBase = AioPaginator[ListVehiclesResponseTypeDef]
else:
    _ListVehiclesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListVehiclesPaginator(_ListVehiclesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListVehicles.html#IoTFleetWise.Paginator.ListVehicles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listvehiclespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVehiclesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListVehiclesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListVehicles.html#IoTFleetWise.Paginator.ListVehicles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listvehiclespaginator)
        """
