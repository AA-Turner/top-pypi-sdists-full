"""
Main interface for mediaconnect service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_mediaconnect import (
        Client,
        DestinationEndpointConnectedWaiter,
        DestinationEndpointDeregisteredWaiter,
        DestinationEndpointDisconnectedWaiter,
        DestinationEndpointRegisteredWaiter,
        FlowActiveWaiter,
        FlowDeletedWaiter,
        FlowStandbyWaiter,
        InputActiveWaiter,
        InputDeletedWaiter,
        InputStandbyWaiter,
        ListBridgesPaginator,
        ListDestinationEndpointsPaginator,
        ListEntitlementsPaginator,
        ListFlowsPaginator,
        ListGatewayInstancesPaginator,
        ListGatewaysPaginator,
        ListOfferingsPaginator,
        ListReservationsPaginator,
        ListRouterInputsPaginator,
        ListRouterNetworkInterfacesPaginator,
        ListRouterOutputsPaginator,
        ListSourceEndpointsPaginator,
        MediaConnectClient,
        OutputActiveWaiter,
        OutputDeletedWaiter,
        OutputRoutedWaiter,
        OutputStandbyWaiter,
        OutputUnroutedWaiter,
        SourceEndpointConnectedWaiter,
        SourceEndpointConnectingWaiter,
        SourceEndpointDeregisteredWaiter,
        SourceEndpointDisconnectedWaiter,
        SourceEndpointDisconnectingWaiter,
        SourceEndpointRegisteredWaiter,
    )

    session = Session()
    client: MediaConnectClient = session.client("mediaconnect")

    destination_endpoint_connected_waiter: DestinationEndpointConnectedWaiter = client.get_waiter("destination_endpoint_connected")
    destination_endpoint_deregistered_waiter: DestinationEndpointDeregisteredWaiter = client.get_waiter("destination_endpoint_deregistered")
    destination_endpoint_disconnected_waiter: DestinationEndpointDisconnectedWaiter = client.get_waiter("destination_endpoint_disconnected")
    destination_endpoint_registered_waiter: DestinationEndpointRegisteredWaiter = client.get_waiter("destination_endpoint_registered")
    flow_active_waiter: FlowActiveWaiter = client.get_waiter("flow_active")
    flow_deleted_waiter: FlowDeletedWaiter = client.get_waiter("flow_deleted")
    flow_standby_waiter: FlowStandbyWaiter = client.get_waiter("flow_standby")
    input_active_waiter: InputActiveWaiter = client.get_waiter("input_active")
    input_deleted_waiter: InputDeletedWaiter = client.get_waiter("input_deleted")
    input_standby_waiter: InputStandbyWaiter = client.get_waiter("input_standby")
    output_active_waiter: OutputActiveWaiter = client.get_waiter("output_active")
    output_deleted_waiter: OutputDeletedWaiter = client.get_waiter("output_deleted")
    output_routed_waiter: OutputRoutedWaiter = client.get_waiter("output_routed")
    output_standby_waiter: OutputStandbyWaiter = client.get_waiter("output_standby")
    output_unrouted_waiter: OutputUnroutedWaiter = client.get_waiter("output_unrouted")
    source_endpoint_connected_waiter: SourceEndpointConnectedWaiter = client.get_waiter("source_endpoint_connected")
    source_endpoint_connecting_waiter: SourceEndpointConnectingWaiter = client.get_waiter("source_endpoint_connecting")
    source_endpoint_deregistered_waiter: SourceEndpointDeregisteredWaiter = client.get_waiter("source_endpoint_deregistered")
    source_endpoint_disconnected_waiter: SourceEndpointDisconnectedWaiter = client.get_waiter("source_endpoint_disconnected")
    source_endpoint_disconnecting_waiter: SourceEndpointDisconnectingWaiter = client.get_waiter("source_endpoint_disconnecting")
    source_endpoint_registered_waiter: SourceEndpointRegisteredWaiter = client.get_waiter("source_endpoint_registered")

    list_bridges_paginator: ListBridgesPaginator = client.get_paginator("list_bridges")
    list_destination_endpoints_paginator: ListDestinationEndpointsPaginator = client.get_paginator("list_destination_endpoints")
    list_entitlements_paginator: ListEntitlementsPaginator = client.get_paginator("list_entitlements")
    list_flows_paginator: ListFlowsPaginator = client.get_paginator("list_flows")
    list_gateway_instances_paginator: ListGatewayInstancesPaginator = client.get_paginator("list_gateway_instances")
    list_gateways_paginator: ListGatewaysPaginator = client.get_paginator("list_gateways")
    list_offerings_paginator: ListOfferingsPaginator = client.get_paginator("list_offerings")
    list_reservations_paginator: ListReservationsPaginator = client.get_paginator("list_reservations")
    list_router_inputs_paginator: ListRouterInputsPaginator = client.get_paginator("list_router_inputs")
    list_router_network_interfaces_paginator: ListRouterNetworkInterfacesPaginator = client.get_paginator("list_router_network_interfaces")
    list_router_outputs_paginator: ListRouterOutputsPaginator = client.get_paginator("list_router_outputs")
    list_source_endpoints_paginator: ListSourceEndpointsPaginator = client.get_paginator("list_source_endpoints")
    ```
"""

from .client import MediaConnectClient
from .paginator import (
    ListBridgesPaginator,
    ListDestinationEndpointsPaginator,
    ListEntitlementsPaginator,
    ListFlowsPaginator,
    ListGatewayInstancesPaginator,
    ListGatewaysPaginator,
    ListOfferingsPaginator,
    ListReservationsPaginator,
    ListRouterInputsPaginator,
    ListRouterNetworkInterfacesPaginator,
    ListRouterOutputsPaginator,
    ListSourceEndpointsPaginator,
)
from .waiter import (
    DestinationEndpointConnectedWaiter,
    DestinationEndpointDeregisteredWaiter,
    DestinationEndpointDisconnectedWaiter,
    DestinationEndpointRegisteredWaiter,
    FlowActiveWaiter,
    FlowDeletedWaiter,
    FlowStandbyWaiter,
    InputActiveWaiter,
    InputDeletedWaiter,
    InputStandbyWaiter,
    OutputActiveWaiter,
    OutputDeletedWaiter,
    OutputRoutedWaiter,
    OutputStandbyWaiter,
    OutputUnroutedWaiter,
    SourceEndpointConnectedWaiter,
    SourceEndpointConnectingWaiter,
    SourceEndpointDeregisteredWaiter,
    SourceEndpointDisconnectedWaiter,
    SourceEndpointDisconnectingWaiter,
    SourceEndpointRegisteredWaiter,
)

Client = MediaConnectClient


__all__ = (
    "Client",
    "DestinationEndpointConnectedWaiter",
    "DestinationEndpointDeregisteredWaiter",
    "DestinationEndpointDisconnectedWaiter",
    "DestinationEndpointRegisteredWaiter",
    "FlowActiveWaiter",
    "FlowDeletedWaiter",
    "FlowStandbyWaiter",
    "InputActiveWaiter",
    "InputDeletedWaiter",
    "InputStandbyWaiter",
    "ListBridgesPaginator",
    "ListDestinationEndpointsPaginator",
    "ListEntitlementsPaginator",
    "ListFlowsPaginator",
    "ListGatewayInstancesPaginator",
    "ListGatewaysPaginator",
    "ListOfferingsPaginator",
    "ListReservationsPaginator",
    "ListRouterInputsPaginator",
    "ListRouterNetworkInterfacesPaginator",
    "ListRouterOutputsPaginator",
    "ListSourceEndpointsPaginator",
    "MediaConnectClient",
    "OutputActiveWaiter",
    "OutputDeletedWaiter",
    "OutputRoutedWaiter",
    "OutputStandbyWaiter",
    "OutputUnroutedWaiter",
    "SourceEndpointConnectedWaiter",
    "SourceEndpointConnectingWaiter",
    "SourceEndpointDeregisteredWaiter",
    "SourceEndpointDisconnectedWaiter",
    "SourceEndpointDisconnectingWaiter",
    "SourceEndpointRegisteredWaiter",
)
