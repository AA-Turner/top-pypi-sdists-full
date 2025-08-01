# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import re
from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.agent.agent_lib import input_tracing
from contrast.agent.protect.rule.mode import Mode
from contrast.utils.loggers.logger import security_log_attack


class SqlInjection(BaseRule):
    """
    SQL Injection Protection rule
    """

    RULE_NAME = "sql-injection"

    def build_attack_with_match(
        self, candidate_string, evaluation=None, attack=None, **kwargs
    ):
        for match in re.finditer(
            re.compile(re.escape(evaluation.input.value)), candidate_string
        ):
            input_len = match.end() - match.start()
            agent_lib_evaluation = input_tracing.check_sql_injection_query(
                match.start(),
                input_len,
                input_tracing.DBType.from_str(kwargs.get("database")),
                candidate_string,
            )
            if not agent_lib_evaluation:
                continue

            evaluation.attack_count += 1

            kwargs["start_idx"] = match.start()
            kwargs["end_idx"] = match.end()
            kwargs["boundary_overrun_idx"] = agent_lib_evaluation.boundary_overrun_index
            kwargs["input_boundary_idx"] = agent_lib_evaluation.input_boundary_index
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
                super(SqlInjection, self).build_attack_without_match(
                    full_eval, attack, **kwargs
                )
                for full_eval in evaluation.fully_evaluate()
                if full_eval.score >= 90
            ),
            None,
        )

    def build_sample(self, evaluation, query, **kwargs):
        sample = self.build_base_sample(evaluation)
        if query is not None:
            sample.details["query"] = query

        if "start_idx" in kwargs:
            sample.details["start"] = int(kwargs["start_idx"])

        if "end_idx" in kwargs:
            sample.details["end"] = int(kwargs["end_idx"])

        if "boundary_overrun_idx" in kwargs:
            sample.details["boundaryOverrunIndex"] = int(kwargs["boundary_overrun_idx"])

        if "input_boundary_idx" in kwargs:
            sample.details["inputBoundaryIndex"] = int(kwargs["input_boundary_idx"])

        return sample

    def infilter_kwargs(self, user_input, patch_policy):
        return dict(database=patch_policy.module)

    def skip_protect_analysis(self, user_input, args, kwargs):
        """
        Some sql libraries use special objects (see from sqlalchemy import text)
        so we cannot just check if user_input is falsy.
        """
        return user_input is None
