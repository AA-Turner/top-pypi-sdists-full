"""Atomic persistence for incremental create-epic mapping documents."""

from __future__ import annotations

import json
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
from uuid import UUID

from agentic_devtools import state
from agentic_devtools.epic_tree.models import EpicTree


def _canonicalize_provider_target(
    provider_name: str, provider_target: str, *, allow_jira_site_only: bool = False
) -> str:
    """Return the provider-specific canonical form of a provider target."""
    target = provider_target.strip()
    if provider_name == "github":
        parts = target.split("/")
        if len(parts) != 2 or not all(parts):
            raise ValueError("GitHub provider_target must be in 'owner/repo' format")
        return "/".join(part.casefold() for part in parts)
    if provider_name == "jira":
        parsed = urlsplit(target)
        if parsed.scheme.casefold() not in {"http", "https"} or not parsed.hostname:
            raise ValueError("Jira provider_target must be an HTTP(S) URL")
        if "@" in parsed.netloc or "?" in target or "#" in target:
            raise ValueError("Jira provider_target must not contain userinfo, query, or fragment components")
        try:
            port = parsed.port
        except ValueError as exc:
            raise ValueError("Jira provider_target must contain a valid port") from exc
        host = parsed.hostname.casefold()
        if ":" in host and not host.startswith("["):
            host = f"[{host}]"
        if port is not None and port != {"http": 80, "https": 443}[parsed.scheme.casefold()]:
            host = f"{host}:{port}"
        # A Jira base URL may itself include a context path (for example
        # ``https://jira.example.com/jira``); only the final path segment is the
        # project key, so any preceding segments are preserved verbatim.
        path = parsed.path.rstrip("/")
        if not path.strip("/"):
            if not allow_jira_site_only:
                raise ValueError("Jira provider_target must include a project-key path segment")
            return f"{parsed.scheme.casefold()}://{host}{path}"
        if allow_jira_site_only:
            return f"{parsed.scheme.casefold()}://{host}{path}"
        project_key_start = path.rfind("/") + 1
        canonical_path = f"{path[:project_key_start]}{path[project_key_start:].upper()}"
        return f"{parsed.scheme.casefold()}://{host}{canonical_path}"
    return target


def _provider_targets_match(
    provider_name: str,
    stored_target: str,
    active_target: str,
    *,
    allow_legacy_site_match: bool,
) -> bool:
    """Return True when the stored target is compatible with the active target.

    ``allow_legacy_site_match`` permits a pre-project-key Jira mapping (stored as
    just the site base URL, without a project-key path segment) to match any
    project on that site. Callers must only set this when the mapping document
    has no entries yet, because a legacy target records no project identity at
    all: once any entry exists, an exact target match (including the
    project-key segment) is required so that pointing the active target at a
    *different* project on the same site cannot silently validate and reuse
    issues that actually belong to another project.
    """
    canonical_active_target = _canonicalize_provider_target(provider_name, active_target)
    try:
        canonical_stored_target = _canonicalize_provider_target(provider_name, stored_target)
    except ValueError:
        canonical_stored_target = stored_target
    if canonical_stored_target == canonical_active_target:
        if provider_name == "jira" and not allow_legacy_site_match:
            stored_path = urlsplit(stored_target.strip()).path
            active_path = urlsplit(canonical_active_target).path
            # A single path segment may be a legacy site context path rather
            # than a project key, so case-folding it can reuse the wrong mapping.
            if stored_path != active_path and stored_path.strip("/").count("/") == 0:
                return False
        return True
    if provider_name != "jira" or not allow_legacy_site_match:
        return False
    active_parts = canonical_active_target.rsplit("/", 1)
    try:
        canonical_stored_site = _canonicalize_provider_target("jira", stored_target, allow_jira_site_only=True)
    except ValueError:
        return False
    return canonical_stored_site == active_parts[0]


def resolve_tree_id(tree: EpicTree | dict[str, Any] | str) -> str:
    """Return a canonical lowercase UUID from a tree model or document."""
    if isinstance(tree, EpicTree):
        value: Any = tree.treeId
    elif isinstance(tree, dict):
        value = tree.get("treeId")
    else:
        value = tree
    if value is None:
        raise ValueError("Epic-tree document does not contain treeId")
    try:
        return str(UUID(str(value)))
    except (ValueError, AttributeError, TypeError) as exc:
        raise ValueError(f"Invalid treeId: {value!r}") from exc


def resolve_mapping_path(tree: EpicTree | dict[str, Any] | str, *, create: bool = True) -> Path:
    """Resolve the mapping file beneath the active workflow state directory."""
    tree_id = resolve_tree_id(tree)
    return state.get_state_dir(create=create) / f"epic-create-mapping-{tree_id}"


def initialize_mapping_document(
    tree: EpicTree | dict[str, Any] | str,
    provider_name: str,
    provider_target: str,
) -> dict[str, Any]:
    """Build an empty schema-v2 mapping document."""
    if not isinstance(provider_name, str) or not provider_name.strip():
        raise ValueError("provider_name must be non-empty")
    if not isinstance(provider_target, str) or not provider_target.strip():
        raise ValueError("provider_target must be non-empty")
    canonical_provider_name = provider_name.strip().casefold()
    return {
        "schemaVersion": "2.0",
        "treeId": resolve_tree_id(tree),
        "provider": {
            "name": canonical_provider_name,
            "target": _canonicalize_provider_target(canonical_provider_name, provider_target),
        },
        "entries": {},
    }


def validate_mapping_document(
    document: Any,
    tree: EpicTree | dict[str, Any] | str | None = None,
    provider_name: str | None = None,
    provider_target: str | None = None,
    *,
    allow_invalid_pending_timestamps: bool = False,
) -> dict[str, Any]:
    """Validate and return a mapping document, optionally against active identity.

    Recovery reads may allow invalid relationship timestamps and pending node
    timestamps; mapping writes use strict validation.
    """
    if not isinstance(document, dict):
        raise ValueError("Mapping document must be a JSON object")
    if document.get("schemaVersion") != "2.0":
        raise ValueError("Mapping document schemaVersion must be '2.0'")
    try:
        document_tree_id = resolve_tree_id(document)
    except ValueError as exc:
        raise ValueError("Mapping document has an invalid treeId") from exc
    if tree is not None and document_tree_id != resolve_tree_id(tree):
        raise ValueError("Mapping document treeId does not match the active tree")
    provider = document.get("provider")
    if (
        not isinstance(provider, dict)
        or not isinstance(provider.get("name"), str)
        or not provider["name"].strip()
        or not isinstance(provider.get("target"), str)
        or not provider["target"].strip()
    ):
        raise ValueError("Mapping document provider must contain non-empty name and target")
    canonical_provider_name = provider["name"].strip().casefold()
    if provider_name is not None and canonical_provider_name != provider_name.strip().casefold():
        raise ValueError("Mapping document provider name does not match the active provider")
    entries = document.get("entries")
    if not isinstance(entries, dict):
        raise ValueError("Mapping document entries must be an object")
    for key, entry in entries.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError("Mapping entry key must be a non-empty string")
        if not isinstance(entry, dict):
            raise ValueError(f"Mapping entry {key!r} must be an object")

        def validate_timestamp(field: str) -> None:
            value = entry.get(field)
            if not isinstance(value, str) or not value.endswith("Z"):
                raise ValueError(f"Mapping entry {key!r} {field} must be an ISO 8601 UTC timestamp ending in 'Z'")
            try:
                parsed = datetime.fromisoformat(value[:-1] + "+00:00")
                if parsed.tzinfo is None or parsed.utcoffset() is None:
                    raise ValueError("timestamp must be timezone-aware")
            except ValueError as exc:
                raise ValueError(
                    f"Mapping entry {key!r} {field} must be an ISO 8601 UTC timestamp ending in 'Z'"
                ) from exc

        def validate_pending_timestamp() -> None:
            try:
                validate_timestamp("pending_since")
            except ValueError:
                if not allow_invalid_pending_timestamps:
                    raise

        operation_type = (
            "link_subissue"
            if key.startswith("link_subissue:")
            else ("add_blocked_by" if key.startswith("add_blocked_by:") else None)
        )
        if operation_type is not None:
            status = entry.get("status")
            if status == "pending":
                expected_fields = {
                    "status",
                    "operation_type",
                    "source_ref",
                    "target_ref",
                    "source_provider_id",
                    "target_provider_id",
                    "pending_since",
                }
                if set(entry) != expected_fields and not (
                    allow_invalid_pending_timestamps and set(entry) == expected_fields - {"pending_since"}
                ):
                    raise ValueError(f"Mapping relationship entry {key!r} has an invalid pending shape")
                source_id = entry.get("source_provider_id")
                target_id = entry.get("target_provider_id")
                if not isinstance(source_id, str) or not source_id.strip():
                    raise ValueError(f"Mapping relationship entry {key!r} has an invalid source_provider_id")
                if not (
                    isinstance(target_id, str)
                    and target_id.strip()
                    or operation_type == "link_subissue"
                    and target_id is None
                ):
                    raise ValueError(f"Mapping relationship entry {key!r} has an invalid target_provider_id")
                validate_pending_timestamp()
            elif status == "confirmed":
                expected_fields = {
                    "status",
                    "operation_type",
                    "source_ref",
                    "target_ref",
                    "source_provider_id",
                    "target_provider_id",
                    "confirmed_at",
                    "result",
                }
                if set(entry) != expected_fields and not (
                    allow_invalid_pending_timestamps and set(entry) == expected_fields - {"confirmed_at"}
                ):
                    raise ValueError(f"Mapping relationship entry {key!r} has an invalid confirmed shape")
                for identifier_field in ("source_provider_id", "target_provider_id"):
                    identifier = entry.get(identifier_field)
                    if not isinstance(identifier, str) or not identifier.strip():
                        raise ValueError(f"Mapping relationship entry {key!r} has an invalid {identifier_field}")
                result = entry.get("result")
                if not isinstance(result, str) or result not in {"linked", "already-linked"}:
                    raise ValueError(f"Mapping relationship entry {key!r} has an invalid result")
                try:
                    validate_timestamp("confirmed_at")
                except ValueError:
                    if not allow_invalid_pending_timestamps:
                        raise
            else:
                raise ValueError(f"Mapping relationship entry {key!r} has an invalid status")

            source_ref = entry.get("source_ref")
            target_ref = entry.get("target_ref")
            if (
                entry.get("operation_type") != operation_type
                or not isinstance(source_ref, str)
                or not source_ref.strip()
                or not isinstance(target_ref, str)
                or not target_ref.strip()
                or key != f"{operation_type}:{source_ref}:{target_ref}"
            ):
                raise ValueError(f"Mapping relationship entry {key!r} has a noncanonical key or refs")
        else:
            if ":" in key:
                raise ValueError(f"Mapping node entry key {key!r} is invalid")
            status = entry.get("status")
            if status == "pending":
                if set(entry) in (
                    {"status", "pending_since"},
                    {"status"} if allow_invalid_pending_timestamps else set(),
                ):
                    validate_pending_timestamp()
                elif set(entry) in (
                    {"status", "pending_since", "provider_id", "call_outcome"},
                    {"status", "provider_id", "call_outcome"} if allow_invalid_pending_timestamps else set(),
                ):
                    provider_id = entry.get("provider_id")
                    if not isinstance(provider_id, str) or not provider_id.strip():
                        raise ValueError(f"Mapping node entry {key!r} has an invalid provider_id")
                    call_outcome = entry.get("call_outcome")
                    if not isinstance(call_outcome, str) or call_outcome not in {"created", "existing"}:
                        raise ValueError(f"Mapping node entry {key!r} has an invalid call_outcome")
                    validate_pending_timestamp()
                else:
                    raise ValueError(f"Mapping node entry {key!r} has an invalid pending shape")
            elif status == "created":
                if set(entry) != {"status", "provider_id"}:
                    raise ValueError(f"Mapping node entry {key!r} has an invalid created shape")
                provider_id = entry.get("provider_id")
                if not isinstance(provider_id, str) or not provider_id.strip():
                    raise ValueError(f"Mapping node entry {key!r} has an invalid provider_id")
            elif status == "trusted-match":
                if set(entry) != {"status", "provider_id", "match_basis"}:
                    raise ValueError(f"Mapping node entry {key!r} has an invalid trusted-match shape")
                provider_id = entry.get("provider_id")
                if not isinstance(provider_id, str) or not provider_id.strip():
                    raise ValueError(f"Mapping node entry {key!r} has an invalid provider_id")
                match_basis = entry.get("match_basis")
                if not isinstance(match_basis, str) or match_basis not in {
                    "pre-create-guard",
                    "import-legacy-mapping",
                    "create-existing-response",
                    "pending-confirmation-unresolved",
                }:
                    raise ValueError(f"Mapping node entry {key!r} has an invalid match_basis")
            elif status == "failed":
                error = entry.get("error")
                if set(entry) != {"status", "error"} or not isinstance(error, str) or not error.strip():
                    raise ValueError(f"Mapping node entry {key!r} has an invalid failed shape")
            else:
                raise ValueError(f"Mapping node entry {key!r} has an invalid status")
    if provider_target is not None:
        canonical_target = _canonicalize_provider_target(canonical_provider_name, provider_target)
        if not _provider_targets_match(
            canonical_provider_name, provider["target"], provider_target, allow_legacy_site_match=not entries
        ):
            raise ValueError("Mapping document provider target does not match the active target")
        provider["target"] = canonical_target
    return document


def load_mapping_document(path: Path | str) -> dict[str, Any]:
    """Load and recover an existing mapping document for reconciliation."""
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_mapping_document(document, allow_invalid_pending_timestamps=True)

    def has_valid_timestamp(value: Any) -> bool:
        if not isinstance(value, str) or not value.endswith("Z"):
            return False
        try:
            parsed = datetime.fromisoformat(value[:-1] + "+00:00")
        except ValueError:
            return False
        return parsed.tzinfo is not None and parsed.utcoffset() is not None

    entries = document["entries"]
    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    for key, entry in entries.items():
        if key.startswith(("link_subissue:", "add_blocked_by:")):
            if entry["status"] == "pending" and not has_valid_timestamp(entry.get("pending_since")):
                entry["pending_since"] = now
            elif entry["status"] == "confirmed" and not has_valid_timestamp(entry.get("confirmed_at")):
                entry["status"] = "pending"
                entry["pending_since"] = now
                entry.pop("confirmed_at", None)
                entry.pop("result")

    return validate_mapping_document(document, allow_invalid_pending_timestamps=True)


def atomic_write_mapping_document(path: Path | str, document: dict[str, Any]) -> None:
    """Write a valid mapping document using temp-file plus replace semantics."""
    validate_mapping_document(document)
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as temporary:
            json.dump(document, temporary, ensure_ascii=False, indent=2, sort_keys=True)
            temporary.write("\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_name, destination)
    except Exception:
        try:
            os.unlink(temporary_name)
        except OSError:
            pass
        raise
