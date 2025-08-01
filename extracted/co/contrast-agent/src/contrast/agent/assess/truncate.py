# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from contrast.agent.assess.tag import Tag


ELLIPSIS = "..."
TRUNCATION_FRAGMENT_LENGTH = 50
TRUNCATION_LENGTH = TRUNCATION_FRAGMENT_LENGTH * 2 + len(ELLIPSIS)


def truncate(str_representation, length_factor=1):
    """
    Truncate + return the provided string
    """
    fragment_length = TRUNCATION_FRAGMENT_LENGTH * length_factor
    if len(str_representation) <= 2 * fragment_length + len(ELLIPSIS):
        return str_representation
    return "".join(
        [
            str_representation[:fragment_length],
            ELLIPSIS,
            str_representation[-fragment_length:],
        ]
    )


def truncate_tainted_string(
    str_representation: str, tags: list[Tag] | None
) -> tuple[str, list[Tag]]:
    """
    Truncate + return the provided string and update the provided event's taint_ranges
    accordingly.

    This function assumes:
    - event.taint_ranges has already been calculated
    - each range in event.taint_ranges follows the format "{}:{}"
    - str_representation is the string representation of the tainted object associated
      with the given event, i.e. event.taint_ranges describes str_representation
    """
    if len(str_representation) <= TRUNCATION_LENGTH:
        return str_representation, tags or []
    if not tags:
        return truncate(str_representation), tags or []

    return _truncate_tainted_string(str_representation, tags)


def _truncate_tainted_string(
    str_representation: str, merged_tags: list[Tag]
) -> tuple[str, list[Tag]]:
    """
    The core logic of tainted string truncation. Given a string and a list of simplified
    and merged Tags, truncate the string approximately according to this specification:

    https://github.com/Contrast-Security-Inc/assess-specifications/blob/master/vulnerability/truncate-event-snapshots.md

    Note: this follows the specification very closely, but not exactly.
    """
    truncated = ""
    truncated_ranges = []
    curr_index = 0
    for tag in merged_tags:
        if curr_index < tag.start_index:
            truncated += truncate(str_representation[curr_index : tag.start_index])
        new_fragment = truncate(
            str_representation[tag.start_index : tag.end_index], length_factor=2
        )
        truncated += new_fragment
        truncated_ranges.append(
            Tag.from_range(len(truncated) - len(new_fragment), len(truncated))
        )
        curr_index = tag.end_index
    if curr_index < len(str_representation):
        truncated += truncate(str_representation[curr_index:])

    return truncated, truncated_ranges
