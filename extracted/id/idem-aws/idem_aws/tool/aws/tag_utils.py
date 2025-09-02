import copy
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple


def convert_tag_list_to_dict(hub, tags: List):
    result = {}
    for tag in tags:
        if "Key" in tag:
            result[tag["Key"]] = tag.get("Value")
        else:
            hub.log.warning(
                f"tag {tag} is not in the proper format of 'Key', 'Value' pair"
            )
    return result


def convert_tag_list_to_dict_tagkey(hub, tags: List):
    result = {}
    for tag in tags:
        if "TagKey" in tag:
            result[tag["TagKey"]] = tag.get("TagValue")
        else:
            hub.log.warning(
                f"tag {tag} is not in the proper format of 'TagKey', 'TagValue' pair"
            )
    return result


def convert_tag_dict_to_list(hub, tags: Dict) -> List:
    if tags is None:
        tags = {}
    return [{"Key": key, "Value": value} for key, value in tags.items()]


def convert_tag_dict_to_list_tagkey(hub, tags: Dict) -> List:
    if tags is None:
        tags = {}
    return [{"TagKey": key, "TagValue": value} for key, value in tags.items()]


def diff_tags_list(hub, old_tags: List, new_tags: List) -> Tuple:
    """

    Args:
        hub:
        old_tags:
        new_tags:

    Returns:

    """
    if old_tags is None:
        old_tags = []
    if new_tags is None:
        new_tags = []
    old_tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(old_tags)
    new_tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(new_tags)
    tags_to_remove, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
        old_tags, new_tags
    )
    return [{"Key": key, "Value": value} for key, value in tags_to_remove.items()], [
        {"Key": key, "Value": value} for key, value in tags_to_add.items()
    ]


def diff_tags_dict(hub, old_tags: Dict[str, Any], new_tags: Dict[str, Any]) -> Tuple:
    """

    Args:
        hub:
        old_tags:
        new_tags:

    Returns:

    """
    tags_to_add = {}
    tags_to_remove = {}
    new_tags = copy.deepcopy(new_tags)
    if old_tags is None:
        old_tags = {}
    if new_tags is None:
        new_tags = {}
    for key, value in old_tags.items():
        if key in new_tags:
            if old_tags[key] != new_tags[key]:
                tags_to_remove.update({key: old_tags[key]})
                tags_to_add.update({key: new_tags[key]})
            new_tags.pop(key)
        else:
            tags_to_remove.update({key: old_tags[key]})
    tags_to_add.update(new_tags)
    return tags_to_remove, tags_to_add


def convert_auto_scaling_tag_list_to_dict(hub, tags: List):
    result = {}
    for tag in tags:
        if "key" in tag:
            result[tag["key"]] = tag["value"]
        if "propagate_at_launch" in tag:
            result[f"propagate_at_launch-{tag['key']}"] = tag["propagate_at_launch"]
    return result


def convert_auto_scaling_tag_dict_to_list(hub, tags: Dict):
    result = []
    if tags is None:
        tags = {}
    for key, value in tags.items():
        if "propagate_at_launch" == key.split("-", 1)[0] and isinstance(value, bool):
            continue
        temp_tag = {"key": key, "value": value}
        if f"propagate_at_launch-{key}" in tags:
            temp_tag["propagate_at_launch"] = tags.get(f"propagate_at_launch-{key}")
        result.append(temp_tag)
    return result


def diff_auto_scaling_dict_tags(
    hub, old_tags: Dict[str, Any], new_tags: Dict[str, Any]
):
    tags_to_add = {}
    tags_to_remove = {}
    new_tags = copy.deepcopy(new_tags)
    if old_tags is None:
        old_tags = {}
    if new_tags is None:
        new_tags = {}
    for key, value in old_tags.items():
        if "propagate_at_launch" == key.split("-", 1)[0] and isinstance(value, bool):
            continue
        if key in new_tags:
            if old_tags[key] != new_tags[key]:
                tags_to_remove.update({key: old_tags[key]})
                tags_to_add.update({key: new_tags[key]})
                if f"propagate_at_launch-{key}" in old_tags:
                    tags_to_remove.update(
                        {
                            f"propagate_at_launch-{key}": old_tags[
                                f"propagate_at_launch-{key}"
                            ]
                        }
                    )
                if f"propagate_at_launch-{key}" in new_tags:
                    tags_to_add.update(
                        {
                            f"propagate_at_launch-{key}": new_tags[
                                f"propagate_at_launch-{key}"
                            ]
                        }
                    )
            elif (
                old_tags[f"propagate_at_launch-{key}"]
                != new_tags[f"propagate_at_launch-{key}"]
            ):
                tags_to_remove.update(
                    {
                        key: old_tags[key],
                        f"propagate_at_launch-{key}": old_tags[
                            f"propagate_at_launch-{key}"
                        ],
                    }
                )
                tags_to_add.update(
                    {
                        key: new_tags[key],
                        f"propagate_at_launch-{key}": new_tags[
                            f"propagate_at_launch-{key}"
                        ],
                    }
                )
            new_tags.pop(key)
            new_tags.pop(f"propagate_at_launch-{key}")
        else:
            tags_to_remove.update({key: old_tags[key]})
            if f"propagate_at_launch-{key}" in old_tags:
                tags_to_remove.update(
                    {
                        f"propagate_at_launch-{key}": old_tags[
                            f"propagate_at_launch-{key}"
                        ]
                    }
                )
    tags_to_add.update(new_tags)
    return tags_to_remove, tags_to_add
