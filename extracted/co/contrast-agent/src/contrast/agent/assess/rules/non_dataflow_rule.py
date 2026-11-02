# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.trigger_rule import TriggerRule


class NonDataflowRule(TriggerRule):
    """
    Rule class used for all non-dataflow rules (i.e. crypto rules).
    """

    def update_preflight_hash(self, hasher, source=None, **kwargs):
        """
        This gets called from `create_finding` in the base class
        """
        # source corresponds to the algorithm name for crytpo rules
        if source is not None:
            hasher.update(source)

    @classmethod
    def from_nodes(cls, name: str, nodes):
        return super().from_nodes(name, False, nodes)
