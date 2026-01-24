# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import contrast_fireball

from contrast.agent.agent_lib.input_tracing import InputAnalysisResult
from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.agent.protect.rule.mode import Mode


class BotBlocker(BaseRule):
    RULE_NAME = "bot-blocker"
    FIREBALL_RULE = contrast_fireball.BotBlocker

    def is_prefilter(self) -> bool:
        return self.enabled

    @property
    def mode(self) -> Mode:
        """
        Translate BLOCK mode to BLOCK_AT_PERIMETER
        """
        mode = self.settings.config.get(self.config_rule_path_mode)

        return Mode.BLOCK_AT_PERIMETER if mode == Mode.BLOCK else mode

    def build_sample(
        self,
        evaluation: InputAnalysisResult | None,
        candidate_string: str | None,
        outcome: contrast_fireball.ProtectEventOutcome,
        **kwargs,
    ) -> contrast_fireball.ProtectEventSample:
        sample = self.build_base_sample(
            evaluation,
            outcome=outcome or self.outcome_from_mode,
            rule=self.FIREBALL_RULE(
                details=contrast_fireball.BotBlockerDetails(
                    bot=evaluation.input.filters[0], user_agent=evaluation.input.value
                )
            ),
        )
        return sample
