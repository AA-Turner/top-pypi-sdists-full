# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from functools import cached_property
import contrast
from contrast.agent import scope
from contrast.agent.agent_lib.input_tracing import (
    InputAnalysisResult,
)
from contrast.agent.settings import Settings
from contrast.api.attack import Attack, ProtectResponse
from contrast.api.sample import Sample
from contrast.agent.protect.rule.mode import Mode
from contrast.utils.decorators import fail_loudly, fail_quietly
from contrast.utils.stack_trace_utils import build_and_clean_stack
from contrast_vendor import structlog as logging
from contrast.utils.loggers.logger import security_log_attack
from contrast.utils.string_utils import ensure_string

logger = logging.getLogger("contrast")


BLOCKING_RULES = frozenset([Mode.BLOCK, Mode.BLOCK_AT_PERIMETER])
PREFILTER_RULES = frozenset([Mode.BLOCK_AT_PERIMETER])
POSTFILTER_RULES = frozenset([Mode.BLOCK, Mode.MONITOR])

PREFILTER = "prefilter"
INFILTER = "infilter"
POSTFILTER = "postfilter"


class BaseRule:
    """
    Base rule object that all protection rules will inherit
    """

    RULE_NAME = "base-rule"

    def __init__(self):
        self.settings = Settings()
        self.settings.protect_rules[self.name] = self
        self.probe_analysis_enabled = self.settings.config.get(
            "protect.probe_analysis.enable"
        )

    @property
    def name(self):
        return self.RULE_NAME

    @property
    def mode(self):
        """
        Return the mode for this rule based.

        Order of precedence:
        1. Config (contract_security.yaml)
        2. Settings from TS
        3. Default mode
        """
        return self.settings.config.get(self.config_rule_path_mode)

    @cached_property
    def config_rule_path_mode(self):
        return f"protect.rules.{self.name}.mode"

    def is_prefilter(self):
        """
        Checks if a rules mode is for prefilter
        """
        return self.enabled and self.mode in PREFILTER_RULES

    def is_postfilter(self):
        """
        Checks if a rules mode is for postfilter
        """
        return self.enabled and self.mode in POSTFILTER_RULES

    def is_blocked(self):
        """
        Checks if a rules mode is for blocking
        """
        return self.enabled and self.mode in BLOCKING_RULES

    @property
    def enabled(self):
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

    def should_block(self, attack):
        return attack and attack.response == ProtectResponse.BLOCKED

    def excluded(self, exclusions):
        """
        Check if rule is being excluded from evaluation
        :param exclusions:
        :return: True if excluded, else False
        """

        if not exclusions or len(exclusions) == 0:
            return False

        logger.debug("Checking %s exclusion(s) in %s", len(exclusions), self.name)
        return any(ex.match_protect_rule(self.name) for ex in exclusions)

    def prefilter(self):
        """
        Scans the input analysis for the rule and looks for matched attack signatures

        Will throw a SecurityException if a response needs to be blocked
        """
        logger.debug("PROTECT: Prefilter for %s", self.name)

        attack = self.find_attack(analysis_stage=PREFILTER)
        if attack is None or len(attack.samples) == 0:
            return

        self._append_to_context(attack)

        if attack.response == ProtectResponse.BLOCKED_AT_PERIMETER:
            raise contrast.SecurityException(rule_name=self.name)

    def _infilter(self, match_string, **kwargs):
        """
        Scans the input analysis for the rule and looks for matched attack signatures. The call to this method may be
        rule specific and include additional context in a args list.
        """
        if self.mode == Mode.OFF:
            return

        logger.debug("PROTECT: Infilter for %s", self.name)

        attack = self.find_attack(match_string, analysis_stage=INFILTER, **kwargs)
        if attack is None or len(attack.samples) == 0:
            return

        self._append_to_context(attack)

        if self.should_block(attack):
            raise contrast.SecurityException(rule_name=self.name)

    @fail_loudly("Failed to run protect rule")
    def protect(self, patch_policy, user_input, args, kwargs):
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

    def infilter_kwargs(self, user_input, patch_policy):
        return {}

    def skip_protect_analysis(self, user_input, args, kwargs):
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

    def convert_input(self, user_input):
        return ensure_string(user_input)

    def postfilter(self):
        """
        Scans the input analysis for the rule and looks for matched attack signatures

        Appends attacker to the context if a positive evaluation is found
        """
        if self.mode == Mode.OFF or not self.probe_analysis_enabled:
            return

        logger.debug("PROTECT: Postfilter", rule=self.name)

        attack = self.find_attack(analysis_stage=POSTFILTER)
        if attack is None or len(attack.samples) == 0:
            return

        self._append_to_context(attack)

        if self.should_block(attack):
            raise contrast.SecurityException(rule_name=self.name)

    def find_attack(self, candidate_string=None, analysis_stage=None, **kwargs):
        """
        Finds the attacker in the original string if present
        """
        if candidate_string is not None:
            logger.debug("Checking for %s in %s", self.name, candidate_string)

        evaluations_for_rule = self.evaluations_for_rule()

        attack = None
        for evaluation in evaluations_for_rule:
            if analysis_stage == POSTFILTER and evaluation.attack_count > 0:
                continue
            if candidate_string:
                if candidate_string.find(evaluation.input.value) == -1:
                    continue

                attack = self.build_attack_with_match(
                    candidate_string, evaluation, attack, **kwargs
                )
            else:
                attack = self.build_attack_without_match(evaluation, attack, **kwargs)

        return attack

    def build_attack_with_match(
        self,
        candidate_string,
        evaluation: InputAnalysisResult | None = None,
        attack: Attack | None = None,
        **kwargs,
    ):
        attack = self.build_or_append_attack(
            evaluation, attack, candidate_string, **kwargs
        )

        if evaluation:
            evaluation.attack_count += 1

        attack.response = self.response_from_mode(self.mode)
        security_log_attack(attack, evaluation)
        return attack

    def build_attack_without_match(
        self,
        evaluation: InputAnalysisResult | None = None,
        attack: Attack | None = None,
        **kwargs,
    ):
        if evaluation and evaluation.score < 10:
            return None
        if self.mode == Mode.BLOCK_AT_PERIMETER:
            attack = self.build_or_append_attack(evaluation, attack, **kwargs)

            attack.response = self.response_from_mode(self.mode)
            security_log_attack(attack, evaluation)
        elif evaluation is None or evaluation.attack_count == 0:
            attack = self.build_or_append_attack(evaluation, attack, **kwargs)
            attack.response = ProtectResponse.PROBED
            security_log_attack(attack, evaluation)

        return attack

    def build_or_append_attack(
        self,
        evaluation: InputAnalysisResult,
        attack: Attack | None = None,
        candidate_string=None,
        **kwargs,
    ):
        if attack is None:
            attack = self.build_base_attack()

        attack.add_sample(self.build_sample(evaluation, candidate_string, **kwargs))

        return attack

    def build_base_attack(self):
        return Attack(self.name)

    def build_sample(self, evaluation: InputAnalysisResult, candidate_string, **kwargs):
        return self.build_base_sample(evaluation)

    def build_user_input(self, evaluation):
        return evaluation.input

    def build_base_sample(self, evaluation, prebuilt_stack=None):
        return Sample(
            user_input=self.build_user_input(evaluation),
            stack=prebuilt_stack if prebuilt_stack else build_and_clean_stack(),
        )

    def _append_to_context(self, attack):
        context = contrast.REQUEST_CONTEXT.get()
        if context is None:
            # do not remove; this case is not yet well-understood
            logger.debug("WARNING: failed to get request context in _append_to_context")
            return

        context.attacks.append(attack)

    _RESPONSE_MAP = {
        Mode.MONITOR: ProtectResponse.MONITORED,
        Mode.BLOCK: ProtectResponse.BLOCKED,
        Mode.BLOCK_AT_PERIMETER: ProtectResponse.BLOCKED_AT_PERIMETER,
        Mode.OFF: ProtectResponse.NO_ACTION,
    }

    def response_from_mode(self, mode):
        return self._RESPONSE_MAP.get(mode)

    def evaluations_for_rule(self, context=None):
        if context is None:
            context = contrast.REQUEST_CONTEXT.get()
        if context is None:
            # do not remove; this case is not yet well-understood
            logger.debug(
                "WARNING: failed to get request context in evaluations_for_rule"
            )
            return []

        return [
            evaluation
            for evaluation in context.user_input_analysis
            if evaluation.rule_id == self.RULE_NAME
        ]

    @fail_quietly("Failed to log user input for protect rule")
    def log_safely(self, method_name, user_input):
        """
        Attempt to log user supplied input but do not fail if unable to do so.
        """
        logger.debug(
            "Applying %s rule method %s with user input %s",
            self.name,
            method_name,
            ensure_string(user_input, errors="replace"),
        )
