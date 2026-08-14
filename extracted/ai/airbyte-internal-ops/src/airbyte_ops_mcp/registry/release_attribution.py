# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Resolve connector release attribution from Git history, registry data, and docs."""

from __future__ import annotations

import json
import logging
import re
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import IO, Any, Callable, Literal, Protocol

import gcsfs
import requests
import yaml
from packaging.version import InvalidVersion, Version
from pydantic import BaseModel

from airbyte_ops_mcp.airbyte_repo.changelog_parser import parse_changelog_entries
from airbyte_ops_mcp.github_api import resolve_default_github_token
from airbyte_ops_mcp.registry._constants import DOC_FILE_NAME, METADATA_FOLDER
from airbyte_ops_mcp.registry._gcs_helpers import get_gcs_credentials_token
from airbyte_ops_mcp.registry.store import RegistryStore

logger = logging.getLogger(__name__)

_COMMIT_SEPARATOR = "\x01"
_PR_NUMBER_RE = re.compile(r"\(#(\d+)\)\s*$")
_NOREPLY_RE = re.compile(
    r"^(?P<id>\d+)\+(?P<login>[^@]+)@users\.noreply\.github\.com$",
    re.IGNORECASE,
)
_BOT_RE = re.compile(r"\[bot\]$", re.IGNORECASE)
_METADATA_PATH_RE = re.compile(
    r"^airbyte-integrations/connectors/(?P<connector>[^/]+)/metadata\.yaml$"
)
_VERSION_LINE_RE = re.compile(r"^\+\s*dockerImageTag:\s*[\"']?(?P<version>[^\"'\s#]+)")
_GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
_GITHUB_REPO_OWNER = "airbytehq"
_GITHUB_REPO_NAME = "airbyte"
_GITHUB_REPO = f"{_GITHUB_REPO_OWNER}/{_GITHUB_REPO_NAME}"


class ReleaseAttribution(BaseModel):
    """Attribution metadata for one published connector version."""

    pr_number: int | None = None
    pr_url: str | None = None
    pr_author_id: int | None = None
    pr_author_login: str | None = None
    pr_author_type: Literal["User", "Bot"] | None = None
    attributed_to: str | None = None
    merge_commit_sha: str | None = None
    merged_at: datetime | None = None
    source: Literal["publish", "git-backfill", "prerelease", "changelog"]


class ReleaseAttributionSummary(BaseModel):
    """Summary statistics for a release attribution index."""

    connectors: int
    versions: int
    versions_with_pr: int
    versions_with_author_login: int
    duplicate_versions_collapsed: int

    @property
    def pr_percentage(self) -> float:
        """Return the percentage of versions with a PR number."""
        return _percentage(self.versions_with_pr, self.versions)

    @property
    def author_login_percentage(self) -> float:
        """Return the percentage of versions with an author login."""
        return _percentage(self.versions_with_author_login, self.versions)


class ReleaseAttributionIndex(BaseModel):
    """Connector/version release attribution index."""

    connectors: dict[str, dict[str, ReleaseAttribution]]
    summary: ReleaseAttributionSummary


class ReleaseAttributionLookupResult(BaseModel):
    """Result of resolving attribution for one connector version."""

    connector_name: str
    version: str
    status: Literal["found", "unattributed", "not_found", "error"]
    lookup_path: Literal["index", "metadata", "changelog", "none"]
    attribution: ReleaseAttribution | None = None
    error: str | None = None


class ReleaseAttributionListResult(BaseModel):
    """Attribution lookup results for one connector's versions."""

    connector_name: str
    items: list[ReleaseAttributionLookupResult]
    error: str | None = None


class _ReadableRegistryFileSystem(Protocol):
    """Minimal filesystem interface needed for attribution lookups."""

    def open(self, path: str, mode: str = "r") -> Any:
        """Open a registry object for reading."""


@dataclass
class _LookupContext:
    """Shared inputs and index-derived state for an attribution tier."""

    filesystem: _ReadableRegistryFileSystem
    store: RegistryStore
    connector: str
    version: str
    latest_version: str | None
    entry: dict[str, Any] | None

    @property
    def entry_exists(self) -> bool:
        """Return whether the requested version exists in the index."""
        return self.entry is not None


_LookupResolver = Callable[[_LookupContext], ReleaseAttributionLookupResult | None]


def _version_sort_key(version: str) -> tuple[int, Version | str]:
    """Sort valid semantic versions before malformed version strings."""
    try:
        return (1, Version(version))
    except InvalidVersion:
        return (0, version)


def _metadata_path(store: RegistryStore, connector: str, version: str) -> str:
    return f"{store.bucket_root}/{METADATA_FOLDER}/airbyte/{connector}/{version}/metadata.yaml"


def _index_path(store: RegistryStore, connector: str) -> str:
    return f"{store.bucket_root}/{METADATA_FOLDER}/airbyte/{connector}/versions.json"


def _doc_path(store: RegistryStore, connector: str, version: str) -> str:
    return f"{store.bucket_root}/{METADATA_FOLDER}/airbyte/{connector}/{version}/{DOC_FILE_NAME}"


def _lookup_from_release(
    *,
    connector: str,
    version: str,
    release: Any,
    lookup_path: Literal["index", "metadata"],
) -> ReleaseAttributionLookupResult:
    if not isinstance(release, dict):
        return ReleaseAttributionLookupResult(
            connector_name=connector,
            version=version,
            status="error",
            lookup_path=lookup_path,
            error="Release attribution is not an object.",
        )
    try:
        attribution = ReleaseAttribution.model_validate(release)
    except Exception as exc:
        return ReleaseAttributionLookupResult(
            connector_name=connector,
            version=version,
            status="error",
            lookup_path=lookup_path,
            error=f"Invalid release attribution: {exc}",
        )
    return ReleaseAttributionLookupResult(
        connector_name=connector,
        version=version,
        status="found",
        lookup_path=lookup_path,
        attribution=attribution,
    )


def _lookup_metadata(
    fs: _ReadableRegistryFileSystem,
    store: RegistryStore,
    connector: str,
    version: str,
) -> ReleaseAttributionLookupResult:
    try:
        with fs.open(_metadata_path(store, connector, version), "r") as handle:
            raw = yaml.safe_load(handle)
    except FileNotFoundError:
        return ReleaseAttributionLookupResult(
            connector_name=connector,
            version=version,
            status="not_found",
            lookup_path="none",
        )
    except Exception as exc:
        logger.warning(
            "Failed to read release metadata for %s@%s: %s",
            connector,
            version,
            exc,
        )
        return ReleaseAttributionLookupResult(
            connector_name=connector,
            version=version,
            status="error",
            lookup_path="metadata",
            error=str(exc),
        )

    if not isinstance(raw, dict) or not isinstance(raw.get("data"), dict):
        return ReleaseAttributionLookupResult(
            connector_name=connector,
            version=version,
            status="error",
            lookup_path="metadata",
            error="Metadata is not a mapping.",
        )
    generated = raw["data"].get("generated")
    release = generated.get("release") if isinstance(generated, dict) else None
    if release is None:
        return ReleaseAttributionLookupResult(
            connector_name=connector,
            version=version,
            status="unattributed",
            lookup_path="metadata",
        )
    return _lookup_from_release(
        connector=connector,
        version=version,
        release=release,
        lookup_path="metadata",
    )


def _changelog_attribution(
    *,
    connector: str,
    version: str,
    content: str,
) -> ReleaseAttributionLookupResult:
    entries = parse_changelog_entries(
        content,
        _GITHUB_REPO,
        allow_prerelease=True,
        allow_pr_cell_text=True,
    )
    if not entries:
        logger.warning("Could not parse a changelog table from registry doc.md")
    for _line, entry_version, date_str, _displayed_pr, pr_number, _full_line in entries:
        if entry_version != version:
            continue
        merged_at = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        attribution = ReleaseAttribution(
            pr_number=pr_number,
            pr_url=f"https://github.com/{_GITHUB_REPO}/pull/{pr_number}",
            merged_at=merged_at,
            source="changelog",
        )
        return ReleaseAttributionLookupResult(
            connector_name=connector,
            version=version,
            status="found",
            lookup_path="changelog",
            attribution=_enrich_changelog_record(attribution),
        )
    return ReleaseAttributionLookupResult(
        connector_name=connector,
        version=version,
        status="unattributed",
        lookup_path="changelog",
    )


def _enrich_changelog_record(record: ReleaseAttribution) -> ReleaseAttribution:
    """Best-effort enrich a changelog PR using the shared GraphQL path."""
    token = resolve_default_github_token(allow_none=True)
    if not token or record.pr_number is None:
        if not token:
            logger.warning(
                "No GitHub token available to enrich changelog PR %s", record.pr_number
            )
        return record
    try:
        data = _fetch_pr_data([record.pr_number], token=token)
        pull_request = data.get(record.pr_number)
        return _apply_pr_data(record, pull_request) if pull_request else record
    except Exception as exc:
        logger.warning(
            "Failed to enrich changelog PR %s; using changelog attribution: %s",
            record.pr_number,
            exc,
        )
        return record


def _resolve_index_tier(
    context: _LookupContext,
) -> ReleaseAttributionLookupResult | None:
    if context.entry is None or "release" not in context.entry:
        return None
    return _lookup_from_release(
        connector=context.connector,
        version=context.version,
        release=context.entry["release"],
        lookup_path="index",
    )


def _resolve_metadata_tier(
    context: _LookupContext,
) -> ReleaseAttributionLookupResult:
    return _lookup_metadata(
        context.filesystem,
        context.store,
        context.connector,
        context.version,
    )


def _resolve_changelog_tier(
    context: _LookupContext,
) -> ReleaseAttributionLookupResult | None:
    if context.latest_version is None:
        return None
    try:
        with context.filesystem.open(
            _doc_path(context.store, context.connector, context.latest_version), "r"
        ) as handle:
            return _changelog_attribution(
                connector=context.connector,
                version=context.version,
                content=handle.read(),
            )
    except FileNotFoundError:
        logger.warning(
            "Changelog doc.md not found for %s@%s; attribution remains unresolved",
            context.connector,
            context.latest_version,
        )
    except Exception as exc:
        logger.warning(
            "Failed to read changelog for %s from %s: %s",
            context.connector,
            context.latest_version,
            exc,
        )
    return None


_LOOKUP_RESOLVERS: tuple[_LookupResolver, ...] = (
    _resolve_index_tier,
    _resolve_metadata_tier,
    _resolve_changelog_tier,
)


def _fetch_pr_data(
    pr_numbers: list[int],
    *,
    token: str,
    batch_size: int = 100,
) -> dict[int, dict[str, Any]]:
    pr_data: dict[int, dict[str, Any]] = {}
    for start in range(0, len(pr_numbers), batch_size):
        data = _request_graphql(
            _graphql_query(pr_numbers[start : start + batch_size]), token
        )
        for key, value in data.items():
            if key.startswith("pr_") and isinstance(value, dict):
                pr_data[int(key[3:])] = value
    return pr_data


def _apply_pr_data(
    record: ReleaseAttribution,
    pull_request: dict[str, Any] | None,
) -> ReleaseAttribution:
    if not pull_request:
        return record
    author = pull_request.get("author")
    author_id = author.get("databaseId") if isinstance(author, dict) else None
    author_login = author.get("login") if isinstance(author, dict) else None
    raw_author_type = author.get("__typename") if isinstance(author, dict) else None
    author_type: Literal["User", "Bot"] | None = (
        raw_author_type if raw_author_type in {"User", "Bot"} else None
    )
    updates: dict[str, Any] = {}
    if pull_request.get("url"):
        updates["pr_url"] = pull_request["url"]
    if isinstance(author_id, int):
        updates["pr_author_id"] = author_id
    if isinstance(author_login, str):
        updates["pr_author_login"] = author_login
    if author_type is not None:
        updates["pr_author_type"] = author_type
        updates["attributed_to"] = _attributed_to(author_type, author_login)
    merge_commit = pull_request.get("mergeCommit")
    if isinstance(merge_commit, dict) and merge_commit.get("oid"):
        updates["merge_commit_sha"] = merge_commit["oid"]
    if isinstance(pull_request.get("mergedAt"), str):
        updates["merged_at"] = datetime.fromisoformat(
            pull_request["mergedAt"]
        ).astimezone(timezone.utc)
    return record.model_copy(update=updates)


def _make_registry_fs() -> gcsfs.GCSFileSystem:
    return gcsfs.GCSFileSystem(token=get_gcs_credentials_token())


def _read_version_index(
    fs: _ReadableRegistryFileSystem,
    store: RegistryStore,
    connector: str,
) -> tuple[dict[str, Any] | None, str | None]:
    try:
        with fs.open(_index_path(store, connector), "r") as handle:
            raw = json.load(handle)
    except FileNotFoundError:
        return None, None
    except Exception as exc:
        logger.warning(
            "Failed to read release attribution index for %s: %s",
            connector,
            exc,
        )
        return None, str(exc)
    if not isinstance(raw, dict):
        logger.warning(
            "Release attribution index for %s is not a JSON object.",
            connector,
        )
        return None, "Release attribution index is not a JSON object."
    if not isinstance(raw.get("versions"), list):
        logger.warning(
            "Release attribution index for %s is missing a `versions` list.",
            connector,
        )
        return None, "Release attribution index is missing a `versions` list."
    return raw, None


def lookup_release_attribution(
    store: RegistryStore,
    connector: str,
    version: str,
    *,
    fs: _ReadableRegistryFileSystem | None = None,
) -> ReleaseAttributionLookupResult:
    """Resolve release attribution from the index, metadata, then `doc.md`.

    The changelog fallback reads the latest published `doc.md` copy and is
    read-only; it never writes changelog-derived attribution into the index.
    The result distinguishes a found record, a successfully read but
    unattributed version, a missing version, and a lookup error.
    """
    filesystem = fs or _make_registry_fs()
    index, _ = _read_version_index(filesystem, store, connector)
    latest_version: str | None = version if index is None else None
    entry: dict[str, Any] | None = None
    if index is not None:
        entries = index.get("versions", [])
        version_entries = [
            item
            for item in entries
            if isinstance(item, dict) and isinstance(item.get("version"), str)
        ]
        latest_version = max(
            (item["version"] for item in version_entries),
            key=_version_sort_key,
            default=None,
        )
        entry = next(
            (
                item
                for item in entries
                if isinstance(item, dict) and item.get("version") == version
            ),
            None,
        )

    context = _LookupContext(
        filesystem=filesystem,
        store=store,
        connector=connector,
        version=version,
        latest_version=latest_version,
        entry=entry,
    )
    last_result: ReleaseAttributionLookupResult | None = None
    for resolver in _LOOKUP_RESOLVERS:
        result = resolver(context)
        if result is None:
            continue
        last_result = result
        if result.status in {"found", "error"}:
            return result

    if last_result is None:
        return ReleaseAttributionLookupResult(
            connector_name=connector,
            version=version,
            status="not_found",
            lookup_path="none",
        )
    if last_result.status == "unattributed" and not context.entry_exists:
        return last_result.model_copy(update={"status": "not_found"})
    return last_result


def list_release_attribution(
    store: RegistryStore,
    connector: str,
    *,
    limit: int = 50,
    with_metadata_fallback: bool = False,
    fs: _ReadableRegistryFileSystem | None = None,
) -> ReleaseAttributionListResult:
    """List release attribution for a connector's versions, newest first.

    Metadata fallback is disabled by default to avoid one GCS read per
    unattributed version in a single listing request.
    """
    if limit < 1:
        raise ValueError("limit must be at least 1")
    filesystem = fs or _make_registry_fs()
    index, index_error = _read_version_index(filesystem, store, connector)
    if index is None:
        return ReleaseAttributionListResult(
            connector_name=connector,
            items=[],
            error=index_error or "Release attribution index was not found.",
        )

    entries = [
        entry
        for entry in index["versions"]
        if isinstance(entry, dict) and isinstance(entry.get("version"), str)
    ]
    entries.sort(key=lambda entry: _version_sort_key(entry["version"]), reverse=True)
    items: list[ReleaseAttributionLookupResult] = []
    for entry in entries[:limit]:
        version = entry["version"]
        if "release" in entry:
            result = _lookup_from_release(
                connector=connector,
                version=version,
                release=entry["release"],
                lookup_path="index",
            )
            items.append(result)
            continue
        if with_metadata_fallback:
            items.append(_lookup_metadata(filesystem, store, connector, version))
        else:
            items.append(
                ReleaseAttributionLookupResult(
                    connector_name=connector,
                    version=version,
                    status="unattributed",
                    lookup_path="index",
                )
            )
    if with_metadata_fallback:
        unresolved = {
            item.version
            for item in items
            if item.status in {"unattributed", "not_found"}
        }
        if unresolved:
            latest_version = entries[0]["version"]
            try:
                with filesystem.open(
                    _doc_path(store, connector, latest_version), "r"
                ) as handle:
                    content = handle.read()
                changelog = {
                    entry_version: _changelog_attribution(
                        connector=connector,
                        version=entry_version,
                        content=content,
                    )
                    for entry_version in unresolved
                }
                items = [
                    changelog.get(item.version, item)
                    if item.status in {"unattributed", "not_found"}
                    else item
                    for item in items
                ]
            except FileNotFoundError:
                logger.warning(
                    "Changelog doc.md not found for %s@%s; attribution remains unresolved",
                    connector,
                    latest_version,
                )
            except Exception as exc:
                logger.warning(
                    "Failed to read changelog for %s from %s: %s",
                    connector,
                    latest_version,
                    exc,
                )
    return ReleaseAttributionListResult(connector_name=connector, items=items)


def _percentage(numerator: int, denominator: int) -> float:
    return round(numerator * 100 / denominator, 2) if denominator else 0.0


def extract_pr_number(subject: str) -> int | None:
    """Extract a trailing pull request number from a commit subject."""
    match = _PR_NUMBER_RE.search(subject.strip())
    return int(match.group(1)) if match else None


def derive_git_author(
    name: str,
    email: str,
) -> tuple[int | None, str | None, Literal["User", "Bot"] | None]:
    """Derive GitHub author identity fields without making a network request."""
    noreply_match = _NOREPLY_RE.match(email.strip())
    login = noreply_match.group("login") if noreply_match else None
    author_id = int(noreply_match.group("id")) if noreply_match else None
    bot = bool(_BOT_RE.search(login or "") or _BOT_RE.search(name.strip()))
    author_type: Literal["User", "Bot"] | None = "Bot" if bot else None
    if login and not bot:
        author_type = "User"
    return author_id, login, author_type


def _attributed_to(
    author_type: Literal["User", "Bot"] | None,
    author_login: str | None,
) -> str | None:
    return author_login if author_type == "User" else None


def _build_record(
    *,
    sha: str,
    author_name: str,
    author_email: str,
    committed_at: str,
    subject: str,
    source: Literal["publish", "git-backfill", "prerelease"],
    pr_number_override: int | None = None,
    is_prerelease: bool = False,
) -> ReleaseAttribution:
    """Build a record using the committer date as the merge time.

    The committer date is deliberate: `%cI` records when GitHub merged the
    squash commit, whereas `%aI` records when the contributor originally wrote it.
    """
    author_id, author_login, author_type = derive_git_author(author_name, author_email)
    merged_at = (
        None
        if is_prerelease
        else datetime.fromisoformat(committed_at).astimezone(timezone.utc)
    )
    pr_number = (
        pr_number_override
        if pr_number_override is not None
        else extract_pr_number(subject)
    )
    return ReleaseAttribution(
        pr_number=pr_number,
        pr_url=(
            f"https://github.com/{_GITHUB_REPO_OWNER}/{_GITHUB_REPO_NAME}/pull/{pr_number}"
            if pr_number
            else None
        ),
        pr_author_id=author_id,
        pr_author_login=author_login,
        pr_author_type=author_type,
        attributed_to=_attributed_to(author_type, author_login),
        merge_commit_sha=None if is_prerelease else sha,
        merged_at=merged_at,
        source=source,
    )


def _git_command(repo_path: Path, *args: str) -> subprocess.Popen[str]:
    return subprocess.Popen(
        ["git", "-C", str(repo_path), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _ensure_full_clone(repo_path: Path) -> None:
    """Raise when `repo_path` is a shallow Git checkout."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "rev-parse", "--is-shallow-repository"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise ValueError(
            f"Could not verify Git repository {repo_path}; "
            "provide a valid full Git clone."
        ) from exc
    if result.stdout.strip().lower() == "true":
        raise ValueError(
            f"Git repository {repo_path} is shallow; a full clone is required "
            "for release attribution backfill."
        )


def build_release_attribution(
    repo_path: Path,
    metadata_path: Path,
    *,
    pr_number: int | None = None,
    is_prerelease: bool = False,
) -> ReleaseAttribution:
    """Build attribution for the last commit touching one metadata file."""
    relative_path = metadata_path.resolve().relative_to(repo_path.resolve())
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(repo_path),
                "log",
                "-1",
                "--format=%H%x1f%an%x1f%ae%x1f%cI%x1f%s",
                "--",
                str(relative_path),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise ValueError(
            f"Could not read Git history for {metadata_path}; "
            "provide a valid Git repository and metadata path."
        ) from exc
    header = result.stdout.rstrip("\n")
    if not header:
        raise ValueError(f"No Git history found for {metadata_path}")
    sha, name, email, committed_at, subject = header.split("\x1f", 4)
    return _build_record(
        sha=sha,
        author_name=name,
        author_email=email,
        committed_at=committed_at,
        subject=subject,
        source="prerelease" if is_prerelease else "publish",
        pr_number_override=pr_number,
        is_prerelease=is_prerelease,
    )


def _parse_commit_header(line: str) -> tuple[str, str, str, str, str] | None:
    if not line.startswith(_COMMIT_SEPARATOR):
        return None
    fields = line[1:].rstrip("\n").split("\x1f", 4)
    if len(fields) != 5:
        return None
    return fields[0], fields[1], fields[2], fields[3], fields[4]


def _iter_version_records(
    output: IO[str],
) -> list[tuple[str, str, ReleaseAttribution]]:
    """Parse version bumps from a streamed `git log` output."""
    records: list[tuple[str, str, ReleaseAttribution]] = []
    current: ReleaseAttribution | None = None
    current_connector: str | None = None
    for line in output:
        header = _parse_commit_header(line)
        if header:
            sha, name, email, committed_at, subject = header
            current = _build_record(
                sha=sha,
                author_name=name,
                author_email=email,
                committed_at=committed_at,
                subject=subject,
                source="git-backfill",
            )
            current_connector = None
            continue
        path_match = re.match(r"\+\+\+ b/(.*)", line.rstrip("\n"))
        if path_match:
            metadata_match = _METADATA_PATH_RE.match(path_match.group(1))
            current_connector = (
                metadata_match.group("connector") if metadata_match else None
            )
            continue
        if current and current_connector:
            version_match = _VERSION_LINE_RE.match(line.rstrip("\n"))
            if version_match:
                records.append(
                    (current_connector, version_match.group("version"), current)
                )
    return records


def scan_release_attribution(
    repo_path: Path,
    *,
    connector: str | None = None,
) -> ReleaseAttributionIndex:
    """Scan connector metadata history in one streamed Git subprocess."""
    _ensure_full_clone(repo_path)
    pathspec = (
        f"airbyte-integrations/connectors/{connector}/metadata.yaml"
        if connector
        else "airbyte-integrations/connectors/*/metadata.yaml"
    )
    process = _git_command(
        repo_path,
        "log",
        "--format=\x01%H\x1f%an\x1f%ae\x1f%cI\x1f%s",
        "-p",
        "-U0",
        "--",
        pathspec,
    )
    if process.stdout is None:
        raise RuntimeError("Git scan did not provide a stdout stream")
    records = _iter_version_records(process.stdout)
    return_code = process.wait()
    if return_code:
        raise ValueError(f"Could not scan Git history (exit code {return_code})")

    index: dict[str, dict[str, ReleaseAttribution]] = {}
    duplicate_count = 0
    for connector_name, version, record in records:
        connector_versions = index.setdefault(connector_name, {})
        if version in connector_versions:
            duplicate_count += 1
            logger.debug(
                "Superseded attribution for %s@%s: %s replaced by %s",
                connector_name,
                version,
                connector_versions[version].merge_commit_sha,
                record.merge_commit_sha,
            )
            continue
        connector_versions[version] = record

    summary = ReleaseAttributionSummary(
        connectors=len(index),
        versions=sum(len(versions) for versions in index.values()),
        versions_with_pr=sum(
            record.pr_number is not None
            for versions in index.values()
            for record in versions.values()
        ),
        versions_with_author_login=sum(
            record.pr_author_login is not None
            for versions in index.values()
            for record in versions.values()
        ),
        duplicate_versions_collapsed=duplicate_count,
    )
    return ReleaseAttributionIndex(connectors=index, summary=summary)


def _graphql_query(pr_numbers: list[int]) -> str:
    fields = "\n".join(
        f"pr_{number}: pullRequest(number: {number}) {{ "
        "url author { login __typename ... on User { databaseId } "
        "... on Bot { databaseId } } mergedAt mergeCommit { oid } "
        "}"
        for number in pr_numbers
    )
    return (
        f'query {{ repository(owner: "{_GITHUB_REPO_OWNER}", '
        f'name: "{_GITHUB_REPO_NAME}") {{{fields}}} }}'
    )


def _request_graphql(
    query: str,
    token: str,
    *,
    retries: int = 4,
) -> dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    for attempt in range(retries):
        try:
            response = requests.post(
                _GITHUB_GRAPHQL_URL,
                headers=headers,
                json={"query": query},
                timeout=30,
            )
        except requests.RequestException as exc:
            if attempt == retries - 1:
                raise ValueError(
                    "GitHub GraphQL request failed after retries."
                ) from exc
            time.sleep(min(2**attempt, 30))
            continue
        if response.status_code not in {403, 429}:
            response.raise_for_status()
            payload: dict[str, Any] = response.json()
            data = payload.get("data", {})
            repository = data.get("repository") if isinstance(data, dict) else None
            errors = payload.get("errors")
            if errors:
                error_items = errors if isinstance(errors, list) else [errors]
                failed_aliases = [
                    str(error.get("path", [])[-1])
                    for error in error_items
                    if isinstance(error, dict)
                    and isinstance(error.get("path"), list)
                    and error.get("path")
                ]
                logger.warning(
                    "GitHub GraphQL returned partial errors for aliases: %s",
                    failed_aliases or error_items,
                )
            if isinstance(repository, dict) and repository:
                return repository
            raise ValueError("GitHub GraphQL query returned no repository data")
        if attempt == retries - 1:
            response.raise_for_status()
        retry_after = response.headers.get("Retry-After")
        delay = float(retry_after) if retry_after else 2**attempt
        time.sleep(min(delay, 30))
    raise AssertionError("unreachable")


def enrich_release_attribution(
    index: ReleaseAttributionIndex,
    *,
    token: str | None = None,
    batch_size: int = 100,
) -> ReleaseAttributionIndex:
    """Enrich records with PR metadata using batched GitHub GraphQL requests."""
    token = token or resolve_default_github_token()
    pr_numbers = sorted(
        {
            record.pr_number
            for versions in index.connectors.values()
            for record in versions.values()
            if record.pr_number is not None
        }
    )
    pr_data = _fetch_pr_data(pr_numbers, token=token, batch_size=batch_size)

    for versions in index.connectors.values():
        for version, record in versions.items():
            if record.pr_number is None or record.pr_number not in pr_data:
                continue
            versions[version] = _apply_pr_data(record, pr_data[record.pr_number])
    index.summary.versions_with_author_login = sum(
        record.pr_author_login is not None
        for versions in index.connectors.values()
        for record in versions.values()
    )
    return index


def write_release_attribution_index(
    index: ReleaseAttributionIndex,
    output_path: Path,
) -> None:
    """Write an attribution index as indented JSON with UTC timestamps."""
    output_path.write_text(
        json.dumps(index.model_dump(mode="json"), indent=2, sort_keys=True) + "\n"
    )


def read_release_attribution_index(path: Path) -> ReleaseAttributionIndex:
    """Read an attribution index written by `write_release_attribution_index`."""
    return ReleaseAttributionIndex.model_validate_json(path.read_text())
