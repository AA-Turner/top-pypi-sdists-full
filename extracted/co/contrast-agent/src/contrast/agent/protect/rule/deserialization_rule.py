# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.agent_lib.input_tracing import InputAnalysisResult
from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.agent.protect.rule.deserialization.pickle_searcher import PickleSearcher
from contrast.agent.protect.rule.deserialization.yaml_searcher import YAMLSearcher
from contrast.api import user_input
from contrast.utils.string_utils import ends_with_any
from contrast.utils.stack_trace_utils import build_and_clean_stack

from contrast_vendor import structlog as logging
import contextlib

logger = logging.getLogger("contrast")


class Deserialization(BaseRule):
    """
    Deserialization Protection rule
    """

    RULE_NAME = "untrusted-deserialization"

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
    def custom_searchers(self):
        return [PickleSearcher(), YAMLSearcher()]

    def is_prefilter(self):
        return False

    def is_postfilter(self):
        return False

    def skip_protect_analysis(self, user_input, args, kwargs):
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

    def convert_input(self, user_input):
        if isinstance(user_input, (str, bytes)):
            data = user_input
        else:
            data = self._get_stream_data(user_input)

        return super().convert_input(data)

    def _get_stream_data(self, user_input):
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

    def find_attack(self, candidate_string=None, **kwargs):
        """
        Finds the attacker in the original string if present
        """
        if candidate_string is not None:
            logger.debug("Checking for %s in %s", self.name, candidate_string)

        attack = None
        if self.evaluate_custom_searchers(candidate_string):
            evaluation = self.build_evaluation(candidate_string)
            attack = self.build_attack_with_match(
                candidate_string, evaluation, attack, **kwargs
            )

        return attack

    def report_attack_without_finding(self, value, **kwargs):
        attack = self.build_attack_with_match(value, None, **kwargs)
        self._append_to_context(attack)

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

    def build_sample(self, evaluation, input_value, **kwargs):
        sample = self.build_base_sample(evaluation)

        sample.details["command"] = False

        if "deserializer" in kwargs:
            sample.details["deserializer"] = kwargs["deserializer"]

        return sample

    def evaluate_custom_searchers(self, attack_vector):
        searcher_score = 0
        for searcher in self.custom_searchers:
            impact = searcher.impact_of(attack_vector)

            if impact > 0:
                logger.debug("Match on custom searcher: %s", searcher.searcher_id)

                searcher_score += impact
                if searcher_score >= searcher.IMPACT_HIGH:
                    return True

        return False

    def build_evaluation(self, value) -> InputAnalysisResult:
        """
        Given a user-input value, aka gadget, create an InputAnalysisResult instance.

        :param value: the user input containing a Gadget
        """
        return InputAnalysisResult(
            user_input.UserInput(type=user_input.InputType.UNKNOWN, value=value),
            self.RULE_NAME,
            0,
        )

    def infilter_kwargs(self, user_input, patch_policy):
        stack_elements = build_and_clean_stack()

        return dict(
            deserializer=patch_policy.method_name, stack_elements=stack_elements
        )
