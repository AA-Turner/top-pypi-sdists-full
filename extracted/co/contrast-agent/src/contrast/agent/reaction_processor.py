# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.disable_reaction import DisableReaction

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class ReactionProcessor:
    @staticmethod
    def process(application_settings, settings):
        if isinstance(application_settings, list):
            ts_reactions = application_settings

            for reaction in ts_reactions:
                operation = reaction.get("operation", "")
                msg = reaction.get("message", "")

                logger.debug("Received the following reaction: %s %s", operation, msg)

                if operation == DisableReaction.NAME:
                    DisableReaction.run(settings.config)
