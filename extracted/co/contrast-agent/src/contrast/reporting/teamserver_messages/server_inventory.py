# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from typing import Literal
import requests

from .base_ts_message import BaseTsServerMessage
from contrast.utils.decorators import fail_loudly


class ServerInventory(BaseTsServerMessage):
    def __init__(
        self,
        *,
        operating_system: str,
        runtime_path: str,
        runtime_version: str,
        hostname: str,
        is_kubernetes: bool,
        is_docker: bool,
        cloud_provider: Literal["aws", "azure"] | None,
        cloud_resource_id: str | None,
        process_memory_limit_bytes: int | None,
    ):
        super().__init__()

        self.base_url = f"{self.settings.api_url}/agents/v1.1/"

        self.body: dict[str, str | dict[str, int]] = {
            "operating_system": operating_system,
            "runtime_path": runtime_path,
            "runtime_version": runtime_version,
            "hostname": hostname,
        }

        if cloud_provider and cloud_resource_id:
            self.body["cloud_provider"] = cloud_provider
            self.body["cloud_resource_id"] = cloud_resource_id

        if is_kubernetes:
            self.body["is_kubernetes"] = "true"

        if is_docker:
            self.body["is_docker"] = "true"

        if process_memory_limit_bytes is not None:
            self.body["memory_metrics"] = {
                "process_memory_limit_bytes": process_memory_limit_bytes,
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
