"""
Repo-specific configuration loader for agentic-devtools.

Reads and validates `.github/agdt-config.json` from a target repository root,
exposing structured access to review focus areas and other repo-specific metadata.

Both the config file and any referenced files are optional — if missing, functions
return safe defaults so the review workflow proceeds without repo-specific context.
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

CONFIG_FILE = ".github/agdt-config.json"

# Platform configuration constants
VALID_ISSUE_ADAPTERS: frozenset[str] = frozenset({"jira", "github", "markdown"})
VALID_CODE_HOSTING: frozenset[str] = frozenset({"github", "azure_devops", "other"})
DEFAULT_ISSUE_ADAPTER: str = "jira"
DEFAULT_CODE_HOSTING: str = "other"

# Phase 0 configuration defaults
PHASE_0_DEFAULT_ENABLED: bool = False
PHASE_0_DEFAULT_SYNC_BACK_ON_MERGE: bool = False
PHASE_0_DEFAULT_SYNC_BACK_FIELDS: tuple[str, ...] = ("comment",)

# Valid sync-back field identifiers (canonical order for error messages).
VALID_SYNC_BACK_FIELDS: tuple[str, ...] = ("comment", "label", "status")
_VALID_SYNC_BACK_FIELDS_SET: frozenset[str] = frozenset(VALID_SYNC_BACK_FIELDS)


def load_repo_config(repo_path: str) -> dict:
    """
    Load and return the parsed contents of `.github/agdt-config.json`.

    The config file is optional.  If it is absent, an empty dict is returned
    and no error is raised.  If the file exists but contains invalid JSON a
    warning is logged and an empty dict is returned.

    Args:
        repo_path: Absolute (or relative) path to the root of the target repo.

    Returns:
        Parsed config dict, or ``{}`` when the file is missing or unreadable.
    """
    config_path = Path(repo_path) / CONFIG_FILE
    if not config_path.exists():
        return {}

    try:
        content = config_path.read_text(encoding="utf-8")
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            logger.warning(
                "Expected a JSON object in %s, got %s; ignoring.",
                config_path,
                type(parsed).__name__,
            )
            return {}
        return parsed
    except json.JSONDecodeError as exc:
        logger.warning("Invalid JSON in %s: %s", config_path, exc)
        return {}
    except OSError as exc:
        logger.warning("Could not read %s: %s", config_path, exc)
        return {}


def load_review_focus_areas(repo_path: str) -> str | None:
    """
    Load the review focus areas markdown content referenced in the repo config.

    Reads ``review.focus-areas-file`` from `.github/agdt-config.json`, then
    returns the raw markdown text of that file.  All files are optional — if
    either the config or the referenced markdown file is missing the function
    returns ``None`` without raising.

    Args:
        repo_path: Absolute (or relative) path to the root of the target repo.

    Returns:
        Raw markdown string, or ``None`` when no focus areas are configured.
    """
    config = load_repo_config(repo_path)

    review_section = config.get("review")
    if review_section is None:
        return None
    if not isinstance(review_section, dict):
        logger.warning(
            "Expected 'review' section in %s to be an object, got %s; ignoring.",
            CONFIG_FILE,
            type(review_section).__name__,
        )
        return None

    focus_areas_file = review_section.get("focus-areas-file")
    if not focus_areas_file:
        return None
    if not isinstance(focus_areas_file, str):
        logger.warning(
            "Expected 'review.focus-areas-file' in %s to be a string, got %s; ignoring.",
            CONFIG_FILE,
            type(focus_areas_file).__name__,
        )
        return None

    repo_root = Path(repo_path).resolve()
    focus_path = (repo_root / focus_areas_file).resolve()

    # Reject paths that escape the repository root (path traversal guard).
    try:
        focus_path.relative_to(repo_root)
    except ValueError:
        logger.warning(
            "Configured focus-areas-file path %s escapes repository root %s; ignoring.",
            focus_path,
            repo_root,
        )
        return None

    if not focus_path.exists():
        logger.warning("focus-areas-file not found: %s", focus_path)
        return None

    try:
        return focus_path.read_text(encoding="utf-8")
    except OSError as exc:
        logger.warning("Could not read focus-areas-file %s: %s", focus_path, exc)
        return None


def _validate_phase_0(raw: object) -> dict:
    """Validate and normalize the ``phase_0`` sub-section.

    Returns a dict with at least ``enabled``, ``sync_back_on_merge``, and
    ``sync_back_fields`` keys, using safe defaults for any that are missing
    or invalid.  Unknown keys are preserved for forward-compatibility.

    When both ``enabled`` and ``sync_back_on_merge`` are ``True``, unknown
    field names in ``sync_back_fields`` cause a ``ValueError`` listing all
    unrecognized entries and the valid options.  When either gate is ``False``,
    unknown fields are silently accepted (the config is inactive).

    Deduplication is applied silently (order-preserving) before validation.
    Explicit ``None`` or an absent ``sync_back_fields`` key defaults to
    ``["comment"]`` without any warning.

    Args:
        raw: The raw value of ``platform.phase_0`` (may be None, a dict, or
             any other type if the user mis-configured the file).

    Returns:
        Validated dict with guaranteed keys and correct types.

    Raises:
        ValueError: When both gates are active and ``sync_back_fields``
            contains entries not in ``VALID_SYNC_BACK_FIELDS``.
    """
    defaults: dict = {
        "enabled": PHASE_0_DEFAULT_ENABLED,
        "sync_back_on_merge": PHASE_0_DEFAULT_SYNC_BACK_ON_MERGE,
        "sync_back_fields": list(PHASE_0_DEFAULT_SYNC_BACK_FIELDS),
    }

    if raw is None:
        return defaults

    if not isinstance(raw, dict):
        logger.warning(
            "Expected 'platform.phase_0' in %s to be an object, got %s; using defaults.",
            CONFIG_FILE,
            type(raw).__name__,
        )
        return defaults

    # Start with unknown keys preserved, then overwrite known keys with validated values.
    result = {**raw}

    # Validate enabled (must be bool).
    enabled = raw.get("enabled", PHASE_0_DEFAULT_ENABLED)
    if not isinstance(enabled, bool):
        logger.warning(
            "Expected 'platform.phase_0.enabled' in %s to be a boolean, got %s; using default.",
            CONFIG_FILE,
            type(enabled).__name__,
        )
        enabled = PHASE_0_DEFAULT_ENABLED
    result["enabled"] = enabled

    # Validate sync_back_on_merge (must be bool).
    sync_back_on_merge = raw.get("sync_back_on_merge", PHASE_0_DEFAULT_SYNC_BACK_ON_MERGE)
    if not isinstance(sync_back_on_merge, bool):
        logger.warning(
            "Expected 'platform.phase_0.sync_back_on_merge' in %s to be a boolean, got %s; using default.",
            CONFIG_FILE,
            type(sync_back_on_merge).__name__,
        )
        sync_back_on_merge = PHASE_0_DEFAULT_SYNC_BACK_ON_MERGE
    result["sync_back_on_merge"] = sync_back_on_merge

    # Validate sync_back_fields (must be list of strings).
    # Treat explicit None the same as absent key — default silently.
    if "sync_back_fields" not in raw or raw["sync_back_fields"] is None:
        sync_back_fields = list(PHASE_0_DEFAULT_SYNC_BACK_FIELDS)
    else:
        sync_back_fields = raw["sync_back_fields"]
        if not isinstance(sync_back_fields, list) or not all(isinstance(f, str) for f in sync_back_fields):
            logger.warning(
                "Expected 'platform.phase_0.sync_back_fields' in %s to be a list of strings, got %s; using default.",
                CONFIG_FILE,
                type(sync_back_fields).__name__,
            )
            sync_back_fields = list(PHASE_0_DEFAULT_SYNC_BACK_FIELDS)
        else:
            # Deduplicate preserving first-occurrence order.
            sync_back_fields = list(dict.fromkeys(sync_back_fields))

    # Reject unknown fields only when both gates are active.
    if enabled is True and sync_back_on_merge is True:
        unknown = [f for f in sync_back_fields if f not in _VALID_SYNC_BACK_FIELDS_SET]
        if unknown:
            quoted = ", ".join(json.dumps(u) for u in unknown)
            valid_list = ", ".join(VALID_SYNC_BACK_FIELDS)
            msg = f"Unknown sync_back_fields: {quoted}. Valid options are: {valid_list}"
            raise ValueError(msg)

    result["sync_back_fields"] = list(sync_back_fields)

    return result


def validate_phase_0_config(phase_0: object) -> dict[str, object]:
    """Public wrapper around ``_validate_phase_0`` for external consumers.

    Accepts a ``phase_0`` dict (or any object) and returns a validated/normalized
    dict with guaranteed ``enabled``, ``sync_back_on_merge``, and ``sync_back_fields``
    keys.

    Args:
        phase_0: The raw ``phase_0`` value to validate.

    Returns:
        Validated dict with guaranteed keys and correct types.

    Raises:
        ValueError: When both gates are active and ``sync_back_fields``
            contains entries not in ``VALID_SYNC_BACK_FIELDS``.
    """
    return _validate_phase_0(phase_0)


def load_platform_config(repo_path: str) -> dict:
    """
    Load the ``platform`` section from `.github/agdt-config.json`.

    Returns a dict with all platform keys guaranteed present, using safe
    defaults for any that are missing or invalid.  Unknown keys in the
    ``platform`` section are silently preserved for forward-compatibility.

    Args:
        repo_path: Absolute (or relative) path to the root of the target repo.

    Returns:
        Dict with at least ``issue_adapter``, ``code_hosting``, ``jira``,
        ``github``, ``azure_devops``, and ``phase_0`` keys.
    """
    config = load_repo_config(repo_path)
    platform = config.get("platform")

    if platform is None:
        platform = {}
    elif not isinstance(platform, dict):
        logger.warning(
            "Expected 'platform' section in %s to be an object, got %s; using defaults.",
            CONFIG_FILE,
            type(platform).__name__,
        )
        platform = {}

    # Validate issue_adapter enum.
    issue_adapter = platform.get("issue_adapter", DEFAULT_ISSUE_ADAPTER)
    if not isinstance(issue_adapter, str) or issue_adapter not in VALID_ISSUE_ADAPTERS:
        logger.warning(
            "Invalid issue_adapter value %r in %s; using default %r.",
            issue_adapter,
            CONFIG_FILE,
            DEFAULT_ISSUE_ADAPTER,
        )
        issue_adapter = DEFAULT_ISSUE_ADAPTER

    # Validate code_hosting enum.
    code_hosting = platform.get("code_hosting", DEFAULT_CODE_HOSTING)
    if not isinstance(code_hosting, str) or code_hosting not in VALID_CODE_HOSTING:
        logger.warning(
            "Invalid code_hosting value %r in %s; using default %r.",
            code_hosting,
            CONFIG_FILE,
            DEFAULT_CODE_HOSTING,
        )
        code_hosting = DEFAULT_CODE_HOSTING

    # Validate platform-specific sub-dicts (None from JSON null is also replaced).
    for key in ("jira", "github", "azure_devops"):
        value = platform.get(key)
        if not isinstance(value, dict):
            if value is not None:
                logger.warning(
                    "Expected 'platform.%s' in %s to be an object, got %s; using empty dict.",
                    key,
                    CONFIG_FILE,
                    type(value).__name__,
                )
            platform[key] = {}

    result = {**platform}
    result["issue_adapter"] = issue_adapter
    result["code_hosting"] = code_hosting
    result.setdefault("jira", {})
    result.setdefault("github", {})
    result.setdefault("azure_devops", {})
    result["phase_0"] = _validate_phase_0(platform.get("phase_0"))

    return result


def save_platform_config(repo_path: str, platform_config: dict) -> bool:
    """
    Write the ``platform`` section to `.github/agdt-config.json`.

    Reads the existing config (if any), sets ``config["platform"]`` to
    *platform_config*, and writes the merged result back.  The ``.github/``
    directory and the config file are created when they do not exist.

    Args:
        repo_path: Absolute (or relative) path to the root of the target repo.
        platform_config: Dict to store as the ``platform`` section.

    Returns:
        ``True`` on success, ``False`` on failure (with a warning logged).
    """
    if not isinstance(platform_config, dict):
        logger.warning(
            "Expected platform_config to be a dict, got %s; refusing to write invalid platform section.",
            type(platform_config).__name__,
        )
        return False

    config = load_repo_config(repo_path)
    config["platform"] = platform_config

    config_path = Path(repo_path) / CONFIG_FILE
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        return True
    except (OSError, TypeError, ValueError) as exc:
        logger.warning("Could not write %s: %s", config_path, exc)
        return False


# ---------------------------------------------------------------------------
# Review decision policy loader (FR-006)
# ---------------------------------------------------------------------------


def load_review_decision_policy(repo_path: str) -> dict:
    """Load the review decision policy from ``.github/agdt-config.json``.

    Reads ``review.decision-policy`` (preferred) or the alias
    ``review.decision_policy`` (underscore form) and returns the raw dict.
    Missing sections, missing keys, or invalid types all produce safe defaults.

    Args:
        repo_path: Absolute (or relative) path to the target repo root.

    Returns:
        Policy config dict (may be empty if not configured).
    """
    config = load_repo_config(repo_path)

    review = config.get("review")
    if not isinstance(review, dict):
        return {}

    if "decision-policy" in review:
        policy = review["decision-policy"]
    elif "decision_policy" in review:
        policy = review["decision_policy"]
    else:
        policy = None
    if not isinstance(policy, dict):
        return {}

    return policy


# ---------------------------------------------------------------------------
# Review model routing loader (FR-009)
# ---------------------------------------------------------------------------


def load_review_model_config(repo_path: str) -> dict:
    """Load review model routing configuration from ``.github/agdt-config.json``.

    Reads ``review.model-routing`` (preferred) or the aliases
    ``review.models`` / ``review.model_routing`` and returns the raw dict.

    Args:
        repo_path: Absolute (or relative) path to the target repo root.

    Returns:
        Model routing config dict (may be empty if not configured).
    """
    config = load_repo_config(repo_path)

    review = config.get("review")
    if not isinstance(review, dict):
        return {}

    if "model-routing" in review:
        model_routing = review["model-routing"]
    elif "models" in review:
        model_routing = review["models"]
    elif "model_routing" in review:
        model_routing = review["model_routing"]
    else:
        model_routing = None
    if not isinstance(model_routing, dict):
        return {}

    return model_routing
