# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from contrast.agent.policy import constants
from contrast.agent.assess.assess_exceptions import ContrastAssessException
from contrast.agent.policy.policy_node import PolicyNode
from contrast_fireball import AssessEventType


class SourceNode(PolicyNode):
    ALL = "ALL"

    SOURCE_TAG = "UNTRUSTED"

    def __init__(
        self,
        module,
        class_name="",
        instance_method=True,
        method_name="",
        target="RETURN",
        node_type=None,
        tags=None,
        source_name="",
        version=ALL,
        policy_patch=True,
    ):
        super().__init__(
            module,
            class_name,
            instance_method,
            method_name,
            source_name,
            target,
            tags,
            policy_patch=policy_patch,
        )

        self.version = version
        self.type = node_type

        if tags is None:
            self.tags = {self.SOURCE_TAG}
        else:
            self.tags.add(self.SOURCE_TAG)

        self.validate()

    @classmethod
    def dynamic(cls, module, class_name, column_name, tags, policy_patch=True):
        """
        Create a dynamic source node, one with the dynamic_source_id property.
        """
        instance_method = True
        method_name = column_name
        target = "RETURN"

        node = cls(
            module,
            class_name,
            instance_method,
            method_name,
            target,
            constants.DB_SOURCE_TYPE,
            tags=tags,
            policy_patch=policy_patch,
        )

        node.add_property("dynamic_source_id", node.name)

        return node

    @property
    def node_type(self):
        """
        This is confusing. Sources are Creation action but Propagation type. Oh
        and also Type refers to input type, like parameter, so we have to call
        this node_type. :-/
        """
        return AssessEventType.PROPAGATION

    def validate(self):
        super().validate()

        if not self.targets:
            raise ContrastAssessException(
                f"Source {self.name} did not have a proper target. Unable to create."
            )

        if not self.type:
            raise ContrastAssessException(
                f"Source {self.name} did not have a proper type. Unable to create."
            )
