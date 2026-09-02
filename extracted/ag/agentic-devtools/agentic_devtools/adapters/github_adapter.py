"""GitHub Issues adapter using the ``gh`` CLI via subprocess.

Wraps ``gh issue`` commands and parses their JSON output into the shared
adapter TypedDicts defined in :mod:`agentic_devtools.adapters.base`.
"""

from __future__ import annotations

import json
import subprocess
import time
from collections.abc import Callable, Mapping
from typing import Any

import yaml

from agentic_devtools.adapters.base import (
    Comment,
    CommentResult,
    IssueAdapter,
    IssueDetailWithRaw,
    IssueFilters,
    IssueResult,
    IssueSummary,
    IssueTypeInfo,
    NormalizedIssue,
    PropertySchema,
)
from agentic_devtools.adapters.github_schema import (
    DESCRIPTION_MAP,
    WELL_KNOWN_LABELS,
    canonicalize,
    copy_default_properties,
    parse_form_fields,
    slugify,
)
from agentic_devtools.cli.subprocess_utils import run_safe


class GitHubIssuesAdapter(IssueAdapter):
    """Issue adapter backed by the ``gh`` CLI for GitHub Issues."""

    def __init__(
        self,
        repo: str,
        run_command: Callable[..., subprocess.CompletedProcess] | None = None,
    ) -> None:
        self._repo = repo
        self._run: Callable[..., subprocess.CompletedProcess] = run_command or run_safe
        self._labels_cache: list[str] | None = None
        self._forms_cache: dict[str, dict[str, Any]] | None = None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _exec(self, args: list[str], timeout: float | None = None) -> subprocess.CompletedProcess:
        """Run a ``gh`` command and raise on failure.

        Args:
            args: Command arguments to execute.
            timeout: Optional wall-clock timeout in seconds. Non-positive
                values raise ``RuntimeError`` immediately.
        """
        if timeout is not None and timeout <= 0:
            raise RuntimeError(f"Timeout must be positive, got {timeout}")
        try:
            run_kwargs: dict[str, object] = {"capture_output": True, "text": True, "shell": False}
            if timeout is not None:
                run_kwargs["timeout"] = timeout
            result = self._run(args, **run_kwargs)
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"gh command timed out after {exc.timeout}s") from exc
        if result.returncode != 0:
            raise RuntimeError(f"gh command failed: {result.stderr}")
        return result

    def _parse_json(self, stdout: str) -> object:
        """Parse JSON from *stdout*, raising on failure."""
        try:
            return json.loads(stdout)
        except (json.JSONDecodeError, TypeError) as exc:
            raise RuntimeError(f"Failed to parse gh output: {exc}") from exc

    @staticmethod
    def _coerce_str(value: object) -> str:
        """Coerce *value* to ``str``, treating ``None`` as ``""``."""
        return str(value) if value is not None else ""

    # ------------------------------------------------------------------
    # IssueAdapter interface
    # ------------------------------------------------------------------

    def _repo_args(self) -> list[str]:
        """Return ``['--repo', slug]`` when a repo is configured, else ``[]``."""
        return ["--repo", self._repo] if self._repo else []

    def create_issue(self, title: str, description: str, labels: list[str] | None = None) -> IssueResult:
        """Create a GitHub issue via ``gh issue create``."""
        args = ["gh", "issue", "create", *self._repo_args(), "--title", title, "--body", description]
        for label in labels or []:
            args += ["--label", label]
        result = self._exec(args)
        url = result.stdout.strip()
        issue_id = url.rstrip("/").rsplit("/", 1)[-1] if url else ""
        return IssueResult(issue_id=issue_id, url=url)

    def get_issue(self, issue_id: str) -> IssueDetailWithRaw:
        """Fetch a GitHub issue via ``gh issue view``.

        Returns an :class:`IssueDetailWithRaw` that includes the standard
        fields plus a ``raw`` dict preserving selected GitHub response fields
        such as ``createdAt``, ``updatedAt``, and ``assignees``.
        """
        args = [
            "gh",
            "issue",
            "view",
            issue_id,
            *self._repo_args(),
            "--json",
            "number,title,body,state,labels,url,comments,createdAt,updatedAt,assignees",
        ]
        result = self._exec(args)
        data = self._parse_json(result.stdout)
        if not isinstance(data, dict):
            raise RuntimeError(f"Failed to parse gh output: expected dict, got {type(data).__name__}")

        raw_labels = data.get("labels")
        if not isinstance(raw_labels, list):
            raw_labels = []
        label_names = [lb["name"] if isinstance(lb, dict) else str(lb) for lb in raw_labels]

        raw_comments = data.get("comments") or []
        if not isinstance(raw_comments, list):
            raise RuntimeError(
                f"Failed to parse gh output: expected comments to be a list, got {type(raw_comments).__name__}"
            )

        comments: list[Comment] = []
        for index, c in enumerate(raw_comments):
            if not isinstance(c, dict):
                raise RuntimeError(
                    "Failed to parse gh output: expected each comment to be a dict, "
                    f"but item at index {index} is {type(c).__name__}"
                )
            id_raw = c.get("id")
            body_raw = c.get("body")
            created_at_raw = c.get("createdAt")
            comments.append(
                Comment(
                    comment_id=self._coerce_str(id_raw),
                    body=self._coerce_str(body_raw),
                    created_at=self._coerce_str(created_at_raw),
                )
            )

        # Build raw dict from the full parsed response, preserving only
        # keys that GitHub actually returned (no synthetic None entries).
        raw: dict[str, object] = {}
        for key in ("createdAt", "updatedAt", "assignees"):
            if key in data:
                raw[key] = data[key]

        return IssueDetailWithRaw(
            issue_id=str(data.get("number", "")),
            title=data.get("title", ""),
            description=data.get("body", ""),
            status=data.get("state", ""),
            labels=label_names,
            url=data.get("url", ""),
            comments=comments,
            raw=raw,
        )

    def add_comment(self, issue_id: str, comment: str) -> CommentResult:
        """Add a comment via ``gh issue comment``."""
        args = ["gh", "issue", "comment", issue_id, *self._repo_args(), "--body", comment]
        self._exec(args)
        return CommentResult(comment_id="")

    def list_issues(self, filters: IssueFilters | None = None) -> list[IssueSummary]:
        """List GitHub issues via ``gh issue list``."""
        args = ["gh", "issue", "list", *self._repo_args(), "--json", "number,title,state,labels,url"]
        if filters:
            for label in filters.get("labels", []):
                args += ["--label", label]
            state = filters.get("state")
            if state:
                args += ["--state", state]
            assignee = filters.get("assignee")
            if assignee:
                args += ["--assignee", assignee]

        result = self._exec(args)
        items = self._parse_json(result.stdout)
        if not isinstance(items, list):
            raise RuntimeError(f"Failed to parse gh output: expected list, got {type(items).__name__}")

        summaries: list[IssueSummary] = []
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise RuntimeError(
                    "Failed to parse gh output: expected each issue to be a dict, "
                    f"but item at index {index} is {type(item).__name__}"
                )
            raw_labels = item.get("labels")
            if not isinstance(raw_labels, list):
                raw_labels = []
            label_names = [lb["name"] if isinstance(lb, dict) else str(lb) for lb in raw_labels]
            summaries.append(
                IssueSummary(
                    issue_id=str(item.get("number", "")),
                    title=item.get("title", ""),
                    status=item.get("state", ""),
                    labels=label_names,
                    url=item.get("url", ""),
                )
            )
        return summaries

    # ------------------------------------------------------------------
    # Label / assignee extraction helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_first_label_value(labels: list[str], prefix: str) -> str:
        """Return the value after *prefix* from the first matching label.

        Uses **case-sensitive** prefix matching.  Returns ``""`` when no label
        matches.
        """
        for label in labels:
            if isinstance(label, str) and label.startswith(prefix):
                return label[len(prefix) :]
        return ""

    @staticmethod
    def _extract_assignees(raw: Mapping[str, Any]) -> list[str]:
        """Extract assignee login strings from the raw GitHub response.

        Entries that are not dicts, lack a ``"login"`` key, or have a
        non-string/``None`` login value are silently skipped.
        """
        raw_assignees = raw.get("assignees")
        if not isinstance(raw_assignees, list):
            return []
        result: list[str] = []
        for entry in raw_assignees:
            if not isinstance(entry, dict):
                continue
            login = entry.get("login")
            if isinstance(login, str) and login:
                result.append(login)
        return result

    # ------------------------------------------------------------------
    # Normalize
    # ------------------------------------------------------------------

    def normalize(self, issue_detail: IssueDetailWithRaw) -> NormalizedIssue:
        """Normalize a GitHub issue detail into a provider-agnostic representation.

        Maps :class:`IssueDetailWithRaw` fields into a uniform
        :class:`NormalizedIssue`.  All logic is pure in-process
        transformation — no I/O occurs.
        """
        # Required identity fields — KeyError on missing is intentional
        issue_id = issue_detail["issue_id"]
        title = issue_detail["title"]
        url = issue_detail["url"]

        # Optional fields with safe defaults
        description_raw = issue_detail.get("description")
        if description_raw is None:
            description = ""
        elif isinstance(description_raw, str):
            description = description_raw
        else:
            description = str(description_raw)
        status_raw = issue_detail.get("status")
        status = status_raw.strip().lower() if isinstance(status_raw, str) and status_raw.strip() else "unknown"

        labels_raw = issue_detail.get("labels")
        labels = [str(item) for item in labels_raw if item is not None] if isinstance(labels_raw, list) else []

        comments_raw = issue_detail.get("comments")
        comments: list[Comment] = []
        if isinstance(comments_raw, list):
            for entry in comments_raw:
                if not isinstance(entry, dict):
                    continue
                comment_id_raw = entry.get("comment_id")
                body_raw = entry.get("body")
                created_at_raw = entry.get("created_at")
                comments.append(
                    Comment(
                        comment_id=self._coerce_str(comment_id_raw),
                        body=self._coerce_str(body_raw),
                        created_at=self._coerce_str(created_at_raw),
                    )
                )

        raw_value = issue_detail.get("raw")
        raw: dict[str, object] = raw_value if isinstance(raw_value, dict) else {}

        # Raw-derived temporal fields
        raw_created_at = raw.get("createdAt", "")
        created_at = raw_created_at if isinstance(raw_created_at, str) else ""
        raw_updated_at = raw.get("updatedAt", "")
        updated_at = raw_updated_at if isinstance(raw_updated_at, str) else ""

        return NormalizedIssue(
            issue_id=issue_id,
            title=title,
            url=url,
            provider="github",
            description=description,
            status=status,
            labels=labels,
            comments=comments,
            created_at=created_at,
            updated_at=updated_at,
            raw=raw,
        )

    def get_issue_types(self) -> list[IssueTypeInfo]:
        """Return available issue types for the GitHub repository.

        Discovers types from repository labels and issue form templates.
        Returns at least one entry (baseline ``"issue"`` type) even when
        no recognizable labels or forms are found. When no explicit
        ``owner/repo`` slug is configured, falls back to the baseline type
        without attempting repository-scoped schema discovery.
        """
        if not self._repo:
            return [IssueTypeInfo(name="issue", description=DESCRIPTION_MAP["issue"])]

        deadline = time.monotonic() + 10.0

        # Fetch labels (uses cache if available)
        labels = self._get_cached_labels()
        if labels is None:
            labels = self._fetch_labels(deadline)

        # Fetch form templates (uses cache if available)
        forms = self._get_cached_forms()
        if forms is None:
            forms = self._fetch_form_templates(deadline)

        # Build type set from labels
        seen_slugs: set[str] = set()
        types: list[IssueTypeInfo] = []

        for label in labels:
            slug = slugify(label)
            canonical = canonicalize(slug)
            if canonical not in WELL_KNOWN_LABELS:
                continue
            if canonical in seen_slugs:
                continue
            seen_slugs.add(canonical)
            description = DESCRIPTION_MAP.get(canonical, "GitHub issue type")
            types.append(IssueTypeInfo(name=canonical, description=description))

        # Merge form-derived types
        for form_slug, form_data in forms.items():
            canonical = canonicalize(form_slug)
            if canonical in seen_slugs:
                continue
            seen_slugs.add(canonical)
            # Description priority: DESCRIPTION_MAP > form description > generic
            if canonical in DESCRIPTION_MAP:
                description = DESCRIPTION_MAP[canonical]
            else:
                form_desc = form_data.get("description")
                if isinstance(form_desc, str) and form_desc.strip():
                    description = form_desc.strip()
                else:
                    description = "GitHub issue type"
            types.append(IssueTypeInfo(name=canonical, description=description))

        # Ensure baseline default
        if not types:
            types.append(IssueTypeInfo(name="issue", description=DESCRIPTION_MAP["issue"]))

        # Sort by name for deterministic output
        types.sort(key=lambda t: t["name"])
        return types

    def get_type_properties(self, type_name: str) -> list[PropertySchema]:
        """Return field schema for a GitHub issue type.

        Args:
            type_name: Issue type name (from ``get_issue_types()`` results).

        Raises:
            ValueError: If *type_name* is empty or whitespace-only.
        """
        if not isinstance(type_name, str) or not type_name.strip():
            raise ValueError("type_name must be a non-empty string")
        type_name = type_name.strip()
        if not self._repo:
            return copy_default_properties()

        deadline = time.monotonic() + 10.0

        # Ensure forms cache is populated before lookup
        if self._get_cached_forms() is None:
            self._fetch_form_templates(deadline)

        # Look up form by canonicalized type name
        form_data = self._find_form_for_type(type_name)
        if form_data is None:
            return copy_default_properties()

        # Parse form body
        body = form_data.get("body")
        if not isinstance(body, list):
            return copy_default_properties()

        try:
            form_fields = parse_form_fields(body)
        except Exception:
            return copy_default_properties()

        # Compose: DEFAULT_PROPERTIES + form fields, deduped by name
        result = copy_default_properties()
        existing_names = {p["name"] for p in result}
        for field in form_fields:
            if field["name"] not in existing_names:
                result.append(field)
                existing_names.add(field["name"])
        return result

    # ------------------------------------------------------------------
    # Schema discovery helpers
    # ------------------------------------------------------------------

    def _get_cached_labels(self) -> list[str] | None:
        """Return cached labels or None if not yet fetched."""
        return self._labels_cache

    def _get_cached_forms(self) -> dict[str, dict[str, Any]] | None:
        """Return cached form templates or None if not yet fetched."""
        return self._forms_cache

    def _fetch_labels(self, deadline: float) -> list[str]:
        """Fetch all repository labels via paginated gh api calls.

        Populates ``_labels_cache`` only on full success.
        """
        labels: list[str] = []
        page = 1
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RuntimeError("Deadline exceeded while fetching labels")
            args = [
                "gh",
                "api",
                f"repos/{self._repo}/labels?per_page=100&page={page}",
            ]
            result = self._exec(args, timeout=remaining)
            data = self._parse_json(result.stdout)
            if not isinstance(data, list):
                raise RuntimeError(f"Expected list from labels API, got {type(data).__name__}")
            if not data:
                break
            for item in data:
                if isinstance(item, dict):
                    name = item.get("name")
                    if isinstance(name, str):
                        labels.append(name)
            page += 1

        self._labels_cache = labels
        return labels

    def _fetch_form_templates(self, deadline: float) -> dict[str, dict[str, Any]]:
        """Fetch and parse issue form templates from the repository.

        Fetches the ``.github/ISSUE_TEMPLATE`` directory listing, then each
        YAML file's raw content. Individual template fetch or parse failures
        are silently skipped; ``_forms_cache`` is populated with whatever
        templates parsed successfully (partial-success caching).
        Returns an empty dict on 404 (no template directory).
        """
        forms: dict[str, dict[str, Any]] = {}

        # Fetch directory listing
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise RuntimeError("Deadline exceeded while fetching form templates")

        args = [
            "gh",
            "api",
            f"repos/{self._repo}/contents/.github/ISSUE_TEMPLATE",
        ]
        try:
            result = self._exec(args, timeout=remaining)
        except RuntimeError as exc:
            # 404 means no template directory — not an error
            if "HTTP 404" in str(exc):
                self._forms_cache = forms
                return forms
            raise

        data = self._parse_json(result.stdout)
        if not isinstance(data, list):
            self._forms_cache = forms
            return forms

        # Filter YAML files, exclude config files
        yaml_files: list[dict[str, Any]] = []
        for item in data:
            if not isinstance(item, dict):
                continue
            name = item.get("name")
            if not isinstance(name, str):
                continue
            name_lower = name.lower()
            if name_lower in ("config.yml", "config.yaml"):
                continue
            if name_lower.endswith(".yml") or name_lower.endswith(".yaml"):
                yaml_files.append(item)

        # Fetch each form template
        for file_info in yaml_files:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RuntimeError("Deadline exceeded while fetching form templates")

            path = file_info.get("path")
            if not isinstance(path, str):
                continue

            fetch_args = [
                "gh",
                "api",
                f"repos/{self._repo}/contents/{path}",
                "-H",
                "Accept: application/vnd.github.raw",
            ]
            try:
                file_result = self._exec(fetch_args, timeout=remaining)
            except RuntimeError:
                continue  # Skip malformed/unavailable templates

            try:
                parsed = yaml.safe_load(file_result.stdout)
            except yaml.YAMLError:
                continue  # Skip malformed YAML

            if not isinstance(parsed, dict):
                continue

            # Extract form name and slugify
            form_name = parsed.get("name")
            if not isinstance(form_name, str) or not form_name.strip():
                continue

            form_slug = slugify(form_name.strip())
            if not form_slug:
                continue
            forms[form_slug] = parsed

        self._forms_cache = forms
        return forms

    def _find_form_for_type(self, type_name: str) -> dict[str, Any] | None:
        """Look up a form template by canonicalized type name."""
        canonical = canonicalize(slugify(type_name))
        forms = self._forms_cache or {}
        # Direct match
        if canonical in forms:
            return forms[canonical]
        # Try canonicalized form slugs
        for form_slug, form_data in forms.items():
            if canonicalize(form_slug) == canonical:
                return form_data
        return None
