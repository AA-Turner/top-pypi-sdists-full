# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections import defaultdict
from functools import cached_property
from itertools import chain
import contrast

from contrast.agent.policy import constants
from contrast.agent.assess.assess_exceptions import ContrastAssessException
from contrast.agent.policy.trigger_node import TriggerNode
from contrast.agent.policy.utils import generate_policy
from contrast.agent.assess.rules import build_finding, send_finding
from contrast.agent.assess.rules.base_rule import BaseRule
from contrast.utils.assess.duck_utils import safe_getattr


from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class TriggerRule(BaseRule):
    UNTRUSTED = "UNTRUSTED"

    ENCODER_START = "CUSTOM_ENCODED_"
    VALIDATOR_START = "CUSTOM_VALIDATED_"
    # If a level 1 rule comes from TeamServer, it will have the
    # tag "custom-encoder-#{name}" or "custom-validator-#{name}".
    # All rules should take this into account.
    # Additionally, if something is marked "limited-chars" it means
    # it has been properly vetted to not contain dangerous input.
    LIMITED_CHARS = "LIMITED_CHARS"
    CUSTOM_ENCODED = "CUSTOM_ENCODED"
    CUSTOM_VALIDATED = "CUSTOM_VALIDATED"

    def __init__(
        self, name: str, dataflow: bool, disallowed_tags=None, required_tags=None
    ):
        self._name = name

        self.dataflow = dataflow
        # Mapping of (module, method) -> [TriggerNode]
        self._nodes: defaultdict[tuple[str, str], list[TriggerNode]] = defaultdict(list)

        self.required_tags = []
        self.populate_tags(required_tags)

        self.disallowed_tags = []
        self.populate_disallowed(disallowed_tags)

        super().__init__()

    @property
    def name(self):
        return self._name

    @property
    def disabled(self):
        """
        Property indicating whether rule is disabled
        """
        if super().disabled:
            return True

        ctx = contrast.REQUEST_CONTEXT.get()
        if ctx is None:
            return False

        return bool(
            ctx.excluded_assess_rules and self.name in ctx.excluded_assess_rules
        )

    @cached_property
    def loud_name(self):
        return str(self.name.upper().replace("-", "_"))

    @property
    def nodes(self):
        return list(chain.from_iterable(self._nodes.values()))

    def populate_tags(self, required_tags):
        if not self.dataflow:
            return

        self.validate_tags(required_tags)

        self.required_tags = required_tags if required_tags else []
        if self.UNTRUSTED not in self.required_tags:
            self.required_tags.append(self.UNTRUSTED)

    def populate_disallowed(self, disallowed_tags):
        if not self.dataflow:
            return

        self.validate_tags(disallowed_tags)

        self.disallowed_tags = disallowed_tags if disallowed_tags else []

        self.disallowed_tags.append(self.LIMITED_CHARS)
        self.disallowed_tags.append(self.CUSTOM_ENCODED)
        self.disallowed_tags.append(self.CUSTOM_VALIDATED)
        self.disallowed_tags.append(self.ENCODER_START + self.loud_name)
        self.disallowed_tags.append(self.VALIDATOR_START + self.loud_name)

    def validate_tags(self, tags):
        if not tags:
            return

        for item in tags:
            if (
                item not in constants.VALID_TAGS
                and item not in constants.VALID_SOURCE_TAGS
            ):
                raise ContrastAssessException(
                    f"Rule {self.name} had an invalid tag. {item} is not a known value"
                )

    def _is_violated(self, node, source, **kwargs):
        return node.trigger_action.is_violated(
            source, self.required_tags, self.disallowed_tags, **kwargs
        )

    def is_violated_properties(self, node, properties):
        """
        Determine whether rule was violated based on properties
        """
        return self._is_violated(node, properties)

    def is_violated(self, node, source, **kwargs):
        """
        Determine whether rule was violated based on source object
        """
        if self.count_threshold_reached():
            return False

        # The rule is violated if the object is marked as source
        if safe_getattr(source, "cs__source", False):
            return True

        return self._is_violated(node, source, **kwargs)

    def extract_source(self, node, source, args, kwargs):
        """
        Extract source from given source string based on trigger action
        """
        return node.trigger_action.extract_source(source, args, kwargs)

    def find_trigger_nodes(self, module: str, method: str) -> list[TriggerNode]:
        """
        Find the trigger node matching the module and method for this rule
        """
        return self._nodes[(module, method)]

    def create_finding(self, properties, node, target, **kwargs):
        return build_finding(self, properties, **kwargs)

    def build_and_append_finding(
        self,
        context,
        properties: dict[str, str],
        node,
        target,
        **kwargs,
    ):
        finding = self.create_finding(
            properties,
            node,
            target,
            request=context.request.to_fireball_assess_request(),
            **kwargs,
        )

        # if after creating the finding, we discover that this finding already exists
        # in context, then do not add it and return early
        for curr_finding in context.findings:
            if finding.hash == curr_finding.hash:
                return

        logger.debug(
            "Trigger %s detected: %s triggered %s",
            node.name,
            str(id(target)),
            self.name,
        )

        self.finding_reported()
        send_finding(finding, context)

    JSON_NAME = "name"
    JSON_DISALLOWED_TAGS = "disallowed_tags"
    JSON_REQUIRED_TAGS = "required_tags"
    JSON_NODES = "nodes"
    JSON_DATAFLOW = "dataflow"

    @classmethod
    def from_nodes(
        cls, name: str, dataflow: bool, nodes, disallowed_tags=None, required_tags=None
    ):
        instance = cls(name, dataflow, disallowed_tags, required_tags)
        for node in generate_policy(
            TriggerNode,
            nodes,
            dataflow=instance.dataflow,
        ):
            instance._nodes[(node.location, node.method_name)].append(node)

        return instance

    def __repr__(self):
        return f"{self.__class__.__name__} - {self.name}"
