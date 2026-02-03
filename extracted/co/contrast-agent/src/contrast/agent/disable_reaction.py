# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from typing import Any

from contrast.configuration.agent_config import AgentConfig
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class DisableReaction:
    NAME = "DISABLE"
    ENABLE = "enable"
    MESSAGE = "Contrast received instructions to disable itself - Disabling now"

    @staticmethod
    def run(
        config: AgentConfig,
        *,
        reason: str,
        additional_info: dict[str, Any] | None = None,
    ):
        logger.warning(
            DisableReaction.MESSAGE, reason=reason, **(additional_info or {})
        )

        if config:
            enable_option = config.get_option("enable")
            # We need to set the override here in case the Agent is set to enable by a higher precedence option like
            # env var.
            enable_option.override_value = False
            # But we also set the UI option b/c the value technically came from TeamServer
            enable_option.ui_value = False
