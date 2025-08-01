# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.adjusted_span import AdjustedSpan
from contrast.agent.assess.policy.propagators import BasePropagator
from contrast.agent.assess.utils import copy_events, get_properties
from contrast.utils.assess.tag_utils import merge_tags


class SlicePropagator(BasePropagator):
    def _propagate(self):
        slice_: slice = self.preshift.args[0]
        source_properties = get_properties(self.preshift.obj)

        if slice_.step in (1, None):
            # fast path for common case of step=1
            obj_len = self.preshift.obj_length
            start, stop, _ = slice_.indices(obj_len)
            span = AdjustedSpan(start, stop)
            source_tags = source_properties.tags_at_range(span)
            for label, rng in source_tags.items():
                self.target_properties.add_existing_tag(label, rng)

        else:
            # slow but correct
            #
            # This walks the source string's slice view, index by index
            # and copies each tag individually to the target string.
            # For large slices, this is slower than the fast path above.

            # This is like the coolest thing ever. I found it here:
            # https://stackoverflow.com/a/42883770/4312739
            # It converts a slice to a range of indices
            offsets = list(range(self.preshift.obj_length)[slice_])

            for target_offset, source_offset in enumerate(offsets):
                span = AdjustedSpan(source_offset, source_offset + 1)
                source_tags = source_properties.tags_at_range(span)
                for name in source_tags:
                    end_offset = target_offset + 1
                    new_span = AdjustedSpan(target_offset, end_offset)
                    self.target_properties.add_tag(name, new_span)

        copy_events(self.target_properties, source_properties)
        merge_tags(self.target_properties.tags)
