# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import re

import contrast_fireball

from contrast.agent.agent_lib.input_tracing import (
    InputAnalysisResult,
    check_cmd_injection_query,
)
from contrast.agent.policy.patch_location_policy import PatchLocationPolicy
from contrast_vendor import structlog as logging

from .base_rule import BaseRule

logger = logging.getLogger("contrast")


class CmdInjection(BaseRule):
    """
    Command Injection Protection rule
    """

    RULE_NAME = "cmd-injection"

    FIREBALL_RULE = contrast_fireball.CmdInjection

    def find_sink_attack(
        self,
        candidate_string: str,
        **kwargs,
    ) -> list[contrast_fireball.ProtectEventSample]:
        command_string = str(candidate_string)

        attack_samples = []
        for result in self.worth_watching_results():
            for match in re.finditer(
                re.compile(re.escape(result.input.value)),
                candidate_string,
            ):
                if check_cmd_injection_query(
                    match.start(), len(result.input.value), command_string
                ):
                    attack_sample = self.build_sample(
                        result,
                        candidate_string,
                        self.outcome_from_mode,
                        start_index=match.start(),
                        end_index=match.end(),
                        **kwargs,
                    )
                    attack_samples.append(attack_sample)

        return attack_samples

    def build_sample(
        self,
        evaluation: InputAnalysisResult | None,
        candidate_string: str | None,
        outcome: contrast_fireball.ProtectEventOutcome,
        **kwargs,
    ) -> contrast_fireball.ProtectEventSample:
        assert evaluation is not None
        sample = self.build_base_sample(
            evaluation,
            outcome=outcome or self.outcome_from_mode,
            rule=self.FIREBALL_RULE(
                details=contrast_fireball.CmdInjectionDetails(
                    command=candidate_string,
                    start_index=kwargs["start_index"],
                    end_index=kwargs["end_index"],
                )
                if candidate_string
                else None
            ),
        )

        return sample

    def infilter_kwargs(
        self, user_input: str, patch_policy: PatchLocationPolicy
    ) -> dict[str, object]:
        return dict(method=patch_policy.method_name, original_command=user_input)

    def skip_protect_analysis(
        self, user_input: object, args: tuple, kwargs: dict[str, object]
    ) -> bool:
        """
        cmdi rule supports list user input as well as str and bytes
        Do not skip protect analysis if user input is a  populated list
        """
        if isinstance(user_input, list) and user_input:
            return False

        return super().skip_protect_analysis(user_input, args, kwargs)

    def convert_input(self, user_input: object) -> str:
        if isinstance(user_input, list):
            user_input = " ".join(user_input)

        return super().convert_input(user_input)

    def _infilter(self, match_string: str, **kwargs):
        # TODO: PYT-3088
        #  deserialization_rule = Settings().protect_rules[Deserialization.RULE_NAME]
        #  deserialization_rule.check_for_deserialization()

        super()._infilter(match_string, **kwargs)
