# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import contrast_fireball
import requests

from contrast.utils.decorators import fail_loudly

from .base_ts_message import BaseTsServerMessage


class ServerInventory(BaseTsServerMessage):
    def __init__(
        self,
        inventory: contrast_fireball.ServerInventory,
    ):
        super().__init__()

        self.base_url = f"{self.settings.api_url}/agents/v1.1/"

        self.body: dict[str, str | bool | dict[str, int]] = {
            "operating_system": inventory.operating_system,
            "runtime_path": inventory.runtime_path,
            "runtime_version": inventory.runtime_version,
            "hostname": inventory.hostname,
        }

        if inventory.cloud_provider and inventory.cloud_resource_id:
            self.body["cloud_provider"] = inventory.cloud_provider
            self.body["cloud_resource_id"] = inventory.cloud_resource_id

        if inventory.is_kubernetes:
            self.body["is_kubernetes"] = True

        if inventory.is_docker:
            self.body["is_docker"] = True

        if (
            inventory.memory_metrics
            and inventory.memory_metrics.process_memory_limit_bytes is not None
        ):
            self.body["memory_metrics"] = {
                "process_memory_limit_bytes": inventory.memory_metrics.process_memory_limit_bytes,
            }

    @property
    def name(self) -> str:
        return "server-inventory"

    @property
    def path(self) -> str:
        return "/".join(
            [
                "servers",
                self.server_name_b64,
                self.server_path_b64,
                self.server_type_b64,
                "inventory",
            ]
        )

    @property
    def request_method(self):
        return requests.post

    @fail_loudly()
    def process_response(self, response, reporting_client):
        self.process_response_code(response, reporting_client)
