# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import re

import contrast_fireball

from contrast.agent.agent_lib import input_tracing
from contrast.agent.policy.patch_location_policy import PatchLocationPolicy
from contrast.agent.protect.rule.base_rule import BaseRule


class SqlInjection(BaseRule):
    """
    SQL Injection Protection rule
    """

    RULE_NAME = "sql-injection"
    FIREBALL_RULE = contrast_fireball.SqlInjection

    def find_sink_attack(
        self,
        candidate_string: str,
        **kwargs,
    ) -> list[contrast_fireball.ProtectEventSample]:
        attack_samples = []
        for result in self.worth_watching_results():
            for match in re.finditer(
                re.compile(re.escape(result.input.value)),
                candidate_string,
            ):
                if full_evaluation := input_tracing.check_sql_injection_query(
                    match.start(),
                    len(result.input.value),
                    input_tracing.DBType.from_str(kwargs["database"]),
                    candidate_string,
                ):
                    attack_sample = self.build_sample(
                        result,
                        candidate_string,
                        self.outcome_from_mode,
                        start_idx=match.start(),
                        end_idx=match.end(),
                        boundary_overrun_idx=full_evaluation.boundary_overrun_index,
                        input_boundary_idx=full_evaluation.input_boundary_index,
                        **kwargs,
                    )
                    attack_samples.append(attack_sample)

        return attack_samples

    def build_sample(
        self,
        evaluation: input_tracing.InputAnalysisResult | None,
        candidate_string: str | None,
        outcome: contrast_fireball.ProtectEventOutcome,
        **kwargs,
    ) -> contrast_fireball.ProtectEventSample:
        assert evaluation is not None
        sample = self.build_base_sample(
            evaluation,
            outcome=outcome or self.outcome_from_mode,
            rule=self.FIREBALL_RULE(
                details=contrast_fireball.SqlInjectionDetails(
                    query=query,
                    start=kwargs["start_idx"],
                    end=kwargs["end_idx"],
                    boundary_overrun_index=kwargs["boundary_overrun_idx"],
                    input_boundary_index=kwargs["input_boundary_idx"],
                )
                if (query := candidate_string)
                else None,
            ),
        )

        return sample

    def infilter_kwargs(self, user_input: str, patch_policy: PatchLocationPolicy):
        return dict(database=patch_policy.module)

    def skip_protect_analysis(
        self, user_input: object, args: tuple, kwargs: dict[str, object]
    ) -> bool:
        """
        Some sql libraries use special objects (see from sqlalchemy import text)
        so we cannot just check if user_input is falsy.
        """
        return user_input is None
