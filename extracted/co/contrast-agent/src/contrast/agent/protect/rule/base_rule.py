# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from dataclasses import asdict, replace
from functools import cached_property
from typing import TYPE_CHECKING

from contrast_fireball import (
    ProtectEventInput,
    ProtectEventOutcome,
    ProtectEventSample,
    ProtectEventSource,
    ProtectEventStackFrame,
    ProtectRule,
    ProtectTimestamp,
)

import contrast
from contrast.agent import scope
from contrast.agent.agent_lib.input_tracing import (
    InputAnalysisResult,
)
from contrast.agent.policy.patch_location_policy import PatchLocationPolicy
from contrast.agent.protect.rule.mode import Mode
from contrast.agent.settings import Settings
from contrast.utils.decorators import fail_loudly, fail_quietly
from contrast.utils.stack_trace_utils import build_protect_stack
from contrast.utils.string_utils import ensure_string
from contrast.utils.timer import now_ms
from contrast_vendor import structlog as logging

if TYPE_CHECKING:
    from contrast.agent.request_context import RequestContext


logger = logging.getLogger("contrast")


BLOCKING_RULES = frozenset([Mode.BLOCK, Mode.BLOCK_AT_PERIMETER])
PREFILTER_RULES = frozenset([Mode.BLOCK_AT_PERIMETER])
POSTFILTER_RULES = frozenset([Mode.BLOCK, Mode.MONITOR])


class BaseRule:
    """
    Base rule object that all protection rules will inherit
    """

    RULE_NAME = "base-rule"
    FIREBALL_RULE: ProtectRule

    def __init__(self):
        self.settings = Settings()
        self.settings.protect_rules[self.name] = self
        self.probe_analysis_enabled = self.settings.config.get(
            "protect.probe_analysis.enable"
        )
        self.is_worth_watching_rule = self.name in ("cmd-injection", "sql-injection")

    @property
    def name(self):
        return self.RULE_NAME

    @property
    def mode(self) -> Mode:
        return self.settings.config.get(self.config_rule_path_mode, Mode.OFF)

    @cached_property
    def config_rule_path_mode(self) -> str:
        return f"protect.rules.{self.name}.mode"

    def is_prefilter(self) -> bool:
        """
        Checks if a rules mode is for prefilter
        """
        return self.enabled and self.mode in PREFILTER_RULES

    def is_postfilter(self) -> bool:
        """
        Checks if a rules mode is for postfilter
        """
        return self.enabled and self.mode in POSTFILTER_RULES

    def is_blocked(self) -> bool:
        """
        Checks if a rules mode is for blocking
        """
        return self.enabled and self.mode in BLOCKING_RULES

    @property
    def enabled(self) -> bool:
        """
        A rule is enabled only if all 3 conditions are met:
        1. rule is not in disabled rules list
        2. rule mode is not OFF
        3. an exclusion wasn't applied from Teamserver
        """
        disabled_rules = self.settings.config.get("protect.rules.disabled_rules")
        if disabled_rules and self.name in disabled_rules:
            return False

        req_ctx = contrast.REQUEST_CONTEXT.get()
        if req_ctx is not None and req_ctx.excluded_protect_rules:
            return self.name not in req_ctx.excluded_protect_rules

        return self.mode != Mode.OFF

    def should_block(self, attack_events: list[ProtectEventSample]) -> bool:
        return any(
            sample.outcome == ProtectEventOutcome.BLOCKED for sample in attack_events
        )

    def prefilter(self):
        """
        Scans the input analysis for the rule and looks for matched attack signatures

        Will throw a SecurityException if a response needs to be blocked
        """
        logger.debug("PROTECT: Prefilter for %s", self.name)

        if results := self.full_analysis_results():
            attack_events = self.build_perimeter_attack_event(results)
            self._extend_context(attack_events)

            if any(
                sample.outcome == ProtectEventOutcome.BLOCKED_AT_PERIMETER
                for sample in attack_events
            ):
                raise contrast.SecurityException(rule_name=self.name)

    def build_perimeter_attack_event(
        self, results: list[InputAnalysisResult]
    ) -> list[ProtectEventSample]:
        outcome = (
            ProtectEventOutcome.BLOCKED_AT_PERIMETER
            if (
                self.mode == Mode.BLOCK_AT_PERIMETER
                and any(e.score >= 90 for e in results)
            )
            else ProtectEventOutcome.SUSPICIOUS
        )

        samples = [
            self.build_sample(result, outcome=outcome, candidate_string=None)
            for result in results
        ]
        return samples

    def _infilter(self, match_string: str, **kwargs):
        """
        Scans the input analysis for the rule and looks for matched attack signatures. The call to this method may be
        rule specific and include additional context in a args list.
        """
        if self.mode == Mode.OFF:
            return

        logger.debug("PROTECT: Infilter for %s", self.name)
        attack_events = self.find_sink_attack(match_string, **kwargs)
        if not attack_events:
            return

        self._extend_context(attack_events)

        if self.should_block(attack_events):
            raise contrast.SecurityException(rule_name=self.name)

    @fail_loudly("Failed to run protect rule")
    def protect(
        self,
        patch_policy: PatchLocationPolicy,
        user_input: object,
        args: tuple,
        kwargs: dict[str, object],
    ):
        if not self.enabled:
            return

        if self.skip_protect_analysis(user_input, args, kwargs):
            return

        with scope.contrast_scope():
            user_input = self.convert_input(user_input)
            if not user_input:
                return

            self.log_safely(patch_policy.method_name, user_input)

            self._infilter(user_input, **self.infilter_kwargs(user_input, patch_policy))

    def infilter_kwargs(self, user_input: str, patch_policy: PatchLocationPolicy):
        return {}

    def skip_protect_analysis(
        self, user_input: object, args: tuple, kwargs: dict[str, object]
    ) -> bool:
        """
        We only want to run protect on user input that is of a type supported
        by the rule.

        Most rules use this implementation, but some override this depending on
        expected user input types.

        :return: Bool if to skip running protect infilter
        """
        if not user_input:
            return True

        if isinstance(user_input, (str, bytes)):
            return False

        logger.debug(
            "WARNING: unknown input type %s for rule %s", type(user_input), self.name
        )

        return True

    def convert_input(self, user_input: object) -> str:
        return ensure_string(user_input)

    def find_sink_attack(
        self,
        candidate_string: str,
        **kwargs,
    ) -> list[ProtectEventSample]:
        """
        Finds the attacker in the original string if present
        """
        if not candidate_string:
            return []

        logger.debug("Checking for %s in %s", self.name, candidate_string)

        attack_samples = [
            self.build_sample(
                result, candidate_string, self.outcome_from_mode, **kwargs
            )
            for result in self.worth_watching_results()
            if result.input.value in candidate_string
        ]
        return attack_samples

    def postfilter(self):
        """
        Scans the input analysis for the rule and looks for matched attack signatures

        Appends attacker to the context if a positive evaluation is found
        """
        if self.mode == Mode.OFF or not self.probe_analysis_enabled:
            return

        logger.debug("PROTECT: Postfilter", rule=self.name)

        if probe_results := self.probe_results():
            self._extend_context(self.build_probe_attack_event(probe_results))

    def build_probe_attack_event(
        self, results: list[InputAnalysisResult]
    ) -> list[ProtectEventSample]:
        samples = [
            self.build_sample(
                result, outcome=ProtectEventOutcome.PROBED, candidate_string=None
            )
            for result in results
        ]
        return samples

    def build_sample(
        self,
        evaluation: InputAnalysisResult | None,
        candidate_string: str | None,
        outcome: ProtectEventOutcome,
        **kwargs,
    ) -> ProtectEventSample:
        assert evaluation is not None
        return self.build_base_sample(
            evaluation,
            outcome=outcome,
            rule=self.FIREBALL_RULE(details=None),
        )

    def build_user_input(self, evaluation: InputAnalysisResult) -> ProtectEventInput:
        return evaluation.input

    def build_base_sample(
        self,
        evaluation: InputAnalysisResult | None,
        rule: ProtectRule,
        outcome: ProtectEventOutcome,
        prebuilt_stack: list[ProtectEventStackFrame] | None = None,
    ) -> ProtectEventSample:
        """Builds the base ProtectEventSample for a given input analysis result and rule.

        The returned ProtectEventSample will have sensitive data redacted according to masking
        rules.
        """

        if evaluation is not None:
            evaluation.attack_count += 1

        context = contrast.REQUEST_CONTEXT.get()
        assert context is not None

        request = context.request
        input = self.build_user_input(evaluation)
        if context.request_data_masker:
            context.request_data_masker.mask_sensitive_data(request)
            input = context.request_data_masker.mask_attack_input(input)
            if (
                rule.details
                and context.request_data_masker.mask_rules.mask_attack_vector
            ):
                rule = replace(
                    rule,
                    details=type(rule.details)(
                        **{
                            k: context.request_data_masker.mask_attack_vector(v)
                            if isinstance(v, str)
                            else v
                            for k, v in asdict(rule.details).items()
                        }
                    ),
                )

        return ProtectEventSample(
            rule=rule,
            outcome=outcome,
            source=ProtectEventSource(
                ip=request.client_addr,
                x_forwarded_for=request.headers.get("X-Forwarded-For"),
            ),
            input=input,
            request=request.to_fireball_request(),
            route=None,  # TODO: PYT-3982, populate for Incident Traces.
            stack=prebuilt_stack if prebuilt_stack else build_protect_stack(),
            timestamp=ProtectTimestamp(now_ms()),
        )

    def _extend_context(self, attack_events: list[ProtectEventSample]):
        context = contrast.REQUEST_CONTEXT.get()
        if context is None:
            # do not remove; this case is not yet well-understood
            logger.debug("WARNING: failed to get request context in _append_to_context")
            return

        context.attack_events.extend(attack_events)

    _OUTCOME_MAP = {
        Mode.MONITOR: ProtectEventOutcome.EXPLOITED,
        Mode.BLOCK: ProtectEventOutcome.BLOCKED,
        Mode.BLOCK_AT_PERIMETER: ProtectEventOutcome.BLOCKED_AT_PERIMETER,
    }

    @property
    def outcome_from_mode(self) -> ProtectEventOutcome:
        return self._OUTCOME_MAP[self.mode]

    def worth_watching_results(
        self, context: RequestContext | None = None
    ) -> list[InputAnalysisResult]:
        """
        Returns analysis results that are worth watching. For some rules, this
        list could be a super-set of the full analysis results.
        """
        if context is None:
            context = contrast.REQUEST_CONTEXT.get()
        if context is None:
            # do not remove; this case is not yet well-understood
            logger.debug(
                "WARNING: failed to get request context in worth_watching_results"
            )
            return []

        return [
            evaluation
            for evaluation in context.user_input_analysis
            if evaluation.rule_id == self.RULE_NAME
        ]

    def full_analysis_results(self, context: RequestContext | None = None):
        """
        Returns fully evaluated analysis results for this rule.
        """
        worth_watching_results = self.worth_watching_results(context)
        if self.is_worth_watching_rule:
            full_results = [
                full_result
                for ww_result in worth_watching_results
                if (full_result := ww_result.fully_evaluate())
            ]
            return full_results
        else:
            # No additional analysis is needed if not a worth-watching rule
            return worth_watching_results

    def probe_results(self) -> list[InputAnalysisResult]:
        """
        Returns probe analysis results for this rule.

        Probe results include any input analysis result with a score >= 90
        that hasn't already been reported in an attack.
        """
        return [
            full_result
            for full_result in self.full_analysis_results()
            if full_result.attack_count == 0 and full_result.score >= 90
        ]

    @fail_quietly("Failed to log user input for protect rule")
    def log_safely(self, method_name: str, user_input: object):
        """
        Attempt to log user supplied input but do not fail if unable to do so.
        """
        logger.debug(
            "Applying %s rule method %s with user input %s",
            self.name,
            method_name,
            ensure_string(user_input, errors="replace"),
        )
