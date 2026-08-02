"""Detect CI/local mode, MR context, and related issue context.

Resolution order:
1. Explicit CLI flags (--mr-iid, --issue-iid, --job-id, --pipeline-id) or positional refs
2. CI environment variables ($CI_MERGE_REQUEST_IID, etc.)
3. glab CLI detection (current branch MR, git remote)
4. Git ref parsing (refs/merge-requests/NNN/head)

Chained resolution: job -> pipeline -> MR -> issue (each level enriches the next).

Output: JSON object with all detected context fields.

Internally the detection is expressed as pure ``_detect_*`` functions that read
the current state and *return* a typed sub-model (``ProjectCtx``, ``MrCtx``,
``IssueCtx``, ``EpicCtx``, ``PipelineCtx``, ``GitCtx``); ``detect()`` is the sole
assembler that composes those values into the final ``Context``. ``Context``
keeps a flat field surface on purpose: it is the JSON output contract and the
type the CLI-runner consumers construct and read directly.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Annotated, Any, Self

import typer

from ...common.glab.models import GitLabIssue, Mr
from ...common.glab.runner import run_glab
from ...common.issue_tracking.platform import Platform, platform_for_url
from ...config import CACHE_DIR as _XDG_CACHE_DIR
from .parse_refs import parse_gitlab_refs

CACHE_DIR = _XDG_CACHE_DIR / "detect-context-cache"
CACHE_TTL_SECONDS = 300  # 5 minutes

# Historical location, under Claude's own dir before the XDG move.
_LEGACY_CACHE_DIR = Path.home() / ".claude" / "pysae-ai-tools" / "detect-context-cache"


def migrate_legacy() -> None:
    """Relocate the context cache from ``~/.claude`` to the XDG cache dir, once. Best-effort."""
    try:
        if _LEGACY_CACHE_DIR.is_dir() and not CACHE_DIR.exists():
            CACHE_DIR.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(_LEGACY_CACHE_DIR), str(CACHE_DIR))
    except OSError:
        pass


@dataclass
class DetectArgs:
    refs: list[str] = field(default_factory=list)
    mr_iid: str = ""
    issue_iid: str = ""
    job_id: str = ""
    pipeline_id: str = ""
    local: bool = False


@dataclass
class Context:
    # Mode
    is_ci: bool = False

    # Local git (from git commands, not API)
    git_branch: str = ""
    git_sha: str = ""
    git_prod_version: str = ""
    # Repo owner / top-level namespace (GitHub owner, GitLab group) — holds the
    # group-scoped labels (workflow::*, type::*, …).
    owner: str = ""

    # Project
    project_id: str = ""
    project_path: str = ""
    project_url: str = ""
    default_branch: str = ""

    # Issue-tracking provider, derived from the repo host: "gitlab" | "github".
    issue_provider: str = ""

    # MR
    mr_iid: str = ""
    mr_title: str = ""
    mr_description: str = ""
    mr_author: str = ""
    mr_labels: list[str] = field(default_factory=list)
    mr_assignees: list[str] = field(default_factory=list)
    mr_url: str = ""
    mr_source_branch: str = ""
    mr_target_branch: str = ""

    # Issue (linked to MR or explicit)
    issue_iid: str = ""
    issue_title: str = ""
    issue_description: str = ""
    issue_labels: list[str] = field(default_factory=list)
    issue_assignees: list[str] = field(default_factory=list)
    issue_url: str = ""

    # Epic (from issue's epic field, details from group epics API)
    epic_iid: str = ""
    epic_title: str = ""
    epic_description: str = ""
    epic_labels: list[str] = field(default_factory=list)
    epic_url: str = ""

    # Pipeline/job (CI only)
    pipeline_id: str = ""
    pipeline_url: str = ""
    job_id: str = ""
    job_name: str = ""

    # Diagnostics
    detection_sources: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# ─── Typed sub-models ────────────────────────────────────────────────────────
#
# Each sub-model groups the flat ``Context`` fields of one concern. ``read``
# extracts the current value from the context and ``write`` composes a resolved
# value back into it — the ``_detect_*`` functions build on these to stay pure
# (read current state, return a resolved sub-model) while ``detect()`` owns the
# single write path.


@dataclass
class GitCtx:
    branch: str = ""
    sha: str = ""
    prod_version: str = ""

    @classmethod
    def read(cls, ctx: Context) -> Self:
        return cls(branch=ctx.git_branch, sha=ctx.git_sha, prod_version=ctx.git_prod_version)

    def write(self, ctx: Context) -> None:
        ctx.git_branch = self.branch
        ctx.git_sha = self.sha
        ctx.git_prod_version = self.prod_version


@dataclass
class ProjectCtx:
    id: str = ""
    path: str = ""
    url: str = ""
    default_branch: str = ""

    @classmethod
    def read(cls, ctx: Context) -> Self:
        return cls(
            id=ctx.project_id,
            path=ctx.project_path,
            url=ctx.project_url,
            default_branch=ctx.default_branch,
        )

    def write(self, ctx: Context) -> None:
        ctx.project_id = self.id
        ctx.project_path = self.path
        ctx.project_url = self.url
        ctx.default_branch = self.default_branch


@dataclass
class MrCtx:
    iid: str = ""
    title: str = ""
    description: str = ""
    author: str = ""
    labels: list[str] = field(default_factory=list)
    assignees: list[str] = field(default_factory=list)
    url: str = ""
    source_branch: str = ""
    target_branch: str = ""

    @classmethod
    def read(cls, ctx: Context) -> Self:
        return cls(
            iid=ctx.mr_iid,
            title=ctx.mr_title,
            description=ctx.mr_description,
            author=ctx.mr_author,
            labels=ctx.mr_labels,
            assignees=ctx.mr_assignees,
            url=ctx.mr_url,
            source_branch=ctx.mr_source_branch,
            target_branch=ctx.mr_target_branch,
        )

    def write(self, ctx: Context) -> None:
        ctx.mr_iid = self.iid
        ctx.mr_title = self.title
        ctx.mr_description = self.description
        ctx.mr_author = self.author
        ctx.mr_labels = self.labels
        ctx.mr_assignees = self.assignees
        ctx.mr_url = self.url
        ctx.mr_source_branch = self.source_branch
        ctx.mr_target_branch = self.target_branch


@dataclass
class IssueCtx:
    iid: str = ""
    title: str = ""
    description: str = ""
    labels: list[str] = field(default_factory=list)
    assignees: list[str] = field(default_factory=list)
    url: str = ""

    @classmethod
    def read(cls, ctx: Context) -> Self:
        return cls(
            iid=ctx.issue_iid,
            title=ctx.issue_title,
            description=ctx.issue_description,
            labels=ctx.issue_labels,
            assignees=ctx.issue_assignees,
            url=ctx.issue_url,
        )

    def write(self, ctx: Context) -> None:
        ctx.issue_iid = self.iid
        ctx.issue_title = self.title
        ctx.issue_description = self.description
        ctx.issue_labels = self.labels
        ctx.issue_assignees = self.assignees
        ctx.issue_url = self.url


@dataclass
class EpicCtx:
    iid: str = ""
    title: str = ""
    description: str = ""
    labels: list[str] = field(default_factory=list)
    url: str = ""

    @classmethod
    def read(cls, ctx: Context) -> Self:
        return cls(
            iid=ctx.epic_iid,
            title=ctx.epic_title,
            description=ctx.epic_description,
            labels=ctx.epic_labels,
            url=ctx.epic_url,
        )

    def write(self, ctx: Context) -> None:
        ctx.epic_iid = self.iid
        ctx.epic_title = self.title
        ctx.epic_description = self.description
        ctx.epic_labels = self.labels
        ctx.epic_url = self.url


@dataclass
class PipelineCtx:
    id: str = ""
    url: str = ""
    job_id: str = ""
    job_name: str = ""

    @classmethod
    def read(cls, ctx: Context) -> Self:
        return cls(id=ctx.pipeline_id, url=ctx.pipeline_url, job_id=ctx.job_id, job_name=ctx.job_name)

    def write(self, ctx: Context) -> None:
        ctx.pipeline_id = self.id
        ctx.pipeline_url = self.url
        ctx.job_id = self.job_id
        ctx.job_name = self.job_name


@dataclass
class CiCtx:
    is_ci: bool = False
    project: ProjectCtx = field(default_factory=ProjectCtx)
    pipeline: PipelineCtx = field(default_factory=PipelineCtx)
    mr: MrCtx = field(default_factory=MrCtx)


def _run_glab(*args: str, timeout: int = 15) -> str | None:
    """Run a glab command, return stdout or None on failure."""
    res = run_glab(*args, timeout=timeout)
    return res.stdout if res.ok else None


def _run_git(*args: str, timeout: int = 10) -> str | None:
    """Run a git command, return stdout or None on failure."""
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def _parse_json(raw: str, ctx: Context, label: str) -> Any:
    """Parse a glab JSON payload, always recording a warning on failure.

    Single error policy: any invalid-JSON glab response appends a warning to the
    context, whatever the call site (AC-3). Returns the decoded value, or ``None``
    when the payload could not be parsed.
    """
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        ctx.warnings.append(f"{label} returned invalid JSON")
        return None


def _mr_str_iid(mr: Mr) -> str:
    """Render an API MR iid as the context's string form (empty when absent)."""
    return str(mr.iid) if mr.iid else ""


def _merge_full_mr(existing: MrCtx, data: dict[str, Any]) -> MrCtx:
    """Fill every empty MR field from a full API MR payload, preserving what is set."""
    parsed = Mr.from_api(data)
    return MrCtx(
        iid=existing.iid or _mr_str_iid(parsed),
        title=existing.title or parsed.title,
        description=existing.description or parsed.description,
        author=existing.author or parsed.author.username,
        labels=existing.labels or list(parsed.labels),
        assignees=existing.assignees or [u.username for u in parsed.assignees],
        url=existing.url or parsed.web_url,
        source_branch=existing.source_branch or parsed.source_branch,
        target_branch=existing.target_branch or parsed.target_branch,
    )


def _merge_issue(existing: IssueCtx, data: dict[str, Any]) -> IssueCtx:
    """Fill every empty issue field from an API issue payload, preserving what is set."""
    parsed = GitLabIssue.from_api(data)
    return IssueCtx(
        iid=existing.iid or (str(parsed.iid) if parsed.iid else ""),
        title=existing.title or parsed.title,
        description=existing.description or parsed.description,
        labels=existing.labels or list(parsed.labels),
        assignees=existing.assignees or [u.username for u in parsed.assignees],
        url=existing.url or parsed.web_url,
    )


def _detect_ci(ctx: Context) -> CiCtx:
    """Resolve context from CI environment variables."""
    if not os.environ.get("CI"):
        return CiCtx()

    ctx.detection_sources.append("ci-env")
    project = ProjectCtx(
        id=os.environ.get("CI_PROJECT_ID", ""),
        path=os.environ.get("CI_PROJECT_PATH", ""),
        url=os.environ.get("CI_PROJECT_URL", ""),
        default_branch=os.environ.get("CI_DEFAULT_BRANCH", ""),
    )
    pipeline = PipelineCtx(
        id=os.environ.get("CI_PIPELINE_ID", ""),
        url=os.environ.get("CI_PIPELINE_URL", ""),
        job_id=os.environ.get("CI_JOB_ID", ""),
        job_name=os.environ.get("CI_JOB_NAME", ""),
    )

    mr = MrCtx()
    mr_iid = os.environ.get("CI_MERGE_REQUEST_IID", "")
    if mr_iid:
        mr = MrCtx(
            iid=mr_iid,
            title=os.environ.get("CI_MERGE_REQUEST_TITLE", ""),
            source_branch=os.environ.get("CI_MERGE_REQUEST_SOURCE_BRANCH_NAME", ""),
            target_branch=os.environ.get("CI_MERGE_REQUEST_TARGET_BRANCH_NAME", ""),
            url=f"{project.url}/-/merge_requests/{mr_iid}" if project.url else "",
        )
        ctx.detection_sources.append("ci-mr-vars")

    return CiCtx(is_ci=True, project=project, pipeline=pipeline, mr=mr)


def _detect_from_git_ref(ctx: Context) -> tuple[GitCtx, MrCtx, ProjectCtx]:
    """Resolve info from local git state (no API calls): branch, detached HEAD, remote URL."""
    git = GitCtx.read(ctx)
    mr = MrCtx.read(ctx)
    project = ProjectCtx.read(ctx)

    # MR IID from detached HEAD ref
    if not mr.iid:
        ref = _run_git("symbolic-ref", "HEAD")
        if not ref:
            log = _run_git("log", "-1", "--format=%D", "HEAD")
            if log:
                match = re.search(r"refs/merge-requests/(\d+)/head", log)
                if match:
                    mr.iid = match.group(1)
                    ctx.detection_sources.append("git-ref-detached")

    # Local branch and commit SHA
    branch = _run_git("branch", "--show-current")
    if branch:
        git.branch = branch
    sha = _run_git("rev-parse", "HEAD")
    if sha:
        git.sha = sha

    # Prod version from remote prod branch
    prod_msg = _run_git("log", "origin/prod", "-1", "--format=%s")
    if prod_msg:
        version_match = re.search(r"v\d+\.\d+\.\d+(?:-[0-9A-Za-z][0-9A-Za-z.-]*)?", prod_msg)
        if version_match:
            git.prod_version = version_match.group(0)

    # Project host + path from git remote (works without glab). The host drives
    # the issue-tracking provider, so it is captured generically (gitlab.com,
    # github.com, self-hosted) rather than pinned to gitlab.com.
    if not project.path:
        remote_url = _run_git("remote", "get-url", "origin")
        if remote_url:
            # SSH: git@gitlab.com:pysae/api.git -> (gitlab.com, pysae/api)
            # HTTPS: https://github.com/acme/widget.git -> (github.com, acme/widget)
            match = re.search(r"(?:https?://|ssh://)?(?:[^@/]+@)?([^/:]+)[:/](.+?)(?:\.git)?/?$", remote_url)
            if match:
                host, project.path = match.group(1), match.group(2)
                project.url = project.url or f"https://{host}/{project.path}"
                ctx.detection_sources.append("git-remote")

    return git, mr, project


def _detect_from_glab(ctx: Context) -> tuple[ProjectCtx, MrCtx]:
    """Resolve project and MR from glab CLI."""
    project = ProjectCtx.read(ctx)
    mr = MrCtx.read(ctx)

    if not project.id or not project.path:
        raw = _run_glab("repo", "view", "--output", "json")
        if raw:
            data = _parse_json(raw, ctx, "glab repo view")
            if data is not None:
                project = ProjectCtx(
                    id=project.id or str(data.get("id", "")),
                    path=project.path or data.get("path_with_namespace", ""),
                    url=project.url or data.get("web_url", ""),
                    default_branch=project.default_branch or data.get("default_branch", ""),
                )
                ctx.detection_sources.append("glab-repo")

    if not mr.iid:
        raw = _run_glab("mr", "view", "--output", "json")
        if raw:
            data = _parse_json(raw, ctx, "glab mr view")
            if data is not None:
                mr = _merge_full_mr(mr, data)
                ctx.detection_sources.append("glab-mr-view")

    return project, mr


def _detect_mr_details(ctx: Context) -> MrCtx:
    """Fetch MR details via API if we have mr_iid but missing fields."""
    mr = MrCtx.read(ctx)
    if not mr.iid or not ctx.project_id:
        return mr
    if mr.target_branch and mr.source_branch and mr.title:
        return mr

    raw = _run_glab("api", f"projects/{ctx.project_id}/merge_requests/{mr.iid}")
    if not raw:
        return mr
    data = _parse_json(raw, ctx, "MR API")
    if data is None:
        return mr
    mr = _merge_full_mr(mr, data)
    ctx.detection_sources.append("glab-api-mr")
    return mr


def _extract_epic(existing: EpicCtx, issue_data: dict[str, Any]) -> EpicCtx:
    """Extract epic info from an issue API response if not already set."""
    if existing.iid:
        return existing
    epic = issue_data.get("epic")
    if not isinstance(epic, dict):
        return existing
    epic_url = str(epic.get("url", ""))
    # The API returns a relative URL (/groups/pysae/-/epics/259), make it absolute
    if epic_url and not epic_url.startswith("http"):
        epic_url = f"https://gitlab.com{epic_url}"
    return EpicCtx(iid=str(epic.get("iid", "")), title=str(epic.get("title", "")), url=epic_url)


def _detect_linked_issue(ctx: Context) -> tuple[IssueCtx, EpicCtx]:
    """Detect issue linked to the MR (from description or closing references)."""
    issue = IssueCtx.read(ctx)
    epic = EpicCtx.read(ctx)
    if issue.iid or not ctx.mr_iid or not ctx.project_id:
        return issue, epic

    # Try closing issues API
    raw = _run_glab("api", f"projects/{ctx.project_id}/merge_requests/{ctx.mr_iid}/closes_issues")
    if raw:
        issues = _parse_json(raw, ctx, "MR closes_issues API")
        if issues:
            issue = _merge_issue(issue, issues[0])
            epic = _extract_epic(epic, issues[0])
            ctx.detection_sources.append("mr-closes-issues")
            return issue, epic

    # Fallback: parse MR title/description for Closes #NNN / Fixes #NNN
    if ctx.mr_title:
        match = re.search(r"(?:closes?|fixes?|resolves?)\s+#(\d+)", ctx.mr_title, re.IGNORECASE)
        if match:
            issue.iid = match.group(1)
            ctx.detection_sources.append("mr-title-regex")

    return issue, epic


def _detect_project_id_for_api(ctx: Context) -> str:
    """Return the project identifier usable in an API path (id, else URL-encoded path)."""
    if ctx.project_id:
        return ctx.project_id
    if ctx.project_path:
        return ctx.project_path.replace("/", "%2F")
    return ""


def _resolve_job_to_pipeline(ctx: Context) -> tuple[PipelineCtx, ProjectCtx]:
    """If we have a job_id but no pipeline_id, fetch the job to get its pipeline."""
    pipeline = PipelineCtx.read(ctx)
    project = ProjectCtx.read(ctx)
    if not pipeline.job_id or pipeline.id:
        return pipeline, project
    project_id = _detect_project_id_for_api(ctx)
    if not project_id:
        return pipeline, project

    raw = _run_glab("api", f"projects/{project_id}/jobs/{pipeline.job_id}")
    if not raw:
        return pipeline, project
    data = _parse_json(raw, ctx, "Job API")
    if data is None:
        return pipeline, project

    job_pipeline = data.get("pipeline", {})
    pipeline = PipelineCtx(
        id=pipeline.id or str(job_pipeline.get("id", "")),
        url=pipeline.url or str(job_pipeline.get("web_url", "")),
        job_id=pipeline.job_id,
        job_name=pipeline.job_name or data.get("name", ""),
    )
    if not project.id:
        proj = data.get("project", {})
        project.id = str(proj.get("id", "")) if proj else ""
    ctx.detection_sources.append("job-api")
    return pipeline, project


def _resolve_pipeline_to_mr(ctx: Context) -> tuple[PipelineCtx, MrCtx]:
    """If we have a pipeline_id but no MR, check if the pipeline is associated with a MR."""
    pipeline = PipelineCtx.read(ctx)
    mr = MrCtx.read(ctx)
    if not pipeline.id or mr.iid:
        return pipeline, mr
    project_id = _detect_project_id_for_api(ctx)
    if not project_id:
        return pipeline, mr

    raw = _run_glab("api", f"projects/{project_id}/pipelines/{pipeline.id}")
    if not raw:
        return pipeline, mr
    data = _parse_json(raw, ctx, "Pipeline API")
    if data is None:
        return pipeline, mr

    pipeline_ref = data.get("ref", "")
    pipeline = replace(pipeline, url=pipeline.url or data.get("web_url", ""))
    ctx.detection_sources.append("pipeline-api")

    # Check if ref is a MR ref (refs/merge-requests/NNN/head) → extract MR IID directly
    mr_ref_match = re.match(r"refs/merge-requests/(\d+)/head", pipeline_ref)
    if mr_ref_match:
        # The MR fields are re-detected from the MR API downstream.
        ctx.detection_sources.append("pipeline-mr-ref")
        return pipeline, MrCtx(iid=mr_ref_match.group(1))

    # Otherwise, set source_branch and try to find MR by branch name
    source_branch = mr.source_branch or pipeline_ref
    mr = replace(mr, source_branch=source_branch)
    if source_branch:
        raw = _run_glab(
            "api",
            f"projects/{project_id}/merge_requests?mr_source_branch={source_branch}&state=opened&per_page=1",
        )
        if raw:
            mrs = _parse_json(raw, ctx, "pipeline MR lookup")
            if mrs:
                parsed = Mr.from_api(mrs[0])
                mr = MrCtx(
                    iid=_mr_str_iid(parsed),
                    title=parsed.title,
                    url=parsed.web_url,
                    source_branch=source_branch,
                    target_branch=parsed.target_branch,
                )
                ctx.detection_sources.append("pipeline-mr-lookup")

    return pipeline, mr


def _detect_issue_details(ctx: Context) -> tuple[IssueCtx, EpicCtx]:
    """Fetch issue details via API if we have issue_iid but missing fields."""
    issue = IssueCtx.read(ctx)
    epic = EpicCtx.read(ctx)
    if not issue.iid or not ctx.project_id:
        return issue, epic
    if issue.title and issue.url and epic.iid:
        return issue, epic

    raw = _run_glab("api", f"projects/{ctx.project_id}/issues/{issue.iid}")
    if not raw:
        return issue, epic
    data = _parse_json(raw, ctx, "Issue API")
    if data is None:
        return issue, epic
    issue = _merge_issue(issue, data)
    epic = _extract_epic(epic, data)
    ctx.detection_sources.append("glab-api-issue")
    return issue, epic


def _detect_epic_details(ctx: Context) -> EpicCtx:
    """Fetch epic description and labels via group epics API if we have epic_iid."""
    epic = EpicCtx.read(ctx)
    if not epic.iid or epic.description:
        return epic
    # The epic URL contains the group path: /groups/pysae/-/epics/259
    # Extract group from epic_url or fall back to project_path parent
    group_path = ""
    if epic.url:
        match = re.search(r"gitlab\.com/groups/(.+?)/-/epics/", epic.url)
        if match:
            group_path = match.group(1)
    if not group_path and ctx.project_path:
        # Use the top-level group from project_path (e.g. "pysae/api" -> "pysae")
        group_path = ctx.project_path.split("/")[0]
    if not group_path:
        return epic

    encoded_group = group_path.replace("/", "%2F")
    raw = _run_glab("api", f"groups/{encoded_group}/epics/{epic.iid}")
    if not raw:
        return epic
    data = _parse_json(raw, ctx, "Epic API")
    if data is None:
        return epic
    epic = EpicCtx(
        iid=epic.iid,
        title=epic.title,
        description=epic.description or data.get("description", ""),
        labels=epic.labels or data.get("labels", []),
        url=epic.url or data.get("web_url", ""),
    )
    ctx.detection_sources.append("glab-api-epic")
    return epic


def _detect_issue_mr(ctx: Context) -> MrCtx:
    """If we have an issue but no MR, try to find a related MR."""
    mr = MrCtx.read(ctx)
    if mr.iid or not ctx.issue_iid or not ctx.project_id:
        return mr

    raw = _run_glab("api", f"projects/{ctx.project_id}/issues/{ctx.issue_iid}/related_merge_requests")
    if raw:
        mrs = _parse_json(raw, ctx, "issue related_merge_requests API")
        if mrs:
            open_mrs = [item for item in mrs if item.get("state") == "opened"]
            chosen = open_mrs[0] if open_mrs else mrs[0]
            ctx.detection_sources.append("issue-related-mr")
            return _mr_from_related(chosen)

    # Fallback: closed_by
    raw = _run_glab("api", f"projects/{ctx.project_id}/issues/{ctx.issue_iid}/closed_by")
    if raw:
        mrs = _parse_json(raw, ctx, "issue closed_by API")
        if mrs:
            ctx.detection_sources.append("issue-closed-by-mr")
            return _mr_from_related(mrs[0])

    return mr


def _mr_from_related(data: dict[str, Any]) -> MrCtx:
    """Build the MR sub-model from an issue-related MR list item (subset of fields)."""
    parsed = Mr.from_api(data)
    return MrCtx(
        iid=_mr_str_iid(parsed),
        title=parsed.title,
        url=parsed.web_url,
        source_branch=parsed.source_branch,
        target_branch=parsed.target_branch,
    )


def _apply_overrides(ctx: Context, args: DetectArgs) -> None:
    """Apply explicit CLI overrides (--mr-iid, --issue-iid, or positional refs).

    This is the explicit-input layer, not a detector: it writes user-provided
    values straight onto the context and clears the fields that must be
    re-detected from them.
    """
    # Parse positional refs first (e.g. "!42", "#123", URLs)
    if args.refs:
        ref = parse_gitlab_refs(" ".join(args.refs))
        if ref.mr_iid and not args.mr_iid:
            args.mr_iid = ref.mr_iid
        if ref.issue_iid and not args.issue_iid:
            args.issue_iid = ref.issue_iid
        if ref.job_id:
            ctx.job_id = ref.job_id
            ctx.detection_sources.append("cli-ref-job")
        if ref.pipeline_id:
            ctx.pipeline_id = ref.pipeline_id
            ctx.detection_sources.append("cli-ref-pipeline")
        if ref.project_path:
            ctx.project_path = ref.project_path
            ctx.project_url = f"https://gitlab.com/{ref.project_path}"
            # Resolve project_id from path so it takes priority over local repo detection
            raw = _run_glab("api", f"projects/{ref.project_path.replace('/', '%2F')}")
            if raw:
                data = _parse_json(raw, ctx, "project resolve API")
                if data is not None:
                    ctx.project_id = str(data.get("id", ""))
                    ctx.default_branch = ctx.default_branch or data.get("default_branch", "")
            ctx.detection_sources.append("cli-ref-project")

    if args.job_id:
        ctx.job_id = args.job_id
        ctx.detection_sources.append("cli-job-id")

    if args.pipeline_id:
        ctx.pipeline_id = args.pipeline_id
        ctx.detection_sources.append("cli-pipeline-id")

    if args.mr_iid:
        ctx.mr_iid = args.mr_iid
        # Clear derived fields that need re-detection
        MrCtx(iid=args.mr_iid).write(ctx)
        ctx.detection_sources.append("cli-mr-iid")

    if args.issue_iid:
        ctx.issue_iid = args.issue_iid
        IssueCtx(iid=args.issue_iid).write(ctx)
        ctx.detection_sources.append("cli-issue-iid")


def _cache_key(cwd: str) -> str:
    """Return a stable filename-safe hash for the given working directory."""
    return hashlib.sha256(cwd.encode()).hexdigest()[:16]


def _cache_path(cwd: str) -> Path:
    """Return the cache file path for the given working directory."""
    return CACHE_DIR / f"{_cache_key(cwd)}.json"


def _read_cache(cwd: str, *, local_only: bool) -> dict[str, object] | None:
    """Read cached context for cwd.

    Returns None if:
    - cache file is missing or unreadable
    - cache is older than TTL (5 min)
    - local_only=False but cache was generated with local=True (incomplete data)
    """
    path = _cache_path(cwd)
    if not path.exists():
        return None
    age = time.time() - path.stat().st_mtime
    if age > CACHE_TTL_SECONDS:
        return None
    try:
        data: dict[str, object] = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    # If caller wants full context but cache was generated in local mode, reject
    cached_local = data.get("_cache_local", False)
    if not local_only and cached_local:
        return None
    return data


def _write_cache(cwd: str, output: dict[str, object], *, local_only: bool) -> None:
    """Write context output to cache file, including the generation mode."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = _cache_path(cwd)
    to_write = {**output, "_cache_local": local_only}
    try:
        path.write_text(json.dumps(to_write, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass


def detect(args: DetectArgs) -> Context:
    """Run the full detection pipeline and return the context.

    With --local: only CI env vars + git (no glab API calls).
    """
    local_only = args.local
    ctx = Context()

    # 1. CI env vars (fast, no subprocess)
    ci = _detect_ci(ctx)
    ctx.is_ci = ci.is_ci
    ci.project.write(ctx)
    ci.pipeline.write(ctx)
    ci.mr.write(ctx)

    # 2. Apply explicit overrides (includes ref parsing)
    _apply_overrides(ctx, args)

    # 3. Git ref parsing (for detached HEAD in CI)
    git, mr, project = _detect_from_git_ref(ctx)
    git.write(ctx)
    mr.write(ctx)
    project.write(ctx)

    # When a URL provides an explicit project (cli-ref-project), skip local repo
    # detection — the target project differs from the current working directory.
    cross_project = "cli-ref-project" in ctx.detection_sources

    if not local_only:
        # 4. glab CLI detection (project + MR from current branch) — skip for cross-project refs
        if not cross_project:
            project, mr = _detect_from_glab(ctx)
            project.write(ctx)
            mr.write(ctx)

        # 5. Chained resolution: job -> pipeline -> MR (needs project_id from steps 1-4)
        pipeline, project = _resolve_job_to_pipeline(ctx)
        pipeline.write(ctx)
        project.write(ctx)
        pipeline, mr = _resolve_pipeline_to_mr(ctx)
        pipeline.write(ctx)
        mr.write(ctx)

        # 6. If issue provided but no MR, find related MR
        if ctx.issue_iid and not ctx.mr_iid:
            _detect_issue_mr(ctx).write(ctx)

        # 7. Fetch missing MR details
        _detect_mr_details(ctx).write(ctx)

        # 8. Detect linked issue from MR
        issue, epic = _detect_linked_issue(ctx)
        issue.write(ctx)
        epic.write(ctx)

        # 9. Fetch missing issue details (also extracts epic from issue response)
        issue, epic = _detect_issue_details(ctx)
        issue.write(ctx)
        epic.write(ctx)

        # 10. Fetch epic details (description, labels) if epic_iid was found
        _detect_epic_details(ctx).write(ctx)

    # 11. Fallback for mr_target_branch
    if not ctx.mr_target_branch:
        ctx.mr_target_branch = ctx.default_branch or "main"

    # 12. Issue-tracking provider + owner, derived from the repo identity. The
    # provider comes from the URL host; without a URL we keep the GitLab default.
    if ctx.project_url:
        ctx.issue_provider = platform_for_url(ctx.project_url).value
    elif ctx.project_path:
        ctx.issue_provider = Platform.GITLAB.value
    if ctx.project_path and "/" in ctx.project_path:
        ctx.owner = ctx.project_path.split("/", 1)[0]

    # NOTE: per-repo *config* (the .pysae-ai-tools.yaml, Slack routing, domain labels)
    # is deliberately NOT resolved here — that stable data lives behind the `project`
    # commands (`project show` / `project list`). detect-context stays purely the
    # *dynamic* branch context (MR, issue, epic, CI), so it is always resolved live.

    return ctx


def main(
    refs: Annotated[
        list[str] | None, typer.Argument(help="GitLab refs: !IID, #IID, MR/issue/job/pipeline URLs")
    ] = None,
    mr_iid: Annotated[str, typer.Option("--mr-iid", help="Explicit MR IID override")] = "",
    issue_iid: Annotated[str, typer.Option("--issue-iid", help="Explicit issue IID override")] = "",
    job_id: Annotated[str, typer.Option("--job-id", help="Job ID (resolves to pipeline -> MR -> issue)")] = "",
    pipeline_id: Annotated[str, typer.Option("--pipeline-id", help="Pipeline ID (resolves to MR -> issue)")] = "",
    local: Annotated[bool, typer.Option("--local", help="Skip glab API calls, use only git + CI env vars")] = False,
    full: Annotated[bool, typer.Option("--full", help="Include empty fields in output (default: omit them)")] = False,
    cached: Annotated[
        bool,
        typer.Option("--cached", help="Return cached context for current cwd (refresh if >5min stale)"),
    ] = False,
) -> None:
    """Detect CI/local mode, MR, and issue context."""
    cwd = os.getcwd()

    # --cached: serve from cache if fresh and mode-compatible, otherwise refresh
    if cached:
        cached_data = _read_cache(cwd, local_only=local)
        if cached_data is not None:
            # Strip internal cache metadata before output
            cached_data.pop("_cache_local", None)
            json.dump(cached_data, sys.stdout, indent=2)
            sys.stdout.write("\n")
            return
        # Cache miss, stale, or wrong mode — run detection with requested mode

    args = DetectArgs(
        refs=refs or [],
        mr_iid=mr_iid,
        issue_iid=issue_iid,
        job_id=job_id,
        pipeline_id=pipeline_id,
        local=local,
    )

    ctx = detect(args)
    output = asdict(ctx)

    if not full:
        output = {k: v for k, v in output.items() if v}

    # Write cache for future --cached calls
    _write_cache(cwd, output, local_only=local)

    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")
