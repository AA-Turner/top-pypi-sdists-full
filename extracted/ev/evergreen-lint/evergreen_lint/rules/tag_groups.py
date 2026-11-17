"""Shared tag group checking, used by the rules that enforce tag groups on tasks and variants."""
from __future__ import annotations

import re
from typing import Iterable, List, NamedTuple, Optional

from evergreen_lint.model import LintError


class TagGroupsConfig(NamedTuple):
    group_name: str
    tag_list: List[str]
    min_num_of_tags: int = 0
    max_num_of_tags: int = 1000
    tag_regex: Optional[str] = None


def check_tag_groups(
    kind: str,
    name: str,
    tags: Optional[Iterable[str]],
    tag_groups: List[TagGroupsConfig],
) -> List[LintError]:
    """
    Check the tags of a single task or build variant against the tag groups.

    :param kind: What is being checked, as it should appear in the messages, e.g. "task".
    :param name: Name of the task or build variant being checked.
    :param tags: The tags of the task or build variant. None is treated as no tags.
    :param tag_groups: The tag groups to enforce.
    """
    tag_regex_mismatch_error_msg = (
        "{kind_capitalized} tags requirement is not met. The {kind} '{name}' has tags that"
        " matches '{tag_regex}' tag regex of '{group_name}' tag group and is not listed in the"
        " group: {tag_list}. Please remove the following tag(s) from the {kind}"
        " '{name}': {tags_to_remove}."
    )
    num_of_tags_mismatch_error_msg = (
        "{kind_capitalized} tags requirement is not met. The {kind} '{name}' should have no less"
        " than '{min_num_of_tags}' and no more than '{max_num_of_tags}' tag(s) of"
        " '{group_name}' tag group list: {tag_list}. Found tags: {matching_tags}."
        " Please add/remove tag(s) of the tag group list to/from the {kind} '{name}'"
        " to match the requirement."
    )

    failed_checks = []
    actual_tags_set = set(tags) if tags is not None else set()

    for tag_group_config in tag_groups:
        matching_tag_regex_tags = actual_tags_set
        if tag_group_config.tag_regex is not None:
            matching_tag_regex_tags = {
                t for t in actual_tags_set if re.match(tag_group_config.tag_regex, t)
            }

        matching_tag_list_tags = {
            t for t in matching_tag_regex_tags if t in tag_group_config.tag_list
        }
        tags_to_remove = matching_tag_regex_tags - matching_tag_list_tags
        num_of_matching_tags = len(matching_tag_list_tags)

        if tags_to_remove:
            failed_checks.append(
                tag_regex_mismatch_error_msg.format(
                    kind_capitalized=kind.capitalize(),
                    kind=kind,
                    name=name,
                    tag_regex=tag_group_config.tag_regex,
                    group_name=tag_group_config.group_name,
                    tag_list=tag_group_config.tag_list,
                    tags_to_remove=sorted(tags_to_remove),
                )
            )

        if (
            num_of_matching_tags < tag_group_config.min_num_of_tags
            or num_of_matching_tags > tag_group_config.max_num_of_tags
        ):
            failed_checks.append(
                num_of_tags_mismatch_error_msg.format(
                    kind_capitalized=kind.capitalize(),
                    kind=kind,
                    name=name,
                    min_num_of_tags=tag_group_config.min_num_of_tags,
                    max_num_of_tags=tag_group_config.max_num_of_tags,
                    group_name=tag_group_config.group_name,
                    tag_list=tag_group_config.tag_list,
                    matching_tags=sorted(matching_tag_list_tags),
                )
            )

    return failed_checks
