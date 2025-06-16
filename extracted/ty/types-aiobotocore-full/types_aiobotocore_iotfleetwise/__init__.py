"""
Main interface for iotfleetwise service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotfleetwise import (
        Client,
        GetVehicleStatusPaginator,
        IoTFleetWiseClient,
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
    async with session.create_client("iotfleetwise") as client:
        client: IoTFleetWiseClient
        ...


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

from .client import IoTFleetWiseClient
from .paginator import (
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

Client = IoTFleetWiseClient


__all__ = (
    "Client",
    "GetVehicleStatusPaginator",
    "IoTFleetWiseClient",
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
