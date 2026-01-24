from pathlib import Path
from urllib.parse import urlparse
import os
VIDEO_VARIABLE_KEYMAP = {
    "info": {
        "keys": ["info", "video_info", "video"],
        "type": dict,
    },
    "video_id": {
        "keys": ["id", "video_id"],
        "type": str,
    },
    "video_url": {
        "keys": ["url", "video_url"],
        "type": str,
    },
    "video_path": {
        "keys": ["path", "video_path"],
        "type": str,
    },
}
def _build_reverse_keymap(keymap):
    reverse = {}
    for canonical_key, cfg in keymap.items():
        for alias in cfg["keys"]:
            reverse[alias] = canonical_key
    return reverse



VIDEO_KEYS = ("video_url", "video_id", "video_path", "info")


def _is_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
        return bool(parsed.scheme and parsed.netloc)
    except Exception:
        return False


def _is_path(value: str) -> bool:
    return (
        os.path.exists(value)
        or value.startswith(("/", "./", "../", "~"))
    )


def infer_video_arg(arg):
    """
    Infer (key, value) from a single positional argument.
    """

    if isinstance(arg, dict):
        return "info", arg

    if isinstance(arg, Path):
        return "video_path", str(arg)

    if isinstance(arg, str):
        if _is_path(arg):
            return "video_path", os.path.expanduser(arg)

        if _is_url(arg):
            return "video_url", arg

        return "video_id", arg

    raise TypeError(f"Unsupported argument type: {type(arg).__name__}")
REVERSE_VIDEO_KEYMAP = _build_reverse_keymap(VIDEO_VARIABLE_KEYMAP)
def normalize_video_inputs(*args, **kwargs):
    """
    Normalizes positional args and keyword args into canonical video inputs.
    """

    normalized = {key: None for key in VIDEO_VARIABLE_KEYMAP}

    # 1️⃣ Positional args inference
    for arg in args:
        key, value = infer_video_arg(arg)
        normalized[key] = value

    # 2️⃣ Keyword args override inference
    for incoming_key, value in kwargs.items():
        canonical_key = REVERSE_VIDEO_KEYMAP.get(incoming_key)
        if not canonical_key:
            continue

        expected_type = VIDEO_VARIABLE_KEYMAP[canonical_key]["type"]
        if value is not None and not isinstance(value, expected_type):
            raise TypeError(
                f"{canonical_key} must be {expected_type.__name__}, "
                f"got {type(value).__name__}"
            )

        # --- semantic validation for string values ---
        if isinstance(value, str):

            if canonical_key == "video_url" and not _is_url(value):
                # Demote to video_id
                normalized["video_id"] = value
                continue

            if canonical_key == "video_path" and not _is_path(value):
                # Demote to video_id
                normalized["video_id"] = value
                continue

        normalized[canonical_key] = value

    return normalized

def get_video_url_path_from_args(*args, **kwargs):
    data = normalize_video_inputs(*args, **kwargs)

    return (
        data["video_url"],
        data["video_id"],
        data["video_path"],
        data["info"],
    )
