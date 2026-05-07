from typing import Collection


def tag_matches(datasource_tag: str, context_tags: Collection[str]) -> bool:
    for t in context_tags:
        if t == datasource_tag:
            return True
        split = t.split(":")
        if len(split) == 2 and split[0] == datasource_tag:
            return True
    return False
