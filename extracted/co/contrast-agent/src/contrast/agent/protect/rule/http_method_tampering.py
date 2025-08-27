# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast
from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.api.user_input import InputType

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class MethodTampering(BaseRule):
    RULE_NAME = "method-tampering"
    USER_INPUT_KEY = InputType.METHOD.name

    def postfilter(self):
        """
        At postfilter we generate activity if input analysis was found and depending on application response code.

        If response code is either 4xx or 5xx, application was not exploited (only probed) by an unexpected HTTP method.
        If response code is anything else, then an unexpected HTTP method successfully exploited the application.
        """
        logger.debug("PROTECT: Postfilter", rule=self.name)

        evaluations_for_rule = self.evaluations_for_rule()

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
            context.attacks.extend(
                self.build_attack_without_match(
                    evaluation=evaluation,
                    method=evaluation.input.value,
                    response_code=response_code,
                )
                for evaluation in evaluations_for_rule
            )
        else:
            context.attacks.extend(
                self.build_attack_with_match(
                    None,
                    evaluation=evaluation,
                    method=evaluation.input.value,
                    response_code=response_code,
                )
                for evaluation in evaluations_for_rule
            )

    def build_sample(self, evaluation, candidate_string, **kwargs):
        sample = self.build_base_sample(evaluation)

        sample.details["method"] = kwargs.get("method", "")
        sample.details["responseCode"] = kwargs.get("response_code", -1)

        return sample
