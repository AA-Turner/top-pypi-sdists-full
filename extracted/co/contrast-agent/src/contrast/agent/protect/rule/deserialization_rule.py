# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import contextlib

import contrast_fireball
from contrast_fireball import (
    AttackInputType,
    DocumentType,
    ProtectEventInput,
    ProtectEventSample,
)

from contrast.agent.agent_lib.input_tracing import InputAnalysisResult
from contrast.agent.policy.patch_location_policy import PatchLocationPolicy
from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.agent.protect.rule.deserialization.custom_searcher import CustomSearcher
from contrast.agent.protect.rule.deserialization.pickle_searcher import PickleSearcher
from contrast.agent.protect.rule.deserialization.yaml_searcher import YAMLSearcher
from contrast.utils.stack_trace_utils import build_protect_stack
from contrast.utils.string_utils import ends_with_any
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class Deserialization(BaseRule):
    """
    Deserialization Protection rule
    """

    RULE_NAME = "untrusted-deserialization"
    FIREBALL_RULE = contrast_fireball.UntrustedDeserialization

    # pickle and pyyaml both use load
    METHODS = [
        "loads",
        "load",
        "construct_object",
        "construct_python_object_apply",
        "construct_mapping",
        "make_python_instance",
    ]
    FILENAMES = ["pickle.py", "yaml.constructor.py", "yaml.__init__.py"]

    UNKNOWN = "UNKNOWN"

    @property
    def custom_searchers(self) -> list[CustomSearcher]:
        return [PickleSearcher(), YAMLSearcher()]

    def is_prefilter(self) -> bool:
        return False

    def is_postfilter(self) -> bool:
        return False

    def skip_protect_analysis(
        self, user_input: object, args: tuple, kwargs: dict[str, object]
    ) -> bool:
        """
        Deserialization rule will receive io streams as user input.

        :return: Bool if to skip running protect infilter
        """
        if not user_input:
            return True

        # checking if obj has attr "read" is more robust than using isinstance
        if hasattr(user_input, "read"):
            return False

        return super().skip_protect_analysis(user_input, args, kwargs)

    def convert_input(self, user_input: object) -> str:
        if isinstance(user_input, (str, bytes)):
            data = user_input
        else:
            data = self._get_stream_data(user_input)

        return super().convert_input(data)

    def _get_stream_data(self, user_input: object) -> str:
        """
        Get data from a stream object but make sure to return the stream position
        to the original location.

        :param user_input: obj we expect to be a stream with attrs read, tell and seek
        :return: str or bytes
        """
        if not all(hasattr(user_input, attr) for attr in ["read", "tell", "seek"]):
            return ""

        # Find current steam position
        try:
            seek_loc = user_input.tell()
        except Exception:
            seek_loc = 0

        # Read the object data
        try:
            data = user_input.read()
        except Exception:
            data = ""

        # Return object to original stream position so it can be re-read
        with contextlib.suppress(Exception):
            user_input.seek(seek_loc)

        return data

    def find_sink_attack(
        self,
        candidate_string: str | None = None,
        **kwargs,
    ) -> list[ProtectEventSample]:
        """
        Finds the attacker in the original string if present
        """
        assert candidate_string is not None
        logger.debug("Checking for %s in %s", self.name, candidate_string)

        attack_samples = []
        if self.evaluate_custom_searchers(candidate_string):
            evaluation = self.build_evaluation(candidate_string)
            attack_samples = [
                self.build_sample(
                    evaluation, candidate_string, self.outcome_from_mode, **kwargs
                )
            ]

        return attack_samples

    def check_for_deserialization(self):
        """
        For the sandbox feature of this rule, we need to determine if we're in a deserializer when a command is called.
        Command injection's infilter method should call this to check and let us handle attack detection and exception
        raising before doing their work.
        """
        found_on_stack = False

        # TODO: PYT-3088 get the stack_elements
        stack_elements = []
        for element in stack_elements[::-1]:
            lower_file_name = element.file_name.lower()

            if (
                element.method_name
                and element.method_name in self.METHODS
                and (
                    lower_file_name in self.FILENAMES
                    or ends_with_any(lower_file_name, self.FILENAMES)
                )
            ):
                found_on_stack = True
                break

        # TODO: PYT-3088
        #  determine what value to pass here; modify this method signature as needed
        if found_on_stack:
            pass
        #     self.report_attack_without_finding("")
        #     if self.should_block(attack):
        #         raise contrast.SecurityException(rule_name=self.name)

    def build_sample(
        self,
        evaluation: InputAnalysisResult | None,
        candidate_string: str | None,
        outcome: contrast_fireball.ProtectEventOutcome,
        **kwargs,
    ) -> ProtectEventSample:
        assert evaluation is not None
        sample = self.build_base_sample(
            evaluation,
            outcome=outcome or self.outcome_from_mode,
            rule=self.FIREBALL_RULE(
                details=contrast_fireball.UntrustedDeserializationDetails(
                    deserializer=kwargs["deserializer"],
                    command=False,
                )
                if "deserializer" in kwargs
                else None
            ),
        )

        return sample

    def evaluate_custom_searchers(self, attack_vector: str):
        searcher_score = 0
        for searcher in self.custom_searchers:
            impact = searcher.impact_of(attack_vector)

            if impact > 0:
                logger.debug("Match on custom searcher: %s", searcher.searcher_id)

                searcher_score += impact
                if searcher_score >= searcher.IMPACT_HIGH:
                    return True

        return False

    def build_evaluation(self, value: str) -> InputAnalysisResult:
        """
        Given a user-input value, aka gadget, create an InputAnalysisResult instance.

        :param value: the user input containing a Gadget
        """
        return InputAnalysisResult(
            ProtectEventInput(
                filters=[],
                input_type=AttackInputType.UNKNOWN,
                time=None,
                value=value,
                document_type=DocumentType.NORMAL,
            ),
            self.RULE_NAME,
            0,
        )

    def infilter_kwargs(self, user_input: str, patch_policy: PatchLocationPolicy):
        stack_elements = build_protect_stack()

        return dict(
            deserializer=patch_policy.method_name, stack_elements=stack_elements
        )
