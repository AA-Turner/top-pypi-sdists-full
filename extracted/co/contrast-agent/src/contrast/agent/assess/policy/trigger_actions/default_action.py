# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from copy import copy

from contrast.agent.assess.tag import Tag
from contrast.agent.assess.utils import get_properties
from contrast.utils.assess.tag_utils import (
    combine,
    is_covered,
    ordered_merge,
    intersection,
)


class DefaultAction:
    """
    Default action used to evaluate whether a trigger rule is violated

    Most trigger nodes simply need to determine whether any of the trigger node sources
    contain an UNTRUSTED range that isn't also covered by a mitigating tag. However,
    some nodes (e.g. some SSRF triggers) may require more sophisticated logic to
    determine whether the rule was violated. These nodes can specify custom actions
    that implement the necessary logic.

    Custom actions must implement (or inherit) the following four attributes:
        * is_violated
        * find_all_tag_ranges
        * find_any_tag_ranges
        * extract_source
        * unwind_source (boolean)
    """

    def is_violated(self, source, required_tags, disallowed_tags, **kwargs):
        if (source_properties := get_properties(source)) is None:
            return False

        # The spec dictates that in order to violate a rule, a range must contain
        # ALL required tags
        vulnerable_tag_ranges = self.find_all_tag_ranges(
            source_properties, required_tags
        )

        if not vulnerable_tag_ranges:
            return False

        # The spec dictates that ANY disallowed tag can mitigate a rule violation
        secure_tag_ranges = self.find_any_tag_ranges(source_properties, disallowed_tags)

        if not secure_tag_ranges:
            return True

        # figure out if there are any vulnerable ranges that aren't
        # covered by a secure one. if there are, the rule was violated
        return not is_covered(vulnerable_tag_ranges, secure_tag_ranges)

    def find_all_tag_ranges(self, properties, desired_tags):
        """
        Find tag ranges that are common to ALL of the given tags

        :param properties:
        :param desired_tags:
        :return: list of Tag instances
        """

        if not properties.is_tracked() or not desired_tags:
            return []

        trimmed = False
        tag_ranges = [Tag(properties.last_tagged_index() + 1, 0)]

        for tag in desired_tags:
            tags = properties.fetch_tags(tag)
            tag_ranges = intersection(tags, tag_ranges)
            trimmed = True

        if not trimmed:
            return []

        return combine(tag_ranges)

    def find_any_tag_ranges(self, properties, desired_tags):
        """
        Find tag ranges that belong to ANY of the given tags

        :param properties:
        :param desired_tags:
        :return: list of Tag instances
        """
        tag_ranges = []

        if not properties.is_tracked() or not desired_tags:
            return tag_ranges

        for tag in desired_tags:
            found = properties.fetch_tags(tag)
            if found:
                tag_ranges = ordered_merge(tag_ranges, copy(found))

        return tag_ranges

    def extract_source(self, source, args, kwargs):
        """
        For some rules (eg ssrf) the source is an object containing a tracked string.
        By default, the source is unmodified.
        This method should be overridden as required.
        """
        return source

    # for sources that are more complex data structures, like lists, dicts, etc., we
    # call `cs__apply_trigger` once per element by default. Set this to False in a
    # subclass to disable this behavior. This will cause `cs__apply_trigger` (and
    # `extract_source`) to receive the original, unmodified source object.
    unwind_source = True

    # unwind_source prevents `trigger_policy.apply` from calling `cs__apply_trigger` on
    # each element of a complex data structure. It doesn't prevent `cs__apply_trigger` from
    # calling itself recursively for complex source data structures. Some rules (e.g. NoSQLi)
    # require this behavior. Set this to False in a subclass to only call `cs__apply_source`
    # exactly once for a single source.
    unwind_source_recurse = True
