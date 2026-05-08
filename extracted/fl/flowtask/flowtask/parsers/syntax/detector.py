"""Format detection for Flowtask task definitions.

Two entry points:

- ``detect_format(path)``: by filename suffix.
- ``sniff_format(content)``: by attempting to parse the string in order.
"""
from pathlib import Path
from typing import Literal

import orjson
import yaml

try:
    import tomllib  # Python 3.11+
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]


Format = Literal["json", "yaml", "toml"]

_SUFFIX_MAP: dict[str, Format] = {
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
}


def detect_format(path: Path) -> Format:
    """Return the format implied by the file's suffix.

    Args:
        path: Filesystem path. Suffix lookup is case-insensitive.

    Returns:
        ``"json"``, ``"yaml"``, or ``"toml"``.

    Raises:
        ValueError: when the suffix is not one of the four supported ones.
    """
    suffix = Path(path).suffix.lower()
    try:
        return _SUFFIX_MAP[suffix]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported task file suffix {suffix!r}; "
            f"expected one of {sorted(_SUFFIX_MAP)}."
        ) from exc


def sniff_format(content: str) -> Format:
    """Best-effort format detection from raw content.

    Tries JSON, then YAML, then TOML. The first successful parse wins.

    Note:
        JSON is tried first because every valid JSON document is also valid
        YAML. This ensures the correct classification for ambiguous content.

    Args:
        content: Raw string content of a task definition.

    Returns:
        ``"json"``, ``"yaml"``, or ``"toml"``.

    Raises:
        ValueError: when the content does not parse as any supported format.
    """
    try:
        orjson.loads(content)
        return "json"
    except orjson.JSONDecodeError:
        pass
    try:
        result = yaml.safe_load(content)
        # Only classify as YAML when the result is a mapping (task definitions
        # are always objects). Scalars, lists, and None indicate YAML parsed
        # something that isn't a task, so fall through to TOML.
        if isinstance(result, dict):
            return "yaml"
    except yaml.YAMLError:
        pass
    try:
        tomllib.loads(content)
        return "toml"
    except Exception:  # tomllib.TOMLDecodeError or tomli.TOMLKitError
        pass
    raise ValueError("Content does not parse as JSON, YAML, or TOML.")
