# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.base_rule import BaseRule
from contrast.agent.assess.rules import build_finding, send_finding


class BaseResponseRule(BaseRule):
    EXCLUDED_RESPONSE_CODES = [301, 302, 307, 404, 410, 500]
    EXCLUDED_CONTENT_TYPES = ["json", "xml"]

    @property
    def name(self):
        raise NotImplementedError

    def is_violated(self, header, body, form_tags, meta_tags):
        raise NotImplementedError

    def is_valid(self, status_code, content_type):
        """
        Rule is valid for analysis if response has matching content-type and status-code
        :return: bool
        """
        return not (
            status_code in self.EXCLUDED_RESPONSE_CODES
            or any(
                [
                    c_type
                    for c_type in self.EXCLUDED_CONTENT_TYPES
                    if c_type in content_type
                ]
            )
        )

    def update_preflight_hash(self, hasher, **kwargs):
        # Response rules do not update the hash
        pass

    def create_finding(self, properties):
        return build_finding(self, properties)

    def build_and_append_finding(self, properties, context):
        finding = self.create_finding(properties)
        send_finding(finding, context)
