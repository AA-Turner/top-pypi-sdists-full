# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import contextlib
from collections.abc import Generator, Mapping
from typing import Any, Protocol

import contrast_fireball

from contrast.agent.request import Request
from contrast.configuration.agent_config import AgentConfig


class Reporter(Protocol):
    # NOTE: server_type is separate from config because its default value
    # is generated at runtime.
    def initialize_application(
        self, config: AgentConfig, server_type=""
    ) -> dict[str, object]: ...

    def get_settings_if_changed(
        self,
    ) -> contrast_fireball.InitTeamServerSettings | None: ...

    def new_effective_config(self, effective_config_report: Any) -> None: ...

    def new_discovered_routes(self, routes: set[contrast_fireball.DiscoveredRoute]): ...

    def new_observed_route(self, route: contrast_fireball.ObservedRoute): ...

    def new_protect_events(
        self, events: list[contrast_fireball.ProtectEventSample]
    ): ...

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

    def new_server_inventory(self, inventory: contrast_fireball.ServerInventory): ...

    @contextlib.contextmanager
    def observability_trace(
        self,
        *,
        send_trace: bool,
        attributes: contrast_fireball.OtelAttributes | None = None,
    ) -> Generator: ...


def get_reporting_client(config: Mapping) -> Reporter:
    client_type = config.get("api.reporting_client")
    if client_type == "fireball":
        from contrast.reporting.fireball import Client
    elif client_type == "direct":
        from contrast.reporting.reporting_client import ReportingClient as Client
    else:
        raise ValueError(f"Invalid reporting client: {client_type}")

    return Client()
