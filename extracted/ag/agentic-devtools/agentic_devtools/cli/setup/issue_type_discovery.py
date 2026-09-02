"""Automated issue type discovery during agdt-setup.

After platform configuration is saved, this module calls the adapter's
``get_issue_types()`` method and persists the results to
``.agdt/config/project.json`` with timestamps. Discovery is non-fatal:
failures are reported to stderr and setup continues.

Property discovery is performed after type discovery: for each type,
``get_type_properties()`` is called and results are mapped to
``PropertyEntry`` records with ``included_in_template=True`` default.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from agentic_devtools.adapters.base import IssueTypeInfo
from agentic_devtools.cli.config.project_config import (
    IssueTypeEntry,
    ProjectIssueTypesMetadata,
    PropertyEntry,
    validate_issue_types_metadata,
)
from agentic_devtools.cli.setup.property_change_detection import (
    PropertyChangeResult,
    detect_property_changes,
)
from agentic_devtools.cli.setup.provider_connectivity import check_provider_connectivity
from agentic_devtools.cli.setup.refresh_outcome import RefreshOutcome

if TYPE_CHECKING:
    from agentic_devtools.adapters.base import IssueAdapter
    from agentic_devtools.adapters.types import PropertySchema

_logger = logging.getLogger(__name__)
_AUTHORIZATION_STATUS_PATTERN = re.compile(r"\b(?:401|403)\b")


def _resolve_project_identifier(platform_config: dict[str, Any]) -> tuple[str, str] | None:
    """Resolve project identifier and provider slug from platform config.

    Returns:
        A ``(project_id, provider_slug)`` tuple, or ``None`` when the
        identifier cannot be resolved.
    """
    issue_adapter = platform_config.get("issue_adapter", "")

    if issue_adapter == "jira":
        jira_cfg = platform_config.get("jira", {})
        if not isinstance(jira_cfg, dict):
            jira_cfg = {}
        project_key = jira_cfg.get("project_key")
        if project_key and isinstance(project_key, str) and project_key.strip():
            return (project_key.strip(), "jira")
        return None

    if issue_adapter == "github":
        gh_cfg = platform_config.get("github", {})
        if not isinstance(gh_cfg, dict):
            gh_cfg = {}
        # Primary: combined "repo" key
        repo = gh_cfg.get("repo")
        if repo and isinstance(repo, str) and repo.strip():
            return (repo.strip(), "github")
        # Fallback: owner + name
        owner = gh_cfg.get("repo_owner", "")
        name = gh_cfg.get("repo_name", "")
        if isinstance(owner, str) and isinstance(name, str) and owner.strip() and name.strip():
            return (f"{owner.strip()}/{name.strip()}", "github")
        return None

    if issue_adapter == "markdown":
        return ("_default", "markdown")

    return None


def _map_issue_type_info(info: IssueTypeInfo) -> IssueTypeEntry | None:
    """Map adapter ``IssueTypeInfo`` to persistence ``IssueTypeEntry``.

    Skips entries with blank or missing ``name`` (debug log).

    Returns:
        An ``IssueTypeEntry`` dict, or ``None`` when the entry should be skipped.
    """
    name = info.get("name", "")  # type: ignore[arg-type]
    if not isinstance(name, str) or not name.strip():
        _logger.debug("Skipping IssueTypeInfo with blank/missing name: %r", info)
        return None
    normalized_name = name.strip()

    description = info.get("description", "")  # type: ignore[arg-type]
    if not isinstance(description, str):
        description = ""

    return IssueTypeEntry(
        id=normalized_name,
        name=normalized_name,
        description=description,
        is_subtask=False,
        properties=[],
    )


def _build_metadata(
    issue_types: list[IssueTypeEntry],
    provider: str,
    existing: ProjectIssueTypesMetadata | None,
    *,
    update_refreshed: bool = True,
) -> ProjectIssueTypesMetadata:
    """Build a ``ProjectIssueTypesMetadata`` with correct timestamp logic.

    First discovery sets both ``lastDiscovered`` and ``lastRefreshed`` to now.
    A refresh preserves ``lastDiscovered`` and updates ``lastRefreshed`` only
    when *update_refreshed* is ``True``.
    """
    now_utc = datetime.now(tz=timezone.utc).isoformat()

    if existing is not None:
        last_discovered = existing.get("lastDiscovered", now_utc)
        if update_refreshed:
            last_refreshed = now_utc
        else:
            last_refreshed = existing.get("lastRefreshed", now_utc)
    else:
        last_discovered = now_utc
        last_refreshed = now_utc

    return ProjectIssueTypesMetadata(
        lastDiscovered=last_discovered,
        lastRefreshed=last_refreshed,
        provider=provider,
        issue_types=issue_types,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Property discovery helpers (FR-002, FR-002a, FR-005)
# ──────────────────────────────────────────────────────────────────────────────


def _title_case_display_name(name: str) -> str:
    """Convert a property name to a title-cased display name.

    Replaces underscores with spaces and applies Python's ``str.title()``.
    No special handling for camelCase or dots.

    Examples:
        >>> _title_case_display_name("story_points")
        'Story Points'
        >>> _title_case_display_name("customField10042")
        'Customfield10042'
    """
    return name.replace("_", " ").title()


def _map_property_schema(schema: PropertySchema) -> PropertyEntry:
    """Map an adapter ``PropertySchema`` to a persistence ``PropertyEntry``.

    Sets ``included_in_template`` to ``True`` and derives ``display_name``
    from ``name`` via :func:`_title_case_display_name`.
    """
    return PropertyEntry(
        name=schema["name"],
        display_name=_title_case_display_name(schema["name"]),
        type=schema["type"],
        required=schema["required"],
        allowed_values=schema["allowed_values"],
        included_in_template=True,
    )


def _merge_properties(
    new_properties: list[PropertyEntry],
    existing_properties: list[PropertyEntry],
) -> list[PropertyEntry]:
    """Merge newly-discovered properties with existing cached properties.

    Preserves ``included_in_template`` from existing properties when the
    property name matches. Updates ``type``, ``required``, ``allowed_values``,
    and ``display_name`` from new data. New properties (not in existing)
    default to ``included_in_template=True``.

    Args:
        new_properties: Properties freshly discovered from the adapter.
        existing_properties: Previously cached properties (may be empty).

    Returns:
        Merged property list in the order of *new_properties*.
    """
    existing_by_name: dict[str, PropertyEntry] = {p["name"]: p for p in existing_properties}

    merged: list[PropertyEntry] = []
    for prop in new_properties:
        existing = existing_by_name.get(prop["name"])
        if existing is not None:
            # Preserve user customization of included_in_template
            merged.append(
                PropertyEntry(
                    name=prop["name"],
                    display_name=prop["display_name"],
                    type=prop["type"],
                    required=prop["required"],
                    allowed_values=prop["allowed_values"],
                    included_in_template=existing["included_in_template"],
                )
            )
        else:
            merged.append(prop)
    return merged


def discover_properties_for_project(
    adapter: IssueAdapter,
    issue_types: list[IssueTypeEntry],
    existing_types: list[IssueTypeEntry] | None,
) -> tuple[list[IssueTypeEntry], bool, bool]:
    """Discover properties for each issue type via the adapter.

    For each type, calls ``adapter.get_type_properties(type_name)`` and maps
    the results to ``PropertyEntry`` records. Handles partial failures
    gracefully: a failure for one type does not block other types.

    Pre-seeds each type's ``properties`` from *existing_types* (by name match)
    so that a ``NotImplementedError`` short-circuit preserves cached data.

    Args:
        adapter: The configured issue adapter instance.
        issue_types: Freshly-mapped issue types (with ``properties: []``).
        existing_types: Previously cached issue types (for merge), or ``None``.

    Returns:
        A tuple of ``(updated_types, at_least_one_success, any_failure)`` where
        *at_least_one_success* is ``True`` when at least one type's properties
        were successfully fetched (even if the result was an empty list), and
        *any_failure* is ``True`` when at least one property-fetch call raised
        an error.
    """
    # Build lookup of existing properties by type name for merge/preserve
    existing_by_name: dict[str, list[PropertyEntry]] = {}
    if existing_types is not None:
        for et in existing_types:
            existing_by_name[et["name"]] = et.get("properties", [])

    # Pre-seed: copy existing properties to new types so short-circuit preserves cache
    for t in issue_types:
        if t["name"] in existing_by_name:
            t["properties"] = list(existing_by_name[t["name"]])

    at_least_one_success = False
    any_failure = False

    for t in issue_types:
        type_name = t["name"]
        try:
            raw_properties = adapter.get_type_properties(type_name)
        except NotImplementedError:
            _logger.debug("Property discovery stopped: adapter does not implement get_type_properties()")
            return (issue_types, at_least_one_success, any_failure)
        except Exception as exc:  # noqa: BLE001
            print(
                f"  \u26a0 Property discovery failed ({type_name}): {exc}",
                file=sys.stderr,
            )
            any_failure = True
            # Preserve existing properties (already pre-seeded)
            continue

        # Map and merge with change detection
        new_properties = [_map_property_schema(schema) for schema in raw_properties]
        existing_props = existing_by_name.get(type_name, [])

        saved_dict: dict[str, dict[str, Any]] | None = (
            {p["name"]: dict(p) for p in existing_props} if existing_types is not None else None
        )
        fresh_dict: dict[str, dict[str, Any]] = {p["name"]: dict(p) for p in new_properties}

        result: PropertyChangeResult = detect_property_changes(saved_dict, fresh_dict)

        at_least_one_success = True
        if result.has_changes:
            t["properties"] = cast(list[PropertyEntry], list(result.merged.values()))
        prop_count = len(t["properties"])
        print(f"  {type_name}: {prop_count} properties discovered")

    return (issue_types, at_least_one_success, any_failure)


def discover_issue_types(
    git_root: Path,
    *,
    force_refresh: bool = False,
    skip_platform_detection: bool = False,
    standalone: bool = False,
    preflight_connectivity: tuple[bool, str | None] | None = None,
    preflight_warning_emitted: bool = False,
) -> RefreshOutcome:
    """Discover issue types from the configured provider and persist them.

    Called by ``setup_cmd()`` after platform configuration is saved. This is
    non-fatal: failures produce a warning to stderr and setup continues.

    Args:
        git_root: Repository root path.
        force_refresh: When ``True``, re-discover even if cache exists.
        skip_platform_detection: When ``True``, skip discovery entirely.
        standalone: When ``True`` (the ``--refresh-issue-types`` early-return
            path), persistence is strictly non-destructive: ``project.json`` is
            never overwritten when the existing file is malformed/non-object,
            and no write occurs when every property-fetch call fails.
        preflight_connectivity: Optional connectivity result from an earlier
            setup preflight in the same run. When provided, this function reuses
            it instead of probing again.
        preflight_warning_emitted: Whether an earlier setup preflight already
            printed an unreachable-provider warning for this provider.

    Returns:
        A :class:`RefreshOutcome` describing the outcome. The normal setup flow
        ignores the return value; the standalone refresh path consumes it.
    """
    if skip_platform_detection:
        _logger.debug("Issue type discovery skipped: --skip-platform-detection is active")
        return RefreshOutcome.skipped("skip_platform_detection")

    # Load platform config to resolve project identifier
    from agentic_devtools.config import load_platform_config  # noqa: PLC0415

    platform_config = load_platform_config(str(git_root))

    resolved = _resolve_project_identifier(platform_config)
    if resolved is None:
        _logger.debug("Issue type discovery skipped: cannot resolve project identifier")
        return RefreshOutcome.skipped("issue_type_discovery_unsupported")

    project_id, provider_slug = resolved

    # Check cache: if valid cache exists and not force_refresh, skip
    from agentic_devtools.cli.config.project_config import (  # noqa: PLC0415
        load_project_config,
    )

    project_cfg = load_project_config(git_root=git_root)
    metadata_section = project_cfg.get("issue_types_metadata")

    # Get existing metadata for timestamp preservation on refresh
    existing: ProjectIssueTypesMetadata | None = None
    if isinstance(metadata_section, dict) and project_id in metadata_section:
        entry = metadata_section[project_id]
        if isinstance(entry, dict):
            try:
                validate_issue_types_metadata(entry)
            except ValueError:
                _logger.debug(
                    "Ignoring invalid cached issue type metadata for project %r",
                    project_id,
                )
            else:
                existing = entry  # type: ignore[assignment]

    if existing is not None and not force_refresh:
        _logger.debug(
            "Issue type discovery skipped: valid cache exists for project %r (use --refresh-issue-types to force)",
            project_id,
        )
        return RefreshOutcome.success()

    if preflight_connectivity is None:
        is_connected, connectivity_error = check_provider_connectivity(provider_slug, git_root, timeout=5.0)
    else:
        is_connected, connectivity_error = preflight_connectivity
    if not is_connected:
        error_message = connectivity_error or "Provider unreachable"
        if not preflight_warning_emitted:
            print(
                f"  ⚠ Issue type discovery skipped: {provider_slug} is unreachable ({error_message})",
                file=sys.stderr,
            )
        return RefreshOutcome.failed("provider_unreachable", error_message)

    # Call adapter get_issue_types()
    try:
        from agentic_devtools.adapters import get_adapter  # noqa: PLC0415

        adapter = get_adapter(str(git_root))
        raw_types = adapter.get_issue_types()
    except NotImplementedError:
        _logger.debug(
            "Issue type discovery skipped: provider %r does not implement get_issue_types()",
            provider_slug,
        )
        return RefreshOutcome.skipped("issue_type_discovery_unsupported")
    except Exception as exc:  # noqa: BLE001
        exc_type = type(exc).__name__
        msg = str(exc)
        lower_msg = msg.lower()
        # Check for permissions/authorization hints
        if _AUTHORIZATION_STATUS_PATTERN.search(msg) or "forbidden" in lower_msg or "unauthorized" in lower_msg:
            print(
                f"  ⚠ Issue type discovery failed ({exc_type}): {msg}"
                " — credentials may lack sufficient permissions or authorization"
                " to access issue type metadata",
                file=sys.stderr,
            )
        else:
            print(
                f"  ⚠ Issue type discovery failed ({exc_type}): {msg}",
                file=sys.stderr,
            )
        return RefreshOutcome.failed("provider_unreachable", f"{exc_type}: {msg}")

    # Map results — guard against adapter returning None/non-iterable or
    # yielding unexpected element types (keeps non-fatal contract).
    mapped_types: list[IssueTypeEntry] = []
    try:
        for info in raw_types:
            entry_mapped = _map_issue_type_info(info)
            if entry_mapped is not None:
                mapped_types.append(entry_mapped)
    except Exception as exc:  # noqa: BLE001
        print(
            f"  ⚠ Issue type discovery: failed to map results ({type(exc).__name__}: {exc}) — skipping persist",
            file=sys.stderr,
        )
        return RefreshOutcome.failed("mapping_error", f"{type(exc).__name__}: {exc}")

    # Discover properties for each type (FR-001, FR-003, FR-004, FR-005, FR-006)
    existing_types = existing.get("issue_types", []) if existing is not None else None
    mapped_types, properties_success, properties_any_failure = discover_properties_for_project(
        adapter, mapped_types, existing_types
    )

    # Standalone refresh is strictly non-destructive: initial discovery may only
    # persist when at least one property-fetch call completed successfully
    # (including an empty property list). Zero-success paths — e.g. every fetch
    # raised, the adapter short-circuited with NotImplementedError before any
    # successful call, or no issue types were returned — must leave the cache
    # untouched (FR-002, FR-005).
    if standalone and not properties_success:
        if properties_any_failure:
            error_message = "All property discovery calls failed; project.json left unchanged."
            display_message = "all property discovery calls failed; cached metadata left unchanged."
        elif not mapped_types:
            error_message = (
                "Provider returned no issue types, so no property discovery call completed successfully; "
                "project.json left unchanged."
            )
            display_message = "no issue types were returned; cached metadata left unchanged."
        else:
            error_message = "No property discovery call completed successfully; project.json left unchanged."
            display_message = "property discovery did not complete successfully; cached metadata left unchanged."
        print(
            f"  ⚠ Issue type refresh failed: {display_message}",
            file=sys.stderr,
        )
        return RefreshOutcome.failed("property_fetch_failed", error_message)

    # Build metadata — only update lastRefreshed if at least one property discovery succeeded
    metadata = _build_metadata(mapped_types, provider_slug, existing, update_refreshed=properties_success)

    # Validate before persist
    try:
        validate_issue_types_metadata(metadata)  # type: ignore[arg-type]
    except ValueError as exc:
        print(
            f"  ⚠ Issue type discovery: validation failed ({exc}) — skipping persist",
            file=sys.stderr,
        )
        return RefreshOutcome.failed("validation_error", str(exc))

    # Persist with a stable sidecar lock. We cannot lock ``project.json``
    # itself for the read-modify-write cycle because the atomic ``os.replace()``
    # below swaps the pathname to a new inode: on Unix a waiter holding the lock
    # on the old inode could then read stale content and clobber a concurrent
    # writer, and on Windows replacing a still-open locked target can fail. A
    # dedicated sidecar (``project.json.lock``) is never replaced, so the lock
    # serializes the whole read + atomic-replace across processes (FR-005).
    from agentic_devtools.file_locking import locked_file  # noqa: PLC0415

    config_path = git_root / ".agdt" / "config" / "project.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = config_path.with_name(config_path.name + ".lock")

    try:
        with locked_file(lock_path, mode="a", exclusive=True):
            try:
                content = config_path.read_text(encoding="utf-8")
            except FileNotFoundError:
                content = ""
            malformed = False
            try:
                cfg = json.loads(content) if content.strip() else {}
            except json.JSONDecodeError:
                cfg = {}
                malformed = True
            if not isinstance(cfg, dict):
                cfg = {}
                malformed = True

            # Standalone refresh is strictly non-destructive: never overwrite a
            # malformed/non-object project.json with regenerated content.
            if malformed and standalone:
                print(
                    "  ⚠ Issue type refresh failed: existing project.json is malformed; leaving it unchanged.",
                    file=sys.stderr,
                )
                return RefreshOutcome.failed(
                    "malformed_project_json",
                    "Existing project.json is malformed or not a JSON object; left unchanged.",
                )

            if not isinstance(cfg.get("issue_types_metadata"), dict):
                cfg["issue_types_metadata"] = {}
            cfg["issue_types_metadata"][project_id] = metadata

            serialized = json.dumps(cfg, indent=2, sort_keys=True) + "\n"

            # Atomic write: write to a temp sibling, then os.replace() so a
            # crash or interruption cannot leave project.json partially written.
            # The sidecar lock (held above) serializes this across processes.
            tmp_fd, tmp_name = tempfile.mkstemp(dir=config_path.parent, prefix=".project_json_", suffix=".tmp")
            try:
                with os.fdopen(tmp_fd, "w", encoding="utf-8") as tmp_f:
                    tmp_f.write(serialized)
                os.replace(tmp_name, config_path)
            except Exception:
                # Clean up the temp file if the replace fails
                try:
                    os.unlink(tmp_name)
                except OSError:
                    pass
                raise
    except Exception as exc:  # noqa: BLE001
        print(
            f"  ⚠ Issue type discovery: failed to persist ({type(exc).__name__}: {exc})",
            file=sys.stderr,
        )
        return RefreshOutcome.failed("persist_error", f"{type(exc).__name__}: {exc}")

    type_count = len(mapped_types)
    print(f"  ✓ Discovered {type_count} issue type(s) for project {project_id!r}")
    return RefreshOutcome.success()
