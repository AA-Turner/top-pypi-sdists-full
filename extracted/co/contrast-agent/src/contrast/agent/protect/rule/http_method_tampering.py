# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import contrast_fireball

import contrast
from contrast.agent.agent_lib.input_tracing import InputAnalysisResult
from contrast.agent.protect.rule.base_rule import BaseRule
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class MethodTampering(BaseRule):
    RULE_NAME = "method-tampering"
    FIREBALL_RULE = contrast_fireball.MethodTampering

    def postfilter(self):
        """
        At postfilter we generate activity if input analysis was found and depending on application response code.

        If response code is either 4xx or 5xx, application was not exploited (only probed) by an unexpected HTTP method.
        If response code is anything else, then an unexpected HTTP method successfully exploited the application.
        """
        logger.debug("PROTECT: Postfilter", rule=self.name)

        worth_watching_results = self.worth_watching_results()
        assert len(worth_watching_results) <= 1
        if not worth_watching_results:
            return

        result = worth_watching_results[0]

        context = contrast.REQUEST_CONTEXT.get()

        # do not remove; this case is not yet well-understood
        if (
            context is None
            or not hasattr(context, "response")
            or context.response is None
        ):
            logger.debug("WARNING: failed to get context in MethodTampering.postfilter")
            return

        response_code = context.response.status_code
        if str(response_code).startswith("4") or str(response_code).startswith("5"):
            if not self.probe_analysis_enabled:
                logger.debug(
                    "PROTECT: skipping probe report",
                    reason="probe analysis disabled",
                    rule=self.name,
                )
                return

            samples = self.build_probe_attack_event([result])

        else:
            samples = [
                self.build_sample(
                    evaluation=result,
                    candidate_string=None,
                    outcome=self.outcome_from_mode,
                    method=result.input.value,
                    response_code=response_code,
                )
            ]

        assert samples is not None
        context.attack_events.extend(samples)

    def build_sample(
        self,
        evaluation: InputAnalysisResult | None,
        candidate_string: str | None,
        outcome: contrast_fireball.ProtectEventOutcome,
        **kwargs,
    ) -> contrast_fireball.ProtectEventSample:
        assert evaluation is not None
        context = contrast.REQUEST_CONTEXT.get()
        assert context is not None
        assert context.response is not None

        sample = self.build_base_sample(
            evaluation,
            outcome=outcome or self.outcome_from_mode,
            rule=self.FIREBALL_RULE(
                details=contrast_fireball.MethodTamperingDetails(
                    method=evaluation.input.value,
                    response_code=context.response.status_code,
                )
            ),
        )

        return sample
