import logging
import re
from enum import Enum

from ._constants import UNVERSIONED_DISPLAY_LABEL
from ._types import VersionKey, VersionMap

logger = logging.getLogger(__name__)

_UNVERSIONED_ALIASES: frozenset[str] = frozenset({"null", "unv", "none", "unversioned"})


def normalize_version(version: VersionKey) -> str:
    """Normalize version-like values to lowercase canonical routing keys.

    - ``Enum`` members are unwrapped via ``.value`` before normalization.
    - ``None``, empty strings, whitespace-only strings, and the aliases
      ``"null"``, ``"unv"``, ``"none"``, ``"unversioned"`` (case-insensitive)
      all normalize to ``"unv"``.
    - All other values are stripped, then lowercased via ``str(version).lower()``,
      including bare integers (e.g. ``3`` → ``"3"``).
    """
    if isinstance(version, Enum):
        version = version.value
    stringified = str(version).strip() if version is not None else ""
    if version is None or not stringified or stringified.lower() in _UNVERSIONED_ALIASES:
        return "unv"
    return stringified.lower()


def normalize_prefix(prefix: str) -> str:
    """Return an API prefix guaranteed to start with ``/``.

    Raises ``ValueError`` for empty strings — use ``"/"`` explicitly
    if you intend to match all paths.
    """
    if not prefix:
        raise ValueError("prefix must not be empty; pass '/' explicitly to match all paths")
    normalized = prefix if prefix.startswith("/") else f"/{prefix}"
    if normalized != "/":
        normalized = normalized.rstrip("/")
    return normalized


def normalize_unversioned_label(version: VersionKey) -> str:
    """Map unversioned-like keys to a stable display label."""
    normalized = normalize_version(version)
    if normalized == "unv":
        return UNVERSIONED_DISPLAY_LABEL
    return normalized


def validate_version_mapping_keys(version_mapping: VersionMap) -> None:
    """Ensure version keys do not collide after normalization."""
    seen: dict[str, str] = {}
    for key in version_mapping:
        normalized = normalize_version(key)
        if normalized in seen:
            existing_key = seen[normalized]
            raise ValueError(
                "Duplicate version keys after normalization: "
                f"{existing_key!r} and {key!r} both normalize to '{normalized}'."
            )
        seen[normalized] = str(key)


def _latest_mapped_version(version_values: list[str]) -> str:
    """Pick the latest mapped version deterministically.

    Comparison uses only numeric segments (e.g. ``"v2"`` → ``(2,)``).
    Non-numeric characters between digits are ignored, so versions
    like ``"v1a2"`` and ``"v1b1"`` are compared as ``(1, 2)`` vs ``(1, 1)``.
    """
    candidates = [v for v in version_values if v != "unv"]
    if not candidates:
        return "unv"

    numeric_candidates = [v for v in candidates if re.search(r"\d", v)]
    if numeric_candidates:
        return max(
            numeric_candidates,
            key=lambda value: (tuple(int(x) for x in re.findall(r"\d+", value)), value),
        )

    return sorted(candidates)[-1]


def _default_mapped_version(
    *, version_values: set[str], default_version: VersionKey | None
) -> str | None:
    """Return a normalized default version only when it exists in the mapping."""
    if default_version is None:
        return None

    normalized_default = normalize_version(default_version)
    if normalized_default in version_values:
        return normalized_default

    return None


def _resolve_missing_requested_version(
    *,
    version_values: set[str],
    mapped_default: str | None,
) -> str:
    """Resolve version when the request does not include a version header."""
    if "unv" in version_values:
        return "unv"

    if mapped_default is not None:
        return mapped_default

    return _latest_mapped_version(list(version_values))


def _resolve_unknown_requested_version(
    *,
    version_values: set[str],
    mapped_default: str | None,
) -> str:
    """Resolve version when the request header is present but not mapped."""
    if mapped_default is not None:
        return mapped_default

    if "unv" in version_values:
        return "unv"

    return _latest_mapped_version(list(version_values))


def resolve_version(
    *,
    requested_version: str | None,
    version_mapping: VersionMap | None = None,
    default_version: VersionKey | None = None,
    strict: bool = False,
) -> str:
    """Resolve request version using explicit, deterministic fallback precedence.

    Fallback order when the requested version is not in *version_mapping*:

    1. *default_version* (if provided and present in the mapping)
    2. ``"unv"`` (if present in the mapping)
    3. Latest numeric version

    When *strict* is ``True``, an unrecognised requested version raises
    ``ValueError`` instead of falling back.  Missing headers (``None``)
    still fall back normally — strict mode only rejects explicit but
    unknown version values.

    .. important::

    Raises ``ValueError`` if *version_mapping* keys collide after
    normalization (e.g. ``None`` and ``"unversioned"`` both normalize
    to ``"unv"``).
    """
    if version_mapping is None:
        if requested_version is None:
            return "unv"
        return normalize_version(requested_version)

    version_values = {normalize_version(key) for key in version_mapping}
    if len(version_values) < len(version_mapping):
        validate_version_mapping_keys(version_mapping)
    mapped_default = _default_mapped_version(
        version_values=version_values,
        default_version=default_version,
    )
    requested_normalized = (
        normalize_version(requested_version) if requested_version is not None else None
    )

    if requested_normalized in version_values:
        return requested_normalized

    if requested_normalized is None:
        return _resolve_missing_requested_version(
            version_values=version_values,
            mapped_default=mapped_default,
        )

    if strict:
        raise ValueError(
            f"Requested API version {requested_normalized!r} is not available. "
            f"Available versions: {', '.join(sorted(version_values))}"
        )

    resolved = _resolve_unknown_requested_version(
        version_values=version_values,
        mapped_default=mapped_default,
    )
    logger.warning(
        "Requested API version %r is not mapped (available: %s); falling back to %r",
        requested_normalized,
        ", ".join(sorted(version_values)),
        resolved,
    )
    return resolved


def map_version_path(path: str, *, version: str, prefix: str) -> str:
    """Rewrite an incoming path to include resolved version under the API prefix.

    The prefix precondition is also enforced upstream by the dispatch guard
    ``_should_dispatch_request``, but the check here is intentional
    defense-in-depth — do not remove it.
    """
    if prefix == "/":
        if not path.startswith("/"):
            raise ValueError(f"path {path!r} does not start with prefix {prefix!r}")
    elif not (path == prefix or path.startswith(f"{prefix}/")):
        raise ValueError(f"path {path!r} does not start with prefix {prefix!r}")
    normalized_version = normalize_version(version)
    remainder = path[len(prefix) :]
    if remainder and not remainder.startswith("/"):
        remainder = f"/{remainder}"

    # If the incoming path is already version-qualified, keep it as-is.
    version_segment = f"/{normalized_version}"
    if remainder == version_segment or remainder.startswith(f"{version_segment}/"):
        return path

    # Normalize bare trailing slash so /api/ behaves identically to /api.
    if remainder == "/":
        remainder = ""
    return f"{prefix.rstrip('/')}/{normalized_version}{remainder}"


def resolve_prefix(prefix: str | None) -> str:
    """Return normalized API prefix, defaulting to `/api`."""
    if prefix is None:
        prefix = "/api"

    return normalize_prefix(prefix)


__all__ = (
    "map_version_path",
    "normalize_prefix",
    "normalize_unversioned_label",
    "normalize_version",
    "resolve_prefix",
    "resolve_version",
    "validate_version_mapping_keys",
)
