# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import requests

from .base_ts_message import BaseTsAppMessage, PYTHON
from ._traces import _Traces
from contrast.utils.decorators import fail_loudly
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class Preflight(BaseTsAppMessage):
    def __init__(self, findings, request):
        super().__init__()

        self.findings = findings
        # NOTE: we cannot send our Request object to other threads, because its data is
        # invalidated by webob once the server sends the associated response. Any work
        # that needs to happen with the request object must be guaranteed to finish
        # before our middleware sends back a response.
        self.reportable_request = request and request.reportable_format

        self.body = {"messages": []}
        for idx, finding in enumerate(self.findings):
            message = {
                "appLanguage": PYTHON,
                "appName": self.agent_state.get_app_name(),
                "appPath": self.settings.app_path,
                "appVersion": self.settings.app_version,
                "code": "TRACE",
                "data": f"{finding.rule_id},{finding.hash}",
                "key": idx,
            }
            self.body["messages"].append(message)

    @property
    def name(self):
        return "preflight"

    @property
    def path(self):
        return "preflight"

    @property
    def request_method(self):
        return requests.put

    @property
    def expected_response_codes(self):
        return [200]

    @fail_loudly("Failed to process Preflight response")
    def process_response(self, response, reporting_client):
        logger.debug("PREFLIGHT: Processing message")
        if not self.process_response_code(response, reporting_client):
            logger.debug("PREFLIGHT: invalid response code; exiting")
            return

        body = response.text
        finding_idxs_to_report = self._parse_body(body)
        if finding_idxs_to_report is not None and len(finding_idxs_to_report) > 0:
            logger.debug("PREFLIGHT: found indexes to report")
        else:
            logger.debug("PREFLIGHT: no indexes to report; exiting")
        for finding_idx in finding_idxs_to_report:
            finding = self.findings[finding_idx]
            logger.debug(
                "PREFLIGHT: generating Trace from finding for %s", finding.rule_id
            )
            traces_msg = _Traces(finding, self.reportable_request)
            logger.debug("PREFLIGHT: generated Trace from finding; queuing")
            reporting_client.add_message(traces_msg)
            logger.debug("PREFLIGHT: Trace queued")

    @staticmethod
    def _parse_body(body):
        """
        A preflight response body is a comma-separated list of finding indices that
        should be reported in a Traces message. Some elements of this list will have a
        *, meaning TS needs an AppCreate message before it will accept this finding.
        We've decided in PYT-2119 to not send findings with a *.
        """
        indices = body.strip('"').split(",")
        return [int(index) for index in indices if index.isdigit()]
