# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from typing import TYPE_CHECKING

import contrast
from contrast.agent.assess.adjusted_span import AdjustedSpan
from contrast.utils.assess.duck_utils import safe_getattr
from contrast.utils.assess.tag_utils import merge_tags

if TYPE_CHECKING:
    from contrast.agent.assess.properties import Properties


def get_properties(value) -> Properties | None:
    return safe_getattr(value, "cs__properties", None)


def set_properties(obj, props):
    obj.cs__properties = props


def clear_properties():
    contrast.STRING_TRACKER.clear()


def is_trackable(obj):
    return hasattr(obj, "cs__properties")


def is_tracked(value):
    return value in contrast.STRING_TRACKER


def track_string(value):
    return contrast.STRING_TRACKER.track(value)


def track_and_tag(value, label="UNTRUSTED", start=None, end=None):
    properties = track_string(value)
    if not properties:
        return None

    if start is None:
        start = 0
    if end is None:
        end = len(value)

    properties.add_tag(label, AdjustedSpan(start, end))
    return properties


def copy_events(target_props, source_props):
    if (
        source_props is None
        or target_props is None
        or target_props is source_props
        or source_props.event is None
    ):
        return

    target_props.event = source_props.event


def copy_from(to_obj, from_obj, shift=0, skip_tags=None):
    """Copy events and tags from from_obj to to_obj"""
    if from_obj is to_obj:
        return

    if (from_props := get_properties(from_obj)) is None:
        return

    # we assume to_obj has already been tracked and has properties
    to_props = get_properties(to_obj)

    if from_props == to_props:
        return

    copy_events(to_props, from_props)

    for key in from_props.tag_keys():
        if skip_tags and key in skip_tags:
            continue

        from_props_tags = from_props.fetch_tags(key)
        new_tags = [tag.copy_modified(shift) for tag in from_props_tags]

        existing_tags = to_props.fetch_tags(key)

        if existing_tags:
            existing_tags.extend(new_tags)
        else:
            to_props.set_tag(key, new_tags)


def get_last_event_from_sources(sources):
    """
    Gathers from given sources the parent IDs that should be used for an event
    """
    return [
        props.event
        for source in sources
        if (props := get_properties(source)) and props.event
    ]


def copy_tags_in_span(target, source_properties, span, offset=0):
    """
    Given source properties, copies tags at a given span to the target
    """
    span = AdjustedSpan(*tuple(x + offset for x in span))
    source_tags = source_properties.tags_at_range(span)
    if not source_tags:
        return get_properties(target)

    target_properties = track_string(target)
    if target_properties is None:
        return get_properties(target)

    for name, tags in source_tags.items():
        for tag in tags:
            target_properties.add_existing_tag(name, tag)

    merge_tags(target_properties.tags)
    return target_properties


def copy_tags_to_offset(target_properties, source_tags, target_offset):
    """
    Given source tags, copy to target properties at offset.

    The caller is responsible for updating the string tracker if necessary.
    """
    for name, tags in source_tags.items():
        for tag in tags:
            new_tag = tag.copy_modified(target_offset)
            target_properties.add_existing_tag(name, new_tag)
