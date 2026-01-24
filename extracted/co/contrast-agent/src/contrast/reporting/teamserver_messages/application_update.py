# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import requests

from .base_ts_message import BaseTsAppMessage
from contrast.utils.decorators import fail_loudly
from contrast_vendor import structlog as logging
from contrast_fireball import Library

logger = logging.getLogger("contrast")


class ApplicationUpdate(BaseTsAppMessage):
    def __init__(self, libraries: list[Library]):
        super().__init__()

        self.extra_headers["Content-Type"] = "application/json"

        # activity message sends "components" aka "architectures"
        # so we will not send the "components" field at this time.

        # field "timestamp" represents the amount of time that has passed
        # since the app settings were changed (not an actual timestamp).
        self.body = {
            "timestamp": self.since_last_update,
            "libraries": [
                {
                    "classCount": lib.class_count,
                    "file": lib.file,
                    "hash": lib.hash,
                    "url": lib.url,
                    "version": lib.version,
                    "externalDate": lib.external_date,
                    "internalDate": lib.internal_date,
                    "tags": self.settings.config.get("inventory.tags"),
                }
                for lib in libraries
                if lib.hash
            ],
        }

    @property
    def name(self):
        return "application-update"

    @property
    def path(self):
        return "update/application"

    @property
    def request_method(self):
        return requests.put

    @fail_loudly("Failed to process ApplicationUpdate response")
    def process_response(self, response, reporting_client):
        self.process_response_code(response, reporting_client)
