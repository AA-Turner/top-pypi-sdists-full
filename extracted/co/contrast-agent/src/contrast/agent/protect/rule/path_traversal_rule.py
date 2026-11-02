# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from typing import TYPE_CHECKING

import contrast_fireball

from contrast.agent.protect.rule.base_rule import BaseRule

if TYPE_CHECKING:
    from contrast.agent.agent_lib.input_tracing import InputAnalysisResult
    from contrast.agent.policy.patch_location_policy import PatchLocationPolicy


class PathTraversal(BaseRule):
    RULE_NAME = "path-traversal"
    FIREBALL_RULE = contrast_fireball.PathTraversal

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
            outcome=outcome,
            rule=self.FIREBALL_RULE(
                details=contrast_fireball.PathTraversalDetails(
                    path=path,
                )
                if (path := candidate_string)
                else None
            ),
        )
        return sample

    def infilter_kwargs(self, user_input: str, patch_policy: PatchLocationPolicy):
        return dict(method=patch_policy.method_name)
