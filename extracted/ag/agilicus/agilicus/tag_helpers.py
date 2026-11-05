"""Common tag extraction, conversion, and mutation helpers."""

import agilicus


def extract_tags_list(tags_obj):
    if tags_obj is None:
        return []
    if isinstance(tags_obj, agilicus.Tags):
        return [t for t in (tags_obj.value or []) if t]
    if isinstance(tags_obj, (list, tuple, set)):
        return [t for t in tags_obj if t]
    return [tags_obj] if tags_obj else []


def to_tags_model(tags_list):
    if tags_list is None:
        return None
    if isinstance(tags_list, agilicus.Tags):
        return tags_list
    items = extract_tags_list(tags_list)
    return agilicus.Tags(items)


def apply_tag_updates(
    existing_tags,
    tags=None,
    add_tags=None,
    remove_tags=None,
    clear_tags=False,
):
    if clear_tags:
        current = []
    elif tags is not None and len(tags) > 0:
        current = [t for t in tags if t]
    else:
        current = extract_tags_list(existing_tags)

    if remove_tags:
        remove_set = set(remove_tags)
        current = [t for t in current if t not in remove_set]

    if add_tags:
        for t in add_tags:
            if t and t not in current:
                current.append(t)

    return current
