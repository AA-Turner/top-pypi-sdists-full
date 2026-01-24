# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.trigger_rule import TriggerRule
from contrast_fireball import AssessEvent


class DataflowRule(TriggerRule):
    """
    Rule class used for all dataflow rules. Hash computation includes events.
    """

    def update_preflight_hash(self, hasher, events: list[AssessEvent] = None, **kwargs):
        """
        This gets called from `create_finding` in the base class

        It turns out that only three things differentiate dataflow findings:
            1. The name of the rule that was triggered
            2. The name and type of the source event(s)
            3. The request context

        Information from the current request is used to update the hash at the
        end of the request lifecycle in middleware.
        """
        for event in events or []:
            for source in event.event_sources:
                hasher.update(source.source_type)
                hasher.update(source.source_name)

    @classmethod
    def from_nodes(cls, name, nodes, disallowed_tags=None, required_tags=None):
        return super().from_nodes(name, True, nodes, disallowed_tags, required_tags)
