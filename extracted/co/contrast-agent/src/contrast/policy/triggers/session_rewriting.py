# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.triggers.session_rewriting_rule import (
    SessionRewritingRule,
)
from contrast.agent.policy.registry import register_trigger_rule


register_trigger_rule(
    SessionRewritingRule.from_nodes(
        "session-rewriting",
        [
            {
                # default use_cookies is True which is a safe value
                "module": "beaker.session",
                "class_name": "Session",
                "method_name": "__init__",
                "source": "ARG_3,KWARG:use_cookies",
            }
        ],
    )
)
