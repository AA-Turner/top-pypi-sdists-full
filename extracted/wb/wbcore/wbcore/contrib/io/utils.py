import urllib.parse
from collections import defaultdict
from typing import Any


def nest_row(row: dict[str, Any], sep="__") -> dict[str, Any]:
    """
    Utility function to nest row based on seperator.

    Examples:
        Row with key containing "__" such as "key__nested_key" will be converted to a dictionary "{"key": "nested_key"}"
    Args:
        row: The un-nested row
        sep: The seperated to use for nested separation

    Returns:
        A nested dictionary
    """
    res = defaultdict(dict)
    for k, v in row.items():
        splits = k.split(sep, maxsplit=1)
        if len(splits) == 2:
            res[splits[0]][splits[1]] = v
        else:
            res[k] = v
    return dict(res)


def parse_endpoint(request, segment: str, **extra_kwargs) -> str:
    parts = urllib.parse.urlsplit(request.get_full_path())
    new_path = f"{parts.path.rstrip('/')}/{segment}/" if parts.path else f"/{segment}/"
    res = urllib.parse.urlunsplit((parts.scheme, parts.netloc, new_path, parts.query, parts.fragment))
    return res


def get_import_export_identifier(view) -> str:
    try:
        identifier = view.IDENTIFIER
    except AttributeError:
        identifier = "{0.app_label}:{0.model}".format(view.get_content_type())
    return identifier
