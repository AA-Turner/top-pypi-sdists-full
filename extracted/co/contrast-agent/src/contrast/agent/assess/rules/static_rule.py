# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.base_rule import BaseRule
from contrast.agent.assess.rules import build_finding, send_finding


class StaticRule(BaseRule):
    """
    Base class for provider and config-based rules

    These kinds of rules send their findings immediately rather than relying on a
    request context.
    """

    def build_and_send_finding(self, properties, **kwargs):
        finding = build_finding(self, properties, **kwargs)

        self.finding_reported()
        send_finding(finding)
