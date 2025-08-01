# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from contrast_fireball import InventoryComponent, ArchitectureComponent, Browser
import requests
from dataclasses import asdict

from contrast.agent.request import Request
from contrast.api.attack import Attack
from contrast.reporting.request_masker import RequestMasker

from .base_ts_message import BaseTsAppMessage
from contrast.utils.decorators import fail_loudly
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class ApplicationActivity(BaseTsAppMessage):
    def __init__(
        self,
        *,
        inventory_components: list[InventoryComponent] | None = None,
        attacks: list[Attack] | None = None,
        request: Request | None = None,
        request_data_masker: RequestMasker | None = None,
    ):
        super().__init__()

        if inventory_components is None:
            inventory_components = []
        if attacks is None:
            attacks = []

        self.body = {"lastUpdate": self.since_last_update}

        self.body["inventory"] = {
            # Used by TeamServer to aggregate counts across a given time period, for
            # Protect and attacker activity.
            "activityDuration": 0,
            "components": [],
        }
        if architecture_components := [
            asdict(c)
            for c in inventory_components
            if isinstance(c, ArchitectureComponent)
        ]:
            self.body["inventory"]["components"] = architecture_components
        if browsers := [c for c in inventory_components if isinstance(c, Browser)]:
            self.body["inventory"]["browsers"] = browsers
        if attacks and request:
            self.body["defend"] = {"attackers": []}

            for attack in attacks:
                self.body["defend"]["attackers"].append(
                    {
                        "protectionRules": {
                            attack.rule_id: attack.to_json(request, request_data_masker)
                        },
                        "source": {
                            "ip": request.client_addr or "",
                            "xForwardedFor": request.headers.get("X-Forwarded-For")
                            or "",
                        },
                    }
                )

    @property
    def name(self):
        return "application-activity"

    @property
    def path(self):
        return "activity/application"

    @property
    def request_method(self):
        return requests.put

    @property
    def expected_response_codes(self):
        return [200, 204]

    @fail_loudly("Failed to process Activity response")
    def process_response(self, response, reporting_client):
        if not self.process_response_code(response, reporting_client):
            return

        body = response.json()

        self.settings.process_ts_reactions(body)
