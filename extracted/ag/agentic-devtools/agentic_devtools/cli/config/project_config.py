"""
Project-level configuration stored in ``.agdt/config/project.json``.

This file is per-repo, versionable, and shareable across the team.
It stores project-specific settings such as Jira project keys,
corporate/VPN hostnames, and the Jira base URL.
"""

import json
import sys
from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path
from typing import Any, TypedDict, cast

_CONFIG_DIR = "config"
_CONFIG_FILENAME = "project.json"


# ──────────────────────────────────────────────────────────────────────────────
# TypedDict definitions for issue_types_metadata schema (FR-001 / FR-003)
# ──────────────────────────────────────────────────────────────────────────────


class PropertyEntry(TypedDict):
    """Schema for a single property within an issue type."""

    name: str
    display_name: str
    type: str
    required: bool
    allowed_values: list[str] | None
    included_in_template: bool


class IssueTypeEntry(TypedDict):
    """Schema for a single issue type entry."""

    id: str
    name: str
    description: str
    is_subtask: bool
    properties: list[PropertyEntry]


class ProjectIssueTypesMetadata(TypedDict):
    """Schema for the issue_types_metadata entry of a single project."""

    lastDiscovered: str
    lastRefreshed: str
    provider: str
    issue_types: list[IssueTypeEntry]


def _get_config_path(git_root: Path | None = None) -> Path | None:
    """Return the path to ``.agdt/config/project.json`` or ``None``.

    When *git_root* is given it is used directly; otherwise the root is
    detected from the current working directory.
    """
    if git_root is None:
        # Deferred import to avoid circular dependency
        from agentic_devtools.state import _get_git_repo_root

        git_root = _get_git_repo_root()
    if git_root is None:
        return None
    return git_root / ".agdt" / _CONFIG_DIR / _CONFIG_FILENAME


def load_project_config(*, git_root: Path | None = None) -> dict[str, Any]:
    """Read ``.agdt/config/project.json`` and return its contents.

    When *git_root* is given, the config is read from that repo root
    instead of detecting the root from the current working directory.

    Returns ``{}`` when the file does not exist, the current directory is
    not inside a git repository, or the JSON is malformed.
    """
    config_path = _get_config_path(git_root)
    if config_path is None or not config_path.exists():
        return {}
    try:
        parsed = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print(
            f"Warning: Malformed JSON in {config_path}. Using empty config.",
            file=sys.stderr,
        )
        return {}
    except (OSError, UnicodeDecodeError):
        print(
            f"Warning: Cannot read {config_path}. Using empty config.",
            file=sys.stderr,
        )
        return {}
    if not isinstance(parsed, dict):
        print(
            f"Warning: Expected JSON object in {config_path}, got {type(parsed).__name__}. Using empty config.",
            file=sys.stderr,
        )
        return {}
    return migrate_legacy_model_inventory(parsed, emit_warnings=False)


def save_project_config(config: dict[str, Any], *, git_root: Path | None = None) -> Path:
    """Write *config* to ``.agdt/config/project.json``, creating directories as needed.

    When *git_root* is given, the config is written under that repo root
    instead of detecting the root from the current working directory.

    Returns the path that was written.

    Raises ``RuntimeError`` if the git repository root cannot be determined.
    Raises ``ValueError`` if any entry in ``issue_types_metadata`` is invalid.
    """
    config = migrate_legacy_model_inventory(config)
    if "issue_types_metadata" in config:
        metadata = config["issue_types_metadata"]
        if not isinstance(metadata, dict):
            raise ValueError(f"issue_types_metadata must be a dict, got {type(metadata).__name__}")
        for project_key, entry in metadata.items():
            try:
                validate_issue_types_metadata(entry)
            except ValueError as exc:
                raise ValueError(f"issue_types_metadata[{project_key!r}]: {exc}") from exc
    config_path = _get_config_path(git_root)
    if config_path is None:
        raise RuntimeError("Cannot determine git repository root. Run from inside a git repo.")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return config_path


def get_project_config_value(key: str) -> str | None:
    """Return a single value from the project config, or ``None``."""
    value = load_project_config().get(key)
    if value is None:
        return None
    return str(value)


def get_available_models() -> list[str]:
    """Return the cached top-level ``availableModels`` inventory.

    This is the environment capability list populated by ``agdt-setup``.
    Setup refreshes the inventory on every run by default; ``--no-refresh-models``
    skips the live query and reuses the cached inventory. Returns ``[]`` when
    the key is absent or not a list; non-string entries are filtered out.
    """
    value = load_project_config().get("availableModels")
    if not isinstance(value, list):
        return []
    models: list[str] = []
    for model in value:
        if isinstance(model, str):
            normalized = model.strip()
            if normalized:
                models.append(normalized)
    return models


MODEL_COST_FRESHNESS_DAYS = 90
MODEL_SURFACE_KEYS = frozenset({"copilot", "vscode", "docs"})
_SURFACE_IDENTITY_FIELD: dict[str, str] = {"copilot": "modelId", "vscode": "displayName", "docs": "displayName"}
DEFAULT_MODEL_ALLOWLIST = (
    "auto",
    "claude-sonnet-5",
    "claude-opus-5",
    "claude-opus-4.8",
    "claude-opus-4.8-fast",
    "claude-opus-4.7",
    "claude-sonnet-4.6",
    "claude-opus-4.6",
    "claude-sonnet-4.5",
    "claude-opus-4.5",
    "claude-haiku-4.5",
    "gpt-5.6-sol",
    "gpt-5.6-terra",
    "gpt-5.6-luna",
    "gpt-5.5",
    "gpt-5.4",
    "gpt-5.4-mini",
    "gpt-5.3-codex",
    "gpt-5-mini",
    "mai-code-1-flash-picker",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.1-pro-preview",
    "grok-4.5",
    "kimi-k3",
    "kimi-k2.7-code",
    "grok-4.6",
    "mai-code-1.1-flash",
)
KNOWN_NON_PRICEABLE_MODELS = frozenset({"auto"})

MODEL_SURFACE_DISPLAY_NAMES = {
    "auto": "Auto",
    "claude-sonnet-5": "Claude Sonnet 5",
    "claude-opus-5": "Claude Opus 5",
    "claude-haiku-4.5": "Claude Haiku 4.5",
    "claude-opus-4.5": "Claude Opus 4.5",
    "claude-opus-4.6": "Claude Opus 4.6",
    "claude-opus-4.7": "Claude Opus 4.7",
    "claude-opus-4.8": "Claude Opus 4.8",
    "claude-opus-4.8-fast": "Claude Opus 4.8 Fast",
    "claude-sonnet-4.5": "Claude Sonnet 4.5",
    "claude-sonnet-4.6": "Claude Sonnet 4.6",
    "gpt-5.5": "GPT-5.5",
    "gpt-5.6-sol": "GPT-5.6 Sol",
    "gpt-5.6-terra": "GPT-5.6 Terra",
    "gpt-5.6-luna": "GPT-5.6 Luna",
    "gpt-5.4": "GPT-5.4",
    "gpt-5.4-mini": "GPT-5.4 mini",
    "gpt-5.3-codex": "GPT-5.3 Codex",
    "gpt-5-mini": "GPT-5 mini",
    "mai-code-1-flash-picker": "MAI Code 1 Flash Picker",
    "gemini-3.7-flash": "Gemini 3.7 Flash",
    "gemini-3.6-flash": "Gemini 3.6 Flash",
    "gemini-3.1-pro-preview": "Gemini 3.1 Pro Preview",
    "gemini-3-flash-preview": "Gemini 3 Flash Preview",
    "gemini-3.5-flash": "Gemini 3.5 Flash",
    "gemini-2.5-pro": "Gemini 2.5 Pro",
    "grok-4.5": "Grok 4.5",
    "kimi-k3": "Kimi K3",
    "kimi-k2.7-code": "Kimi K2.7 Code",
    "grok-4.6": "Grok 4.6",
    "mai-code-1.1-flash": "MAI Code 1.1 Flash",
}

DEFAULT_COST_DATA_AS_OF = "2026-08-22T00:00:00+00:00"

MODEL_CATALOG = {
    "claude-haiku-4.5": {
        "inputRatePerM": 0.8,
        "outputRatePerM": 4.0,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
    "claude-opus-4.5": {
        "inputRatePerM": 15.0,
        "outputRatePerM": 75.0,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
    "claude-opus-4.6": {
        "inputRatePerM": 15.0,
        "outputRatePerM": 75.0,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
    "claude-opus-4.7": {
        "inputRatePerM": 15.0,
        "outputRatePerM": 75.0,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
    "claude-opus-4.8": {
        "inputRatePerM": 15.0,
        "outputRatePerM": 75.0,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
    "claude-sonnet-4.5": {
        "inputRatePerM": 3.0,
        "outputRatePerM": 15.0,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
    "claude-sonnet-4.6": {
        "inputRatePerM": 3.0,
        "outputRatePerM": 15.0,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
    "gpt-5.5": {
        "inputRatePerM": 1.25,
        "outputRatePerM": 10.0,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
    "gpt-5.4": {
        "inputRatePerM": 1.25,
        "outputRatePerM": 10.0,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
    "gpt-5.4-mini": {
        "inputRatePerM": 0.15,
        "outputRatePerM": 0.6,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
    "gpt-5.3-codex": {
        "inputRatePerM": 1.25,
        "outputRatePerM": 10.0,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
    "gpt-5-mini": {
        "inputRatePerM": 0.25,
        "outputRatePerM": 2.0,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
    "gemini-3.1-pro-preview": {
        "inputRatePerM": 1.25,
        "outputRatePerM": 5.0,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
    "gemini-3-flash-preview": {
        "inputRatePerM": 0.075,
        "outputRatePerM": 0.3,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
    "gemini-3.5-flash": {
        "inputRatePerM": 0.075,
        "outputRatePerM": 0.3,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
    "gemini-2.5-pro": {
        "inputRatePerM": 1.25,
        "outputRatePerM": 10.0,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 100_000,
        "assumedOutputTokens": 10_000,
        "priceCategory": "standard",
        "provenance": "curated-catalog",
        "costDataAsOf": DEFAULT_COST_DATA_AS_OF,
    },
}

_CATALOG_FIELDS: frozenset[str] = frozenset(next(iter(MODEL_CATALOG.values()))) if MODEL_CATALOG else frozenset()

_MODEL_ENTRY_FIELDS: frozenset[str] = frozenset(
    {
        "modelId",
        "surfaces",
        "pricingStatus",
        "inputRatePerM",
        "outputRatePerM",
        "currency",
        "rateUnit",
        "assumedInputTokens",
        "assumedOutputTokens",
        "modelledSessionCost",
        "priceCategory",
        "unavailableReason",
        "provenance",
        "costDataAsOf",
        "observedAt",
        "sourceMetadata",
    }
)
_PRICEABLE_FIELDS: frozenset[str] = frozenset(
    {
        "inputRatePerM",
        "outputRatePerM",
        "currency",
        "rateUnit",
        "assumedInputTokens",
        "assumedOutputTokens",
        "modelledSessionCost",
        "priceCategory",
        "provenance",
        "costDataAsOf",
    }
)
_PRICE_INPUT_FIELDS = _PRICEABLE_FIELDS - {"modelledSessionCost"}
_COST_REQUIRED_FIELDS = _PRICEABLE_FIELDS
_PRICING_STATUSES = frozenset({"priceable", "unavailable", "non_priceable"})
_UNAVAILABLE_REASONS = frozenset({"missing", "invalid"})
_ACP_PRICING_SOURCES = frozenset({"acp-live", "acp-cache"})
_MONETARY_FIELDS = frozenset(
    {
        "inputRatePerM",
        "outputRatePerM",
        "currency",
        "rateUnit",
        "assumedInputTokens",
        "assumedOutputTokens",
        "modelledSessionCost",
        "costDataAsOf",
    }
)

WARN_COST_DATA_STALE = "WARN_COST_DATA_STALE"
WARN_COST_DATA_MISSING = "WARN_COST_DATA_MISSING"
WARN_COST_DATA_INVALID = "WARN_COST_DATA_INVALID"
WARN_COST_DATA_UNAVAILABLE = "WARN_COST_DATA_UNAVAILABLE"


def _is_tagged_cost_warning(message: str) -> bool:
    """Return whether *message* already carries a recognized cost-warning tag."""
    return message.startswith(
        (
            f"{WARN_COST_DATA_MISSING}:",
            f"{WARN_COST_DATA_INVALID}:",
            f"{WARN_COST_DATA_STALE}:",
            f"{WARN_COST_DATA_UNAVAILABLE}:",
        )
    )


def _coerce_decimal(value: Any, *, field_name: str) -> Decimal:
    """Coerce *value* to ``Decimal`` using a strict, non-NaN conversion."""
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be numeric, not boolean")
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError(f"{field_name} must be finite")
        return value
    if isinstance(value, (int, float, str)):
        try:
            decimal_value = Decimal(str(value))
        except InvalidOperation as exc:  # pragma: no cover - covered by ValueError path
            raise ValueError(f"{field_name} is not a valid numeric value: {value!r}") from exc
        if not decimal_value.is_finite():
            raise ValueError(f"{field_name} must be finite")
        return decimal_value
    raise ValueError(f"{field_name} must be numeric, got {type(value).__name__}")


def calculate_modelled_session_cost(
    input_rate_per_m: Any,
    output_rate_per_m: Any,
    assumed_input_tokens: Any,
    assumed_output_tokens: Any,
) -> str:
    """Return the exact decimal session cost as a JSON-safe string."""
    input_rate = _coerce_decimal(input_rate_per_m, field_name="inputRatePerM")
    if input_rate < 0:
        raise ValueError("inputRatePerM must be non-negative")
    output_rate = _coerce_decimal(output_rate_per_m, field_name="outputRatePerM")
    if output_rate < 0:
        raise ValueError("outputRatePerM must be non-negative")
    input_tokens = _coerce_decimal(assumed_input_tokens, field_name="assumedInputTokens")
    if input_tokens < 0 or input_tokens % 1 != 0:
        raise ValueError("assumedInputTokens must be a non-negative integer")
    output_tokens = _coerce_decimal(assumed_output_tokens, field_name="assumedOutputTokens")
    if output_tokens < 0 or output_tokens % 1 != 0:
        raise ValueError("assumedOutputTokens must be a non-negative integer")

    with localcontext() as decimal_context:
        decimal_context.prec = 28
        total = (input_rate * input_tokens / Decimal("1_000_000")) + (
            output_rate * output_tokens / Decimal("1_000_000")
        )
        normalized = total.normalize()
        return format(normalized, "f")


def _parse_cost_data_timestamp(value: Any) -> datetime:
    """Parse a cost-data timestamp and normalize it to UTC.

    Side-effect-free: raises ``ValueError`` on invalid input without printing.
    Callers that want to emit a warning are responsible for catching the error
    and printing the message themselves.
    """
    if value is None:
        raise ValueError(f"{WARN_COST_DATA_MISSING}: cost metadata is absent")
    if not isinstance(value, str):
        raise ValueError(f"{WARN_COST_DATA_INVALID}: cost metadata must be an ISO-8601 UTC string")

    timestamp = value.strip()
    if not timestamp:
        raise ValueError(f"{WARN_COST_DATA_MISSING}: cost metadata is blank")

    try:
        if timestamp.endswith("Z"):
            timestamp = timestamp[:-1] + "+00:00"
        parsed = datetime.fromisoformat(timestamp)
    except ValueError as exc:
        raise ValueError(f"{WARN_COST_DATA_INVALID}: cost metadata is not valid ISO-8601: {value!r}") from exc

    if parsed.tzinfo is None:
        raise ValueError(f"{WARN_COST_DATA_INVALID}: cost metadata must include a timezone offset")

    try:
        return parsed.astimezone(UTC)
    except (OverflowError, OSError) as exc:
        raise ValueError(
            f"{WARN_COST_DATA_INVALID}: cost metadata timestamp is out of representable range: {value!r}"
        ) from exc


def _format_cost_warning_context(model_id: str | None = None, provenance: str | None = None) -> str:
    """Return an optional warning-context prefix for model-specific cost metadata messages."""
    context_parts: list[str] = []
    if isinstance(model_id, str) and model_id.strip():
        context_parts.append(f"model {model_id.strip()!r}")
    if isinstance(provenance, str) and provenance.strip():
        context_parts.append(f"source={provenance.strip()}")
    return f"{' '.join(context_parts)}: " if context_parts else ""


def _get_warning_provenance(entry: Mapping[str, Any] | None) -> str:
    """Return the best available source label for warning messages about a model row."""
    if isinstance(entry, Mapping):
        provenance = entry.get("provenance")
        if isinstance(provenance, str) and provenance.strip():
            return provenance.strip()
        source_metadata = entry.get("sourceMetadata")
        if isinstance(source_metadata, Mapping):
            source = source_metadata.get("source")
            if isinstance(source, str) and source.strip():
                return source.strip()
    return "unknown"


def warn_cost_data_locale(
    value: Any,
    *,
    now: datetime | None = None,
    emit_warnings: bool = True,
    model_id: str | None = None,
    provenance: str | None = None,
) -> None:
    """Backward-compatible alias for stale cost-data warnings."""
    warn_cost_data_stale(value, now=now, emit_warnings=emit_warnings, model_id=model_id, provenance=provenance)


def warn_cost_data_stale(
    value: Any,
    *,
    now: datetime | None = None,
    emit_warnings: bool = True,
    model_id: str | None = None,
    provenance: str | None = None,
) -> None:
    """Warn only when cost-data metadata is older than the freshness window."""
    try:
        parsed_utc = _parse_cost_data_timestamp(value)
    except ValueError as exc:
        if emit_warnings:
            print(str(exc), file=sys.stderr)
        raise
    reference_now = now or datetime.now(UTC)
    if parsed_utc > reference_now:
        message = f"{WARN_COST_DATA_INVALID}: cost metadata timestamp is in the future"
        if emit_warnings:
            print(message, file=sys.stderr)
        raise ValueError(message)
    freshness_window = timedelta(days=MODEL_COST_FRESHNESS_DAYS)
    if reference_now - parsed_utc > freshness_window:
        context = _format_cost_warning_context(model_id, provenance)
        message = f"{WARN_COST_DATA_STALE}: {context}cost metadata is older than {MODEL_COST_FRESHNESS_DAYS} days"
        if emit_warnings:
            print(message, file=sys.stderr)


def warn_cost_data_missing(value: Any, *, now: datetime | None = None) -> None:
    """Fail closed when cost metadata is absent or blank; valid timestamps are accepted."""
    del now
    if value is None:
        message = f"{WARN_COST_DATA_MISSING}: cost metadata is absent"
        print(message, file=sys.stderr)
        raise ValueError(message)
    if isinstance(value, str) and not value.strip():
        message = f"{WARN_COST_DATA_MISSING}: cost metadata is blank"
        print(message, file=sys.stderr)
        raise ValueError(message)
    if isinstance(value, str):
        return
    message = f"{WARN_COST_DATA_INVALID}: cost metadata must be an ISO-8601 UTC string"
    print(message, file=sys.stderr)
    raise ValueError(message)


def warn_cost_data_invalid(value: Any, *, now: datetime | None = None) -> None:
    """Fail closed when cost metadata is malformed or missing a usable timestamp."""
    del now
    if value is None:
        message = f"{WARN_COST_DATA_MISSING}: cost metadata is absent"
        print(message, file=sys.stderr)
        raise ValueError(message)
    if isinstance(value, str) and not value.strip():
        message = f"{WARN_COST_DATA_MISSING}: cost metadata is blank"
        print(message, file=sys.stderr)
        raise ValueError(message)
    try:
        _parse_cost_data_timestamp(value)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise


def validate_model_metadata(entry: dict[str, Any], *, emit_warnings: bool = True) -> None:
    """Validate a status-aware normalized model tree entry."""
    if not isinstance(entry, dict):
        raise ValueError("model metadata entry must be a dict")

    required_fields = ("modelId", "surfaces")
    for field in required_fields:
        if field not in entry:
            raise ValueError(f"missing required field {field!r} in model metadata")

    model_id = entry.get("modelId")
    if not isinstance(model_id, str) or not model_id.strip():
        raise ValueError("modelId must be a non-empty string")

    surfaces = entry.get("surfaces")
    if not isinstance(surfaces, dict):
        raise ValueError("surfaces must be a mapping")
    unknown_surfaces = set(surfaces) - MODEL_SURFACE_KEYS
    if unknown_surfaces:
        raise ValueError(f"surfaces contains unsupported keys: {sorted(unknown_surfaces)}")
    missing_surfaces = MODEL_SURFACE_KEYS - set(surfaces)
    if missing_surfaces:
        raise ValueError(f"surfaces missing required keys: {sorted(missing_surfaces)}")
    for surface, surface_value in surfaces.items():
        if not isinstance(surface_value, dict):
            raise ValueError(f"surfaces[{surface!r}] must map to a dict")
        if not surface_value:
            raise ValueError(f"surfaces[{surface!r}] must not be empty")
        identity_field = _SURFACE_IDENTITY_FIELD[surface]
        if not isinstance(surface_value.get(identity_field), str) or not surface_value[identity_field].strip():
            raise ValueError(f"surfaces[{surface!r}] must contain a non-empty {identity_field!r}")
        if surface == "copilot" and surface_value[identity_field].strip() != model_id.strip():
            raise ValueError("surfaces['copilot']['modelId'] must match modelId")

    pricing_status = entry.get("pricingStatus")
    if pricing_status is None:
        raise ValueError("missing required field 'pricingStatus' in model metadata")
    if not isinstance(pricing_status, str) or pricing_status not in _PRICING_STATUSES:
        raise ValueError(f"pricingStatus must be one of {sorted(_PRICING_STATUSES)}")
    unavailable_reason = entry.get("unavailableReason")
    if pricing_status == "unavailable":
        if unavailable_reason is not None and (
            not isinstance(unavailable_reason, str) or unavailable_reason not in _UNAVAILABLE_REASONS
        ):
            raise ValueError(f"unavailableReason must be one of {sorted(_UNAVAILABLE_REASONS)} when provided")
    elif unavailable_reason is not None:
        raise ValueError("unavailableReason is only supported when pricingStatus is 'unavailable'")
    if pricing_status != "non_priceable" and model_id in KNOWN_NON_PRICEABLE_MODELS:
        raise ValueError("routing options must use non_priceable status")
    if pricing_status != "priceable":
        if _MONETARY_FIELDS.intersection(entry):
            raise ValueError(f"{WARN_COST_DATA_INVALID}: {pricing_status} model cannot carry monetary fields")
        price_category = entry.get("priceCategory")
        if price_category is not None and (not isinstance(price_category, str) or not price_category.strip()):
            raise ValueError("priceCategory must be a non-empty string or None")
        for optional_field in ("provenance", "observedAt"):
            value = entry.get(optional_field)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(f"{optional_field} must be a non-empty string when provided")
        observed_at = entry.get("observedAt")
        if observed_at is not None:
            _parse_cost_data_timestamp(observed_at)
        source_metadata = entry.get("sourceMetadata")
        if source_metadata is not None and not isinstance(source_metadata, dict):
            raise ValueError("sourceMetadata must be a mapping when provided")
        if pricing_status == "non_priceable" and model_id not in KNOWN_NON_PRICEABLE_MODELS:
            raise ValueError("non_priceable status is reserved for routing options")
        return

    missing_cost_fields = _PRICEABLE_FIELDS - set(entry)
    if missing_cost_fields:
        raise ValueError(
            f"{WARN_COST_DATA_MISSING}: model {model_id!r} source={entry.get('provenance', 'unknown')} "
            f"missing required field(s) {sorted(missing_cost_fields)}"
        )

    currency = entry.get("currency")
    if not isinstance(currency, str) or not currency.strip():
        raise ValueError("currency must be a non-empty string")

    rate_unit = entry.get("rateUnit")
    if not isinstance(rate_unit, str) or not rate_unit.strip():
        raise ValueError("rateUnit must be a non-empty string")

    provenance = entry.get("provenance")
    if not isinstance(provenance, str) or not provenance.strip():
        raise ValueError("provenance must be a non-empty string")

    price_category = entry.get("priceCategory")
    if not isinstance(price_category, str) or not price_category.strip():
        raise ValueError("priceCategory must be a non-empty string")

    input_rate = _coerce_decimal(entry["inputRatePerM"], field_name="inputRatePerM")
    if input_rate < 0:
        raise ValueError("inputRatePerM must be non-negative")
    output_rate = _coerce_decimal(entry["outputRatePerM"], field_name="outputRatePerM")
    if output_rate < 0:
        raise ValueError("outputRatePerM must be non-negative")

    input_tokens = entry.get("assumedInputTokens")
    if isinstance(input_tokens, bool) or not isinstance(input_tokens, int) or input_tokens < 0:
        raise ValueError("assumedInputTokens must be a non-negative integer")
    output_tokens = entry.get("assumedOutputTokens")
    if isinstance(output_tokens, bool) or not isinstance(output_tokens, int) or output_tokens < 0:
        raise ValueError("assumedOutputTokens must be a non-negative integer")

    cost_data_as_of = entry.get("costDataAsOf")
    warn_cost_data_locale(
        cost_data_as_of,
        emit_warnings=emit_warnings,
        model_id=model_id,
        provenance=provenance,
    )

    expected_cost = calculate_modelled_session_cost(
        entry["inputRatePerM"],
        entry["outputRatePerM"],
        entry["assumedInputTokens"],
        entry["assumedOutputTokens"],
    )
    actual_cost = entry.get("modelledSessionCost")
    if not isinstance(actual_cost, str):
        raise ValueError(f"modelledSessionCost must be a string for {model_id!r}, got {type(actual_cost).__name__!r}")
    try:
        actual_decimal = Decimal(actual_cost)
    except InvalidOperation as exc:
        raise ValueError(f"modelledSessionCost is not a valid decimal for {model_id!r}: {actual_cost!r}") from exc
    if not actual_decimal.is_finite():
        raise ValueError(f"modelledSessionCost must be finite for {model_id!r}: {actual_cost!r}")
    if actual_decimal != Decimal(expected_cost):
        raise ValueError(
            f"modelledSessionCost mismatch for {model_id!r}: expected {expected_cost!r}, got {actual_cost!r}"
        )
    source_metadata = entry.get("sourceMetadata")
    if source_metadata is not None and not isinstance(source_metadata, dict):
        raise ValueError("sourceMetadata must be a mapping when provided")
    observed_at = entry.get("observedAt")
    if observed_at is not None:
        _parse_cost_data_timestamp(observed_at)


def _build_model_metadata_entry(
    model_id: str,
    *,
    existing_entry: dict[str, Any] | None = None,
    acp_record: Any | None = None,
    acp_cache_record: Any | None = None,
    warn_pricing_unavailable: bool = True,
    emit_warnings: bool = True,
) -> dict[str, Any]:
    """Normalize one model row using live ACP, cache, project, then catalog data."""
    if not isinstance(model_id, str):
        raise ValueError("model_id must be a string")
    normalized_id = model_id.strip()
    if not normalized_id:
        raise ValueError("model_id must not be blank")

    if isinstance(existing_entry, dict):
        existing_model_id = existing_entry.get("modelId")
        if (
            isinstance(existing_model_id, str)
            and existing_model_id.strip()
            and existing_model_id.strip() != normalized_id
        ):
            raise ValueError(
                f"existing modelId {existing_model_id!r} does not match normalized model id {normalized_id!r}"
            )
    if acp_record is not None:
        acp_model_id = getattr(acp_record, "model_id", None)
        if isinstance(acp_model_id, str) and acp_model_id.strip() and acp_model_id.strip() != normalized_id:
            raise ValueError(f"ACP model_id {acp_model_id!r} does not match normalized model id {normalized_id!r}")
    if acp_cache_record is not None:
        acp_cache_model_id = getattr(acp_cache_record, "model_id", None)
        if (
            isinstance(acp_cache_model_id, str)
            and acp_cache_model_id.strip()
            and acp_cache_model_id.strip() != normalized_id
        ):
            raise ValueError(
                f"ACP cache model_id {acp_cache_model_id!r} does not match normalized model id {normalized_id!r}"
            )

    model_entry = (
        {k: v for k, v in existing_entry.items() if k in _MODEL_ENTRY_FIELDS}
        if isinstance(existing_entry, dict)
        else {}
    )
    model_entry["modelId"] = normalized_id

    catalog_entry = MODEL_CATALOG.get(normalized_id)

    surfaces = model_entry.get("surfaces")
    if not isinstance(surfaces, dict):
        surfaces = {}
    else:
        surfaces = dict(surfaces)
    raw_metadata = getattr(acp_record, "raw_metadata", None)
    live_name = raw_metadata.get("name") if isinstance(raw_metadata, Mapping) and "name" in raw_metadata else None
    display_name = (
        live_name.strip()
        if isinstance(live_name, str) and live_name.strip()
        else MODEL_SURFACE_DISPLAY_NAMES.get(normalized_id, normalized_id)
    )
    existing_copilot = surfaces.get("copilot")
    if isinstance(existing_copilot, dict):
        copilot_model_id = existing_copilot.get("modelId")
        if isinstance(copilot_model_id, str) and copilot_model_id.strip() and copilot_model_id.strip() != normalized_id:
            raise ValueError(
                "surfaces['copilot']['modelId'] "
                f"{copilot_model_id!r} does not match normalized model id {normalized_id!r}"
            )
    surfaces.setdefault("copilot", {"modelId": normalized_id})
    surfaces.setdefault("vscode", {"displayName": display_name})
    surfaces.setdefault("docs", {"displayName": display_name})
    if isinstance(live_name, str) and live_name.strip():
        for surface in ("vscode", "docs"):
            surface_value = surfaces.get(surface)
            if not isinstance(surface_value, dict):
                surface_value = {}
            else:
                surface_value = dict(surface_value)
            surface_value["displayName"] = display_name
            surfaces[surface] = surface_value
    model_entry["surfaces"] = {key: surfaces[key] for key in sorted(surfaces)}

    source_metadata: dict[str, Any] = {}
    existing_source = model_entry.get("sourceMetadata")
    if isinstance(existing_source, dict):
        source_metadata.update(existing_source)

    acp_pricing: dict[str, Any] | None = None
    acp_pricing_source: str | None = getattr(acp_record, "source", None) if acp_record is not None else None
    acp_cache_pricing_metadata: Mapping[str, Any] | None = None
    acp_invalid = False
    acp_invalid_source: str | None = None
    pricing_unavailable = False
    if acp_record is not None:
        from agentic_devtools.ai_providers.copilot_discovery import extract_acp_pricing

        if isinstance(raw_metadata, Mapping):
            acp_metadata = raw_metadata.get("_meta")
            relevant_meta = (
                {
                    key: acp_metadata[key]
                    for key in ("copilotUsage", "copilotPriceCategory", "copilotEnablement")
                    if key in acp_metadata
                }
                if isinstance(acp_metadata, Mapping)
                else {}
            )
            source_metadata["acp"] = relevant_meta
        source = getattr(acp_record, "source", "acp-live")
        source_metadata["source"] = source
        observed_at = getattr(acp_record, "observed_at", None)
        if isinstance(observed_at, str) and observed_at.strip():
            source_metadata["observedAt"] = observed_at
            model_entry["observedAt"] = observed_at
        if normalized_id not in KNOWN_NON_PRICEABLE_MODELS:
            try:
                acp_pricing = extract_acp_pricing(raw_metadata if isinstance(raw_metadata, Mapping) else {})
            except ValueError as exc:
                acp_invalid = True
                acp_invalid_source = source
                print(
                    f"{WARN_COST_DATA_INVALID}: model {normalized_id!r} source={source}: {exc}",
                    file=sys.stderr,
                )
    if (
        acp_pricing is None
        and not acp_invalid
        and acp_cache_record is not None
        and normalized_id not in KNOWN_NON_PRICEABLE_MODELS
    ):
        from agentic_devtools.ai_providers.copilot_discovery import extract_acp_pricing

        cached_raw_metadata = getattr(acp_cache_record, "raw_metadata", None)
        if isinstance(cached_raw_metadata, Mapping):
            try:
                acp_pricing = extract_acp_pricing(cached_raw_metadata)
            except ValueError as exc:
                acp_invalid = True
                acp_invalid_source = getattr(acp_cache_record, "source", "acp-cache")
                print(
                    f"{WARN_COST_DATA_INVALID}: model {normalized_id!r} source={acp_invalid_source}: {exc}",
                    file=sys.stderr,
                )
            else:
                if acp_pricing is not None:
                    acp_pricing_source = getattr(acp_cache_record, "source", "acp-cache")
                    acp_cache_pricing_metadata = cached_raw_metadata

    if normalized_id in KNOWN_NON_PRICEABLE_MODELS:
        model_entry = {key: value for key, value in model_entry.items() if key not in _MONETARY_FIELDS}
        model_entry["pricingStatus"] = "non_priceable"
        model_entry["priceCategory"] = "non_priceable"
        model_entry["provenance"] = "static-catalog"
        model_entry.pop("unavailableReason", None)
    elif acp_pricing is not None:
        if acp_cache_pricing_metadata is not None:
            cache_meta = acp_cache_pricing_metadata.get("_meta")
            if isinstance(cache_meta, Mapping):
                cached_acp_fields = {
                    key: cache_meta[key]
                    for key in ("copilotUsage", "copilotPriceCategory", "copilotEnablement")
                    if key in cache_meta
                }
                merged_acp = dict(cached_acp_fields)
                live_acp = source_metadata.get("acp")
                if isinstance(live_acp, dict):
                    merged_acp.update(live_acp)
                source_metadata["acp"] = merged_acp
        model_entry = {key: value for key, value in model_entry.items() if key not in _PRICEABLE_FIELDS}
        model_entry.update(acp_pricing)
        _raw_category = (
            source_metadata.get("acp", {}).get("copilotPriceCategory")
            if isinstance(source_metadata.get("acp"), dict)
            else None
        )
        model_entry["priceCategory"] = (
            _raw_category.strip() if isinstance(_raw_category, str) and _raw_category.strip() else "unknown"
        )
        model_entry["provenance"] = acp_pricing_source if isinstance(acp_pricing_source, str) else "acp-live"
        model_entry["pricingStatus"] = "priceable"
        model_entry.pop("unavailableReason", None)
    elif acp_invalid:
        model_entry = {key: value for key, value in model_entry.items() if key not in _MONETARY_FIELDS}
        model_entry["pricingStatus"] = "unavailable"
        _raw_unavailable_category = (
            source_metadata.get("acp", {}).get("copilotPriceCategory")
            if isinstance(source_metadata.get("acp"), dict)
            else None
        )
        model_entry["priceCategory"] = (
            _raw_unavailable_category.strip()
            if isinstance(_raw_unavailable_category, str) and _raw_unavailable_category.strip()
            else None
        )
        model_entry["provenance"] = (
            acp_invalid_source if isinstance(acp_invalid_source, str) else getattr(acp_record, "source", "acp-live")
        )
        model_entry["unavailableReason"] = "invalid"
    else:
        existing_status = model_entry.get("pricingStatus")
        existing_is_priceable = existing_status == "priceable" or (
            existing_status is None and _PRICE_INPUT_FIELDS.issubset(model_entry)
        )
        if existing_is_priceable:
            model_entry["pricingStatus"] = "priceable"
        elif catalog_entry is not None:
            unavailable_source_markers = {model_entry.get("provenance")}
            existing_source = model_entry.get("sourceMetadata")
            existing_source_marker = existing_source.get("source") if isinstance(existing_source, dict) else None
            if isinstance(existing_source_marker, str):
                unavailable_source_markers.add(existing_source_marker)
            # Treat either persisted source marker as authoritative enough to keep ACP-invalid rows
            # fail-closed. The fallback only upgrades unavailable rows when neither marker points
            # to ACP discovery.
            unavailable_reason = model_entry.get("unavailableReason")
            unavailable_source_is_acp = any(
                isinstance(marker, str) and marker in _ACP_PRICING_SOURCES for marker in unavailable_source_markers
            )
            unavailable_from_invalid_acp_source = (
                acp_record is None
                and existing_status == "unavailable"
                and unavailable_reason == "invalid"
                and unavailable_source_is_acp
            )
            if unavailable_from_invalid_acp_source:
                model_entry = {key: value for key, value in model_entry.items() if key not in _MONETARY_FIELDS}
                model_entry["pricingStatus"] = "unavailable"
                model_entry.setdefault("priceCategory", None)
                model_entry["unavailableReason"] = "invalid"
            else:
                if existing_status == "unavailable":
                    model_entry = {
                        key: value
                        for key, value in model_entry.items()
                        if key not in _PRICEABLE_FIELDS and key not in {"pricingStatus", "unavailableReason"}
                    }
                    model_entry.update(catalog_entry)
                else:
                    for field_name, default_value in catalog_entry.items():
                        if field_name not in model_entry or model_entry[field_name] is None:
                            model_entry[field_name] = default_value
                model_entry["pricingStatus"] = "priceable"
                model_entry.pop("unavailableReason", None)
        else:
            pricing_unavailable = True
            model_entry = {key: value for key, value in model_entry.items() if key not in _MONETARY_FIELDS}
            model_entry["pricingStatus"] = "unavailable"
            model_entry.setdefault("priceCategory", None)
            # Preserve "invalid" for ACP-sourced rows so the fail-closed marker is not
            # downgraded to "missing" on subsequent loads when ACP is not available and
            # the model is also absent from the catalog.
            _prior_provenance = model_entry.get("provenance")
            _prior_is_acp_invalid = (
                acp_record is None
                and existing_status == "unavailable"
                and model_entry.get("unavailableReason") == "invalid"
                and isinstance(_prior_provenance, str)
                and _prior_provenance in _ACP_PRICING_SOURCES
            )
            if not _prior_is_acp_invalid:
                model_entry["unavailableReason"] = "missing"
            if acp_record is not None:
                model_entry["provenance"] = getattr(acp_record, "source", "acp-live")
            else:
                model_entry.setdefault("provenance", "project-config")

    if (
        acp_record is not None
        and model_entry.get("pricingStatus") != "non_priceable"
        and isinstance(source_metadata.get("acp"), dict)
    ):
        acp_category = source_metadata["acp"].get("copilotPriceCategory")
        if isinstance(acp_category, str) and acp_category.strip():
            model_entry["priceCategory"] = acp_category.strip()
    if "pricingStatus" in model_entry and model_entry["pricingStatus"] == "priceable":
        model_entry.setdefault(
            "modelledSessionCost",
            calculate_modelled_session_cost(
                model_entry["inputRatePerM"],
                model_entry["outputRatePerM"],
                model_entry["assumedInputTokens"],
                model_entry["assumedOutputTokens"],
            ),
        )
    if source_metadata:
        model_entry["sourceMetadata"] = source_metadata
    validate_model_metadata(model_entry, emit_warnings=emit_warnings)
    if pricing_unavailable and warn_pricing_unavailable:
        print(
            f"{WARN_COST_DATA_UNAVAILABLE}: model {normalized_id!r} "
            f"source={getattr(acp_record, 'source', 'project-config')}",
            file=sys.stderr,
        )
    return model_entry


def get_model_metadata(model_id: str, *, git_root: Path | None = None) -> dict[str, Any] | None:
    """Return the normalized model metadata entry for *model_id* when present."""
    if not isinstance(model_id, str):
        return None
    model_key = model_id.strip()
    if not model_key:
        return None
    config = load_project_config(git_root=git_root)
    models = config.get("models")
    if not isinstance(models, dict):
        return None
    entry = models.get(model_key)
    if not isinstance(entry, dict):
        return None
    try:
        normalized_entry = (
            _build_model_metadata_entry(model_key, existing_entry=entry) if "pricingStatus" not in entry else entry
        )
        validate_model_metadata(normalized_entry)
    except ValueError:
        return None
    return normalized_entry


def _build_invalid_unavailable_marker(model_id: str, entry: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Build a canonical unavailable marker for an invalid persisted model row."""
    normalized_id = model_id.strip()
    default_display_name = MODEL_SURFACE_DISPLAY_NAMES.get(normalized_id, normalized_id)
    source_metadata = entry.get("sourceMetadata") if isinstance(entry, Mapping) else None
    raw_price_category = entry.get("priceCategory") if isinstance(entry, Mapping) else None
    provenance = entry.get("provenance") if isinstance(entry, Mapping) else None
    if not isinstance(provenance, str) or not provenance.strip():
        source_marker = source_metadata.get("source") if isinstance(source_metadata, Mapping) else None
        provenance = source_marker if isinstance(source_marker, str) and source_marker.strip() else "unknown"

    surfaces = entry.get("surfaces") if isinstance(entry, Mapping) else None
    vscode_display_name = default_display_name
    docs_display_name = default_display_name
    if isinstance(surfaces, Mapping):
        for surface_name, default_name in (("vscode", default_display_name), ("docs", default_display_name)):
            surface_value = surfaces.get(surface_name)
            surface_display_name = surface_value.get("displayName") if isinstance(surface_value, Mapping) else None
            if isinstance(surface_display_name, str) and surface_display_name.strip():
                if surface_name == "vscode":
                    vscode_display_name = surface_display_name.strip()
                else:
                    docs_display_name = surface_display_name.strip()
            else:
                if surface_name == "vscode":
                    vscode_display_name = default_name
                else:
                    docs_display_name = default_name

    marker = {
        "modelId": normalized_id,
        "surfaces": {
            "copilot": {"modelId": normalized_id},
            "vscode": {"displayName": vscode_display_name},
            "docs": {"displayName": docs_display_name},
        },
        "pricingStatus": "unavailable",
        "priceCategory": raw_price_category.strip()
        if isinstance(raw_price_category, str) and raw_price_category.strip()
        else None,
        "provenance": provenance,
        "unavailableReason": "invalid",
    }
    if isinstance(source_metadata, dict):
        marker["sourceMetadata"] = dict(source_metadata)
    observed_at = entry.get("observedAt") if isinstance(entry, Mapping) else None
    if isinstance(observed_at, str) and observed_at.strip():
        try:
            _parse_cost_data_timestamp(observed_at)
        except ValueError:
            pass
        else:
            marker["observedAt"] = observed_at
    validate_model_metadata(marker, emit_warnings=False)
    return marker


def migrate_legacy_model_inventory(config: dict[str, Any], *, emit_warnings: bool = True) -> dict[str, Any]:
    """Migrate legacy flat ``availableModels`` entries to the normalized ``models`` tree."""
    if not isinstance(config, dict):
        raise ValueError("config must be a dict")

    migrated = dict(config)
    legacy_models = migrated.get("availableModels")
    existing_models = migrated.get("models")
    if not isinstance(existing_models, dict):
        existing_models = {}

    normalized: dict[str, dict[str, Any]] = {}
    seen: set[str] = set()
    for model_id, entry in existing_models.items():
        if not isinstance(model_id, str):
            continue
        normalized_key = model_id.strip()
        if not normalized_key:
            continue
        if isinstance(entry, dict):
            try:
                if "pricingStatus" in entry:
                    entry_model_id = entry.get("modelId")
                    if not isinstance(entry_model_id, str) or entry_model_id.strip() != normalized_key:
                        raise ValueError(
                            f"modelId {entry_model_id!r} does not match normalized model key {normalized_key!r}"
                        )
                    validate_model_metadata(entry, emit_warnings=False)
                normalized[normalized_key] = _build_model_metadata_entry(
                    normalized_key,
                    existing_entry=entry,
                    warn_pricing_unavailable=False,
                    emit_warnings=emit_warnings,
                )
                seen.add(normalized_key)
            except ValueError as exc:
                message = str(exc)
                if emit_warnings and _is_tagged_cost_warning(message):
                    print(message, file=sys.stderr)
                elif emit_warnings:
                    warning_provenance = _get_warning_provenance(entry)
                    print(
                        f"WARN_COST_DATA_INVALID: could not rebuild normalized entry for {normalized_key!r}, "
                        f"source={warning_provenance}, persisting unavailable marker",
                        file=sys.stderr,
                    )
                normalized[normalized_key] = _build_invalid_unavailable_marker(normalized_key, entry)
                seen.add(normalized_key)

    ordered_models: list[str] = []
    if isinstance(legacy_models, list):
        for model in legacy_models:
            if not isinstance(model, str):
                continue
            candidate = model.strip()
            if not candidate:
                continue
            if candidate not in seen:
                try:
                    normalized[candidate] = _build_model_metadata_entry(
                        candidate,
                        warn_pricing_unavailable=False,
                        emit_warnings=emit_warnings,
                    )
                    seen.add(candidate)
                except ValueError as exc:
                    message = str(exc)
                    if emit_warnings and _is_tagged_cost_warning(message):
                        print(message, file=sys.stderr)
                    elif emit_warnings:
                        print(
                            f"WARN_COST_DATA_INVALID: could not build normalized entry for {candidate!r}",
                            file=sys.stderr,
                        )
            if candidate not in ordered_models:
                ordered_models.append(candidate)

    if normalized:
        all_normalized_ids = list(ordered_models) + [m for m in normalized if m not in ordered_models]
        migrated["models"] = {mid: normalized[mid] for mid in all_normalized_ids if mid in normalized}
    else:
        migrated.pop("models", None)
    if isinstance(legacy_models, list):
        migrated["availableModels"] = list(dict.fromkeys(ordered_models))
    return migrated


# ──────────────────────────────────────────────────────────────────────────────
# issue_types_metadata validation and access (FR-002 / FR-004 / FR-005)
# ──────────────────────────────────────────────────────────────────────────────


def _validate_utc_timestamp(value: Any, field_name: str) -> None:
    """Validate an ISO-8601 UTC timestamp field.

    Requirements:
    - Must be a string parseable by ``datetime.fromisoformat()``
    - Must be timezone-aware (``tzinfo`` is not ``None``)
    - Must have zero UTC offset (``+00:00``)
    - Must NOT use the ``Z`` suffix
    """
    if not isinstance(value, str):
        raise ValueError(f"'{field_name}' must be a string, got {type(value).__name__}")
    if value.endswith("Z") or value.endswith("z"):
        raise ValueError(f"'{field_name}' must use '+00:00' explicit UTC offset, not 'Z' suffix")
    try:
        dt = datetime.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError(f"'{field_name}' is not a valid ISO-8601 timestamp: {value!r}")
    if dt.tzinfo is None:
        raise ValueError(f"'{field_name}' must be timezone-aware (include UTC offset)")
    if dt.utcoffset() != UTC.utcoffset(None):
        raise ValueError(f"'{field_name}' must have zero UTC offset (+00:00)")
    if not value.endswith("+00:00"):
        raise ValueError(f"'{field_name}' must use canonical '+00:00' UTC offset, got {value!r}")


def _validate_property_entry(prop: Any, issue_type_index: int, index: int) -> None:
    """Validate a single PropertyEntry dict."""
    prefix = f"issue_types[{issue_type_index}].properties[{index}]"
    if not isinstance(prop, dict):
        raise ValueError(f"{prefix} must be a dict, got {type(prop).__name__}")

    for str_field in ("name", "display_name", "type"):
        val = prop.get(str_field)
        if not isinstance(val, str):
            raise ValueError(f"{prefix}.{str_field} must be a string, got {type(val).__name__}")
        if not val.strip():
            raise ValueError(f"{prefix}.{str_field} must be a non-empty string")

    for bool_field in ("required", "included_in_template"):
        val = prop.get(bool_field)
        if not isinstance(val, bool):
            raise ValueError(f"{prefix}.{bool_field} must be a boolean, got {type(val).__name__}")

    if "allowed_values" not in prop:
        raise ValueError(f"{prefix}.allowed_values must be present (use null when not applicable)")
    allowed = prop["allowed_values"]
    if allowed is not None:
        if not isinstance(allowed, list):
            raise ValueError(f"{prefix}.allowed_values must be a list or null, got {type(allowed).__name__}")
        for i, item in enumerate(allowed):
            if not isinstance(item, str):
                raise ValueError(f"{prefix}.allowed_values[{i}] must be a string, got {type(item).__name__}")
            if not item.strip():
                raise ValueError(f"{prefix}.allowed_values[{i}] must be a non-empty string")


def _validate_issue_type_entry(entry: Any, index: int) -> None:
    """Validate a single IssueTypeEntry dict."""
    prefix = f"issue_types[{index}]"
    if not isinstance(entry, dict):
        raise ValueError(f"{prefix} must be a dict, got {type(entry).__name__}")

    for str_field in ("id", "name"):
        val = entry.get(str_field)
        if not isinstance(val, str):
            raise ValueError(f"{prefix}.{str_field} must be a string, got {type(val).__name__}")
        if not val.strip():
            raise ValueError(f"{prefix}.{str_field} must be a non-empty string")

    description = entry.get("description")
    if not isinstance(description, str):
        raise ValueError(f"{prefix}.description must be a string, got {type(description).__name__}")

    is_subtask = entry.get("is_subtask")
    if not isinstance(is_subtask, bool):
        raise ValueError(f"{prefix}.is_subtask must be a boolean, got {type(is_subtask).__name__}")

    properties = entry.get("properties")
    if not isinstance(properties, list):
        raise ValueError(f"{prefix}.properties must be a list, got {type(properties).__name__}")

    for i, prop in enumerate(properties):
        _validate_property_entry(prop, index, i)


def validate_issue_types_metadata(entry: dict[str, Any]) -> None:
    """Validate a single project's ``issue_types_metadata`` entry.

    Raises ``ValueError`` with a descriptive message when the entry violates
    the schema contract. Unknown extra keys are accepted at all levels for
    forward compatibility.
    """
    if not isinstance(entry, dict):
        raise ValueError(f"issue_types_metadata entry must be a dict, got {type(entry).__name__}")

    # Top-level required fields
    for field in ("lastDiscovered", "lastRefreshed", "provider", "issue_types"):
        if field not in entry:
            raise ValueError(f"missing required field '{field}'")

    # Timestamp validation
    _validate_utc_timestamp(entry["lastDiscovered"], "lastDiscovered")
    _validate_utc_timestamp(entry["lastRefreshed"], "lastRefreshed")

    # Provider validation
    provider = entry["provider"]
    if not isinstance(provider, str):
        raise ValueError(f"'provider' must be a string, got {type(provider).__name__}")
    if not provider.strip():
        raise ValueError("'provider' must be a non-empty string")

    # issue_types validation
    issue_types = entry["issue_types"]
    if not isinstance(issue_types, list):
        raise ValueError(f"'issue_types' must be a list, got {type(issue_types).__name__}")

    for i, it in enumerate(issue_types):
        _validate_issue_type_entry(it, i)


def get_issue_types_metadata(project_key: str, *, git_root: Path | None = None) -> ProjectIssueTypesMetadata | None:
    """Return the ``issue_types_metadata`` entry for *project_key*, or ``None``.

    Returns ``None`` when:
    - The ``issue_types_metadata`` key is absent from project config
    - The given *project_key* has no entry in ``issue_types_metadata``
    - The stored entry for *project_key* is not a dict
    - The stored entry for *project_key* fails schema validation
    """
    config = load_project_config(git_root=git_root)
    metadata = config.get("issue_types_metadata")
    if not isinstance(metadata, dict):
        return None
    entry = metadata.get(project_key)
    if not isinstance(entry, dict):
        return None
    try:
        validate_issue_types_metadata(entry)
    except ValueError:
        return None
    return cast(ProjectIssueTypesMetadata, entry)


# ──────────────────────────────────────────────────────────────────────────────
# Sync-eligible key mapping (FR-005)
# ──────────────────────────────────────────────────────────────────────────────


def _validate_string(value: Any) -> str | None:
    """Validator: value must be a non-empty string. Returns error or None."""
    if not isinstance(value, str) or not value.strip():
        return "must be a non-empty string"
    return None


def _validate_string_list(value: Any) -> str | None:
    """Validator: value must be a non-empty list of non-empty strings."""
    if not isinstance(value, list):
        return "must be a list"
    if not value:
        return "must not be empty"
    for i, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            return f"element at index {i} must be a non-empty string"
    return None


def _validate_comma_string(value: Any) -> str | None:
    """Validator: value must be a non-empty comma-separated string."""
    if not isinstance(value, str) or not value.strip():
        return "must be a non-empty string"
    if not any(part.strip() for part in value.split(",")):
        return "must contain at least one comma-separated item"
    return None


SYNC_ELIGIBLE_KEYS: dict[str, dict[str, Any]] = {
    "default_copilot_model": {
        "state_key": "copilot.model_id",
        "validator": _validate_string,
    },
    "defaultCommitIssueType": {
        "state_key": "versionControl.commitMessageType",
        "validator": _validate_string,
    },
    "availableCommitIssueTypes": {
        "state_key": "versionControl.availableCommitIssueTypes",
        "validator": _validate_string_list,
    },
    "jira_project_keys": {
        "state_key": "jira_project_keys",
        "validator": _validate_comma_string,
    },
    "jira_base_url": {
        "state_key": "jira_base_url",
        "validator": _validate_string,
    },
    "corporate_network_test_host": {
        "state_key": "corporate_network_test_host",
        "validator": _validate_string,
    },
    "vpn_hostnames": {
        "state_key": "vpn_hostnames",
        "validator": _validate_comma_string,
    },
    "vpn_url": {
        "state_key": "vpn_url",
        "validator": _validate_string,
    },
}
"""Mapping of project.json keys eligible for sync-back.

Each entry maps a ``project.json`` key name to:
- ``state_key``: the per-worktree state key where the source value lives
- ``validator``: a callable that returns ``None`` on success or an error string
"""


# ──────────────────────────────────────────────────────────────────────────────
# Effective project config (opt-in gate) — FR-002, FR-003
# ──────────────────────────────────────────────────────────────────────────────


def load_effective_project_config(*, git_root: Path | None = None) -> dict[str, Any]:
    """Load project config honoring the opt-in ``config_mode`` toggle.

    When ``config_mode`` is ``"auto"`` (or absent, which defaults to
    ``"auto"``), delegates to :func:`load_project_config` and returns
    the full configuration dictionary.

    When ``config_mode`` is ``"manual"``, returns an empty dict ``{}``,
    effectively making project.json invisible to resolution chains.

    Raises ``ValueError`` when the stored ``config_mode`` is an invalid value
    (neither ``"auto"`` nor ``"manual"``).
    """
    from agentic_devtools.cli.config.opt_in_mode import get_config_mode, validate_config_mode

    mode = get_config_mode()
    error = validate_config_mode(mode)
    if error:
        raise ValueError(error)
    if mode == "manual":
        return {}
    return load_project_config(git_root=git_root)


def get_effective_project_config_value(key: str) -> str | None:
    """Return a single value from the effective project config, or ``None``.

    Honors ``config_mode``: when mode is ``"manual"``, always returns
    ``None``.  When mode is ``"auto"``, resolves from ``project.json``.

    Raises:
        ValueError: When the stored ``config_mode`` is invalid.
    """
    value = load_effective_project_config().get(key)
    if value is None:
        return None
    return str(value)
