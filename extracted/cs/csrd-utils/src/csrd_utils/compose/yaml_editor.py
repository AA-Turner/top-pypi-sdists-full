"""Round-trip YAML helpers powered by ruamel.yaml.

Provides comment-preserving load / save / merge primitives so that
hand-edited ``csrd-compose.yaml`` files keep their comments intact
when the CLI appends services or infra nodes.

All public functions operate on ``ruamel.yaml`` ``CommentedMap`` /
``CommentedSeq`` objects — callers never need to import ``ruamel`` directly.
"""

import io
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

# Shared round-trip YAML instance — reuse to amortise setup cost.
_yaml = YAML()
_yaml.preserve_quotes = True  # keep user quote style
_yaml.width = 120  # avoid aggressive line wrapping
_yaml.default_flow_style = False


# ---------------------------------------------------------------------------
# Load / save
# ---------------------------------------------------------------------------


def load_yaml(path: Path) -> dict[str, Any]:
    """Round-trip load a YAML file, returning the commented mapping.

    Returns an empty ``CommentedMap`` when the file is empty or contains
    only whitespace / comments.
    """

    from ruamel.yaml.comments import CommentedMap

    data = _yaml.load(path.read_text(encoding="utf-8"))
    if data is None:
        return CommentedMap()
    if not isinstance(data, dict):
        raise ValueError("Compose spec must be a YAML object")
    return data  # type: ignore[return-value]


def save_yaml(data: dict[str, Any], path: Path) -> None:
    """Write *data* back to *path*, preserving comments and formatting."""

    path.parent.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    _yaml.dump(data, buf)
    path.write_text(buf.getvalue(), encoding="utf-8")


def dumps_yaml(data: dict[str, Any]) -> str:
    """Serialize *data* to a YAML string (round-trip safe)."""

    buf = io.StringIO()
    _yaml.dump(data, buf)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Merge helpers
# ---------------------------------------------------------------------------


def set_key(mapping: dict[str, Any], key: str, value: Any) -> None:
    """Set *key* in a round-trip mapping, preserving surrounding comments."""

    mapping[key] = value


def ensure_list_item(
    mapping: dict[str, Any],
    list_key: str,
    item: dict[str, Any],
    *,
    match_field: str = "name",
) -> bool:
    """Append *item* to ``mapping[list_key]`` if no entry matches *match_field*.

    Creates the list if it doesn't exist. Returns ``True`` when a new item was
    appended, ``False`` when a duplicate was found.
    """

    from ruamel.yaml.comments import CommentedSeq

    if list_key not in mapping:
        mapping[list_key] = CommentedSeq()

    seq = mapping[list_key]
    match_value = item.get(match_field)
    if match_value is not None:
        for existing in seq:
            if isinstance(existing, dict) and existing.get(match_field) == match_value:
                return False

    seq.append(item)
    return True


def deep_merge(
    base: dict[str, Any],
    overlay: dict[str, Any],
    *,
    merge_lists: bool = False,
) -> dict[str, Any]:
    """Recursively merge *overlay* into *base* (in-place), returning *base*.

    Scalar values in *overlay* overwrite *base*. Nested dicts are merged
    recursively. Lists are replaced by default; set ``merge_lists=True``
    to extend instead.
    """

    for key, overlay_value in overlay.items():
        if key in base and isinstance(base[key], dict) and isinstance(overlay_value, dict):
            deep_merge(base[key], overlay_value, merge_lists=merge_lists)
        elif (
            merge_lists
            and key in base
            and isinstance(base[key], list)
            and isinstance(overlay_value, list)
        ):
            for v in overlay_value:
                if v not in base[key]:
                    base[key].append(v)
        else:
            base[key] = overlay_value

    return base
