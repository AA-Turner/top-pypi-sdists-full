# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.policy.propagators import BasePropagator
from contrast.agent.assess.utils import (
    copy_events,
    copy_tags_in_span,
    get_properties,
)


class SplitPropagator(BasePropagator):
    PARTITION_METHODS = ["partition", "rpartition"]
    REVERSE_METHODS = ["rsplit", "rpartition"]

    def track_target(self):
        # NOP. Let propagate handle the decision to track
        pass

    @property
    def needs_propagation(self):
        return self.any_source_tracked

    def build_event(self, target_properties, tagged):
        parents = [self.source_properties.event] if self.source_properties.event else []
        # For split, the tagged individual string is passed when building the
        # event, but the target is actually the array of strings that was
        # returned by split.
        target_properties.build_event(
            self.node,
            tagged,
            self.preshift.obj,
            self.target,
            self.preshift.args,
            self.preshift.kwargs,
            parents,
            None,
        )

    def add_tags_and_properties(self, ret):
        if self.source_properties is None:
            return

        for target in self.target:
            if self.node.tags:
                self.apply_tags(self.node, target)

            if self.node.untags:
                self.apply_untags(self.node, target)

            target_properties = get_properties(target)
            if target_properties is None:
                continue

            target_properties.add_properties(self.node.properties)

            self.build_event(target_properties, target)

    def propagate(self):
        source = self.sources[0]
        self.source_properties = get_properties(source)
        if self.source_properties is None:
            return

        # Offset in the original string
        source_offset = 0

        reverse = self.node.method_name in self.REVERSE_METHODS

        # The target (result of split) is an array of strings
        target = self.target[::-1] if reverse else self.target

        if self.node.method_name in self.PARTITION_METHODS:
            partition = self.preshift.args[0]
        else:
            partition = None

        for newstr in target:
            if reverse:
                source_offset = source.rfind(newstr)
                source = source[:source_offset]
            else:
                source_offset = source.find(newstr, source_offset)

            if partition and newstr == partition:
                # Make sure that we don't skip another string that just happens
                # to be the same as the partition string.
                partition = None
                continue

            span = (source_offset, source_offset + len(newstr))
            copy_tags_in_span(newstr, self.source_properties, span)

            target_properties = get_properties(newstr)
            if target_properties is not None:
                copy_events(target_properties, self.source_properties)
