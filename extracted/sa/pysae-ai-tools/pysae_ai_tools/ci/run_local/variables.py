"""Build the job environment: predefined ``CI_*`` + group/project + YAML vars.

Precedence (lowest → highest), matching GitLab's documented order for the
subset we reconstruct locally::

    predefined < YAML global < YAML job < group (parent→child) < project < CLI

Values are then expanded for ``$VAR`` / ``${VAR}`` cross-references (GitLab
expands variable *values* before the job runs; we must do it ourselves because
the generated ``env.sh`` single-quotes values, so bash won't expand them).
"""

import re
import subprocess
from urllib.parse import quote, urlsplit

from ...internal.detect_context.detect import Context
from ..common.glab import glab_api
from .models import CiVariable, EnvResult

_VAR_TOKEN = re.compile(r"\$(\$|\{[A-Za-z_][A-Za-z0-9_]*\}|[A-Za-z_][A-Za-z0-9_]*)")
_MAX_EXPANSION_PASSES = 10


def _slug(value: str, *, max_len: int = 63) -> str:
    """GitLab ``*_SLUG`` form: lowercase, non-alphanumerics → ``-``, trimmed."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:max_len].strip("-")


def _git(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def expand_value(value: str, env: dict[str, str]) -> str:
    """Expand ``$VAR`` / ``${VAR}`` against ``env`` (one pass).

    ``$$`` collapses to a literal ``$``. An undefined reference is left intact
    so we never silently blank out something that may resolve at runtime.
    """

    def repl(match: re.Match[str]) -> str:
        token = match.group(1)
        if token == "$":
            return "$"
        name = token[1:-1] if token.startswith("{") else token
        if name in env:
            return env[name]
        return match.group(0)

    return _VAR_TOKEN.sub(repl, value)


def _expand_all(env: dict[str, str], raw_keys: set[str]) -> dict[str, str]:
    """Fixpoint-expand cross-references among variables (skipping ``raw`` ones)."""
    current = dict(env)
    for _ in range(_MAX_EXPANSION_PASSES):
        nxt = {k: (v if k in raw_keys else expand_value(v, current)) for k, v in current.items()}
        if nxt == current:
            break
        current = nxt
    return current


def predefined(ctx: Context, job_name: str, stage: str, workdir: str, pipeline_id: str = "") -> dict[str, str]:
    """Synthesize the predefined ``CI_*`` variables from the detected context."""
    server_url = ""
    server_host = "gitlab.com"
    if ctx.project_url:
        parts = urlsplit(ctx.project_url)
        if parts.scheme and parts.netloc:
            server_url = f"{parts.scheme}://{parts.netloc}"
            server_host = parts.netloc

    registry = "registry.gitlab.com" if server_host.endswith("gitlab.com") else f"registry.{server_host}"
    branch = ctx.mr_source_branch or ctx.git_branch or ctx.default_branch
    project_path = ctx.project_path
    project_name = project_path.rsplit("/", 1)[-1] if project_path else ""
    namespace = project_path.rsplit("/", 1)[0] if "/" in project_path else ""

    env: dict[str, str] = {
        "CI": "true",
        "GITLAB_CI": "true",
        "CI_PROJECT_DIR": workdir,
        "CI_PROJECT_ID": ctx.project_id,
        "CI_PROJECT_PATH": project_path,
        "CI_PROJECT_NAME": project_name,
        "CI_PROJECT_NAMESPACE": namespace,
        "CI_PROJECT_PATH_SLUG": _slug(project_path),
        "CI_PROJECT_URL": ctx.project_url,
        "CI_DEFAULT_BRANCH": ctx.default_branch,
        "CI_JOB_NAME": job_name,
        "CI_JOB_STAGE": stage,
        "CI_PIPELINE_SOURCE": "merge_request_event" if ctx.mr_iid else "push",
        "CI_PIPELINE_ID": pipeline_id or ctx.pipeline_id,
    }
    if server_url:
        env["CI_SERVER_URL"] = server_url
        env["CI_SERVER_HOST"] = server_host
        env["CI_API_V4_URL"] = f"{server_url}/api/v4"
    env["CI_REGISTRY"] = registry
    if project_path:
        env["CI_REGISTRY_IMAGE"] = f"{registry}/{project_path}"
    if ctx.git_sha:
        env["CI_COMMIT_SHA"] = ctx.git_sha
        env["CI_COMMIT_SHORT_SHA"] = ctx.git_sha[:8]
    if branch:
        env["CI_COMMIT_REF_NAME"] = branch
        env["CI_COMMIT_BRANCH"] = "" if ctx.mr_iid else branch
        env["CI_COMMIT_REF_SLUG"] = _slug(branch)
    if ctx.mr_iid:
        env["CI_MERGE_REQUEST_IID"] = ctx.mr_iid
        env["CI_MERGE_REQUEST_SOURCE_BRANCH_NAME"] = ctx.mr_source_branch
        env["CI_MERGE_REQUEST_TARGET_BRANCH_NAME"] = ctx.mr_target_branch
        env["CI_MERGE_REQUEST_TITLE"] = ctx.mr_title

    user_email = _git("config", "user.email")
    user_name = _git("config", "user.name")
    if user_email:
        env["GITLAB_USER_EMAIL"] = user_email
    if user_name:
        env["GITLAB_USER_NAME"] = user_name

    return {k: v for k, v in env.items() if v != ""}


def _parse_api_vars(data: object, source: str, warnings: list[str] | None = None) -> list[CiVariable]:
    if not isinstance(data, list):
        return []
    out: list[CiVariable] = []
    for entry in data:
        if not isinstance(entry, dict):
            continue
        key = entry.get("key")
        if not isinstance(key, str):
            continue
        if warnings is not None and entry.get("variable_type") == "file":
            warnings.append(
                f"Variable '{key}' is a file-type CI/CD variable — GitLab exposes it as a path to a temp file; "
                "here it carries the raw content. A script using it as a path may behave differently."
            )
        out.append(
            CiVariable(
                key=key,
                value=str(entry.get("value", "") or ""),
                source=source,
                environment_scope=str(entry.get("environment_scope", "*") or "*"),
                masked=bool(entry.get("masked", False)),
                protected=bool(entry.get("protected", False)),
                raw=bool(entry.get("raw", False)),
            )
        )
    return out


def _ancestor_groups(project_path: str) -> list[str]:
    """Ancestor group paths of a project, ordered parent → child."""
    segments = project_path.split("/")
    if len(segments) < 2:
        return []
    groups: list[str] = []
    for i in range(1, len(segments)):
        groups.append("/".join(segments[:i]))
    return groups


_PER_PAGE = 100
_MAX_PAGES = 50  # safety bound (5000 variables) against a pagination bug


def _fetch_all_vars(path: str, source: str, warnings: list[str]) -> list[CiVariable] | None:
    """Fetch every page of a CI/CD variables endpoint. ``None`` on API failure."""
    out: list[CiVariable] = []
    for page in range(1, _MAX_PAGES + 1):
        data = glab_api(f"{path}?per_page={_PER_PAGE}&page={page}")
        if data is None:
            return None
        if not isinstance(data, list) or not data:
            break
        out.extend(_parse_api_vars(data, source, warnings))
        if len(data) < _PER_PAGE:
            break
    return out


def fetch_group_vars(project_path: str, scope: str, warnings: list[str]) -> list[CiVariable]:
    """Group CI/CD variables for every ancestor group, parent → child order."""
    collected: list[CiVariable] = []
    for group in _ancestor_groups(project_path):
        vars_ = _fetch_all_vars(f"groups/{quote(group, safe='')}/variables", f"group:{group}", warnings)
        if vars_ is None:
            warnings.append(f"Could not read group variables for '{group}' (insufficient access?) — skipped.")
            continue
        collected.extend(vars_)
    return _filter_scope(collected, scope)


def fetch_project_vars(project_id: str, scope: str, warnings: list[str]) -> list[CiVariable]:
    """Project-level CI/CD variables."""
    vars_ = _fetch_all_vars(f"projects/{project_id}/variables", "project", warnings)
    if vars_ is None:
        warnings.append("Could not read project variables (insufficient access?) — skipped.")
        return []
    return _filter_scope(vars_, scope)


def _filter_scope(variables: list[CiVariable], scope: str) -> list[CiVariable]:
    return [v for v in variables if v.environment_scope in ("*", scope)]


def build_env(
    *,
    predefined_vars: dict[str, str],
    yaml_global: dict[str, str],
    yaml_job: dict[str, str],
    group_vars: list[CiVariable],
    project_vars: list[CiVariable],
    cli_vars: dict[str, str],
) -> EnvResult:
    """Fold every layer in precedence order, then expand cross-references."""
    result = EnvResult()
    raw_keys: set[str] = set()

    def apply(items: dict[str, str], source: str) -> None:
        for key, value in items.items():
            result.env[key] = value
            result.provenance[key] = source

    def apply_vars(items: list[CiVariable]) -> None:
        for var in items:
            result.env[var.key] = var.value
            result.provenance[var.key] = var.source
            if var.raw:
                raw_keys.add(var.key)
            else:
                raw_keys.discard(var.key)

    apply(predefined_vars, "predefined")
    apply(yaml_global, "yaml-global")
    apply(yaml_job, "yaml-job")
    apply_vars(group_vars)
    apply_vars(project_vars)
    apply(cli_vars, "cli")

    result.env = _expand_all(result.env, raw_keys)
    return result
