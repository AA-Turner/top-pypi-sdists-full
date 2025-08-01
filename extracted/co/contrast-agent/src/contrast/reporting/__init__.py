# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations


from collections.abc import Generator, Mapping
import contextlib
from typing import Protocol


from contrast.agent.request import Request
from contrast.configuration.agent_config import AgentConfig
from contrast.reporting.teamserver_messages.base_ts_message import BaseTsMessage
import contrast_fireball


class Reporter(Protocol):
    # NOTE: server_type is separate from config because its default value
    # is generated at runtime.
    def initialize_application(self, config: AgentConfig, server_type="") -> bool: ...

    def new_discovered_routes(self, routes: set[contrast_fireball.DiscoveredRoute]): ...

    def new_observed_route(self, route: contrast_fireball.ObservedRoute): ...

    # new_findings is a batching method, but the Fireball client
    # will accept a single finding at a time and batch them internally.
    # When Fireball is the primary reporting client, we should consider
    # moving findings to a fire-and-forget model instead of batching.
    def new_findings(
        self, findings: list[contrast_fireball.AssessFinding], request: Request | None
    ): ...

    def new_libraries(self, libraries: list[contrast_fireball.Library]): ...

    def new_library_observations(
        self, observations: list[contrast_fireball.LibraryObservation]
    ): ...

    def new_inventory_components(
        self, components: list[contrast_fireball.InventoryComponent]
    ): ...

    @contextlib.contextmanager
    def observability_trace(
        self,
        *,
        send_trace: bool,
        attributes: contrast_fireball.OtelAttributes | None = None,
    ) -> Generator: ...

    # Legacy methods from direct reporting
    def add_message(self, msg: BaseTsMessage): ...

    def send_message(self, msg: BaseTsMessage): ...

    def retry_message(self, msg: BaseTsMessage): ...


def get_reporting_client(config: Mapping) -> Reporter:
    client_type = config.get("api.reporting_client")
    if client_type == "fireball":
        from contrast.reporting.fireball import Client
    elif client_type == "direct":
        from contrast.reporting.reporting_client import ReportingClient as Client
    else:
        raise ValueError(f"Invalid reporting client: {client_type}")

    return Client()
