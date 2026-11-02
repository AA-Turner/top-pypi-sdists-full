"""Resolve SpecKit issue hierarchy and inherited parent-spec context."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any
from urllib.parse import quote

from agentic_devtools.cli.ci.agent_assignment import _gh_api_call

_LEVEL_RE = re.compile(r"""^level:[ \t]*(?:"([^"]*)"|'([^']*)'|([^#"'\n]*?))(?:[ \t]+#.*)?[ \t]*$""", re.MULTILINE)
_RAW_LEVEL_RE = re.compile(r"^level:", re.MULTILINE)
_VALID_LEVELS = {"epic", "feature", "task"}
_REPO_SEGMENT_RE = re.compile(r"^[A-Za-z0-9._-]+$")


@dataclass(frozen=True)
class Resolution:
    """Resolved hierarchy and parent-spec context for one issue."""

    hierarchy_level: str
    spec_dir: str
    spec_context: str
    parent_number: str
    reason: str
    exit_code: int = 0


def authoritative_level(labels: object, issue_type: object) -> str:
    """Return the issue's authoritative level, preserving epic and conflict precedence."""
    values: set[str] = set()
    if isinstance(labels, list):
        for label in labels:
            value = label.get("name") if isinstance(label, dict) else label
            if isinstance(value, str):
                values.add(value.strip().lower())
    if isinstance(issue_type, dict):
        issue_type = issue_type.get("name")
    if isinstance(issue_type, str):
        values.add(issue_type.strip().lower())
    if "epic" in values:
        return "epic"
    non_epic = values & {"task", "feature"}
    if len(non_epic) > 1:
        return "unknown"
    return next(iter(non_epic), "")


def metadata_level(hierarchy_yml_text: str | None) -> str | None:
    """Parse one canonical ``level`` declaration; return unknown for malformed metadata."""
    if hierarchy_yml_text is None:
        return None
    matches = list(_LEVEL_RE.finditer(hierarchy_yml_text))
    raw_count = len(_RAW_LEVEL_RE.findall(hierarchy_yml_text))
    if raw_count != 1 or len(matches) != 1:
        return "unknown"
    value = next((group for group in matches[0].groups() if group is not None), "").strip().lower()
    return value if value in _VALID_LEVELS else "unknown"


def combine_levels(authoritative: str, metadata: str | None) -> str:
    """Combine issue signals and hierarchy metadata using the trigger's existing precedence."""
    if authoritative == "epic":
        return "epic"
    if authoritative == "unknown":
        return "unknown"
    if metadata == "unknown":
        return "unknown"
    if metadata and authoritative and metadata != authoritative:
        return "unknown"
    return metadata or authoritative or "unknown"


def _parent_name_with_owner(parent: dict[str, Any] | None) -> str:
    """Return the parent's validated ``owner/repo`` name, or '' when parent/number/repo is invalid."""
    if not isinstance(parent, dict):
        return ""
    number = parent.get("number")
    if not (isinstance(number, int) and number > 0):
        return ""
    repository = parent.get("repository")
    name_with_owner = repository.get("nameWithOwner") if isinstance(repository, dict) else None
    return name_with_owner if isinstance(name_with_owner, str) and name_with_owner else ""


def find_parent_spec(tree_paths: list[str], parent_number: int | str) -> list[str]:
    """Return matching parent ``spec.md`` paths, including supported zero-padded layouts."""
    number = str(parent_number)
    patterns = [
        re.compile(rf"^specs/{re.escape(number)}-[^/]+/spec\.md$"),
        re.compile(rf"^specs/[^/]+/{re.escape(number)}/spec\.md$"),
        re.compile(rf"^specs/[^/]+/{re.escape(number)}-[^/]+/spec\.md$"),
    ]
    padding_widths = {
        len(match.group(1))
        for path in tree_paths
        for segment in PurePosixPath(path).parts[1:-1]
        if (match := re.match(r"^(0\d+)(?:-|$)", segment))
    }
    for padding_width in sorted(padding_widths):
        padded_number = number.zfill(padding_width)
        if padded_number != number:
            patterns.extend(
                (
                    re.compile(rf"^specs/{re.escape(padded_number)}-[^/]+/spec\.md$"),
                    re.compile(rf"^specs/[^/]+/{re.escape(padded_number)}/spec\.md$"),
                    re.compile(rf"^specs/[^/]+/{re.escape(padded_number)}-[^/]+/spec\.md$"),
                )
            )
    return sorted({path for path in tree_paths if any(pattern.fullmatch(path) for pattern in patterns)})


def resolve(
    issue: dict[str, Any],
    parent: dict[str, Any] | None,
    tree_paths: list[str],
    *,
    hierarchy_yml_text: str | None = None,
    repo: str = "",
) -> Resolution:
    """Resolve hierarchy while enforcing the parent-first spec gate."""
    number = issue.get("number")
    issue_number = str(number) if isinstance(number, int) and number > 0 else ""
    hierarchy_paths = [
        path
        for path in tree_paths
        if path.endswith("/hierarchy.yml")
        and (
            PurePosixPath(path).parent.name == issue_number
            or PurePosixPath(path).parent.name.startswith(f"{issue_number}-")
        )
    ]
    spec_dir = PurePosixPath(hierarchy_paths[0]).parent.as_posix() if len(hierarchy_paths) == 1 else ""
    metadata = "unknown" if len(hierarchy_paths) > 1 else metadata_level(hierarchy_yml_text)
    issue_level = authoritative_level(issue.get("labels"), issue.get("type"))
    level = combine_levels(issue_level, metadata)
    task_candidate = level == "task" or issue_level == "task"
    if not hierarchy_paths and task_candidate:
        task_dirs = {
            PurePosixPath(path).parent.as_posix()
            for path in tree_paths
            if path.endswith("/tasks.md")
            and (
                PurePosixPath(path).parent.name == issue_number
                or PurePosixPath(path).parent.name.startswith(f"{issue_number}-")
            )
        }
        if len(task_dirs) == 1:
            spec_dir = next(iter(task_dirs))

    parent_number_raw = parent.get("number") if isinstance(parent, dict) else None
    parent_number = str(parent_number_raw) if isinstance(parent_number_raw, int) and parent_number_raw > 0 else ""
    parent_repo = _parent_name_with_owner(parent)
    same_repo_parent = bool(parent_repo) and bool(repo) and parent_repo.casefold() == repo.casefold()

    if same_repo_parent:
        matches = find_parent_spec(tree_paths, parent_number)
        if not matches:
            return Resolution("blocked", spec_dir, "", parent_number, "parent-spec-missing", 3)
        if len(matches) > 1 and task_candidate:
            return Resolution("task", spec_dir, "", parent_number, "parent-spec-ambiguous", 2)
        if level == "task":
            return Resolution("task", spec_dir, matches[0], parent_number, "parent-spec-found")

    if task_candidate and not same_repo_parent:
        if parent is None:
            return Resolution("feature", spec_dir, "", "", "task-without-parent")
        return Resolution("feature", spec_dir, "", parent_number, "task-cross-repo-parent")
    return Resolution(level, spec_dir, "", parent_number, "resolved")


class GitHubHierarchyLookup:
    """Read issue, hierarchy, parent, and spec-tree data from GitHub."""

    def __init__(self, repo: str, ref: str, token: str) -> None:
        parts = repo.split("/")
        if (
            len(parts) != 2
            or not all(_REPO_SEGMENT_RE.fullmatch(part) for part in parts)
            or any(part in {".", ".."} for part in parts)
        ):
            raise ValueError("repo must be in owner/repo form using GitHub-safe characters")
        if not ref.strip():
            raise ValueError("ref must not be empty")
        self.repo = repo
        self.owner, self.repo_name = parts
        self.ref = ref
        self.token = token

    def _json_api(self, endpoint: str, *, method: str = "GET", body: dict[str, Any] | None = None) -> dict[str, Any]:
        response = _gh_api_call(endpoint, method=method, body=body, token=self.token or None)
        payload = json.loads(response)
        if not isinstance(payload, dict):
            raise RuntimeError("GitHub API returned an unexpected response")
        return payload

    def fetch_issue(self, issue_number: int) -> dict[str, Any]:
        """Fetch issue labels and type."""
        return self._json_api(f"/repos/{self.repo}/issues/{issue_number}")

    def fetch_parent(self, issue_number: int) -> dict[str, Any] | None:
        """Fetch the issue's parent and owning repository through GraphQL."""
        query = (
            "query($owner: String!, $repo: String!, $childNumber: Int!) { "
            "repository(owner: $owner, name: $repo) { issue(number: $childNumber) { "
            "parent { number repository { nameWithOwner } } } } }"
        )
        response = self._json_api(
            "/graphql",
            method="POST",
            body={
                "query": query,
                "variables": {"owner": self.owner, "repo": self.repo_name, "childNumber": issue_number},
            },
        )
        if response.get("errors"):
            raise RuntimeError(f"GitHub GraphQL request returned errors: {response['errors']}")
        try:
            parent = response["data"]["repository"]["issue"]["parent"]
        except (KeyError, TypeError) as exc:
            raise RuntimeError("GitHub GraphQL response did not contain issue parent data") from exc
        if parent is None:
            return None
        if not isinstance(parent, dict) or not _parent_name_with_owner(parent):
            raise RuntimeError("GitHub GraphQL returned an invalid parent")
        return parent

    def fetch_tree(self) -> tuple[list[str], bool]:
        """Fetch ``specs/`` blob paths from the requested ref and its truncation flag."""
        ref = self._json_api(f"/repos/{self.repo}/git/ref/heads/{quote(self.ref, safe='')}")
        try:
            commit_sha = ref["object"]["sha"]
            commit = self._json_api(f"/repos/{self.repo}/git/commits/{quote(commit_sha, safe='')}")
            root_tree_sha = commit["tree"]["sha"]
            root_tree = self._json_api(f"/repos/{self.repo}/git/trees/{quote(root_tree_sha, safe='')}")
            specs = next(
                (
                    entry
                    for entry in root_tree.get("tree", [])
                    if entry.get("path") == "specs" and entry.get("type") == "tree"
                ),
                None,
            )
            if specs is None:
                return [], False
            specs_tree = self._json_api(f"/repos/{self.repo}/git/trees/{quote(specs['sha'], safe='')}?recursive=1")
            entries = specs_tree.get("tree")
            if not isinstance(entries, list):
                raise RuntimeError("GitHub tree response did not contain a tree")
            paths = [
                f"specs/{entry['path']}"
                for entry in entries
                if isinstance(entry, dict) and entry.get("type") == "blob" and isinstance(entry.get("path"), str)
            ]
            return paths, specs_tree.get("truncated") is True
        except (KeyError, TypeError) as exc:
            raise RuntimeError("GitHub tree response was incomplete") from exc

    def fetch_hierarchy(self, tree_paths: list[str], issue_number: int) -> tuple[list[str], str | None]:
        """Return issue hierarchy file paths and the sole file's decoded content."""
        candidates = [
            path
            for path in tree_paths
            if path.endswith("/hierarchy.yml")
            and (
                PurePosixPath(path).parent.name == str(issue_number)
                or PurePosixPath(path).parent.name.startswith(f"{issue_number}-")
            )
        ]
        if len(candidates) != 1:
            return candidates, None
        response = self._json_api(
            f"/repos/{self.repo}/contents/{quote(candidates[0], safe='/')}?ref={quote(self.ref, safe='')}"
        )
        try:
            if response.get("encoding") != "base64" or not isinstance(response.get("content"), str):
                raise RuntimeError("GitHub hierarchy blob was not base64 encoded")
            return candidates, base64.b64decode(response["content"]).decode("utf-8")
        except (ValueError, UnicodeDecodeError) as exc:
            raise RuntimeError("GitHub hierarchy blob could not be decoded") from exc

    def search_paths(self, filename: str) -> list[str]:
        """Search all code-result pages for a specs filename on the requested default branch."""
        repository = self._json_api(f"/repos/{self.repo}")
        if repository.get("default_branch") != self.ref:
            raise RuntimeError(
                "GitHub code search only searches the repository's default branch; "
                f"requested ref {self.ref!r} cannot use this fallback"
            )
        paths: list[str] = []
        query = quote(f"filename:{filename} path:specs/ repo:{self.repo}", safe="")
        page = 1
        while True:
            result = self._json_api(f"/search/code?q={query}&per_page=100&page={page}")
            items = result.get("items")
            if not isinstance(items, list):
                raise RuntimeError("GitHub Search API returned an invalid items list")
            found = [item["path"] for item in items if isinstance(item, dict) and isinstance(item.get("path"), str)]
            paths.extend(found)
            if result.get("incomplete_results") is True:
                raise RuntimeError("GitHub Search API returned incomplete results")
            if len(items) < 100:
                return paths
            if page == 10:
                raise RuntimeError("GitHub Search API reached its 1000-result limit")
            page += 1


def _write_outputs(resolution: Resolution) -> None:
    """Print the JSON result and append simple outputs when running in Actions."""
    values = {
        "hierarchy_level": resolution.hierarchy_level,
        "spec_dir": resolution.spec_dir,
        "spec_context": resolution.spec_context,
        "parent_number": resolution.parent_number,
        "reason": resolution.reason,
    }
    print(json.dumps(values))
    output_path = os.environ.get("GITHUB_OUTPUT", "")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as output:
            for key, value in values.items():
                output.write(f"{key}={value.replace('\n', '').replace('\r', '')}\n")


def _lookup_failure(
    issue: dict[str, Any] | None,
    reason: str = "lookup-failed",
    *,
    task_resolution: bool = False,
) -> Resolution:
    """Return the failure result while preserving the authoritative Epic exception."""
    if issue and authoritative_level(issue.get("labels"), issue.get("type")) == "epic":
        return Resolution("epic", "", "", "", "resolved")
    exit_code = (
        2
        if issue is None or task_resolution or authoritative_level(issue.get("labels"), issue.get("type")) == "task"
        else 0
    )
    return Resolution("unknown", "", "", "", reason, exit_code)


def _handle_parent_spec_missing(*, issue_number: int, parent_number: str, repo: str, token: str) -> None:
    """Preserve the existing parent-first comment and label behavior."""
    comment_on_issue = os.environ.get("SPECKIT_COMMENT_ON_ISSUE", "") != "false"
    if comment_on_issue:
        run_id = os.environ.get("GITHUB_RUN_ID", "")
        body = "\n".join(
            [
                "✋ **SpecKit: Parent issue must be specked first**",
                "",
                f"This issue (#{issue_number}) is a sub-issue of #{parent_number}, "
                f"which has not been processed by SpecKit yet. Please add the `speckit` label to #{parent_number} "
                "first and wait for it to complete before re-triggering this issue.",
                "",
                "---",
                f"_This comment was posted by the [SpecKit GitHub Action](https://github.com/{repo}/actions/runs/{run_id})._",
            ]
        )
        try:
            _gh_api_call(
                f"/repos/{repo}/issues/{issue_number}/comments",
                method="POST",
                body={"body": body},
                token=token or None,
            )
        except Exception as exc:
            print(f"Warning: failed to post parent-first comment: {exc}", file=sys.stderr)
    event_path = os.environ.get("GITHUB_EVENT_PATH", "")
    event_label = ""
    if event_path:
        try:
            with open(event_path, encoding="utf-8") as event_file:
                event = json.load(event_file)
            label = event.get("label") if isinstance(event, dict) else None
            event_label = label.get("name", "") if isinstance(label, dict) else ""
        except OSError, json.JSONDecodeError:
            event_label = ""
    trigger_label = event_label or os.environ.get("SPECKIT_TRIGGER_LABEL", "speckit")
    for label in (trigger_label, "speckit:processing"):
        if label:
            try:
                _gh_api_call(
                    f"/repos/{repo}/issues/{issue_number}/labels/{quote(label, safe='')}",
                    method="DELETE",
                    token=token or None,
                )
            except Exception as exc:
                if "404" not in str(exc):
                    print(f"Warning: failed to remove {label}: {exc}", file=sys.stderr)
    try:
        _gh_api_call(
            f"/repos/{repo}/labels/speckit%3Ablocked",
            method="GET",
            token=token or None,
        )
    except Exception as exc:
        if "404" in str(exc):
            try:
                _gh_api_call(
                    f"/repos/{repo}/labels",
                    method="POST",
                    body={
                        "name": "speckit:blocked",
                        "color": "d93f0b",
                        "description": "Blocked: parent issue must be specked first",
                    },
                    token=token or None,
                )
            except Exception as create_exc:
                if "422" not in str(create_exc):
                    print(f"Warning: failed to create speckit:blocked label: {create_exc}", file=sys.stderr)
        else:
            print(f"Warning: failed to get speckit:blocked label: {exc}", file=sys.stderr)
    try:
        _gh_api_call(
            f"/repos/{repo}/issues/{issue_number}/labels",
            method="POST",
            body={"labels": ["speckit:blocked"]},
            token=token or None,
        )
    except Exception as exc:
        print(f"Warning: failed to add speckit:blocked label: {exc}", file=sys.stderr)


def _run_resolution(lookup: GitHubHierarchyLookup, issue_number: int, repo: str) -> Resolution:
    """Fetch issue/tree/hierarchy/parent data and compute the final result.

    Pure pipeline: no output writing, no process exit. Callers decide how to surface
    ``resolution.exit_code`` (CLI exit vs. folding into a single workflow-safe outcome).
    """
    issue: dict[str, Any] | None = None
    try:
        issue = lookup.fetch_issue(issue_number)
        tree_paths, truncated = lookup.fetch_tree()
    except Exception as exc:
        print(f"Warning: hierarchy lookup failed: {exc}", file=sys.stderr)
        return _lookup_failure(issue)

    if truncated:
        try:
            hierarchy_paths = lookup.search_paths("hierarchy.yml")
        except Exception as exc:
            if authoritative_level(issue.get("labels"), issue.get("type")) == "task":
                print(f"Warning: hierarchy lookup failed: {exc}", file=sys.stderr)
                return _lookup_failure(issue)
            hierarchy_paths = []
        tree_paths = list(dict.fromkeys(tree_paths + hierarchy_paths))
    else:
        hierarchy_paths = tree_paths

    try:
        matching_hierarchies, hierarchy_text = lookup.fetch_hierarchy(hierarchy_paths, issue_number)
        if len(matching_hierarchies) > 1:
            hierarchy_text = "level: invalid\nlevel: duplicated\n"
    except Exception as exc:
        if authoritative_level(issue.get("labels"), issue.get("type")) == "task":
            print(f"Warning: hierarchy lookup failed: {exc}", file=sys.stderr)
            return _lookup_failure(issue)
        print(f"Warning: hierarchy metadata lookup failed: {exc}", file=sys.stderr)
        # Metadata is unreadable, not merely absent: force an "unknown" result below (via
        # metadata_level) instead of returning early, so the parent-first gate still runs.
        hierarchy_text = ""

    issue_authoritative_level = authoritative_level(issue.get("labels"), issue.get("type"))
    task_candidate = issue_authoritative_level == "task" or (
        combine_levels(issue_authoritative_level, metadata_level(hierarchy_text)) == "task"
    )
    try:
        parent = lookup.fetch_parent(issue_number)
    except Exception as exc:
        if task_candidate:
            print(f"Warning: hierarchy lookup failed: {exc}", file=sys.stderr)
            return _lookup_failure(issue, task_resolution=True)
        parent = None

    parent_repo = _parent_name_with_owner(parent)
    same_repo_parent = bool(parent_repo) and parent_repo.casefold() == repo.casefold()
    parent_paths = tree_paths
    if truncated and same_repo_parent:
        try:
            parent_paths = list(dict.fromkeys(tree_paths + lookup.search_paths("spec.md")))
        except Exception as exc:
            if task_candidate:
                print(f"Warning: parent spec lookup failed: {exc}", file=sys.stderr)
                return _lookup_failure(issue, task_resolution=True)
            parent = None
    return resolve(
        issue,
        parent,
        parent_paths,
        hierarchy_yml_text=hierarchy_text,
        repo=repo,
    )


def _build_lookup(parser: argparse.ArgumentParser, repo: str, ref: str, token: str) -> GitHubHierarchyLookup:
    """Construct the lookup client, routing invalid CLI arguments through ``parser.error``."""
    try:
        return GitHubHierarchyLookup(repo, ref, token)
    except ValueError as exc:
        parser.error(str(exc))
        raise AssertionError("parser.error always raises SystemExit") from exc  # pragma: no cover


def _add_common_resolver_args(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """Register and parse the ``--issue-number``/``--repo``/``--ref`` arguments shared by both CLIs."""
    parser.add_argument("--issue-number", type=int, required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--ref", default="main")
    args = parser.parse_args()
    if args.issue_number <= 0:
        parser.error("--issue-number must be positive")
    return args


def resolve_hierarchy_command() -> None:
    """Resolve one GitHub issue and emit workflow outputs; exit 2/3 on unsafe results."""
    parser = argparse.ArgumentParser(description="Resolve SpecKit issue hierarchy and parent spec context")
    args = _add_common_resolver_args(parser)
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
    lookup = _build_lookup(parser, args.repo, args.ref, token)
    resolution = _run_resolution(lookup, args.issue_number, args.repo)
    _write_outputs(resolution)
    if resolution.reason == "parent-spec-missing":
        _handle_parent_spec_missing(
            issue_number=args.issue_number,
            parent_number=resolution.parent_number,
            repo=args.repo,
            token=token,
        )
    if resolution.exit_code:
        raise SystemExit(resolution.exit_code)


def reresolve_task_level(lookup: GitHubHierarchyLookup, issue_number: int, repo: str, token: str) -> Resolution:
    """Re-resolve a task issue's hierarchy for a single-call, exit-code-free workflow contract.

    Folds the resolver's exit-code contract (0=resolved, 3=blocked, anything else=lookup
    failure) into one finalized ``Resolution`` so a calling workflow step never branches on
    subprocess exit status or decodes JSON to recover that policy itself. A blocked result is
    returned unchanged (after triggering the same parent-first comment/labels as the direct
    CLI) so the caller still observes ``hierarchy_level == "blocked"``. Any other failure falls
    back to ``hierarchy_level == "task"`` with no spec context, matching the stopped outcome a
    directly-failing lookup previously forced in workflow YAML, so the downstream
    parent-context gate still runs and fails the issue.
    """
    resolution = _run_resolution(lookup, issue_number, repo)
    if resolution.reason == "parent-spec-missing":
        _handle_parent_spec_missing(
            issue_number=issue_number,
            parent_number=resolution.parent_number,
            repo=repo,
            token=token,
        )
        return resolution
    if resolution.exit_code or resolution.hierarchy_level == "unknown":
        return Resolution("task", "", "", "", "", 0)
    return resolution


def reresolve_task_level_command() -> None:
    """CLI wrapper around :func:`reresolve_task_level`; always emits outputs and exits 0."""
    parser = argparse.ArgumentParser(description="Re-resolve a task issue's hierarchy for workflow consumption")
    args = _add_common_resolver_args(parser)
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
    lookup = _build_lookup(parser, args.repo, args.ref, token)
    resolution = reresolve_task_level(lookup, args.issue_number, args.repo, token)
    _write_outputs(resolution)
