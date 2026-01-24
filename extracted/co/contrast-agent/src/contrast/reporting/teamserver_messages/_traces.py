# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

import requests

from contrast.api.utils import as_camel_dict
from contrast.utils.decorators import fail_loudly
from contrast_vendor import structlog as logging

from .base_ts_message import BaseTsAppMessage

logger = logging.getLogger("contrast")


class _Traces(BaseTsAppMessage):
    """This class should only be instantiated by Preflight's response handler"""

    def __init__(self, finding, reportable_request):
        super().__init__()

        self.extra_headers["Report-Hash"] = str(finding.hash)

        self.body = self._build_body(finding, reportable_request)

    @property
    def name(self) -> str:
        return "traces"

    @property
    def path(self) -> str:
        return "traces"

    @property
    def request_method(self):
        return requests.put

    @fail_loudly("Failed to process Traces response")
    def process_response(self, response, reporting_client):
        self.process_response_code(response, reporting_client)

    def _build_body(self, finding, reportable_request):
        base_body = {
            "created": finding.created,
            "events": [as_camel_dict(event) for event in finding.events],
            "properties": finding.properties,
            "routes": [as_camel_dict(route) for route in finding.routes],
            "ruleId": finding.rule_id,
            "tags": finding.tags,
            "version": finding.version,
        }
        if session_id := self.settings.config.session_id:
            base_body["session_id"] = session_id
        if reportable_request is not None:
            base_body["request"] = reportable_request

        return base_body
