# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import re

from contrast.agent.agent_lib.input_tracing import check_cmd_injection_query
from contrast.agent.protect.rule.mode import Mode
from contrast.utils.loggers.logger import security_log_attack
from .base_rule import BaseRule

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class CmdInjection(BaseRule):
    """
    Command Injection Protection rule
    """

    RULE_NAME = "cmd-injection"

    BIN_SH_C = "/bin/sh-c"

    START_IDX = "start_idx"
    END_IDX = "end_idx"

    def find_attack(self, candidate_string=None, **kwargs):
        command_string = str(candidate_string) if candidate_string else None

        return super().find_attack(command_string, **kwargs)

    def build_attack_with_match(
        self, candidate_string, evaluation=None, attack=None, **kwargs
    ):
        for match in re.finditer(
            re.compile(re.escape(evaluation.input.value)), candidate_string
        ):
            input_len = match.end() - match.start()
            agent_lib_evaluation = check_cmd_injection_query(
                match.start(), input_len, candidate_string
            )
            if not agent_lib_evaluation:
                continue

            evaluation.attack_count += 1

            kwargs["startIndex"] = match.start()
            kwargs["endIndex"] = match.end()
            attack = self.build_or_append_attack(
                evaluation, attack, candidate_string, **kwargs
            )

        if attack is not None:
            attack.response = self.response_from_mode(self.mode)
            security_log_attack(attack, evaluation)

        return attack

    def build_attack_without_match(self, evaluation=None, attack=None, **kwargs):
        if self.mode == Mode.BLOCK_AT_PERIMETER:
            return super().build_attack_without_match(evaluation, attack, **kwargs)
        if evaluation.score < 10:
            return None

        return next(
            (
                super(CmdInjection, self).build_attack_without_match(
                    full_eval, attack, **kwargs
                )
                for full_eval in evaluation.fully_evaluate()
                if full_eval.score >= 90
            ),
            None,
        )

    def build_sample(self, evaluation, command, **kwargs):
        sample = self.build_base_sample(evaluation)
        if command is not None:
            sample.details["command"] = command

        if "startIndex" in kwargs:
            sample.details["startIndex"] = int(kwargs["startIndex"])

        if "endIndex" in kwargs:
            sample.details["endIndex"] = int(kwargs["endIndex"])

        return sample

    def infilter_kwargs(self, user_input, patch_policy):
        return dict(method=patch_policy.method_name, original_command=user_input)

    def skip_protect_analysis(self, user_input, args, kwargs):
        """
        cmdi rule supports list user input as well as str and bytes
        Do not skip protect analysis if user input is a  populated list
        """
        if isinstance(user_input, list) and user_input:
            return False

        return super().skip_protect_analysis(user_input, args, kwargs)

    def convert_input(self, user_input):
        if isinstance(user_input, list):
            user_input = " ".join(user_input)

        return super().convert_input(user_input)

    def _infilter(self, match_string, **kwargs):
        # TODO: PYT-3088
        #  deserialization_rule = Settings().protect_rules[Deserialization.RULE_NAME]
        #  deserialization_rule.check_for_deserialization()

        super()._infilter(match_string, **kwargs)
